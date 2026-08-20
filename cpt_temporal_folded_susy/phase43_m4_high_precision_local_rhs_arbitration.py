#!/usr/bin/env python3
"""Phase 43 -- frozen-state high-precision local RHS arbitration.

This executable consumes the separately committed Phase-43 manifest, the
committed Phase-42 raw result, and the committed Phase-42 checkpoint.  It
does not solve a root or integrate an ODE.  At the ninety stored local
``(xi, q)`` slots it compares the byte-pinned NumPy64 variational RHS against
an independently reconstructed exact SymPy action and fixed mpmath
finite-difference ladders.

The program writes no files.  Progress goes to stderr and exactly one finite
``RESULT_JSON=`` record goes to stdout, including on ``INVALID_RUN``.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import ast
import dataclasses
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Mapping, Sequence

import mpmath
import numpy as np
import scipy
import sympy as sp
from mpmath import mp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.resolve()
MANIFEST_PATH = SCRIPT_PATH.with_name(
    "PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_INPUTS.json"
)
PHASE42_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json"
)
CHECKPOINT_PATH = SCRIPT_PATH.with_name("PHASE42_M4_FIXED_ROOT_CHECKPOINT.json")
PHASE41_PATH = SCRIPT_PATH.with_name("phase41_m4_two_source_intersection.py")

MANIFEST_COMMIT = "91a15d9a8d0c000e1ce7c7d8d83f399b600cff55"
MANIFEST_SHA256 = (
    "de2c8c130e1aae6b6b93ee4c3d1137357067f9ddd5e8c68916037f2ffc325b39"
)
RESULT_SCHEMA = "ice-phase43-high-precision-local-rhs-arbitration/v1"
PHASE42_RESULT_SCHEMA = "ice-phase42-fixed-root-tangent-disentanglement/v1"
CHECKPOINT_SCHEMA = "ice-phase42-fixed-root-checkpoint/v1"
RESULT_PREFIX = "RESULT_JSON="

TARGETS = ("shared_zero", "phi_plus", "a_plus")
FRACTION_STRINGS = ("0", "0.25", "0.5", "0.75", "1")
DIRECTIONS = tuple(range(6))
PRECISIONS = (80, 120)
NORMALIZATION_MODES = (
    "lifted_binary64_geometry",
    "native_mpmath_geometry",
)
SAME_EPSILON_STRINGS = ("2e-5", "1e-5", "5e-6")
PROSPECTIVE_H_STRINGS = (
    "1e-6",
    "1e-8",
    "1e-10",
    "1e-12",
    "1e-14",
    "1e-16",
)
PROSPECTIVE_OFFSETS = ("h", "h/2", "-h/2", "-h")

EXACT_IDS = (
    "P43.freeze.committed_artifacts_runner_and_environment",
    "P43.input.strict_phase42_state_identity",
    "P43.scope.local_only_no_solver_or_time_column",
    "P43.symbolic.independent_action_and_directional_identity",
    "P43.math.binary64_lift_precision_ladders_and_metrics",
    "P43.retention.complete_slot_and_classification_schema",
    "P43.guard.fail_closed_gate1_and_null_outputs",
)
NUMERICAL_IDS = (
    "P43.reproduction.phase42_local_source_controls",
    "P43.reference.independent_symbolic_and_precision_agreement",
    "P43.reference.same_step_and_small_step_R4",
    "P43.arbitration.source_RHS_implementation",
    "P43.arbitration.phase42_stable_violations",
    "P43.classification.complete_nonexclusive_local_ledger",
)


class InvalidRun(RuntimeError):
    """Infrastructure, provenance, exact, or retention contract failure."""


class SlotEvaluationError(RuntimeError):
    """A declared scientific slot failed without invalidating infrastructure."""

    def __init__(self, message: str, *, payload: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.payload = dict(payload or {})


class DuplicateJSONKey(InvalidRun):
    """A strict JSON object repeated a key."""


def progress(message: str) -> None:
    try:
        print(f"[Phase43] {message}", file=sys.stderr, flush=True)
    except Exception:
        # Diagnostic stderr must never suppress the one fail-closed stdout record.
        pass


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
        value = json.loads(
            raw.decode("utf-8"),
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
    path: Path,
    expected_sha: str,
    *,
    label: str,
    expected_size: int | None = None,
) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != expected_sha:
        raise InvalidRun(
            f"{label} SHA drift: expected {expected_sha}, observed {observed}"
        )
    if expected_size is not None and len(raw) != expected_size:
        raise InvalidRun(f"{label} byte-length drift")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise InvalidRun(f"{label} must end in exactly one LF")
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


def raw_git_observation(*arguments: str, binary: bool = False) -> dict[str, Any]:
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


def relative_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError as exc:
        raise InvalidRun(f"path is outside repository: {path}") from exc


def verify_file_pin(path: Path, commit: str, expected_sha: str) -> dict[str, Any]:
    rel = relative_repo_path(path)
    raw = path.read_bytes()
    if sha256_bytes(raw) != expected_sha:
        raise InvalidRun(f"byte drift for {rel}")
    committed = subprocess.run(
        ["git", "show", f"{commit}:{rel}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if committed.returncode != 0:
        raise InvalidRun(f"cannot read committed pin {commit}:{rel}")
    if committed.stdout != raw or sha256_bytes(committed.stdout) != expected_sha:
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
        "sha256": expected_sha,
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


def repository_worktree_snapshot() -> list[dict[str, Any]]:
    """Hash all tracked and nonignored untracked files without mutating them."""
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise InvalidRun(
            "cannot enumerate worktree snapshot: "
            + completed.stderr.decode(errors="replace").strip()
        )
    records: list[dict[str, Any]] = []
    decoded: list[str] = []
    for raw_path in completed.stdout.split(b"\0"):
        if not raw_path:
            continue
        try:
            decoded.append(raw_path.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise InvalidRun("non-UTF8 path in worktree snapshot") from exc
    for relative in sorted(set(decoded)):
        path = REPO_ROOT / relative
        if path.is_symlink():
            records.append(
                {"path": relative, "kind": "symlink", "target": os.readlink(path)}
            )
            continue
        if not path.is_file():
            raise InvalidRun(f"enumerated path is not a file: {relative}")
        raw = path.read_bytes()
        records.append(
            {
                "path": relative,
                "kind": "file",
                "size": len(raw),
                "sha256": sha256_bytes(raw),
            }
        )
    return records


def source_pin_specs(manifest: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    artifacts = manifest["immutable_artifacts"]
    entries: dict[str, Mapping[str, Any]] = {
        "manifest": {
            "path": relative_repo_path(MANIFEST_PATH),
            "commit": MANIFEST_COMMIT,
            "sha256": MANIFEST_SHA256,
        },
        "phase42_result": artifacts["phase42_raw_result"],
        "phase42_checkpoint": artifacts["phase42_checkpoint"],
        "phase42_manifest": artifacts["phase42_input_manifest"],
        "phase42_runner": artifacts["phase42_runner"],
        "phase42_report": artifacts["phase42_report"],
        "phase41_script": artifacts["phase41_executable"],
        "phase41_manifest": artifacts["phase41_input_manifest"],
        "pyproject": artifacts["dependency_locks"]["pyproject"],
        "uv_lock": artifacts["dependency_locks"]["uv_lock"],
    }
    result: dict[str, dict[str, str]] = {}
    for name, entry in entries.items():
        sha = entry.get("sha256", entry.get("outer_file_sha256_including_final_LF"))
        if not isinstance(sha, str):
            raise InvalidRun(f"missing SHA pin for {name}")
        result[name] = {
            "path": str(entry["path"]),
            "commit": str(entry["commit"]),
            "sha256": sha,
        }
    return result


def verify_source_closure(manifest: Mapping[str, Any]) -> dict[str, Any]:
    files = {
        name: verify_file_pin(
            REPO_ROOT / pin["path"], pin["commit"], pin["sha256"]
        )
        for name, pin in source_pin_specs(manifest).items()
    }
    return {"git_HEAD": git_output("rev-parse", "HEAD"), "files": files}


def observe_source_closure_raw(
    manifest: Mapping[str, Any] | None,
) -> dict[str, Any]:
    head = raw_git_observation("rev-parse", "HEAD")
    output: dict[str, Any] = {
        "git_HEAD": head["stdout"] if head["ok"] else None,
        "git_HEAD_observation_error": None if head["ok"] else head["stderr"],
        "files": {},
    }
    if manifest is None:
        output["pin_schema_error"] = "manifest unavailable"
        return output
    try:
        specs = source_pin_specs(manifest)
    except Exception as exc:
        output["pin_schema_error"] = f"{type(exc).__name__}: {exc}"[:2048]
        return output
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
        blob = raw_git_observation(
            "show", f"{pin['commit']}:{pin['path']}", binary=True
        )
        blob_raw = blob["stdout"] if blob["ok"] else None
        ancestor = raw_git_observation(
            "merge-base", "--is-ancestor", pin["commit"], "HEAD"
        )
        output["files"][name] = {
            "path": pin["path"],
            "expected_commit": pin["commit"],
            "expected_sha256": pin["sha256"],
            "observed_sha256": observed_sha,
            "current_sha_matches_expected": observed_sha == pin["sha256"],
            "current_byte_observation_error": byte_error,
            "expected_commit_blob_sha256": (
                sha256_bytes(blob_raw) if isinstance(blob_raw, bytes) else None
            ),
            "expected_commit_blob_matches_current_bytes": bool(
                raw is not None and isinstance(blob_raw, bytes) and raw == blob_raw
            ),
            "expected_commit_is_ancestor_of_HEAD": bool(ancestor["ok"]),
            "blob_observation_error": None if blob["ok"] else blob["stderr"],
            "ancestor_observation_error": (
                None if ancestor["ok"] else ancestor["stderr"]
            ),
        }
    return output


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
        raise InvalidRun("Phase43 runner must be committed before production")
    if git_output("status", "--porcelain=v1", "--", rel):
        raise InvalidRun("Phase43 runner path is dirty")
    latest = git_output("log", "-1", "--format=%H", "--", rel)
    if not latest or latest == MANIFEST_COMMIT:
        raise InvalidRun("runner was not committed after the Stage-1 manifest")
    raw = SCRIPT_PATH.read_bytes()
    committed = subprocess.run(
        ["git", "show", f"{latest}:{rel}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if committed.returncode != 0 or committed.stdout != raw:
        raise InvalidRun("runner differs from its latest committed blob")
    for ancestor, descendant, label in (
        (latest, "HEAD", "runner commit is not an ancestor of HEAD"),
        (
            MANIFEST_COMMIT,
            latest,
            "runner commit does not descend from Stage-1 manifest",
        ),
    ):
        check = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if check.returncode != 0:
            raise InvalidRun(label)
    return {
        "path": rel,
        "observed_sha256": sha256_bytes(raw),
        "observed_size_bytes": len(raw),
        "git_tracked": True,
        "git_clean_for_path": True,
        "latest_path_commit": latest,
        "latest_commit_blob_sha256": sha256_bytes(committed.stdout),
        "latest_commit_blob_matches_current_bytes": True,
        "latest_path_commit_is_ancestor_of_HEAD": True,
        "manifest_commit_is_ancestor_of_runner_commit": True,
    }


def observe_runner_provenance_raw() -> dict[str, Any]:
    try:
        rel = SCRIPT_PATH.resolve().relative_to(REPO_ROOT).as_posix()
    except Exception as exc:
        return {"path": None, "observation_error": f"{type(exc).__name__}: {exc}"}
    try:
        raw = SCRIPT_PATH.read_bytes()
        observed_sha: str | None = sha256_bytes(raw)
        size: int | None = len(raw)
        read_error: str | None = None
    except Exception as exc:
        raw = None
        observed_sha = None
        size = None
        read_error = f"{type(exc).__name__}: {exc}"[:2048]
    tracked = raw_git_observation("ls-files", "--error-unmatch", rel)
    dirty = raw_git_observation("status", "--porcelain=v1", "--", rel)
    latest_record = raw_git_observation("log", "-1", "--format=%H", "--", rel)
    latest = (
        str(latest_record["stdout"])
        if latest_record["ok"] and latest_record["stdout"]
        else None
    )
    blob = (
        raw_git_observation("show", f"{latest}:{rel}", binary=True)
        if latest
        else {"ok": False, "stdout": b"", "stderr": "latest unavailable"}
    )
    blob_raw = blob["stdout"] if blob["ok"] else None
    latest_ancestor = (
        raw_git_observation("merge-base", "--is-ancestor", latest, "HEAD")
        if latest
        else {"ok": False}
    )
    manifest_ancestor = (
        raw_git_observation(
            "merge-base", "--is-ancestor", MANIFEST_COMMIT, latest
        )
        if latest
        else {"ok": False}
    )
    return {
        "path": rel,
        "observed_sha256": observed_sha,
        "observed_size_bytes": size,
        "current_byte_observation_error": read_error,
        "git_tracked": bool(tracked["ok"]),
        "git_clean_for_path": bool(dirty["ok"] and dirty["stdout"] == ""),
        "git_status_porcelain": dirty["stdout"] if dirty["ok"] else None,
        "latest_path_commit": latest,
        "latest_commit_blob_sha256": (
            sha256_bytes(blob_raw) if isinstance(blob_raw, bytes) else None
        ),
        "latest_commit_blob_matches_current_bytes": bool(
            raw is not None and isinstance(blob_raw, bytes) and raw == blob_raw
        ),
        "latest_path_commit_is_ancestor_of_HEAD": bool(latest_ancestor["ok"]),
        "manifest_commit_is_ancestor_of_runner_commit": bool(
            manifest_ancestor["ok"]
        ),
        "runner_commit_is_after_manifest_stage": bool(
            latest is not None and latest != MANIFEST_COMMIT
        ),
    }


def observed_runtime_fingerprint(manifest: Mapping[str, Any]) -> dict[str, Any]:
    expected = manifest["strict_runtime_environment"]["fingerprint"]
    observed = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build": list(platform.python_build()),
        "python_compiler": platform.python_compiler(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "sympy_version": sp.__version__,
        "mpmath_version": mpmath.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "libc": list(platform.libc_ver()),
        "thread_environment": {
            name: os.environ.get(name)
            for name in expected["thread_environment"]
        },
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
    expected_executable = Path(
        manifest["strict_runtime_environment"]["resolved_python_executable"]
    ).resolve()
    observed_executable = Path(sys.executable).resolve()
    if observed_executable != expected_executable:
        raise InvalidRun(
            f"wrong Python executable: {observed_executable} != {expected_executable}"
        )
    required_launch = (
        REPO_ROOT / manifest["strict_runtime_environment"]["launch_executable"]
    ).absolute()
    observed_launch = Path(sys.executable).absolute()
    if observed_launch != required_launch:
        raise InvalidRun(
            "runner was not launched through frozen venv path: "
            f"{observed_launch} != {required_launch}"
        )
    expected_prefix = (REPO_ROOT / ".venv").absolute()
    observed_prefix = Path(sys.prefix).absolute()
    if observed_prefix != expected_prefix:
        raise InvalidRun(
            f"virtual-environment prefix drift: {observed_prefix} != {expected_prefix}"
        )
    if sys.dont_write_bytecode is not True:
        raise InvalidRun("sys.dont_write_bytecode is not true")
    return {
        "verified": True,
        "launch_executable": str(observed_launch),
        "python_executable": str(observed_executable),
        "virtual_environment_prefix": str(observed_prefix),
        "strict_fingerprint": observed,
    }


def start_provenance_guard(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source": verify_source_closure(manifest),
        "runner": observed_runner_provenance(),
        "runtime": observed_runtime_fingerprint(manifest),
        "pycache": repository_pycache_snapshot(),
        "worktree": repository_worktree_snapshot(),
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
        "worktree": repository_worktree_snapshot(),
        "HEAD": git_output("rev-parse", "HEAD"),
    }
    comparisons = {
        key: end[key] == start[key]
        for key in (
            "source",
            "runner",
            "runtime",
            "pycache",
            "worktree",
            "HEAD",
        )
    }
    if not all(comparisons.values()):
        raise InvalidRun(f"pre-emission TOCTOU drift: {comparisons}")
    return {"start": dict(start), "end": end, "comparisons": comparisons}


def canonical_array_bytes(array: np.ndarray) -> tuple[str, bytes]:
    values = np.asarray(array)
    if np.iscomplexobj(values):
        canonical = np.ascontiguousarray(values, dtype=np.dtype("<c16"))
        return "<c16", canonical.tobytes(order="C")
    canonical = np.ascontiguousarray(values, dtype=np.dtype("<f8"))
    return "<f8", canonical.tobytes(order="C")


def decode_complex_pairs(
    value: Any, *, shape: tuple[int, ...], path: str
) -> np.ndarray:
    pairs = np.asarray(value, dtype=np.float64)
    if pairs.shape != shape + (2,):
        raise InvalidRun(f"complex-pair shape mismatch at {path}")
    array = np.empty(shape, dtype=np.complex128)
    array.real[...] = pairs[..., 0]
    array.imag[...] = pairs[..., 1]
    if not np.all(np.isfinite(array.real)) or not np.all(np.isfinite(array.imag)):
        raise InvalidRun(f"nonfinite complex array at {path}")
    return array


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
    if expected_shape is not None and shape != expected_shape:
        raise InvalidRun(f"shape mismatch at {path}: {shape} != {expected_shape}")
    encoding = record.get("complex_encoding")
    if encoding is None:
        array = np.asarray(record["values"], dtype=np.float64)
        expected_runtime = "float64"
        expected_canonical = "<f8"
        if array.shape != shape:
            raise InvalidRun(f"real array shape mismatch at {path}")
    elif encoding == "terminal [real,imag] pairs":
        array = decode_complex_pairs(record["values"], shape=shape, path=path)
        expected_runtime = "complex128"
        expected_canonical = "<c16"
    else:
        raise InvalidRun(f"unknown complex encoding at {path}: {encoding}")
    if str(record["runtime_dtype"]) != expected_runtime:
        raise InvalidRun(f"runtime dtype drift at {path}")
    dtype, raw = canonical_array_bytes(array)
    if dtype != expected_canonical or record["canonical_little_endian_dtype"] != dtype:
        raise InvalidRun(f"canonical dtype drift at {path}")
    if sha256_bytes(raw) != record["canonical_little_endian_sha256"]:
        raise InvalidRun(f"canonical array SHA drift at {path}")
    if not np.all(np.isfinite(array.real)) or (
        np.iscomplexobj(array) and not np.all(np.isfinite(array.imag))
    ):
        raise InvalidRun(f"nonfinite array at {path}")
    return array


def json_ready(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return json_ready(dataclasses.asdict(value))
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            if not np.all(np.isfinite(value.real)) or not np.all(
                np.isfinite(value.imag)
            ):
                raise InvalidRun("nonfinite complex ndarray in result")
            pairs = np.empty(value.shape + (2,), dtype=np.float64)
            pairs[..., 0] = value.real
            pairs[..., 1] = value.imag
            return pairs.tolist()
        if not np.all(np.isfinite(value)):
            raise InvalidRun("nonfinite ndarray in result")
        return value.tolist()
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, complex):
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise InvalidRun("nonfinite complex value in result")
        return [float(value.real), float(value.imag)]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InvalidRun("nonfinite float in result")
        return value
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, child in value.items():
            encoded_key = str(key)
            if encoded_key in output:
                raise InvalidRun(
                    f"JSON key collision after stringification: {encoded_key}"
                )
            output[encoded_key] = json_ready(child)
        return output
    if isinstance(value, (list, tuple)):
        return [json_ready(child) for child in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise InvalidRun(f"cannot serialize value of type {type(value).__name__}")


@dataclass
class Audit:
    exact_records: list[dict[str, Any]] = field(default_factory=list)
    numerical_records: list[dict[str, Any]] = field(default_factory=list)

    def _unique(self, check_id: str) -> None:
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
        self._unique(check_id)
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
        self._unique(check_id)
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
            raise InvalidRun(f"slot completed twice: {key}")
        if status not in {
            "SUCCESS",
            "EVALUATION_FAILED",
            "NOT_RUN_UPSTREAM_INVALID",
        }:
            raise InvalidRun(f"invalid terminal status: {status}")
        encoded_payload = json_ready(payload)
        slot["terminal_status"] = status
        slot["payload"] = encoded_payload
        slot["error"] = error

    def fail_unfinished(self, reason: str) -> None:
        for key, slot in self.slots.items():
            if slot["terminal_status"] is None:
                self.finish(key, "NOT_RUN_UPSTREAM_INVALID", error=reason)

    def assert_complete(self) -> None:
        missing = [
            key for key, slot in self.slots.items()
            if slot["terminal_status"] is None
        ]
        if missing:
            raise InvalidRun(f"unterminated slots: {missing[:8]}")

    def summary(self) -> dict[str, Any]:
        by_kind: dict[str, int] = {}
        by_status: dict[str, int] = {}
        for slot in self.slots.values():
            kind = str(slot["metadata"]["slot_kind"])
            by_kind[kind] = by_kind.get(kind, 0) + 1
            status = str(slot["terminal_status"])
            by_status[status] = by_status.get(status, 0) + 1
        return {
            "declared_total": len(self.slots),
            "by_kind": dict(sorted(by_kind.items())),
            "by_terminal_status": dict(sorted(by_status.items())),
        }


@dataclass(frozen=True)
class FrozenPoint:
    label: str
    delta_a: str
    delta_phi: str
    saddle_w: np.ndarray
    fraction_times: np.ndarray
    fraction_xi: np.ndarray
    fraction_tangents: np.ndarray
    local_records: Mapping[tuple[str, int], Mapping[str, Any]]
    perturbation_records: Mapping[
        tuple[str, int, str, int], Mapping[str, Any]
    ]


@dataclass(frozen=True)
class FrozenContext:
    phase42_result: Mapping[str, Any]
    checkpoint: Mapping[str, Any]
    phase41: ModuleType
    coordinate_scales: np.ndarray
    linear_map: np.ndarray
    points: Mapping[str, FrozenPoint]
    forbidden_call_counter: Mapping[str, int]
    validation: Mapping[str, Any]


@dataclass(frozen=True)
class IndependentFamily:
    w: tuple[sp.Symbol, ...]
    action: sp.Expr
    gradient: sp.Matrix
    hessian: sp.Matrix
    elements: tuple[sp.Expr, ...]
    direct_base: tuple[sp.Symbol, ...]
    direct_direction: tuple[sp.Symbol, ...]
    direct_gradient_derivative: sp.Matrix


@dataclass(frozen=True)
class ReferenceEvaluators:
    exact_family: IndependentFamily
    rounding_family: IndependentFamily
    exact_gradient: Callable[..., Any]
    exact_hessian: Callable[..., Any]
    exact_direct: Callable[..., Any]
    rounding_hessian: Callable[..., Any]
    fingerprints: Mapping[str, Any]


def midpoint_element_independent(
    left_a: sp.Expr,
    left_phi: sp.Expr,
    right_a: sp.Expr,
    right_phi: sp.Expr,
    proper_time: sp.Expr,
    step: sp.Expr,
) -> sp.Expr:
    midpoint_a = (left_a + right_a) / sp.Integer(2)
    midpoint_phi = (left_phi + right_phi) / sp.Integer(2)
    difference_a = right_a - left_a
    difference_phi = right_phi - left_phi
    slope = sp.sqrt(sp.Rational(2, 3))
    potential = sp.Rational(3, 4) * (
        sp.Integer(1) - sp.exp(-slope * midpoint_phi)
    ) ** 2
    return sp.Integer(2) * sp.pi**2 * (
        (
            -sp.Integer(6) * midpoint_a * difference_a**2
            + midpoint_a**3 * difference_phi**2
        )
        / (sp.Integer(2) * proper_time * step)
        + proper_time
        * step
        * (-sp.Integer(3) * midpoint_a + midpoint_a**3 * potential)
    )


def build_independent_family(
    delta_a_text: str,
    delta_phi_text: str,
    *,
    source_rounding_control: bool,
) -> IndependentFamily:
    w = sp.symbols("p43_w_a1 p43_w_phi1 p43_w_a2 p43_w_phi2 p43_w_a3 p43_w_phi3 p43_w_T")
    z = sp.symbols("p43_a1 p43_phi1 p43_a2 p43_phi2 p43_a3 p43_phi3 p43_T")
    if source_rounding_control:
        base_a: sp.Expr = sp.Float("3.5668031935672753", 50)
        base_phi: sp.Expr = sp.Float("1.0185809464006637", 50)
        scale_values: tuple[sp.Expr, ...] = (
            sp.Float("3.5668031935672753", 50),
            sp.Float("1.0185809464006637", 50),
            sp.Float("3.5668031935672753", 50),
            sp.Float("1.0185809464006637", 50),
            sp.Float("3.5668031935672753", 50),
            sp.Float("1.0185809464006637", 50),
            sp.Float("0.7", 50),
        )
        delta_a: sp.Expr = sp.Float(delta_a_text, 50)
        delta_phi: sp.Expr = sp.Float(delta_phi_text, 50)
    else:
        base_a = sp.Rational("3.5668031935672753")
        base_phi = sp.Rational("1.0185809464006637")
        scale_values = (
            sp.Rational("3.5668031935672753"),
            sp.Rational("1.0185809464006637"),
            sp.Rational("3.5668031935672753"),
            sp.Rational("1.0185809464006637"),
            sp.Rational("3.5668031935672753"),
            sp.Rational("1.0185809464006637"),
            sp.Rational("0.7"),
        )
        delta_a = sp.Rational(delta_a_text)
        delta_phi = sp.Rational(delta_phi_text)
    left = (
        base_a * (sp.Integer(1) - delta_a / sp.Integer(2)),
        base_phi - delta_phi / sp.Integer(2),
    )
    right = (
        base_a * (sp.Integer(1) + delta_a / sp.Integer(2)),
        base_phi + delta_phi / sp.Integer(2),
    )
    nodes = (
        left,
        (z[0], z[1]),
        (z[2], z[3]),
        (z[4], z[5]),
        right,
    )
    step = sp.Rational(1, 4)
    elements = tuple(
        midpoint_element_independent(
            nodes[index][0],
            nodes[index][1],
            nodes[index + 1][0],
            nodes[index + 1][1],
            z[-1],
            step,
        )
        for index in range(4)
    )
    action_z = sp.expand(sum(elements, sp.Integer(0)))
    action = action_z.subs(
        {z[index]: scale_values[index] * w[index] for index in range(7)}
    )
    gradient = sp.Matrix([sp.diff(action, variable) for variable in w])
    hessian = sp.hessian(action, w)
    direct_base = sp.symbols("p43_b0:7")
    direct_direction = sp.symbols("p43_d0:7")
    epsilon = sp.Symbol("p43_epsilon", real=True)
    path_substitution = {
        w[index]: direct_base[index] + epsilon * direct_direction[index]
        for index in range(7)
    }
    direct = sp.Matrix(
        [
            sp.diff(gradient[index].subs(path_substitution), epsilon).subs(
                epsilon, sp.Integer(0)
            )
            for index in range(7)
        ]
    )
    return IndependentFamily(
        w=tuple(w),
        action=action,
        gradient=gradient,
        hessian=hessian,
        elements=elements,
        direct_base=tuple(direct_base),
        direct_direction=tuple(direct_direction),
        direct_gradient_derivative=direct,
    )


def audit_reference_source_boundary() -> dict[str, Any]:
    function_names = (
        "midpoint_element_independent",
        "build_independent_family",
        "make_reference_evaluators",
        "finite_mp_vector",
        "reference_flow",
        "reference_hessian_action",
        "reference_direct_action",
    )
    forbidden_names = {
        "phase41",
        "PHASE41_PATH",
        "np",
        "scipy",
        "eval",
        "parse_expr",
        "action_at",
        "gradient_at",
        "hessian_at",
        "flow_xi",
        "hessian_xi",
        "xi_to_w",
        "build_symbolic_family",
        "numeric_model",
        "source_objects",
        "source_analytic_action",
        "source_flow",
        "FrozenContext",
    }
    records: dict[str, Any] = {}
    for name in function_names:
        function = globals().get(name)
        if function is None:
            raise InvalidRun(f"independent reference function missing: {name}")
        source = inspect.getsource(function)
        tree = ast.parse(source)
        observed = sorted(
            {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name) and node.id in forbidden_names
            }
            | {
                node.attr
                for node in ast.walk(tree)
                if isinstance(node, ast.Attribute) and node.attr in forbidden_names
            }
        )
        if observed:
            raise InvalidRun(
                f"independent reference boundary violation in {name}: {observed}"
            )
        records[name] = {
            "source_sha256": sha256_bytes(source.encode("utf-8")),
            "forbidden_references": observed,
        }
    return records


def make_reference_evaluators(
    delta_a_text: str, delta_phi_text: str
) -> ReferenceEvaluators:
    exact = build_independent_family(
        delta_a_text, delta_phi_text, source_rounding_control=False
    )
    rounding = build_independent_family(
        delta_a_text, delta_phi_text, source_rounding_control=True
    )
    if any(isinstance(node, sp.Float) for node in sp.preorder_traversal(exact.action)):
        raise InvalidRun("machine/approximate Float entered exact action tree")
    if len(exact.elements) != 4 or len(exact.w) != 7:
        raise InvalidRun("independent action cardinality drift")
    jacobian_identity = exact.hessian - exact.gradient.jacobian(exact.w)
    symmetry_identity = exact.hessian - exact.hessian.T
    base_substitution = {
        exact.w[index]: exact.direct_base[index] for index in range(7)
    }
    expected_direct = exact.hessian.subs(base_substitution) * sp.Matrix(
        exact.direct_direction
    )
    direct_identity = exact.direct_gradient_derivative - expected_direct
    exact_checks = {
        "hessian_equals_gradient_jacobian": all(
            sp.simplify(value) == 0 for value in jacobian_identity
        ),
        "hessian_symmetric": all(
            sp.simplify(value) == 0 for value in symmetry_identity
        ),
        "direct_gradient_chain_rule": all(
            sp.simplify(value) == 0 for value in direct_identity
        ),
        "four_elements": len(exact.elements) == 4,
        "seven_variables": len(exact.w) == 7,
        "exact_tree_has_no_SymPy_Float": not any(
            isinstance(node, sp.Float)
            for node in sp.preorder_traversal(exact.action)
        ),
    }
    if not all(exact_checks.values()):
        raise InvalidRun(f"independent symbolic identity failed: {exact_checks}")
    exact_gradient = sp.lambdify((exact.w,), exact.gradient, modules="mpmath")
    exact_hessian = sp.lambdify((exact.w,), exact.hessian, modules="mpmath")
    exact_direct = sp.lambdify(
        (exact.direct_base, exact.direct_direction),
        exact.direct_gradient_derivative,
        modules="mpmath",
    )
    rounding_hessian = sp.lambdify(
        (rounding.w,), rounding.hessian, modules="mpmath"
    )
    return ReferenceEvaluators(
        exact_family=exact,
        rounding_family=rounding,
        exact_gradient=exact_gradient,
        exact_hessian=exact_hessian,
        exact_direct=exact_direct,
        rounding_hessian=rounding_hessian,
        fingerprints={
            "exact_action_srepr_sha256": sha256_bytes(
                sp.srepr(exact.action).encode("utf-8")
            ),
            "exact_gradient_srepr_sha256": sha256_bytes(
                sp.srepr(exact.gradient).encode("utf-8")
            ),
            "exact_hessian_srepr_sha256": sha256_bytes(
                sp.srepr(exact.hessian).encode("utf-8")
            ),
            "direct_gradient_srepr_sha256": sha256_bytes(
                sp.srepr(exact.direct_gradient_derivative).encode("utf-8")
            ),
            "rounding_action_srepr_sha256": sha256_bytes(
                sp.srepr(rounding.action).encode("utf-8")
            ),
            "exact_checks": exact_checks,
        },
    )


def mp_from_binary64(value: float) -> mp.mpf:
    number = float(value)
    if not math.isfinite(number):
        raise SlotEvaluationError("cannot lift nonfinite binary64")
    numerator, denominator = number.as_integer_ratio()
    return mp.mpf(numerator) / mp.mpf(denominator)


def mp_complex_from_binary64(value: complex) -> mp.mpc:
    number = complex(value)
    return mp.mpc(
        mp_from_binary64(float(number.real)),
        mp_from_binary64(float(number.imag)),
    )


def mp_vector_from_numpy(value: np.ndarray) -> list[mp.mpc]:
    array = np.asarray(value, dtype=np.complex128).reshape(-1)
    return [mp_complex_from_binary64(complex(item)) for item in array]


def mp_real_matrix_from_numpy(value: np.ndarray) -> mp.matrix:
    array = np.asarray(value, dtype=np.float64)
    return mp.matrix(
        [
            [mp_from_binary64(float(array[row, column])) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def flatten_mp(value: Any, expected: int) -> list[Any]:
    if isinstance(value, mp.matrix):
        output = [value[index] for index in range(len(value))]
    elif isinstance(value, (list, tuple)):
        output = []
        for item in value:
            if isinstance(item, (list, tuple)):
                output.extend(item)
            else:
                output.append(item)
    else:
        raise SlotEvaluationError(
            f"unexpected mpmath evaluator output: {type(value).__name__}"
        )
    if len(output) != expected:
        raise SlotEvaluationError(
            f"mpmath evaluator length {len(output)} != {expected}"
        )
    return output


def matrix_mp(value: Any, rows: int, columns: int) -> mp.matrix:
    if isinstance(value, mp.matrix):
        if value.rows != rows or value.cols != columns:
            raise SlotEvaluationError("mpmath matrix shape drift")
        return value
    flat = flatten_mp(value, rows * columns)
    return mp.matrix(
        [
            flat[row * columns : (row + 1) * columns]
            for row in range(rows)
        ]
    )


def finite_mp_vector(value: Sequence[Any], *, label: str) -> list[mp.mpc]:
    output: list[mp.mpc] = []
    for item in value:
        number = mp.mpc(item)
        if not mp.isfinite(number.real) or not mp.isfinite(number.imag):
            raise SlotEvaluationError(f"nonfinite {label}")
        output.append(number)
    return output


def reference_flow(
    evaluators: ReferenceEvaluators,
    saddle_w: Sequence[Any],
    linear_map: mp.matrix,
    xi: Sequence[Any],
) -> list[mp.mpc]:
    xi_matrix = mp.matrix(list(xi))
    saddle_matrix = mp.matrix(list(saddle_w))
    w_value = saddle_matrix + linear_map * xi_matrix
    gradient = mp.matrix(flatten_mp(evaluators.exact_gradient(tuple(w_value)), 7))
    raw = linear_map.T * gradient
    return finite_mp_vector(
        [mp.mpc(-mp.conj(raw[index])) for index in range(7)],
        label="independent reference flow",
    )


def reference_hessian_action(
    evaluators: ReferenceEvaluators,
    variant: str,
    saddle_w: Sequence[Any],
    linear_map: mp.matrix,
    xi: Sequence[Any],
    q: Sequence[Any],
) -> list[mp.mpc]:
    if variant == "exact":
        hessian_function = evaluators.exact_hessian
    elif variant == "source_rounding_control":
        hessian_function = evaluators.rounding_hessian
    else:
        raise InvalidRun(f"undeclared independent Hessian variant: {variant}")
    xi_matrix = mp.matrix(list(xi))
    q_matrix = mp.matrix(list(q))
    saddle_matrix = mp.matrix(list(saddle_w))
    w_value = saddle_matrix + linear_map * xi_matrix
    hessian = matrix_mp(hessian_function(tuple(w_value)), 7, 7)
    raw = linear_map.T * hessian * linear_map * q_matrix
    return finite_mp_vector(
        [mp.mpc(-mp.conj(raw[index])) for index in range(7)],
        label=f"independent {variant} Hessian action",
    )


def reference_direct_action(
    evaluators: ReferenceEvaluators,
    saddle_w: Sequence[Any],
    linear_map: mp.matrix,
    xi: Sequence[Any],
    q: Sequence[Any],
) -> list[mp.mpc]:
    xi_matrix = mp.matrix(list(xi))
    q_matrix = mp.matrix(list(q))
    saddle_matrix = mp.matrix(list(saddle_w))
    w_value = saddle_matrix + linear_map * xi_matrix
    w_direction = linear_map * q_matrix
    direct_w = mp.matrix(
        flatten_mp(
            evaluators.exact_direct(tuple(w_value), tuple(w_direction)), 7
        )
    )
    raw = linear_map.T * direct_w
    return finite_mp_vector(
        [mp.mpc(-mp.conj(raw[index])) for index in range(7)],
        label="independent direct-gradient action",
    )


def mp_norm(value: Sequence[Any]) -> mp.mpf:
    return mp.sqrt(mp.fsum(abs(item) ** 2 for item in value))


def mp_relative(left: Sequence[Any], right: Sequence[Any]) -> mp.mpf:
    if len(left) != len(right):
        raise SlotEvaluationError("relative metric vector length mismatch")
    difference = mp_norm([left[i] - right[i] for i in range(len(left))])
    denominator = max(mp_norm(left), mp_norm(right), mp.mpf("1e-100"))
    return difference / denominator


def mp_max_component_relative(
    left: Sequence[Any], right: Sequence[Any]
) -> mp.mpf:
    if len(left) != len(right):
        raise SlotEvaluationError(
            "max-component-relative metric vector length mismatch"
        )
    floor = mp.mpf("1e-100")
    return max(
        abs(left[index] - right[index])
        / max(abs(left[index]), abs(right[index]), floor)
        for index in range(len(left))
    )


def mp_max_abs(left: Sequence[Any], right: Sequence[Any]) -> mp.mpf:
    if len(left) != len(right):
        raise SlotEvaluationError("max-abs vector length mismatch")
    return max(abs(left[i] - right[i]) for i in range(len(left)))


def mp_number_string(value: Any, dps: int) -> str:
    if mp.dps != dps:
        raise InvalidRun(
            f"mp serialization context drift: active {mp.dps}, declared {dps}"
        )
    number = mp.mpf(value)
    if not mp.isfinite(number):
        raise InvalidRun("nonfinite mp number in result")
    if number == 0:
        return "0.0"
    return mp.nstr(
        number,
        n=dps,
        strip_zeros=False,
        min_fixed=0,
        max_fixed=0,
    )


def mp_complex_payload(value: Any, dps: int) -> list[str]:
    number = mp.mpc(value)
    return [
        mp_number_string(number.real, dps),
        mp_number_string(number.imag, dps),
    ]


def mp_vector_payload(value: Sequence[Any], dps: int) -> list[list[str]]:
    return [mp_complex_payload(item, dps) for item in value]


def mp_metric_payload(value: Any, dps: int) -> str:
    return mp_number_string(value, dps)


def retained_mp_metric(value: Any, dps: int) -> dict[str, Any]:
    return {
        "computed_dps": dps,
        "value": mp_metric_payload(value, dps),
    }


def binary64_payload(value: np.ndarray) -> dict[str, Any]:
    array = np.asarray(value)
    flattened = array.reshape(-1)
    components: list[Any] = []
    if np.iscomplexobj(array):
        for item in flattened:
            number = complex(item)
            components.append(
                {
                    "real_hex": float(number.real).hex(),
                    "imag_hex": float(number.imag).hex(),
                    "real_ratio": list(float(number.real).as_integer_ratio()),
                    "imag_ratio": list(float(number.imag).as_integer_ratio()),
                    "real_signed_zero": bool(
                        number.real == 0.0 and math.copysign(1.0, number.real) < 0
                    ),
                    "imag_signed_zero": bool(
                        number.imag == 0.0 and math.copysign(1.0, number.imag) < 0
                    ),
                }
            )
    else:
        for item in flattened:
            number = float(item)
            components.append(
                {
                    "hex": number.hex(),
                    "ratio": list(number.as_integer_ratio()),
                    "signed_zero": bool(
                        number == 0.0 and math.copysign(1.0, number) < 0
                    ),
                }
            )
    dtype, raw = canonical_array_bytes(array)
    return {
        "shape": list(array.shape),
        "canonical_dtype": dtype,
        "canonical_raw_sha256": sha256_bytes(raw),
        "components": components,
    }


def independently_decode_all_array_records(
    value: Any,
    *,
    path: str = "$",
    output: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    decoded = {} if output is None else output
    if is_array_record(value):
        if path in decoded:
            raise InvalidRun(f"duplicate checkpoint array path: {path}")
        decoded[path] = decode_array_record(value, path=path)
        return decoded
    if isinstance(value, dict):
        for key, child in value.items():
            independently_decode_all_array_records(
                child, path=f"{path}.{key}", output=decoded
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            independently_decode_all_array_records(
                child, path=f"{path}[{index}]", output=decoded
            )
    return decoded


def independently_verify_checkpoint_array_ledger(
    checkpoint: Mapping[str, Any]
) -> dict[str, Any]:
    actual: dict[str, np.ndarray] = {}
    conventions = checkpoint["coordinate_and_orientation_conventions"]
    actual["coordinates.scales"] = decode_array_record(
        conventions["coordinate_scales"], path="$.coordinates.scales"
    )
    actual["coordinates.row_scales"] = decode_array_record(
        conventions["row_scales"], path="$.coordinates.row_scales"
    )
    for name in (
        "saddle_zero_w",
        "hessian_zero_w",
        "eigenvalues_zero",
        "oriented_eigenvectors_zero",
        "linear_map",
        "inverse_metric_mobility_w",
        "metric_tensor_w",
        "xi_reflection",
        "linear_map_z_from_xi",
    ):
        actual[f"fixed.{name}"] = decode_array_record(
            checkpoint["fixed_metric"][name], path=f"$.fixed.{name}"
        )
    maps = checkpoint["mode_and_reflection_maps"]
    for label, field_name in (
        ("modes.DST", "DST_basis"),
        ("modes.nested", "nested_basis"),
        ("modes.transition", "DST_to_nested_transition"),
        ("reflection.w", "reflection_w"),
        ("reflection.R14", "reflection_R14_interleaved"),
    ):
        actual[label] = decode_array_record(maps[field_name], path=f"$.{label}")
    actual["chart.center"] = decode_array_record(
        checkpoint["upward_chart"]["center"], path="$.chart.center"
    )
    actual["chart.tangent"] = decode_array_record(
        checkpoint["upward_chart"]["tangent"], path="$.chart.tangent"
    )
    for saddle_label, record in checkpoint["saddles"].items():
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
            actual[f"saddle.{saddle_label}.{suffix}"] = decode_array_record(
                wrapper, path=f"$.saddle.{saddle_label}.{suffix}"
            )
    primaries = checkpoint["primary_intersections"]
    for primary_label, wrapper in primaries["all_parameter_vectors"].items():
        result = primaries["all_phase41_results"][primary_label]
        actual[f"primary.{primary_label}.parameters"] = decode_array_record(
            wrapper, path=f"$.primary.{primary_label}.parameters"
        )
        actual[f"primary.{primary_label}.intersection_state_z"] = (
            decode_complex_pairs(
                result["intersection_z"],
                shape=(7,),
                path=f"$.primary.{primary_label}.intersection_state_z",
            )
        )
        jacobian = np.asarray(
            result["variational_scaled_root_jacobian"], dtype=np.float64
        )
        if not np.all(np.isfinite(jacobian)):
            raise InvalidRun(f"nonfinite primary Jacobian: {primary_label}")
        actual[
            f"primary.{primary_label}.variational_scaled_root_jacobian"
        ] = jacobian
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
    for target_label, target in primaries["phase42_fixed_root_targets"].items():
        for suffix, key_path in target_field_map.items():
            wrapper: Any = target
            for key in key_path:
                wrapper = wrapper[key]
            actual[f"target.{target_label}.{suffix}"] = decode_array_record(
                wrapper, path=f"$.target.{target_label}.{suffix}"
            )
        actual[f"target.{target_label}.recorded_gamma_state_z"] = (
            decode_complex_pairs(
                target["phase41_primary_result"]["intersection_z"],
                shape=(7,),
                path=f"$.target.{target_label}.recorded_gamma_state_z",
            )
        )
    embedded = checkpoint["critical_array_shape_and_finiteness_ledger"][
        "records"
    ]
    if set(actual) != set(embedded):
        raise InvalidRun(
            "checkpoint 204-array label mapping drift: "
            f"missing={sorted(set(embedded)-set(actual))[:8]}, "
            f"extra={sorted(set(actual)-set(embedded))[:8]}"
        )
    retained: dict[str, Any] = {}
    for label, values in actual.items():
        record = embedded[label]
        expected_shape = tuple(int(value) for value in record["expected_shape"])
        actual_shape = tuple(int(value) for value in record["actual_shape"])
        if values.shape != expected_shape or values.shape != actual_shape:
            raise InvalidRun(f"checkpoint mapped shape drift: {label}")
        runtime_dtype = "complex128" if np.iscomplexobj(values) else "float64"
        if record["runtime_dtype"] != runtime_dtype or not np.all(
            np.isfinite(values)
        ):
            raise InvalidRun(f"checkpoint mapped dtype/finiteness drift: {label}")
        canonical_dtype, raw = canonical_array_bytes(values)
        digest = sha256_bytes(raw)
        if digest != record["canonical_little_endian_sha256"]:
            raise InvalidRun(f"checkpoint mapped array SHA drift: {label}")
        if not (
            record["finite_numeric"] is True
            and record["shape_matches"] is True
            and record["passed"] is True
        ):
            raise InvalidRun(f"checkpoint mapped status flag false: {label}")
        retained[label] = {
            "shape": list(values.shape),
            "runtime_dtype": runtime_dtype,
            "canonical_dtype": canonical_dtype,
            "sha256": digest,
        }
    if len(retained) != 204:
        raise InvalidRun("checkpoint mapped array count is not 204")
    return {"mapped_count": len(retained), "records": retained}


def expected_fail_closed_outputs() -> dict[str, Any]:
    return {
        "m2_and_m4_actions_identified": False,
        "m2_and_m4_upward_cycles_identified": False,
        "m2_and_m4_common_determinant_line_constructed": False,
        "m3_and_m4_canonical_sign_equality_proved": False,
        "m3_and_m4_common_determinant_line_constructed": False,
        "straight_arm_intersections_searched": False,
        "cap_reintersections_searched": False,
        "continuous_direction_coverage_proved": False,
        "root_exhaustion_proved": False,
        "exact_nonlinear_upward_manifold_certified": False,
        "all_saddles_and_upward_components_complete": False,
        "non_Stokes_chamber_certified": False,
        "all_relative_good_ends_classified": False,
        "physical_original_cycle_derived": False,
        "metric_homotopy_tested": False,
        "BFV_Pfaffian_Pin_orientation_computed": False,
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "cutoff_limit": None,
        "continuum_limit": None,
        "quantum_gravity_explanation": None,
        "gate1_status": "OPEN_PARTIAL_PROGRESS",
    }


def expected_desired_outputs() -> dict[str, None]:
    return {
        "desired_phase43_local_arbitration": None,
        "desired_local_RHS_implementation_verdict": None,
        "desired_double_precision_FD_verdict": None,
        "desired_integrated_tangent_verdict": None,
        "desired_reference_corroboration": None,
        "desired_local_orientation_sign": None,
        "desired_global_intersection_coefficient": None,
    }


def manifest_contract_maps(
    manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    exact = {
        str(record["id"]): record for record in manifest["contracts"]["exact"]
    }
    numerical = {
        str(record["id"]): record
        for record in manifest["contracts"]["numerical"]
    }
    if tuple(exact) != EXACT_IDS or tuple(numerical) != NUMERICAL_IDS:
        raise InvalidRun("manifest contract ids/order drift")
    if manifest["run_semantics"]["exact_contract_count"] != len(EXACT_IDS):
        raise InvalidRun("manifest exact-contract count drift")
    if manifest["run_semantics"]["numerical_contract_count"] != len(
        NUMERICAL_IDS
    ):
        raise InvalidRun("manifest numerical-contract count drift")
    return exact, numerical


def validate_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    manifest_contract_maps(manifest)
    if manifest.get("phase") != 43:
        raise InvalidRun("manifest phase drift")
    if manifest.get("status") != "POST_PHASE42_DIAGNOSTIC_INPUT_FREEZE":
        raise InvalidRun("manifest status drift")
    if manifest.get("is_preregistration") is not False:
        raise InvalidRun("manifest preregistration status drift")
    if manifest.get("is_scientific_evidence") is not False:
        raise InvalidRun("manifest evidence status drift")
    runtime_contract = manifest["strict_runtime_environment"]
    if not (
        runtime_contract["sys_dont_write_bytecode_required"] is True
        and runtime_contract["repository_file_writes_allowed"] is False
        and runtime_contract[
            "source_and_environment_TOCTOU_recheck_before_RESULT_JSON"
        ]
        is True
    ):
        raise InvalidRun("strict runtime/write/TOCTOU declaration drift")
    frozen = manifest["frozen_local_inputs"]
    if tuple(frozen["points_in_fixed_order"]) != TARGETS:
        raise InvalidRun("target order drift")
    if tuple(frozen["flow_fractions_in_fixed_order"]) != FRACTION_STRINGS:
        raise InvalidRun("fraction order drift")
    if tuple(frozen["transported_direction_indices_in_fixed_order"]) != DIRECTIONS:
        raise InvalidRun("direction order drift")
    if int(frozen["slot_count"]) != 90:
        raise InvalidRun("base slot count drift")
    protocol = manifest["arbitrary_precision_protocol"]
    if tuple(protocol["precision_tiers_decimal_digits"]) != PRECISIONS:
        raise InvalidRun("precision tier drift")
    if int(protocol["authoritative_reference_tier_decimal_digits"]) != 120:
        raise InvalidRun("authoritative precision drift")
    same = protocol["phase42_same_step_replay"]
    if tuple(same["normalization_modes_in_fixed_order"]) != NORMALIZATION_MODES:
        raise InvalidRun("normalization-mode order drift")
    if tuple(same["epsilon_values"]) != SAME_EPSILON_STRINGS:
        raise InvalidRun("same-step epsilon drift")
    if same["D2"] != (
        "D2(epsilon)=[V(xi+epsilon*q_hat)-V(xi-epsilon*q_hat)]/(2*epsilon)."
    ):
        raise InvalidRun("same-step D2 formula declaration drift")
    if same["R4_neighbor"] != (
        "||q||*[4*D2(1e-5)-D2(2e-5)]/3."
    ):
        raise InvalidRun("same-step neighbor R4 declaration drift")
    if same["R4_fixed"] != (
        "||q||*[4*D2(5e-6)-D2(1e-5)]/3."
    ):
        raise InvalidRun("same-step fixed R4 declaration drift")
    prospective = protocol["prospective_small_step_ladder"]
    if prospective["normalization_mode"] != "native_mpmath_geometry":
        raise InvalidRun("prospective normalization mode drift")
    if tuple(prospective["R4_base_h_values_in_fixed_order"]) != (
        PROSPECTIVE_H_STRINGS
    ):
        raise InvalidRun("prospective h ladder drift")
    if tuple(prospective["endpoint_offsets_for_each_h"]) != PROSPECTIVE_OFFSETS:
        raise InvalidRun("manifest endpoint-offset declaration drift")
    if prospective["fixed_primary_h"] != "1e-12":
        raise InvalidRun("primary h drift")
    if prospective["fixed_coarse_neighbor_h"] != "1e-10":
        raise InvalidRun("coarse neighbor h drift")
    if prospective["fixed_fine_neighbor_h"] != "1e-14":
        raise InvalidRun("fine neighbor h drift")
    if prospective["R4_formula"] != (
        "R4(h)=[V(xi-h*q_hat)-8*V(xi-h*q_hat/2)+"
        "8*V(xi+h*q_hat/2)-V(xi+h*q_hat)]/(6*h), restored by ||q||."
    ):
        raise InvalidRun("prospective R4 formula declaration drift")
    if protocol["time_column_evaluations"] != []:
        raise InvalidRun("time-column evaluation was declared")
    if protocol["ODE_solver_evaluations"] != []:
        raise InvalidRun("ODE evaluation was declared")
    if protocol["root_solver_evaluations"] != []:
        raise InvalidRun("root evaluation was declared")
    if manifest["required_fail_closed_outputs"] != expected_fail_closed_outputs():
        raise InvalidRun("fail-closed output ledger drift")
    if manifest["desired_outputs"] != expected_desired_outputs():
        raise InvalidRun("desired-output null ledger drift")
    if manifest["historical_statuses_must_remain"] != {
        "phase41_numerical_contracts": "8/9",
        "phase41_tangent_status": "TANGENT_CONTROL_FAILED",
        "phase42_reference_tangent": "REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE",
        "phase42_protocol_local_anomaly_label": "VARIATIONAL_RHS_BUG_EVIDENCE",
        "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
        "phase43_ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
        "global_promotion": "PROHIBITED",
    }:
        raise InvalidRun("historical status boundary drift")
    thresholds = manifest["acceptance_thresholds"]
    expected_thresholds = {
        "phase42_source_vector_reproduction_max_abs": "5e-15",
        "source_rounding_control_vs_independent_exact_decimal_relative_max": "1e-40",
        "symbolic_hessian_vs_gradient_directional_relative_max": "1e-50",
        "80_vs_120_precision_stability_relative_max": "1e-50",
        "same_step_high_precision_R4_to_symbolic_relative_max": "1e-12",
        "small_step_primary_R4_to_symbolic_relative_max": "1e-30",
        "small_step_reference_neighbor_relative_max": "1e-28",
        "source_numpy64_hessian_action_to_high_precision_relative_max": "5e-13",
        "phase42_stable_violation_threshold_reproduced": "1e-7",
        "phase42_reference_stability_threshold_reproduced": "1e-6",
    }
    for key, value in expected_thresholds.items():
        if thresholds.get(key) != value:
            raise InvalidRun(f"threshold drift: {key}")
    expected_metrics = {
        "mp_vector_norm": (
            "sqrt(sum(abs(z_i)**2)) evaluated wholly in the active mp context."
        ),
        "symmetric_relative": (
            "rel(x,y)=||x-y||_2/max(||x||_2,||y||_2,1e-100), where "
            "1e-100 is parsed directly as mp.mpf."
        ),
        "max_component_relative": (
            "max_i abs(x_i-y_i)/max(abs(x_i),abs(y_i),1e-100)."
        ),
        "binary64_reproduction_max_abs": (
            "Maximum absolute complex-component difference after recomputing "
            "the stored Phase-42 source analytic, D2, and R4 vectors."
        ),
        "precision_stability": (
            "rel(value_at_80_dps,value_at_120_dps) after both are retained as "
            "decimal strings without float conversion."
        ),
        "reference_neighbor_stability": (
            "max(rel(R4(1e-12),R4(1e-10)),rel(R4(1e-12),R4(1e-14)))."
        ),
        "old_to_high_precision_improvement_ratio": (
            "Phase42 stored fixed-to-analytic rel divided by max(120-dps "
            "same-step R4-to-A_H rel,1e-100); retained descriptively and never "
            "used to select a slot or step."
        ),
    }
    if manifest["metric_definitions"] != expected_metrics:
        raise InvalidRun("metric-definition declaration drift")
    retention = manifest["declared_output_retention"]
    if retention["slot_terminal_statuses"] != [
        "SUCCESS",
        "EVALUATION_FAILED",
        "NOT_RUN_UPSTREAM_INVALID",
    ]:
        raise InvalidRun("slot terminal vocabulary drift")
    result_contract = manifest["declared_output_retention"]["result_artifact"]
    if result_contract["schema"] != RESULT_SCHEMA:
        raise InvalidRun("result schema drift")
    if result_contract["stdout_prefix"] != RESULT_PREFIX:
        raise InvalidRun("stdout prefix drift")
    if result_contract["outer_file_sha256"] is not None:
        raise InvalidRun("result outer hash was prefilled")
    if result_contract["payload_sha256_without_self"] is not None:
        raise InvalidRun("result payload hash was prefilled")
    pilot = manifest["known_precommit_design_audit"]
    if not (
        pilot["pilot_is_not_a_production_run"] is True
        and pilot["pilot_has_no_committed_runner_or_raw_artifact"] is True
        and pilot["pilot_is_not_admissible_phase43_evidence"] is True
        and pilot["threshold_was_not_changed_after_pilot"] is True
    ):
        raise InvalidRun("precommit pilot disclosure drift")
    return {
        "phase": 43,
        "status": manifest["status"],
        "base_slot_count": 90,
        "precision_tiers": list(PRECISIONS),
        "same_step_normalization_modes": list(NORMALIZATION_MODES),
        "time_column_excluded": True,
        "ODE_and_root_solvers_declared": False,
        "desired_outputs_all_null": True,
        "gate1_status": "OPEN_PARTIAL_PROGRESS",
    }


def verify_self_digest(
    payload: Mapping[str, Any], field_name: str, expected: str, *, label: str
) -> None:
    embedded = payload.get(field_name)
    if embedded != expected:
        raise InvalidRun(f"{label} embedded self digest drift")
    without_self = dict(payload)
    without_self.pop(field_name, None)
    recomputed = sha256_bytes(canonical_json_bytes(without_self))
    if recomputed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")


def fraction_string(value: Any) -> str:
    number = float(value)
    for text in FRACTION_STRINGS:
        if number == float(text):
            return text
    raise InvalidRun(f"undeclared flow fraction: {value}")


def epsilon_string(value: Any) -> str:
    number = float(value)
    for text in SAME_EPSILON_STRINGS:
        if number == float(text):
            return text
    raise InvalidRun(f"undeclared epsilon: {value}")


def import_pinned_phase41(manifest: Mapping[str, Any]) -> ModuleType:
    pin = source_pin_specs(manifest)["phase41_script"]
    before = sha256_bytes(PHASE41_PATH.read_bytes())
    if before != pin["sha256"]:
        raise InvalidRun("Phase41 source drift before import")
    module_name = "ice_phase41_m4_phase43_source_target"
    specification = importlib.util.spec_from_file_location(module_name, PHASE41_PATH)
    if specification is None or specification.loader is None:
        raise InvalidRun("cannot construct Phase41 module spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    if sha256_bytes(PHASE41_PATH.read_bytes()) != before:
        raise InvalidRun("Phase41 source changed during import")
    phase41_manifest = manifest["immutable_artifacts"]["phase41_input_manifest"]
    if module.INPUT_COMMIT != phase41_manifest["commit"]:
        raise InvalidRun("Phase41 embedded manifest commit drift")
    if module.INPUT_SHA256 != phase41_manifest["sha256"]:
        raise InvalidRun("Phase41 embedded manifest SHA drift")
    return module


def install_forbidden_call_guards(phase41: ModuleType) -> dict[str, int]:
    counter: dict[str, int] = {}

    def forbidden(name: str) -> Callable[..., Any]:
        counter[name] = 0

        def reject(*_args: Any, **_kwargs: Any) -> Any:
            counter[name] += 1
            raise InvalidRun(f"forbidden Phase43 solver/trajectory call: {name}")

        return reject

    names = (
        "solve_signed_saddle_grids",
        "solve_main_saddle",
        "solve_primary_intersections",
        "build_fixed_metric",
        "build_nested_chart",
        "residual_and_variational_jacobian",
        "integrate_chart",
        "solve_ivp",
        "root",
        "least_squares",
    )
    for name in names:
        if hasattr(phase41, name):
            setattr(phase41, name, forbidden(name))
    return counter


def validate_and_rehydrate_inputs(
    manifest: Mapping[str, Any]
) -> FrozenContext:
    artifacts = manifest["immutable_artifacts"]
    result_pin = artifacts["phase42_raw_result"]
    checkpoint_pin = artifacts["phase42_checkpoint"]
    result, result_raw = read_pinned_json(
        PHASE42_RESULT_PATH,
        result_pin["outer_file_sha256_including_final_LF"],
        label="Phase42 raw result",
        expected_size=int(result_pin["size_bytes"]),
    )
    checkpoint, checkpoint_raw = read_pinned_json(
        CHECKPOINT_PATH,
        checkpoint_pin["outer_file_sha256_including_final_LF"],
        label="Phase42 checkpoint",
    )
    if result.get("schema") != PHASE42_RESULT_SCHEMA:
        raise InvalidRun("Phase42 result schema drift")
    if result.get("phase") != 42 or result.get("run_status") != "VALID_TYPED_RUN":
        raise InvalidRun("Phase42 result status drift")
    if result.get("exit_code") != 0:
        raise InvalidRun("Phase42 result exit-code drift")
    verify_self_digest(
        result,
        "result_payload_sha256_without_self",
        result_pin["result_payload_sha256_without_self"],
        label="Phase42 result",
    )
    if checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise InvalidRun("checkpoint schema drift")
    if checkpoint.get("checkpoint_status") != "POST_HOC_REGENERATED_CHECKPOINT":
        raise InvalidRun("checkpoint status drift")
    verify_self_digest(
        checkpoint,
        "checkpoint_payload_sha256_without_self",
        checkpoint_pin["checkpoint_payload_sha256_without_self"],
        label="Phase42 checkpoint",
    )
    decoded_checkpoint = independently_decode_all_array_records(checkpoint)
    checkpoint_array_ledger = checkpoint[
        "critical_array_shape_and_finiteness_ledger"
    ]
    declared_array_count = int(checkpoint_array_ledger["checked_array_count"])
    if not (
        checkpoint_array_ledger["all_passed"] is True
        and checkpoint_array_ledger["fail_closed"] is True
        and isinstance(checkpoint_array_ledger["records"], dict)
        and len(checkpoint_array_ledger["records"]) == declared_array_count
        and declared_array_count == 204
        and len(decoded_checkpoint) == 191
    ):
        raise InvalidRun(
            "checkpoint independently decoded array count does not match ledger"
        )
    mapped_checkpoint_arrays = independently_verify_checkpoint_array_ledger(
        checkpoint
    )
    explicit_checkpoint_array_validation = {}
    for path, values in decoded_checkpoint.items():
        canonical_dtype, canonical_raw = canonical_array_bytes(values)
        explicit_checkpoint_array_validation[path] = {
            "shape": list(values.shape),
            "runtime_dtype": str(values.dtype),
            "canonical_dtype": canonical_dtype,
            "sha256": sha256_bytes(canonical_raw),
        }
    coordinate_record = checkpoint["coordinate_and_orientation_conventions"][
        "coordinate_scales"
    ]
    coordinate_scales = decode_array_record(
        coordinate_record,
        path="$.coordinate_and_orientation_conventions.coordinate_scales",
        expected_shape=(7,),
    )
    linear_record = checkpoint["fixed_metric"]["linear_map"]
    linear_map = decode_array_record(
        linear_record,
        path="$.fixed_metric.linear_map",
        expected_shape=(7, 7),
    )
    checkpoint_pins = manifest["frozen_local_inputs"]["checkpoint_array_pins"]
    if coordinate_record["canonical_little_endian_sha256"] != checkpoint_pins[
        "coordinate_scales_raw_sha256"
    ]:
        raise InvalidRun("coordinate-scale pin drift")
    if linear_record["canonical_little_endian_sha256"] != checkpoint_pins[
        "fixed_linear_map_raw_sha256"
    ]:
        raise InvalidRun("linear-map pin drift")
    if coordinate_scales.tolist() != [
        float(text) for text in checkpoint_pins["coordinate_scales_decimal_literals"]
    ]:
        raise InvalidRun("coordinate-scale literal drift")

    slot_ledger = result.get("slot_ledger")
    if not isinstance(slot_ledger, dict):
        raise InvalidRun("Phase42 slot ledger missing")
    points: dict[str, FrozenPoint] = {}
    result_pins = manifest["frozen_local_inputs"][
        "phase42_array_and_subtree_pins"
    ]
    source_pins = manifest["frozen_local_inputs"]["source_points"]
    known = manifest["known_phase42_negative_control"]
    total_q_identities = 0
    total_perturbations = 0
    for label in TARGETS:
        augmented_key = f"augmented|{label}|tight_augmented"
        augmented_slot = slot_ledger.get(augmented_key)
        if not isinstance(augmented_slot, dict):
            raise InvalidRun(f"missing Phase42 augmented slot: {label}")
        if augmented_slot.get("terminal_status") != "SUCCESS":
            raise InvalidRun(f"Phase42 augmented slot not successful: {label}")
        payload = augmented_slot.get("payload")
        if not isinstance(payload, dict):
            raise InvalidRun(f"Phase42 augmented payload missing: {label}")
        pin = result_pins[label]
        if sha256_bytes(canonical_json_bytes(payload)) != pin[
            "tight_augmented_payload_canonical_json_sha256"
        ]:
            raise InvalidRun(f"tight augmented subtree drift: {label}")
        fraction_times = np.asarray(payload["fraction_times"], dtype=np.float64)
        if fraction_times.shape != (5,) or not np.all(np.isfinite(fraction_times)):
            raise InvalidRun(f"fraction time shape/finiteness drift: {label}")
        fraction_xi = decode_complex_pairs(
            payload["fraction_xi"],
            shape=(5, 7),
            path=f"$.slot_ledger.{augmented_key}.payload.fraction_xi",
        )
        fraction_tangents = decode_complex_pairs(
            payload["fraction_tangents"],
            shape=(5, 7, 6),
            path=f"$.slot_ledger.{augmented_key}.payload.fraction_tangents",
        )
        if sha256_bytes(canonical_array_bytes(fraction_times)[1]) != pin[
            "fraction_times_raw_float64_sha256"
        ]:
            raise InvalidRun(f"fraction-time raw pin drift: {label}")
        if sha256_bytes(canonical_array_bytes(fraction_xi)[1]) != pin[
            "fraction_xi_raw_complex128_sha256"
        ]:
            raise InvalidRun(f"fraction-xi raw pin drift: {label}")
        if sha256_bytes(canonical_array_bytes(fraction_tangents)[1]) != pin[
            "fraction_tangents_raw_complex128_sha256"
        ]:
            raise InvalidRun(f"fraction-tangent raw pin drift: {label}")
        local_point = result["local_variational_diagnostics"]["points"][label]
        if sha256_bytes(canonical_json_bytes(local_point)) != pin[
            "local_point_payload_canonical_json_sha256"
        ]:
            raise InvalidRun(f"local diagnostic subtree drift: {label}")
        records = local_point.get("direction_records")
        if not isinstance(records, list) or len(records) != 30:
            raise InvalidRun(f"local direction record count drift: {label}")
        local_records: dict[tuple[str, int], Mapping[str, Any]] = {}
        stable_slots: set[tuple[str, int]] = set()
        violation_slots: set[tuple[str, int]] = set()
        for record_index, record in enumerate(records):
            fraction = fraction_string(record["fraction"])
            direction = int(record["direction"])
            key = (fraction, direction)
            if key in local_records or direction not in DIRECTIONS:
                raise InvalidRun(f"duplicate/invalid local direction record: {label}")
            fraction_index = FRACTION_STRINGS.index(fraction)
            if record_index != fraction_index * len(DIRECTIONS) + direction:
                raise InvalidRun(
                    f"local direction record order drift: {label}/{key}"
                )
            expected_q_json = [
                payload["fraction_tangents"][fraction_index][row][direction]
                for row in range(7)
            ]
            if record["q"] != expected_q_json:
                raise InvalidRun(f"q duplicate identity drift: {label}/{key}")
            total_q_identities += 1
            local_records[key] = record
            if record.get("stable") is True:
                stable_slots.add(key)
            if record.get("stable_violation") is True:
                violation_slots.add(key)
        expected_violations = {
            (str(fraction), int(direction))
            for fraction, direction in known["stable_violation_slots"][label]
        }
        expected_unstable = {
            (str(fraction), int(direction))
            for fraction, direction in known[
                "unstable_slots_retained_but_not_bug_evidence"
            ][label]
        }
        if violation_slots != expected_violations:
            raise InvalidRun(f"stable-violation cohort drift: {label}")
        if set(local_records) - stable_slots != expected_unstable:
            raise InvalidRun(f"unstable cohort drift: {label}")
        if len(stable_slots) != int(pin["stable_count"]):
            raise InvalidRun(f"stable count drift: {label}")
        if len(violation_slots) != int(pin["stable_violation_count"]):
            raise InvalidRun(f"violation count drift: {label}")

        perturbations: dict[
            tuple[str, int, str, int], Mapping[str, Any]
        ] = {}
        for candidate in slot_ledger.values():
            if not isinstance(candidate, dict):
                continue
            metadata = candidate.get("metadata")
            if not isinstance(metadata, dict):
                continue
            if metadata.get("slot_kind") != "local_RHS_perturbation":
                continue
            if metadata.get("point") != label:
                continue
            key = (
                fraction_string(metadata["fraction"]),
                int(metadata["direction"]),
                epsilon_string(metadata["epsilon"]),
                int(metadata["sign"]),
            )
            if key in perturbations:
                raise InvalidRun(f"duplicate perturbation record: {label}/{key}")
            if candidate.get("terminal_status") != "SUCCESS":
                raise InvalidRun(f"non-success perturbation record: {label}/{key}")
            candidate_payload = candidate.get("payload")
            if not isinstance(candidate_payload, dict):
                raise InvalidRun(f"missing perturbation payload: {label}/{key}")
            perturbations[key] = candidate_payload
        if len(perturbations) != 180:
            raise InvalidRun(f"perturbation record count drift: {label}")
        total_perturbations += len(perturbations)

        saddle_record = checkpoint["saddles"][label]["saddle_w"]
        saddle_w = decode_array_record(
            saddle_record,
            path=f"$.saddles.{label}.saddle_w",
            expected_shape=(7,),
        )
        source_pin = source_pins[label]
        if saddle_record["canonical_little_endian_sha256"] != source_pin[
            "checkpoint_saddle_w_raw_sha256"
        ]:
            raise InvalidRun(f"saddle_w pin drift: {label}")
        checkpoint_source = checkpoint["saddles"][label]["source_point"]
        if checkpoint_source != {
            "delta_a": float(source_pin["delta_a"]),
            "delta_phi": float(source_pin["delta_phi"]),
        }:
            raise InvalidRun(f"source point drift: {label}")
        points[label] = FrozenPoint(
            label=label,
            delta_a=str(source_pin["delta_a"]),
            delta_phi=str(source_pin["delta_phi"]),
            saddle_w=saddle_w,
            fraction_times=fraction_times,
            fraction_xi=fraction_xi,
            fraction_tangents=fraction_tangents,
            local_records=local_records,
            perturbation_records=perturbations,
        )
    if total_q_identities != 90 or total_perturbations != 540:
        raise InvalidRun("Phase42 local retained-slot total drift")
    phase41 = import_pinned_phase41(manifest)
    counter = install_forbidden_call_guards(phase41)
    validation = {
        "phase42_result_outer_sha256": sha256_bytes(result_raw),
        "phase42_result_self_digest": result_pin[
            "result_payload_sha256_without_self"
        ],
        "checkpoint_outer_sha256": sha256_bytes(checkpoint_raw),
        "checkpoint_self_digest": checkpoint_pin[
            "checkpoint_payload_sha256_without_self"
        ],
        "checkpoint_explicit_array_records_independently_decoded": len(
            decoded_checkpoint
        ),
        "checkpoint_critical_arrays_independently_mapped": (
            mapped_checkpoint_arrays["mapped_count"]
        ),
        "checkpoint_explicit_array_validation": (
            explicit_checkpoint_array_validation
        ),
        "checkpoint_critical_array_mapping_validation": (
            mapped_checkpoint_arrays["records"]
        ),
        "q_duplicate_identities": total_q_identities,
        "perturbation_records": total_perturbations,
        "point_count": len(points),
        "base_slot_count": 90,
        "time_column_records_consumed": 0,
        "ODE_or_root_calls_declared": 0,
    }
    return FrozenContext(
        phase42_result=result,
        checkpoint=checkpoint,
        phase41=phase41,
        coordinate_scales=coordinate_scales,
        linear_map=linear_map,
        points=points,
        forbidden_call_counter=counter,
        validation=validation,
    )


def base_key(point: str, fraction: str, direction: int) -> str:
    return f"point={point}|fraction={fraction}|direction={direction}"


def independently_expected_slot_keys() -> set[str]:
    keys = {"symbolic|independent_model", "symbolic|reference_boundary"}
    for point in TARGETS:
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                base = base_key(point, fraction, direction)
                keys.update(
                    {
                        f"input|{base}",
                        f"source|{base}|analytic",
                        f"source|{base}|summary",
                    }
                )
                for epsilon in SAME_EPSILON_STRINGS:
                    for sign in (-1, 1):
                        keys.add(
                            f"source|{base}|epsilon={epsilon}|sign={sign}"
                        )
                    keys.add(f"source_D2|{base}|epsilon={epsilon}")
                for reference in ("neighbor_2e-5", "fixed_1e-5"):
                    keys.add(f"source_R4|{base}|reference={reference}")
                for dps in PRECISIONS:
                    for method in (
                        "hessian",
                        "gradient_directional",
                        "rounding_control",
                    ):
                        keys.add(
                            f"reference|{base}|dps={dps}|method={method}"
                        )
                    for mode in NORMALIZATION_MODES:
                        for epsilon in SAME_EPSILON_STRINGS:
                            for sign in (-1, 1):
                                keys.add(
                                    f"same_step|{base}|dps={dps}|mode={mode}|epsilon={epsilon}|sign={sign}"
                                )
                            keys.add(
                                f"same_step_D2|{base}|dps={dps}|mode={mode}|epsilon={epsilon}"
                            )
                        for reference in (
                            "neighbor_2e-5",
                            "fixed_1e-5",
                        ):
                            keys.add(
                                f"same_step_R4|{base}|dps={dps}|mode={mode}|reference={reference}"
                            )
                    for h in PROSPECTIVE_H_STRINGS:
                        for offset in PROSPECTIVE_OFFSETS:
                            keys.add(
                                f"prospective|{base}|dps={dps}|h={h}|offset={offset}"
                            )
                        for scale in ("h", "h/2"):
                            keys.add(
                                f"prospective_D2|{base}|dps={dps}|h={h}|scale={scale}"
                            )
                        keys.add(
                            f"prospective_R4|{base}|dps={dps}|h={h}"
                        )
                for classification in (
                    "reference",
                    "source_RHS",
                    "double_FD",
                ):
                    keys.add(
                        f"classification|{base}|kind={classification}"
                    )
    for point in TARGETS:
        for aggregate in ("reference", "source_RHS", "double_FD"):
            keys.add(f"point_aggregate|point={point}|kind={aggregate}")
    for aggregate in (
        "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE",
        "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES",
        "PHASE43_LOCAL_ARBITRATION",
        "INTEGRATED_TANGENT_EVOLUTION",
        "ODE_SOLVER_NOISE_COMPONENT",
    ):
        keys.add(f"global_aggregate|kind={aggregate}")
    return keys


def preenumerate_slots(
    manifest: Mapping[str, Any], ledger: SlotLedger
) -> dict[str, Any]:
    ledger.declare("symbolic|independent_model", slot_kind="symbolic_model")
    ledger.declare("symbolic|reference_boundary", slot_kind="symbolic_boundary")
    for point in TARGETS:
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                base = base_key(point, fraction, direction)
                cohort = [fraction, direction] in manifest[
                    "known_phase42_negative_control"
                ]["stable_violation_slots"][point]
                ledger.declare(
                    f"input|{base}",
                    slot_kind="frozen_input",
                    point=point,
                    fraction=fraction,
                    direction=direction,
                    disclosed_anomaly_cohort=cohort,
                )
                ledger.declare(
                    f"source|{base}|analytic",
                    slot_kind="source_analytic",
                    point=point,
                    fraction=fraction,
                    direction=direction,
                )
                for epsilon in SAME_EPSILON_STRINGS:
                    for sign in (-1, 1):
                        ledger.declare(
                            f"source|{base}|epsilon={epsilon}|sign={sign}",
                            slot_kind="source_endpoint",
                            point=point,
                            fraction=fraction,
                            direction=direction,
                            epsilon=epsilon,
                            sign=sign,
                        )
                    ledger.declare(
                        f"source_D2|{base}|epsilon={epsilon}",
                        slot_kind="source_D2",
                        point=point,
                        fraction=fraction,
                        direction=direction,
                        epsilon=epsilon,
                    )
                for reference in ("neighbor_2e-5", "fixed_1e-5"):
                    ledger.declare(
                        f"source_R4|{base}|reference={reference}",
                        slot_kind="source_R4",
                        point=point,
                        fraction=fraction,
                        direction=direction,
                        reference=reference,
                    )
                ledger.declare(
                    f"source|{base}|summary",
                    slot_kind="source_summary",
                    point=point,
                    fraction=fraction,
                    direction=direction,
                )
                for dps in PRECISIONS:
                    for method in ("hessian", "gradient_directional", "rounding_control"):
                        ledger.declare(
                            f"reference|{base}|dps={dps}|method={method}",
                            slot_kind="reference_analytic",
                            point=point,
                            fraction=fraction,
                            direction=direction,
                            dps=dps,
                            method=method,
                        )
                    for mode in NORMALIZATION_MODES:
                        for epsilon in SAME_EPSILON_STRINGS:
                            for sign in (-1, 1):
                                ledger.declare(
                                    f"same_step|{base}|dps={dps}|mode={mode}|epsilon={epsilon}|sign={sign}",
                                    slot_kind="same_step_endpoint",
                                    point=point,
                                    fraction=fraction,
                                    direction=direction,
                                    dps=dps,
                                    mode=mode,
                                    epsilon=epsilon,
                                    sign=sign,
                                )
                            ledger.declare(
                                f"same_step_D2|{base}|dps={dps}|mode={mode}|epsilon={epsilon}",
                                slot_kind="same_step_D2",
                                point=point,
                                fraction=fraction,
                                direction=direction,
                                dps=dps,
                                mode=mode,
                                epsilon=epsilon,
                            )
                        for reference in ("neighbor_2e-5", "fixed_1e-5"):
                            ledger.declare(
                                f"same_step_R4|{base}|dps={dps}|mode={mode}|reference={reference}",
                                slot_kind="same_step_R4",
                                point=point,
                                fraction=fraction,
                                direction=direction,
                                dps=dps,
                                mode=mode,
                                reference=reference,
                            )
                    for h in PROSPECTIVE_H_STRINGS:
                        for offset in PROSPECTIVE_OFFSETS:
                            ledger.declare(
                                f"prospective|{base}|dps={dps}|h={h}|offset={offset}",
                                slot_kind="prospective_endpoint",
                                point=point,
                                fraction=fraction,
                                direction=direction,
                                dps=dps,
                                h=h,
                                offset=offset,
                            )
                        for scale in ("h", "h/2"):
                            ledger.declare(
                                f"prospective_D2|{base}|dps={dps}|h={h}|scale={scale}",
                                slot_kind="prospective_D2",
                                point=point,
                                fraction=fraction,
                                direction=direction,
                                dps=dps,
                                h=h,
                                scale=scale,
                            )
                        ledger.declare(
                            f"prospective_R4|{base}|dps={dps}|h={h}",
                            slot_kind="prospective_R4",
                            point=point,
                            fraction=fraction,
                            direction=direction,
                            dps=dps,
                            h=h,
                        )
                for classification in ("reference", "source_RHS", "double_FD"):
                    ledger.declare(
                        f"classification|{base}|kind={classification}",
                        slot_kind="slot_classification",
                        point=point,
                        fraction=fraction,
                        direction=direction,
                        classification=classification,
                    )
    for point in TARGETS:
        for aggregate in ("reference", "source_RHS", "double_FD"):
            ledger.declare(
                f"point_aggregate|point={point}|kind={aggregate}",
                slot_kind="point_aggregate",
                point=point,
                aggregate=aggregate,
            )
    for aggregate in (
        "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE",
        "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES",
        "PHASE43_LOCAL_ARBITRATION",
        "INTEGRATED_TANGENT_EVOLUTION",
        "ODE_SOLVER_NOISE_COMPONENT",
    ):
        ledger.declare(
            f"global_aggregate|kind={aggregate}",
            slot_kind="global_aggregate",
            aggregate=aggregate,
        )
    counts: dict[str, int] = {}
    for slot in ledger.slots.values():
        kind = str(slot["metadata"]["slot_kind"])
        counts[kind] = counts.get(kind, 0) + 1
    expected_counts = {
        "frozen_input": 90,
        "global_aggregate": 5,
        "point_aggregate": 9,
        "prospective_D2": 2160,
        "prospective_R4": 1080,
        "prospective_endpoint": 4320,
        "reference_analytic": 540,
        "same_step_D2": 1080,
        "same_step_R4": 720,
        "same_step_endpoint": 2160,
        "slot_classification": 270,
        "source_analytic": 90,
        "source_D2": 270,
        "source_R4": 180,
        "source_endpoint": 540,
        "source_summary": 90,
        "symbolic_boundary": 1,
        "symbolic_model": 1,
    }
    if counts != expected_counts:
        raise InvalidRun(
            f"full predeclared slot-kind count drift: {counts}"
        )
    expected_keys = independently_expected_slot_keys()
    if set(ledger.slots) != expected_keys or len(expected_keys) != 13606:
        missing = sorted(expected_keys - set(ledger.slots))[:8]
        extra = sorted(set(ledger.slots) - expected_keys)[:8]
        raise InvalidRun(
            f"full predeclared key-set drift: missing={missing}, extra={extra}"
        )
    return {
        "total_declared": len(ledger.slots),
        "by_kind": dict(sorted(counts.items())),
        "expected_key_set_sha256": sha256_bytes(
            "\n".join(sorted(expected_keys)).encode("utf-8")
        ),
        "observed_key_set_sha256": sha256_bytes(
            "\n".join(sorted(ledger.slots)).encode("utf-8")
        ),
        "base_slot_count": 90,
        "all_slots_declared_before_scientific_evaluation": True,
    }


@dataclass(frozen=True)
class BaseOutcome:
    point: str
    fraction: str
    direction: int
    disclosed_anomaly: bool
    source_reproduction_passed: bool
    independent_reference_passed: bool
    r4_reference_passed: bool
    reference_completion: str
    source_rhs_completion: str
    double_fd_completion: str
    reference_status: str
    source_rhs_evidence: str
    double_fd_evidence: str
    source_reproduction_max_abs: float | None
    source_to_reference_relative: Mapping[str, Any] | None
    metric_paths: Mapping[str, Sequence[str]]


def np_max_abs(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left, dtype=np.complex128)
    b = np.asarray(right, dtype=np.complex128)
    if a.shape != b.shape:
        raise SlotEvaluationError("NumPy comparison shape mismatch")
    if not np.all(np.isfinite(a.real)) or not np.all(np.isfinite(a.imag)):
        raise SlotEvaluationError("nonfinite NumPy left vector")
    if not np.all(np.isfinite(b.real)) or not np.all(np.isfinite(b.imag)):
        raise SlotEvaluationError("nonfinite NumPy right vector")
    return float(np.max(np.abs(a - b)))


def phase42_binary64_vector_relative(
    left: np.ndarray, right: np.ndarray
) -> float:
    a = np.asarray(left, dtype=np.complex128).reshape(-1)
    b = np.asarray(right, dtype=np.complex128).reshape(-1)
    if a.shape != b.shape or not np.all(np.isfinite(a)) or not np.all(
        np.isfinite(b)
    ):
        raise SlotEvaluationError(
            "Phase42 binary64 relative-vector inputs are mismatched/nonfinite"
        )
    return float(
        np.linalg.norm(a - b)
        / max(np.linalg.norm(a), np.linalg.norm(b), 1.0e-30)
    )


def p42_vector(value: Any, *, path: str) -> np.ndarray:
    return decode_complex_pairs(value, shape=(7,), path=path)


def attempt_slot(
    ledger: SlotLedger,
    key: str,
    operation: Callable[[], tuple[Any, Mapping[str, Any]]],
) -> Any | None:
    try:
        value, payload = operation()
        ledger.finish(key, "SUCCESS", payload=payload)
        return value
    except InvalidRun:
        raise
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"[:4096]
        payload = dict(getattr(exc, "payload", {}) or {})
        ledger.finish(key, "EVALUATION_FAILED", payload=payload, error=error)
        return None


def finish_dependency_failure(
    ledger: SlotLedger, key: str, reason: str
) -> None:
    ledger.finish(key, "NOT_RUN_UPSTREAM_INVALID", error=reason[:4096])


def source_objects(
    context: FrozenContext, point: FrozenPoint
) -> tuple[Any, Any, Any]:
    model = context.phase41.numeric_model(
        float(point.delta_a), float(point.delta_phi)
    )
    saddle = SimpleNamespace(saddle_w=point.saddle_w)
    fixed = SimpleNamespace(linear_map=context.linear_map)
    return model, saddle, fixed


def source_analytic_action(
    context: FrozenContext,
    point: FrozenPoint,
    model: Any,
    saddle: Any,
    fixed: Any,
    xi: np.ndarray,
    q: np.ndarray,
) -> np.ndarray:
    value = -np.conjugate(
        context.phase41.hessian_xi(model, saddle, fixed, xi) @ q
    )
    result = np.asarray(value, dtype=np.complex128).reshape(7)
    if not np.all(np.isfinite(result.real)) or not np.all(np.isfinite(result.imag)):
        raise SlotEvaluationError("nonfinite source analytic Hessian action")
    return result


def source_flow(
    context: FrozenContext,
    model: Any,
    saddle: Any,
    fixed: Any,
    xi: np.ndarray,
) -> np.ndarray:
    value = context.phase41.flow_xi(model, saddle, fixed, xi)
    result = np.asarray(value, dtype=np.complex128).reshape(7)
    if not np.all(np.isfinite(result.real)) or not np.all(np.isfinite(result.imag)):
        raise SlotEvaluationError("nonfinite source flow")
    return result


def vector_scale(value: Sequence[Any], scalar: Any) -> list[Any]:
    return [scalar * item for item in value]


def vector_difference(left: Sequence[Any], right: Sequence[Any]) -> list[Any]:
    if len(left) != len(right):
        raise SlotEvaluationError("vector difference length mismatch")
    return [left[index] - right[index] for index in range(len(left))]


def vector_linear_combination(
    left_scale: Any,
    left: Sequence[Any],
    right_scale: Any,
    right: Sequence[Any],
) -> list[Any]:
    if len(left) != len(right):
        raise SlotEvaluationError("vector combination length mismatch")
    return [
        left_scale * left[index] + right_scale * right[index]
        for index in range(len(left))
    ]


def central_D2(
    plus: Sequence[Any], minus: Sequence[Any], epsilon: Any
) -> list[Any]:
    return vector_scale(
        vector_difference(plus, minus),
        mp.mpf(1) / (mp.mpf(2) * epsilon),
    )


def restored_R4(
    fine_D2: Sequence[Any],
    coarse_D2: Sequence[Any],
    restoration_norm: Any,
) -> list[Any]:
    return vector_scale(
        vector_linear_combination(
            mp.mpf(4), fine_D2, mp.mpf(-1), coarse_D2
        ),
        restoration_norm / mp.mpf(3),
    )


def mp_lift_numpy_vector(value: np.ndarray) -> list[mp.mpc]:
    return mp_vector_from_numpy(np.asarray(value, dtype=np.complex128))


def mp_geometry(
    q64: np.ndarray, mode: str
) -> tuple[list[mp.mpc], mp.mpf, Mapping[str, Any]]:
    q_array = np.asarray(q64, dtype=np.complex128).reshape(7)
    if mode == "lifted_binary64_geometry":
        q_norm64 = float(np.linalg.norm(q_array))
        if not math.isfinite(q_norm64) or q_norm64 <= 0.0:
            raise SlotEvaluationError("binary64 q norm vanished")
        q_hat64 = q_array / q_norm64
        q_hat = mp_lift_numpy_vector(q_hat64)
        restore = mp_from_binary64(q_norm64)
        metadata = {
            "q_norm_binary64": q_norm64,
            "q_hat_binary64": q_hat64,
            "geometry_inputs_lifted_from_exact_binary64_ratios": True,
        }
    elif mode == "native_mpmath_geometry":
        q = mp_lift_numpy_vector(q_array)
        restore = mp_norm(q)
        if not mp.isfinite(restore) or restore <= 0:
            raise SlotEvaluationError("mpmath q norm vanished")
        q_hat = [item / restore for item in q]
        metadata = {
            "q_norm_binary64": float(np.linalg.norm(q_array)),
            "geometry_inputs_lifted_before_mpmath_normalization": True,
        }
    else:
        raise InvalidRun(f"undeclared normalization mode: {mode}")
    return q_hat, restore, metadata


def mp_endpoint(
    evaluators: ReferenceEvaluators,
    saddle_mp: Sequence[Any],
    linear_mp: mp.matrix,
    xi_mp: Sequence[Any],
    direction: Sequence[Any],
    displacement: Any,
) -> tuple[list[mp.mpc], list[mp.mpc]]:
    state = [
        mp.mpc(xi_mp[index] + displacement * direction[index])
        for index in range(7)
    ]
    flow = reference_flow(evaluators, saddle_mp, linear_mp, state)
    return state, flow


def process_base_slot(
    manifest: Mapping[str, Any],
    context: FrozenContext,
    evaluators: ReferenceEvaluators,
    point: FrozenPoint,
    fraction: str,
    direction: int,
    ledger: SlotLedger,
) -> BaseOutcome:
    base = base_key(point.label, fraction, direction)
    fraction_index = FRACTION_STRINGS.index(fraction)
    xi64 = np.asarray(point.fraction_xi[fraction_index], dtype=np.complex128)
    q64 = np.asarray(
        point.fraction_tangents[fraction_index, :, direction],
        dtype=np.complex128,
    )
    p42 = point.local_records[(fraction, direction)]
    disclosed = bool(p42["stable_violation"])
    input_key = f"input|{base}"
    q_norm64 = float(np.linalg.norm(q64))
    q_norm_reproduction = abs(q_norm64 - float(p42["q_norm"]))
    ledger.finish(
        input_key,
        "SUCCESS",
        payload={
            "point": point.label,
            "fraction": fraction,
            "direction": direction,
            "fraction_time": float(point.fraction_times[fraction_index]),
            "xi": xi64,
            "q": q64,
            "xi_binary64_identity": binary64_payload(xi64),
            "q_binary64_identity": binary64_payload(q64),
            "source_JSON_paths": {
                "xi_vector": (
                    f"$.slot_ledger['augmented|{point.label}|tight_augmented']"
                    f".payload.fraction_xi[{fraction_index}]"
                ),
                "xi_components": [
                    f"$.slot_ledger['augmented|{point.label}|tight_augmented']"
                    f".payload.fraction_xi[{fraction_index}][{row}]"
                    for row in range(7)
                ],
                "q_components": [
                    f"$.slot_ledger['augmented|{point.label}|tight_augmented']"
                    f".payload.fraction_tangents[{fraction_index}][{row}]"
                    f"[{direction}]"
                    for row in range(7)
                ],
                "phase42_local_direction_record": (
                    f"$.local_variational_diagnostics.points.{point.label}."
                    f"direction_records[{fraction_index * len(DIRECTIONS) + direction}]"
                ),
                "checkpoint_saddle_w": f"$.saddles.{point.label}.saddle_w",
                "checkpoint_linear_map": "$.fixed_metric.linear_map",
            },
            "q_norm_binary64": q_norm64,
            "stored_q_norm": float(p42["q_norm"]),
            "q_norm_reproduction_absolute": q_norm_reproduction,
            "stored_stable": bool(p42["stable"]),
            "stored_stable_violation": disclosed,
            "stored_neighbor_symmetric_relative": float(
                p42["neighbor_symmetric_relative"]
            ),
            "stored_fixed_to_analytic_symmetric_relative": float(
                p42["fixed_to_analytic_symmetric_relative"]
            ),
        },
    )

    model, saddle, fixed = source_objects(context, point)
    source_values: dict[str, Any] = {}
    source_reproduction_errors: list[float] = [q_norm_reproduction]
    analytic_key = f"source|{base}|analytic"

    def compute_source_analytic() -> tuple[np.ndarray, Mapping[str, Any]]:
        value = source_analytic_action(
            context, point, model, saddle, fixed, xi64, q64
        )
        stored = p42_vector(
            p42["analytic_hessian_action"],
            path=f"$.local.{point.label}.{fraction}.{direction}.analytic",
        )
        error = np_max_abs(value, stored)
        source_reproduction_errors.append(error)
        return value, {
            "value": value,
            "stored_phase42_value": stored,
            "reproduction_max_abs": error,
            "implementation": "-conjugate(phase41.hessian_xi@q)",
        }

    source_values["analytic"] = attempt_slot(
        ledger, analytic_key, compute_source_analytic
    )
    q_hat64: np.ndarray | None = None
    if math.isfinite(q_norm64) and q_norm64 > 0.0:
        q_hat64 = q64 / q_norm64
    source_endpoints: dict[tuple[str, int], np.ndarray] = {}
    for epsilon_text in SAME_EPSILON_STRINGS:
        for sign in (-1, 1):
            key = f"source|{base}|epsilon={epsilon_text}|sign={sign}"
            if q_hat64 is None:
                finish_dependency_failure(ledger, key, "source q norm unavailable")
                continue

            def compute_source_endpoint(
                epsilon_text: str = epsilon_text, sign: int = sign
            ) -> tuple[np.ndarray, Mapping[str, Any]]:
                epsilon = float(epsilon_text)
                state = xi64 + sign * epsilon * q_hat64
                value = source_flow(context, model, saddle, fixed, state)
                stored_payload = point.perturbation_records[
                    (fraction, direction, epsilon_text, sign)
                ]
                stored_state = p42_vector(
                    stored_payload["xi"], path=f"$.perturbation.{key}.xi"
                )
                stored_flow = p42_vector(
                    stored_payload["flow_xi"], path=f"$.perturbation.{key}.flow"
                )
                state_error = np_max_abs(state, stored_state)
                flow_error = np_max_abs(value, stored_flow)
                source_reproduction_errors.extend((state_error, flow_error))
                return value, {
                    "xi": state,
                    "flow_xi": value,
                    "stored_phase42_xi": stored_state,
                    "stored_phase42_flow_xi": stored_flow,
                    "state_reproduction_max_abs": state_error,
                    "flow_reproduction_max_abs": flow_error,
                }

            value = attempt_slot(ledger, key, compute_source_endpoint)
            if value is not None:
                source_endpoints[(epsilon_text, sign)] = value

    source_summary_key = f"source|{base}|summary"
    source_d2: dict[str, np.ndarray] = {}
    source_r4: dict[str, np.ndarray] = {}
    p42_d2_names = {
        "2e-5": "2e-05",
        "1e-5": "1e-05",
        "5e-6": "5e-06",
    }
    for epsilon_text in SAME_EPSILON_STRINGS:
        d2_key = f"source_D2|{base}|epsilon={epsilon_text}"
        if (epsilon_text, 1) not in source_endpoints or (
            epsilon_text,
            -1,
        ) not in source_endpoints:
            finish_dependency_failure(
                ledger, d2_key, "source endpoint pair unavailable"
            )
            continue

        def compute_source_d2(
            epsilon_text: str = epsilon_text,
        ) -> tuple[np.ndarray, Mapping[str, Any]]:
            epsilon = float(epsilon_text)
            value = (
                source_endpoints[(epsilon_text, 1)]
                - source_endpoints[(epsilon_text, -1)]
            ) / (2.0 * epsilon)
            if not np.all(np.isfinite(value)):
                raise SlotEvaluationError("nonfinite source D2")
            stored = p42_vector(
                p42["D2"][p42_d2_names[epsilon_text]],
                path=(
                    f"$.local.{point.label}.{fraction}.{direction}.D2."
                    f"{epsilon_text}"
                ),
            )
            error = np_max_abs(value, stored)
            source_reproduction_errors.append(error)
            return value, {
                "epsilon": epsilon_text,
                "value": value,
                "stored_phase42_value": stored,
                "reproduction_max_abs": error,
            }

        d2_value = attempt_slot(ledger, d2_key, compute_source_d2)
        if d2_value is not None:
            source_d2[epsilon_text] = d2_value

    source_r4_specs = {
        "neighbor_2e-5": (
            "1e-5",
            "2e-5",
            "R4_neighbor_2e-5",
        ),
        "fixed_1e-5": ("5e-6", "1e-5", "R4_fixed_1e-5"),
    }
    for reference, (fine, coarse, stored_field) in source_r4_specs.items():
        r4_key = f"source_R4|{base}|reference={reference}"
        if fine not in source_d2 or coarse not in source_d2:
            finish_dependency_failure(
                ledger, r4_key, "source D2 dependency unavailable"
            )
            continue

        def compute_source_r4(
            reference: str = reference,
            fine: str = fine,
            coarse: str = coarse,
            stored_field: str = stored_field,
        ) -> tuple[np.ndarray, Mapping[str, Any]]:
            value = q_norm64 * (
                4.0 * source_d2[fine] - source_d2[coarse]
            ) / 3.0
            if not np.all(np.isfinite(value)):
                raise SlotEvaluationError("nonfinite source R4")
            stored = p42_vector(
                p42[stored_field],
                path=(
                    f"$.local.{point.label}.{fraction}.{direction}."
                    f"{stored_field}"
                ),
            )
            error = np_max_abs(value, stored)
            source_reproduction_errors.append(error)
            return value, {
                "reference": reference,
                "value": value,
                "stored_phase42_value": stored,
                "reproduction_max_abs": error,
            }

        r4_value = attempt_slot(ledger, r4_key, compute_source_r4)
        if r4_value is not None:
            source_r4[reference] = r4_value

    recomputed_stable: bool | None = None
    recomputed_violation: bool | None = None
    source_ledger_reproduced = False
    if (
        source_values["analytic"] is not None
        and len(source_d2) == 3
        and len(source_r4) == 2
    ):

        def compute_source_summary() -> tuple[bool, Mapping[str, Any]]:
            nonlocal recomputed_stable, recomputed_violation
            neighbor_relative = phase42_binary64_vector_relative(
                source_r4["fixed_1e-5"], source_r4["neighbor_2e-5"]
            )
            fixed_relative = phase42_binary64_vector_relative(
                source_r4["fixed_1e-5"], source_values["analytic"]
            )
            neighbor_error = abs(
                neighbor_relative - float(p42["neighbor_symmetric_relative"])
            )
            fixed_error = abs(
                fixed_relative
                - float(p42["fixed_to_analytic_symmetric_relative"])
            )
            source_reproduction_errors.extend((neighbor_error, fixed_error))
            recomputed_stable = bool(neighbor_relative <= 1.0e-6)
            recomputed_violation = bool(
                recomputed_stable and fixed_relative > 1.0e-7
            )
            ledger_match = bool(
                recomputed_stable == bool(p42["stable"])
                and recomputed_violation == bool(p42["stable_violation"])
            )
            return True, {
                "recomputed_neighbor_symmetric_relative": neighbor_relative,
                "stored_neighbor_symmetric_relative": float(
                    p42["neighbor_symmetric_relative"]
                ),
                "neighbor_metric_reproduction_absolute": neighbor_error,
                "recomputed_fixed_to_analytic_symmetric_relative": fixed_relative,
                "stored_fixed_to_analytic_symmetric_relative": float(
                    p42["fixed_to_analytic_symmetric_relative"]
                ),
                "fixed_metric_reproduction_absolute": fixed_error,
                "recomputed_stable": recomputed_stable,
                "stored_phase42_stable": bool(p42["stable"]),
                "recomputed_stable_violation": recomputed_violation,
                "stored_phase42_stable_violation": bool(
                    p42["stable_violation"]
                ),
                "stable_and_violation_ledger_reproduced": ledger_match,
                "all_source_reproduction_max_abs": max(
                    source_reproduction_errors
                ),
            }

        summary_value = attempt_slot(
            ledger, source_summary_key, compute_source_summary
        )
        if summary_value is not None:
            source_ledger_reproduced = bool(
                recomputed_stable == bool(p42["stable"])
                and recomputed_violation == bool(p42["stable_violation"])
            )
    else:
        finish_dependency_failure(
            ledger,
            source_summary_key,
            "source analytic, D2, or R4 dependency unavailable",
        )

    hp_analytic: dict[int, list[mp.mpc]] = {}
    hp_direct: dict[int, list[mp.mpc]] = {}
    hp_rounding: dict[int, list[mp.mpc]] = {}
    same_r4: dict[tuple[int, str, str], list[mp.mpc]] = {}
    prospective_r4: dict[tuple[int, str], list[mp.mpc]] = {}
    analytic_metrics: dict[str, Any] = {}
    analytic_component_metrics: dict[str, Any] = {}
    analytic_metric_records: dict[str, Any] = {}
    analytic_component_metric_records: dict[str, Any] = {}
    same_metrics: dict[str, Any] = {}
    same_component_metrics: dict[str, Any] = {}
    same_metric_records: dict[str, Any] = {}
    same_component_metric_records: dict[str, Any] = {}
    prospective_metrics: dict[str, Any] = {}
    prospective_component_metrics: dict[str, Any] = {}
    prospective_metric_records: dict[str, Any] = {}
    prospective_component_metric_records: dict[str, Any] = {}
    for dps in PRECISIONS:
        with mp.workdps(dps):
            xi_mp = mp_lift_numpy_vector(xi64)
            q_mp = mp_lift_numpy_vector(q64)
            saddle_mp = mp_lift_numpy_vector(point.saddle_w)
            linear_mp = mp_real_matrix_from_numpy(context.linear_map)
            for method in ("hessian", "gradient_directional", "rounding_control"):
                key = f"reference|{base}|dps={dps}|method={method}"

                def compute_reference(
                    method: str = method,
                ) -> tuple[list[mp.mpc], Mapping[str, Any]]:
                    if method == "hessian":
                        value = reference_hessian_action(
                            evaluators,
                            "exact",
                            saddle_mp,
                            linear_mp,
                            xi_mp,
                            q_mp,
                        )
                    elif method == "gradient_directional":
                        value = reference_direct_action(
                            evaluators, saddle_mp, linear_mp, xi_mp, q_mp
                        )
                    else:
                        value = reference_hessian_action(
                            evaluators,
                            "source_rounding_control",
                            saddle_mp,
                            linear_mp,
                            xi_mp,
                            q_mp,
                        )
                    return value, {
                        "dps": dps,
                        "method": method,
                        "value": mp_vector_payload(value, dps),
                        "backend": "sympy.lambdify(modules='mpmath')",
                        "float_conversion_after_lift": False,
                    }

                value = attempt_slot(ledger, key, compute_reference)
                if value is not None:
                    if method == "hessian":
                        hp_analytic[dps] = value
                    elif method == "gradient_directional":
                        hp_direct[dps] = value
                    else:
                        hp_rounding[dps] = value
            if dps in hp_analytic and dps in hp_direct:
                metric_key = f"hessian_to_direct_dps_{dps}"
                analytic_metrics[metric_key] = mp_relative(
                    hp_analytic[dps], hp_direct[dps]
                )
                analytic_component_metrics[metric_key] = mp_max_component_relative(
                    hp_analytic[dps], hp_direct[dps]
                )
                analytic_metric_records[metric_key] = retained_mp_metric(
                    analytic_metrics[metric_key], dps
                )
                analytic_component_metric_records[
                    metric_key
                ] = retained_mp_metric(
                    analytic_component_metrics[metric_key], dps
                )
            if dps in hp_analytic and dps in hp_rounding:
                metric_key = f"exact_to_rounding_dps_{dps}"
                analytic_metrics[metric_key] = mp_relative(
                    hp_analytic[dps], hp_rounding[dps]
                )
                analytic_component_metrics[metric_key] = mp_max_component_relative(
                    hp_analytic[dps], hp_rounding[dps]
                )
                analytic_metric_records[metric_key] = retained_mp_metric(
                    analytic_metrics[metric_key], dps
                )
                analytic_component_metric_records[
                    metric_key
                ] = retained_mp_metric(
                    analytic_component_metrics[metric_key], dps
                )
            if dps in hp_direct and dps in hp_rounding:
                metric_key = f"direct_to_rounding_dps_{dps}"
                analytic_metrics[metric_key] = mp_relative(
                    hp_direct[dps], hp_rounding[dps]
                )
                analytic_component_metrics[metric_key] = mp_max_component_relative(
                    hp_direct[dps], hp_rounding[dps]
                )
                analytic_metric_records[metric_key] = retained_mp_metric(
                    analytic_metrics[metric_key], dps
                )
                analytic_component_metric_records[
                    metric_key
                ] = retained_mp_metric(
                    analytic_component_metrics[metric_key], dps
                )

            for mode in NORMALIZATION_MODES:
                try:
                    q_hat, restore, geometry_metadata = mp_geometry(q64, mode)
                except InvalidRun:
                    raise
                except Exception as exc:
                    reason = f"normalization failed: {type(exc).__name__}: {exc}"
                    for epsilon_text in SAME_EPSILON_STRINGS:
                        for sign in (-1, 1):
                            finish_dependency_failure(
                                ledger,
                                f"same_step|{base}|dps={dps}|mode={mode}|epsilon={epsilon_text}|sign={sign}",
                                reason,
                            )
                        finish_dependency_failure(
                            ledger,
                            f"same_step_D2|{base}|dps={dps}|mode={mode}|epsilon={epsilon_text}",
                            reason,
                        )
                    for reference in ("neighbor_2e-5", "fixed_1e-5"):
                        finish_dependency_failure(
                            ledger,
                            f"same_step_R4|{base}|dps={dps}|mode={mode}|reference={reference}",
                            reason,
                        )
                    continue
                endpoints: dict[tuple[str, int], list[mp.mpc]] = {}
                for epsilon_text in SAME_EPSILON_STRINGS:
                    for sign in (-1, 1):
                        key = f"same_step|{base}|dps={dps}|mode={mode}|epsilon={epsilon_text}|sign={sign}"

                        def compute_same_endpoint(
                            epsilon_text: str = epsilon_text, sign: int = sign
                        ) -> tuple[list[mp.mpc], Mapping[str, Any]]:
                            epsilon = mp.mpf(epsilon_text)
                            state, value = mp_endpoint(
                                evaluators,
                                saddle_mp,
                                linear_mp,
                                xi_mp,
                                q_hat,
                                sign * epsilon,
                            )
                            return value, {
                                "dps": dps,
                                "mode": mode,
                                "epsilon": epsilon_text,
                                "sign": sign,
                                "xi": mp_vector_payload(state, dps),
                                "flow_xi": mp_vector_payload(value, dps),
                                "q_norm": mp_metric_payload(restore, dps),
                                "q_hat": mp_vector_payload(q_hat, dps),
                                "geometry": {
                                    key: (
                                        json_ready(value)
                                        if not isinstance(value, (mp.mpf, mp.mpc))
                                        else mp_metric_payload(value, dps)
                                    )
                                    for key, value in geometry_metadata.items()
                                },
                            }

                        value = attempt_slot(ledger, key, compute_same_endpoint)
                        if value is not None:
                            endpoints[(epsilon_text, sign)] = value
                d2_values: dict[str, list[mp.mpc]] = {}
                for epsilon_text in SAME_EPSILON_STRINGS:
                    key = f"same_step_D2|{base}|dps={dps}|mode={mode}|epsilon={epsilon_text}"
                    if (epsilon_text, -1) not in endpoints or (
                        epsilon_text,
                        1,
                    ) not in endpoints:
                        finish_dependency_failure(
                            ledger, key, "same-step endpoint pair unavailable"
                        )
                        continue
                    def compute_same_d2(
                        epsilon_text: str = epsilon_text,
                    ) -> tuple[list[mp.mpc], Mapping[str, Any]]:
                        epsilon = mp.mpf(epsilon_text)
                        d2 = finite_mp_vector(
                            central_D2(
                                endpoints[(epsilon_text, 1)],
                                endpoints[(epsilon_text, -1)],
                                epsilon,
                            ),
                            label="same-step high-precision D2",
                        )
                        return d2, {
                            "dps": dps,
                            "mode": mode,
                            "epsilon": epsilon_text,
                            "D2": mp_vector_payload(d2, dps),
                        }

                    d2 = attempt_slot(ledger, key, compute_same_d2)
                    if d2 is not None:
                        d2_values[epsilon_text] = d2
                r4_specs = {
                    "neighbor_2e-5": ("1e-5", "2e-5"),
                    "fixed_1e-5": ("5e-6", "1e-5"),
                }
                for reference, (fine, coarse) in r4_specs.items():
                    key = f"same_step_R4|{base}|dps={dps}|mode={mode}|reference={reference}"
                    if fine not in d2_values or coarse not in d2_values:
                        finish_dependency_failure(
                            ledger, key, "same-step D2 dependency unavailable"
                        )
                        continue
                    def compute_same_r4(
                        reference: str = reference,
                        fine: str = fine,
                        coarse: str = coarse,
                    ) -> tuple[
                        tuple[list[mp.mpc], mp.mpf | None, mp.mpf | None],
                        Mapping[str, Any],
                    ]:
                        r4 = finite_mp_vector(
                            restored_R4(
                                d2_values[fine], d2_values[coarse], restore
                            ),
                            label="same-step high-precision R4",
                        )
                        to_analytic = (
                            mp_relative(r4, hp_analytic[dps])
                            if dps in hp_analytic
                            else None
                        )
                        component = (
                            mp_max_component_relative(r4, hp_analytic[dps])
                            if dps in hp_analytic
                            else None
                        )
                        return (r4, to_analytic, component), {
                            "dps": dps,
                            "mode": mode,
                            "reference": reference,
                            "R4": mp_vector_payload(r4, dps),
                            "to_symbolic_hessian_relative": (
                                mp_metric_payload(to_analytic, dps)
                                if to_analytic is not None
                                else None
                            ),
                            "to_symbolic_hessian_max_component_relative": (
                                mp_metric_payload(component, dps)
                                if component is not None
                                else None
                            ),
                        }

                    computed_r4 = attempt_slot(ledger, key, compute_same_r4)
                    if computed_r4 is not None:
                        r4, to_analytic, component = computed_r4
                        same_r4[(dps, mode, reference)] = r4
                    else:
                        to_analytic = None
                        component = None
                    if to_analytic is not None and component is not None:
                        metric_key = (
                            f"dps={dps}|mode={mode}|reference={reference}"
                        )
                        same_metrics[metric_key] = to_analytic
                        same_component_metrics[metric_key] = component
                        same_metric_records[metric_key] = retained_mp_metric(
                            same_metrics[metric_key], dps
                        )
                        same_component_metric_records[
                            metric_key
                        ] = retained_mp_metric(
                            same_component_metrics[metric_key], dps
                        )

            try:
                q_hat_native, restore_native, native_metadata = mp_geometry(
                    q64, "native_mpmath_geometry"
                )
            except InvalidRun:
                raise
            except Exception as exc:
                reason = f"prospective normalization failed: {type(exc).__name__}: {exc}"
                for h_text in PROSPECTIVE_H_STRINGS:
                    for offset in PROSPECTIVE_OFFSETS:
                        finish_dependency_failure(
                            ledger,
                            f"prospective|{base}|dps={dps}|h={h_text}|offset={offset}",
                            reason,
                        )
                    for scale in ("h", "h/2"):
                        finish_dependency_failure(
                            ledger,
                            f"prospective_D2|{base}|dps={dps}|h={h_text}|scale={scale}",
                            reason,
                        )
                    finish_dependency_failure(
                        ledger,
                        f"prospective_R4|{base}|dps={dps}|h={h_text}",
                        reason,
                    )
                continue
            for h_text in PROSPECTIVE_H_STRINGS:
                h = mp.mpf(h_text)
                displacement_by_offset = {
                    "h": h,
                    "h/2": h / mp.mpf(2),
                    "-h/2": -h / mp.mpf(2),
                    "-h": -h,
                }
                endpoints: dict[str, list[mp.mpc]] = {}
                for offset in PROSPECTIVE_OFFSETS:
                    key = f"prospective|{base}|dps={dps}|h={h_text}|offset={offset}"

                    def compute_prospective_endpoint(
                        offset: str = offset,
                    ) -> tuple[list[mp.mpc], Mapping[str, Any]]:
                        state, value = mp_endpoint(
                            evaluators,
                            saddle_mp,
                            linear_mp,
                            xi_mp,
                            q_hat_native,
                            displacement_by_offset[offset],
                        )
                        return value, {
                            "dps": dps,
                            "normalization_mode": "native_mpmath_geometry",
                            "h": h_text,
                            "offset": offset,
                            "xi": mp_vector_payload(state, dps),
                            "flow_xi": mp_vector_payload(value, dps),
                            "q_norm": mp_metric_payload(restore_native, dps),
                            "q_hat": mp_vector_payload(q_hat_native, dps),
                            "geometry": {
                                key: (
                                    json_ready(value)
                                    if not isinstance(value, (mp.mpf, mp.mpc))
                                    else mp_metric_payload(value, dps)
                                )
                                for key, value in native_metadata.items()
                            },
                        }

                    value = attempt_slot(
                        ledger, key, compute_prospective_endpoint
                    )
                    if value is not None:
                        endpoints[offset] = value
                d2_values: dict[str, list[mp.mpc]] = {}
                d2_dependencies = {
                    "h": ("h", "-h", h),
                    "h/2": ("h/2", "-h/2", h / mp.mpf(2)),
                }
                for scale, (plus, minus, epsilon) in d2_dependencies.items():
                    key = f"prospective_D2|{base}|dps={dps}|h={h_text}|scale={scale}"
                    if plus not in endpoints or minus not in endpoints:
                        finish_dependency_failure(
                            ledger, key, "prospective endpoint pair unavailable"
                        )
                        continue
                    def compute_prospective_d2(
                        scale: str = scale,
                        plus: str = plus,
                        minus: str = minus,
                        epsilon: mp.mpf = epsilon,
                    ) -> tuple[list[mp.mpc], Mapping[str, Any]]:
                        d2 = finite_mp_vector(
                            central_D2(
                                endpoints[plus], endpoints[minus], epsilon
                            ),
                            label="prospective high-precision D2",
                        )
                        return d2, {
                            "dps": dps,
                            "h": h_text,
                            "scale": scale,
                            "D2": mp_vector_payload(d2, dps),
                        }

                    d2 = attempt_slot(ledger, key, compute_prospective_d2)
                    if d2 is not None:
                        d2_values[scale] = d2
                r4_key = f"prospective_R4|{base}|dps={dps}|h={h_text}"
                if "h" not in d2_values or "h/2" not in d2_values:
                    finish_dependency_failure(
                        ledger, r4_key, "prospective D2 dependency unavailable"
                    )
                    continue
                def compute_prospective_r4() -> tuple[
                    tuple[list[mp.mpc], mp.mpf | None, mp.mpf | None],
                    Mapping[str, Any],
                ]:
                    r4 = finite_mp_vector(
                        restored_R4(
                            d2_values["h/2"],
                            d2_values["h"],
                            restore_native,
                        ),
                        label="prospective high-precision R4",
                    )
                    to_analytic = (
                        mp_relative(r4, hp_analytic[dps])
                        if dps in hp_analytic
                        else None
                    )
                    component = (
                        mp_max_component_relative(r4, hp_analytic[dps])
                        if dps in hp_analytic
                        else None
                    )
                    return (r4, to_analytic, component), {
                        "dps": dps,
                        "normalization_mode": "native_mpmath_geometry",
                        "h": h_text,
                        "R4": mp_vector_payload(r4, dps),
                        "to_symbolic_hessian_relative": (
                            mp_metric_payload(to_analytic, dps)
                            if to_analytic is not None
                            else None
                        ),
                        "to_symbolic_hessian_max_component_relative": (
                            mp_metric_payload(component, dps)
                            if component is not None
                            else None
                        ),
                    }

                computed_r4 = attempt_slot(
                    ledger, r4_key, compute_prospective_r4
                )
                if computed_r4 is not None:
                    r4, to_analytic, component = computed_r4
                    prospective_r4[(dps, h_text)] = r4
                else:
                    to_analytic = None
                    component = None
                if to_analytic is not None and component is not None:
                    metric_key = f"dps={dps}|h={h_text}"
                    prospective_metrics[metric_key] = to_analytic
                    prospective_component_metrics[metric_key] = component
                    prospective_metric_records[metric_key] = retained_mp_metric(
                        prospective_metrics[metric_key], dps
                    )
                    prospective_component_metric_records[
                        metric_key
                    ] = retained_mp_metric(
                        prospective_component_metrics[metric_key], dps
                    )

    source_reproduction_complete = bool(
        source_values["analytic"] is not None
        and len(source_endpoints) == 6
        and len(source_d2) == 3
        and len(source_r4) == 2
        and ledger.slots[source_summary_key]["terminal_status"] == "SUCCESS"
        and len(source_reproduction_errors) == 21
    )
    reproduction_max = (
        max(source_reproduction_errors)
        if source_reproduction_complete
        else None
    )
    with mp.workdps(120):
        thresholds = {
            key: mp.mpf(value)
            for key, value in manifest["acceptance_thresholds"].items()
            if isinstance(value, str) and key != "threshold_policy"
        }
        if 80 in hp_analytic and 120 in hp_analytic:
            analytic_metrics["hessian_80_to_120"] = mp_relative(
                hp_analytic[80], hp_analytic[120]
            )
            analytic_component_metrics[
                "hessian_80_to_120"
            ] = mp_max_component_relative(hp_analytic[80], hp_analytic[120])
            analytic_metric_records[
                "hessian_80_to_120"
            ] = retained_mp_metric(analytic_metrics["hessian_80_to_120"], 120)
            analytic_component_metric_records[
                "hessian_80_to_120"
            ] = retained_mp_metric(
                analytic_component_metrics["hessian_80_to_120"], 120
            )
        if 80 in hp_direct and 120 in hp_direct:
            analytic_metrics["direct_80_to_120"] = mp_relative(
                hp_direct[80], hp_direct[120]
            )
            analytic_component_metrics[
                "direct_80_to_120"
            ] = mp_max_component_relative(hp_direct[80], hp_direct[120])
            analytic_metric_records["direct_80_to_120"] = retained_mp_metric(
                analytic_metrics["direct_80_to_120"], 120
            )
            analytic_component_metric_records[
                "direct_80_to_120"
            ] = retained_mp_metric(
                analytic_component_metrics["direct_80_to_120"], 120
            )
        if 80 in hp_rounding and 120 in hp_rounding:
            analytic_metrics["rounding_80_to_120"] = mp_relative(
                hp_rounding[80], hp_rounding[120]
            )
            analytic_component_metrics[
                "rounding_80_to_120"
            ] = mp_max_component_relative(hp_rounding[80], hp_rounding[120])
            analytic_metric_records[
                "rounding_80_to_120"
            ] = retained_mp_metric(analytic_metrics["rounding_80_to_120"], 120)
            analytic_component_metric_records[
                "rounding_80_to_120"
            ] = retained_mp_metric(
                analytic_component_metrics["rounding_80_to_120"], 120
            )

        same_precision_metrics: dict[str, mp.mpf] = {}
        same_precision_component_metrics: dict[str, mp.mpf] = {}
        for mode in NORMALIZATION_MODES:
            for reference in ("neighbor_2e-5", "fixed_1e-5"):
                low_key = (80, mode, reference)
                high_key = (120, mode, reference)
                metric_key = f"mode={mode}|reference={reference}"
                if low_key in same_r4 and high_key in same_r4:
                    same_precision_metrics[metric_key] = mp_relative(
                        same_r4[low_key], same_r4[high_key]
                    )
                    same_precision_component_metrics[
                        metric_key
                    ] = mp_max_component_relative(
                        same_r4[low_key], same_r4[high_key]
                    )
        prospective_precision_metrics: dict[str, mp.mpf] = {}
        prospective_precision_component_metrics: dict[str, mp.mpf] = {}
        for h_text in PROSPECTIVE_H_STRINGS:
            low_key = (80, h_text)
            high_key = (120, h_text)
            if low_key in prospective_r4 and high_key in prospective_r4:
                prospective_precision_metrics[h_text] = mp_relative(
                    prospective_r4[low_key], prospective_r4[high_key]
                )
                prospective_precision_component_metrics[
                    h_text
                ] = mp_max_component_relative(
                    prospective_r4[low_key], prospective_r4[high_key]
                )

        required_analytic_metric_keys = {
            "hessian_to_direct_dps_80",
            "hessian_to_direct_dps_120",
            "exact_to_rounding_dps_80",
            "exact_to_rounding_dps_120",
            "direct_to_rounding_dps_80",
            "direct_to_rounding_dps_120",
            "hessian_80_to_120",
            "direct_80_to_120",
            "rounding_80_to_120",
        }
        analytic_complete = bool(
            required_analytic_metric_keys <= set(analytic_metrics)
            and required_analytic_metric_keys <= set(analytic_component_metrics)
        )
        analytic_pass = bool(
            analytic_complete
            and analytic_metrics["hessian_to_direct_dps_80"]
            <= thresholds["symbolic_hessian_vs_gradient_directional_relative_max"]
            and analytic_metrics["hessian_to_direct_dps_120"]
            <= thresholds["symbolic_hessian_vs_gradient_directional_relative_max"]
            and analytic_metrics["exact_to_rounding_dps_80"]
            <= thresholds[
                "source_rounding_control_vs_independent_exact_decimal_relative_max"
            ]
            and analytic_metrics["exact_to_rounding_dps_120"]
            <= thresholds[
                "source_rounding_control_vs_independent_exact_decimal_relative_max"
            ]
            and all(
                analytic_metrics[key]
                <= thresholds["80_vs_120_precision_stability_relative_max"]
                for key in (
                    "hessian_80_to_120",
                    "direct_80_to_120",
                    "rounding_80_to_120",
                )
            )
        )

        same_all_required = [
            (dps, mode, reference)
            for dps in PRECISIONS
            for mode in NORMALIZATION_MODES
            for reference in ("neighbor_2e-5", "fixed_1e-5")
        ]
        same_authoritative_required = [
            (120, mode, reference)
            for mode in NORMALIZATION_MODES
            for reference in ("neighbor_2e-5", "fixed_1e-5")
        ]
        same_precision_required = {
            f"mode={mode}|reference={reference}"
            for mode in NORMALIZATION_MODES
            for reference in ("neighbor_2e-5", "fixed_1e-5")
        }
        same_complete = bool(
            all(key in same_r4 for key in same_all_required)
            and same_precision_required <= set(same_precision_metrics)
            and 120 in hp_analytic
        )
        same_pass = bool(
            same_complete
            and all(
                mp_relative(same_r4[key], hp_analytic[120])
                <= thresholds["same_step_high_precision_R4_to_symbolic_relative_max"]
                for key in same_authoritative_required
            )
            and all(
                same_precision_metrics[key]
                <= thresholds["80_vs_120_precision_stability_relative_max"]
                for key in same_precision_required
            )
        )

        all_prospective_complete = all(
            (dps, h_text) in prospective_r4
            for dps in PRECISIONS
            for h_text in PROSPECTIVE_H_STRINGS
        )
        prospective_precision_complete = set(
            prospective_precision_metrics
        ) == set(PROSPECTIVE_H_STRINGS)
        primary_key = (120, "1e-12")
        coarse_key = (120, "1e-10")
        fine_key = (120, "1e-14")
        prospective_fixed_complete = (
            primary_key in prospective_r4
            and coarse_key in prospective_r4
            and fine_key in prospective_r4
            and 120 in hp_analytic
        )
        primary_error: mp.mpf | None = None
        primary_component_error: mp.mpf | None = None
        neighbor_stability: mp.mpf | None = None
        neighbor_component_stability: mp.mpf | None = None
        if prospective_fixed_complete:
            primary_error = mp_relative(
                prospective_r4[primary_key], hp_analytic[120]
            )
            primary_component_error = mp_max_component_relative(
                prospective_r4[primary_key], hp_analytic[120]
            )
            neighbor_stability = max(
                mp_relative(
                    prospective_r4[primary_key], prospective_r4[coarse_key]
                ),
                mp_relative(
                    prospective_r4[primary_key], prospective_r4[fine_key]
                ),
            )
            neighbor_component_stability = max(
                mp_max_component_relative(
                    prospective_r4[primary_key], prospective_r4[coarse_key]
                ),
                mp_max_component_relative(
                    prospective_r4[primary_key], prospective_r4[fine_key]
                ),
            )
        prospective_complete = bool(
            all_prospective_complete
            and prospective_precision_complete
            and prospective_fixed_complete
        )
        prospective_pass = bool(
            prospective_complete
            and primary_error is not None
            and primary_error
            <= thresholds["small_step_primary_R4_to_symbolic_relative_max"]
            and neighbor_stability is not None
            and neighbor_stability
            <= thresholds["small_step_reference_neighbor_relative_max"]
            and all(
                prospective_precision_metrics[h_text]
                <= thresholds["80_vs_120_precision_stability_relative_max"]
                for h_text in PROSPECTIVE_H_STRINGS
            )
        )
        reference_complete = bool(
            analytic_complete and same_complete and prospective_complete
        )
        reference_pass = bool(
            reference_complete and analytic_pass and same_pass and prospective_pass
        )
        reference_completion = (
            "COMPLETE" if reference_complete else "INCOMPLETE"
        )
        reference_status = (
            "CORROBORATED" if reference_pass else "INCONCLUSIVE"
        )

        reproduction_pass = bool(
            source_reproduction_complete
            and reproduction_max is not None
            and mp_from_binary64(reproduction_max)
            <= thresholds["phase42_source_vector_reproduction_max_abs"]
            and source_ledger_reproduced
        )
        source_to_reference: mp.mpf | None = None
        source_to_reference_component: mp.mpf | None = None
        if source_values["analytic"] is not None and 120 in hp_analytic:
            lifted_source = mp_lift_numpy_vector(source_values["analytic"])
            source_to_reference = mp_relative(
                lifted_source, hp_analytic[120]
            )
            source_to_reference_component = mp_max_component_relative(
                lifted_source, hp_analytic[120]
            )
        source_complete = bool(
            source_reproduction_complete
            and reference_complete
            and source_to_reference is not None
        )
        source_completion = "COMPLETE" if source_complete else "INCOMPLETE"
        if not source_complete or not reproduction_pass or not reference_pass:
            source_evidence = "INCONCLUSIVE"
        elif source_to_reference <= thresholds[
            "source_numpy64_hessian_action_to_high_precision_relative_max"
        ]:
            source_evidence = "NOT_SUPPORTED"
        else:
            source_evidence = "SUPPORTED"

        same_fixed_keys = [
            (120, mode, "fixed_1e-5") for mode in NORMALIZATION_MODES
        ]
        fd_complete = bool(
            source_complete
            and reference_complete
            and all(key in same_r4 for key in same_fixed_keys)
        )
        if not disclosed:
            double_fd_completion = "COMPLETE" if fd_complete else "INCOMPLETE"
            if not fd_complete or not reproduction_pass or not reference_pass:
                double_fd_evidence = "INCONCLUSIVE"
                double_fd_rationale = (
                    "OUTSIDE_DISCLOSED_COHORT_AND_REQUIRED_LOCAL_PREREQUISITE_"
                    "INCOMPLETE_OR_INCONCLUSIVE; excluded from 33-slot aggregate"
                )
            else:
                double_fd_evidence = "NOT_SUPPORTED"
                double_fd_rationale = (
                    "OUTSIDE_DISCLOSED_33_SLOT_STABLE_VIOLATION_COHORT; all "
                    "local prerequisites complete, retained but excluded from "
                    "the quantified anomaly aggregate"
                )
        else:
            double_fd_completion = "COMPLETE" if fd_complete else "INCOMPLETE"
            if not fd_complete or not reproduction_pass or not reference_pass:
                double_fd_evidence = "INCONCLUSIVE"
                double_fd_rationale = (
                    "SOURCE_REPRODUCTION_OR_INDEPENDENT_REFERENCE_PREREQUISITE_"
                    "INCOMPLETE_OR_INCONCLUSIVE"
                )
            else:
                stored_violation = bool(
                    disclosed
                    and mp_from_binary64(
                        float(p42["fixed_to_analytic_symmetric_relative"])
                    )
                    > thresholds[
                        "phase42_stable_violation_threshold_reproduced"
                    ]
                    and mp_from_binary64(
                        float(p42["neighbor_symmetric_relative"])
                    )
                    <= thresholds[
                        "phase42_reference_stability_threshold_reproduced"
                    ]
                )
                hp_same_pass = all(
                    mp_relative(same_r4[key], hp_analytic[120])
                    <= thresholds[
                        "same_step_high_precision_R4_to_symbolic_relative_max"
                    ]
                    for key in same_fixed_keys
                )
                conjunction = bool(
                    stored_violation
                    and source_evidence == "NOT_SUPPORTED"
                    and hp_same_pass
                )
                double_fd_evidence = (
                    "SUPPORTED" if conjunction else "NOT_SUPPORTED"
                )
                double_fd_rationale = (
                    "SAME_STEPS_HIGH_PRECISION_CORROBORATE_REFERENCE"
                    if conjunction
                    else "ALL_PREREQUISITES_COMPLETE_BUT_FROZEN_CONJUNCTION_FALSE"
                )

        improvement_ratios: dict[str, mp.mpf] = {}
        for mode in NORMALIZATION_MODES:
            for reference in ("neighbor_2e-5", "fixed_1e-5"):
                metric_key = (
                    f"dps=120|mode={mode}|reference={reference}"
                )
                if metric_key in same_metrics:
                    improvement_ratios[
                        f"mode={mode}|reference={reference}"
                    ] = mp_from_binary64(
                        float(p42["fixed_to_analytic_symmetric_relative"])
                    ) / max(same_metrics[metric_key], mp.mpf("1e-100"))

        reference_key = f"classification|{base}|kind=reference"
        source_class_key = f"classification|{base}|kind=source_RHS"
        fd_class_key = f"classification|{base}|kind=double_FD"
        reference_metric_paths = [
            f"reference|{base}|dps={dps}|method={method}"
            for dps in PRECISIONS
            for method in ("hessian", "gradient_directional", "rounding_control")
        ] + [
            f"same_step_R4|{base}|dps={dps}|mode={mode}|reference={reference}"
            for dps in PRECISIONS
            for mode in NORMALIZATION_MODES
            for reference in ("neighbor_2e-5", "fixed_1e-5")
        ] + [
            f"prospective_R4|{base}|dps={dps}|h={h_text}"
            for dps in PRECISIONS
            for h_text in PROSPECTIVE_H_STRINGS
        ]
        source_metric_paths = [
            analytic_key,
            *[
                f"source_D2|{base}|epsilon={epsilon}"
                for epsilon in SAME_EPSILON_STRINGS
            ],
            *[
                f"source_R4|{base}|reference={reference}"
                for reference in ("neighbor_2e-5", "fixed_1e-5")
            ],
            source_summary_key,
            *reference_metric_paths,
        ]
        fd_metric_paths = [
            source_summary_key,
            *[
                f"source_R4|{base}|reference={reference}"
                for reference in ("neighbor_2e-5", "fixed_1e-5")
            ],
            *[
                f"same_step_R4|{base}|dps=120|mode={mode}|reference=fixed_1e-5"
                for mode in NORMALIZATION_MODES
            ],
            source_class_key,
            reference_key,
        ]
        ledger.finish(
            reference_key,
            "SUCCESS",
            payload={
                "completion": reference_completion,
                "evidence_status": reference_status,
                "analytic_path_passed": analytic_pass,
                "same_step_passed": same_pass,
                "prospective_passed": prospective_pass,
                "analytic_symmetric_relative": analytic_metric_records,
                "analytic_max_component_relative": (
                    analytic_component_metric_records
                ),
                "same_step_to_reference_symmetric_relative": (
                    same_metric_records
                ),
                "same_step_to_reference_max_component_relative": (
                    same_component_metric_records
                ),
                "same_step_80_vs_120_precision_stability_relative": {
                    key: retained_mp_metric(value, 120)
                    for key, value in same_precision_metrics.items()
                },
                "same_step_80_vs_120_max_component_relative": {
                    key: retained_mp_metric(value, 120)
                    for key, value in same_precision_component_metrics.items()
                },
                "prospective_to_reference_symmetric_relative": (
                    prospective_metric_records
                ),
                "prospective_to_reference_max_component_relative": (
                    prospective_component_metric_records
                ),
                "prospective_80_vs_120_precision_stability_relative": {
                    key: retained_mp_metric(value, 120)
                    for key, value in prospective_precision_metrics.items()
                },
                "prospective_80_vs_120_max_component_relative": {
                    key: retained_mp_metric(value, 120)
                    for key, value in prospective_precision_component_metrics.items()
                },
                "primary_R4_to_symbolic_relative": (
                    retained_mp_metric(primary_error, 120)
                    if primary_error is not None
                    else None
                ),
                "primary_R4_to_symbolic_max_component_relative": (
                    retained_mp_metric(primary_component_error, 120)
                    if primary_component_error is not None
                    else None
                ),
                "reference_neighbor_stability": (
                    retained_mp_metric(neighbor_stability, 120)
                    if neighbor_stability is not None
                    else None
                ),
                "reference_neighbor_max_component_stability": (
                    retained_mp_metric(neighbor_component_stability, 120)
                    if neighbor_component_stability is not None
                    else None
                ),
                "old_to_high_precision_improvement_ratio": {
                    key: retained_mp_metric(value, 120)
                    for key, value in improvement_ratios.items()
                },
                "metric_paths": reference_metric_paths,
            },
        )
        ledger.finish(
            source_class_key,
            "SUCCESS",
            payload={
                "completion": source_completion,
                "evidence_status": source_evidence,
                "source_reproduction_complete": source_reproduction_complete,
                "source_reproduction_passed": reproduction_pass,
                "source_to_high_precision_relative": (
                    retained_mp_metric(source_to_reference, 120)
                    if source_to_reference is not None
                    else None
                ),
                "source_to_high_precision_max_component_relative": (
                    retained_mp_metric(source_to_reference_component, 120)
                    if source_to_reference_component is not None
                    else None
                ),
                "metric_paths": source_metric_paths,
                "interpretation": (
                    "local RHS implementation used by the integrated tangent; "
                    "integrated evolution itself is not tested"
                ),
            },
        )
        ledger.finish(
            fd_class_key,
            "SUCCESS",
            payload={
                "completion": double_fd_completion,
                "evidence_status": double_fd_evidence,
                "disclosed_anomaly_cohort": disclosed,
                "quantified_in_33_slot_aggregate": disclosed,
                "rationale": double_fd_rationale,
                "stored_phase42_fixed_to_analytic_relative": float(
                    p42["fixed_to_analytic_symmetric_relative"]
                ),
                "stored_phase42_neighbor_relative": float(
                    p42["neighbor_symmetric_relative"]
                ),
                "metric_paths": fd_metric_paths,
            },
        )
        source_relative_string = (
            retained_mp_metric(source_to_reference, 120)
            if source_to_reference is not None
            else None
        )
    return BaseOutcome(
        point=point.label,
        fraction=fraction,
        direction=direction,
        disclosed_anomaly=disclosed,
        source_reproduction_passed=reproduction_pass,
        independent_reference_passed=analytic_pass,
        r4_reference_passed=bool(same_pass and prospective_pass),
        reference_completion=reference_completion,
        source_rhs_completion=source_completion,
        double_fd_completion=double_fd_completion,
        reference_status=reference_status,
        source_rhs_evidence=source_evidence,
        double_fd_evidence=double_fd_evidence,
        source_reproduction_max_abs=reproduction_max,
        source_to_reference_relative=source_relative_string,
        metric_paths={
            "reference": (reference_key, *reference_metric_paths),
            "source_RHS": (source_class_key, *source_metric_paths),
            "double_FD": (fd_class_key, *fd_metric_paths),
        },
    )


def aggregate_local_outcomes(
    manifest: Mapping[str, Any],
    outcomes: Sequence[BaseOutcome],
    ledger: SlotLedger,
) -> dict[str, Any]:
    if len(outcomes) != 90:
        raise InvalidRun(f"base-outcome count {len(outcomes)} != 90")
    identity = {
        (outcome.point, outcome.fraction, outcome.direction)
        for outcome in outcomes
    }
    expected_identity = {
        (point, fraction, direction)
        for point in TARGETS
        for fraction in FRACTION_STRINGS
        for direction in DIRECTIONS
    }
    if identity != expected_identity:
        raise InvalidRun("base-outcome identity set drift")

    point_payloads: dict[str, dict[str, Any]] = {}
    for point in TARGETS:
        point_outcomes = [item for item in outcomes if item.point == point]
        anomaly_outcomes = [
            item for item in point_outcomes if item.disclosed_anomaly
        ]
        expected_anomalies = int(
            manifest["known_phase42_negative_control"][
                "stable_violation_counts"
            ][point]
        )
        if len(point_outcomes) != 30 or len(anomaly_outcomes) != expected_anomalies:
            raise InvalidRun(f"point aggregation cardinality drift: {point}")

        reference_complete = all(
            item.reference_completion == "COMPLETE" for item in point_outcomes
        )
        reference_evidence = (
            "CORROBORATED"
            if reference_complete
            and all(item.reference_status == "CORROBORATED" for item in point_outcomes)
            else "INCONCLUSIVE"
        )
        reference_key = f"point_aggregate|point={point}|kind=reference"
        ledger.finish(
            reference_key,
            "SUCCESS",
            payload={
                "completion": "COMPLETE" if reference_complete else "INCOMPLETE",
                "evidence_status": reference_evidence,
                "quantifier": "CORROBORATED iff all thirty slots are complete and corroborated",
                "base_classification_paths": [
                    f"classification|{base_key(point, item.fraction, item.direction)}|kind=reference"
                    for item in point_outcomes
                ],
            },
        )

        source_complete = all(
            item.source_rhs_completion == "COMPLETE" for item in point_outcomes
        )
        if any(
            item.source_rhs_completion == "COMPLETE"
            and item.source_rhs_evidence == "SUPPORTED"
            for item in point_outcomes
        ):
            source_evidence = "SUPPORTED"
        elif source_complete and all(
            item.source_rhs_evidence == "NOT_SUPPORTED" for item in point_outcomes
        ):
            source_evidence = "NOT_SUPPORTED"
        else:
            source_evidence = "INCONCLUSIVE"
        source_key = f"point_aggregate|point={point}|kind=source_RHS"
        ledger.finish(
            source_key,
            "SUCCESS",
            payload={
                "completion": "COMPLETE" if source_complete else "INCOMPLETE",
                "evidence_status": source_evidence,
                "quantifier": (
                    "SUPPORTED if any complete slot supports; NOT_SUPPORTED only "
                    "if all thirty complete slots do not support"
                ),
                "base_classification_paths": [
                    f"classification|{base_key(point, item.fraction, item.direction)}|kind=source_RHS"
                    for item in point_outcomes
                ],
            },
        )

        fd_complete = all(
            item.double_fd_completion == "COMPLETE"
            for item in anomaly_outcomes
        )
        if fd_complete and all(
            item.double_fd_evidence == "SUPPORTED" for item in anomaly_outcomes
        ):
            fd_evidence = "SUPPORTED"
        elif fd_complete and any(
            item.double_fd_evidence == "NOT_SUPPORTED" for item in anomaly_outcomes
        ):
            fd_evidence = "NOT_SUPPORTED"
        else:
            fd_evidence = "INCONCLUSIVE"
        fd_key = f"point_aggregate|point={point}|kind=double_FD"
        ledger.finish(
            fd_key,
            "SUCCESS",
            payload={
                "completion": "COMPLETE" if fd_complete else "INCOMPLETE",
                "evidence_status": fd_evidence,
                "quantified_disclosed_slot_count": len(anomaly_outcomes),
                "excluded_noncohort_slot_count": 30 - len(anomaly_outcomes),
                "quantifier": (
                    "SUPPORTED iff every disclosed stable-violation slot is "
                    "complete and supported; noncohort slots are retained but excluded"
                ),
                "base_classification_paths": [
                    f"classification|{base_key(point, item.fraction, item.direction)}|kind=double_FD"
                    for item in anomaly_outcomes
                ],
            },
        )
        point_payloads[point] = {
            "reference": {
                "completion": "COMPLETE" if reference_complete else "INCOMPLETE",
                "evidence_status": reference_evidence,
                "ledger_path": reference_key,
            },
            "source_RHS": {
                "completion": "COMPLETE" if source_complete else "INCOMPLETE",
                "evidence_status": source_evidence,
                "ledger_path": source_key,
            },
            "double_FD_disclosed_anomalies_only": {
                "completion": "COMPLETE" if fd_complete else "INCOMPLETE",
                "evidence_status": fd_evidence,
                "disclosed_slot_count": len(anomaly_outcomes),
                "ledger_path": fd_key,
            },
        }

    all_source_complete = all(
        item.source_rhs_completion == "COMPLETE" for item in outcomes
    )
    if any(
        item.source_rhs_completion == "COMPLETE"
        and item.source_rhs_evidence == "SUPPORTED"
        for item in outcomes
    ):
        global_source = "SUPPORTED"
    elif all_source_complete and all(
        item.source_rhs_evidence == "NOT_SUPPORTED" for item in outcomes
    ):
        global_source = "NOT_SUPPORTED"
    else:
        global_source = "INCONCLUSIVE"
    source_global_key = (
        "global_aggregate|kind=LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE"
    )
    ledger.finish(
        source_global_key,
        "SUCCESS",
        payload={
            "completion": "COMPLETE" if all_source_complete else "INCOMPLETE",
            "evidence_status": global_source,
            "quantified_slot_count": 90,
            "point_aggregate_paths": [
                f"point_aggregate|point={point}|kind=source_RHS"
                for point in TARGETS
            ],
        },
    )

    anomaly_outcomes = [item for item in outcomes if item.disclosed_anomaly]
    if len(anomaly_outcomes) != 33:
        raise InvalidRun("global disclosed anomaly count is not 33")
    all_fd_complete = all(
        item.double_fd_completion == "COMPLETE" for item in anomaly_outcomes
    )
    if all_fd_complete and all(
        item.double_fd_evidence == "SUPPORTED" for item in anomaly_outcomes
    ):
        global_fd = "SUPPORTED"
    elif all_fd_complete and any(
        item.double_fd_evidence == "NOT_SUPPORTED" for item in anomaly_outcomes
    ):
        global_fd = "NOT_SUPPORTED"
    else:
        global_fd = "INCONCLUSIVE"
    fd_global_key = (
        "global_aggregate|kind="
        "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES"
    )
    ledger.finish(
        fd_global_key,
        "SUCCESS",
        payload={
            "completion": "COMPLETE" if all_fd_complete else "INCOMPLETE",
            "evidence_status": global_fd,
            "quantified_disclosed_slot_count": 33,
            "excluded_noncohort_slot_count": 57,
            "point_aggregate_paths": [
                f"point_aggregate|point={point}|kind=double_FD"
                for point in TARGETS
            ],
        },
    )

    if global_source == "SUPPORTED":
        arbitration = "LOCAL_RHS_IMPLEMENTATION_MISMATCH_SUPPORTED"
    elif global_source == "NOT_SUPPORTED" and global_fd == "SUPPORTED":
        arbitration = "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_SUPPORTED"
    else:
        arbitration = "MIXED_OR_INCONCLUSIVE"
    arbitration_key = "global_aggregate|kind=PHASE43_LOCAL_ARBITRATION"
    ledger.finish(
        arbitration_key,
        "SUCCESS",
        payload={
            "completion": (
                "COMPLETE"
                if all_source_complete and all_fd_complete
                else "INCOMPLETE"
            ),
            "evidence_status": arbitration,
            "no_forced_unique_cause": True,
            "source_RHS_path": source_global_key,
            "double_FD_path": fd_global_key,
        },
    )
    integrated_key = "global_aggregate|kind=INTEGRATED_TANGENT_EVOLUTION"
    ledger.finish(
        integrated_key,
        "SUCCESS",
        payload={
            "completion": "NOT_TESTED_LOCAL_ONLY",
            "evidence_status": "NOT_TESTED_LOCAL_ONLY",
            "time_column_evaluations": 0,
            "integrated_tangent_evaluations": 0,
        },
    )
    ode_key = "global_aggregate|kind=ODE_SOLVER_NOISE_COMPONENT"
    ledger.finish(
        ode_key,
        "SUCCESS",
        payload={
            "completion": "NOT_TESTED_LOCAL_ONLY",
            "evidence_status": "NOT_TESTED_LOCAL_ONLY",
            "ODE_solver_evaluations": 0,
            "historical_phase42_solver_noise_evidence_unchanged": True,
        },
    )
    return {
        "points": point_payloads,
        "global_local": {
            "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE": global_source,
            "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES": global_fd,
            "PHASE43_LOCAL_ARBITRATION": arbitration,
            "INTEGRATED_TANGENT_EVOLUTION": "NOT_TESTED_LOCAL_ONLY",
            "ODE_SOLVER_NOISE_COMPONENT": "NOT_TESTED_LOCAL_ONLY",
        },
        "quantifiers": {
            "all_local_slots": 90,
            "disclosed_anomaly_slots": 33,
            "noncohort_slots_retained_but_excluded_from_FD_claim": 57,
        },
    }


def audit_local_only_source_scope() -> dict[str, Any]:
    tree = ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"))
    forbidden_call_names = {
        "solve_ivp",
        "root",
        "least_squares",
        "solve_signed_saddle_grids",
        "solve_main_saddle",
        "solve_primary_intersections",
        "integrate_chart",
        "residual_and_variational_jacobian",
    }
    observed: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name: str | None = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name in forbidden_call_names:
            observed.append(str(name))
    if observed:
        raise InvalidRun(f"forbidden local-scope calls in runner AST: {observed}")
    return {
        "forbidden_call_names": sorted(forbidden_call_names),
        "observed_forbidden_calls": observed,
        "time_column_evaluation_call_sites": 0,
        "integrated_tangent_evaluation_call_sites": 0,
    }


def math_protocol_runtime_controls(
    manifest: Mapping[str, Any], preenumeration: Mapping[str, Any]
) -> dict[str, Any]:
    process_source = inspect.getsource(process_base_slot)
    helper_sources = {
        "central_D2": inspect.getsource(central_D2),
        "restored_R4": inspect.getsource(restored_R4),
        "mp_number_string": inspect.getsource(mp_number_string),
        "binary64_payload": inspect.getsource(binary64_payload),
    }
    source_call_controls = {
        "process_calls_central_D2_twice": process_source.count("central_D2(") == 2,
        "process_calls_restored_R4_twice": process_source.count("restored_R4(")
        == 2,
        "central_D2_uses_declared_vector_difference": (
            "vector_difference(plus, minus)" in helper_sources["central_D2"]
            and "mp.mpf(2) * epsilon" in helper_sources["central_D2"]
        ),
        "restored_R4_uses_fixed_4_minus_1_over_3": all(
            token in helper_sources["restored_R4"]
            for token in (
                "mp.mpf(4)",
                "mp.mpf(-1)",
                "restoration_norm / mp.mpf(3)",
            )
        ),
    }
    with mp.workdps(120):
        exact_lift_controls: dict[str, bool] = {}
        for value in (
            0.1,
            -1.25,
            float.fromhex("0x0.0000000000001p-1022"),
            float.fromhex("0x1.fffffffffffffp+10"),
        ):
            numerator, denominator = value.as_integer_ratio()
            exact_lift_controls[value.hex()] = bool(
                mp_from_binary64(value) * mp.mpf(denominator)
                == mp.mpf(numerator)
            )
        signed_zero_payload = binary64_payload(
            np.asarray([-0.0, 0.0], dtype=np.float64)
        )
        signed_zero_control = bool(
            signed_zero_payload["components"][0]["signed_zero"] is True
            and signed_zero_payload["components"][1]["signed_zero"] is False
            and signed_zero_payload["components"][0]["ratio"] == [0, 1]
        )

        h = mp.mpf(2)
        restoration = mp.mpf(23)
        minus_h = [mp.mpf(11)]
        minus_half = [mp.mpf(13)]
        plus_half = [mp.mpf(17)]
        plus_h = [mp.mpf(19)]
        d2_h = central_D2(plus_h, minus_h, h)
        d2_half = central_D2(plus_half, minus_half, h / mp.mpf(2))
        prospective_observed = restored_R4(d2_half, d2_h, restoration)[0]
        prospective_expected = restoration * (
            minus_h[0]
            - mp.mpf(8) * minus_half[0]
            + mp.mpf(8) * plus_half[0]
            - plus_h[0]
        ) / (mp.mpf(6) * h)
        prospective_formula_control = prospective_observed == prospective_expected

        coarse = central_D2([mp.mpf(29)], [mp.mpf(5)], mp.mpf(2))
        fine = central_D2([mp.mpf(31)], [mp.mpf(7)], mp.mpf(1))
        same_observed = restored_R4(fine, coarse, restoration)[0]
        same_expected = restoration * (
            mp.mpf(4) * fine[0] - coarse[0]
        ) / mp.mpf(3)
        same_formula_control = same_observed == same_expected

        norm_floor_control = bool(
            mp_relative([mp.mpf("1e-120")], [mp.mpf(0)])
            == mp.mpf("1e-20")
            and mp_max_component_relative(
                [mp.mpf("1e-120")], [mp.mpf(0)]
            )
            == mp.mpf("1e-20")
        )
        threshold_controls = {
            key: bool(mp.isfinite(mp.mpf(text)) and mp.mpf(text) > 0)
            for key, text in manifest["acceptance_thresholds"].items()
            if isinstance(text, str) and key != "threshold_policy"
        }

    with mp.workdps(80):
        serialization_value = mp.mpf("1.25")
        serialization_text = mp_number_string(serialization_value, 80)
        serialization_roundtrip = bool(
            isinstance(serialization_text, str)
            and mp.mpf(serialization_text) == serialization_value
            and mp_number_string(mp.mpf(0), 80) == "0.0"
            and all(
                isinstance(component, str)
                for component in mp_complex_payload(mp.mpc(1, -2), 80)
            )
        )
        wrong_context_rejected = False
        try:
            mp_number_string(serialization_value, 120)
        except InvalidRun:
            wrong_context_rejected = True
        raw_mp_rejected = False
        try:
            json_ready(serialization_value)
        except InvalidRun:
            raw_mp_rejected = True

    key_hash_control = bool(
        preenumeration["total_declared"] == 13606
        and preenumeration["expected_key_set_sha256"]
        == preenumeration["observed_key_set_sha256"]
    )
    checks = {
        **source_call_controls,
        "all_binary64_ratio_lifts_exact": all(exact_lift_controls.values()),
        "binary64_signed_zero_retained": signed_zero_control,
        "same_step_R4_formula_control": bool(same_formula_control),
        "prospective_R4_formula_control": bool(prospective_formula_control),
        "metric_norm_floor_control": norm_floor_control,
        "all_decimal_thresholds_directly_parse_finite_positive": all(
            threshold_controls.values()
        )
        and len(threshold_controls) == 10,
        "mp_serialization_roundtrip": serialization_roundtrip,
        "wrong_mp_context_rejected": wrong_context_rejected,
        "raw_mp_object_rejected_before_JSON": raw_mp_rejected,
        "full_preenumerated_key_hash_matches": key_hash_control,
    }
    if not all(checks.values()):
        raise InvalidRun(f"mathematical protocol runtime control failed: {checks}")
    return {
        "checks": checks,
        "binary64_ratio_lift_controls": exact_lift_controls,
        "signed_zero_payload": signed_zero_payload,
        "threshold_parse_controls": threshold_controls,
        "helper_source_sha256": {
            name: sha256_bytes(source.encode("utf-8"))
            for name, source in helper_sources.items()
        },
        "process_base_slot_source_sha256": sha256_bytes(
            process_source.encode("utf-8")
        ),
    }


def classification_schema_validation(
    ledger: SlotLedger,
) -> dict[str, Any]:
    allowed_tri_state = {"SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
    classification_slots = [
        slot
        for slot in ledger.slots.values()
        if slot["metadata"]["slot_kind"] == "slot_classification"
    ]
    point_slots = [
        slot
        for slot in ledger.slots.values()
        if slot["metadata"]["slot_kind"] == "point_aggregate"
    ]
    global_slots = [
        slot
        for slot in ledger.slots.values()
        if slot["metadata"]["slot_kind"] == "global_aggregate"
    ]
    if len(classification_slots) != 270 or len(point_slots) != 9 or len(global_slots) != 5:
        raise InvalidRun("classification slot count drift")
    dependency_graph: dict[str, list[str]] = {}
    resolved_by_owner_kind: dict[str, int] = {}

    def same_base(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
        return all(
            left.get(name) == right.get(name)
            for name in ("point", "fraction", "direction")
        )

    def require_canonical_dependency(
        owner: Mapping[str, Any], dependency: Mapping[str, Any]
    ) -> None:
        owner_metadata = owner["metadata"]
        dependency_metadata = dependency["metadata"]
        owner_kind = owner_metadata["slot_kind"]
        dependency_kind = dependency_metadata["slot_kind"]
        if owner_kind == "slot_classification":
            if not same_base(owner_metadata, dependency_metadata):
                raise InvalidRun("classification dependency crosses a base slot")
            classification = owner_metadata["classification"]
            allowed = {
                "reference": {
                    "reference_analytic",
                    "same_step_R4",
                    "prospective_R4",
                },
                "source_RHS": {
                    "source_analytic",
                    "source_D2",
                    "source_R4",
                    "source_summary",
                    "reference_analytic",
                    "same_step_R4",
                    "prospective_R4",
                },
                "double_FD": {
                    "source_summary",
                    "source_R4",
                    "same_step_R4",
                    "slot_classification",
                },
            }[classification]
            if dependency_kind not in allowed:
                raise InvalidRun(
                    "classification cites a noncanonical dependency kind"
                )
            if classification == "double_FD":
                if dependency_kind == "same_step_R4" and not (
                    dependency_metadata.get("dps") == 120
                    and dependency_metadata.get("reference") == "fixed_1e-5"
                ):
                    raise InvalidRun("double-FD cites a nonfixed R4 dependency")
                if dependency_kind == "slot_classification" and (
                    dependency_metadata.get("classification")
                    not in {"reference", "source_RHS"}
                ):
                    raise InvalidRun("double-FD classification dependency drift")
            return
        if owner_kind == "point_aggregate":
            expected_classification = {
                "reference": "reference",
                "source_RHS": "source_RHS",
                "double_FD": "double_FD",
            }[owner_metadata["aggregate"]]
            if not (
                dependency_kind == "slot_classification"
                and dependency_metadata.get("point") == owner_metadata.get("point")
                and dependency_metadata.get("classification")
                == expected_classification
            ):
                raise InvalidRun("point aggregate dependency is noncanonical")
            return
        if owner_kind == "global_aggregate":
            aggregate = owner_metadata["aggregate"]
            if aggregate == "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE":
                valid = dependency_kind == "point_aggregate" and (
                    dependency_metadata.get("aggregate") == "source_RHS"
                )
            elif aggregate == (
                "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES"
            ):
                valid = dependency_kind == "point_aggregate" and (
                    dependency_metadata.get("aggregate") == "double_FD"
                )
            elif aggregate == "PHASE43_LOCAL_ARBITRATION":
                valid = dependency_kind == "global_aggregate" and (
                    dependency_metadata.get("aggregate")
                    in {
                        "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE",
                        "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES",
                    }
                )
            else:
                valid = False
            if not valid:
                raise InvalidRun("global-local aggregate dependency is noncanonical")
            return
        raise InvalidRun(f"undeclared dependency-owning slot kind: {owner_kind}")

    def resolve_paths(owner: Mapping[str, Any], paths: Any) -> None:
        if not isinstance(paths, list) or any(
            not isinstance(path, str) for path in paths
        ):
            raise InvalidRun("cited metric/dependency paths are not a string list")
        if len(paths) != len(set(paths)):
            raise InvalidRun("duplicate cited dependency path")
        owner_key = str(owner["key"])
        dependency_graph.setdefault(owner_key, [])
        for path in paths:
            if path == owner_key:
                raise InvalidRun("self-referential classification/aggregate path")
            dependency = ledger.slots.get(path)
            if dependency is None:
                raise InvalidRun(f"cited ledger path does not resolve: {path}")
            if dependency["terminal_status"] not in {
                "SUCCESS",
                "EVALUATION_FAILED",
                "NOT_RUN_UPSTREAM_INVALID",
            }:
                raise InvalidRun(f"cited ledger path is not terminal: {path}")
            require_canonical_dependency(owner, dependency)
            dependency_graph[owner_key].append(path)
            owner_kind = str(owner["metadata"]["slot_kind"])
            resolved_by_owner_kind[owner_kind] = (
                resolved_by_owner_kind.get(owner_kind, 0) + 1
            )

    for slot in classification_slots:
        if slot["terminal_status"] != "SUCCESS" or not isinstance(
            slot["payload"], dict
        ):
            raise InvalidRun("classification record is not terminal SUCCESS")
        payload = slot["payload"]
        if payload.get("completion") not in {"COMPLETE", "INCOMPLETE"}:
            raise InvalidRun("slot classification completion vocabulary drift")
        kind = slot["metadata"]["classification"]
        status = payload.get("evidence_status")
        if kind == "reference":
            if status not in {"CORROBORATED", "INCONCLUSIVE"}:
                raise InvalidRun("reference evidence vocabulary drift")
        elif status not in allowed_tri_state:
            raise InvalidRun("tri-state evidence vocabulary drift")
        resolve_paths(slot, payload.get("metric_paths"))
    for slot in point_slots + global_slots:
        if slot["terminal_status"] != "SUCCESS" or not isinstance(
            slot["payload"], dict
        ):
            raise InvalidRun("aggregate record is not terminal SUCCESS")
        payload = slot["payload"]
        if slot["metadata"]["slot_kind"] == "point_aggregate":
            resolve_paths(slot, payload.get("base_classification_paths"))
        else:
            aggregate = slot["metadata"]["aggregate"]
            if aggregate in {
                "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE",
                "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES",
            }:
                resolve_paths(slot, payload.get("point_aggregate_paths"))
            elif aggregate == "PHASE43_LOCAL_ARBITRATION":
                resolve_paths(
                    slot,
                    [payload.get("source_RHS_path"), payload.get("double_FD_path")],
                )
            else:
                dependency_graph.setdefault(str(slot["key"]), [])

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(key: str) -> None:
        if key in visiting:
            raise InvalidRun(f"cyclic cited ledger dependency at {key}")
        if key in visited:
            return
        visiting.add(key)
        for dependency in dependency_graph.get(key, []):
            if dependency in dependency_graph:
                visit(dependency)
        visiting.remove(key)
        visited.add(key)

    for key in dependency_graph:
        visit(key)
    if resolved_by_owner_kind != {
        "slot_classification": 5940,
        "point_aggregate": 213,
        "global_aggregate": 8,
    }:
        raise InvalidRun(
            f"resolved classification dependency count drift: {resolved_by_owner_kind}"
        )
    fixed = {
        slot["metadata"]["aggregate"]: slot["payload"]["evidence_status"]
        for slot in global_slots
    }
    if fixed.get("INTEGRATED_TANGENT_EVOLUTION") != "NOT_TESTED_LOCAL_ONLY":
        raise InvalidRun("integrated tangent boundary drift")
    if fixed.get("ODE_SOLVER_NOISE_COMPONENT") != "NOT_TESTED_LOCAL_ONLY":
        raise InvalidRun("ODE solver-noise boundary drift")
    return {
        "slot_classifications": len(classification_slots),
        "point_aggregates": len(point_slots),
        "global_local_aggregates": len(global_slots),
        "resolved_cited_dependency_paths": sum(
            resolved_by_owner_kind.values()
        ),
        "resolved_by_owner_kind": resolved_by_owner_kind,
        "dependency_graph_acyclic": True,
        "all_cited_paths_exist_and_are_terminal": True,
        "all_cited_paths_are_canonical_to_owner": True,
        "all_records_terminal_and_typed": True,
        "completion_is_separate_from_evidence": True,
    }


def record_exact_contracts(
    audit: Audit,
    manifest: Mapping[str, Any],
    manifest_validation: Mapping[str, Any],
    context: FrozenContext,
    boundary_audit: Mapping[str, Any],
    symbolic_payload: Mapping[str, Any],
    preenumeration: Mapping[str, Any],
    ledger: SlotLedger,
    provenance: Mapping[str, Any],
) -> None:
    exact_map, _numerical_map = manifest_contract_maps(manifest)
    audit.exact(
        EXACT_IDS[0],
        bool(
            all(provenance["comparisons"].values())
            and provenance["start"]["runner"]["git_tracked"] is True
            and provenance["start"]["runner"]["git_clean_for_path"] is True
            and provenance["start"]["runner"]
            ["latest_commit_blob_matches_current_bytes"]
            is True
        ),
        str(exact_map[EXACT_IDS[0]]["criterion"]),
        {"provenance": provenance},
    )
    audit.exact(
        EXACT_IDS[1],
        bool(
            context.validation["base_slot_count"] == 90
            and context.validation["q_duplicate_identities"] == 90
            and context.validation["perturbation_records"] == 540
            and context.validation["point_count"] == 3
            and context.validation[
                "checkpoint_explicit_array_records_independently_decoded"
            ]
            == 191
            and context.validation[
                "checkpoint_critical_arrays_independently_mapped"
            ]
            == 204
        ),
        str(exact_map[EXACT_IDS[1]]["criterion"]),
        {"input_validation": context.validation},
    )
    source_scope = audit_local_only_source_scope()
    audit.exact(
        EXACT_IDS[2],
        bool(
            not any(context.forbidden_call_counter.values())
            and context.validation["time_column_records_consumed"] == 0
            and context.validation["ODE_or_root_calls_declared"] == 0
            and not source_scope["observed_forbidden_calls"]
        ),
        str(exact_map[EXACT_IDS[2]]["criterion"]),
        {
            "forbidden_call_counter": context.forbidden_call_counter,
            "runner_AST_scope_audit": source_scope,
            "INTEGRATED_TANGENT_EVOLUTION": "NOT_TESTED_LOCAL_ONLY",
        },
    )
    all_symbolic_checks = all(
        all(record["exact_checks"].values())
        for record in symbolic_payload["by_point"].values()
    )
    audit.exact(
        EXACT_IDS[3],
        bool(all_symbolic_checks and boundary_audit),
        str(exact_map[EXACT_IDS[3]]["criterion"]),
        {
            "reference_boundary_audit": boundary_audit,
            "symbolic_fingerprints_and_checks": symbolic_payload,
        },
    )
    math_controls = math_protocol_runtime_controls(
        manifest, preenumeration
    )
    audit.exact(
        EXACT_IDS[4],
        bool(
            manifest_validation["precision_tiers"] == [80, 120]
            and manifest_validation["same_step_normalization_modes"]
            == list(NORMALIZATION_MODES)
            and preenumeration["all_slots_declared_before_scientific_evaluation"]
            is True
            and all(math_controls["checks"].values())
        ),
        str(exact_map[EXACT_IDS[4]]["criterion"]),
        {
            "manifest_validation": manifest_validation,
            "preenumeration": preenumeration,
            "prospective_offsets": list(PROSPECTIVE_OFFSETS),
            "metric_norm_floor": "1e-100",
            "mathematical_protocol_controls": math_controls,
        },
    )
    ledger.assert_complete()
    summary = ledger.summary()
    path_validation = classification_schema_validation(ledger)
    audit.exact(
        EXACT_IDS[5],
        bool(
            summary["declared_total"] == preenumeration["total_declared"]
            and summary["by_terminal_status"].get("None", 0) == 0
        ),
        str(exact_map[EXACT_IDS[5]]["criterion"]),
        {
            "slot_schema_summary": summary,
            "preenumeration": preenumeration,
            "classification_path_validation": path_validation,
        },
    )
    audit.exact(
        EXACT_IDS[6],
        bool(
            manifest["desired_outputs"] == expected_desired_outputs()
            and manifest["required_fail_closed_outputs"]
            == expected_fail_closed_outputs()
            and manifest["historical_statuses_must_remain"]["global_promotion"]
            == "PROHIBITED"
        ),
        str(exact_map[EXACT_IDS[6]]["criterion"]),
        {
            "desired_outputs": expected_desired_outputs(),
            "required_fail_closed_outputs": expected_fail_closed_outputs(),
            "historical_statuses": manifest["historical_statuses_must_remain"],
        },
    )


def record_numerical_contracts(
    audit: Audit,
    manifest: Mapping[str, Any],
    outcomes: Sequence[BaseOutcome],
    aggregation: Mapping[str, Any],
    ledger: SlotLedger,
) -> None:
    _exact_map, numerical_map = manifest_contract_maps(manifest)
    reproduction_pass = all(
        item.source_reproduction_passed for item in outcomes
    )
    independent_pass = all(
        item.independent_reference_passed
        for item in outcomes
    )
    r4_pass = all(
        item.r4_reference_passed
        for item in outcomes
    )
    rhs_pass = all(
        item.source_rhs_completion == "COMPLETE"
        and item.source_rhs_evidence == "NOT_SUPPORTED"
        for item in outcomes
    )
    anomalies = [item for item in outcomes if item.disclosed_anomaly]
    fd_pass = bool(
        len(anomalies) == 33
        and all(
            item.double_fd_completion == "COMPLETE"
            and item.double_fd_evidence == "SUPPORTED"
            for item in anomalies
        )
    )
    classification_validation = classification_schema_validation(ledger)
    values: tuple[tuple[str, bool, Mapping[str, Any]], ...] = (
        (
            NUMERICAL_IDS[0],
            reproduction_pass,
            {
                "all_90_source_reproductions_passed": reproduction_pass,
                "maximum_reproduction_absolute": max(
                    item.source_reproduction_max_abs or 0.0 for item in outcomes
                ),
                "disclosed_anomaly_count_reproduced": len(anomalies),
            },
        ),
        (
            NUMERICAL_IDS[1],
            independent_pass,
            {
                "all_90_independent_reference_paths_passed": independent_pass,
                "independent_analytic_path_pass_count": sum(
                    item.independent_reference_passed for item in outcomes
                ),
            },
        ),
        (
            NUMERICAL_IDS[2],
            r4_pass,
            {
                "all_90_same_and_small_step_R4_controls_passed": r4_pass,
                "all_declared_steps_retained": True,
            },
        ),
        (
            NUMERICAL_IDS[3],
            rhs_pass,
            {
                "all_90_source_RHS_actions_within_threshold": rhs_pass,
                "global_local_evidence": aggregation["global_local"][
                    "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE"
                ],
            },
        ),
        (
            NUMERICAL_IDS[4],
            fd_pass,
            {
                "disclosed_slot_count": len(anomalies),
                "all_33_support_fixed_FD_rule": fd_pass,
                "global_local_evidence": aggregation["global_local"][
                    "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES"
                ],
            },
        ),
        (
            NUMERICAL_IDS[5],
            True,
            classification_validation,
        ),
    )
    for check_id, passed, details in values:
        declared = numerical_map[check_id]
        audit.numerical(
            check_id,
            bool(passed),
            str(declared["criterion"]),
            failure_status=str(declared["failure_status"]),
            failure_invalidates_run=bool(
                declared.get("failure_invalidates_run", False)
            ),
            details=details,
        )


def enforce_audit_cardinality_and_invalidating_failures(audit: Audit) -> None:
    if tuple(record["id"] for record in audit.exact_records) != EXACT_IDS:
        raise InvalidRun("exact audit cardinality/order drift")
    if tuple(record["id"] for record in audit.numerical_records) != NUMERICAL_IDS:
        raise InvalidRun("numerical audit cardinality/order drift")
    invalidating = [
        record["id"]
        for record in audit.numerical_records
        if record["failure_invalidates_run"] is True
        and record["passed"] is not True
    ]
    if invalidating:
        raise InvalidRun(
            "invalidating numerical contracts failed: " + ",".join(invalidating)
        )


def result_with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    ready = json_ready(dict(payload))
    if not isinstance(ready, dict):
        raise InvalidRun("result payload did not serialize as an object")
    ready.pop("result_payload_sha256_without_self", None)
    ready["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_json_bytes(ready)
    )
    canonical_json_bytes(ready)
    return ready


def claim_status_from_aggregation(
    aggregation: Mapping[str, Any], outcomes: Sequence[BaseOutcome]
) -> dict[str, Any]:
    reference = (
        "CORROBORATED"
        if all(item.reference_status == "CORROBORATED" for item in outcomes)
        else "INCONCLUSIVE"
    )
    global_local = aggregation["global_local"]
    return {
        "phase43_local_arbitration": global_local["PHASE43_LOCAL_ARBITRATION"],
        "local_RHS_implementation_mismatch_evidence": global_local[
            "LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE"
        ],
        "double_precision_local_FD_artifact_for_phase42_anomalies": global_local[
            "DOUBLE_PRECISION_LOCAL_FD_ARTIFACT_FOR_PHASE42_ANOMALIES"
        ],
        "independent_high_precision_reference": reference,
        "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
        "ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
        "time_column_as_independent_bug_evidence": "EXCLUDED",
        "phase41_numerical_contracts": "8/9",
        "phase41_tangent_status": "TANGENT_CONTROL_FAILED",
        "phase42_reference_tangent": "REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE",
        "phase42_protocol_local_anomaly_label": "VARIATIONAL_RHS_BUG_EVIDENCE",
        "global_promotion": "PROHIBITED",
        "no_forced_unique_cause": True,
    }


def production_result_payload(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    *,
    preenumeration: Mapping[str, Any],
    manifest_validation: Mapping[str, Any],
    context: FrozenContext,
    symbolic_payload: Mapping[str, Any],
    boundary_audit: Mapping[str, Any],
    outcomes: Sequence[BaseOutcome],
    aggregation: Mapping[str, Any],
    provenance: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "phase": 43,
        "run_status": "VALID_TYPED_RUN",
        "exit_code": 0,
        "counts": {
            "exact_passed": sum(record["passed"] for record in audit.exact_records),
            "exact_total": len(EXACT_IDS),
            "numerical_passed": sum(
                record["passed"] for record in audit.numerical_records
            ),
            "numerical_total": len(NUMERICAL_IDS),
            "base_slots": len(outcomes),
            "disclosed_phase42_anomalies": sum(
                item.disclosed_anomaly for item in outcomes
            ),
        },
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "manifest_validation": manifest_validation,
        "input_validation": context.validation,
        "symbolic_reference": symbolic_payload,
        "reference_boundary_audit": boundary_audit,
        "slot_preenumeration": preenumeration,
        "slot_schema_summary": ledger.summary(),
        "base_outcomes": list(outcomes),
        "local_aggregation": aggregation,
        "claim_status": claim_status_from_aggregation(aggregation, outcomes),
        "slot_ledger": ledger.slots,
        "desired_outputs": expected_desired_outputs(),
        "required_fail_closed_outputs": expected_fail_closed_outputs(),
        "result_artifact_contract": dict(
            manifest["declared_output_retention"]["result_artifact"]
        ),
        "scientific_scope": {
            "frozen_local_xi_q_only": True,
            "time_column_excluded_as_independent_bug_evidence": True,
            "root_solver_evaluations": 0,
            "ODE_solver_evaluations": 0,
            "integrated_tangent_evaluations": 0,
            "new_reference_tangent_or_orientation_calculation": False,
            "determinant_line_or_global_cycle_claim": False,
            "quantum_gravity_claim": False,
            "global_promotion": "PROHIBITED",
        },
        "known_precommit_design_audit": dict(
            manifest["known_precommit_design_audit"]
        ),
        "provenance": provenance,
    }


def emit_result(
    payload: Mapping[str, Any],
    *,
    final_guard: Callable[[], Any] | None = None,
) -> None:
    ready = result_with_self_digest(payload)
    encoded = canonical_json_bytes(ready).decode("utf-8")
    if final_guard is not None:
        final_guard()
    print(f"{RESULT_PREFIX}{encoded}", flush=True)


def invalid_result_skeleton(
    manifest: Mapping[str, Any] | None,
    reason: str,
    *,
    audit: Audit,
    ledger: SlotLedger,
    failure_provenance: Mapping[str, Any],
    force_freeze_contract_invalid: bool,
) -> dict[str, Any]:
    try:
        exact_map, numerical_map = (
            manifest_contract_maps(manifest)
            if manifest is not None
            else ({}, {})
        )
    except Exception:
        exact_map, numerical_map = {}, {}
    existing_exact = {record["id"]: record for record in audit.exact_records}
    existing_numerical = {
        record["id"]: record for record in audit.numerical_records
    }
    exact_records = [
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
        for check_id in EXACT_IDS
    ]
    if force_freeze_contract_invalid:
        exact_records[0] = {
            "id": EXACT_IDS[0],
            "kind": "exact",
            "status": "INVALID_RUN",
            "passed": False,
            "failure_status": "INVALID_RUN",
            "statement": str(
                exact_map.get(EXACT_IDS[0], {}).get("criterion", reason)
            ),
            "details": {
                "late_provenance_or_final_guard_failure": True,
                "invalid_reason": reason,
            },
        }
    numerical_records = []
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
                    "statement": str(
                        declared.get("criterion", reason)
                    ),
                    "details": {"not_completed_reason": reason},
                },
            )
        )
    ledger.fail_unfinished(reason)
    return result_with_self_digest(
        {
            "schema": RESULT_SCHEMA,
            "phase": 43,
            "run_status": "INVALID_RUN",
            "exit_code": 2,
            "invalid_reason": reason,
            "counts": {
                "exact_passed": sum(record["passed"] for record in exact_records),
                "exact_total": len(EXACT_IDS),
                "numerical_passed": sum(
                    record["passed"] for record in numerical_records
                ),
                "numerical_total": len(NUMERICAL_IDS),
            },
            "exact_records": exact_records,
            "numerical_records": numerical_records,
            "slot_schema_summary": ledger.summary() if ledger.slots else None,
            "slot_ledger": ledger.slots,
            "symbolic_reference": None,
            "reference_boundary_audit": None,
            "base_outcomes": None,
            "local_aggregation": None,
            "claim_status": {
                "phase43_local_arbitration": None,
                "local_RHS_implementation_mismatch_evidence": None,
                "double_precision_local_FD_artifact_for_phase42_anomalies": None,
                "independent_high_precision_reference": None,
                "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
                "ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
                "time_column_as_independent_bug_evidence": "EXCLUDED",
                "global_promotion": "PROHIBITED",
            },
            "desired_outputs": expected_desired_outputs(),
            "required_fail_closed_outputs": expected_fail_closed_outputs(),
            "scientific_scope": {
                "local_only": True,
                "production_claim_valid": False,
                "global_promotion": "PROHIBITED",
                "quantum_gravity_claim": False,
            },
            "provenance": {
                "manifest_commit": MANIFEST_COMMIT,
                "manifest_sha256": MANIFEST_SHA256,
                "runner_observed_sha256": (
                    sha256_bytes(SCRIPT_PATH.read_bytes())
                    if SCRIPT_PATH.is_file()
                    else None
                ),
                "failure_observations": failure_provenance,
            },
        }
    )


def capture_failure_provenance(
    manifest: Mapping[str, Any] | None, run_state: Mapping[str, Any]
) -> dict[str, Any]:
    observations: dict[str, Any] = {
        "retained_provenance_start": run_state.get("provenance_start"),
        "retained_provenance_pre_audit": run_state.get(
            "provenance_pre_audit"
        ),
        "retained_provenance_pre_emit": run_state.get("provenance_pre_emit"),
        "raw_start": run_state.get("raw_start"),
    }

    def capture(name: str, operation: Callable[[], Any]) -> None:
        try:
            observations[name] = {"status": "OBSERVED", "value": operation()}
        except Exception as exc:
            observations[name] = {
                "status": "OBSERVATION_FAILED",
                "error": f"{type(exc).__name__}: {exc}"[:4096],
            }

    observations["HEAD_at_failure"] = raw_git_observation("rev-parse", "HEAD")
    observations["runner_at_failure"] = observe_runner_provenance_raw()
    observations["source_at_failure"] = observe_source_closure_raw(manifest)
    capture("pycache_at_failure", repository_pycache_snapshot)
    capture("worktree_at_failure", repository_worktree_snapshot)
    if manifest is not None:
        capture(
            "runtime_at_failure",
            lambda: observed_runtime_fingerprint(manifest),
        )
    return observations


def run_production(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    run_state: dict[str, Any],
) -> int:
    def guarded_finish(stage: str, start: Mapping[str, Any]) -> dict[str, Any]:
        try:
            return finish_provenance_guard(manifest, start)
        except Exception as exc:
            run_state["late_provenance_failure"] = {
                "stage": stage,
                "error": f"{type(exc).__name__}: {exc}"[:4096],
            }
            raise

    manifest_validation = validate_manifest(manifest)
    preenumeration = preenumerate_slots(manifest, ledger)
    run_state["raw_start"] = {
        "runner": observe_runner_provenance_raw(),
        "source": observe_source_closure_raw(manifest),
        "HEAD": raw_git_observation("rev-parse", "HEAD"),
    }
    progress("provenance/start")
    provenance_start = start_provenance_guard(manifest)
    run_state["provenance_start"] = provenance_start

    progress("immutable Phase42 input rehydration")
    context = validate_and_rehydrate_inputs(manifest)
    boundary_audit = audit_reference_source_boundary()
    ledger.finish(
        "symbolic|reference_boundary",
        "SUCCESS",
        payload=boundary_audit,
    )
    progress("independent exact symbolic families")
    evaluators: dict[str, ReferenceEvaluators] = {}
    fingerprints: dict[str, Any] = {}
    for point in TARGETS:
        frozen_point = context.points[point]
        evaluator = make_reference_evaluators(
            frozen_point.delta_a, frozen_point.delta_phi
        )
        evaluators[point] = evaluator
        fingerprints[point] = dict(evaluator.fingerprints)
    symbolic_payload = {
        "by_point": fingerprints,
        "exact_action_rebuilt_without_phase41_import": True,
        "reference_backend": "SymPy lambdify modules='mpmath'",
        "source_rounding_control_digits": 50,
    }
    ledger.finish(
        "symbolic|independent_model", "SUCCESS", payload=symbolic_payload
    )

    progress("ninety frozen local arbitration slots")
    outcomes: list[BaseOutcome] = []
    for point in TARGETS:
        frozen_point = context.points[point]
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                outcomes.append(
                    process_base_slot(
                        manifest,
                        context,
                        evaluators[point],
                        frozen_point,
                        fraction,
                        direction,
                        ledger,
                    )
                )
    aggregation = aggregate_local_outcomes(manifest, outcomes, ledger)
    ledger.assert_complete()

    progress("provenance/pre-audit")
    provenance = guarded_finish("pre_audit", provenance_start)
    run_state["provenance_pre_audit"] = provenance
    record_exact_contracts(
        audit,
        manifest,
        manifest_validation,
        context,
        boundary_audit,
        symbolic_payload,
        preenumeration,
        ledger,
        provenance,
    )
    record_numerical_contracts(
        audit, manifest, outcomes, aggregation, ledger
    )
    enforce_audit_cardinality_and_invalidating_failures(audit)

    payload = production_result_payload(
        manifest,
        audit,
        ledger,
        preenumeration=preenumeration,
        manifest_validation=manifest_validation,
        context=context,
        symbolic_payload=symbolic_payload,
        boundary_audit=boundary_audit,
        outcomes=outcomes,
        aggregation=aggregation,
        provenance=provenance,
    )
    payload["provenance"] = guarded_finish("pre_emit", provenance_start)
    run_state["provenance_pre_emit"] = payload["provenance"]
    emit_result(
        payload,
        final_guard=lambda: guarded_finish("final_stdout_guard", provenance_start),
    )
    return 0


def emergency_finite_invalid_result(reason: str) -> dict[str, Any]:
    clean_reason = str(reason).replace("\x00", "?")[:4096]
    numerical_contracts = (
        ("PHASE42_LOCAL_SOURCE_OR_PLATFORM_DRIFT", True),
        ("HIGH_PRECISION_REFERENCE_INCONCLUSIVE", False),
        ("HIGH_PRECISION_REFERENCE_INCONCLUSIVE", False),
        ("LOCAL_RHS_IMPLEMENTATION_MISMATCH_OR_INCONCLUSIVE", False),
        ("PHASE42_LOCAL_ANOMALY_MIXED_OR_INCONCLUSIVE", False),
        ("LOCAL_ARBITRATION_LEDGER_INCOMPLETE", True),
    )
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
    numerical_records = [
        {
            "id": check_id,
            "kind": "numerical",
            "status": "NOT_RUN_UPSTREAM_INVALID",
            "passed": False,
            "failure_status": numerical_contracts[index][0],
            "failure_invalidates_run": numerical_contracts[index][1],
            "statement": clean_reason,
            "details": {"emergency_fallback": True},
        }
        for index, check_id in enumerate(NUMERICAL_IDS)
    ]
    try:
        runner_sha: str | None = sha256_bytes(SCRIPT_PATH.read_bytes())
        runner_error: str | None = None
    except Exception as exc:
        runner_sha = None
        runner_error = f"{type(exc).__name__}: {exc}"[:1024]
    return result_with_self_digest(
        {
            "schema": RESULT_SCHEMA,
            "phase": 43,
            "run_status": "INVALID_RUN",
            "exit_code": 2,
            "invalid_reason": clean_reason,
            "counts": {
                "exact_passed": 0,
                "exact_total": len(EXACT_IDS),
                "numerical_passed": 0,
                "numerical_total": len(NUMERICAL_IDS),
            },
            "exact_records": exact_records,
            "numerical_records": numerical_records,
            "slot_ledger": {},
            "base_outcomes": None,
            "local_aggregation": None,
            "claim_status": {
                "phase43_local_arbitration": None,
                "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
                "ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
                "global_promotion": "PROHIBITED",
            },
            "desired_outputs": expected_desired_outputs(),
            "required_fail_closed_outputs": expected_fail_closed_outputs(),
            "provenance": {
                "manifest_commit": MANIFEST_COMMIT,
                "manifest_sha256": MANIFEST_SHA256,
                "runner_observed_sha256": runner_sha,
                "runner_observation_error": runner_error,
                "emergency_minimal_provenance": True,
            },
            "emergency_fallback": True,
        }
    )


def main() -> int:
    manifest: dict[str, Any] | None = None
    audit = Audit()
    ledger = SlotLedger()
    run_state: dict[str, Any] = {}
    try:
        raw = MANIFEST_PATH.read_bytes()
        manifest = strict_json_bytes(raw, label="Phase43 manifest")
        observed_sha = sha256_bytes(raw)
        if observed_sha != MANIFEST_SHA256:
            raise InvalidRun(
                f"Phase43 manifest SHA drift: {observed_sha} != {MANIFEST_SHA256}"
            )
        if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            raise InvalidRun("Phase43 manifest must end in exactly one LF")
        run_state["manifest_sha_verified"] = True
        return run_production(manifest, audit, ledger, run_state)
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"[:8192]
        progress(reason)
        try:
            trusted_manifest = (
                manifest
                if run_state.get("manifest_sha_verified") is True
                else None
            )
            failure_provenance = capture_failure_provenance(
                trusted_manifest, run_state
            )
            emit_result(
                invalid_result_skeleton(
                    trusted_manifest,
                    reason,
                    audit=audit,
                    ledger=ledger,
                    failure_provenance=failure_provenance,
                    force_freeze_contract_invalid=(
                        run_state.get("late_provenance_failure") is not None
                    ),
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
