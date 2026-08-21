#!/usr/bin/env python3
"""Phase 44 -- all-slot NumPy64 local-RHS error decomposition.

The separately committed Phase-44 manifest freezes a local arithmetic audit
of all ninety Phase-43 ``(xi, q)`` slots.  This runner reconstructs the exact
symbolic formula, traces the byte-pinned NumPy64 Hessian callable, forms the
fixed S0--S7 hybrid telescope, evaluates every declared contraction order,
and propagates the preregistered forward-error disks.  It never solves a root,
integrates an ODE, evaluates the excluded time column, or promotes a local
result to an integrated/global claim.

The program writes no files.  Progress goes to stderr and exactly one finite
``RESULT_JSON=`` record goes to stdout, including on ``INVALID_RUN``.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import ast
import copy
import dataclasses
import hashlib
import importlib.util
import inspect
import json
import math
import operator
import os
import platform
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Mapping, NoReturn, Sequence

import mpmath
import numpy as np
import scipy
import sympy as sp
from mpmath import mp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.resolve()
MANIFEST_PATH = SCRIPT_PATH.with_name(
    "PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_INPUTS.json"
)
PHASE43_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_RESULT.json"
)
CHECKPOINT_PATH = SCRIPT_PATH.with_name("PHASE42_M4_FIXED_ROOT_CHECKPOINT.json")
PHASE41_PATH = SCRIPT_PATH.with_name("phase41_m4_two_source_intersection.py")

MANIFEST_COMMIT = "03943e8b2b140a5f1b8724d1e2d4439d14964552"
MANIFEST_SHA256 = (
    "4680381aae27ff2faec75960c9bc382336efec2b518098c90a257f542eda9044"
)
RESULT_SCHEMA = "ice-phase44-numpy64-local-rhs-error-decomposition/v1"
PHASE43_RESULT_SCHEMA = "ice-phase43-high-precision-local-rhs-arbitration/v1"
CHECKPOINT_SCHEMA = "ice-phase42-fixed-root-checkpoint/v1"
RESULT_PREFIX = "RESULT_JSON="

TARGETS = ("shared_zero", "phi_plus", "a_plus")
FRACTION_STRINGS = ("0", "0.25", "0.5", "0.75", "1")
DIRECTIONS = tuple(range(6))
AUTHORITATIVE_DPS = 120
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
    "P44.freeze.committed_artifacts_runner_runtime_and_TOCTOU",
    "P44.input.all_90_phase43_slots_and_13_disclosure_identity",
    "P44.scope.local_arithmetic_only",
    "P44.symbolic.independent_componentwise_canonicalization",
    "P44.trace.byte_faithful_numpy64_boundaries_and_AST",
    "P44.math.fixed_hybrid_contractions_conditioning_and_envelopes",
    "P44.retention.complete_nonexclusive_tri_state_ledger",
    "P44.guard.fail_closed_gate1_and_null_outputs",
)
NUMERICAL_IDS = (
    "P44.reproduction.phase43_source_and_reference_vectors",
    "P44.formula.exact_componentwise_identity",
    "P44.decomposition.hybrid_telescoping_closure",
    "P44.forward_error.all_90_declared_model_coverage",
    "P44.forward_error.all_13_phase43_mismatches_covered",
    "P44.contractions.complete_six_way_all_slot_comparison",
    "P44.classification.complete_nonexclusive_causal_ledger",
)

EVIDENCE_KINDS = (
    "formula_mismatch",
    "coefficient_rounding",
    "state_rounding",
    "hessian_rounding",
    "contraction_rounding",
    "cancellation_scale",
    "forward_error_coverage",
    "unresolved_beyond_model",
)
ASSOCIATIONS = ("left_matrix_chain", "vector_first_chain")
SUMMATIONS = ("explicit_naive", "fixed_pairwise", "componentwise_kahan")
SOURCE_BOUNDARY_OPERATIONS = (
    "u64=linear_map@xi",
    "w64=saddle_w+u64",
    "H64=hessian_at(model,w64)",
    "B1_64=linear_map.T@H64",
    "B2_64=B1_64@linear_map",
    "y64=B2_64@q",
    "A64=-numpy.conjugate(y64)",
)
STAGE_IDS = (
    "S0_exact_decimal_reference_exact_w",
    "S1_source_coefficients_exact_w",
    "S2_source_coefficients_lifted_w64",
    "S3_lifted_H64_exact_contractions",
    "S4_lifted_B1_64_exact_tail",
    "S5_lifted_B2_64_exact_q",
    "S6_lifted_y64_exact_outer",
    "S7_lifted_A64",
)
DELTA_IDS = (
    "D_coeff",
    "D_state",
    "D_hessian",
    "D_matmul_1",
    "D_matmul_2",
    "D_matvec",
    "D_outer",
)


class InvalidRun(RuntimeError):
    """Infrastructure, provenance, exact, or retention contract failure."""


class SlotEvaluationError(RuntimeError):
    """Carries the smallest predeclared scientific/trace failure payload."""

    def __init__(self, message: str, *, payload: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.payload = dict(payload or {})


class DuplicateJSONKey(InvalidRun):
    """A strict JSON object repeated a key."""


def progress(message: str) -> None:
    try:
        print(f"[Phase44] {message}", file=sys.stderr, flush=True)
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
        "phase43_manifest": artifacts["phase43_input_manifest"],
        "phase43_runner": artifacts["phase43_runner"],
        "phase43_result": artifacts["phase43_raw_result"],
        "phase42_checkpoint": artifacts["phase42_checkpoint"],
        "phase41_script": artifacts["phase41_target_implementation"],
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
        raise InvalidRun("Phase44 runner must be committed before production")
    if git_output("status", "--porcelain=v1", "--", rel):
        raise InvalidRun("Phase44 runner path is dirty")
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


def p44_gamma_exact(operation_budget: int) -> tuple[mp.mpf, list[int]]:
    if operation_budget < 0 or operation_budget >= 2**53:
        raise InvalidRun(f"invalid gamma operation budget: {operation_budget}")
    numerator = int(operation_budget)
    denominator = 2**53 - numerator
    return mp.mpf(numerator) / mp.mpf(denominator), [numerator, denominator]


def p44_unit_roundoff_exact() -> tuple[mp.mpf, list[int]]:
    denominator = 2**53
    return mp.mpf(1) / mp.mpf(denominator), [1, denominator]


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
                    "real_subnormal": bool(
                        number.real != 0.0
                        and abs(number.real) < sys.float_info.min
                    ),
                    "imag_signed_zero": bool(
                        number.imag == 0.0 and math.copysign(1.0, number.imag) < 0
                    ),
                    "imag_subnormal": bool(
                        number.imag != 0.0
                        and abs(number.imag) < sys.float_info.min
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
                    "subnormal": bool(
                        number != 0.0 and abs(number) < sys.float_info.min
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
        "desired_phase44_overall_diagnosis": None,
        "desired_formula_identity_verdict": None,
        "desired_dominant_rounding_stage": None,
        "desired_all_13_forward_error_coverage": None,
        "desired_integrated_tangent_verdict": None,
        "desired_local_orientation_sign": None,
        "desired_global_intersection_coefficient": None,
    }


def expected_historical_statuses() -> dict[str, str]:
    return {
        "phase41_numerical_contracts": "8/9",
        "phase41_tangent_status": "TANGENT_CONTROL_FAILED",
        "phase42_reference_tangent": (
            "REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE"
        ),
        "phase42_protocol_local_anomaly_label": "VARIATIONAL_RHS_BUG_EVIDENCE",
        "phase43_exact_and_numerical_contracts": "7/7 exact; 4/6 numerical",
        "phase43_independent_reference": "CORROBORATED",
        "phase43_local_RHS_implementation_mismatch_evidence": "SUPPORTED",
        "phase43_double_precision_local_FD_artifact_for_phase42_anomalies": (
            "NOT_SUPPORTED"
        ),
        "phase43_local_arbitration": (
            "LOCAL_RHS_IMPLEMENTATION_MISMATCH_SUPPORTED"
        ),
        "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
        "phase43_ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
        "time_column_as_independent_bug_evidence": "EXCLUDED",
        "global_promotion": "PROHIBITED",
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


@dataclass(frozen=True)
class P44SlotInput:
    point: str
    fraction: str
    direction: int
    disclosed_mismatch: bool | None
    disclosed_phase42_anomaly: bool | None
    xi: np.ndarray
    q: np.ndarray
    source: np.ndarray
    source_binary64_identity: Mapping[str, Any]
    reference: tuple[mp.mpc, ...]
    rounding50_reference: tuple[mp.mpc, ...]
    p43_base_outcome_index: int
    p43_relative_text: str
    p43_source_rhs_evidence: str
    p43_disclosed_anomaly: bool
    stored_fixed_to_analytic_symmetric_relative: float
    stored_neighbor_symmetric_relative: float
    stored_stable_violation: bool


@dataclass(frozen=True)
class P44PointInput:
    label: str
    delta_a: str
    delta_phi: str
    saddle_w: np.ndarray
    model: Any


@dataclass(frozen=True)
class P44Context:
    phase43_result: Mapping[str, Any]
    checkpoint: Mapping[str, Any]
    phase41: ModuleType
    linear_map: np.ndarray
    points: Mapping[str, P44PointInput]
    slots: Mapping[tuple[str, str, int], P44SlotInput]
    forbidden_call_counter: Mapping[str, int]
    validation: Mapping[str, Any]


@dataclass(frozen=True)
class P44NumericSymbolic:
    w: tuple[sp.Symbol, ...]
    exact_action: sp.Expr
    exact_gradient: sp.Matrix
    exact_hessian: sp.Matrix
    rounding50_hessian: sp.Matrix
    exact_hessian_function: Callable[..., Any]
    rounding50_hessian_function: Callable[..., Any]
    fingerprints: Mapping[str, Any]


def p44_validate_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    manifest_contract_maps(manifest)
    if manifest.get("phase") != 44:
        raise InvalidRun("Phase44 manifest phase drift")
    if manifest.get("status") != "PREREGISTERED_POST_PHASE43_DIAGNOSTIC_INPUT_FREEZE":
        raise InvalidRun("Phase44 manifest status drift")
    if manifest.get("is_preregistration") is not True:
        raise InvalidRun("Phase44 manifest preregistration drift")
    if manifest.get("is_scientific_evidence") is not False:
        raise InvalidRun("Phase44 manifest evidence status drift")
    frozen = manifest["frozen_slot_universe"]
    if tuple(frozen["points_in_fixed_order"]) != TARGETS:
        raise InvalidRun("Phase44 point order drift")
    if tuple(frozen["flow_fractions_in_fixed_order"]) != FRACTION_STRINGS:
        raise InvalidRun("Phase44 fraction order drift")
    if tuple(frozen["transported_direction_indices_in_fixed_order"]) != DIRECTIONS:
        raise InvalidRun("Phase44 direction order drift")
    if int(frozen["slot_count"]) != 90:
        raise InvalidRun("Phase44 slot count drift")
    runtime = manifest["strict_runtime_environment"]
    if not (
        runtime["sys_dont_write_bytecode_required"] is True
        and runtime["repository_file_writes_allowed"] is False
        and runtime["source_and_environment_TOCTOU_recheck_before_RESULT_JSON"]
        is True
    ):
        raise InvalidRun("Phase44 runtime/write/TOCTOU declaration drift")
    if manifest["required_fail_closed_outputs"] != expected_fail_closed_outputs():
        raise InvalidRun("Phase44 fail-closed ledger drift")
    if manifest["desired_outputs"] != expected_desired_outputs():
        raise InvalidRun("Phase44 desired-output ledger drift")
    if manifest["historical_statuses_must_remain"] != expected_historical_statuses():
        raise InvalidRun("Phase44 historical-status ledger drift")
    fail_closed = manifest["required_fail_closed_outputs"]
    if sum(value is False for value in fail_closed.values()) != 16:
        raise InvalidRun("Phase44 false fail-closed cardinality drift")
    if sum(value is None for value in fail_closed.values()) != 6:
        raise InvalidRun("Phase44 null fail-closed cardinality drift")
    if fail_closed["gate1_status"] != "OPEN_PARTIAL_PROGRESS":
        raise InvalidRun("Phase44 Gate-1 boundary drift")
    if len(manifest["desired_outputs"]) != 7 or not all(
        value is None for value in manifest["desired_outputs"].values()
    ):
        raise InvalidRun("Phase44 desired-null cardinality drift")
    stages = tuple(
        record["id"] for record in manifest["hybrid_telescoping_protocol"]["stages_in_fixed_order"]
    )
    if stages != STAGE_IDS:
        raise InvalidRun("Phase44 S0-S7 order drift")
    if tuple(
        record["id"]
        for record in manifest["alternative_contraction_protocol"]["associations_in_fixed_order"]
    ) != ASSOCIATIONS:
        raise InvalidRun("Phase44 association order drift")
    if tuple(
        record["id"]
        for record in manifest["alternative_contraction_protocol"]["summation_algorithms_in_fixed_order"]
    ) != SUMMATIONS:
        raise InvalidRun("Phase44 summation order drift")
    thresholds = manifest["acceptance_thresholds"]
    expected_thresholds = {
        "phase43_source_mismatch_relative_reproduction": "5e-13",
        "phase43_reference_reproduction_relative_max": "1e-100",
        "hybrid_telescoping_closure_relative_max": "1e-100",
        "hybrid_telescoping_closure_absolute_max": "1e-100",
        "resolved_stage_delta_relative_floor": "1e-90",
        "source_50_decimal_rounding_control_relative_max": "1e-40",
        "python_literal_and_numpy_pi_component_ulp_model_max": "1",
        "numpy_sqrt_component_ulp_model_max": "8",
        "numpy_exp_component_ulp_model_max": "8",
        "numpy_complex_division_and_integer_power_component_ulp_model_max": "8",
        "forward_envelope_component_utilization_max": "1",
        "forward_envelope_norm_utilization_max": "1",
        "cancellation_capable_risk_scale": "5e-13",
        "source_raw_reproduction_max_abs": "0",
    }
    for key, expected in expected_thresholds.items():
        if thresholds.get(key) != expected:
            raise InvalidRun(f"Phase44 threshold drift: {key}")
    result = manifest["declared_output_retention"]["result_artifact"]
    if result["schema"] != RESULT_SCHEMA or result["stdout_prefix"] != RESULT_PREFIX:
        raise InvalidRun("Phase44 result transport schema drift")
    if result["outer_file_sha256"] is not None or result["payload_sha256_without_self"] is not None:
        raise InvalidRun("Phase44 result digest was prefilled")
    if manifest["declared_output_retention"]["future_runner_path"] != relative_repo_path(SCRIPT_PATH):
        raise InvalidRun("Phase44 future runner path drift")
    if manifest["known_prior_results_and_audit_disclosure"]["phase44_precommit_numerical_pilot_performed"] is not False:
        raise InvalidRun("Phase44 precommit pilot disclosure drift")
    return {
        "phase": 44,
        "status": manifest["status"],
        "slot_count": 90,
        "authoritative_dps": AUTHORITATIVE_DPS,
        "stage_ids": list(STAGE_IDS),
        "alternative_paths": [
            f"{association}|{summation}"
            for association in ASSOCIATIONS
            for summation in SUMMATIONS
        ],
        "desired_outputs_all_null": True,
        "gate1_status": "OPEN_PARTIAL_PROGRESS",
        "root_ODE_time_integrated_evaluations_declared": 0,
    }


def p44_subtree_digest(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def p44_verify_binary64_identity(
    array: np.ndarray, identity: Mapping[str, Any], *, label: str
) -> None:
    values = np.asarray(array, dtype=np.complex128).reshape(-1)
    if identity.get("shape") != list(array.shape):
        raise InvalidRun(f"binary64 identity shape drift: {label}")
    dtype, raw = canonical_array_bytes(array)
    if dtype != identity.get("canonical_dtype"):
        raise InvalidRun(f"binary64 identity dtype drift: {label}")
    if sha256_bytes(raw) != identity.get("canonical_raw_sha256"):
        raise InvalidRun(f"binary64 identity raw SHA drift: {label}")
    components = identity.get("components")
    if not isinstance(components, list) or len(components) != len(values):
        raise InvalidRun(f"binary64 identity component count drift: {label}")
    for index, (number, record) in enumerate(zip(values, components, strict=True)):
        for part_name, component in (
            ("real", float(number.real)),
            ("imag", float(number.imag)),
        ):
            numerator, denominator = component.as_integer_ratio()
            if record.get(f"{part_name}_hex") != component.hex():
                raise InvalidRun(f"binary64 hex drift: {label}/{index}/{part_name}")
            if record.get(f"{part_name}_ratio") != [numerator, denominator]:
                raise InvalidRun(f"binary64 ratio drift: {label}/{index}/{part_name}")
            signed_zero = component == 0.0 and math.copysign(1.0, component) < 0.0
            if record.get(f"{part_name}_signed_zero") is not signed_zero:
                raise InvalidRun(f"binary64 signed-zero drift: {label}/{index}/{part_name}")


def p44_parse_mp_vector(value: Any, *, label: str) -> tuple[mp.mpc, ...]:
    if not isinstance(value, list) or len(value) != 7:
        raise InvalidRun(f"stored mp vector shape drift: {label}")
    output: list[mp.mpc] = []
    with mp.workdps(AUTHORITATIVE_DPS):
        for index, pair in enumerate(value):
            if not isinstance(pair, list) or len(pair) != 2 or not all(
                isinstance(component, str) for component in pair
            ):
                raise InvalidRun(
                    f"stored mp component encoding drift: {label}/{index}"
                )
            number = mp.mpc(mp.mpf(pair[0]), mp.mpf(pair[1]))
            if not mp.isfinite(number.real) or not mp.isfinite(number.imag):
                raise InvalidRun(f"stored nonfinite mp component: {label}/{index}")
            output.append(number)
    return tuple(output)


def p44_install_forbidden_guards(phase41: ModuleType) -> dict[str, int]:
    counter: dict[str, int] = {}

    def forbidden(name: str) -> Callable[..., Any]:
        counter[name] = 0

        def reject(*_args: Any, **_kwargs: Any) -> Any:
            counter[name] += 1
            raise InvalidRun(f"forbidden Phase44 solver/trajectory/flow call: {name}")

        return reject

    names = (
        "solve_signed_saddle_grids",
        "solve_main_saddle",
        "solve_primary_intersections",
        "build_fixed_metric",
        "build_nested_chart",
        "residual_and_variational_jacobian",
        "integrate_chart",
        "integrate_augmented_chart",
        "flow_xi",
        "gradient_at",
        "action_at",
        "solve_ivp",
        "root",
        "least_squares",
    )
    for name in names:
        if hasattr(phase41, name):
            setattr(phase41, name, forbidden(name))
    return counter


def p44_load_context(manifest: Mapping[str, Any]) -> P44Context:
    artifacts = manifest["immutable_artifacts"]
    result_pin = artifacts["phase43_raw_result"]
    result, result_raw = read_pinned_json(
        PHASE43_RESULT_PATH,
        result_pin["outer_file_sha256_including_final_LF"],
        label="Phase43 raw result",
        expected_size=int(result_pin["size_bytes"]),
    )
    if result.get("schema") != PHASE43_RESULT_SCHEMA:
        raise InvalidRun("Phase43 result schema drift")
    if result.get("phase") != 43 or result.get("run_status") != "VALID_TYPED_RUN" or result.get("exit_code") != 0:
        raise InvalidRun("Phase43 result status drift")
    verify_self_digest(
        result,
        "result_payload_sha256_without_self",
        result_pin["result_payload_sha256_without_self"],
        label="Phase43 result",
    )
    ledger = result.get("slot_ledger")
    if not isinstance(ledger, dict):
        raise InvalidRun("Phase43 slot ledger missing")
    keys = sorted(ledger)
    pins = result_pin["canonical_subtree_pins"]
    subtrees = {
        "base_outcomes_sha256": result["base_outcomes"],
        "local_aggregation_sha256": result["local_aggregation"],
        "numerical_records_sha256": result["numerical_records"],
        "ninety_input_records_sha256": {
            key: ledger[key] for key in keys if key.startswith("input|")
        },
        "ninety_source_analytic_records_sha256": {
            key: ledger[key]
            for key in keys
            if key.startswith("source|") and key.endswith("|analytic")
        },
        "ninety_reference_hessian_120_records_sha256": {
            key: ledger[key]
            for key in keys
            if key.startswith("reference|")
            and "|dps=120|method=hessian" in key
        },
    }
    for name, subtree in subtrees.items():
        observed = p44_subtree_digest(subtree)
        if observed != pins[name]:
            raise InvalidRun(f"Phase43 canonical subtree drift: {name}")
    checkpoint_pin = artifacts["phase42_checkpoint"]
    checkpoint, checkpoint_raw = read_pinned_json(
        CHECKPOINT_PATH,
        checkpoint_pin["outer_file_sha256_including_final_LF"],
        label="Phase42 checkpoint",
        expected_size=int(checkpoint_pin["size_bytes"]),
    )
    if checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise InvalidRun("Phase42 checkpoint schema drift")
    verify_self_digest(
        checkpoint,
        "checkpoint_payload_sha256_without_self",
        checkpoint_pin["checkpoint_payload_sha256_without_self"],
        label="Phase42 checkpoint",
    )
    linear_map = decode_array_record(
        checkpoint["fixed_metric"]["linear_map"],
        path="$.fixed_metric.linear_map",
        expected_shape=(7, 7),
    )
    if np.iscomplexobj(linear_map):
        raise InvalidRun("Phase44 linear map must be real float64")
    phase41 = import_pinned_phase41(manifest)
    forbidden_counter = p44_install_forbidden_guards(phase41)
    variants = manifest["frozen_slot_universe"]["source_variants"]
    points: dict[str, P44PointInput] = {}
    for point in TARGETS:
        saddle = decode_array_record(
            checkpoint["saddles"][point]["saddle_w"],
            path=f"$.saddles.{point}.saddle_w",
            expected_shape=(7,),
        )
        delta_a = str(variants[point]["delta_a"])
        delta_phi = str(variants[point]["delta_phi"])
        source_point = checkpoint["saddles"][point]["source_point"]
        if source_point != {
            "delta_a": float(delta_a),
            "delta_phi": float(delta_phi),
        }:
            raise InvalidRun(f"Phase44 checkpoint source variant drift: {point}")
        model = phase41.numeric_model(float(delta_a), float(delta_phi))
        points[point] = P44PointInput(
            label=point,
            delta_a=delta_a,
            delta_phi=delta_phi,
            saddle_w=saddle,
            model=model,
        )
    outcomes = result.get("base_outcomes")
    if not isinstance(outcomes, list) or len(outcomes) != 90:
        raise InvalidRun("Phase43 base outcome cardinality drift")
    outcome_by_key = {
        (str(item["point"]), str(item["fraction"]), int(item["direction"])): (
            index,
            item,
        )
        for index, item in enumerate(outcomes)
    }
    slots: dict[tuple[str, str, int], P44SlotInput] = {}
    with mp.workdps(AUTHORITATIVE_DPS):
        for point in TARGETS:
            for fraction in FRACTION_STRINGS:
                for direction in DIRECTIONS:
                    base_key = (point, fraction, direction)
                    input_key = f"input|point={point}|fraction={fraction}|direction={direction}"
                    source_key = f"source|point={point}|fraction={fraction}|direction={direction}|analytic"
                    reference_key = f"reference|point={point}|fraction={fraction}|direction={direction}|dps=120|method=hessian"
                    rounding_key = f"reference|point={point}|fraction={fraction}|direction={direction}|dps=120|method=rounding_control"
                    records = [ledger.get(key) for key in (input_key, source_key, reference_key, rounding_key)]
                    if any(
                        not isinstance(record, dict)
                        or record.get("terminal_status") != "SUCCESS"
                        or not isinstance(record.get("payload"), dict)
                        for record in records
                    ):
                        raise InvalidRun(f"Phase43 required record incomplete: {base_key}")
                    input_payload = records[0]["payload"]
                    xi = decode_complex_pairs(input_payload["xi"], shape=(7,), path=f"{input_key}.xi")
                    q = decode_complex_pairs(input_payload["q"], shape=(7,), path=f"{input_key}.q")
                    p44_verify_binary64_identity(xi, input_payload["xi_binary64_identity"], label=f"{base_key}/xi")
                    p44_verify_binary64_identity(q, input_payload["q_binary64_identity"], label=f"{base_key}/q")
                    source_payload = records[1]["payload"]
                    source = decode_complex_pairs(
                        source_payload["value"], shape=(7,), path=f"{source_key}.value"
                    )
                    stored_phase42_source = decode_complex_pairs(
                        source_payload["stored_phase42_value"],
                        shape=(7,),
                        path=f"{source_key}.stored_phase42_value",
                    )
                    source_dtype, source_raw = canonical_array_bytes(source)
                    stored_dtype, stored_raw = canonical_array_bytes(stored_phase42_source)
                    if source_dtype != stored_dtype or source_raw != stored_raw:
                        raise InvalidRun(
                            f"Phase43 stored/source binary64 identity drift: {base_key}"
                        )
                    source_identity = binary64_payload(source)
                    reference = p44_parse_mp_vector(records[2]["payload"]["value"], label=reference_key)
                    rounding50 = p44_parse_mp_vector(records[3]["payload"]["value"], label=rounding_key)
                    outcome_entry = outcome_by_key.get(base_key)
                    if not isinstance(outcome_entry, tuple):
                        raise InvalidRun(f"Phase43 base outcome missing: {base_key}")
                    outcome_index, outcome = outcome_entry
                    if not isinstance(outcome, dict):
                        raise InvalidRun(
                            f"Phase43 base outcome malformed: {base_key}"
                        )
                    stored_relative_text = str(
                        outcome["source_to_reference_relative"]["value"]
                    )
                    source_rhs_evidence = outcome.get("source_rhs_evidence")
                    outcome_disclosed_anomaly = outcome.get("disclosed_anomaly")
                    stored_stable_violation = input_payload.get(
                        "stored_stable_violation"
                    )
                    if source_rhs_evidence not in ("SUPPORTED", "NOT_SUPPORTED"):
                        raise InvalidRun(
                            f"Phase43 stored source evidence malformed: {base_key}"
                        )
                    if not isinstance(outcome_disclosed_anomaly, bool) or not isinstance(
                        stored_stable_violation, bool
                    ):
                        raise InvalidRun(
                            f"Phase43 stored disclosure booleans malformed: {base_key}"
                        )
                    slots[base_key] = P44SlotInput(
                        point=point,
                        fraction=fraction,
                        direction=direction,
                        disclosed_mismatch=None,
                        disclosed_phase42_anomaly=None,
                        xi=xi,
                        q=q,
                        source=source,
                        source_binary64_identity=source_identity,
                        reference=reference,
                        rounding50_reference=rounding50,
                        p43_base_outcome_index=outcome_index,
                        p43_relative_text=stored_relative_text,
                        p43_source_rhs_evidence=str(source_rhs_evidence),
                        p43_disclosed_anomaly=outcome_disclosed_anomaly,
                        stored_fixed_to_analytic_symmetric_relative=float(
                            input_payload[
                                "stored_fixed_to_analytic_symmetric_relative"
                            ]
                        ),
                        stored_neighbor_symmetric_relative=float(
                            input_payload["stored_neighbor_symmetric_relative"]
                        ),
                        stored_stable_violation=stored_stable_violation,
                    )
    if len(slots) != 90 or any(
        slot.disclosed_mismatch is not None
        or slot.disclosed_phase42_anomaly is not None
        for slot in slots.values()
    ):
        raise InvalidRun("Phase44 decode-only slot universe drift")
    validation = {
        "phase43_outer_sha256": sha256_bytes(result_raw),
        "phase43_self_digest": result_pin["result_payload_sha256_without_self"],
        "checkpoint_outer_sha256": sha256_bytes(checkpoint_raw),
        "checkpoint_self_digest": checkpoint_pin["checkpoint_payload_sha256_without_self"],
        "canonical_subtree_hashes_verified": len(subtrees),
        "base_slot_count": len(slots),
        "disclosure_join_state": "DECODED_NOT_JOINED_BEFORE_KEY_FREEZE",
        "point_count": len(points),
        "time_column_records_consumed": 0,
        "root_ODE_integrated_calls": 0,
    }
    return P44Context(
        phase43_result=result,
        checkpoint=checkpoint,
        phase41=phase41,
        linear_map=np.asarray(linear_map, dtype=np.float64),
        points=points,
        slots=slots,
        forbidden_call_counter=forbidden_counter,
        validation=validation,
    )


def p44_reconstruct_disclosure_for_slot(
    slot: P44SlotInput, key: tuple[str, str, int]
) -> tuple[bool, bool]:
    with mp.workdps(AUTHORITATIVE_DPS):
        source_lift = tuple(
            mp_complex_from_binary64(value) for value in slot.source
        )
        recomputed_relative = mp_relative(source_lift, slot.reference)
        stored_relative = mp.mpf(slot.p43_relative_text)
        if abs(stored_relative - recomputed_relative) > mp.mpf("1e-100"):
            raise InvalidRun(f"Phase43 stored relative metric drift: {key}")
        mismatch = recomputed_relative > mp.mpf("5e-13")
        expected_evidence = "SUPPORTED" if mismatch else "NOT_SUPPORTED"
        if slot.p43_source_rhs_evidence != expected_evidence:
            raise InvalidRun(
                f"Phase43 independently reconstructed mismatch drift: {key}"
            )
        fixed_relative = mp.mpf(
            repr(slot.stored_fixed_to_analytic_symmetric_relative)
        )
        neighbor_relative = mp.mpf(
            repr(slot.stored_neighbor_symmetric_relative)
        )
        disclosed_anomaly = bool(
            fixed_relative > mp.mpf("1e-7")
            and neighbor_relative <= mp.mpf("1e-6")
        )
        if (
            slot.stored_stable_violation is not disclosed_anomaly
            or slot.p43_disclosed_anomaly is not disclosed_anomaly
        ):
            raise InvalidRun(
                f"Phase42 independently reconstructed anomaly drift: {key}"
            )
        return mismatch, disclosed_anomaly


def p44_join_disclosures_after_preenumeration(
    context: P44Context,
    manifest: Mapping[str, Any],
    preenumeration: Mapping[str, Any],
) -> P44Context:
    declared_keys = tuple(preenumeration.get("declared_keys_in_fixed_order", ()))
    expected_input_keys = tuple(
        f"input|{base_key(point, fraction, direction)}"
        for point in TARGETS
        for fraction in FRACTION_STRINGS
        for direction in DIRECTIONS
    )
    if (
        preenumeration.get("key_set_frozen_before_numerical_evaluation") is not True
        or len(expected_input_keys) != 90
        or any(key not in declared_keys for key in expected_input_keys)
        or len(set(declared_keys)) != len(declared_keys)
    ):
        raise InvalidRun("Phase44 disclosure join preceded complete key freeze")
    if any(
        slot.disclosed_mismatch is not None
        or slot.disclosed_phase42_anomaly is not None
        for slot in context.slots.values()
    ):
        raise InvalidRun("Phase44 disclosure labels were joined before key freeze")

    slots: dict[tuple[str, str, int], P44SlotInput] = {}
    disclosed: list[dict[str, Any]] = []
    for point in TARGETS:
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                key = (point, fraction, direction)
                slot = context.slots[key]
                mismatch, disclosed_anomaly = (
                    p44_reconstruct_disclosure_for_slot(slot, key)
                )
                if mismatch:
                    disclosed.append(
                        {
                            "point": point,
                            "fraction": fraction,
                            "direction": direction,
                            "phase42_disclosed_anomaly": disclosed_anomaly,
                            "phase43_relative": slot.p43_relative_text,
                        }
                    )
                slots[key] = dataclasses.replace(
                    slot,
                    disclosed_mismatch=mismatch,
                    disclosed_phase42_anomaly=disclosed_anomaly,
                )

    declared = manifest["known_prior_results_and_audit_disclosure"][
        "all_thirteen_disclosed_mismatch_slots"
    ]
    if disclosed != declared or len(disclosed) != 13:
        raise InvalidRun("Phase44 disclosed thirteen-slot cohort drift")
    if len(slots) != 90 or sum(
        slot.disclosed_mismatch is True for slot in slots.values()
    ) != 13:
        raise InvalidRun("Phase44 90/13/77 slot split drift")
    mismatch_counts = {
        point: sum(
            slot.disclosed_mismatch is True
            for slot in slots.values()
            if slot.point == point
        )
        for point in TARGETS
    }
    if mismatch_counts != {"shared_zero": 5, "phi_plus": 3, "a_plus": 5}:
        raise InvalidRun("Phase44 independently reconstructed 5/3/5 split drift")
    anomaly_overlap_count = sum(
        slot.disclosed_mismatch is True
        and slot.disclosed_phase42_anomaly is True
        for slot in slots.values()
    )
    if anomaly_overlap_count != 5:
        raise InvalidRun("Phase44 independently reconstructed anomaly overlap drift")
    validation = dict(context.validation)
    validation.update(
        {
            "disclosure_join_state": "JOINED_AFTER_COMPLETE_KEY_FREEZE",
            "preenumerated_key_count_before_disclosure_join": int(
                preenumeration["declared_key_count"]
            ),
            "preenumerated_key_sha256_before_disclosure_join": str(
                preenumeration["declared_keys_sha256"]
            ),
            "disclosed_mismatch_count": 13,
            "within_threshold_control_count": 77,
            "mismatch_counts_by_point": mismatch_counts,
            "phase42_anomaly_overlap_count": anomaly_overlap_count,
        }
    )
    return dataclasses.replace(context, slots=slots, validation=validation)


def p44_midpoint_element(
    left_a: sp.Expr,
    left_phi: sp.Expr,
    right_a: sp.Expr,
    right_phi: sp.Expr,
    proper_time: sp.Expr,
) -> sp.Expr:
    midpoint_a = (left_a + right_a) / sp.Integer(2)
    midpoint_phi = (left_phi + right_phi) / sp.Integer(2)
    difference_a = right_a - left_a
    difference_phi = right_phi - left_phi
    step = sp.Rational(1, 4)
    potential = sp.Rational(3, 4) * (
        sp.Integer(1) - sp.exp(-sp.sqrt(sp.Rational(2, 3)) * midpoint_phi)
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


def p44_generic_independent_action() -> tuple[
    sp.Expr,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    sp.Symbol,
    sp.Symbol,
    sp.Symbol,
    sp.Symbol,
]:
    z = sp.symbols("p44_z_a1 p44_z_phi1 p44_z_a2 p44_z_phi2 p44_z_a3 p44_z_phi3 p44_z_T")
    w = sp.symbols("p44_w_a1 p44_w_phi1 p44_w_a2 p44_w_phi2 p44_w_a3 p44_w_phi3 p44_w_T")
    scales = sp.symbols("p44_s0:7")
    base_a, base_phi, delta_a, delta_phi = sp.symbols(
        "p44_base_a p44_base_phi p44_delta_a p44_delta_phi"
    )
    nodes = (
        (base_a * (1 - delta_a / 2), base_phi - delta_phi / 2),
        (z[0], z[1]),
        (z[2], z[3]),
        (z[4], z[5]),
        (base_a * (1 + delta_a / 2), base_phi + delta_phi / 2),
    )
    elements = tuple(
        p44_midpoint_element(*nodes[index], *nodes[index + 1], z[-1])
        for index in range(4)
    )
    action_z = sp.expand(sum(elements, sp.Integer(0)))
    independent_action = action_z.subs(
        {z[index]: scales[index] * w[index] for index in range(7)}
    )
    return independent_action, tuple(z), tuple(w), tuple(scales), base_a, base_phi, delta_a, delta_phi


def p44_canonical_difference(left: sp.Expr, right: sp.Expr) -> dict[str, Any]:
    before = left - right
    together = sp.together(before)
    cancelled = sp.cancel(together)
    final = sp.expand(cancelled)
    numerator, denominator = sp.fraction(final)
    return {
        "pre_srepr_sha256": sha256_bytes(sp.srepr(before).encode("utf-8")),
        "post_srepr_sha256": sha256_bytes(sp.srepr(final).encode("utf-8")),
        "pre_count_ops": int(sp.count_ops(before)),
        "post_count_ops": int(sp.count_ops(final)),
        "pre_free_symbols": sorted(str(symbol) for symbol in before.free_symbols),
        "post_free_symbols": sorted(str(symbol) for symbol in final.free_symbols),
        "free_symbols": sorted(str(symbol) for symbol in final.free_symbols),
        "exact_zero": bool(final == 0),
        "syntactic_nonzero_is_not_alone_a_rigorous_transcendental_nonzero_witness": bool(
            final != 0
        ),
        "rigorous_nonzero_witness": None if final != 0 else False,
        "numerator_srepr": sp.srepr(numerator),
        "denominator_srepr": sp.srepr(denominator),
        "canonicalization_order": ["together", "cancel", "expand"],
    }


def p44_formula_audit(
    context: P44Context,
) -> tuple[dict[str, Any], dict[str, str]]:
    generic_action, generic_z, generic_w, scales, base_a, base_phi, delta_a, delta_phi = (
        p44_generic_independent_action()
    )
    if any(isinstance(node, sp.Float) for node in sp.preorder_traversal(generic_action)):
        raise InvalidRun("SymPy Float entered Phase44 exact independent action")
    source_family = context.phase41.build_symbolic_family()
    semantic_targets: dict[str, sp.Expr] = {
        "a_1": generic_z[0],
        "phi_1": generic_z[1],
        "a_2": generic_z[2],
        "phi_2": generic_z[3],
        "a_3": generic_z[4],
        "phi_3": generic_z[5],
        "T": generic_z[6],
        "a_boundary": base_a,
        "phi_boundary": base_phi,
        "delta_a": delta_a,
        "delta_phi": delta_phi,
    }
    source_symbols = (
        *source_family.variables_z,
        source_family.boundary_a,
        source_family.boundary_phi,
        source_family.delta_a,
        source_family.delta_phi,
    )
    source_symbols_by_name = {symbol.name: symbol for symbol in source_symbols}
    if len(source_symbols_by_name) != len(source_symbols) or set(
        source_symbols_by_name
    ) != set(semantic_targets):
        raise InvalidRun("Phase44 source semantic-symbol names drift")
    source_map: dict[sp.Symbol, sp.Expr] = {
        source_symbols_by_name[name]: target
        for name, target in semantic_targets.items()
    }
    source_action_z = source_family.action_z.xreplace(source_map)
    source_action = source_action_z.subs(
        {generic_z[index]: scales[index] * generic_w[index] for index in range(7)}
    )
    if any(isinstance(node, sp.Float) for node in sp.preorder_traversal(source_action)):
        raise InvalidRun("SymPy Float entered Phase44 exact source-side action")
    by_point: dict[str, Any] = {}
    formula_mismatch_states: dict[str, str] = {}
    for point in TARGETS:
        point_input = context.points[point]
        substitutions = {
            delta_a: sp.Rational(point_input.delta_a),
            delta_phi: sp.Rational(point_input.delta_phi),
        }
        independent = generic_action.subs(substitutions)
        source = source_action.subs(substitutions)
        independent_gradient = sp.Matrix(
            [sp.diff(independent, variable) for variable in generic_w]
        )
        source_gradient = sp.Matrix(
            [sp.diff(source, variable) for variable in generic_w]
        )
        independent_hessian = sp.hessian(independent, generic_w)
        source_hessian = sp.hessian(source, generic_w)
        action_record = p44_canonical_difference(source, independent)
        gradient_records = [
            p44_canonical_difference(source_gradient[index], independent_gradient[index])
            for index in range(7)
        ]
        hessian_records = [
            [
                p44_canonical_difference(
                    source_hessian[row, column], independent_hessian[row, column]
                )
                for column in range(7)
            ]
            for row in range(7)
        ]
        identity = bool(
            action_record["exact_zero"]
            and all(record["exact_zero"] for record in gradient_records)
            and all(
                record["exact_zero"]
                for row in hessian_records
                for record in row
            )
        )
        formula_mismatch_states[point] = (
            "NOT_SUPPORTED" if identity else "SUPPORTED"
        )
        by_point[point] = {
            "delta_a": point_input.delta_a,
            "delta_phi": point_input.delta_phi,
            "action": action_record,
            "gradient": gradient_records,
            "hessian": hessian_records,
            "formula_identity": identity,
            "formula_mismatch_evidence": formula_mismatch_states[point],
            "symbolic_placeholders_retained": {
                "base_a": str(base_a),
                "base_phi": str(base_phi),
                "coordinate_scales": [str(scale) for scale in scales],
                "all_present_before_canonicalization": all(
                    symbol in independent.free_symbols
                    and symbol in source.free_symbols
                    for symbol in (base_a, base_phi, *scales)
                ),
            },
            "nonzero_policy": (
                "Per the frozen protocol, a nonzero fixed-chain canonical expression "
                "is formula-mismatch evidence SUPPORTED. This is protocol-defined "
                "canonical-expression evidence, not a general transcendental "
                "nonidentity theorem."
            ),
            "action_components": 1,
            "gradient_components": 7,
            "hessian_components": 49,
        }
    return (
        {
            "by_point": by_point,
            "independent_constructor_source_sha256": sha256_bytes(
                inspect.getsource(p44_generic_independent_action).encode("utf-8")
            ),
            "midpoint_constructor_source_sha256": sha256_bytes(
                inspect.getsource(p44_midpoint_element).encode("utf-8")
            ),
            "source_side_used_only_action_z": True,
            "source_side_access": {
                "build_symbolic_family_source_sha256": sha256_bytes(
                    inspect.getsource(context.phase41.build_symbolic_family).encode(
                        "utf-8"
                    )
                ),
                "action_z_srepr_sha256": sha256_bytes(
                    sp.srepr(source_family.action_z).encode("utf-8")
                ),
                "source_variable_names": [
                    str(symbol) for symbol in source_family.variables_z
                ],
                "semantic_symbol_map": {
                    str(source_symbol): str(source_map[source_symbol])
                    for source_symbol in source_map
                },
                "forbidden_source_objects_consumed": [],
            },
            "independent_boundary_audit": {
                "constructor_source_contains_phase41": "phase41"
                in inspect.getsource(p44_generic_independent_action),
                "constructor_source_contains_lambdify": "lambdify"
                in inspect.getsource(p44_generic_independent_action),
                "constructor_source_contains_evalf": "evalf"
                in inspect.getsource(p44_generic_independent_action),
                "constructor_source_contains_numpy": any(
                    token in inspect.getsource(p44_generic_independent_action)
                    for token in ("numpy", "np.")
                ),
                "independence_denylist_passed": not any(
                    token in inspect.getsource(p44_generic_independent_action)
                    for token in (
                        "phase41",
                        "lambdify",
                        "evalf",
                        "numpy",
                        "np.",
                        "action_w",
                        "gradient_w",
                        "hessian_w",
                    )
                ),
            },
            "exact_tree_has_no_SymPy_Float": True,
            "canonicalization_order": ["together", "cancel", "expand"],
        },
        formula_mismatch_states,
    )


def p44_make_numeric_symbolic(point: P44PointInput) -> P44NumericSymbolic:
    w = sp.symbols("p44_num_w_a1 p44_num_w_phi1 p44_num_w_a2 p44_num_w_phi2 p44_num_w_a3 p44_num_w_phi3 p44_num_w_T")
    z = sp.symbols("p44_num_a1 p44_num_phi1 p44_num_a2 p44_num_phi2 p44_num_a3 p44_num_phi3 p44_num_T")

    def build(use_float50: bool) -> tuple[sp.Expr, sp.Matrix, sp.Matrix]:
        make: Callable[[str], sp.Expr]
        if use_float50:
            make = lambda text: sp.Float(text, 50)
        else:
            make = lambda text: sp.Rational(text)
        base_a = make("3.5668031935672753")
        base_phi = make("1.0185809464006637")
        da = make(point.delta_a)
        dp = make(point.delta_phi)
        scale_texts = (
            "3.5668031935672753",
            "1.0185809464006637",
            "3.5668031935672753",
            "1.0185809464006637",
            "3.5668031935672753",
            "1.0185809464006637",
            "0.7",
        )
        nodes = (
            (base_a * (1 - da / 2), base_phi - dp / 2),
            (z[0], z[1]),
            (z[2], z[3]),
            (z[4], z[5]),
            (base_a * (1 + da / 2), base_phi + dp / 2),
        )
        action_z = sp.expand(
            sum(
                (
                    p44_midpoint_element(*nodes[index], *nodes[index + 1], z[-1])
                    for index in range(4)
                ),
                sp.Integer(0),
            )
        )
        action = action_z.subs(
            {z[index]: make(scale_texts[index]) * w[index] for index in range(7)}
        )
        gradient = sp.Matrix([sp.diff(action, variable) for variable in w])
        return action, gradient, sp.hessian(action, w)

    exact_action, exact_gradient, exact_hessian = build(False)
    _rounding_action, _rounding_gradient, rounding_hessian = build(True)
    if any(isinstance(node, sp.Float) for node in sp.preorder_traversal(exact_action)):
        raise InvalidRun("Float entered Phase44 exact numerical reference tree")
    exact_function = sp.lambdify((w,), exact_hessian, modules="mpmath")
    rounding_function = sp.lambdify((w,), rounding_hessian, modules="mpmath")
    return P44NumericSymbolic(
        w=tuple(w),
        exact_action=exact_action,
        exact_gradient=exact_gradient,
        exact_hessian=exact_hessian,
        rounding50_hessian=rounding_hessian,
        exact_hessian_function=exact_function,
        rounding50_hessian_function=rounding_function,
        fingerprints={
            "exact_action_srepr_sha256": sha256_bytes(sp.srepr(exact_action).encode("utf-8")),
            "exact_gradient_srepr_sha256": sha256_bytes(sp.srepr(exact_gradient).encode("utf-8")),
            "exact_hessian_srepr_sha256": sha256_bytes(sp.srepr(exact_hessian).encode("utf-8")),
            "rounding50_hessian_srepr_sha256": sha256_bytes(sp.srepr(rounding_hessian).encode("utf-8")),
        },
    )


@dataclass(frozen=True)
class P44NodeValue:
    actual: Any
    ideal: mp.mpc
    coefficient_semantics: mp.mpc
    model_radius: mp.mpf
    observed_radius: mp.mpf
    model_ok: bool


@dataclass
class P44TraceStream:
    whole: Any = field(default_factory=hashlib.sha256)
    path_operation: Any = field(default_factory=hashlib.sha256)
    chunk: Any = field(default_factory=hashlib.sha256)
    chunk_event_count: int = 0
    event_count: int = 0
    chunk_hashes: list[str] = field(default_factory=list)
    operation_histogram: dict[str, int] = field(default_factory=dict)
    status_histogram: dict[str, int] = field(default_factory=dict)
    expanded_events: list[dict[str, Any]] = field(default_factory=list)
    path_operation_records: list[dict[str, str]] = field(default_factory=list)
    subnormal_identity_count: int = 0

    def add(self, event: Mapping[str, Any]) -> bytes:
        encoded = canonical_json_bytes(dict(event))
        framed = len(encoded).to_bytes(8, "big", signed=False) + encoded
        self.whole.update(framed)
        path_encoded = canonical_json_bytes(
            {
                "node_path": str(event["node_path"]),
                "operation": str(event["operation"]),
            }
        )
        self.path_operation.update(
            len(path_encoded).to_bytes(8, "big", signed=False) + path_encoded
        )
        self.path_operation_records.append(
            {
                "node_path": str(event["node_path"]),
                "operation": str(event["operation"]),
            }
        )
        def count_subnormal(value: Any) -> int:
            if isinstance(value, dict):
                return sum(
                    (1 if key in ("real_subnormal", "imag_subnormal") and child is True else 0)
                    + count_subnormal(child)
                    for key, child in value.items()
                )
            if isinstance(value, list):
                return sum(count_subnormal(child) for child in value)
            return 0
        self.subnormal_identity_count += count_subnormal(event)
        self.chunk.update(framed)
        self.chunk_event_count += 1
        self.event_count += 1
        operation_name = str(event["operation"])
        status = str(event["terminal_status"])
        self.operation_histogram[operation_name] = (
            self.operation_histogram.get(operation_name, 0) + 1
        )
        self.status_histogram[status] = self.status_histogram.get(status, 0) + 1
        if status != "SUCCESS" or event.get("model_exceeding") is True:
            self.expanded_events.append(dict(event))
        if self.chunk_event_count == 256:
            self.chunk_hashes.append(self.chunk.hexdigest())
            self.chunk = hashlib.sha256()
            self.chunk_event_count = 0
        return framed

    def finish(self) -> dict[str, Any]:
        if self.chunk_event_count:
            self.chunk_hashes.append(self.chunk.hexdigest())
            self.chunk = hashlib.sha256()
            self.chunk_event_count = 0
        return {
            "event_count": self.event_count,
            "chunk_size": 256,
            "chunk_count": len(self.chunk_hashes),
            "chunk_sha256_in_fixed_order": list(self.chunk_hashes),
            "whole_trace_sha256": self.whole.hexdigest(),
            "path_operation_commitment_sha256": self.path_operation.hexdigest(),
            "operation_histogram": dict(sorted(self.operation_histogram.items())),
            "terminal_status_histogram": dict(sorted(self.status_histogram.items())),
            "expanded_exception_or_model_exceeding_events": self.expanded_events,
            "subnormal_identity_count": self.subnormal_identity_count,
            "subnormal_model_ambiguity": self.subnormal_identity_count > 0,
        }


@dataclass(frozen=True)
class P44CallablePlan:
    variant: str
    function: Callable[..., Any]
    source: str
    tree: ast.Module
    function_node: ast.FunctionDef
    argument_name: str
    state_names: tuple[str, ...]
    entries: tuple[tuple[ast.AST, ...], ...]
    normalized_ast_sha256: str
    fingerprint: Mapping[str, Any]
    exact50_literal_mapping: Mapping[str, Any]
    constant_occurrences: Mapping[str, tuple[tuple[ast.AST, str], ...]]
    constant_node_ids: frozenset[int]
    constant_by_node: Mapping[int, P44NodeValue]
    constant_records: Mapping[str, Any]
    constant_model_ok: bool


P44_ALLOWED_AST_NODE_NAMES = {
    "Add",
    "Assign",
    "BinOp",
    "Call",
    "Constant",
    "Div",
    "FunctionDef",
    "List",
    "Load",
    "Module",
    "Mult",
    "Name",
    "Pow",
    "Return",
    "Store",
    "Sub",
    "USub",
    "UnaryOp",
    "arg",
    "arguments",
}


def p44_alpha_normalized_ast_dump(tree: ast.AST) -> str:
    cloned = copy.deepcopy(tree)
    dummy_names = {
        node.id
        for node in ast.walk(cloned)
        if isinstance(node, ast.Name)
        and node.id.startswith("_Dummy_")
        and node.id[7:].isdigit()
    }
    dummy_names.update(
        node.arg
        for node in ast.walk(cloned)
        if isinstance(node, ast.arg)
        and node.arg.startswith("_Dummy_")
        and node.arg[7:].isdigit()
    )
    if len(dummy_names) != 1:
        raise InvalidRun("generated callable does not have one alpha-normalizable Dummy")
    dummy = next(iter(dummy_names))

    class Normalize(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            if node.id == dummy:
                node.id = "_INPUT"
            return node

        def visit_arg(self, node: ast.arg) -> ast.AST:
            if node.arg == dummy:
                node.arg = "_INPUT"
            return node

    normalized = Normalize().visit(cloned)
    ast.fix_missing_locations(normalized)
    return ast.dump(normalized, annotate_fields=True, include_attributes=False)


def p44_json_code_constant(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return {
            "type": "float",
            "hex": value.hex(),
            "ratio": list(value.as_integer_ratio()),
        }
    if isinstance(value, complex):
        return {
            "type": "complex",
            "real_hex": float(value.real).hex(),
            "imag_hex": float(value.imag).hex(),
        }
    if isinstance(value, tuple):
        return [p44_json_code_constant(item) for item in value]
    if hasattr(value, "co_code"):
        return {
            "type": "code",
            "bytecode_sha256": sha256_bytes(value.co_code),
            "constants": [p44_json_code_constant(item) for item in value.co_consts],
            "names": list(value.co_names),
            "varnames": list(value.co_varnames),
        }
    return {"type": type(value).__name__, "repr": repr(value)}


def p44_callable_fingerprint(function: Callable[..., Any]) -> dict[str, Any]:
    source = inspect.getsource(function)
    tree = ast.parse(source)
    dump = ast.dump(tree, annotate_fields=True, include_attributes=False)
    code = function.__code__
    return {
        "inspect_source_text": source,
        "source_sha256": sha256_bytes(source.encode("utf-8")),
        "source_size_bytes": len(source.encode("utf-8")),
        "ast_dump": dump,
        "ast_dump_sha256": sha256_bytes(dump.encode("utf-8")),
        "normalized_ast_sha256": sha256_bytes(
            p44_alpha_normalized_ast_dump(tree).encode("utf-8")
        ),
        "code_bytecode_hex": code.co_code.hex(),
        "code_bytecode_sha256": sha256_bytes(code.co_code),
        "code_constants": [p44_json_code_constant(value) for value in code.co_consts],
        "code_names": list(code.co_names),
        "code_varnames": list(code.co_varnames),
        "code_argcount": int(code.co_argcount),
    }


def p44_scalar_identity(value: Any) -> dict[str, Any]:
    number = complex(value)
    if not math.isfinite(number.real) or not math.isfinite(number.imag):
        raise SlotEvaluationError("nonfinite scalar AST value")
    return {
        "python_type": f"{type(value).__module__}.{type(value).__qualname__}",
        "real_hex": float(number.real).hex(),
        "imag_hex": float(number.imag).hex(),
        "real_ratio": list(float(number.real).as_integer_ratio()),
        "imag_ratio": list(float(number.imag).as_integer_ratio()),
        "real_signed_zero": bool(
            number.real == 0.0 and math.copysign(1.0, number.real) < 0.0
        ),
        "real_subnormal": bool(
            number.real != 0.0 and abs(number.real) < sys.float_info.min
        ),
        "imag_subnormal": bool(
            number.imag != 0.0 and abs(number.imag) < sys.float_info.min
        ),
        "imag_signed_zero": bool(
            number.imag == 0.0 and math.copysign(1.0, number.imag) < 0.0
        ),
    }


def p44_ulp_radius(component: float, count: int) -> mp.mpf:
    if not math.isfinite(component):
        raise SlotEvaluationError("nonfinite component in ulp radius")
    spacing = math.ulp(component)
    return mp_from_binary64(spacing) * count


def p44_component_ulp_distances(actual: Any, exact: Any) -> tuple[mp.mpf, mp.mpf]:
    lifted = mp_complex_from_binary64(complex(actual))
    target = mp.mpc(exact)
    real_spacing = p44_ulp_radius(float(complex(actual).real), 1)
    imag_spacing = p44_ulp_radius(float(complex(actual).imag), 1)
    return (
        abs(lifted.real - target.real) / real_spacing,
        abs(lifted.imag - target.imag) / imag_spacing,
    )


def p44_actual_scalar_operation(operation_name: str, operands: Sequence[Any]) -> Any:
    with np.errstate(all="raise"):
        if operation_name == "add":
            return operator.add(operands[0], operands[1])
        if operation_name == "subtract":
            return operator.sub(operands[0], operands[1])
        if operation_name == "multiply":
            return operator.mul(operands[0], operands[1])
        if operation_name == "divide":
            return operator.truediv(operands[0], operands[1])
        if operation_name == "power":
            return operator.pow(operands[0], operands[1])
        if operation_name == "unary_plus":
            return operator.pos(operands[0])
        if operation_name == "unary_minus":
            return operator.neg(operands[0])
        if operation_name == "exp":
            return np.exp(operands[0])
        if operation_name == "sqrt":
            return np.sqrt(operands[0])
    raise InvalidRun(f"undeclared scalar AST operation: {operation_name}")


def p44_exact_scalar_operation(operation_name: str, operands: Sequence[Any]) -> mp.mpc:
    values = [mp.mpc(value) for value in operands]
    if operation_name == "add":
        return values[0] + values[1]
    if operation_name == "subtract":
        return values[0] - values[1]
    if operation_name == "multiply":
        return values[0] * values[1]
    if operation_name == "divide":
        return values[0] / values[1]
    if operation_name == "power":
        exponent = int(values[1].real)
        if values[1].imag != 0 or exponent < 0 or values[1].real != exponent:
            raise InvalidRun("generated callable has undeclared power exponent")
        return values[0] ** exponent
    if operation_name == "unary_plus":
        return +values[0]
    if operation_name == "unary_minus":
        return -values[0]
    if operation_name == "exp":
        return mp.exp(values[0])
    if operation_name == "sqrt":
        return mp.sqrt(values[0])
    raise InvalidRun(f"undeclared exact scalar AST operation: {operation_name}")


def p44_local_and_propagated_radii(
    operation_name: str,
    actual: Any,
    children: Sequence[P44NodeValue],
    local_exact: mp.mpc,
    *,
    observed: bool,
) -> tuple[mp.mpf, mp.mpf, bool, tuple[mp.mpf, mp.mpf]]:
    gamma1, _gamma1_ratio = p44_gamma_exact(1)
    gamma3, _gamma3_ratio = p44_gamma_exact(3)
    actual_lift = mp_complex_from_binary64(complex(actual))
    local_residual = actual_lift - local_exact
    child_radii = [
        child.observed_radius if observed else child.model_radius
        for child in children
    ]
    propagated = mp.mpf("0")
    local_real = mp.mpf("0")
    local_imag = mp.mpf("0")
    if operation_name in ("unary_plus", "unary_minus"):
        propagated = child_radii[0]
    elif operation_name in ("add", "subtract"):
        propagated = child_radii[0] + child_radii[1]
        local_real = gamma1 * abs(actual_lift.real)
        local_imag = gamma1 * abs(actual_lift.imag)
    elif operation_name == "multiply":
        a = mp_complex_from_binary64(complex(children[0].actual))
        b = mp_complex_from_binary64(complex(children[1].actual))
        propagated = (
            abs(a) * child_radii[1]
            + abs(b) * child_radii[0]
            + child_radii[0] * child_radii[1]
        )
        local_real = gamma3 * (
            abs(a.real * b.real) + abs(a.imag * b.imag)
        )
        local_imag = gamma3 * (
            abs(a.real * b.imag) + abs(a.imag * b.real)
        )
    elif operation_name == "divide":
        a = mp_complex_from_binary64(complex(children[0].actual))
        b = mp_complex_from_binary64(complex(children[1].actual))
        if abs(b) <= child_radii[1]:
            return mp.mpf("0"), mp.mpf("0"), False, (
                mp.mpf("0"),
                mp.mpf("0"),
            )
        propagated = (
            child_radii[0] + abs(a / b) * child_radii[1]
        ) / (abs(b) - child_radii[1])
        local_real = p44_ulp_radius(float(actual_lift.real), 8)
        local_imag = p44_ulp_radius(float(actual_lift.imag), 8)
    elif operation_name == "power":
        base = mp_complex_from_binary64(complex(children[0].actual))
        exponent_lift = mp_complex_from_binary64(complex(children[1].actual))
        exponent = int(exponent_lift.real)
        if (
            exponent_lift.imag != 0
            or exponent_lift.real != exponent
            or exponent < 0
        ):
            return mp.mpf("0"), mp.mpf("0"), False, (
                mp.mpf("0"),
                mp.mpf("0"),
            )
        propagated = (
            (abs(base) + child_radii[0]) ** exponent - abs(base) ** exponent
        )
        local_real = p44_ulp_radius(float(actual_lift.real), 8)
        local_imag = p44_ulp_radius(float(actual_lift.imag), 8)
    elif operation_name == "exp":
        center = mp_complex_from_binary64(complex(children[0].actual))
        propagated = abs(mp.exp(center)) * (mp.exp(child_radii[0]) - 1)
        local_real = p44_ulp_radius(float(actual_lift.real), 8)
        local_imag = p44_ulp_radius(float(actual_lift.imag), 8)
    elif operation_name == "sqrt":
        center = mp_complex_from_binary64(complex(children[0].actual))
        if center.imag != 0 or center.real <= child_radii[0]:
            return mp.mpf("0"), mp.mpf("0"), False, (
                mp.mpf("0"),
                mp.mpf("0"),
            )
        propagated = child_radii[0] / (
            mp.sqrt(center.real) + mp.sqrt(center.real - child_radii[0])
        )
        local_real = p44_ulp_radius(float(actual_lift.real), 8)
        local_imag = p44_ulp_radius(float(actual_lift.imag), 8)
    else:
        raise InvalidRun(f"no scalar radius rule for {operation_name}")
    local_disk = mp.sqrt(local_real**2 + local_imag**2)
    if observed:
        local_disk = abs(local_residual)
    radius = propagated + local_disk
    local_ok = bool(
        abs(local_residual.real) <= local_real
        and abs(local_residual.imag) <= local_imag
    )
    return radius, local_disk, local_ok, (local_real, local_imag)


def p44_ast_operation(node: ast.AST) -> str:
    if isinstance(node, ast.BinOp):
        mapping = {
            ast.Add: "add",
            ast.Sub: "subtract",
            ast.Mult: "multiply",
            ast.Div: "divide",
            ast.Pow: "power",
        }
        for kind, name in mapping.items():
            if isinstance(node.op, kind):
                return name
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return "unary_plus"
        if isinstance(node.op, ast.USub):
            return "unary_minus"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in ("exp", "sqrt"):
            return node.func.id
    raise InvalidRun(f"undeclared evaluation AST node: {type(node).__name__}")


def p44_trace_event(
    *,
    path: str,
    operation_name: str,
    children: Sequence[P44NodeValue],
    result: P44NodeValue,
    local_exact: mp.mpc,
    local_model_components: tuple[mp.mpf, mp.mpf],
    local_model_ok: bool,
) -> dict[str, Any]:
    actual_lift = mp_complex_from_binary64(complex(result.actual))
    local_residual = actual_lift - local_exact
    local_bound = mp.sqrt(
        local_model_components[0] ** 2 + local_model_components[1] ** 2
    )
    utilization = abs(local_residual) / max(local_bound, mp.mpf("1e-100"))
    ulp_distances = p44_component_ulp_distances(result.actual, local_exact)
    return {
        "node_path": path,
        "operation": operation_name,
        "operand_identities": [p44_scalar_identity(child.actual) for child in children],
        "output_identity": p44_scalar_identity(result.actual),
        "exact_120dps_counterpart": mp_complex_payload(result.ideal, AUTHORITATIVE_DPS),
        "coefficient_semantics_120dps": mp_complex_payload(
            result.coefficient_semantics, AUTHORITATIVE_DPS
        ),
        "local_exact_lifted_operand_result": mp_complex_payload(
            local_exact, AUTHORITATIVE_DPS
        ),
        "local_residual": mp_complex_payload(local_residual, AUTHORITATIVE_DPS),
        "local_model_component_radii": [
            mp_number_string(local_model_components[0], AUTHORITATIVE_DPS),
            mp_number_string(local_model_components[1], AUTHORITATIVE_DPS),
        ],
        "model_radius": mp_number_string(result.model_radius, AUTHORITATIVE_DPS),
        "observed_radius": mp_number_string(result.observed_radius, AUTHORITATIVE_DPS),
        "local_model_utilization": mp_number_string(utilization, AUTHORITATIVE_DPS),
        "component_ulp_distances": [
            mp_number_string(ulp_distances[0], AUTHORITATIVE_DPS),
            mp_number_string(ulp_distances[1], AUTHORITATIVE_DPS),
        ],
        "model_exceeding": not local_model_ok,
        "terminal_status": "SUCCESS",
    }


def p44_nested_node_payload(
    values: Any, selector: Callable[[P44NodeValue], Any]
) -> Any:
    if isinstance(values, P44NodeValue):
        return selector(values)
    if isinstance(values, (list, tuple)):
        return [p44_nested_node_payload(value, selector) for value in values]
    raise InvalidRun("structural trace node-value shape drift")


def p44_structural_trace_event(
    *,
    path: str,
    operation_name: str,
    values: Any,
    operand_identities: Sequence[Any],
    output_identity: Mapping[str, Any],
) -> dict[str, Any]:
    zero = mp.mpc("0")
    zero_text = mp_number_string(mp.mpf("0"), AUTHORITATIVE_DPS)
    return {
        "node_path": path,
        "operation": operation_name,
        "operand_identities": list(operand_identities),
        "output_identity": dict(output_identity),
        "exact_120dps_counterpart": p44_nested_node_payload(
            values,
            lambda value: mp_complex_payload(value.ideal, AUTHORITATIVE_DPS),
        ),
        "coefficient_semantics_120dps": p44_nested_node_payload(
            values,
            lambda value: mp_complex_payload(
                value.coefficient_semantics, AUTHORITATIVE_DPS
            ),
        ),
        "local_exact_lifted_operand_result": p44_nested_node_payload(
            values,
            lambda value: mp_complex_payload(
                mp_complex_from_binary64(complex(value.actual)),
                AUTHORITATIVE_DPS,
            ),
        ),
        "local_residual": p44_nested_node_payload(
            values, lambda _value: mp_complex_payload(zero, AUTHORITATIVE_DPS)
        ),
        "local_model_component_radii": p44_nested_node_payload(
            values, lambda _value: [zero_text, zero_text]
        ),
        "model_radius": p44_nested_node_payload(
            values,
            lambda value: mp_number_string(value.model_radius, AUTHORITATIVE_DPS),
        ),
        "observed_radius": p44_nested_node_payload(
            values,
            lambda value: mp_number_string(value.observed_radius, AUTHORITATIVE_DPS),
        ),
        "local_model_utilization": p44_nested_node_payload(
            values, lambda _value: zero_text
        ),
        "component_ulp_distances": p44_nested_node_payload(
            values, lambda _value: [zero_text, zero_text]
        ),
        "model_exceeding": False,
        "terminal_status": "SUCCESS",
    }


def p44_evaluate_ast_node(
    node: ast.AST,
    *,
    source: str,
    environment: Mapping[str, Any],
    state_names: frozenset[str],
    constant_by_node: Mapping[int, P44NodeValue],
    path: str,
    stream: P44TraceStream,
    allow_constant_reuse: bool,
) -> P44NodeValue:
    if allow_constant_reuse and id(node) in constant_by_node:
        cached = constant_by_node[id(node)]
        local_components = (cached.model_radius, mp.mpf("0"))
        event = p44_trace_event(
            path=path,
            operation_name="constant_subtree_reuse",
            children=(),
            result=cached,
            local_exact=cached.ideal,
            local_model_components=local_components,
            local_model_ok=cached.model_ok,
        )
        stream.add(event)
        return cached
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise InvalidRun("generated callable has nonnumeric scalar literal")
        actual = node.value
        segment = ast.get_source_segment(source, node)
        if not isinstance(segment, str):
            raise InvalidRun("cannot recover generated literal source segment")
        ideal = mp.mpc(mp.mpf(segment), 0)
        actual_lift = mp_complex_from_binary64(complex(actual))
        if isinstance(actual, int):
            model_radius = mp.mpf("0")
            model_ok = actual_lift == ideal
        else:
            model_radius = p44_ulp_radius(float(actual), 1)
            model_ok = abs(actual_lift.real - ideal.real) <= model_radius
        result = P44NodeValue(
            actual=actual,
            ideal=ideal,
            coefficient_semantics=ideal,
            model_radius=model_radius,
            observed_radius=abs(actual_lift - ideal),
            model_ok=bool(model_ok),
        )
        stream.add(
            p44_trace_event(
                path=path,
                operation_name="integer_literal" if isinstance(actual, int) else "float_literal",
                children=(),
                result=result,
                local_exact=ideal,
                local_model_components=(model_radius, mp.mpf("0")),
                local_model_ok=bool(model_ok),
            )
        )
        return result
    if isinstance(node, ast.Name):
        if node.id in state_names:
            actual = environment[node.id]
            exact = mp_complex_from_binary64(complex(actual))
            operation_name = "state_name"
            radius = mp.mpf("0")
            ok = True
        elif node.id == "pi":
            actual = environment["pi"]
            exact = mp.mpc(mp.pi, 0)
            operation_name = "numpy_pi"
            radius = p44_ulp_radius(float(actual), 1)
            ok = abs(mp_complex_from_binary64(complex(actual)) - exact) <= radius
        else:
            raise InvalidRun(f"generated callable read undeclared scalar name: {node.id}")
        result = P44NodeValue(
            actual=actual,
            ideal=exact,
            coefficient_semantics=exact,
            model_radius=radius,
            observed_radius=abs(mp_complex_from_binary64(complex(actual)) - exact),
            model_ok=bool(ok),
        )
        stream.add(
            p44_trace_event(
                path=path,
                operation_name=operation_name,
                children=(),
                result=result,
                local_exact=exact,
                local_model_components=(radius, mp.mpf("0")),
                local_model_ok=bool(ok),
            )
        )
        return result
    operation_name = p44_ast_operation(node)
    child_nodes: list[ast.AST]
    if isinstance(node, ast.BinOp):
        child_nodes = [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        child_nodes = [node.operand]
    elif isinstance(node, ast.Call):
        if node.keywords or len(node.args) != 1:
            raise InvalidRun("generated scalar call signature drift")
        child_nodes = [node.args[0]]
    else:
        raise InvalidRun("unreachable generated scalar AST shape")
    children = [
        p44_evaluate_ast_node(
            child,
            source=source,
            environment=environment,
            state_names=state_names,
            constant_by_node=constant_by_node,
            path=f"{path}/{index}",
            stream=stream,
            allow_constant_reuse=allow_constant_reuse,
        )
        for index, child in enumerate(child_nodes)
    ]
    try:
        actual = p44_actual_scalar_operation(
            operation_name, [child.actual for child in children]
        )
        local_exact = p44_exact_scalar_operation(
            operation_name,
            [mp_complex_from_binary64(complex(child.actual)) for child in children],
        )
        ideal = p44_exact_scalar_operation(
            operation_name, [child.ideal for child in children]
        )
        coefficient_semantics = p44_exact_scalar_operation(
            operation_name, [child.coefficient_semantics for child in children]
        )
        model_radius, _local_radius, local_ok, local_components = (
            p44_local_and_propagated_radii(
                operation_name, actual, children, local_exact, observed=False
            )
        )
        observed_radius, _observed_local, _ignored, _ignored_components = (
            p44_local_and_propagated_radii(
                operation_name, actual, children, local_exact, observed=True
            )
        )
    except Exception as exc:
        failure_event = {
            "node_path": path,
            "operation": operation_name,
            "operand_identities": [
                p44_scalar_identity(child.actual) for child in children
            ],
            "output_identity": None,
            "exact_120dps_counterpart": None,
            "coefficient_semantics_120dps": None,
            "local_exact_lifted_operand_result": None,
            "local_residual": None,
            "local_model_component_radii": None,
            "model_radius": None,
            "observed_radius": None,
            "local_model_utilization": None,
            "component_ulp_distances": None,
            "model_exceeding": True,
            "terminal_status": "EVALUATION_FAILED",
            "error_type": type(exc).__name__,
            "error_message": str(exc)[:2048],
        }
        stream.add(failure_event)
        raise SlotEvaluationError(
            f"AST node evaluation failed at {path}: {type(exc).__name__}: {exc}",
            payload={"trace_event": failure_event},
        ) from exc
    model_ok = bool(all(child.model_ok for child in children) and local_ok)
    result = P44NodeValue(
        actual=actual,
        ideal=ideal,
        coefficient_semantics=coefficient_semantics,
        model_radius=model_radius,
        observed_radius=observed_radius,
        model_ok=model_ok,
    )
    stream.add(
        p44_trace_event(
            path=path,
            operation_name=operation_name,
            children=children,
            result=result,
            local_exact=local_exact,
            local_model_components=local_components,
            local_model_ok=local_ok,
        )
    )
    return result


@dataclass(frozen=True)
class P44TraceFanout:
    streams: tuple[P44TraceStream, ...]

    def add(self, event: Mapping[str, Any]) -> bytes:
        framed = b""
        for stream in self.streams:
            framed = stream.add(event)
        return framed


def p44_ast_depends_on_state(node: ast.AST, state_names: frozenset[str]) -> bool:
    return any(
        isinstance(child, ast.Name) and child.id in state_names
        for child in ast.walk(node)
    )


def p44_constant_occurrences(
    entries: Sequence[Sequence[ast.AST]], state_names: frozenset[str]
) -> list[tuple[ast.AST, str]]:
    output: list[tuple[ast.AST, str]] = []

    def visit(node: ast.AST, path: str, parent_depends: bool) -> None:
        depends = p44_ast_depends_on_state(node, state_names)
        if not depends and parent_depends and isinstance(
            node, (ast.Constant, ast.Name, ast.BinOp, ast.UnaryOp, ast.Call)
        ):
            output.append((node, path))
            return
        scalar_children: list[ast.AST] = []
        if isinstance(node, ast.BinOp):
            scalar_children = [node.left, node.right]
        elif isinstance(node, ast.UnaryOp):
            scalar_children = [node.operand]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("exp", "sqrt"):
                scalar_children = list(node.args)
        for index, child in enumerate(scalar_children):
            visit(child, f"{path}/{index}", depends)

    for row, row_entries in enumerate(entries):
        for column, entry in enumerate(row_entries):
            if p44_ast_depends_on_state(entry, state_names):
                visit(entry, f"entry={row},{column}", True)
            else:
                output.append((entry, f"entry={row},{column}"))
    return output


def p44_validate_callable_globals(function: Callable[..., Any]) -> dict[str, Any]:
    globals_map = function.__globals__
    required = {"array", "exp", "pi", "sqrt"}
    missing = required - globals_map.keys()
    if missing:
        raise InvalidRun(f"generated callable global missing: {sorted(missing)}")
    identities = {
        "array_is_numpy_array": globals_map["array"] is np.array,
        "exp_is_numpy_exp": globals_map["exp"] is np.exp,
        "sqrt_is_numpy_sqrt": globals_map["sqrt"] is np.sqrt,
        "pi_hex": float(globals_map["pi"]).hex(),
        "pi_ratio": list(float(globals_map["pi"]).as_integer_ratio()),
        "numpy_pi_hex": float(np.pi).hex(),
        "numpy_pi_ratio": list(float(np.pi).as_integer_ratio()),
    }
    if not (
        identities["array_is_numpy_array"]
        and identities["exp_is_numpy_exp"]
        and identities["sqrt_is_numpy_sqrt"]
        and identities["pi_hex"] == identities["numpy_pi_hex"]
        and identities["pi_ratio"] == identities["numpy_pi_ratio"]
    ):
        raise InvalidRun("generated callable NumPy global identity drift")
    return identities


def p44_exact50_literal_mapping(
    entries: Sequence[Sequence[ast.AST]],
    source: str,
    source_hessian: sp.Matrix,
) -> dict[str, Any]:
    if source_hessian.shape != (7, 7):
        raise InvalidRun("exact50 source Hessian shape drift")

    def rational_key(text: str) -> tuple[int, int]:
        rational = sp.Rational(text)
        return int(rational.p), int(rational.q)

    def ast_float_records(node: ast.AST, path: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []

        def visit(child: ast.AST, child_path: str) -> None:
            if (
                isinstance(child, ast.Constant)
                and not isinstance(child.value, bool)
                and isinstance(child.value, float)
            ):
                segment = ast.get_source_segment(source, child)
                if not isinstance(segment, str):
                    raise InvalidRun("exact50 AST literal lexeme unavailable")
                numerator, denominator = rational_key(segment)
                records.append(
                    {
                        "path": child_path,
                        "lexeme": segment,
                        "absolute_rational": [abs(numerator), denominator],
                    }
                )
            for field_name, value in ast.iter_fields(child):
                if isinstance(value, ast.AST):
                    visit(value, f"{child_path}/{field_name}")
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, ast.AST):
                            visit(item, f"{child_path}/{field_name}[{index}]")

        visit(node, path)
        return records

    def source_float_records(expr: sp.Expr, path: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []

        def visit(child: sp.Basic, child_path: str) -> None:
            if isinstance(child, sp.Float):
                text = str(abs(child))
                numerator, denominator = rational_key(text)
                records.append(
                    {
                        "path": child_path,
                        "decimal": str(child),
                        "absolute_rational": [abs(numerator), denominator],
                    }
                )
            for index, item in enumerate(child.args):
                visit(item, f"{child_path}/args[{index}]")

        visit(expr, path)
        return records

    per_entry: list[list[dict[str, Any]]] = []
    all_pair_records: list[dict[str, Any]] = []
    total_ast = 0
    total_source = 0
    for row in range(7):
        entry_row: list[dict[str, Any]] = []
        for column in range(7):
            ast_records = ast_float_records(
                entries[row][column], f"entry={row},{column}"
            )
            source_records = source_float_records(
                source_hessian[row, column], f"hessian={row},{column}"
            )
            ast_by_value: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
            source_by_value: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
            for record in ast_records:
                ast_by_value[tuple(record["absolute_rational"])].append(record)
            for record in source_records:
                source_by_value[tuple(record["absolute_rational"])].append(record)
            ast_multiset = Counter(
                tuple(record["absolute_rational"]) for record in ast_records
            )
            source_multiset = Counter(
                tuple(record["absolute_rational"]) for record in source_records
            )
            if ast_multiset != source_multiset:
                raise InvalidRun(
                    "generated AST literal/exact50 source multiset drift at "
                    f"{row},{column}"
                )
            entry_pairs: list[dict[str, Any]] = []
            for key in sorted(ast_by_value):
                ast_group = ast_by_value[key]
                source_group = source_by_value[key]
                for occurrence, (ast_record, source_record) in enumerate(
                    zip(ast_group, source_group, strict=True)
                ):
                    pair = {
                        "entry": [row, column],
                        "absolute_rational": [key[0], key[1]],
                        "equal_value_occurrence": occurrence,
                        "AST_path": ast_record["path"],
                        "AST_lexeme": ast_record["lexeme"],
                        "source_path": source_record["path"],
                        "source_decimal": source_record["decimal"],
                    }
                    entry_pairs.append(pair)
                    all_pair_records.append(pair)
            entry_row.append(
                {
                    "entry": [row, column],
                    "AST_float_literal_count": len(ast_records),
                    "source_exact50_Float_count": len(source_records),
                    "bijection_count": len(entry_pairs),
                    "bijection_sha256": p44_sequence_commitment(entry_pairs),
                    "equal_value_duplicates_paired_in_traversal_order": True,
                }
            )
            total_ast += len(ast_records)
            total_source += len(source_records)
        per_entry.append(entry_row)
    if total_ast != total_source or total_ast != len(all_pair_records):
        raise InvalidRun("exact50 literal global bijection cardinality drift")
    return {
        "mapping": (
            "Each generated AST float literal is paired one-to-one, within its "
            "Hessian entry and exact absolute decimal value, with a source "
            "SymPy Float from the pinned 50-decimal hessian_expr. Unary signs "
            "and all enclosing operations remain in the pinned AST."
        ),
        "pair_count": len(all_pair_records),
        "pair_commitment_sha256": p44_sequence_commitment(all_pair_records),
        "per_entry": per_entry,
        "all_49_entry_multisets_bijective": True,
        "replayable_from_pinned_source_hessian_and_generated_AST": True,
    }


def p44_prepare_callable_plan(
    variant: str,
    function: Callable[..., Any],
    source_hessian: sp.Matrix,
    expected_normalized_sha256: str,
) -> P44CallablePlan:
    source = inspect.getsource(function)
    tree = ast.parse(source)
    observed_types = {type(node).__name__ for node in ast.walk(tree)}
    if observed_types != P44_ALLOWED_AST_NODE_NAMES:
        raise InvalidRun(
            f"generated callable AST whitelist drift for {variant}: "
            f"observed={sorted(observed_types)}"
        )
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise InvalidRun(f"generated callable function structure drift: {variant}")
    function_node = tree.body[0]
    if len(function_node.args.args) != 1 or function_node.args.vararg is not None:
        raise InvalidRun(f"generated callable argument structure drift: {variant}")
    if len(function_node.body) != 2:
        raise InvalidRun(f"generated callable body length drift: {variant}")
    assign, returned = function_node.body
    if not isinstance(assign, ast.Assign) or not isinstance(returned, ast.Return):
        raise InvalidRun(f"generated callable assign/return structure drift: {variant}")
    if len(assign.targets) != 1 or not isinstance(assign.targets[0], ast.List):
        raise InvalidRun(f"generated callable tuple-unpack target drift: {variant}")
    argument_name = function_node.args.args[0].arg
    if not isinstance(assign.value, ast.Name) or assign.value.id != argument_name:
        raise InvalidRun(f"generated callable tuple-unpack source drift: {variant}")
    state_nodes = assign.targets[0].elts
    if len(state_nodes) != 7 or not all(isinstance(node, ast.Name) for node in state_nodes):
        raise InvalidRun(f"generated callable state arity drift: {variant}")
    state_names = tuple(node.id for node in state_nodes if isinstance(node, ast.Name))
    return_value = returned.value
    if not (
        isinstance(return_value, ast.Call)
        and isinstance(return_value.func, ast.Name)
        and return_value.func.id == "array"
        and len(return_value.args) == 1
        and not return_value.keywords
        and isinstance(return_value.args[0], ast.List)
    ):
        raise InvalidRun(f"generated callable array return drift: {variant}")
    row_nodes = return_value.args[0].elts
    if len(row_nodes) != 7 or not all(isinstance(row, ast.List) for row in row_nodes):
        raise InvalidRun(f"generated callable Hessian row structure drift: {variant}")
    entries = tuple(
        tuple(row.elts) for row in row_nodes if isinstance(row, ast.List)
    )
    if any(len(row) != 7 for row in entries):
        raise InvalidRun(f"generated callable Hessian column structure drift: {variant}")
    scalar_calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    if scalar_calls != {"array", "exp", "sqrt"}:
        raise InvalidRun(f"generated callable call-name drift: {variant}")
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "sqrt"
            and p44_ast_depends_on_state(node, frozenset(state_names))
        ):
            raise InvalidRun(
                f"state-dependent sqrt is undeclared by Phase44: {variant}"
            )
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            exponent = node.right
            if (
                not isinstance(exponent, ast.Constant)
                or isinstance(exponent.value, bool)
                or not isinstance(exponent.value, int)
                or exponent.value < 0
            ):
                raise InvalidRun(
                    "generated callable power exponent is not a fixed "
                    f"nonnegative integer: {variant}"
                )
    normalized = sha256_bytes(p44_alpha_normalized_ast_dump(tree).encode("utf-8"))
    if normalized != expected_normalized_sha256:
        raise InvalidRun(
            f"generated callable normalized AST SHA drift for {variant}: {normalized}"
        )
    fingerprint = p44_callable_fingerprint(function)
    globals_identity = p44_validate_callable_globals(function)
    exact50_literal_mapping = p44_exact50_literal_mapping(
        entries, source, source_hessian
    )
    state_set = frozenset(state_names)
    occurrences = p44_constant_occurrences(entries, state_set)
    grouped: dict[str, list[tuple[ast.AST, str]]] = {}
    for node, path in occurrences:
        normalized_subtree = ast.dump(
            node, annotate_fields=True, include_attributes=False
        )
        source_lexeme = ast.get_source_segment(source, node)
        if not isinstance(source_lexeme, str):
            raise InvalidRun("constant subtree source lexeme unavailable")
        digest = sha256_bytes(
            canonical_json_bytes(
                {"ast_dump": normalized_subtree, "source_lexeme": source_lexeme}
            )
        )
        grouped.setdefault(digest, []).append((node, path))
    return P44CallablePlan(
        variant=variant,
        function=function,
        source=source,
        tree=tree,
        function_node=function_node,
        argument_name=argument_name,
        state_names=state_names,
        entries=entries,
        normalized_ast_sha256=normalized,
        fingerprint={
            **fingerprint,
            "numpy_global_identities": globals_identity,
            "exact50_literal_mapping": exact50_literal_mapping,
        },
        exact50_literal_mapping=exact50_literal_mapping,
        constant_occurrences={
            digest: tuple(grouped[digest]) for digest in sorted(grouped)
        },
        constant_node_ids=frozenset(
            id(node) for representatives in grouped.values() for node, _path in representatives
        ),
        constant_by_node={},
        constant_records={},
        constant_model_ok=False,
    )


def p44_evaluate_plan_constants(plan: P44CallablePlan) -> P44CallablePlan:
    if plan.constant_by_node or plan.constant_records:
        raise InvalidRun(f"constant boundary evaluated twice: {plan.variant}")
    state_set = frozenset(plan.state_names)
    constant_by_node: dict[int, P44NodeValue] = {}
    constant_records: dict[str, Any] = {}
    for digest in sorted(plan.constant_occurrences):
        representatives = plan.constant_occurrences[digest]
        representative, first_path = representatives[0]
        stream = P44TraceStream()
        try:
            value = p44_evaluate_ast_node(
                representative,
                source=plan.source,
                environment={"pi": plan.function.__globals__["pi"]},
                state_names=state_set,
                constant_by_node={},
                path=f"constant={digest}",
                stream=stream,
                allow_constant_reuse=False,
            )
        except SlotEvaluationError as exc:
            raise SlotEvaluationError(
                (
                    "constant-subtree replay failed for "
                    f"{plan.variant}/{digest}: {exc}"
                ),
                payload={
                    "failure_scope": "constant_subtree_replay",
                    "variant": plan.variant,
                    "failed_digest": digest,
                    "failed_occurrence_paths": [
                        path for _node, path in representatives
                    ],
                    "completed_constant_records": constant_records,
                    "completed_constant_digests_in_fixed_order": list(
                        constant_records
                    ),
                    "failed_trace": stream.finish(),
                    "smallest_exception_payload": exc.payload,
                },
            ) from exc
        boundary_value = dataclasses.replace(
            value,
            coefficient_semantics=mp_complex_from_binary64(complex(value.actual)),
        )
        for occurrence, _path in representatives:
            constant_by_node[id(occurrence)] = boundary_value
        constant_records[digest] = {
            "normalized_subtree_sha256": digest,
            "ast_dump": ast.dump(
                representative, annotate_fields=True, include_attributes=False
            ),
            "source_lexeme": ast.get_source_segment(plan.source, representative),
            "occurrence_count": len(representatives),
            "occurrence_paths": [path for _node, path in representatives],
            "representative_path": first_path,
            "output_identity": p44_scalar_identity(boundary_value.actual),
            "ideal_120dps": mp_complex_payload(boundary_value.ideal, AUTHORITATIVE_DPS),
            "exact_lifted_output_120dps": mp_complex_payload(
                boundary_value.coefficient_semantics, AUTHORITATIVE_DPS
            ),
            "model_radius": mp_number_string(
                boundary_value.model_radius, AUTHORITATIVE_DPS
            ),
            "observed_radius": mp_number_string(
                boundary_value.observed_radius, AUTHORITATIVE_DPS
            ),
            "model_ok": boundary_value.model_ok,
            "ideal_is_exact50_source_semantics": True,
            "exact50_literal_mapping_commitment_sha256": (
                plan.exact50_literal_mapping["pair_commitment_sha256"]
            ),
            "trace": stream.finish(),
        }
    return dataclasses.replace(
        plan,
        constant_by_node=constant_by_node,
        constant_records=constant_records,
        constant_model_ok=all(
            value["model_ok"] is True
            and value["trace"]["subnormal_model_ambiguity"] is False
            for value in constant_records.values()
        ),
    )


def p44_prepare_callable_plans(
    context: P44Context, manifest: Mapping[str, Any]
) -> dict[str, P44CallablePlan]:
    expected = manifest["known_prior_results_and_audit_disclosure"][
        "phase44_precommit_generated_callable_structural_audit"
    ]["normalized_AST_sha256"]
    plans = {
        point: p44_prepare_callable_plan(
            point,
            context.points[point].model.hessian_function,
            context.points[point].model.hessian_expr,
            str(expected[point]),
        )
        for point in TARGETS
    }
    if tuple(plans) != TARGETS:
        raise InvalidRun("generated callable plan order drift")
    return plans


def p44_evaluate_callable_plan(
    plan: P44CallablePlan,
    w64: np.ndarray,
    source_h64: np.ndarray,
    coefficient_reference_hessian: mp.matrix,
) -> tuple[mp.matrix, list[list[mp.mpf]], list[list[mp.mpf]], dict[str, Any]]:
    state_values = np.asarray(w64, dtype=np.complex128).reshape(7)
    environment: dict[str, Any] = {
        name: state_values[index] for index, name in enumerate(plan.state_names)
    }
    environment["pi"] = plan.function.__globals__["pi"]
    whole_stream = P44TraceStream()
    entry_streams: list[list[P44TraceStream]] = [
        [P44TraceStream() for _column in range(7)] for _row in range(7)
    ]
    state_node_values = [
        P44NodeValue(
            actual=state_values[index],
            ideal=mp_complex_from_binary64(complex(state_values[index])),
            coefficient_semantics=mp_complex_from_binary64(
                complex(state_values[index])
            ),
            model_radius=mp.mpf("0"),
            observed_radius=mp.mpf("0"),
            model_ok=True,
        )
        for index in range(7)
    ]
    whole_stream.add(
        p44_structural_trace_event(
            path="assign/tuple_unpack",
            operation_name="tuple_unpack_assign",
            values=state_node_values,
            operand_identities=[
                p44_scalar_identity(state_values[index]) for index in range(7)
            ],
            output_identity={
                "python_type": "tuple_unpack_bindings",
                "bindings_in_fixed_order": list(plan.state_names),
            },
        )
    )
    node_values: list[list[P44NodeValue]] = []
    nested_actual: list[list[Any]] = []
    scalar_constant_by_node = {
        node_id: dataclasses.replace(
            value,
            ideal=value.coefficient_semantics,
            model_radius=mp.mpf("0"),
            observed_radius=mp.mpf("0"),
            model_ok=True,
        )
        for node_id, value in plan.constant_by_node.items()
    }
    trace_failures: list[dict[str, Any]] = []
    entry_path_commitment_matches: list[bool] = []
    entry_terminal_successes: list[bool] = []
    for row in range(7):
        value_row: list[P44NodeValue] = []
        actual_row: list[Any] = []
        for column in range(7):
            fanout = P44TraceFanout((whole_stream, entry_streams[row][column]))
            entry_path = f"entry={row},{column}"
            expected_path_operations = p44_trace_node_path_operations(
                plan.entries[row][column], plan, entry_path
            )
            entry_failed = False
            try:
                value = p44_evaluate_ast_node(
                    plan.entries[row][column],
                    source=plan.source,
                    environment=environment,
                    state_names=frozenset(plan.state_names),
                    constant_by_node=scalar_constant_by_node,
                    path=entry_path,
                    stream=fanout,  # type: ignore[arg-type]
                    allow_constant_reuse=True,
                )
            except SlotEvaluationError as exc:
                entry_failed = True
                observed_path_operations = entry_streams[row][
                    column
                ].path_operation_records
                if observed_path_operations != expected_path_operations[
                    : len(observed_path_operations)
                ]:
                    raise SlotEvaluationError(
                        f"failed trace prefix is not preenumerated: {entry_path}",
                        payload={
                            "failure_scope": "AST_trace_path_commitment",
                            "entry": [row, column],
                            "expected_path_operations": expected_path_operations,
                            "observed_path_operations": observed_path_operations,
                            "completed_whole_trace": whole_stream.finish(),
                            "completed_entry_trace": entry_streams[row][
                                column
                            ].finish(),
                            "completed_per_Hessian_entry_traces": [
                                [
                                    (
                                        entry_streams[seen_row][
                                            seen_column
                                        ].finish()
                                        if entry_streams[seen_row][
                                            seen_column
                                        ].event_count
                                        else None
                                    )
                                    for seen_column in range(7)
                                ]
                                for seen_row in range(7)
                            ],
                            "smallest_exception_payload": exc.payload,
                        },
                    ) from exc
                failure_record = {
                    "entry": [row, column],
                    "error_type": type(exc).__name__,
                    "error_message": str(exc)[:2048],
                    "smallest_node_payload": exc.payload,
                    "completed_event_count": len(observed_path_operations),
                    "terminalized_dependency_count": len(expected_path_operations)
                    - len(observed_path_operations),
                }
                trace_failures.append(failure_record)
                for pending in expected_path_operations[len(observed_path_operations) :]:
                    fanout.add(
                        {
                            "node_path": pending["node_path"],
                            "operation": pending["operation"],
                            "operand_identities": None,
                            "output_identity": None,
                            "exact_120dps_counterpart": None,
                            "coefficient_semantics_120dps": None,
                            "local_exact_lifted_operand_result": None,
                            "local_residual": None,
                            "local_model_component_radii": None,
                            "model_radius": None,
                            "observed_radius": None,
                            "local_model_utilization": None,
                            "component_ulp_distances": None,
                            "model_exceeding": True,
                            "terminal_status": "NOT_RUN_UPSTREAM_INVALID",
                            "dependency_error": str(exc)[:2048],
                        }
                    )
                actual_fallback = np.complex128(source_h64[row, column])
                coefficient_reference = mp.mpc(
                    coefficient_reference_hessian[row, column]
                )
                value = P44NodeValue(
                    actual=actual_fallback,
                    ideal=coefficient_reference,
                    coefficient_semantics=coefficient_reference,
                    model_radius=mp.mpf("0"),
                    observed_radius=abs(
                        mp_complex_from_binary64(complex(actual_fallback))
                        - coefficient_reference
                    ),
                    model_ok=False,
                )
            observed_complete_path_operations = entry_streams[row][
                column
            ].path_operation_records
            if observed_complete_path_operations != expected_path_operations:
                raise SlotEvaluationError(
                    f"trace path-operation completion drift: {entry_path}",
                    payload={
                        "failure_scope": "AST_trace_path_commitment",
                        "entry": [row, column],
                        "expected_path_operations": expected_path_operations,
                        "observed_path_operations": (
                            observed_complete_path_operations
                        ),
                        "completed_whole_trace": whole_stream.finish(),
                        "completed_entry_trace": entry_streams[row][
                            column
                        ].finish(),
                        "completed_per_Hessian_entry_traces": [
                            [
                                (
                                    entry_streams[seen_row][seen_column].finish()
                                    if entry_streams[seen_row][
                                        seen_column
                                    ].event_count
                                    else None
                                )
                                for seen_column in range(7)
                            ]
                            for seen_row in range(7)
                        ],
                    },
                )
            entry_path_commitment_matches.append(True)
            entry_terminal_successes.append(
                not entry_failed
                and entry_streams[row][column].status_histogram
                == {"SUCCESS": len(expected_path_operations)}
            )
            value_row.append(value)
            actual_row.append(value.actual)
        node_values.append(value_row)
        nested_actual.append(actual_row)
        whole_stream.add(
            p44_structural_trace_event(
                path=f"return/list_row[{row}]",
                operation_name="list_constructor",
                values=value_row,
                operand_identities=[
                    p44_scalar_identity(value.actual) for value in value_row
                ],
                output_identity={"python_type": "builtins.list", "length": 7},
            )
        )
    whole_stream.add(
        p44_structural_trace_event(
            path="return/list_outer",
            operation_name="list_constructor",
            values=node_values,
            operand_identities=[
                {"python_type": "builtins.list", "length": 7} for _row in range(7)
            ],
            output_identity={"python_type": "builtins.list", "length": 7},
        )
    )
    with np.errstate(all="raise"):
        interpreted = np.asarray(np.array(nested_actual), dtype=np.complex128).reshape(7, 7)
    dtype, raw = canonical_array_bytes(interpreted)
    source_dtype, source_raw = canonical_array_bytes(source_h64)
    completed_raw_matches_source = dtype == source_dtype and raw == source_raw
    array_event = p44_structural_trace_event(
        path="return/array",
        operation_name="array_constructor",
        values=node_values,
        operand_identities=[
            p44_scalar_identity(node_values[row][column].actual)
            for row in range(7)
            for column in range(7)
        ],
        output_identity=binary64_payload(interpreted),
    )
    array_event["model_exceeding"] = bool(trace_failures)
    whole_stream.add(array_event)
    if not completed_raw_matches_source:
        raise SlotEvaluationError(
            f"AST interpreter failed H64 raw reproduction: {plan.variant}",
            payload={
                "failure_scope": "AST_H64_raw_identity",
                "variant": plan.variant,
                "completed_whole_trace": whole_stream.finish(),
                "completed_per_Hessian_entry_traces": [
                    [entry_streams[row][column].finish() for column in range(7)]
                    for row in range(7)
                ],
                "interpreter_H64_identity": binary64_payload(interpreted),
                "source_H64_identity": binary64_payload(source_h64),
                "raw_bitwise_reproduction": False,
            },
        )
    coefficient_hessian = mp.matrix(
        [
            [node_values[row][column].coefficient_semantics for column in range(7)]
            for row in range(7)
        ]
    )
    model_radii = [
        [node_values[row][column].model_radius for column in range(7)]
        for row in range(7)
    ]
    observed_radii = [
        [node_values[row][column].observed_radius for column in range(7)]
        for row in range(7)
    ]
    per_entry: list[list[Any]] = []
    for row in range(7):
        summary_row: list[Any] = []
        for column in range(7):
            value = node_values[row][column]
            actual_lift = mp_complex_from_binary64(complex(interpreted[row, column]))
            observed_hessian_error = abs(
                actual_lift - value.coefficient_semantics
            )
            observed_hessian_contained = bool(
                observed_hessian_error <= value.observed_radius
            )
            summary_row.append(
                {
                    "entry": [row, column],
                    "trace": entry_streams[row][column].finish(),
                    "output_identity": p44_scalar_identity(interpreted[row, column]),
                    "coefficient_semantics_120dps": mp_complex_payload(
                        value.coefficient_semantics, AUTHORITATIVE_DPS
                    ),
                    "ideal_120dps": mp_complex_payload(value.ideal, AUTHORITATIVE_DPS),
                    "actual_minus_coefficient_semantics": mp_complex_payload(
                        actual_lift - value.coefficient_semantics,
                        AUTHORITATIVE_DPS,
                    ),
                    "model_radius": mp_number_string(
                        value.model_radius, AUTHORITATIVE_DPS
                    ),
                    "observed_radius": mp_number_string(
                        value.observed_radius, AUTHORITATIVE_DPS
                    ),
                    "observed_H64_error_magnitude": mp_number_string(
                        observed_hessian_error, AUTHORITATIVE_DPS
                    ),
                    "observed_H64_error_utilization": mp_number_string(
                        observed_hessian_error
                        / max(value.observed_radius, mp.mpf("1e-100")),
                        AUTHORITATIVE_DPS,
                    ),
                    "observed_H64_error_contained": (
                        observed_hessian_contained
                    ),
                    "model_ok": value.model_ok,
                }
            )
        per_entry.append(summary_row)
    trace = whole_stream.finish()
    expected_trace_shape = p44_plan_trace_shape(plan)
    path_operation_commitment_matches = bool(
        trace["event_count"] == expected_trace_shape["whole_event_count"]
        and trace["path_operation_commitment_sha256"]
        == expected_trace_shape["path_operation_commitment_sha256"]
        and all(entry_path_commitment_matches)
    )
    if not path_operation_commitment_matches:
        raise SlotEvaluationError(
            f"AST whole-trace path-operation drift: {plan.variant}",
            payload={
                "failure_scope": "AST_trace_path_commitment",
                "variant": plan.variant,
                "completed_whole_trace": trace,
                "completed_per_Hessian_entry_summaries": per_entry,
                "expected_trace_shape": expected_trace_shape,
                "interpreter_H64_identity": binary64_payload(interpreted),
                "source_H64_identity": binary64_payload(source_h64),
            },
        )
    all_events_terminal_success = bool(
        trace["terminal_status_histogram"] == {"SUCCESS": trace["event_count"]}
        and all(entry_terminal_successes)
    )
    raw_bitwise_reproduction = bool(
        completed_raw_matches_source and not trace_failures
    )
    all_observed_hessian_errors_contained = all(
        entry["observed_H64_error_contained"]
        for row in per_entry
        for entry in row
    )
    trace.update(
        {
            "variant": plan.variant,
            "normalized_AST_sha256": plan.normalized_ast_sha256,
            "interpreter_H64_identity": binary64_payload(interpreted),
            "source_H64_identity": binary64_payload(source_h64),
            "raw_bitwise_reproduction": raw_bitwise_reproduction,
            "completed_H64_identity_with_source_fallback_for_failed_entries": bool(
                trace_failures
            ),
            "typed_trace_failures": trace_failures,
            "trace_failure_count": len(trace_failures),
            "trace_arithmetic_inconclusive": bool(trace_failures),
            "all_events_terminal_SUCCESS": all_events_terminal_success,
            "all_path_operation_commitments_complete": (
                path_operation_commitment_matches
            ),
            "exact_trace_complete": bool(
                raw_bitwise_reproduction
                and not trace_failures
                and all_events_terminal_success
                and path_operation_commitment_matches
            ),
            "all_entry_models_ok": all(
                value.model_ok for row in node_values for value in row
            ),
            "all_observed_H64_errors_contained": (
                all_observed_hessian_errors_contained
            ),
            "per_Hessian_entry": per_entry,
        }
    )
    if trace_failures:
        raise SlotEvaluationError(
            f"AST interpreter trace incomplete for {plan.variant}",
            payload={
                "failure_scope": "AST_trace_arithmetic",
                "variant": plan.variant,
                "completed_whole_and_per_entry_trace": trace,
                "interpreter_H64_identity_with_retention_fallback": (
                    binary64_payload(interpreted)
                ),
                "source_H64_identity": binary64_payload(source_h64),
                "raw_bitwise_reproduction": False,
                "typed_trace_failures": trace_failures,
            },
        )
    if not all_observed_hessian_errors_contained:
        raise SlotEvaluationError(
            f"observed AST residual envelope failed for {plan.variant}",
            payload={
                "failure_scope": "AST_observed_residual_accounting",
                "variant": plan.variant,
                "completed_whole_and_per_entry_trace": trace,
                "all_observed_H64_errors_contained": False,
            },
        )
    return coefficient_hessian, model_radii, observed_radii, trace


def p44_coefficient_node_value(
    node: ast.AST,
    *,
    plan: P44CallablePlan,
    state_values: Mapping[str, mp.mpc],
    constant_mode: str,
) -> mp.mpc:
    cached = plan.constant_by_node.get(id(node))
    if cached is not None:
        if constant_mode == "binary64_exact_lift":
            return mp.mpc(cached.coefficient_semantics)
        if constant_mode == "source_exact50":
            return mp.mpc(cached.ideal)
        raise InvalidRun(f"undeclared constant semantics mode: {constant_mode}")
    if isinstance(node, ast.Constant):
        segment = ast.get_source_segment(plan.source, node)
        if not isinstance(segment, str):
            raise InvalidRun("coefficient evaluator literal lexeme unavailable")
        return mp.mpc(mp.mpf(segment), 0)
    if isinstance(node, ast.Name):
        if node.id in state_values:
            return mp.mpc(state_values[node.id])
        if node.id == "pi":
            return mp.mpc(mp.pi, 0)
        raise InvalidRun(f"coefficient evaluator undeclared name: {node.id}")
    operation_name = p44_ast_operation(node)
    if isinstance(node, ast.BinOp):
        children = [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        children = [node.operand]
    elif isinstance(node, ast.Call):
        children = list(node.args)
    else:
        raise InvalidRun("coefficient evaluator structural drift")
    return p44_exact_scalar_operation(
        operation_name,
        [
            p44_coefficient_node_value(
                child,
                plan=plan,
                state_values=state_values,
                constant_mode=constant_mode,
            )
            for child in children
        ],
    )


def p44_coefficient_hessian(
    plan: P44CallablePlan,
    w: Sequence[Any],
    *,
    constant_mode: str = "binary64_exact_lift",
) -> mp.matrix:
    state_values = {
        name: mp.mpc(w[index]) for index, name in enumerate(plan.state_names)
    }
    return mp.matrix(
        [
            [
                p44_coefficient_node_value(
                    plan.entries[row][column],
                    plan=plan,
                    state_values=state_values,
                    constant_mode=constant_mode,
                )
                for column in range(7)
            ]
            for row in range(7)
        ]
    )


def p44_disk_propagation(
    operation_name: str,
    centers: Sequence[mp.mpc],
    radii: Sequence[mp.mpf],
) -> tuple[mp.mpc, mp.mpf, bool]:
    if operation_name == "divide" and abs(centers[1]) <= radii[1]:
        # A disk that contains zero has no declared reciprocal model.  Test this
        # before forming the center quotient so that the b == 0 contingency is a
        # finite, typed model failure instead of an uncaught ZeroDivisionError.
        center = (
            mp.mpc("0")
            if centers[1] == 0
            else p44_exact_scalar_operation(operation_name, centers)
        )
        return center, mp.mpf("0"), False
    center = p44_exact_scalar_operation(operation_name, centers)
    if operation_name in ("unary_plus", "unary_minus"):
        return center, radii[0], True
    if operation_name in ("add", "subtract"):
        return center, radii[0] + radii[1], True
    if operation_name == "multiply":
        radius = (
            abs(centers[0]) * radii[1]
            + abs(centers[1]) * radii[0]
            + radii[0] * radii[1]
        )
        return center, radius, True
    if operation_name == "divide":
        radius = (
            radii[0] + abs(centers[0] / centers[1]) * radii[1]
        ) / (abs(centers[1]) - radii[1])
        return center, radius, True
    if operation_name == "power":
        exponent = int(centers[1].real)
        if centers[1].imag != 0 or centers[1].real != exponent or exponent < 0:
            return center, mp.mpf("0"), False
        radius = (abs(centers[0]) + radii[0]) ** exponent - abs(
            centers[0]
        ) ** exponent
        return center, radius, True
    if operation_name == "exp":
        radius = abs(mp.exp(centers[0])) * (mp.exp(radii[0]) - 1)
        return center, radius, True
    if operation_name == "sqrt":
        if centers[0].imag != 0 or centers[0].real <= radii[0]:
            return center, mp.mpf("0"), False
        radius = radii[0] / (
            mp.sqrt(centers[0].real)
            + mp.sqrt(centers[0].real - radii[0])
        )
        return center, radius, True
    raise InvalidRun(f"disk evaluator undeclared operation: {operation_name}")


def p44_coefficient_disk_node(
    node: ast.AST,
    *,
    plan: P44CallablePlan,
    state_values: Mapping[str, mp.mpc],
    state_radii: Mapping[str, mp.mpf],
    include_constant_radii: bool,
) -> tuple[mp.mpc, mp.mpf, bool]:
    cached = plan.constant_by_node.get(id(node))
    if cached is not None:
        return (
            mp.mpc(cached.coefficient_semantics),
            cached.model_radius if include_constant_radii else mp.mpf("0"),
            cached.model_ok if include_constant_radii else True,
        )
    if isinstance(node, ast.Constant):
        segment = ast.get_source_segment(plan.source, node)
        if not isinstance(segment, str):
            raise InvalidRun("disk evaluator literal lexeme unavailable")
        return mp.mpc(mp.mpf(segment), 0), mp.mpf("0"), True
    if isinstance(node, ast.Name):
        if node.id in state_values:
            return (
                mp.mpc(state_values[node.id]),
                mp.mpf(state_radii[node.id]),
                True,
            )
        if node.id == "pi":
            return mp.mpc(mp.pi, 0), mp.mpf("0"), True
        raise InvalidRun(f"disk evaluator undeclared name: {node.id}")
    operation_name = p44_ast_operation(node)
    if isinstance(node, ast.BinOp):
        child_nodes = [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        child_nodes = [node.operand]
    elif isinstance(node, ast.Call):
        child_nodes = list(node.args)
    else:
        raise InvalidRun("disk evaluator structural drift")
    children = [
        p44_coefficient_disk_node(
            child,
            plan=plan,
            state_values=state_values,
            state_radii=state_radii,
            include_constant_radii=include_constant_radii,
        )
        for child in child_nodes
    ]
    center, radius, local_ok = p44_disk_propagation(
        operation_name,
        [child[0] for child in children],
        [child[1] for child in children],
    )
    return center, radius, bool(local_ok and all(child[2] for child in children))


def p44_coefficient_hessian_disk(
    plan: P44CallablePlan,
    w: Sequence[Any],
    w_radii: Sequence[Any],
    *,
    include_constant_radii: bool,
) -> tuple[mp.matrix, list[list[mp.mpf]], bool]:
    state_values = {
        name: mp.mpc(w[index]) for index, name in enumerate(plan.state_names)
    }
    state_radii = {
        name: mp.mpf(w_radii[index]) for index, name in enumerate(plan.state_names)
    }
    centers: list[list[mp.mpc]] = []
    radii: list[list[mp.mpf]] = []
    statuses: list[bool] = []
    for row in range(7):
        center_row: list[mp.mpc] = []
        radius_row: list[mp.mpf] = []
        for column in range(7):
            center, radius, ok = p44_coefficient_disk_node(
                plan.entries[row][column],
                plan=plan,
                state_values=state_values,
                state_radii=state_radii,
                include_constant_radii=include_constant_radii,
            )
            center_row.append(center)
            radius_row.append(radius)
            statuses.append(ok)
        centers.append(center_row)
        radii.append(radius_row)
    return mp.matrix(centers), radii, all(statuses)


def p44_mp_complex_matrix_from_numpy(value: np.ndarray) -> mp.matrix:
    array = np.asarray(value, dtype=np.complex128)
    if array.ndim != 2:
        raise InvalidRun("complex matrix lift requires rank two")
    return mp.matrix(
        [
            [mp_complex_from_binary64(complex(array[row, column])) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def p44_mp_column(value: Sequence[Any]) -> mp.matrix:
    return mp.matrix([[mp.mpc(item)] for item in value])


def p44_matrix_vector(matrix: mp.matrix) -> list[mp.mpc]:
    if matrix.cols != 1:
        raise InvalidRun("expected one-column mpmath matrix")
    return [mp.mpc(matrix[row, 0]) for row in range(matrix.rows)]


def p44_outer_action(y: Sequence[Any]) -> list[mp.mpc]:
    return [mp.mpc(-mp.conj(item)) for item in y]


def p44_exact_hessian_action(
    linear_map: mp.matrix, hessian: mp.matrix, q: Sequence[Any]
) -> tuple[list[mp.mpc], list[mp.mpc]]:
    y_matrix = linear_map.T * hessian * linear_map * p44_mp_column(q)
    y = p44_matrix_vector(y_matrix)
    return y, p44_outer_action(y)


def p44_raw_equal(left: np.ndarray, right: np.ndarray) -> bool:
    left_dtype, left_raw = canonical_array_bytes(left)
    right_dtype, right_raw = canonical_array_bytes(right)
    return left_dtype == right_dtype and left_raw == right_raw


def p44_array_has_subnormal(value: np.ndarray) -> bool:
    array = np.asarray(value)
    real = np.asarray(array.real, dtype=np.float64)
    real_subnormal = np.any(
        (real != 0.0) & (np.abs(real) < np.float64(sys.float_info.min))
    )
    if np.iscomplexobj(array):
        imag = np.asarray(array.imag, dtype=np.float64)
        imag_subnormal = np.any(
            (imag != 0.0) & (np.abs(imag) < np.float64(sys.float_info.min))
        )
    else:
        imag_subnormal = False
    return bool(real_subnormal or imag_subnormal)


def p44_source_operation_shape() -> dict[str, Any]:
    operation_records = [
        {"index": index, "operation": operation}
        for index, operation in enumerate(SOURCE_BOUNDARY_OPERATIONS)
    ]
    failure_node_keys = [
        f"source_operation[{index}]::{operation}"
        for index, operation in enumerate(SOURCE_BOUNDARY_OPERATIONS)
    ]
    return {
        "operation_count": len(operation_records),
        "operations_in_fixed_order": operation_records,
        "operation_commitment_sha256": p44_sequence_commitment(
            operation_records
        ),
        "failure_node_keys_in_fixed_order": failure_node_keys,
        "failure_node_membership_sha256": p44_sequence_commitment(
            [{"failed_node_key": key} for key in failure_node_keys]
        ),
        "applies_identically_to_all_90_slots": True,
    }


def p44_source_boundaries(
    context: P44Context, point: P44PointInput, slot: P44SlotInput
) -> dict[str, Any]:
    linear_map = context.linear_map
    saddle = SimpleNamespace(saddle_w=point.saddle_w)
    fixed = SimpleNamespace(linear_map=linear_map)
    operation_shape = p44_source_operation_shape()
    operation_records = operation_shape["operations_in_fixed_order"]
    membership_digest = operation_shape["operation_commitment_sha256"]
    failure_membership_digest = operation_shape[
        "failure_node_membership_sha256"
    ]
    arrays: dict[str, np.ndarray] = {}
    completed_operations: list[dict[str, Any]] = []

    def capture(
        index: int, name: str, operation: Callable[[], Any]
    ) -> np.ndarray:
        try:
            with np.errstate(all="raise"):
                array = np.asarray(operation(), dtype=np.complex128)
            if not np.all(np.isfinite(array.real)) or not np.all(
                np.isfinite(array.imag)
            ):
                raise InvalidRun(f"nonfinite source boundary: {name}")
        except Exception as exc:
            completed_payload = {
                "retained": {
                    completed_name: binary64_payload(completed_array)
                    for completed_name, completed_array in arrays.items()
                },
                "completed_operations": list(completed_operations),
                "expected_operations_in_fixed_order": operation_records,
                "source_operation_membership_sha256": membership_digest,
                "all_source_boundaries_complete": False,
            }
            raise SlotEvaluationError(
                (
                    "source boundary operation failed at "
                    f"{SOURCE_BOUNDARY_OPERATIONS[index]}: "
                    f"{type(exc).__name__}: {exc}"
                ),
                payload={
                    "failure_scope": "source_boundary_operation",
                    "failed_node_key": (
                        f"source_operation[{index}]::"
                        f"{SOURCE_BOUNDARY_OPERATIONS[index]}"
                    ),
                    "failed_operation_index": index,
                    "failed_operation": SOURCE_BOUNDARY_OPERATIONS[index],
                    "completed_internal_records": list(completed_operations),
                    "completed_source_boundaries": completed_payload,
                    "preenumerated_membership_sha256": membership_digest,
                    "preenumerated_failure_node_membership_sha256": (
                        failure_membership_digest
                    ),
                    "failed_node_is_preenumerated": True,
                    "underlying_error_type": type(exc).__name__,
                    "underlying_error_message": str(exc)[:2048],
                },
            ) from exc
        arrays[name] = array
        completed_operations.append(
            {
                "index": index,
                "operation": SOURCE_BOUNDARY_OPERATIONS[index],
                "boundary_name": name,
                "boundary_identity": binary64_payload(array),
            }
        )
        return array

    u64 = capture(0, "u64", lambda: linear_map @ slot.xi)

    def compute_w64() -> np.ndarray:
        manual_w64 = point.saddle_w + u64
        source_w64 = context.phase41.xi_to_w(saddle, fixed, slot.xi)
        if not p44_raw_equal(manual_w64, source_w64):
            raise InvalidRun(
                "xi_to_w boundary raw drift: "
                f"{slot.point}/{slot.fraction}/{slot.direction}"
            )
        return np.asarray(source_w64)

    w64 = capture(1, "w64", compute_w64)
    h64 = capture(2, "H64", lambda: context.phase41.hessian_at(point.model, w64))
    b1_64 = capture(3, "B1_64", lambda: linear_map.T @ h64)

    def compute_b2_64() -> np.ndarray:
        candidate = b1_64 @ linear_map
        source_hessian_xi = context.phase41.hessian_xi(
            point.model, saddle, fixed, slot.xi
        )
        if not p44_raw_equal(candidate, source_hessian_xi):
            raise InvalidRun(
                "hessian_xi left-association raw drift: "
                f"{slot.point}/{slot.fraction}/{slot.direction}"
            )
        return np.asarray(candidate)

    b2_64 = capture(4, "B2_64", compute_b2_64)
    y64 = capture(5, "y64", lambda: b2_64 @ slot.q)

    def compute_a64() -> np.ndarray:
        candidate = -np.conjugate(y64)
        if not p44_raw_equal(candidate, slot.source):
            raise InvalidRun(
                "stored Phase43 source raw drift: "
                f"{slot.point}/{slot.fraction}/{slot.direction}"
            )
        return np.asarray(candidate)

    a64 = capture(6, "A64", compute_a64)
    return {
        **arrays,
        "subnormal_boundary_names": [
            name for name, array in arrays.items() if p44_array_has_subnormal(array)
        ],
        "retained": {
            name: binary64_payload(array) for name, array in arrays.items()
        },
        "completed_operations": completed_operations,
        "source_operation_membership_sha256": membership_digest,
        "source_paths": {
            "xi_to_w": "phase41.xi_to_w",
            "hessian_at": "phase41.hessian_at",
            "hessian_xi": "phase41.hessian_xi",
            "source_operation_order": list(SOURCE_BOUNDARY_OPERATIONS),
        },
    }


def p44_zero_radii(rows: int, columns: int) -> list[list[mp.mpf]]:
    return [[mp.mpf("0") for _column in range(columns)] for _row in range(rows)]


def p44_mp_matmul_disk(
    left: mp.matrix,
    left_radii: Sequence[Sequence[Any]],
    right: mp.matrix,
    right_radii: Sequence[Sequence[Any]],
    *,
    operation_budget: int | None,
    observed_output: mp.matrix | None,
) -> tuple[mp.matrix, list[list[mp.mpf]], dict[str, Any]]:
    if left.cols != right.rows:
        raise InvalidRun("disk matrix product shape mismatch")
    rows, inner, columns = left.rows, left.cols, right.cols
    exact = left * right
    if operation_budget is None:
        gamma, gamma_ratio = p44_gamma_exact(0)
    else:
        gamma, gamma_ratio = p44_gamma_exact(operation_budget)
    radii: list[list[mp.mpf]] = []
    local_radii: list[list[mp.mpf]] = []
    sum_magnitudes: list[list[mp.mpf]] = []
    residuals: list[list[mp.mpf]] = []
    locally_covered: list[bool] = []
    totally_covered: list[bool] = []
    for row in range(rows):
        radius_row: list[mp.mpf] = []
        local_row: list[mp.mpf] = []
        magnitude_row: list[mp.mpf] = []
        residual_row: list[mp.mpf] = []
        for column in range(columns):
            incoming = mp.fsum(
                abs(left[row, index]) * mp.mpf(right_radii[index][column])
                + abs(right[index, column]) * mp.mpf(left_radii[row][index])
                + mp.mpf(left_radii[row][index])
                * mp.mpf(right_radii[index][column])
                for index in range(inner)
            )
            magnitude_sum = mp.fsum(
                abs(left[row, index]) * abs(right[index, column])
                for index in range(inner)
            )
            local = gamma * magnitude_sum
            total = incoming + local
            if observed_output is None:
                residual = mp.mpf("0")
                locally_covered.append(True)
                totally_covered.append(True)
            else:
                residual = abs(observed_output[row, column] - exact[row, column])
                locally_covered.append(residual <= local)
                totally_covered.append(residual <= total)
            radius_row.append(total)
            local_row.append(local)
            magnitude_row.append(magnitude_sum)
            residual_row.append(residual)
        radii.append(radius_row)
        local_radii.append(local_row)
        sum_magnitudes.append(magnitude_row)
        residuals.append(residual_row)
    payload = {
        "operation_budget": operation_budget,
        "gamma": mp_number_string(gamma, AUTHORITATIVE_DPS),
        "gamma_exact_rational": gamma_ratio,
        "sum_exact_lifted_operand_magnitudes": [
            [mp_number_string(value, AUTHORITATIVE_DPS) for value in row]
            for row in sum_magnitudes
        ],
        "incoming_plus_local_radii": [
            [mp_number_string(value, AUTHORITATIVE_DPS) for value in row]
            for row in radii
        ],
        "local_rounding_radii": [
            [mp_number_string(value, AUTHORITATIVE_DPS) for value in row]
            for row in local_radii
        ],
        "observed_residuals": [
            [mp_number_string(value, AUTHORITATIVE_DPS) for value in row]
            for row in residuals
        ],
        "all_local_rounding_components_covered": all(locally_covered),
        "all_propagated_components_covered": all(totally_covered),
    }
    next_center = exact if observed_output is None else observed_output
    return next_center, radii, payload


def p44_propagate_hessian_radii_to_action(
    linear_map: mp.matrix,
    hessian: mp.matrix,
    hessian_radii: Sequence[Sequence[Any]],
    q: Sequence[Any],
) -> tuple[list[mp.mpc], list[mp.mpf]]:
    zero_l = p44_zero_radii(7, 7)
    zero_q = p44_zero_radii(7, 1)
    first, first_radii, _ = p44_mp_matmul_disk(
        linear_map.T,
        zero_l,
        hessian,
        hessian_radii,
        operation_budget=None,
        observed_output=None,
    )
    second, second_radii, _ = p44_mp_matmul_disk(
        first,
        first_radii,
        linear_map,
        zero_l,
        operation_budget=None,
        observed_output=None,
    )
    y, y_radii, _ = p44_mp_matmul_disk(
        second,
        second_radii,
        p44_mp_column(q),
        zero_q,
        operation_budget=None,
        observed_output=None,
    )
    return p44_outer_action(p44_matrix_vector(y)), [row[0] for row in y_radii]


def p44_median(values: Sequence[mp.mpf]) -> mp.mpf:
    if not values:
        raise InvalidRun("dot-kappa median requires at least one value")
    ordered = sorted(mp.mpf(value) for value in values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2


def p44_dot_kappa_summary(
    records: Sequence[Mapping[str, Any]], *, stage_label: str
) -> dict[str, Any]:
    if not records:
        raise InvalidRun(f"dot-kappa summary is empty: {stage_label}")

    def summarize(values: Sequence[mp.mpf]) -> dict[str, Any]:
        return {
            "count": len(values),
            "maximum": mp_number_string(max(values), AUTHORITATIVE_DPS),
            "median": mp_number_string(p44_median(values), AUTHORITATIVE_DPS),
        }

    grouped: dict[str, list[mp.mpf]] = {}
    all_values: list[mp.mpf] = []
    for record in records:
        path = str(record["path"])
        if "/dot[" not in path:
            raise InvalidRun(f"dot-kappa path lacks fixed dot suffix: {path}")
        stage = path.rsplit("/dot[", 1)[0]
        value = mp.mpf(record["kappa_dot"])
        grouped.setdefault(stage, []).append(value)
        all_values.append(value)
    output = summarize(all_values)
    output.update(
        {
            "stage_label": stage_label,
            "median_policy": "sorted; odd=center, even=mean(two centers)",
            "by_stage": {
                stage: summarize(values) for stage, values in grouped.items()
            },
            "no_cross_algorithm_winner_or_minimum": True,
        }
    )
    return output


def p44_dot_internal_node_names(algorithm: str) -> tuple[str, ...]:
    products = tuple(f"product[{index}]" for index in range(7))
    if algorithm == "explicit_naive":
        return tuple(
            name
            for index in range(7)
            for name in (f"product[{index}]", f"partial[{index}]")
        )
    if algorithm == "fixed_pairwise":
        return products + ("n01", "n23", "n45", "n456", "n0123", "root")
    if algorithm == "componentwise_kahan":
        return tuple(
            name
            for index in range(7)
            for name in (f"product[{index}]", f"kahan[{index}]")
        )
    raise InvalidRun(f"undeclared complex dot algorithm: {algorithm}")


def p44_dot_failure_node_keys(path: str, algorithm: str) -> tuple[str, ...]:
    return tuple(
        [f"{path}/{name}" for name in p44_dot_internal_node_names(algorithm)]
        + [f"{path}/metric"]
    )


def p44_explicit_complex_dot(
    left: Sequence[Any],
    right: Sequence[Any],
    algorithm: str,
    *,
    path: str,
) -> tuple[np.complex128, dict[str, Any]]:
    if len(left) != 7 or len(right) != 7:
        raise InvalidRun("fixed complex dot arity drift")
    expected_names = p44_dot_internal_node_names(algorithm)
    failure_node_keys = p44_dot_failure_node_keys(path, algorithm)
    membership_records = [
        {"failed_node_key": key} for key in failure_node_keys
    ]
    membership_digest = p44_sequence_commitment(membership_records)
    internal: list[dict[str, Any]] = []

    def fail_node(name: str, exc: Exception) -> NoReturn:
        raise SlotEvaluationError(
            (
                f"alternative dot node failed at {path}/{name}: "
                f"{type(exc).__name__}: {exc}"
            ),
            payload={
                "failure_scope": "alternative_internal_node",
                "failed_node_key": f"{path}/{name}",
                "dot_path": path,
                "algorithm": algorithm,
                "completed_internal_records": list(internal),
                "expected_internal_node_names": list(expected_names),
                "expected_failure_node_keys": list(failure_node_keys),
                "preenumerated_membership_sha256": membership_digest,
                "underlying_error_type": type(exc).__name__,
                "underlying_error_message": str(exc)[:2048],
            },
        ) from exc

    products: list[np.complex128] = []

    def product_at(index: int) -> np.complex128:
        name = f"product[{index}]"
        try:
            with np.errstate(all="raise"):
                product = np.complex128(
                    np.multiply(left[index], right[index])
                )
            record = {"node": name, "value": p44_scalar_identity(product)}
        except Exception as exc:
            fail_node(name, exc)
        products.append(product)
        internal.append(record)
        return product

    if algorithm == "explicit_naive":
        accumulator = np.complex128(complex(0.0, 0.0))
        for index in range(7):
            product = product_at(index)
            name = f"partial[{index}]"
            try:
                with np.errstate(all="raise"):
                    accumulator = np.complex128(np.add(accumulator, product))
                record = {
                    "node": name,
                    "value": p44_scalar_identity(accumulator),
                }
            except Exception as exc:
                fail_node(name, exc)
            internal.append(record)
        output = accumulator
    elif algorithm == "fixed_pairwise":
        for index in range(7):
            product_at(index)

        def pair(name: str, left_value: Any, right_value: Any) -> np.complex128:
            try:
                with np.errstate(all="raise"):
                    value = np.complex128(np.add(left_value, right_value))
                record = {"node": name, "value": p44_scalar_identity(value)}
            except Exception as exc:
                fail_node(name, exc)
            internal.append(record)
            return value

        n01 = pair("n01", products[0], products[1])
        n23 = pair("n23", products[2], products[3])
        n45 = pair("n45", products[4], products[5])
        n456 = pair("n456", n45, products[6])
        n0123 = pair("n0123", n01, n23)
        output = pair("root", n0123, n456)
    elif algorithm == "componentwise_kahan":
        real_sum = np.float64(0.0)
        imag_sum = np.float64(0.0)
        real_compensation = np.float64(0.0)
        imag_compensation = np.float64(0.0)
        for index in range(7):
            product = product_at(index)
            name = f"kahan[{index}]"
            try:
                with np.errstate(all="raise"):
                    real_adjusted = np.float64(
                        np.subtract(np.float64(product.real), real_compensation)
                    )
                    real_next = np.float64(np.add(real_sum, real_adjusted))
                    real_compensation = np.float64(
                        np.subtract(
                            np.subtract(real_next, real_sum), real_adjusted
                        )
                    )
                    real_sum = real_next
                    imag_adjusted = np.float64(
                        np.subtract(np.float64(product.imag), imag_compensation)
                    )
                    imag_next = np.float64(np.add(imag_sum, imag_adjusted))
                    imag_compensation = np.float64(
                        np.subtract(
                            np.subtract(imag_next, imag_sum), imag_adjusted
                        )
                    )
                    imag_sum = imag_next
                record = {
                    "node": name,
                    "real_sum": p44_scalar_identity(real_sum),
                    "real_compensation": p44_scalar_identity(real_compensation),
                    "imag_sum": p44_scalar_identity(imag_sum),
                    "imag_compensation": p44_scalar_identity(imag_compensation),
                }
            except Exception as exc:
                fail_node(name, exc)
            internal.append(record)
        output = np.complex128(complex(float(real_sum), float(imag_sum)))
    else:
        raise InvalidRun(f"undeclared complex dot algorithm: {algorithm}")

    try:
        exact_left = [mp_complex_from_binary64(complex(value)) for value in left]
        exact_right = [mp_complex_from_binary64(complex(value)) for value in right]
        exact_terms = [exact_left[index] * exact_right[index] for index in range(7)]
        exact_sum = mp.fsum(exact_terms)
        sum_magnitudes = mp.fsum(
            abs(exact_left[index]) * abs(exact_right[index])
            for index in range(7)
        )
        kappa = sum_magnitudes / max(abs(exact_sum), mp.mpf("1e-100"))
        budgets = {
            "explicit_naive": 56,
            "fixed_pairwise": 54,
            "componentwise_kahan": 98,
        }
        budget = budgets[algorithm]
        gamma, gamma_ratio = p44_gamma_exact(budget)
        error = abs(mp_complex_from_binary64(complex(output)) - exact_sum)
        radius = gamma * sum_magnitudes
    except Exception as exc:
        raise SlotEvaluationError(
            f"alternative dot metric failed at {path}: {type(exc).__name__}: {exc}",
            payload={
                "failure_scope": "alternative_dot_metric",
                "failed_node_key": f"{path}/metric",
                "dot_path": path,
                "algorithm": algorithm,
                "completed_internal_records": list(internal),
                "expected_internal_node_names": list(expected_names),
                "expected_failure_node_keys": list(failure_node_keys),
                "preenumerated_membership_sha256": membership_digest,
                "underlying_error_type": type(exc).__name__,
                "underlying_error_message": str(exc)[:2048],
            },
        ) from exc
    return output, {
        "path": path,
        "algorithm": algorithm,
        "index_order": list(range(7)),
        "products_and_internal_nodes": internal,
        "failure_node_membership_sha256": membership_digest,
        "output_identity": p44_scalar_identity(output),
        "exact_lifted_sum": mp_complex_payload(exact_sum, AUTHORITATIVE_DPS),
        "sum_exact_lifted_operand_magnitudes": mp_number_string(
            sum_magnitudes, AUTHORITATIVE_DPS
        ),
        "kappa_dot": mp_number_string(kappa, AUTHORITATIVE_DPS),
        "operation_budget": budget,
        "gamma": mp_number_string(gamma, AUTHORITATIVE_DPS),
        "gamma_exact_rational": gamma_ratio,
        "forward_radius": mp_number_string(radius, AUTHORITATIVE_DPS),
        "observed_error": mp_number_string(error, AUTHORITATIVE_DPS),
        "within_named_algorithm_bound": error <= radius,
    }


def p44_explicit_matmul(
    left: np.ndarray,
    right: np.ndarray,
    algorithm: str,
    *,
    path: str,
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    left_array = np.asarray(left)
    right_array = np.asarray(right)
    allowed_dtypes = {np.dtype(np.float64), np.dtype(np.complex128)}
    if left_array.dtype not in allowed_dtypes or right_array.dtype not in allowed_dtypes:
        raise InvalidRun("explicit matmul input dtype drift")
    right_was_vector = right_array.ndim == 1
    if left_array.ndim != 2 or right_array.ndim not in (1, 2):
        raise InvalidRun("explicit matmul rank drift")
    if right_was_vector:
        right_array = right_array.reshape(-1, 1)
    if left_array.shape[1] != 7 or right_array.shape[0] != 7:
        raise InvalidRun("explicit matmul fixed inner dimension drift")
    output = np.empty(
        (left_array.shape[0], right_array.shape[1]), dtype=np.complex128
    )
    records: list[dict[str, Any]] = []
    expected_dot_paths = [
        {"dot_path": f"{path}/dot[{row},{column}]"}
        for row in range(output.shape[0])
        for column in range(output.shape[1])
    ]
    membership_digest = p44_sequence_commitment(expected_dot_paths)
    for row in range(output.shape[0]):
        for column in range(output.shape[1]):
            dot_path = f"{path}/dot[{row},{column}]"
            try:
                value, record = p44_explicit_complex_dot(
                    left_array[row, :],
                    right_array[:, column],
                    algorithm,
                    path=dot_path,
                )
            except SlotEvaluationError as exc:
                raise SlotEvaluationError(
                    str(exc),
                    payload={
                        **exc.payload,
                        "matmul_path": path,
                        "failed_dot_path": dot_path,
                        "completed_dot_records_before_failed_dot": list(records),
                        "expected_dot_paths": expected_dot_paths,
                        "matmul_dot_membership_sha256": membership_digest,
                    },
                ) from exc
            output[row, column] = value
            records.append(record)
    if right_was_vector:
        return output[:, 0], records
    return output, records


def p44_alternative_contraction(
    linear_map: np.ndarray,
    h64: np.ndarray,
    q: np.ndarray,
    association: str,
    algorithm: str,
    *,
    retention_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    l_source = np.asarray(linear_map)
    if l_source.dtype != np.dtype(np.float64):
        raise InvalidRun("alternative contraction linear_map dtype drift")
    if np.asarray(h64).dtype != np.dtype(np.complex128):
        raise InvalidRun("alternative contraction H64 dtype drift")
    if np.asarray(q).dtype != np.dtype(np.complex128):
        raise InvalidRun("alternative contraction q dtype drift")
    all_dots: list[dict[str, Any]] = []
    completed_intermediates: dict[str, Any] = {}
    expected_shape = p44_alternative_shape(association, algorithm)

    def run_matmul(
        stage_path: str, left_value: np.ndarray, right_value: np.ndarray
    ) -> np.ndarray:
        try:
            output, records = p44_explicit_matmul(
                left_value, right_value, algorithm, path=stage_path
            )
        except SlotEvaluationError as exc:
            completed_failed_stage = exc.payload.get(
                "completed_dot_records_before_failed_dot", []
            )
            if not isinstance(completed_failed_stage, list):
                completed_failed_stage = []
            failed_node_key = str(exc.payload.get("failed_node_key", ""))
            failed_node_is_preenumerated = failed_node_key in expected_shape[
                "failure_node_keys_in_fixed_order"
            ]
            raise SlotEvaluationError(
                str(exc),
                payload={
                    **exc.payload,
                    "failure_scope": "alternative_internal_node",
                    "association": association,
                    "summation_algorithm": algorithm,
                    "failed_matmul_stage": stage_path,
                    "completed_dot_records": [
                        *all_dots,
                        *completed_failed_stage,
                    ],
                    "completed_intermediates": dict(completed_intermediates),
                    "alternative_expected_shape": expected_shape,
                    "alternative_internal_membership_sha256": expected_shape[
                        "internal_path_commitment_sha256"
                    ],
                    "alternative_failure_node_membership_sha256": (
                        expected_shape["failure_node_membership_sha256"]
                    ),
                    "failed_node_is_preenumerated": (
                        failed_node_is_preenumerated
                    ),
                },
            ) from exc
        all_dots.extend(records)
        return output

    if association == "left_matrix_chain":
        first = run_matmul(
            "left/LT_H", l_source.T, np.asarray(h64)
        )
        completed_intermediates["first"] = binary64_payload(first)
        second = run_matmul(
            "left/B1_L", first, l_source
        )
        completed_intermediates["second"] = binary64_payload(second)
        y = run_matmul(
            "left/B2_q", second, np.asarray(q)
        )
    elif association == "vector_first_chain":
        first = run_matmul(
            "vector_first/L_q", l_source, np.asarray(q)
        )
        completed_intermediates["first"] = binary64_payload(first)
        second = run_matmul(
            "vector_first/H_Lq", np.asarray(h64), first
        )
        completed_intermediates["second"] = binary64_payload(second)
        y = run_matmul(
            "vector_first/LT_HLq", l_source.T, second
        )
    else:
        raise InvalidRun(f"undeclared association: {association}")
    intermediates = dict(completed_intermediates)
    try:
        with np.errstate(all="raise"):
            a = np.asarray(-np.conjugate(y), dtype=np.complex128)
    except Exception as exc:
        raise SlotEvaluationError(
            (
                f"alternative outer operation failed for {association}|{algorithm}: "
                f"{type(exc).__name__}: {exc}"
            ),
            payload={
                "failure_scope": "alternative_outer_operation",
                "failed_node_key": f"{association}|{algorithm}/outer",
                "association": association,
                "summation_algorithm": algorithm,
                "completed_dot_records": list(all_dots),
                "completed_intermediates": dict(completed_intermediates),
                "alternative_expected_shape": expected_shape,
                "alternative_internal_membership_sha256": expected_shape[
                    "internal_path_commitment_sha256"
                ],
                "alternative_failure_node_membership_sha256": expected_shape[
                    "failure_node_membership_sha256"
                ],
                "failed_node_is_preenumerated": True,
                "underlying_error_type": type(exc).__name__,
                "underlying_error_message": str(exc)[:2048],
            },
        ) from exc
    if retention_state is not None:
        retention_state["attempted_alternative_completed_contraction"] = {
            "association": association,
            "summation_algorithm": algorithm,
            "completed_dot_records": list(all_dots),
            "completed_intermediates": dict(completed_intermediates),
            "y_alt": binary64_payload(y),
            "A_alt": binary64_payload(a),
            "alternative_expected_shape": expected_shape,
            "alternative_internal_membership_sha256": expected_shape[
                "internal_path_commitment_sha256"
            ],
            "alternative_failure_node_membership_sha256": expected_shape[
                "failure_node_membership_sha256"
            ],
            "post_contraction_metrics_complete": False,
        }
    budgets = {
        "explicit_naive": 56,
        "fixed_pairwise": 54,
        "componentwise_kahan": 98,
    }
    budget = budgets[algorithm]
    l_mp = p44_mp_complex_matrix_from_numpy(l_source)
    h_mp = p44_mp_complex_matrix_from_numpy(h64)
    q_mp = p44_mp_column(
        [mp_complex_from_binary64(complex(value)) for value in q]
    )
    zero_matrix = p44_zero_radii(7, 7)
    zero_column = p44_zero_radii(7, 1)
    if association == "left_matrix_chain":
        first_mp = p44_mp_complex_matrix_from_numpy(first)
        second_mp = p44_mp_complex_matrix_from_numpy(second)
        first_center, first_radii, first_envelope = p44_mp_matmul_disk(
            l_mp.T,
            zero_matrix,
            h_mp,
            zero_matrix,
            operation_budget=budget,
            observed_output=first_mp,
        )
        second_center, second_radii, second_envelope = p44_mp_matmul_disk(
            first_center,
            first_radii,
            l_mp,
            zero_matrix,
            operation_budget=budget,
            observed_output=second_mp,
        )
        y_center, y_radii, y_envelope = p44_mp_matmul_disk(
            second_center,
            second_radii,
            q_mp,
            zero_column,
            operation_budget=budget,
            observed_output=p44_mp_column(
                [mp_complex_from_binary64(complex(value)) for value in y]
            ),
        )
    else:
        first_mp = p44_mp_column(
            [mp_complex_from_binary64(complex(value)) for value in first]
        )
        second_mp = p44_mp_column(
            [mp_complex_from_binary64(complex(value)) for value in second]
        )
        first_center, first_radii, first_envelope = p44_mp_matmul_disk(
            l_mp,
            zero_matrix,
            q_mp,
            zero_column,
            operation_budget=budget,
            observed_output=first_mp,
        )
        second_center, second_radii, second_envelope = p44_mp_matmul_disk(
            h_mp,
            zero_matrix,
            first_center,
            first_radii,
            operation_budget=budget,
            observed_output=second_mp,
        )
        y_center, y_radii, y_envelope = p44_mp_matmul_disk(
            l_mp.T,
            zero_matrix,
            second_center,
            second_radii,
            operation_budget=budget,
            observed_output=p44_mp_column(
                [mp_complex_from_binary64(complex(value)) for value in y]
            ),
        )
    exact_reference = p44_matrix_vector(l_mp.T * h_mp * l_mp * q_mp)
    observed_y = [mp_complex_from_binary64(complex(value)) for value in y]
    chain_check = p44_envelope_check(
        [observed_y[index] - exact_reference[index] for index in range(7)],
        [row[0] for row in y_radii],
    )
    chain_check["final_propagated_center"] = mp_vector_payload(
        p44_matrix_vector(y_center), AUTHORITATIVE_DPS
    )
    chain_check["exact_lifted_input_reference"] = mp_vector_payload(
        exact_reference, AUTHORITATIVE_DPS
    )
    return {
        "association": association,
        "summation_algorithm": algorithm,
        "input_dtypes": {
            "linear_map": str(l_source.dtype),
            "H64": str(np.asarray(h64).dtype),
            "q": str(np.asarray(q).dtype),
        },
        "intermediates": intermediates,
        "dot_records": all_dots,
        "dot_count": len(all_dots),
        "dot_kappa_summary": p44_dot_kappa_summary(
            all_dots,
            stage_label=f"{association}|{algorithm}",
        ),
        "y_alt": binary64_payload(y),
        "A_alt": binary64_payload(a),
        "named_algorithm_chain_envelope": {
            "operation_budget": budget,
            "first": first_envelope,
            "second": second_envelope,
            "third": y_envelope,
            "final": chain_check,
        },
        "y_alt_array": y,
        "A_alt_array": a,
        "all_named_algorithm_dot_bounds_hold": all(
            record["within_named_algorithm_bound"] for record in all_dots
        ),
    }


def p44_vector_metrics(left: Sequence[Any], right: Sequence[Any]) -> dict[str, Any]:
    left_values = [mp.mpc(value) for value in left]
    right_values = [mp.mpc(value) for value in right]
    differences = [
        left_values[index] - right_values[index] for index in range(len(left_values))
    ]
    floor = mp.mpf("1e-100")
    return {
        "difference_orientation": "left_minus_right",
        "signed_complex_difference": mp_vector_payload(
            differences, AUTHORITATIVE_DPS
        ),
        "symmetric_relative": mp_number_string(
            mp_relative(left_values, right_values), AUTHORITATIVE_DPS
        ),
        "max_component_relative": mp_number_string(
            mp_max_component_relative(left_values, right_values), AUTHORITATIVE_DPS
        ),
        "max_component_absolute": mp_number_string(
            mp_max_abs(left_values, right_values), AUTHORITATIVE_DPS
        ),
        "component_absolute": [
            mp_number_string(abs(value), AUTHORITATIVE_DPS) for value in differences
        ],
        "component_relative": [
            mp_number_string(
                abs(differences[index])
                / max(abs(left_values[index]), abs(right_values[index]), floor),
                AUTHORITATIVE_DPS,
            )
            for index in range(len(differences))
        ],
    }


def p44_envelope_check(
    actual_delta: Sequence[Any], radii: Sequence[Any]
) -> dict[str, Any]:
    deltas = [mp.mpc(value) for value in actual_delta]
    radius_values = [mp.mpf(value) for value in radii]
    floor = mp.mpf("1e-100")
    component_utilizations = [
        abs(deltas[index]) / max(radius_values[index], floor)
        for index in range(len(deltas))
    ]
    norm_radius = mp.sqrt(mp.fsum(radius**2 for radius in radius_values))
    delta_norm = mp_norm(deltas)
    norm_utilization = delta_norm / max(norm_radius, floor)
    return {
        "actual_delta": mp_vector_payload(deltas, AUTHORITATIVE_DPS),
        "component_radii": [
            mp_number_string(radius, AUTHORITATIVE_DPS) for radius in radius_values
        ],
        "component_utilizations": [
            mp_number_string(value, AUTHORITATIVE_DPS)
            for value in component_utilizations
        ],
        "norm_radius": mp_number_string(norm_radius, AUTHORITATIVE_DPS),
        "actual_delta_norm": mp_number_string(delta_norm, AUTHORITATIVE_DPS),
        "norm_utilization": mp_number_string(norm_utilization, AUTHORITATIVE_DPS),
        "all_components_within": all(value <= 1 for value in component_utilizations),
        "norm_within": norm_utilization <= 1,
        "covered": bool(
            all(value <= 1 for value in component_utilizations)
            and norm_utilization <= 1
        ),
    }


def p44_state_formation_envelope(
    linear_map: mp.matrix,
    saddle: Sequence[Any],
    xi: Sequence[Any],
    u64: Sequence[Any],
    w64: Sequence[Any],
) -> tuple[list[mp.mpc], list[mp.mpf], dict[str, Any]]:
    xi_column = p44_mp_column(xi)
    u_exact = p44_matrix_vector(linear_map * xi_column)
    w_exact = [mp.mpc(saddle[index]) + u_exact[index] for index in range(7)]
    u64_lift = [mp_complex_from_binary64(complex(value)) for value in u64]
    w64_lift = [mp_complex_from_binary64(complex(value)) for value in w64]
    _unit, unit_roundoff_ratio = p44_unit_roundoff_exact()
    gamma1, gamma1_ratio = p44_gamma_exact(1)
    gamma56, gamma56_ratio = p44_gamma_exact(56)
    u_radii = [
        gamma56
        * mp.fsum(abs(linear_map[row, column]) * abs(xi[column]) for column in range(7))
        for row in range(7)
    ]
    add_local_component_radii: list[tuple[mp.mpf, mp.mpf]] = []
    add_local_disk_radii: list[mp.mpf] = []
    w_radii: list[mp.mpf] = []
    for index in range(7):
        local_real = gamma1 * abs(w64_lift[index].real)
        local_imag = gamma1 * abs(w64_lift[index].imag)
        local = mp.sqrt(local_real**2 + local_imag**2)
        add_local_component_radii.append((local_real, local_imag))
        add_local_disk_radii.append(local)
        w_radii.append(u_radii[index] + local)
    u_errors = [abs(u64_lift[index] - u_exact[index]) for index in range(7)]
    w_errors = [abs(w64_lift[index] - w_exact[index]) for index in range(7)]
    w_add_local_residuals = [
        w64_lift[index] - (mp.mpc(saddle[index]) + u64_lift[index])
        for index in range(7)
    ]
    w_add_local_errors = [abs(value) for value in w_add_local_residuals]
    payload = {
        "gamma56": mp_number_string(gamma56, AUTHORITATIVE_DPS),
        "unit_roundoff_exact_rational": unit_roundoff_ratio,
        "gamma1_exact_rational": gamma1_ratio,
        "gamma56_exact_rational": gamma56_ratio,
        "u_exact": mp_vector_payload(u_exact, AUTHORITATIVE_DPS),
        "w_exact": mp_vector_payload(w_exact, AUTHORITATIVE_DPS),
        "u_component_radii": [
            mp_number_string(value, AUTHORITATIVE_DPS) for value in u_radii
        ],
        "w_add_local_real_imag_component_radii": [
            [
                mp_number_string(value[0], AUTHORITATIVE_DPS),
                mp_number_string(value[1], AUTHORITATIVE_DPS),
            ]
            for value in add_local_component_radii
        ],
        "w_add_local_component_disk_radii": [
            mp_number_string(value, AUTHORITATIVE_DPS)
            for value in add_local_disk_radii
        ],
        "w_component_radii": [
            mp_number_string(value, AUTHORITATIVE_DPS) for value in w_radii
        ],
        "u_observed_errors": [
            mp_number_string(value, AUTHORITATIVE_DPS) for value in u_errors
        ],
        "w_observed_errors": [
            mp_number_string(value, AUTHORITATIVE_DPS) for value in w_errors
        ],
        "w_add_local_observed_errors": [
            mp_number_string(value, AUTHORITATIVE_DPS)
            for value in w_add_local_errors
        ],
        "w_add_local_observed_real_imag_residuals": [
            [
                mp_number_string(value.real, AUTHORITATIVE_DPS),
                mp_number_string(value.imag, AUTHORITATIVE_DPS),
            ]
            for value in w_add_local_residuals
        ],
        "u_all_covered": all(
            u_errors[index] <= u_radii[index] for index in range(7)
        ),
        "w_all_covered": all(
            w_errors[index] <= w_radii[index] for index in range(7)
        ),
        "w_add_local_all_covered": all(
            abs(w_add_local_residuals[index].real)
            <= add_local_component_radii[index][0]
            and abs(w_add_local_residuals[index].imag)
            <= add_local_component_radii[index][1]
            for index in range(7)
        ),
        "w_add_local_componentwise_rule": (
            "abs(real residual)<=real radius AND "
            "abs(imag residual)<=imag radius; disk hypot is propagation-only"
        ),
    }
    return w_exact, w_radii, payload


def p44_stage_signed_zero_metadata(
    stage_vectors: Mapping[str, Sequence[Any]],
    boundaries: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for stage_id in STAGE_IDS:
        values = [mp.mpc(value) for value in stage_vectors[stage_id]]
        record: dict[str, Any] = {
            "stage_representation": "mpmath_120dps",
            "binary_signed_zero_applicable": False,
            "zero_component_presence": [
                {
                    "real_is_exact_zero": value.real == 0,
                    "imag_is_exact_zero": value.imag == 0,
                    "real_signed_zero": None,
                    "imag_signed_zero": None,
                }
                for value in values
            ],
            "policy": (
                "mpmath exact zeros are unsigned; binary signbits are retained "
                "only when a stage has a direct binary64 boundary origin"
            ),
        }
        if stage_id == STAGE_IDS[6]:
            y_identity = binary64_payload(boundaries["y64"])
            derived_output_signed_zero = []
            for index, component in enumerate(y_identity["components"]):
                real_zero = component["real_ratio"][0] == 0
                imag_zero = component["imag_ratio"][0] == 0
                if (values[index].real == 0) is not real_zero or (
                    values[index].imag == 0
                ) is not imag_zero:
                    raise InvalidRun("S6/y64 zero-component magnitude drift")
                derived_output_signed_zero.append(
                    {
                        "real_is_exact_zero": real_zero,
                        "imag_is_exact_zero": imag_zero,
                        "real_signed_zero": (
                            not component["real_signed_zero"]
                            if real_zero
                            else None
                        ),
                        "imag_signed_zero": (
                            component["imag_signed_zero"]
                            if imag_zero
                            else None
                        ),
                    }
                )
            record["direct_binary64_input_boundary"] = {
                "name": "y64",
                "identity": y_identity,
                "role": "pre_outer_input",
            }
            record["binary_signed_zero_applicable"] = True
            record["zero_component_presence"] = derived_output_signed_zero
            record["derived_output_signed_zero"] = derived_output_signed_zero
            record["derived_output_rule"] = (
                "For A=-conjugate(y), a zero real signbit flips once and a "
                "zero imaginary signbit flips twice, so imag retains y64 sign."
            )
        elif stage_id == STAGE_IDS[7]:
            identity = binary64_payload(boundaries["A64"])
            record.update(
                {
                    "stage_representation": "exact_binary64_ratio_lift",
                    "binary_signed_zero_applicable": True,
                    "direct_binary64_output_boundary": {
                        "name": "A64",
                        "identity": identity,
                    },
                    "zero_component_presence": [
                        {
                            "real_is_exact_zero": component["real_ratio"][0]
                            == 0,
                            "imag_is_exact_zero": component["imag_ratio"][0]
                            == 0,
                            "real_signed_zero": component["real_signed_zero"],
                            "imag_signed_zero": component["imag_signed_zero"],
                        }
                        for component in identity["components"]
                    ],
                }
            )
        output[stage_id] = record
    return output


def p44_stage_and_delta_payload(
    stage_vectors: Mapping[str, Sequence[Any]],
    stage_signed_zero_metadata: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, list[mp.mpc]], dict[str, Any]]:
    if tuple(stage_vectors) != STAGE_IDS:
        raise InvalidRun("hybrid stage order drift")
    if tuple(stage_signed_zero_metadata) != STAGE_IDS:
        raise InvalidRun("hybrid stage signed-zero metadata order drift")
    stages: dict[str, Any] = {}
    normalized = {
        key: [mp.mpc(value) for value in stage_vectors[key]] for key in STAGE_IDS
    }
    for key in STAGE_IDS:
        stages[key] = {
            "value": mp_vector_payload(normalized[key], AUTHORITATIVE_DPS),
            "norm": mp_number_string(mp_norm(normalized[key]), AUTHORITATIVE_DPS),
            "signed_zero_metadata": dict(stage_signed_zero_metadata[key]),
        }
    delta_vectors: dict[str, list[mp.mpc]] = {}
    deltas: dict[str, Any] = {}
    total = [
        normalized[STAGE_IDS[-1]][index] - normalized[STAGE_IDS[0]][index]
        for index in range(7)
    ]
    total_norm = mp_norm(total)
    for index, delta_id in enumerate(DELTA_IDS):
        left = normalized[STAGE_IDS[index + 1]]
        right = normalized[STAGE_IDS[index]]
        vector = [left[component] - right[component] for component in range(7)]
        delta_vectors[delta_id] = vector
        deltas[delta_id] = {
            "from_stage": STAGE_IDS[index],
            "to_stage": STAGE_IDS[index + 1],
            "value": mp_vector_payload(vector, AUTHORITATIVE_DPS),
            "norm": mp_number_string(mp_norm(vector), AUTHORITATIVE_DPS),
            "resolved_delta_relative": mp_number_string(
                mp_relative(left, right), AUTHORITATIVE_DPS
            ),
            "phase43_total_error_fraction": mp_number_string(
                mp_norm(vector) / max(total_norm, mp.mpf("1e-100")),
                AUTHORITATIVE_DPS,
            ),
            "component_metrics": p44_vector_metrics(left, right),
        }
    ordered_sum = [mp.mpc("0") for _component in range(7)]
    for delta_id in DELTA_IDS:
        for component in range(7):
            ordered_sum[component] = (
                ordered_sum[component] + delta_vectors[delta_id][component]
            )
    fsum_cross_check = [
        mp.fsum(delta_vectors[delta_id][component] for delta_id in DELTA_IDS)
        for component in range(7)
    ]
    closure_residual = [ordered_sum[index] - total[index] for index in range(7)]
    closure = {
        "S7_minus_S0": mp_vector_payload(total, AUTHORITATIVE_DPS),
        "ordered_sum_of_deltas": mp_vector_payload(ordered_sum, AUTHORITATIVE_DPS),
        "fsum_cross_check_not_used_for_closure": mp_vector_payload(
            fsum_cross_check, AUTHORITATIVE_DPS
        ),
        "residual": mp_vector_payload(closure_residual, AUTHORITATIVE_DPS),
        "relative": mp_number_string(
            mp_relative(ordered_sum, total), AUTHORITATIVE_DPS
        ),
        "max_absolute": mp_number_string(
            max(abs(value) for value in closure_residual), AUTHORITATIVE_DPS
        ),
    }
    alignments: dict[str, Any] = {}
    floor = mp.mpf("1e-100")
    for left_id in DELTA_IDS:
        for right_id in DELTA_IDS:
            numerator = mp.re(
                mp.fsum(
                    mp.conj(delta_vectors[left_id][index])
                    * delta_vectors[right_id][index]
                    for index in range(7)
                )
            )
            denominator = max(
                mp_norm(delta_vectors[left_id]) * mp_norm(delta_vectors[right_id]),
                floor,
            )
            alignments[f"{left_id}|{right_id}"] = mp_number_string(
                numerator / denominator, AUTHORITATIVE_DPS
            )
    cancellation = {
        "sum_delta_norms_over_total_norm": mp_number_string(
            mp.fsum(mp_norm(delta_vectors[key]) for key in DELTA_IDS)
            / max(total_norm, floor),
            AUTHORITATIVE_DPS,
        ),
        "pairwise_real_alignments": alignments,
    }
    return stages, deltas, delta_vectors, {"closure": closure, "cancellation": cancellation}


def p44_algebraic_dot_condition_records(
    left: np.ndarray, right: np.ndarray, *, path: str
) -> list[dict[str, Any]]:
    left_array = np.asarray(left, dtype=np.complex128)
    right_array = np.asarray(right, dtype=np.complex128)
    if right_array.ndim == 1:
        right_array = right_array.reshape(-1, 1)
    records: list[dict[str, Any]] = []
    for row in range(left_array.shape[0]):
        for column in range(right_array.shape[1]):
            terms = [
                mp_complex_from_binary64(complex(left_array[row, index]))
                * mp_complex_from_binary64(complex(right_array[index, column]))
                for index in range(7)
            ]
            exact_sum = mp.fsum(terms)
            magnitude_sum = mp.fsum(abs(value) for value in terms)
            records.append(
                {
                    "path": f"{path}/dot[{row},{column}]",
                    "algebraic_term_order_only": list(range(7)),
                    "private_BLAS_reduction_order_claimed": False,
                    "terms": mp_vector_payload(terms, AUTHORITATIVE_DPS),
                    "exact_sum": mp_complex_payload(exact_sum, AUTHORITATIVE_DPS),
                    "sum_term_magnitudes": mp_number_string(
                        magnitude_sum, AUTHORITATIVE_DPS
                    ),
                    "kappa_dot": mp_number_string(
                        magnitude_sum / max(abs(exact_sum), mp.mpf("1e-100")),
                        AUTHORITATIVE_DPS,
                    ),
                }
            )
    return records


def p44_singular_values(matrix: mp.matrix) -> list[mp.mpf]:
    singular_values = mp.svd(matrix, compute_uv=False)
    return [mp.mpf(abs(singular_values[index])) for index in range(len(singular_values))]


def p44_conditioning_payload(
    linear_map: mp.matrix,
    hessian64: mp.matrix,
    q: Sequence[Any],
    y3: Sequence[Any],
    s1: Sequence[Any],
    s2: Sequence[Any],
    w_exact: Sequence[Any],
    w64: Sequence[Any],
    source_arrays: Mapping[str, np.ndarray],
    *,
    retention_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    if retention_state is not None:
        retention_state["completed_conditioning"] = output
        retention_state["attempted_conditioning_name"] = "expanded_component"
    expanded: list[mp.mpf] = []
    for output_index in range(7):
        numerator = mp.fsum(
            abs(
                linear_map[first, output_index]
                * hessian64[first, second]
                * linear_map[second, third]
                * q[third]
            )
            for first in range(7)
            for second in range(7)
            for third in range(7)
        )
        expanded.append(
            numerator / max(abs(y3[output_index]), mp.mpf("1e-100"))
        )
    output["expanded_component_cancellation"] = [
        mp_number_string(value, AUTHORITATIVE_DPS) for value in expanded
    ]
    output["max_expanded_component_cancellation"] = mp_number_string(
        max(expanded), AUTHORITATIVE_DPS
    )

    if retention_state is not None:
        retention_state["attempted_conditioning_name"] = "source_dots"
    l_np = np.asarray(source_arrays["linear_map"], dtype=np.complex128)
    source_dot_records = []
    source_dot_records.extend(
        p44_algebraic_dot_condition_records(
            l_np.T, source_arrays["H64"], path="source/B1"
        )
    )
    source_dot_records.extend(
        p44_algebraic_dot_condition_records(
            source_arrays["B1_64"], l_np, path="source/B2"
        )
    )
    source_dot_records.extend(
        p44_algebraic_dot_condition_records(
            source_arrays["B2_64"], source_arrays["q"], path="source/y"
        )
    )
    output["source_algebraic_dot_conditions"] = source_dot_records
    output["source_dot_kappa_summary"] = p44_dot_kappa_summary(
        source_dot_records, stage_label="numpy_source"
    )

    if retention_state is not None:
        retention_state["attempted_conditioning_name"] = "normwise_chain"
    l_singular_values = p44_singular_values(linear_map)
    h_singular_values = p44_singular_values(hessian64)
    l_norm = max(l_singular_values, default=mp.mpf("0"))
    h_norm = max(h_singular_values, default=mp.mpf("0"))
    q_norm = mp_norm(q)
    y_norm = mp_norm(y3)
    chain = l_norm * h_norm * l_norm * q_norm / max(
        y_norm, mp.mpf("1e-100")
    )
    output["normwise_chain"] = {
        "linear_map_norm_2": mp_number_string(l_norm, AUTHORITATIVE_DPS),
        "hessian_norm_2": mp_number_string(h_norm, AUTHORITATIVE_DPS),
        "linear_map_singular_values_120dps": [
            mp_number_string(value, AUTHORITATIVE_DPS)
            for value in l_singular_values
        ],
        "hessian_singular_values_120dps": [
            mp_number_string(value, AUTHORITATIVE_DPS)
            for value in h_singular_values
        ],
        "q_norm_2": mp_number_string(q_norm, AUTHORITATIVE_DPS),
        "y_norm_2": mp_number_string(y_norm, AUTHORITATIVE_DPS),
        "kappa_chain": mp_number_string(chain, AUTHORITATIVE_DPS),
        "singular_values_role": "120dps_diagnostic_approximation",
    }

    if retention_state is not None:
        retention_state["attempted_conditioning_name"] = "state_secant"
    w_relative = mp_relative(w64, w_exact)
    state_secant = mp_relative(s2, s1) / max(w_relative, mp.mpf("1e-100"))
    output["state_secant"] = {
        "w_relative": mp_number_string(w_relative, AUTHORITATIVE_DPS),
        "S2_to_S1_relative": mp_number_string(
            mp_relative(s2, s1), AUTHORITATIVE_DPS
        ),
        "kappa_state": mp_number_string(state_secant, AUTHORITATIVE_DPS),
        "role": "observed_secant_not_global_condition_number",
    }

    if retention_state is not None:
        retention_state["attempted_conditioning_name"] = "roundoff_risk"
    gamma56, gamma56_ratio = p44_gamma_exact(56)
    risk = gamma56 * max(expanded)
    output["roundoff_risk_indicator"] = {
        "gamma56_times_max_kappa_expand": mp_number_string(
            risk, AUTHORITATIVE_DPS
        ),
        "gamma56_exact_rational": gamma56_ratio,
        "threshold": "5e-13",
        "at_or_above_threshold": risk >= mp.mpf("5e-13"),
        "role": "heuristic_cancellation_risk_indicator_not_forward_bound",
    }
    if retention_state is not None:
        retention_state["attempted_conditioning_name"] = None
    return output


def p44_slot_dependency_paths(
    point: str,
    base: str,
    constant_subtree_digests: Sequence[str],
) -> dict[str, list[str]]:
    formula_dependencies = [f"formula|point={point}|action"] + [
        f"formula|point={point}|gradient={component}" for component in range(7)
    ] + [
        f"formula|point={point}|hessian={row},{column}"
        for row in range(7)
        for column in range(7)
    ]
    constant_dependencies = [
        f"constant_subtree|point={point}|sha256={digest}"
        for digest in sorted(constant_subtree_digests)
    ]

    def unique(*groups: Sequence[str]) -> list[str]:
        return list(dict.fromkeys(key for group in groups for key in group))

    coefficient = unique(
        formula_dependencies,
        constant_dependencies,
        [
            f"stage|{base}|{STAGE_IDS[0]}",
            f"stage|{base}|{STAGE_IDS[1]}",
            f"delta|{base}|D_coeff",
        ],
    )
    state = [
        f"boundaries|{base}",
        f"stage|{base}|{STAGE_IDS[1]}",
        f"stage|{base}|{STAGE_IDS[2]}",
        f"delta|{base}|D_state",
    ]
    hessian = [
        f"trace|{base}|whole",
        f"boundaries|{base}",
        f"stage|{base}|{STAGE_IDS[2]}",
        f"stage|{base}|{STAGE_IDS[3]}",
        f"delta|{base}|D_hessian",
    ]
    contraction = [
        f"boundaries|{base}",
        *[f"stage|{base}|{stage}" for stage in STAGE_IDS[3:7]],
        f"delta|{base}|D_matmul_1",
        f"delta|{base}|D_matmul_2",
        f"delta|{base}|D_matvec",
    ]
    cancellation = [
        f"input|{base}",
        f"boundaries|{base}",
        f"stage|{base}|{STAGE_IDS[3]}",
        f"conditioning|{base}|expanded_component",
        f"conditioning|{base}|roundoff_risk",
    ]
    coverage = unique(
        formula_dependencies,
        constant_dependencies,
        [
            f"input|{base}",
            f"boundaries|{base}",
            f"trace|{base}|whole",
            f"envelope|{base}|coefficient",
            f"envelope|{base}|state",
            f"envelope|{base}|scalar_AST",
            f"envelope|{base}|matmul_1",
            f"envelope|{base}|matmul_2",
            f"envelope|{base}|matvec",
            f"envelope|{base}|outer",
            f"envelope|{base}|total_source",
        ],
    )
    return {
        "formula_mismatch": formula_dependencies,
        "coefficient_rounding": coefficient,
        "state_rounding": state,
        "hessian_rounding": hessian,
        "contraction_rounding": contraction,
        "cancellation_scale": cancellation,
        "forward_error_coverage": coverage,
        "unresolved_beyond_model": [
            f"evidence|{base}|formula_mismatch",
            f"evidence|{base}|forward_error_coverage",
        ],
    }


def p44_frozen_record_paths(slot: P44SlotInput) -> dict[str, Any]:
    base = (
        f"point={slot.point}|fraction={slot.fraction}|"
        f"direction={slot.direction}"
    )
    return {
        "phase43_result_artifact": relative_repo_path(PHASE43_RESULT_PATH),
        "phase43_slot_ledger": {
            "input": f"$.slot_ledger['input|{base}']",
            "source_analytic": f"$.slot_ledger['source|{base}|analytic']",
            "reference_hessian_120": (
                f"$.slot_ledger['reference|{base}|dps=120|method=hessian']"
            ),
            "rounding_control_120": (
                f"$.slot_ledger['reference|{base}|dps=120|"
                "method=rounding_control']"
            ),
            "base_outcome": (
                f"$.base_outcomes[{slot.p43_base_outcome_index}]"
            ),
        },
        "phase42_checkpoint_artifact": relative_repo_path(CHECKPOINT_PATH),
        "phase42_checkpoint": {
            "linear_map": "$.fixed_metric.linear_map",
            "saddle_w": f"$.saddles.{slot.point}.saddle_w",
            "source_point": f"$.saddles.{slot.point}.source_point",
        },
        "phase41_source_artifact": relative_repo_path(PHASE41_PATH),
        "no_reconstructed_state_or_direction": True,
    }


def p44_slot_calculation(
    context: P44Context,
    slot: P44SlotInput,
    plan: P44CallablePlan,
    symbolic: P44NumericSymbolic,
    formula_mismatch_state: str,
    retention_state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(slot.disclosed_mismatch, bool) or not isinstance(
        slot.disclosed_phase42_anomaly, bool
    ):
        raise InvalidRun("Phase44 slot disclosure labels were not post-freeze joined")
    retention_state.clear()
    retention_state["stage"] = "source_boundaries"
    retention_state["attempted_parameters"] = {
        "point": slot.point,
        "fraction": slot.fraction,
        "direction": slot.direction,
    }
    retention_state["frozen_input"] = {
        "cohort": "disclosed_13" if slot.disclosed_mismatch else "control_77",
        "disclosed_phase42_anomaly": slot.disclosed_phase42_anomaly,
        "linear_map": binary64_payload(context.linear_map),
        "saddle_w": binary64_payload(context.points[slot.point].saddle_w),
        "xi": binary64_payload(slot.xi),
        "q": binary64_payload(slot.q),
        "stored_source": slot.source_binary64_identity,
        "record_paths": p44_frozen_record_paths(slot),
    }
    point = context.points[slot.point]
    boundaries = p44_source_boundaries(context, point, slot)
    retention_state["completed_source_boundaries"] = {
        "retained": boundaries["retained"],
        "source_paths": boundaries["source_paths"],
        "completed_operations": boundaries["completed_operations"],
        "source_operation_membership_sha256": boundaries[
            "source_operation_membership_sha256"
        ],
        "subnormal_boundary_names": boundaries["subnormal_boundary_names"],
        "all_source_boundaries_complete": True,
    }
    retention_state["stage"] = "independent_and_state_hessian"
    linear_map = mp_real_matrix_from_numpy(context.linear_map)
    saddle = [mp_complex_from_binary64(complex(value)) for value in point.saddle_w]
    xi = [mp_complex_from_binary64(complex(value)) for value in slot.xi]
    q = [mp_complex_from_binary64(complex(value)) for value in slot.q]
    w64_lift = [
        mp_complex_from_binary64(complex(value)) for value in boundaries["w64"]
    ]
    w_exact, w_radii, state_envelope = p44_state_formation_envelope(
        linear_map,
        saddle,
        xi,
        boundaries["u64"],
        boundaries["w64"],
    )
    h0 = matrix_mp(symbolic.exact_hessian_function(tuple(w_exact)), 7, 7)
    y0, s0 = p44_exact_hessian_action(linear_map, h0, q)
    h50 = matrix_mp(
        symbolic.rounding50_hessian_function(tuple(w_exact)), 7, 7
    )
    _y50, s50 = p44_exact_hessian_action(linear_map, h50, q)
    rounding50_stored_reproduction = p44_vector_metrics(
        s50, slot.rounding50_reference
    )
    rounding50_stored_reproduced = bool(
        mp.mpf(rounding50_stored_reproduction["symmetric_relative"])
        <= mp.mpf("1e-100")
        and mp.mpf(rounding50_stored_reproduction["max_component_relative"])
        <= mp.mpf("1e-100")
    )
    if not rounding50_stored_reproduced:
        raise InvalidRun(
            "Phase43 independent 50-decimal rounding-control reproduction drift"
        )
    h1 = p44_coefficient_hessian(plan, w_exact)
    y1, s1 = p44_exact_hessian_action(linear_map, h1, q)
    h_source50 = p44_coefficient_hessian(
        plan, w_exact, constant_mode="source_exact50"
    )
    _y_source50, s_source50 = p44_exact_hessian_action(
        linear_map, h_source50, q
    )
    source50_vs_independent50_hessian = p44_vector_metrics(
        [h_source50[row, column] for row in range(7) for column in range(7)],
        [h50[row, column] for row in range(7) for column in range(7)],
    )
    source50_vs_independent50_action = p44_vector_metrics(
        s_source50, s50
    )
    exact50_source_literal_bijection_passed = bool(
        plan.exact50_literal_mapping["all_49_entry_multisets_bijective"]
        is True
        and plan.exact50_literal_mapping[
            "replayable_from_pinned_source_hessian_and_generated_AST"
        ]
        is True
    )
    h2 = p44_coefficient_hessian(plan, w64_lift)
    y2, s2 = p44_exact_hessian_action(linear_map, h2, q)
    h2_trace, scalar_h_radii, observed_h_radii, trace = p44_evaluate_callable_plan(
        plan, boundaries["w64"], boundaries["H64"], h2
    )
    retention_state["completed_AST_trace"] = trace
    retention_state["stage"] = "post_trace_hybrid_and_envelopes"
    h2_trace_error = max(
        abs(h2_trace[row, column] - h2[row, column])
        for row in range(7)
        for column in range(7)
    )
    if h2_trace_error > mp.mpf("1e-100"):
        raise InvalidRun("AST coefficient semantics and exact evaluator diverged")
    h3 = p44_mp_complex_matrix_from_numpy(boundaries["H64"])
    y3, s3 = p44_exact_hessian_action(linear_map, h3, q)
    b1_lift = p44_mp_complex_matrix_from_numpy(boundaries["B1_64"])
    y4 = p44_matrix_vector(b1_lift * linear_map * p44_mp_column(q))
    s4 = p44_outer_action(y4)
    b2_lift = p44_mp_complex_matrix_from_numpy(boundaries["B2_64"])
    y5 = p44_matrix_vector(b2_lift * p44_mp_column(q))
    s5 = p44_outer_action(y5)
    y6 = [
        mp_complex_from_binary64(complex(value)) for value in boundaries["y64"]
    ]
    s6 = p44_outer_action(y6)
    s7 = [
        mp_complex_from_binary64(complex(value)) for value in boundaries["A64"]
    ]
    stage_vectors = {
        STAGE_IDS[0]: s0,
        STAGE_IDS[1]: s1,
        STAGE_IDS[2]: s2,
        STAGE_IDS[3]: s3,
        STAGE_IDS[4]: s4,
        STAGE_IDS[5]: s5,
        STAGE_IDS[6]: s6,
        STAGE_IDS[7]: s7,
    }
    stages, deltas, delta_vectors, telescope = p44_stage_and_delta_payload(
        stage_vectors,
        p44_stage_signed_zero_metadata(stage_vectors, boundaries),
    )
    retention_state["completed_hybrid_stages"] = stages
    retention_state["completed_hybrid_deltas"] = deltas
    retention_state["completed_telescope"] = telescope
    reference_metrics = p44_vector_metrics(s0, slot.reference)
    source_metric = mp_relative(s7, slot.reference)
    source_metric_reproduction = abs(source_metric - mp.mpf(slot.p43_relative_text))
    if source_metric_reproduction > mp.mpf("1e-100"):
        raise InvalidRun("Phase43 source/reference metric reproduction drift")
    independently_mismatch = source_metric > mp.mpf("5e-13")
    if independently_mismatch is not slot.disclosed_mismatch:
        raise InvalidRun("Phase43 5e-13 label reproduction drift")

    retention_state["stage"] = "forward_envelopes"
    completed_forward_envelopes: dict[str, Any] = {}
    retention_state["completed_forward_envelopes"] = (
        completed_forward_envelopes
    )
    retention_state["attempted_envelope_name"] = "coefficient"
    zero_w_radii = [mp.mpf("0") for _index in range(7)]
    coefficient_center, coefficient_h_radii, coefficient_disk_ok = (
        p44_coefficient_hessian_disk(
            plan,
            w_exact,
            zero_w_radii,
            include_constant_radii=True,
        )
    )
    if coefficient_disk_ok and max(
        abs(coefficient_center[row, column] - h1[row, column])
        for row in range(7)
        for column in range(7)
    ) > mp.mpf("1e-100"):
        raise InvalidRun("coefficient disk center drift")
    _coefficient_action_center, coefficient_action_radii = (
        p44_propagate_hessian_radii_to_action(
            linear_map, h1, coefficient_h_radii, q
        )
    )
    rounding50_residual = [
        s50[index] - s0[index]
        for index in range(7)
    ]
    source_exact50_residual = [
        s_source50[index] - s0[index] for index in range(7)
    ]
    source50_minus_independent50_diagnostic = [
        s_source50[index] - s50[index]
        for index in range(7)
    ]
    rounding50_relative = mp_relative(s50, s0)
    coefficient_combined_radii = [
        abs(source_exact50_residual[index]) + coefficient_action_radii[index]
        for index in range(7)
    ]
    coefficient_envelope = p44_envelope_check(
        delta_vectors["D_coeff"], coefficient_combined_radii
    )
    coefficient_envelope.update(
        {
            "independent_50_decimal_residual": mp_vector_payload(
                rounding50_residual, AUTHORITATIVE_DPS
            ),
            "independently_recomputed_50_decimal_value": mp_vector_payload(
                s50, AUTHORITATIVE_DPS
            ),
            "stored_phase43_50_decimal_value": mp_vector_payload(
                slot.rounding50_reference, AUTHORITATIVE_DPS
            ),
            "stored_phase43_50_decimal_reproduction": (
                rounding50_stored_reproduction
            ),
            "stored_phase43_50_decimal_reproduced_within_both_1e-100_metrics": (
                rounding50_stored_reproduced
            ),
            "source_exact50_minus_S0_residual_used_by_triangle": mp_vector_payload(
                source_exact50_residual, AUTHORITATIVE_DPS
            ),
            "source_exact50_minus_S0_magnitudes_used_by_triangle": [
                mp_number_string(abs(value), AUTHORITATIVE_DPS)
                for value in source_exact50_residual
            ],
            "source_exact50_semantics_value": mp_vector_payload(
                s_source50, AUTHORITATIVE_DPS
            ),
            "source_exact50_minus_independent_50_decimal_diagnostic": mp_vector_payload(
                source50_minus_independent50_diagnostic, AUTHORITATIVE_DPS
            ),
            "source_exact50_minus_independent_50_decimal_diagnostic_magnitudes_not_used_as_radius": [
                mp_number_string(abs(value), AUTHORITATIVE_DPS)
                for value in source50_minus_independent50_diagnostic
            ],
            "source_exact50_vs_independent_50_decimal_Hessian_diagnostic": (
                source50_vs_independent50_hessian
            ),
            "source_exact50_vs_independent_50_decimal_action_diagnostic": (
                source50_vs_independent50_action
            ),
            "source_exact50_literal_bijection_passed": (
                exact50_source_literal_bijection_passed
            ),
            "exact50_literal_bijection": plan.exact50_literal_mapping,
            "independent_50_decimal_relative": mp_number_string(
                rounding50_relative, AUTHORITATIVE_DPS
            ),
            "independent_50_decimal_control_passed": rounding50_relative
            <= mp.mpf("1e-40"),
            "constant_subtree_disk_complete": coefficient_disk_ok,
            "preregistered_rounding_disk_role": (
                "The source exact50 literal bijection anchors every generated "
                "constant-subtree ideal. Its direct S0 residual enters once, "
                "then only the fixed one/eight-ulp plus operation disk reaches "
                "binary64. The independent 50-decimal control and its difference "
                "from source exact50 are diagnostic and never enlarge radius."
            ),
            "conditional_on_formula_identity": True,
        }
    )
    completed_forward_envelopes["coefficient"] = coefficient_envelope

    retention_state["attempted_envelope_name"] = "state"
    state_center, state_h_radii, state_ast_disk_ok = p44_coefficient_hessian_disk(
        plan,
        w_exact,
        w_radii,
        include_constant_radii=False,
    )
    if state_ast_disk_ok and max(
        abs(state_center[row, column] - h1[row, column])
        for row in range(7)
        for column in range(7)
    ) > mp.mpf("1e-100"):
        raise InvalidRun("state disk center drift")
    _state_action_center, state_action_radii = p44_propagate_hessian_radii_to_action(
        linear_map, h1, state_h_radii, q
    )
    state_action_envelope = p44_envelope_check(
        delta_vectors["D_state"], state_action_radii
    )
    state_action_envelope["state_AST_disk_complete"] = state_ast_disk_ok
    state_action_envelope["u_and_w_bounds_passed"] = bool(
        state_envelope["u_all_covered"] and state_envelope["w_all_covered"]
        and state_envelope["w_add_local_all_covered"]
    )
    completed_forward_envelopes["state"] = state_action_envelope

    retention_state["attempted_envelope_name"] = "scalar_AST"
    _scalar_action_center, scalar_action_radii = p44_propagate_hessian_radii_to_action(
        linear_map, h2, scalar_h_radii, q
    )
    scalar_action_envelope = p44_envelope_check(
        delta_vectors["D_hessian"], scalar_action_radii
    )
    scalar_action_envelope["all_local_AST_models_passed"] = bool(
        trace["all_entry_models_ok"]
    )
    scalar_action_envelope["observed_H_radii"] = [
        [mp_number_string(value, AUTHORITATIVE_DPS) for value in row]
        for row in observed_h_radii
    ]
    completed_forward_envelopes["scalar_AST"] = scalar_action_envelope
    retention_state["attempted_envelope_name"] = (
        "scalar_AST_observed_accounting"
    )
    (
        _observed_scalar_action_center,
        observed_scalar_action_radii,
    ) = p44_propagate_hessian_radii_to_action(
        linear_map, h2, observed_h_radii, q
    )
    observed_scalar_action_envelope = p44_envelope_check(
        delta_vectors["D_hessian"], observed_scalar_action_radii
    )
    observed_scalar_action_envelope.update(
        {
            "all_49_observed_H64_errors_contained": trace[
                "all_observed_H64_errors_contained"
            ],
            "role": (
                "a_posteriori_accounting_only_not_prospective_coverage_"
                "predicate"
            ),
            "used_in_forward_error_coverage_classification": False,
        }
    )
    if not observed_scalar_action_envelope["covered"]:
        raise SlotEvaluationError(
            "observed scalar-AST action envelope failed to contain D_hessian",
            payload={
                "failure_scope": "AST_observed_residual_accounting",
                "completed_AST_trace": trace,
                "observed_scalar_action_envelope": (
                    observed_scalar_action_envelope
                ),
            },
        )
    completed_forward_envelopes["scalar_AST_observed_accounting"] = (
        observed_scalar_action_envelope
    )

    retention_state["attempted_envelope_name"] = "matmul_1"
    zero_matrix = p44_zero_radii(7, 7)
    zero_column = p44_zero_radii(7, 1)
    q_column = p44_mp_column(q)
    b1_center, b1_local_radii, b1_local = p44_mp_matmul_disk(
        linear_map.T,
        zero_matrix,
        h3,
        zero_matrix,
        operation_budget=56,
        observed_output=b1_lift,
    )
    b2_tail, b2_tail_radii, _ = p44_mp_matmul_disk(
        b1_center,
        b1_local_radii,
        linear_map,
        zero_matrix,
        operation_budget=None,
        observed_output=None,
    )
    _y_tail, y_tail_radii, _ = p44_mp_matmul_disk(
        b2_tail,
        b2_tail_radii,
        q_column,
        zero_column,
        operation_budget=None,
        observed_output=None,
    )
    matmul1_radii = [row[0] for row in y_tail_radii]
    matmul1_envelope = p44_envelope_check(
        delta_vectors["D_matmul_1"], matmul1_radii
    )
    matmul1_envelope["source_boundary"] = b1_local
    completed_forward_envelopes["matmul_1"] = matmul1_envelope

    retention_state["attempted_envelope_name"] = "matmul_2"
    b2_center, b2_local_radii, b2_local = p44_mp_matmul_disk(
        b1_lift,
        zero_matrix,
        linear_map,
        zero_matrix,
        operation_budget=56,
        observed_output=b2_lift,
    )
    _y_tail2, y_tail2_radii, _ = p44_mp_matmul_disk(
        b2_center,
        b2_local_radii,
        q_column,
        zero_column,
        operation_budget=None,
        observed_output=None,
    )
    matmul2_radii = [row[0] for row in y_tail2_radii]
    matmul2_envelope = p44_envelope_check(
        delta_vectors["D_matmul_2"], matmul2_radii
    )
    matmul2_envelope["source_boundary"] = b2_local
    completed_forward_envelopes["matmul_2"] = matmul2_envelope

    retention_state["attempted_envelope_name"] = "matvec"
    y6_column = p44_mp_column(y6)
    _y_center, y_local_radii, y_local = p44_mp_matmul_disk(
        b2_lift,
        zero_matrix,
        q_column,
        zero_column,
        operation_budget=56,
        observed_output=y6_column,
    )
    matvec_radii = [row[0] for row in y_local_radii]
    matvec_envelope = p44_envelope_check(
        delta_vectors["D_matvec"], matvec_radii
    )
    matvec_envelope["source_boundary"] = y_local
    completed_forward_envelopes["matvec"] = matvec_envelope
    retention_state["attempted_envelope_name"] = "outer"
    outer_envelope = p44_envelope_check(
        delta_vectors["D_outer"], [mp.mpf("0") for _index in range(7)]
    )
    completed_forward_envelopes["outer"] = outer_envelope

    retention_state["attempted_envelope_name"] = "total_source"
    total_h_radii = [
        [
            coefficient_h_radii[row][column]
            + state_h_radii[row][column]
            + scalar_h_radii[row][column]
            for column in range(7)
        ]
        for row in range(7)
    ]
    total_b1_center, total_b1_radii, total_b1 = p44_mp_matmul_disk(
        linear_map.T,
        zero_matrix,
        h3,
        total_h_radii,
        operation_budget=56,
        observed_output=b1_lift,
    )
    total_b2_center, total_b2_radii, total_b2 = p44_mp_matmul_disk(
        total_b1_center,
        total_b1_radii,
        linear_map,
        zero_matrix,
        operation_budget=56,
        observed_output=b2_lift,
    )
    _total_y_center, total_y_radii, total_y = p44_mp_matmul_disk(
        total_b2_center,
        total_b2_radii,
        q_column,
        zero_column,
        operation_budget=56,
        observed_output=y6_column,
    )
    total_radii = [
        total_y_radii[index][0] + abs(source_exact50_residual[index])
        for index in range(7)
    ]
    total_delta = [s7[index] - s0[index] for index in range(7)]
    total_envelope = p44_envelope_check(total_delta, total_radii)
    total_envelope["sequential_source_boundaries"] = {
        "B1": total_b1,
        "B2": total_b2,
        "y": total_y,
    }
    total_envelope["gamma56_kappa_used_as_bound"] = False
    total_envelope["three_sequential_gamma56_disks_used"] = True
    completed_forward_envelopes["total_source"] = total_envelope
    retention_state["attempted_envelope_name"] = None

    alternatives: dict[str, Any] = {}
    all_alternatives_complete = True
    retention_state["stage"] = "alternative_contractions"
    retention_state["completed_alternative_paths"] = []
    retention_state["completed_alternatives"] = alternatives
    for association in ASSOCIATIONS:
        for algorithm in SUMMATIONS:
            alternative_path = f"{association}|{algorithm}"
            retention_state["attempted_alternative_path"] = alternative_path
            expected_alternative_shape = p44_alternative_shape(
                association, algorithm
            )
            try:
                alternative = p44_alternative_contraction(
                    context.linear_map,
                    boundaries["H64"],
                    slot.q,
                    association,
                    algorithm,
                    retention_state=retention_state,
                )
            except SlotEvaluationError as exc:
                exception_details = dict(exc.payload)
                exception_details.setdefault(
                    "failure_scope", "alternative_post_contraction_metrics"
                )
                exception_details.setdefault(
                    "failed_node_key",
                    f"{alternative_path}/post_contraction_metrics",
                )
                exception_details.setdefault(
                    "failed_node_is_preenumerated", True
                )
                raise SlotEvaluationError(
                    str(exc),
                    payload={
                        "attempted_alternative_path": alternative_path,
                        "failed_alternative_path": alternative_path,
                        "completed_contraction": retention_state.get(
                            "attempted_alternative_completed_contraction"
                        ),
                        "alternative_failure_node_membership_sha256": (
                            expected_alternative_shape[
                                "failure_node_membership_sha256"
                            ]
                        ),
                        "smallest_exception_payload": dict(exc.payload),
                        **exception_details,
                    },
                ) from exc
            except Exception as exc:
                raise SlotEvaluationError(
                    (
                        "alternative post-contraction metrics failed for "
                        f"{alternative_path}: {type(exc).__name__}: {exc}"
                    ),
                    payload={
                        "failure_scope": "alternative_post_contraction_metrics",
                        "failed_alternative_path": alternative_path,
                        "failed_node_key": (
                            f"{alternative_path}/post_contraction_metrics"
                        ),
                        "failed_node_is_preenumerated": True,
                        "alternative_failure_node_membership_sha256": (
                            expected_alternative_shape[
                                "failure_node_membership_sha256"
                            ]
                        ),
                        "completed_contraction": retention_state.get(
                            "attempted_alternative_completed_contraction"
                        ),
                        "underlying_error_type": type(exc).__name__,
                        "underlying_error_message": str(exc)[:2048],
                    },
                ) from exc
            try:
                y_alt_array = alternative.pop("y_alt_array")
                a_alt_array = alternative.pop("A_alt_array")
                y_alt = [
                    mp_complex_from_binary64(complex(value))
                    for value in y_alt_array
                ]
                a_alt = [
                    mp_complex_from_binary64(complex(value))
                    for value in a_alt_array
                ]
                alternative["comparisons"] = {
                    "A_alt_to_S3": p44_vector_metrics(a_alt, s3),
                    "A_alt_to_S0": p44_vector_metrics(a_alt, s0),
                    "A_alt_to_S7": p44_vector_metrics(a_alt, s7),
                    "y_alt_to_pre_outer_S3": p44_vector_metrics(y_alt, y3),
                }
            except Exception as exc:
                raise SlotEvaluationError(
                    (
                        "alternative comparison failed for "
                        f"{alternative_path}: {type(exc).__name__}: {exc}"
                    ),
                    payload={
                        "failure_scope": "alternative_comparisons",
                        "failed_alternative_path": alternative_path,
                        "failed_node_key": f"{alternative_path}/comparisons",
                        "failed_node_is_preenumerated": True,
                        "alternative_failure_node_membership_sha256": (
                            expected_alternative_shape[
                                "failure_node_membership_sha256"
                            ]
                        ),
                        "completed_contraction": retention_state.get(
                            "attempted_alternative_completed_contraction"
                        ),
                        "completed_comparison_payload": alternative,
                        "underlying_error_type": type(exc).__name__,
                        "underlying_error_message": str(exc)[:2048],
                    },
                ) from exc
            alternatives[alternative_path] = alternative
            retention_state["attempted_alternative_completed_contraction"] = None
            retention_state["completed_alternative_paths"].append(
                alternative_path
            )
            retention_state["attempted_alternative_path"] = None
            all_alternatives_complete = bool(
                all_alternatives_complete and alternative["dot_count"] > 0
            )

    retention_state["stage"] = "conditioning_and_classification"
    conditioning = p44_conditioning_payload(
        linear_map,
        h3,
        q,
        y3,
        s1,
        s2,
        w_exact,
        w64_lift,
        {
            "linear_map": context.linear_map,
            "H64": boundaries["H64"],
            "B1_64": boundaries["B1_64"],
            "B2_64": boundaries["B2_64"],
            "q": slot.q,
        },
        retention_state=retention_state,
    )
    retention_state["completed_conditioning"] = conditioning
    retention_state["stage"] = "classification"
    floor = mp.mpf("1e-90")
    resolved = {
        delta_id: mp.mpf(deltas[delta_id]["resolved_delta_relative"])
        for delta_id in DELTA_IDS
    }
    formula_identity_established = formula_mismatch_state == "NOT_SUPPORTED"
    constant_trace_complete = bool(plan.constant_records) and all(
        int(record["trace"]["event_count"]) > 0
        and record["trace"]["terminal_status_histogram"]
        == {"SUCCESS": int(record["trace"]["event_count"])}
        for record in plan.constant_records.values()
    )
    state_boundary_complete = all(
        name in boundaries["retained"] for name in ("u64", "w64")
    )
    hessian_trace_complete = bool(trace["exact_trace_complete"])
    contraction_boundary_complete = all(
        name in boundaries["retained"]
        for name in ("B1_64", "B2_64", "y64", "A64")
    )
    coefficient_model_prerequisites = bool(
        formula_identity_established
        and constant_trace_complete
        and rounding50_stored_reproduced
        and rounding50_relative <= mp.mpf("1e-40")
        and exact50_source_literal_bijection_passed
        and coefficient_disk_ok
        and plan.constant_model_ok
    )
    total_prerequisites = bool(
        coefficient_model_prerequisites
        and state_ast_disk_ok
        and state_envelope["u_all_covered"]
        and state_envelope["w_all_covered"]
        and state_envelope["w_add_local_all_covered"]
        and trace["all_entry_models_ok"]
        and trace["trace_failure_count"] == 0
        and trace["subnormal_model_ambiguity"] is False
        and not boundaries["subnormal_boundary_names"]
        and b1_local["all_local_rounding_components_covered"]
        and b2_local["all_local_rounding_components_covered"]
        and y_local["all_local_rounding_components_covered"]
    )
    if not formula_identity_established or not constant_trace_complete:
        coefficient_state = "INCONCLUSIVE"
    else:
        coefficient_state = (
            "SUPPORTED" if resolved["D_coeff"] > floor else "NOT_SUPPORTED"
        )
    if not state_boundary_complete:
        state_state = "INCONCLUSIVE"
    else:
        state_state = "SUPPORTED" if resolved["D_state"] > floor else "NOT_SUPPORTED"
    if not hessian_trace_complete:
        hessian_state = "INCONCLUSIVE"
    else:
        hessian_state = (
            "SUPPORTED" if resolved["D_hessian"] > floor else "NOT_SUPPORTED"
        )
    if not contraction_boundary_complete:
        contraction_state = "INCONCLUSIVE"
    else:
        contraction_state = (
            "SUPPORTED"
            if any(
                resolved[key] > floor
                for key in ("D_matmul_1", "D_matmul_2", "D_matvec")
            )
            else "NOT_SUPPORTED"
        )
    cancellation_state = (
        "SUPPORTED"
        if conditioning["roundoff_risk_indicator"]["at_or_above_threshold"]
        else "NOT_SUPPORTED"
    )
    all_stage_envelopes_covered = all(
        envelope["covered"]
        for envelope in (
            coefficient_envelope,
            state_action_envelope,
            scalar_action_envelope,
            matmul1_envelope,
            matmul2_envelope,
            matvec_envelope,
            outer_envelope,
        )
    )
    all_sequential_propagated_boundaries_covered = bool(
        total_b1["all_propagated_components_covered"]
        and total_b2["all_propagated_components_covered"]
        and total_y["all_propagated_components_covered"]
    )
    if not total_prerequisites:
        coverage_state = "INCONCLUSIVE"
    else:
        coverage_state = (
            "SUPPORTED"
            if (
                total_envelope["covered"]
                and all_stage_envelopes_covered
                and all_sequential_propagated_boundaries_covered
            )
            else "NOT_SUPPORTED"
        )
    if not formula_identity_established or coverage_state == "INCONCLUSIVE":
        unresolved_state = "INCONCLUSIVE"
    elif coverage_state == "NOT_SUPPORTED":
        unresolved_state = "SUPPORTED"
    else:
        unresolved_state = "NOT_SUPPORTED"
    evidence = {
        "formula_mismatch": formula_mismatch_state,
        "coefficient_rounding": coefficient_state,
        "state_rounding": state_state,
        "hessian_rounding": hessian_state,
        "contraction_rounding": contraction_state,
        "cancellation_scale": cancellation_state,
        "forward_error_coverage": coverage_state,
        "unresolved_beyond_model": unresolved_state,
    }
    evidence_input_completion = {
        "formula_mismatch": formula_mismatch_state
        in ("SUPPORTED", "NOT_SUPPORTED"),
        "coefficient_rounding": constant_trace_complete,
        "state_rounding": state_boundary_complete,
        "hessian_rounding": hessian_trace_complete,
        "contraction_rounding": contraction_boundary_complete,
        "cancellation_scale": True,
        "forward_error_coverage": True,
        "unresolved_beyond_model": True,
    }
    if tuple(evidence) != EVIDENCE_KINDS or any(
        value not in ("SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE")
        for value in evidence.values()
    ):
        raise InvalidRun("slot nonexclusive tri-state ledger drift")
    if tuple(evidence_input_completion) != EVIDENCE_KINDS:
        raise InvalidRun("slot evidence-completion ledger drift")
    dependency_base = base_key(slot.point, slot.fraction, slot.direction)
    dependency_paths = p44_slot_dependency_paths(
        slot.point,
        dependency_base,
        tuple(plan.constant_records),
    )
    retention_state["completed_evidence"] = evidence
    retention_state["completed_evidence_input_completion"] = (
        evidence_input_completion
    )
    retention_state["completed_dependency_paths"] = dependency_paths
    closure_relative = mp.mpf(telescope["closure"]["relative"])
    closure_absolute = mp.mpf(telescope["closure"]["max_absolute"])
    source_raw_reproduced = p44_raw_equal(boundaries["A64"], slot.source)
    source_reproduced = bool(
        source_raw_reproduced
        and source_metric_reproduction <= mp.mpf("1e-100")
        and independently_mismatch is slot.disclosed_mismatch
    )
    trace_exact_complete = bool(
        trace["trace_failure_count"] == 0
        and trace["raw_bitwise_reproduction"] is True
        and trace["all_events_terminal_SUCCESS"] is True
        and trace["all_path_operation_commitments_complete"] is True
        and trace["exact_trace_complete"] is True
    )
    flags = {
        "reference_reproduced": bool(
            mp.mpf(reference_metrics["symmetric_relative"]) <= mp.mpf("1e-100")
            and mp.mpf(reference_metrics["max_component_relative"])
            <= mp.mpf("1e-100")
        ),
        "source_reproduced": source_reproduced,
        "source_raw_bitwise_reproduced": source_raw_reproduced,
        "rounding50_reproduced": rounding50_stored_reproduced,
        "trace_failure_count": int(trace["trace_failure_count"]),
        "trace_raw_bitwise_reproduction": bool(
            trace["raw_bitwise_reproduction"]
        ),
        "trace_all_events_terminal_SUCCESS": bool(
            trace["all_events_terminal_SUCCESS"]
        ),
        "trace_path_operation_commitments_complete": bool(
            trace["all_path_operation_commitments_complete"]
        ),
        "trace_exact_complete": trace_exact_complete,
        "mismatch_label_reproduced": independently_mismatch is slot.disclosed_mismatch,
        "telescope_closed": bool(
            closure_relative <= mp.mpf("1e-100")
            and closure_absolute <= mp.mpf("1e-100")
        ),
        "all_alternatives_complete": all_alternatives_complete,
        "classification_complete": True,
        "coverage_supported": coverage_state == "SUPPORTED",
        "coverage_state": coverage_state,
    }
    payload = {
        "point": slot.point,
        "fraction": slot.fraction,
        "direction": slot.direction,
        "cohort": "disclosed_13" if slot.disclosed_mismatch else "control_77",
        "disclosed_phase42_anomaly": slot.disclosed_phase42_anomaly,
        "input_identities": {
            "linear_map": binary64_payload(context.linear_map),
            "saddle_w": binary64_payload(point.saddle_w),
            "xi": binary64_payload(slot.xi),
            "q": binary64_payload(slot.q),
            "stored_source": slot.source_binary64_identity,
        },
        "frozen_record_paths": p44_frozen_record_paths(slot),
        "source_boundaries": boundaries["retained"],
        "source_operation_records": boundaries["completed_operations"],
        "source_operation_membership_sha256": boundaries[
            "source_operation_membership_sha256"
        ],
        "source_boundary_subnormal_model_ambiguity": {
            "present": bool(boundaries["subnormal_boundary_names"]),
            "boundary_names": boundaries["subnormal_boundary_names"],
        },
        "source_paths": boundaries["source_paths"],
        "AST_trace": trace,
        "hybrid_stages": stages,
        "hybrid_deltas": deltas,
        "telescope": telescope,
        "reference_reproduction": reference_metrics,
        "source_reference_reproduction": {
            "recomputed_relative": mp_number_string(source_metric, AUTHORITATIVE_DPS),
            "stored_phase43_relative": slot.p43_relative_text,
            "metric_reproduction_absolute": mp_number_string(
                source_metric_reproduction, AUTHORITATIVE_DPS
            ),
            "threshold": "5e-13",
            "independently_reconstructed_mismatch": independently_mismatch,
        },
        "state_formation_envelope": state_envelope,
        "forward_envelopes": {
            "coefficient": coefficient_envelope,
            "state": state_action_envelope,
            "scalar_AST": scalar_action_envelope,
            "matmul_1": matmul1_envelope,
            "matmul_2": matmul2_envelope,
            "matvec": matvec_envelope,
            "outer": outer_envelope,
            "total_source": total_envelope,
            "scalar_AST_observed_accounting": (
                observed_scalar_action_envelope
            ),
            "prerequisites": {
                "formula_identity_established": formula_identity_established,
                "constant_subtree_trace_complete": constant_trace_complete,
                "coefficient_contribution_classification_complete": bool(
                    constant_trace_complete
                ),
                "coefficient_model_prerequisites_passed": (
                    coefficient_model_prerequisites
                ),
                "source_exact50_literal_bijection_passed": (
                    exact50_source_literal_bijection_passed
                ),
                "fifty_decimal_control_passed": rounding50_relative
                <= mp.mpf("1e-40"),
                "literal_pi_sqrt_exp_division_power_basic_models_passed": bool(
                    plan.constant_model_ok
                    and trace["all_entry_models_ok"]
                    and trace["trace_failure_count"] == 0
                    and trace["subnormal_model_ambiguity"] is False
                ),
                "source_boundary_subnormal_model_ambiguity_absent": not bool(
                    boundaries["subnormal_boundary_names"]
                ),
                "state_bounds_passed": bool(
                    state_envelope["u_all_covered"]
                    and state_envelope["w_all_covered"]
                    and state_envelope["w_add_local_all_covered"]
                    and state_ast_disk_ok
                ),
                "three_source_contraction_local_bounds_passed": bool(
                    b1_local["all_local_rounding_components_covered"]
                    and b2_local["all_local_rounding_components_covered"]
                    and y_local["all_local_rounding_components_covered"]
                ),
                "all_total_prerequisites_passed": total_prerequisites,
                "all_declared_stage_envelopes_covered": all_stage_envelopes_covered,
                "all_sequential_propagated_boundaries_covered": (
                    all_sequential_propagated_boundaries_covered
                ),
            },
        },
        "alternative_contractions": alternatives,
        "conditioning": conditioning,
        "evidence": evidence,
        "evidence_input_completion": evidence_input_completion,
        "contribution_classification_separate_from_model_coverage": True,
        "dependency_paths": dependency_paths,
        "completion": "COMPLETE",
    }
    retention_state["stage"] = "slot_payload_complete"
    return payload, flags


def p44_trace_node_event_count(node: ast.AST, plan: P44CallablePlan) -> int:
    if id(node) in plan.constant_node_ids:
        return 1
    if isinstance(node, (ast.Constant, ast.Name)):
        return 1
    if isinstance(node, ast.BinOp):
        children = [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        children = [node.operand]
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        children = list(node.args)
    else:
        raise InvalidRun(f"trace event count structural drift: {type(node).__name__}")
    return 1 + sum(p44_trace_node_event_count(child, plan) for child in children)


def p44_trace_node_path_operations(
    node: ast.AST, plan: P44CallablePlan, path: str
) -> list[dict[str, str]]:
    if id(node) in plan.constant_node_ids:
        return [{"node_path": path, "operation": "constant_subtree_reuse"}]
    if isinstance(node, ast.Constant):
        operation_name = (
            "integer_literal" if isinstance(node.value, int) else "float_literal"
        )
        return [{"node_path": path, "operation": operation_name}]
    if isinstance(node, ast.Name):
        operation_name = "state_name" if node.id in plan.state_names else "numpy_pi"
        return [{"node_path": path, "operation": operation_name}]
    operation_name = p44_ast_operation(node)
    if isinstance(node, ast.BinOp):
        children = [node.left, node.right]
    elif isinstance(node, ast.UnaryOp):
        children = [node.operand]
    elif isinstance(node, ast.Call):
        children = list(node.args)
    else:
        raise InvalidRun("trace path-operation structural drift")
    output: list[dict[str, str]] = []
    for index, child in enumerate(children):
        output.extend(
            p44_trace_node_path_operations(child, plan, f"{path}/{index}")
        )
    output.append({"node_path": path, "operation": operation_name})
    return output


def p44_path_operation_commitment(records: Sequence[Mapping[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        encoded = canonical_json_bytes(
            {
                "node_path": str(record["node_path"]),
                "operation": str(record["operation"]),
            }
        )
        digest.update(len(encoded).to_bytes(8, "big", signed=False) + encoded)
    return digest.hexdigest()


def p44_plan_trace_shape(plan: P44CallablePlan) -> dict[str, Any]:
    per_entry = [
        [
            p44_trace_node_event_count(plan.entries[row][column], plan)
            for column in range(7)
        ]
        for row in range(7)
    ]
    scalar_events = sum(sum(row) for row in per_entry)
    structural_events = 10
    total = scalar_events + structural_events
    path_operations: list[dict[str, str]] = [
        {
            "node_path": "assign/tuple_unpack",
            "operation": "tuple_unpack_assign",
        }
    ]
    for row in range(7):
        for column in range(7):
            path_operations.extend(
                p44_trace_node_path_operations(
                    plan.entries[row][column], plan, f"entry={row},{column}"
                )
            )
        path_operations.append(
            {"node_path": f"return/list_row[{row}]", "operation": "list_constructor"}
        )
    path_operations.extend(
        [
            {"node_path": "return/list_outer", "operation": "list_constructor"},
            {"node_path": "return/array", "operation": "array_constructor"},
        ]
    )
    if len(path_operations) != total:
        raise InvalidRun("preenumerated trace path count drift")
    return {
        "per_entry_event_counts": per_entry,
        "scalar_event_count": scalar_events,
        "structural_event_count": structural_events,
        "whole_event_count": total,
        "chunk_size": 256,
        "chunk_count": (total + 255) // 256,
        "path_operation_commitment_sha256": p44_path_operation_commitment(
            path_operations
        ),
        "path_operation_records_retained_by_commitment": len(path_operations),
    }


def p44_ast_node_inventory(plan: P44CallablePlan) -> dict[str, Any]:
    stream = hashlib.sha256()
    chunk = hashlib.sha256()
    chunk_count = 0
    chunk_size = 256
    chunk_hashes: list[str] = []
    type_histogram: dict[str, int] = {}
    count = 0

    def visit(node: ast.AST, path: str) -> None:
        nonlocal chunk, chunk_count, count
        record = {
            "path": path,
            "node_type": type(node).__name__,
            "subtree_sha256": sha256_bytes(
                ast.dump(node, annotate_fields=True, include_attributes=False).encode(
                    "utf-8"
                )
            ),
        }
        encoded = canonical_json_bytes(record)
        framed = len(encoded).to_bytes(8, "big", signed=False) + encoded
        stream.update(framed)
        chunk.update(framed)
        chunk_count += 1
        count += 1
        type_histogram[record["node_type"]] = (
            type_histogram.get(record["node_type"], 0) + 1
        )
        if chunk_count == chunk_size:
            chunk_hashes.append(chunk.hexdigest())
            chunk = hashlib.sha256()
            chunk_count = 0
        for field_name, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                visit(value, f"{path}/{field_name}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    if isinstance(child, ast.AST):
                        visit(child, f"{path}/{field_name}[{index}]")

    visit(plan.tree, "Module")
    if chunk_count:
        chunk_hashes.append(chunk.hexdigest())
    return {
        "node_count": count,
        "chunk_size": chunk_size,
        "chunk_count": len(chunk_hashes),
        "chunk_sha256_in_fixed_order": chunk_hashes,
        "whole_inventory_sha256": stream.hexdigest(),
        "node_type_histogram": dict(sorted(type_histogram.items())),
        "node_paths_are_replayable_from_pinned_AST": True,
    }


def p44_sequence_commitment(records: Sequence[Mapping[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        encoded = canonical_json_bytes(dict(record))
        digest.update(len(encoded).to_bytes(8, "big", signed=False) + encoded)
    return digest.hexdigest()


def p44_alternative_shape(association: str, algorithm: str) -> dict[str, Any]:
    if association == "left_matrix_chain":
        stages = (("left/LT_H", 7, 7), ("left/B1_L", 7, 7), ("left/B2_q", 7, 1))
    elif association == "vector_first_chain":
        stages = (
            ("vector_first/L_q", 7, 1),
            ("vector_first/H_Lq", 7, 1),
            ("vector_first/LT_HLq", 7, 1),
        )
    else:
        raise InvalidRun("alternative shape association drift")
    internal_names = list(p44_dot_internal_node_names(algorithm))
    records: list[dict[str, Any]] = []
    failure_node_keys: list[str] = []
    dot_count = 0
    for stage, rows, columns in stages:
        for row in range(rows):
            for column in range(columns):
                dot_path = f"{stage}/dot[{row},{column}]"
                dot_count += 1
                for node_name in internal_names:
                    records.append({"dot_path": dot_path, "node": node_name})
                failure_node_keys.extend(
                    p44_dot_failure_node_keys(dot_path, algorithm)
                )
    failure_node_keys.extend(
        (
            f"{association}|{algorithm}/outer",
            f"{association}|{algorithm}/post_contraction_metrics",
            f"{association}|{algorithm}/comparisons",
        )
    )
    failure_records = [
        {"failed_node_key": key} for key in failure_node_keys
    ]
    return {
        "dot_count": dot_count,
        "internal_node_count": len(records),
        "internal_path_commitment_sha256": p44_sequence_commitment(records),
        "internal_node_names_per_dot": internal_names,
        "failure_node_count": len(failure_node_keys),
        "failure_node_keys_in_fixed_order": failure_node_keys,
        "failure_node_membership_sha256": p44_sequence_commitment(
            failure_records
        ),
    }


def p44_global_constant_subtree_records(
    plans: Mapping[str, P44CallablePlan]
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for point in TARGETS:
        for digest, record in plans[point].constant_records.items():
            existing = output.setdefault(
                digest,
                {
                    "normalized_subtree_sha256": digest,
                    "ast_dump": record["ast_dump"],
                    "source_lexeme": record["source_lexeme"],
                    "variant_records": {},
                    "complete_variant_occurrence_paths": [],
                },
            )
            if (
                existing["ast_dump"] != record["ast_dump"]
                or existing["source_lexeme"] != record["source_lexeme"]
            ):
                raise InvalidRun("global constant-subtree digest collision")
            existing["variant_records"][point] = record
            existing["complete_variant_occurrence_paths"].extend(
                f"point={point}/{path}" for path in record["occurrence_paths"]
            )
    for record in output.values():
        record["variant_count"] = len(record["variant_records"])
        record["occurrence_count"] = len(record["complete_variant_occurrence_paths"])
    return dict(sorted(output.items()))


def p44_preenumerate(
    ledger: SlotLedger, plans: Mapping[str, P44CallablePlan]
) -> dict[str, Any]:
    trace_shapes = {point: p44_plan_trace_shape(plans[point]) for point in TARGETS}
    inventories = {point: p44_ast_node_inventory(plans[point]) for point in TARGETS}
    alternative_shapes = {
        f"{association}|{algorithm}": p44_alternative_shape(association, algorithm)
        for association in ASSOCIATIONS
        for algorithm in SUMMATIONS
    }
    source_operation_shape = p44_source_operation_shape()
    global_constant_digests = sorted(
        {
            digest
            for point in TARGETS
            for digest in plans[point].constant_occurrences
        }
    )
    for point in TARGETS:
        ledger.declare(f"formula|point={point}|action", slot_kind="formula_action")
        for component in range(7):
            ledger.declare(
                f"formula|point={point}|gradient={component}",
                slot_kind="formula_gradient",
            )
        for row in range(7):
            for column in range(7):
                ledger.declare(
                    f"formula|point={point}|hessian={row},{column}",
                    slot_kind="formula_hessian",
                )
        ledger.declare(
            f"callable|point={point}|fingerprint", slot_kind="callable_fingerprint"
        )
        ledger.declare(
            f"callable|point={point}|AST_node_inventory",
            slot_kind="AST_node_inventory",
        )
        for digest in sorted(plans[point].constant_occurrences):
            ledger.declare(
                f"constant_subtree|point={point}|sha256={digest}",
                slot_kind="constant_subtree",
            )
    for digest in global_constant_digests:
        ledger.declare(
            f"constant_subtree_global|sha256={digest}",
            slot_kind="global_constant_subtree",
        )
    for point in TARGETS:
        trace_shape = trace_shapes[point]
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                base = base_key(point, fraction, direction)
                metadata = {
                    "point": point,
                    "fraction": fraction,
                    "direction": direction,
                }
                ledger.declare(f"input|{base}", slot_kind="frozen_input", **metadata)
                ledger.declare(
                    f"boundaries|{base}", slot_kind="source_boundaries", **metadata
                )
                ledger.declare(
                    f"trace|{base}|whole", slot_kind="AST_trace_whole", **metadata
                )
                for row in range(7):
                    for column in range(7):
                        ledger.declare(
                            f"trace|{base}|entry={row},{column}",
                            slot_kind="AST_trace_entry",
                            **metadata,
                        )
                for chunk_index in range(int(trace_shape["chunk_count"])):
                    ledger.declare(
                        f"trace|{base}|chunk={chunk_index}",
                        slot_kind="AST_trace_chunk",
                        **metadata,
                    )
                for stage_id in STAGE_IDS:
                    ledger.declare(
                        f"stage|{base}|{stage_id}",
                        slot_kind="hybrid_stage",
                        **metadata,
                    )
                for delta_id in DELTA_IDS:
                    ledger.declare(
                        f"delta|{base}|{delta_id}",
                        slot_kind="hybrid_delta",
                        **metadata,
                    )
                for association in ASSOCIATIONS:
                    for algorithm in SUMMATIONS:
                        ledger.declare(
                            f"alternative|{base}|{association}|{algorithm}",
                            slot_kind="alternative_contraction",
                            **metadata,
                        )
                for name in (
                    "expanded_component",
                    "source_dots",
                    "normwise_chain",
                    "state_secant",
                    "roundoff_risk",
                ):
                    ledger.declare(
                        f"conditioning|{base}|{name}",
                        slot_kind="conditioning",
                        **metadata,
                    )
                for name in (
                    "coefficient",
                    "state",
                    "scalar_AST",
                    "matmul_1",
                    "matmul_2",
                    "matvec",
                    "outer",
                    "total_source",
                    "scalar_AST_observed_accounting",
                ):
                    ledger.declare(
                        f"envelope|{base}|{name}",
                        slot_kind="forward_envelope",
                        **metadata,
                    )
                for evidence_kind in EVIDENCE_KINDS:
                    ledger.declare(
                        f"evidence|{base}|{evidence_kind}",
                        slot_kind="tri_state_evidence",
                        **metadata,
                    )
                ledger.declare(
                    f"slot|{base}|complete", slot_kind="base_slot", **metadata
                )
    scopes = [f"point={point}" for point in TARGETS] + [
        "global",
        "cohort=disclosed_13",
        "cohort=control_77",
    ]
    for scope in scopes:
        for evidence_kind in EVIDENCE_KINDS:
            for quantifier in ("existential_any", "universal_all"):
                ledger.declare(
                    f"aggregate|{scope}|{evidence_kind}|{quantifier}",
                    slot_kind="tri_state_aggregate",
                )
    for contract_id in EXACT_IDS + NUMERICAL_IDS:
        ledger.declare(f"contract|{contract_id}", slot_kind="contract")
    frozen_keys = tuple(ledger.slots)
    return {
        "declared_key_count": len(frozen_keys),
        "declared_keys_in_fixed_order": list(frozen_keys),
        "declared_keys_sha256": sha256_bytes(
            canonical_json_bytes({"keys": list(frozen_keys)})
        ),
        "trace_shapes_by_point": trace_shapes,
        "AST_node_inventories_by_point": inventories,
        "source_operation_shape": source_operation_shape,
        "alternative_internal_shapes": alternative_shapes,
        "global_constant_subtree_digests": global_constant_digests,
        "key_set_frozen_before_numerical_evaluation": True,
    }


def p44_finish_formula_and_plan_ledger(
    ledger: SlotLedger,
    formula: Mapping[str, Any],
    plans: Mapping[str, P44CallablePlan],
    preenumeration: Mapping[str, Any],
) -> dict[str, Any]:
    for point in TARGETS:
        point_formula = formula["by_point"][point]
        ledger.finish(
            f"formula|point={point}|action",
            "SUCCESS",
            payload=point_formula["action"],
        )
        for component in range(7):
            ledger.finish(
                f"formula|point={point}|gradient={component}",
                "SUCCESS",
                payload=point_formula["gradient"][component],
            )
        for row in range(7):
            for column in range(7):
                ledger.finish(
                    f"formula|point={point}|hessian={row},{column}",
                    "SUCCESS",
                    payload=point_formula["hessian"][row][column],
                )
        ledger.finish(
            f"callable|point={point}|fingerprint",
            "SUCCESS",
            payload=plans[point].fingerprint,
        )
        ledger.finish(
            f"callable|point={point}|AST_node_inventory",
            "SUCCESS",
            payload=preenumeration["AST_node_inventories_by_point"][point],
        )
        for digest, record in plans[point].constant_records.items():
            ledger.finish(
                f"constant_subtree|point={point}|sha256={digest}",
                "SUCCESS",
                payload=record,
            )
    global_constant_records = p44_global_constant_subtree_records(plans)
    if sorted(global_constant_records) != preenumeration[
        "global_constant_subtree_digests"
    ]:
        raise InvalidRun("global constant-subtree key drift after evaluation")
    for digest, record in global_constant_records.items():
        ledger.finish(
            f"constant_subtree_global|sha256={digest}",
            "SUCCESS",
            payload=record,
        )
    return global_constant_records


def p44_finish_base_slot_ledger(
    ledger: SlotLedger,
    payload: Mapping[str, Any],
    flags: dict[str, Any],
    trace_shape: Mapping[str, Any],
    alternative_shapes: Mapping[str, Any],
) -> None:
    base = base_key(
        str(payload["point"]), str(payload["fraction"]), int(payload["direction"])
    )
    trace = dict(payload["AST_trace"])
    entries = trace.pop("per_Hessian_entry")
    if int(trace["event_count"]) != int(trace_shape["whole_event_count"]):
        raise SlotEvaluationError(
            f"preenumerated trace event count drift: {base}",
            payload={
                "failure_scope": "AST_trace_retention_commitment",
                "completed_AST_trace": payload["AST_trace"],
            },
        )
    if len(trace["chunk_sha256_in_fixed_order"]) != int(
        trace_shape["chunk_count"]
    ):
        raise SlotEvaluationError(
            f"preenumerated trace chunk count drift: {base}",
            payload={
                "failure_scope": "AST_trace_retention_commitment",
                "completed_AST_trace": payload["AST_trace"],
            },
        )
    if trace["path_operation_commitment_sha256"] != trace_shape[
        "path_operation_commitment_sha256"
    ]:
        raise SlotEvaluationError(
            f"preenumerated trace path-operation drift: {base}",
            payload={
                "failure_scope": "AST_trace_retention_commitment",
                "completed_AST_trace": payload["AST_trace"],
            },
        )
    for row in range(7):
        for column in range(7):
            entry = entries[row][column]
            if int(entry["trace"]["event_count"]) != int(
                trace_shape["per_entry_event_counts"][row][column]
            ):
                raise SlotEvaluationError(
                    f"preenumerated entry trace count drift: {base}",
                    payload={
                        "failure_scope": "AST_trace_retention_commitment",
                        "completed_AST_trace": payload["AST_trace"],
                        "forced_failed_trace_entry": [row, column],
                    },
                )
    for association in ASSOCIATIONS:
        for algorithm in SUMMATIONS:
            path = f"{association}|{algorithm}"
            alternative = payload["alternative_contractions"][path]
            observed_internal_paths = [
                {"dot_path": dot["path"], "node": node["node"]}
                for dot in alternative["dot_records"]
                for node in dot["products_and_internal_nodes"]
            ]
            expected_shape = alternative_shapes[path]
            expected_gamma_ratio = p44_gamma_exact(
                {
                    "explicit_naive": 56,
                    "fixed_pairwise": 54,
                    "componentwise_kahan": 98,
                }[algorithm]
            )[1]
            dot_failure_memberships_match = all(
                dot.get("failure_node_membership_sha256")
                == p44_sequence_commitment(
                    [
                        {"failed_node_key": key}
                        for key in p44_dot_failure_node_keys(
                            str(dot["path"]), algorithm
                        )
                    ]
                )
                and dot.get("operation_budget")
                == {
                    "explicit_naive": 56,
                    "fixed_pairwise": 54,
                    "componentwise_kahan": 98,
                }[algorithm]
                and dot.get("gamma_exact_rational")
                == expected_gamma_ratio
                for dot in alternative["dot_records"]
            )
            chain = alternative["named_algorithm_chain_envelope"]
            if (
                alternative["dot_count"] != expected_shape["dot_count"]
                or len(observed_internal_paths)
                != expected_shape["internal_node_count"]
                or p44_sequence_commitment(observed_internal_paths)
                != expected_shape["internal_path_commitment_sha256"]
                or not dot_failure_memberships_match
                or chain.get("operation_budget")
                != {
                    "explicit_naive": 56,
                    "fixed_pairwise": 54,
                    "componentwise_kahan": 98,
                }[algorithm]
                or any(
                    chain[stage].get("gamma_exact_rational")
                    != expected_gamma_ratio
                    for stage in ("first", "second", "third")
                )
            ):
                raise SlotEvaluationError(
                    f"preenumerated alternative internal-path drift: {base}/{path}",
                    payload={
                        "failure_scope": (
                            "base_slot_alternative_retention_commitment"
                        ),
                        "failed_alternative_path": path,
                    },
                )
    if (
        tuple(payload["hybrid_stages"]) != STAGE_IDS
        or tuple(payload["hybrid_deltas"]) != DELTA_IDS
        or tuple(payload["alternative_contractions"])
        != tuple(
            f"{association}|{algorithm}"
            for association in ASSOCIATIONS
            for algorithm in SUMMATIONS
        )
        or tuple(payload["forward_envelopes"])
        != (
            "coefficient",
            "state",
            "scalar_AST",
            "matmul_1",
            "matmul_2",
            "matvec",
            "outer",
            "total_source",
            "scalar_AST_observed_accounting",
            "prerequisites",
        )
        or tuple(payload["evidence"]) != EVIDENCE_KINDS
        or tuple(payload["dependency_paths"]) != EVIDENCE_KINDS
        or any(
            payload["evidence"][kind]
            not in ("SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE")
            for kind in EVIDENCE_KINDS
        )
        or flags.get("classification_complete") is not True
    ):
        raise InvalidRun(f"atomic base-slot payload schema drift: {base}")
    required_conditioning = {
        "expanded_component_cancellation",
        "max_expanded_component_cancellation",
        "source_algebraic_dot_conditions",
        "source_dot_kappa_summary",
        "normwise_chain",
        "state_secant",
        "roundoff_risk_indicator",
    }
    if required_conditioning != set(payload["conditioning"]):
        raise InvalidRun(f"atomic conditioning payload incomplete: {base}")
    source_shape = p44_source_operation_shape()
    if (
        payload["source_operation_membership_sha256"]
        != source_shape["operation_commitment_sha256"]
        or len(payload["source_operation_records"])
        != source_shape["operation_count"]
        or payload["state_formation_envelope"]["unit_roundoff_exact_rational"]
        != [1, 2**53]
        or payload["state_formation_envelope"]["gamma1_exact_rational"]
        != p44_gamma_exact(1)[1]
        or payload["state_formation_envelope"]["gamma56_exact_rational"]
        != p44_gamma_exact(56)[1]
        or payload["forward_envelopes"]["prerequisites"].get(
            "source_exact50_literal_bijection_passed"
        )
        is not True
    ):
        raise InvalidRun(f"atomic fixed-math provenance drift: {base}")
    flags["fixed_hybrid_contract_validated"] = True
    flags["retention_schema_validated"] = True
    slot_payload_sha256 = sha256_bytes(canonical_json_bytes(payload))
    ledger.finish(
        f"input|{base}",
        "SUCCESS",
        payload={
            "cohort": payload["cohort"],
            "disclosed_phase42_anomaly": payload["disclosed_phase42_anomaly"],
            "identities": payload["input_identities"],
            "record_paths": payload["frozen_record_paths"],
        },
    )
    ledger.finish(
        f"boundaries|{base}",
        "SUCCESS",
        payload={
            "boundaries": payload["source_boundaries"],
            "paths": payload["source_paths"],
            "completed_operations": payload["source_operation_records"],
            "source_operation_membership_sha256": payload[
                "source_operation_membership_sha256"
            ],
            "all_source_boundaries_complete": True,
            "subnormal_model_ambiguity": payload[
                "source_boundary_subnormal_model_ambiguity"
            ],
        },
    )
    ledger.finish(f"trace|{base}|whole", "SUCCESS", payload=trace)
    for row in range(7):
        for column in range(7):
            entry = entries[row][column]
            ledger.finish(
                f"trace|{base}|entry={row},{column}",
                "SUCCESS",
                payload=entry,
            )
    for index, digest in enumerate(trace["chunk_sha256_in_fixed_order"]):
        ledger.finish(
            f"trace|{base}|chunk={index}",
            "SUCCESS",
            payload={"chunk_index": index, "sha256": digest, "chunk_size": 256},
        )
    for stage_id in STAGE_IDS:
        ledger.finish(
            f"stage|{base}|{stage_id}",
            "SUCCESS",
            payload=payload["hybrid_stages"][stage_id],
        )
    for delta_id in DELTA_IDS:
        ledger.finish(
            f"delta|{base}|{delta_id}",
            "SUCCESS",
            payload=payload["hybrid_deltas"][delta_id],
        )
    for association in ASSOCIATIONS:
        for algorithm in SUMMATIONS:
            path = f"{association}|{algorithm}"
            alternative = payload["alternative_contractions"][path]
            ledger.finish(
                f"alternative|{base}|{association}|{algorithm}",
                "SUCCESS",
                payload={
                    "path": path,
                    "payload_sha256": sha256_bytes(canonical_json_bytes(alternative)),
                    "dot_count": alternative["dot_count"],
                    "dot_kappa_summary": alternative["dot_kappa_summary"],
                    "y_alt": alternative["y_alt"],
                    "A_alt": alternative["A_alt"],
                    "comparisons": alternative["comparisons"],
                    "named_algorithm_chain_envelope": alternative[
                        "named_algorithm_chain_envelope"
                    ],
                    "full_payload_path": f"slot_records.{base}.alternative_contractions.{path}",
                },
            )
    conditioning = payload["conditioning"]
    condition_payloads = {
        "expanded_component": {
            "values": conditioning["expanded_component_cancellation"],
            "maximum": conditioning["max_expanded_component_cancellation"],
        },
        "source_dots": {
            "records": conditioning["source_algebraic_dot_conditions"],
            "summary": conditioning["source_dot_kappa_summary"],
        },
        "normwise_chain": conditioning["normwise_chain"],
        "state_secant": conditioning["state_secant"],
        "roundoff_risk": conditioning["roundoff_risk_indicator"],
    }
    for name, value in condition_payloads.items():
        ledger.finish(f"conditioning|{base}|{name}", "SUCCESS", payload=value)
    for name in (
        "coefficient",
        "state",
        "scalar_AST",
        "matmul_1",
        "matmul_2",
        "matvec",
        "outer",
        "total_source",
        "scalar_AST_observed_accounting",
    ):
        ledger.finish(
            f"envelope|{base}|{name}",
            "SUCCESS",
            payload=payload["forward_envelopes"][name],
        )
    for evidence_kind in EVIDENCE_KINDS:
        ledger.finish(
            f"evidence|{base}|{evidence_kind}",
            "SUCCESS",
            payload={
                "state": payload["evidence"][evidence_kind],
                "input_completion": payload["evidence_input_completion"][
                    evidence_kind
                ],
                "dependency_path": payload["dependency_paths"][evidence_kind],
                "nonexclusive": True,
            },
        )
    ledger.finish(
        f"slot|{base}|complete",
        "SUCCESS",
        payload={
            "payload_sha256": slot_payload_sha256,
            "full_payload_path": f"slot_records.{base}",
            "flags": dict(flags),
        },
    )


def p44_existential_state(states: Sequence[str]) -> str:
    if any(state == "SUPPORTED" for state in states):
        return "SUPPORTED"
    if all(state == "NOT_SUPPORTED" for state in states):
        return "NOT_SUPPORTED"
    return "INCONCLUSIVE"


def p44_universal_state(states: Sequence[str]) -> str:
    if all(state == "SUPPORTED" for state in states):
        return "SUPPORTED"
    if any(state == "NOT_SUPPORTED" for state in states):
        return "NOT_SUPPORTED"
    return "INCONCLUSIVE"


def p44_aggregate_and_finish(
    ledger: SlotLedger,
    slot_records: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    records = list(slot_records.values())
    if len(records) != 90:
        raise InvalidRun("aggregate base-slot cardinality drift")
    scoped: dict[str, list[Mapping[str, Any]]] = {
        **{
            f"point={point}": [record for record in records if record["point"] == point]
            for point in TARGETS
        },
        "global": records,
        "cohort=disclosed_13": [
            record for record in records if record["cohort"] == "disclosed_13"
        ],
        "cohort=control_77": [
            record for record in records if record["cohort"] == "control_77"
        ],
    }
    expected_counts = {
        "point=shared_zero": 30,
        "point=phi_plus": 30,
        "point=a_plus": 30,
        "global": 90,
        "cohort=disclosed_13": 13,
        "cohort=control_77": 77,
    }
    output: dict[str, Any] = {}
    for scope, scope_records in scoped.items():
        if len(scope_records) != expected_counts[scope]:
            raise InvalidRun(f"aggregate scope cardinality drift: {scope}")
        evidence_output: dict[str, Any] = {}
        for evidence_kind in EVIDENCE_KINDS:
            states = [str(record["evidence"][evidence_kind]) for record in scope_records]
            existential = p44_existential_state(states)
            universal = p44_universal_state(states)
            histogram = {
                state: states.count(state)
                for state in ("SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE")
            }
            member_dependency_paths = [
                f"evidence|{base_key(str(record['point']), str(record['fraction']), int(record['direction']))}|{evidence_kind}"
                for record in scope_records
            ]
            evidence_output[evidence_kind] = {
                "existential_any": existential,
                "universal_all": universal,
                "state_histogram": histogram,
                "slot_count": len(states),
            }
            for quantifier, state in (
                ("existential_any", existential),
                ("universal_all", universal),
            ):
                ledger.finish(
                    f"aggregate|{scope}|{evidence_kind}|{quantifier}",
                    "SUCCESS",
                    payload={
                        "scope": scope,
                        "evidence_kind": evidence_kind,
                        "quantifier": quantifier,
                        "state": state,
                        "state_histogram": histogram,
                        "slot_count": len(states),
                        "dependency_path": member_dependency_paths,
                    },
                )
        output[scope] = evidence_output
    output["cohort_protocol"] = {
        "ALL_13_WITHIN_DECLARED_FORWARD_ERROR_MODEL": output[
            "cohort=disclosed_13"
        ]["forward_error_coverage"]["universal_all"],
        "ALL_77_WITHIN_DECLARED_FORWARD_ERROR_MODEL": output[
            "cohort=control_77"
        ]["forward_error_coverage"]["universal_all"],
        "same_rules_applied_without_selection": True,
    }
    return output


def p44_validate_dependency_ledger(ledger: SlotLedger) -> dict[str, Any]:
    graph: dict[str, list[str]] = {}
    edge_count = 0
    for key, record in ledger.slots.items():
        if record["metadata"]["slot_kind"] not in (
            "tri_state_evidence",
            "tri_state_aggregate",
        ):
            continue
        if record["terminal_status"] != "SUCCESS":
            raise InvalidRun(f"evidence dependency source is not SUCCESS: {key}")
        payload = record["payload"]
        if not isinstance(payload, dict) or not isinstance(
            payload.get("dependency_path"), list
        ):
            raise InvalidRun(f"evidence dependency path missing: {key}")
        dependencies = [str(value) for value in payload["dependency_path"]]
        if len(dependencies) != len(set(dependencies)):
            raise InvalidRun(f"duplicate evidence dependency edge: {key}")
        slot_kind = record["metadata"]["slot_kind"]
        if slot_kind == "tri_state_evidence":
            evidence_kind = key.rsplit("|", 1)[1]
            metadata = record["metadata"]
            point = str(metadata["point"])
            base = base_key(
                point,
                str(metadata["fraction"]),
                int(metadata["direction"]),
            )
            constant_digests = [
                candidate.rsplit("=", 1)[1]
                for candidate in ledger.slots
                if candidate.startswith(
                    f"constant_subtree|point={point}|sha256="
                )
            ]
            expected_dependencies = p44_slot_dependency_paths(
                point, base, constant_digests
            )[evidence_kind]
            if dependencies != expected_dependencies:
                raise InvalidRun(
                    f"noncanonical slot evidence dependencies: {key}"
                )
        else:
            parts = key.split("|")
            if len(parts) != 4:
                raise InvalidRun(f"aggregate dependency key drift: {key}")
            scope, evidence_kind = parts[1], parts[2]
            expected_dependencies = []
            for candidate, candidate_record in ledger.slots.items():
                if (
                    candidate_record["metadata"]["slot_kind"]
                    != "tri_state_evidence"
                    or candidate.rsplit("|", 1)[1] != evidence_kind
                ):
                    continue
                candidate_metadata = candidate_record["metadata"]
                candidate_point = str(candidate_metadata["point"])
                candidate_base = base_key(
                    candidate_point,
                    str(candidate_metadata["fraction"]),
                    int(candidate_metadata["direction"]),
                )
                if scope.startswith("point="):
                    member = candidate_point == scope.removeprefix("point=")
                elif scope == "global":
                    member = True
                elif scope.startswith("cohort="):
                    input_record = ledger.slots[f"input|{candidate_base}"]
                    input_payload = input_record.get("payload")
                    member = bool(
                        isinstance(input_payload, dict)
                        and input_payload.get("cohort")
                        == scope.removeprefix("cohort=")
                    )
                else:
                    raise InvalidRun(f"undeclared aggregate scope: {scope}")
                if member:
                    expected_dependencies.append(candidate)
            if dependencies != expected_dependencies:
                raise InvalidRun(
                    f"noncanonical aggregate dependencies: {key}"
                )
        for dependency in dependencies:
            target = ledger.slots.get(dependency)
            if target is None:
                raise InvalidRun(f"dangling evidence dependency: {key} -> {dependency}")
            if target["terminal_status"] != "SUCCESS":
                raise InvalidRun(
                    f"nonterminal evidence dependency: {key} -> {dependency}"
                )
        graph[key] = dependencies
        edge_count += len(dependencies)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(key: str) -> None:
        if key in visited:
            return
        if key in visiting:
            raise InvalidRun(f"cyclic evidence dependency graph at {key}")
        visiting.add(key)
        for dependency in graph.get(key, []):
            if dependency in graph:
                visit(dependency)
        visiting.remove(key)
        visited.add(key)

    for key in graph:
        visit(key)
    return {
        "evidence_node_count": len(graph),
        "dependency_edge_count": edge_count,
        "all_targets_declared_and_successful": True,
        "canonical_paths_match_classification_and_aggregate_semantics": True,
        "acyclic": True,
    }


def p44_terminalize_failed_base_slot(
    ledger: SlotLedger,
    base: str,
    exc: SlotEvaluationError,
    trace_shape: Mapping[str, Any] | None = None,
) -> None:
    reason = f"{type(exc).__name__}: {exc}"[:4096]
    exception_payload = dict(exc.payload)
    failure_scope = str(exception_payload.get("failure_scope", ""))
    failed_node_key = exception_payload.get("failed_node_key")
    exception_node_membership: dict[str, Any] | None = None
    if isinstance(failed_node_key, str) and failed_node_key:
        if failure_scope == "source_boundary_operation":
            expected_source_shape = p44_source_operation_shape()
            exception_node_membership = {
                "failed_node_key": failed_node_key,
                "membership_scope": "source_operation_shape",
                "expected_membership_sha256": expected_source_shape[
                    "failure_node_membership_sha256"
                ],
                "reported_membership_sha256": exception_payload.get(
                    "preenumerated_failure_node_membership_sha256"
                ),
                "failed_node_is_preenumerated": failed_node_key
                in expected_source_shape["failure_node_keys_in_fixed_order"],
            }
        else:
            attempted_path = exception_payload.get("attempted_alternative_path")
            if not isinstance(attempted_path, str) or "|" not in attempted_path:
                attempted_path = exception_payload.get("failed_alternative_path")
            if isinstance(attempted_path, str) and "|" in attempted_path:
                association, algorithm = attempted_path.split("|", 1)
                expected_alternative_shape = p44_alternative_shape(
                    association, algorithm
                )
                exception_node_membership = {
                    "failed_node_key": failed_node_key,
                    "membership_scope": "alternative_failure_node_shape",
                    "expected_membership_sha256": expected_alternative_shape[
                        "failure_node_membership_sha256"
                    ],
                    "reported_membership_sha256": exception_payload.get(
                        "alternative_failure_node_membership_sha256"
                    ),
                    "failed_node_is_preenumerated": failed_node_key
                    in expected_alternative_shape[
                        "failure_node_keys_in_fixed_order"
                    ],
                }
        if exception_node_membership is not None:
            exception_node_membership["membership_commitment_matches"] = bool(
                exception_node_membership["reported_membership_sha256"]
                == exception_node_membership["expected_membership_sha256"]
            )
            exception_payload["exception_node_membership_validation"] = (
                exception_node_membership
            )
    trace_failed = failure_scope in {
        "AST_trace_path_commitment",
        "AST_H64_raw_identity",
        "AST_trace_arithmetic",
        "AST_trace_retention_commitment",
    }
    completed_success_trace = exception_payload.get("completed_AST_trace")
    forced_failed_trace_entry = exception_payload.get(
        "forced_failed_trace_entry"
    )
    input_key = f"input|{base}"
    if (
        isinstance(exception_payload.get("frozen_input"), dict)
        and input_key in ledger.slots
        and ledger.slots[input_key]["terminal_status"] is None
    ):
        ledger.finish(
            input_key,
            "SUCCESS",
            payload=exception_payload["frozen_input"],
        )
    boundary_key = f"boundaries|{base}"
    if (
        isinstance(exception_payload.get("completed_source_boundaries"), dict)
        and boundary_key in ledger.slots
        and ledger.slots[boundary_key]["terminal_status"] is None
    ):
        boundary_complete = bool(
            exception_payload["completed_source_boundaries"].get(
                "all_source_boundaries_complete"
            )
        )
        ledger.finish(
            boundary_key,
            "SUCCESS" if boundary_complete else "EVALUATION_FAILED",
            payload={
                **exception_payload["completed_source_boundaries"],
                "exception_node_membership_validation": (
                    exception_node_membership
                ),
            },
            error=None if boundary_complete else reason,
        )
    completed_whole: Mapping[str, Any] | None = None
    completed_entries: Any = None
    if isinstance(completed_success_trace, dict):
        completed_whole = completed_success_trace
        completed_entries = completed_success_trace.get("per_Hessian_entry")
    full_trace = exception_payload.get("completed_whole_and_per_entry_trace")
    if completed_whole is None and isinstance(full_trace, dict):
        completed_whole = full_trace
        completed_entries = full_trace.get("per_Hessian_entry")
    elif completed_whole is None and isinstance(
        exception_payload.get("completed_whole_trace"), dict
    ):
        completed_whole = exception_payload["completed_whole_trace"]
        completed_entries = exception_payload.get(
            "completed_per_Hessian_entry_summaries",
            exception_payload.get("completed_per_Hessian_entry_traces"),
        )

    if isinstance(completed_entries, list) and len(completed_entries) == 7:
        for row in range(7):
            if not isinstance(completed_entries[row], list) or len(
                completed_entries[row]
            ) != 7:
                break
            for column in range(7):
                entry_payload = completed_entries[row][column]
                trace_payload = (
                    entry_payload.get("trace")
                    if isinstance(entry_payload, dict)
                    and isinstance(entry_payload.get("trace"), dict)
                    else entry_payload
                )
                if not isinstance(trace_payload, dict):
                    continue
                histogram = trace_payload.get("terminal_status_histogram", {})
                entry_success = bool(
                    isinstance(histogram, dict)
                    and histogram
                    and set(histogram) == {"SUCCESS"}
                    and forced_failed_trace_entry != [row, column]
                )
                entry_key = f"trace|{base}|entry={row},{column}"
                if ledger.slots[entry_key]["terminal_status"] is None:
                    ledger.finish(
                        entry_key,
                        "SUCCESS" if entry_success else "EVALUATION_FAILED",
                        payload=entry_payload,
                        error=None if entry_success else reason,
                    )
    else:
        failed_entry = exception_payload.get("entry")
        partial_entry = exception_payload.get("completed_entry_trace")
        if (
            isinstance(failed_entry, list)
            and len(failed_entry) == 2
            and isinstance(partial_entry, dict)
        ):
            entry_key = (
                f"trace|{base}|entry={int(failed_entry[0])},"
                f"{int(failed_entry[1])}"
            )
            if ledger.slots[entry_key]["terminal_status"] is None:
                ledger.finish(
                    entry_key,
                    "EVALUATION_FAILED",
                    payload={
                        "partial_trace": partial_entry,
                        "expected_path_operations": exception_payload.get(
                            "expected_path_operations"
                        ),
                        "observed_path_operations": exception_payload.get(
                            "observed_path_operations"
                        ),
                    },
                    error=reason,
                )

    if completed_whole is not None and trace_shape is not None:
        hashes = completed_whole.get("chunk_sha256_in_fixed_order")
        full_chunk_commitment = bool(
            completed_whole.get("event_count")
            == trace_shape.get("whole_event_count")
            and isinstance(hashes, list)
            and len(hashes) == trace_shape.get("chunk_count")
        )
        if full_chunk_commitment:
            for index, digest in enumerate(hashes):
                chunk_key = f"trace|{base}|chunk={index}"
                if ledger.slots[chunk_key]["terminal_status"] is None:
                    ledger.finish(
                        chunk_key,
                        "SUCCESS",
                        payload={
                            "chunk_index": index,
                            "sha256": digest,
                            "chunk_size": 256,
                            "whole_trace_terminal_status": (
                                "EVALUATION_FAILED" if trace_failed else "SUCCESS"
                            ),
                        },
                    )
    trace_key = f"trace|{base}|whole"
    if (
        completed_whole is not None
        and trace_key in ledger.slots
        and ledger.slots[trace_key]["terminal_status"] is None
    ):
        ledger.finish(
            trace_key,
            "EVALUATION_FAILED" if trace_failed else "SUCCESS",
            payload={
                "smallest_exception_payload": exception_payload,
                "completed_whole_trace": completed_whole,
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:2048],
            },
            error=reason if trace_failed else None,
        )

    completed_stages = exception_payload.get("completed_hybrid_stages")
    if isinstance(completed_stages, dict):
        for stage_id in STAGE_IDS:
            key = f"stage|{base}|{stage_id}"
            if (
                stage_id in completed_stages
                and key in ledger.slots
                and ledger.slots[key]["terminal_status"] is None
            ):
                ledger.finish(key, "SUCCESS", payload=completed_stages[stage_id])
    completed_deltas = exception_payload.get("completed_hybrid_deltas")
    if isinstance(completed_deltas, dict):
        for delta_id in DELTA_IDS:
            key = f"delta|{base}|{delta_id}"
            if (
                delta_id in completed_deltas
                and key in ledger.slots
                and ledger.slots[key]["terminal_status"] is None
            ):
                ledger.finish(key, "SUCCESS", payload=completed_deltas[delta_id])
    completed_envelopes = exception_payload.get("completed_forward_envelopes")
    if isinstance(completed_envelopes, dict):
        for name, payload in completed_envelopes.items():
            key = f"envelope|{base}|{name}"
            if key in ledger.slots and ledger.slots[key]["terminal_status"] is None:
                ledger.finish(key, "SUCCESS", payload=payload)
    if failure_scope == "AST_observed_residual_accounting":
        observed_key = f"envelope|{base}|scalar_AST_observed_accounting"
        if (
            observed_key in ledger.slots
            and ledger.slots[observed_key]["terminal_status"] is None
        ):
            ledger.finish(
                observed_key,
                "EVALUATION_FAILED",
                payload={
                    "observed_scalar_action_envelope": exception_payload.get(
                        "observed_scalar_action_envelope"
                    ),
                    "all_observed_H64_errors_contained": exception_payload.get(
                        "all_observed_H64_errors_contained"
                    ),
                    "completed_AST_trace": exception_payload.get(
                        "completed_AST_trace",
                        exception_payload.get(
                            "completed_whole_and_per_entry_trace"
                        ),
                    ),
                    "smallest_exception_payload": exception_payload,
                },
                error=reason,
            )
    attempted_envelope = exception_payload.get("attempted_envelope_name")
    if isinstance(attempted_envelope, str) and attempted_envelope:
        attempted_envelope_key = f"envelope|{base}|{attempted_envelope}"
        if (
            attempted_envelope_key in ledger.slots
            and ledger.slots[attempted_envelope_key]["terminal_status"] is None
        ):
            ledger.finish(
                attempted_envelope_key,
                "EVALUATION_FAILED",
                payload={
                    "attempted_envelope_name": attempted_envelope,
                    "smallest_exception_payload": exception_payload,
                },
                error=reason,
            )
    completed_alternatives = exception_payload.get("completed_alternatives")
    forced_failed_alternative = exception_payload.get(
        "failed_alternative_path"
    )
    if isinstance(completed_alternatives, dict):
        for path, alternative in completed_alternatives.items():
            if not isinstance(alternative, dict) or "|" not in str(path):
                continue
            association, algorithm = str(path).split("|", 1)
            key = f"alternative|{base}|{association}|{algorithm}"
            if key not in ledger.slots or ledger.slots[key]["terminal_status"] is not None:
                continue
            try:
                expected_shape = p44_alternative_shape(association, algorithm)
                observed_internal_paths = [
                    {"dot_path": dot["path"], "node": node["node"]}
                    for dot in alternative["dot_records"]
                    for node in dot["products_and_internal_nodes"]
                ]
                complete = bool(
                    str(path) != forced_failed_alternative
                    and
                    alternative["dot_count"] == expected_shape["dot_count"]
                    and len(observed_internal_paths)
                    == expected_shape["internal_node_count"]
                    and p44_sequence_commitment(observed_internal_paths)
                    == expected_shape["internal_path_commitment_sha256"]
                )
            except Exception:
                complete = False
            ledger.finish(
                key,
                "SUCCESS" if complete else "EVALUATION_FAILED",
                payload={
                    "path": path,
                    "completed_before_downstream_failure": True,
                    "full_payload": alternative,
                },
                error=None if complete else reason,
            )
    attempted_alternative = exception_payload.get("attempted_alternative_path")
    if (
        isinstance(attempted_alternative, str)
        and attempted_alternative
        and (
            not isinstance(completed_alternatives, dict)
            or attempted_alternative not in completed_alternatives
        )
        and "|" in attempted_alternative
    ):
        association, algorithm = attempted_alternative.split("|", 1)
        key = f"alternative|{base}|{association}|{algorithm}"
        if key in ledger.slots and ledger.slots[key]["terminal_status"] is None:
            completed_contraction = exception_payload.get(
                "completed_contraction",
                exception_payload.get(
                    "attempted_alternative_completed_contraction"
                ),
            )
            if not isinstance(completed_contraction, dict):
                completed_contraction = {}
            ledger.finish(
                key,
                "EVALUATION_FAILED",
                payload={
                    "path": attempted_alternative,
                    "attempted_but_not_completed": True,
                    "failure_scope": failure_scope,
                    "failed_node_key": exception_payload.get(
                        "failed_node_key"
                    ),
                    "failed_matmul_stage": exception_payload.get(
                        "failed_matmul_stage"
                    ),
                    "completed_dot_records": exception_payload.get(
                        "completed_dot_records",
                        completed_contraction.get("completed_dot_records", []),
                    ),
                    "completed_internal_records_in_failed_dot": (
                        exception_payload.get("completed_internal_records", [])
                    ),
                    "completed_intermediates": exception_payload.get(
                        "completed_intermediates",
                        completed_contraction.get("completed_intermediates", {}),
                    ),
                    "completed_contraction_checkpoint": completed_contraction,
                    "preenumerated_membership_sha256": (
                        exception_payload.get(
                            "alternative_internal_membership_sha256"
                        )
                    ),
                    "exception_node_membership_validation": (
                        exception_node_membership
                    ),
                    "smallest_exception_payload": exception_payload,
                },
                error=reason,
            )
    completed_conditioning = exception_payload.get("completed_conditioning")
    if isinstance(completed_conditioning, dict):
        conditioning_payloads: dict[str, Any] = {}
        if {
            "expanded_component_cancellation",
            "max_expanded_component_cancellation",
        }.issubset(completed_conditioning):
            conditioning_payloads["expanded_component"] = {
                "values": completed_conditioning.get(
                    "expanded_component_cancellation"
                ),
                "maximum": completed_conditioning.get(
                    "max_expanded_component_cancellation"
                ),
            }
        if {
            "source_algebraic_dot_conditions",
            "source_dot_kappa_summary",
        }.issubset(completed_conditioning):
            conditioning_payloads["source_dots"] = {
                "records": completed_conditioning.get(
                    "source_algebraic_dot_conditions"
                ),
                "summary": completed_conditioning.get(
                    "source_dot_kappa_summary"
                ),
            }
        for name, source_name in (
            ("normwise_chain", "normwise_chain"),
            ("state_secant", "state_secant"),
            ("roundoff_risk", "roundoff_risk_indicator"),
        ):
            if source_name in completed_conditioning:
                conditioning_payloads[name] = completed_conditioning[source_name]
        for name, payload in conditioning_payloads.items():
            key = f"conditioning|{base}|{name}"
            if key in ledger.slots and ledger.slots[key]["terminal_status"] is None:
                ledger.finish(key, "SUCCESS", payload=payload)
    attempted_conditioning = exception_payload.get("attempted_conditioning_name")
    if isinstance(attempted_conditioning, str) and attempted_conditioning:
        attempted_conditioning_key = (
            f"conditioning|{base}|{attempted_conditioning}"
        )
        if (
            attempted_conditioning_key in ledger.slots
            and ledger.slots[attempted_conditioning_key]["terminal_status"] is None
        ):
            ledger.finish(
                attempted_conditioning_key,
                "EVALUATION_FAILED",
                payload={
                    "attempted_conditioning_name": attempted_conditioning,
                    "smallest_exception_payload": exception_payload,
                },
                error=reason,
            )
    completed_evidence = exception_payload.get("completed_evidence")
    completed_evidence_input_completion = exception_payload.get(
        "completed_evidence_input_completion"
    )
    completed_dependencies = exception_payload.get("completed_dependency_paths")
    if isinstance(completed_evidence, dict) and isinstance(
        completed_dependencies, dict
    ):
        for evidence_kind in EVIDENCE_KINDS:
            key = f"evidence|{base}|{evidence_kind}"
            if (
                evidence_kind in completed_evidence
                and evidence_kind in completed_dependencies
                and key in ledger.slots
                and ledger.slots[key]["terminal_status"] is None
            ):
                ledger.finish(
                    key,
                    "SUCCESS",
                    payload={
                        "state": completed_evidence[evidence_kind],
                        "input_completion": (
                            completed_evidence_input_completion.get(evidence_kind)
                            if isinstance(
                                completed_evidence_input_completion, dict
                            )
                            else None
                        ),
                        "dependency_path": completed_dependencies[evidence_kind],
                        "nonexclusive": True,
                    },
                )
    slot_key = f"slot|{base}|complete"
    if slot_key in ledger.slots and ledger.slots[slot_key]["terminal_status"] is None:
        ledger.finish(
            slot_key,
            "EVALUATION_FAILED",
            payload={
                "smallest_exception_payload": exc.payload,
                "error_type": type(exc).__name__,
                "error_message": str(exc)[:2048],
            },
            error=reason,
        )
    for key, record in ledger.slots.items():
        if base in key and record["terminal_status"] is None:
            ledger.finish(key, "NOT_RUN_UPSTREAM_INVALID", error=reason)


def p44_terminalize_failed_constant_phase(
    ledger: SlotLedger,
    formula: Mapping[str, Any],
    structural_plans: Mapping[str, P44CallablePlan],
    completed_plans: Mapping[str, P44CallablePlan],
    failed_point: str,
    exc: SlotEvaluationError,
    preenumeration: Mapping[str, Any],
) -> None:
    """Retain every completed constant sibling and the smallest failed trace."""
    reason = f"{type(exc).__name__}: {exc}"[:4096]
    failure_payload = dict(exc.payload)
    failed_digest = str(failure_payload.get("failed_digest", ""))
    partial_records = failure_payload.get("completed_constant_records", {})
    if not isinstance(partial_records, dict):
        partial_records = {}

    for point in TARGETS:
        point_formula = formula["by_point"][point]
        formula_records = [
            (f"formula|point={point}|action", point_formula["action"]),
            *[
                (
                    f"formula|point={point}|gradient={component}",
                    point_formula["gradient"][component],
                )
                for component in range(7)
            ],
            *[
                (
                    f"formula|point={point}|hessian={row},{column}",
                    point_formula["hessian"][row][column],
                )
                for row in range(7)
                for column in range(7)
            ],
        ]
        for key, payload in formula_records:
            if ledger.slots[key]["terminal_status"] is None:
                ledger.finish(key, "SUCCESS", payload=payload)
        for key, payload in (
            (
                f"callable|point={point}|fingerprint",
                structural_plans[point].fingerprint,
            ),
            (
                f"callable|point={point}|AST_node_inventory",
                preenumeration["AST_node_inventories_by_point"][point],
            ),
        ):
            if ledger.slots[key]["terminal_status"] is None:
                ledger.finish(key, "SUCCESS", payload=payload)

    for point, plan in completed_plans.items():
        for digest, record in plan.constant_records.items():
            key = f"constant_subtree|point={point}|sha256={digest}"
            if ledger.slots[key]["terminal_status"] is None:
                ledger.finish(key, "SUCCESS", payload=record)

    for digest in sorted(structural_plans[failed_point].constant_occurrences):
        key = f"constant_subtree|point={failed_point}|sha256={digest}"
        if ledger.slots[key]["terminal_status"] is not None:
            continue
        if digest in partial_records:
            ledger.finish(key, "SUCCESS", payload=partial_records[digest])
        elif digest == failed_digest:
            ledger.finish(
                key,
                "EVALUATION_FAILED",
                payload={
                    "failed_digest": failed_digest,
                    "failed_trace": failure_payload.get("failed_trace"),
                    "smallest_exception_payload": failure_payload.get(
                        "smallest_exception_payload"
                    ),
                    "completed_sibling_digests": list(partial_records),
                },
                error=reason,
            )

    global_failed_key = f"constant_subtree_global|sha256={failed_digest}"
    if (
        failed_digest
        and global_failed_key in ledger.slots
        and ledger.slots[global_failed_key]["terminal_status"] is None
    ):
        ledger.finish(
            global_failed_key,
            "EVALUATION_FAILED",
            payload={
                "failed_variant": failed_point,
                "failed_digest": failed_digest,
                "failed_trace": failure_payload.get("failed_trace"),
                "completed_sibling_digests": list(partial_records),
            },
            error=reason,
        )


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
        "constant_evaluation_failure": run_state.get(
            "constant_evaluation_failure"
        ),
        "base_slot_failure": run_state.get("base_slot_failure"),
        "retained_completed_slot_records": run_state.get(
            "completed_slot_records"
        ),
        "retained_completed_slot_flags": run_state.get(
            "completed_slot_flags"
        ),
        "late_provenance_failure": run_state.get("late_provenance_failure"),
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


def p44_record_contracts(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    *,
    provenance: Mapping[str, Any],
    manifest_validation: Mapping[str, Any],
    context: P44Context,
    formula: Mapping[str, Any],
    formula_states: Mapping[str, str],
    plans: Mapping[str, P44CallablePlan],
    preenumeration: Mapping[str, Any],
    slot_flags: Mapping[str, Mapping[str, Any]],
    aggregates: Mapping[str, Any],
    dependency_validation: Mapping[str, Any],
) -> None:
    exact_map, numerical_map = manifest_contract_maps(manifest)
    callable_stable = bool(provenance["callable_TOCTOU"]["all_equal"])
    exact_values: dict[str, tuple[bool, Mapping[str, Any]]] = {
        EXACT_IDS[0]: (
            bool(
                all(provenance["comparisons"].values()) and callable_stable
            ),
            {
                "manifest_validation": dict(manifest_validation),
                "provenance_comparisons": provenance["comparisons"],
                "callable_start_end_equal": callable_stable,
            },
        ),
        EXACT_IDS[1]: (
            bool(
                context.validation["base_slot_count"] == 90
                and context.validation["disclosed_mismatch_count"] == 13
                and context.validation["within_threshold_control_count"] == 77
                and context.validation["mismatch_counts_by_point"]
                == {"shared_zero": 5, "phi_plus": 3, "a_plus": 5}
                and context.validation["phase42_anomaly_overlap_count"] == 5
            ),
            context.validation,
        ),
        EXACT_IDS[2]: (
            all(value == 0 for value in context.forbidden_call_counter.values()),
            {
                "forbidden_call_counter": dict(context.forbidden_call_counter),
                "root_ODE_time_integrated_tangent_calls": 0,
            },
        ),
        EXACT_IDS[3]: (
            bool(
                formula["exact_tree_has_no_SymPy_Float"]
                and formula["independent_boundary_audit"][
                    "independence_denylist_passed"
                ]
                and len(formula["by_point"]) == 3
            ),
            {
                "formula_states": dict(formula_states),
                "component_counts": {"action": 3, "gradient": 21, "hessian": 147},
                "source_side_access": formula["source_side_access"],
                "independent_boundary_audit": formula["independent_boundary_audit"],
            },
        ),
        EXACT_IDS[4]: (
            bool(
                all(
                    flags["source_reproduced"]
                    and flags["source_raw_bitwise_reproduced"]
                    and flags["trace_failure_count"] == 0
                    and flags["trace_raw_bitwise_reproduction"]
                    and flags["trace_all_events_terminal_SUCCESS"]
                    and flags["trace_path_operation_commitments_complete"]
                    and flags["trace_exact_complete"]
                    for flags in slot_flags.values()
                )
                and all(
                    plans[point].normalized_ast_sha256
                    == manifest["known_prior_results_and_audit_disclosure"][
                        "phase44_precommit_generated_callable_structural_audit"
                    ]["normalized_AST_sha256"][point]
                    for point in TARGETS
                )
            ),
            {
                "slot_count": len(slot_flags),
                "normalized_AST_sha256": {
                    point: plans[point].normalized_ast_sha256 for point in TARGETS
                },
                "constant_model_status": {
                    point: plans[point].constant_model_ok for point in TARGETS
                },
                "trace_exact_completion_count": sum(
                    flags["trace_exact_complete"]
                    for flags in slot_flags.values()
                ),
                "trace_failure_count": sum(
                    flags["trace_failure_count"] for flags in slot_flags.values()
                ),
                "raw_bitwise_reproduction_count": sum(
                    flags["trace_raw_bitwise_reproduction"]
                    for flags in slot_flags.values()
                ),
            },
        ),
        EXACT_IDS[5]: (
            bool(
                len(slot_flags) == 90
                and all(
                    flags["rounding50_reproduced"]
                    for flags in slot_flags.values()
                )
                and all(flags["all_alternatives_complete"] for flags in slot_flags.values())
                and all(
                    flags.get("fixed_hybrid_contract_validated") is True
                    for flags in slot_flags.values()
                )
            ),
            {
                "slot_count": len(slot_flags),
                "stage_count_per_slot": 8,
                "delta_count_per_slot": 7,
                "alternative_count_per_slot": 6,
                "rounding50_reproduction_count": sum(
                    flags["rounding50_reproduced"]
                    for flags in slot_flags.values()
                ),
                "source_contraction_budget": 56,
                "alternative_budgets": {
                    "explicit_naive": 56,
                    "fixed_pairwise": 54,
                    "componentwise_kahan": 98,
                },
            },
        ),
        EXACT_IDS[6]: (
            bool(
                tuple(ledger.slots) == tuple(preenumeration["declared_keys_in_fixed_order"])
                and len(slot_flags) == 90
                and all(flags["classification_complete"] for flags in slot_flags.values())
                and all(
                    flags.get("retention_schema_validated") is True
                    for flags in slot_flags.values()
                )
                and dependency_validation["acyclic"] is True
                and dependency_validation[
                    "canonical_paths_match_classification_and_aggregate_semantics"
                ]
                is True
                and dependency_validation["evidence_node_count"] == 816
                and all(
                    slot["terminal_status"] is not None
                    or key.startswith("contract|")
                    for key, slot in ledger.slots.items()
                )
            ),
            {
                "declared_key_count": preenumeration["declared_key_count"],
                "declared_keys_sha256": preenumeration["declared_keys_sha256"],
                "nonexclusive_evidence_kind_count": len(EVIDENCE_KINDS),
                "dependency_validation": dict(dependency_validation),
            },
        ),
        EXACT_IDS[7]: (
            bool(
                manifest["required_fail_closed_outputs"]
                == expected_fail_closed_outputs()
                and manifest["desired_outputs"] == expected_desired_outputs()
                and manifest["historical_statuses_must_remain"]
                == expected_historical_statuses()
            ),
            {
                "false_count": sum(
                    value is False for value in expected_fail_closed_outputs().values()
                ),
                "null_count": sum(
                    value is None for value in expected_fail_closed_outputs().values()
                ),
                "desired_null_count": len(expected_desired_outputs()),
                "gate1_status": expected_fail_closed_outputs()["gate1_status"],
            },
        ),
    }
    for check_id in EXACT_IDS:
        passed, details = exact_values[check_id]
        audit.exact(
            check_id,
            passed,
            str(exact_map[check_id]["criterion"]),
            details=details,
        )
    disclosed_flags = [
        flags
        for base, flags in slot_flags.items()
        if base in {
            base_key(str(record["point"]), str(record["fraction"]), int(record["direction"]))
            for record in manifest["known_prior_results_and_audit_disclosure"][
                "all_thirteen_disclosed_mismatch_slots"
            ]
        }
    ]
    numerical_values: dict[str, tuple[bool, Mapping[str, Any]]] = {
        NUMERICAL_IDS[0]: (
            all(
                flags["reference_reproduced"]
                and flags["source_reproduced"]
                and flags["mismatch_label_reproduced"]
                for flags in slot_flags.values()
            ),
            {"slot_count": len(slot_flags), "disclosed_mismatch_count": 13},
        ),
        NUMERICAL_IDS[1]: (
            all(state == "NOT_SUPPORTED" for state in formula_states.values()),
            {"formula_mismatch_states": dict(formula_states)},
        ),
        NUMERICAL_IDS[2]: (
            all(flags["telescope_closed"] for flags in slot_flags.values()),
            {"closed_count": sum(flags["telescope_closed"] for flags in slot_flags.values())},
        ),
        NUMERICAL_IDS[3]: (
            all(flags["coverage_supported"] for flags in slot_flags.values()),
            {
                "supported_count": sum(
                    flags["coverage_supported"] for flags in slot_flags.values()
                ),
                "state_histogram": {
                    state: sum(flags["coverage_state"] == state for flags in slot_flags.values())
                    for state in ("SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE")
                },
            },
        ),
        NUMERICAL_IDS[4]: (
            len(disclosed_flags) == 13
            and all(flags["coverage_supported"] for flags in disclosed_flags),
            {
                "cohort_count": len(disclosed_flags),
                "aggregate": aggregates["cohort_protocol"][
                    "ALL_13_WITHIN_DECLARED_FORWARD_ERROR_MODEL"
                ],
            },
        ),
        NUMERICAL_IDS[5]: (
            all(
                flags["all_alternatives_complete"]
                and flags.get("fixed_hybrid_contract_validated") is True
                for flags in slot_flags.values()
            ),
            {"slot_count": len(slot_flags), "paths_per_slot": 6},
        ),
        NUMERICAL_IDS[6]: (
            all(
                flags["classification_complete"]
                and flags.get("retention_schema_validated") is True
                for flags in slot_flags.values()
            )
            and dependency_validation["acyclic"] is True
            and dependency_validation[
                "canonical_paths_match_classification_and_aggregate_semantics"
            ]
            is True
            and dependency_validation["evidence_node_count"] == 816,
            {
                "slot_count": len(slot_flags),
                "evidence_kinds": list(EVIDENCE_KINDS),
                "aggregates_complete": True,
                "no_forced_unique_cause": True,
            },
        ),
    }
    for check_id in NUMERICAL_IDS:
        passed, details = numerical_values[check_id]
        declared = numerical_map[check_id]
        audit.numerical(
            check_id,
            passed,
            str(declared["criterion"]),
            failure_status=str(declared["failure_status"]),
            failure_invalidates_run=bool(declared["failure_invalidates_run"]),
            details=details,
        )
    records = {
        record["id"]: record for record in audit.exact_records + audit.numerical_records
    }
    for contract_id in EXACT_IDS + NUMERICAL_IDS:
        ledger.finish(
            f"contract|{contract_id}", "SUCCESS", payload=records[contract_id]
        )
    ledger.assert_complete()
    enforce_audit_cardinality_and_invalidating_failures(audit)


def p44_callable_snapshot(
    plans: Mapping[str, P44CallablePlan]
) -> dict[str, Any]:
    return {
        point: {
            **p44_callable_fingerprint(plans[point].function),
            "numpy_global_identities": p44_validate_callable_globals(
                plans[point].function
            ),
            "exact50_literal_mapping": plans[point].exact50_literal_mapping,
        }
        for point in TARGETS
    }


def p44_finish_provenance_and_callable_guard(
    manifest: Mapping[str, Any],
    provenance_start: Mapping[str, Any],
    plans: Mapping[str, P44CallablePlan],
    callable_start: Mapping[str, Any],
) -> dict[str, Any]:
    provenance = finish_provenance_guard(manifest, provenance_start)
    callable_end = p44_callable_snapshot(plans)
    equality = {
        point: callable_end[point] == callable_start[point] for point in TARGETS
    }
    if not all(equality.values()):
        raise InvalidRun(f"generated callable TOCTOU drift: {equality}")
    output = dict(provenance)
    output["callable_TOCTOU"] = {
        "start": dict(callable_start),
        "end": callable_end,
        "per_variant_equal": equality,
        "all_equal": True,
        "numpy_globals_reverified_at_end": True,
    }
    return output


def p44_run_production(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    run_state: dict[str, Any],
) -> int:
    manifest_validation = p44_validate_manifest(manifest)
    run_state["raw_start"] = {
        "runner": observe_runner_provenance_raw(),
        "source": observe_source_closure_raw(manifest),
        "HEAD": raw_git_observation("rev-parse", "HEAD"),
    }
    progress("provenance/start")
    provenance_start = start_provenance_guard(manifest)
    run_state["provenance_start"] = provenance_start
    progress("strict pinned Phase43/42/41 input audit")
    context = p44_load_context(manifest)
    progress("exact independent/source formula canonicalization")
    formula, formula_states = p44_formula_audit(context)
    progress("generated callable structural discovery and full key freeze")
    structural_plans = p44_prepare_callable_plans(context, manifest)
    callable_start = {
        point: dict(structural_plans[point].fingerprint) for point in TARGETS
    }
    preenumeration = p44_preenumerate(ledger, structural_plans)
    progress("post-freeze disclosed-cohort join and validation")
    context = p44_join_disclosures_after_preenumeration(
        context, manifest, preenumeration
    )
    plans: dict[str, P44CallablePlan] = {}
    for point in TARGETS:
        try:
            with mp.workdps(AUTHORITATIVE_DPS):
                plans[point] = p44_evaluate_plan_constants(
                    structural_plans[point]
                )
        except SlotEvaluationError as exc:
            run_state["constant_evaluation_failure"] = exc.payload
            p44_terminalize_failed_constant_phase(
                ledger,
                formula,
                structural_plans,
                plans,
                point,
                exc,
                preenumeration,
            )
            raise InvalidRun(
                f"required Phase44 constant trace incomplete: {point}: {exc}"
            ) from exc
    global_constant_records = p44_finish_formula_and_plan_ledger(
        ledger, formula, plans, preenumeration
    )
    progress("independent 120-dps numerical Hessian evaluators")
    symbolic = {
        point: p44_make_numeric_symbolic(context.points[point])
        for point in TARGETS
    }
    slot_records: dict[str, Mapping[str, Any]] = {}
    slot_flags: dict[str, Mapping[str, Any]] = {}
    run_state["completed_slot_records"] = slot_records
    run_state["completed_slot_flags"] = slot_flags
    completed = 0
    for point in TARGETS:
        for fraction in FRACTION_STRINGS:
            for direction in DIRECTIONS:
                key_tuple = (point, fraction, direction)
                slot = context.slots[key_tuple]
                base = base_key(point, fraction, direction)
                slot_retention_state: dict[str, Any] = {}
                try:
                    with mp.workdps(AUTHORITATIVE_DPS):
                        payload, flags = p44_slot_calculation(
                            context,
                            slot,
                            plans[point],
                            symbolic[point],
                            formula_states[point],
                            slot_retention_state,
                        )
                except SlotEvaluationError as exc:
                    terminal_exc = exc
                    payload_scope = str(exc.payload.get("failure_scope", ""))
                    if (
                        payload_scope.startswith("AST_")
                        or payload_scope.startswith("source_boundary_")
                        or payload_scope.startswith("alternative_")
                    ):
                        terminal_exc = SlotEvaluationError(
                            str(exc),
                            payload={**slot_retention_state, **exc.payload},
                        )
                    else:
                        terminal_exc = SlotEvaluationError(
                            str(exc),
                            payload={
                                "failure_scope": (
                                    "base_slot_"
                                    + str(
                                        slot_retention_state.get(
                                            "stage", "scientific_arithmetic"
                                        )
                                    )
                                ),
                                **slot_retention_state,
                                "smallest_exception_payload": exc.payload,
                            },
                        )
                    run_state["base_slot_failure"] = {
                        "base": base,
                        "attempted_parameters": {
                            "point": point,
                            "fraction": fraction,
                            "direction": direction,
                        },
                        "smallest_exception_payload": terminal_exc.payload,
                        "completed_sibling_base_keys": list(slot_records),
                    }
                    p44_terminalize_failed_base_slot(
                        ledger,
                        base,
                        terminal_exc,
                        preenumeration["trace_shapes_by_point"][point],
                    )
                    raise InvalidRun(
                        f"required Phase44 slot incomplete: {base}: {terminal_exc}"
                    ) from exc
                except InvalidRun as exc:
                    wrapped = SlotEvaluationError(
                        (
                            "Phase44 exact/source slot contract failed at "
                            f"{base}: {exc}"
                        ),
                        payload={
                            "failure_scope": (
                                "base_slot_exact_or_structural_"
                                + str(
                                    slot_retention_state.get(
                                        "stage", "contract_validation"
                                    )
                                )
                            ),
                            **slot_retention_state,
                            "underlying_error_type": type(exc).__name__,
                            "underlying_error_message": str(exc)[:2048],
                            "completed_sibling_base_keys": list(slot_records),
                        },
                    )
                    run_state["base_slot_failure"] = {
                        "base": base,
                        **wrapped.payload,
                    }
                    p44_terminalize_failed_base_slot(
                        ledger,
                        base,
                        wrapped,
                        preenumeration["trace_shapes_by_point"][point],
                    )
                    raise InvalidRun(
                        f"required Phase44 exact/source slot invalid: {base}: {exc}"
                    ) from exc
                except (ArithmeticError, ValueError) as exc:
                    wrapped = SlotEvaluationError(
                        (
                            "declared Phase44 scientific arithmetic failed at "
                            f"{base}: {type(exc).__name__}: {exc}"
                        ),
                        payload={
                            "failure_scope": "base_slot_scientific_arithmetic",
                            "attempted_parameters": {
                                "point": point,
                                "fraction": fraction,
                                "direction": direction,
                            },
                            "underlying_error_type": type(exc).__name__,
                            "underlying_error_message": str(exc)[:2048],
                            "completed_sibling_base_keys": list(slot_records),
                            **slot_retention_state,
                        },
                    )
                    run_state["base_slot_failure"] = {
                        "base": base,
                        **wrapped.payload,
                    }
                    p44_terminalize_failed_base_slot(
                        ledger,
                        base,
                        wrapped,
                        preenumeration["trace_shapes_by_point"][point],
                    )
                    raise InvalidRun(
                        f"required Phase44 slot incomplete: {base}: {wrapped}"
                    ) from exc
                try:
                    p44_finish_base_slot_ledger(
                        ledger,
                        payload,
                        flags,
                        preenumeration["trace_shapes_by_point"][point],
                        preenumeration["alternative_internal_shapes"],
                    )
                except SlotEvaluationError as exc:
                    wrapped = SlotEvaluationError(
                        str(exc),
                        payload={
                            **slot_retention_state,
                            "completed_slot_payload": payload,
                            "completed_slot_payload_sha256": sha256_bytes(
                                canonical_json_bytes(payload)
                            ),
                            **exc.payload,
                        },
                    )
                    run_state["base_slot_failure"] = {
                        "base": base,
                        **wrapped.payload,
                    }
                    p44_terminalize_failed_base_slot(
                        ledger,
                        base,
                        wrapped,
                        preenumeration["trace_shapes_by_point"][point],
                    )
                    raise InvalidRun(
                        f"required Phase44 retention commitment invalid: {base}: {exc}"
                    ) from exc
                except InvalidRun as exc:
                    wrapped = SlotEvaluationError(
                        f"preenumerated slot-retention validation failed: {base}: {exc}",
                        payload={
                            "failure_scope": "slot_retention_or_path_commitment",
                            "attempted_parameters": {
                                "point": point,
                                "fraction": fraction,
                                "direction": direction,
                            },
                            "underlying_error_type": type(exc).__name__,
                            "underlying_error_message": str(exc)[:2048],
                            "completed_slot_payload_sha256": sha256_bytes(
                                canonical_json_bytes(payload)
                            ),
                            "completed_slot_payload": payload,
                            "completed_sibling_base_keys": [
                                key for key in slot_records if key != base
                            ],
                            **slot_retention_state,
                        },
                    )
                    run_state["base_slot_failure"] = {
                        "base": base,
                        **wrapped.payload,
                    }
                    p44_terminalize_failed_base_slot(
                        ledger,
                        base,
                        wrapped,
                        preenumeration["trace_shapes_by_point"][point],
                    )
                    raise InvalidRun(
                        f"required Phase44 slot retention incomplete: {base}: {exc}"
                    ) from exc
                slot_records[base] = payload
                slot_flags[base] = flags
                completed += 1
                if completed % 10 == 0 or completed == 90:
                    progress(f"all-slot arithmetic audit {completed}/90")
    aggregates = p44_aggregate_and_finish(ledger, slot_records)
    dependency_validation = p44_validate_dependency_ledger(ledger)
    progress("provenance/end and callable TOCTOU")
    provenance = p44_finish_provenance_and_callable_guard(
        manifest, provenance_start, plans, callable_start
    )
    run_state["provenance_pre_audit"] = provenance
    p44_record_contracts(
        manifest,
        audit,
        ledger,
        provenance=provenance,
        manifest_validation=manifest_validation,
        context=context,
        formula=formula,
        formula_states=formula_states,
        plans=plans,
        preenumeration=preenumeration,
        slot_flags=slot_flags,
        aggregates=aggregates,
        dependency_validation=dependency_validation,
    )
    typed_scientific_outcomes = [
        (
            "SYMBOLIC_FORMULA_IDENTITY_SUPPORTED"
            if all(state == "NOT_SUPPORTED" for state in formula_states.values())
            else "SYMBOLIC_FORMULA_MISMATCH_SUPPORTED"
        ),
        (
            "DECLARED_FLOAT64_FORWARD_ERROR_MODEL_SUPPORTED_ALL_13"
            if aggregates["cohort_protocol"][
                "ALL_13_WITHIN_DECLARED_FORWARD_ERROR_MODEL"
            ]
            == "SUPPORTED"
            else "PHASE43_MISMATCH_COHORT_MIXED_OR_UNRESOLVED"
        ),
        "LOCAL_ROUNDING_CONTRIBUTIONS_MIXED_NONEXCLUSIVE",
    ]
    if aggregates["global"]["unresolved_beyond_model"]["existential_any"] == "SUPPORTED":
        typed_scientific_outcomes.append("UNRESOLVED_BEYOND_DECLARED_MODEL_SUPPORTED")
    typed_scientific_outcomes.append(
        "INTEGRATED_TANGENT_EVOLUTION_NOT_TESTED_LOCAL_ONLY"
    )
    declared_typed_outcomes = set(
        manifest["run_semantics"]["valid_typed_scientific_outcomes"]
    )
    if any(value not in declared_typed_outcomes for value in typed_scientific_outcomes):
        raise InvalidRun("undeclared Phase44 typed scientific outcome")
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 44,
        "run_status": "VALID_TYPED_RUN",
        "exit_code": 0,
        "counts": {
            "exact_passed": sum(record["passed"] for record in audit.exact_records),
            "exact_total": len(EXACT_IDS),
            "numerical_passed": sum(
                record["passed"] for record in audit.numerical_records
            ),
            "numerical_total": len(NUMERICAL_IDS),
            "base_slots": 90,
            "disclosed_mismatches": 13,
            "controls": 77,
        },
        "manifest_validation": manifest_validation,
        "input_validation": context.validation,
        "exact_formula_audit": formula,
        "generated_callable_fingerprints": {
            point: plans[point].fingerprint for point in TARGETS
        },
        "constant_subtree_records": {
            point: plans[point].constant_records for point in TARGETS
        },
        "global_deduplicated_constant_subtree_records": global_constant_records,
        "numeric_symbolic_fingerprints": {
            point: symbolic[point].fingerprints for point in TARGETS
        },
        "preenumeration": preenumeration,
        "slot_records": slot_records,
        "classification_aggregates": aggregates,
        "dependency_validation": dependency_validation,
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "slot_schema_summary": ledger.summary(),
        "slot_ledger": ledger.slots,
        "desired_outputs": expected_desired_outputs(),
        "required_fail_closed_outputs": expected_fail_closed_outputs(),
        "historical_statuses_must_remain": manifest[
            "historical_statuses_must_remain"
        ],
        "claim_status": {
            "phase44_local_arithmetic_diagnosis": "LOCAL_ROUNDING_CONTRIBUTIONS_MIXED_NONEXCLUSIVE",
            "typed_scientific_outcomes": typed_scientific_outcomes,
            "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
            "ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
            "global_promotion": "PROHIBITED",
            "gate1_status": "OPEN_PARTIAL_PROGRESS",
        },
        "scientific_scope": {
            "all_90_frozen_local_slots": True,
            "selected_mismatch_only_run": False,
            "root_solver_evaluations": 0,
            "ODE_solver_evaluations": 0,
            "time_column_evaluations": 0,
            "integrated_tangent_evaluations": 0,
            "orientation_or_determinant_line_evaluations": 0,
            "global_intersection_claim": False,
            "no_unique_cause_forced": True,
        },
        "result_artifact_contract": manifest["declared_output_retention"][
            "result_artifact"
        ],
        "provenance": provenance,
    }
    try:
        run_state["provenance_pre_emit"] = (
            p44_finish_provenance_and_callable_guard(
                manifest, provenance_start, plans, callable_start
            )
        )
    except Exception as exc:
        run_state["late_provenance_failure"] = {
            "stage": "pre_emit",
            "error": f"{type(exc).__name__}: {exc}"[:4096],
        }
        raise
    payload["provenance"] = run_state["provenance_pre_emit"]
    def final_guard() -> None:
        try:
            p44_finish_provenance_and_callable_guard(
                manifest, provenance_start, plans, callable_start
            )
        except Exception as exc:
            run_state["late_provenance_failure"] = {
                "stage": "final_stdout_guard",
                "error": f"{type(exc).__name__}: {exc}"[:4096],
            }
            raise

    emit_result(payload, final_guard=final_guard)
    return 0


def p44_invalid_result_skeleton(
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
            manifest_contract_maps(manifest) if manifest is not None else ({}, {})
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
                "statement": str(exact_map.get(check_id, {}).get("criterion", reason)),
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
                "late_provenance_or_callable_final_guard_failure": True,
                "invalid_reason": reason,
            },
        }
    numerical_records = [
        existing_numerical.get(
            check_id,
            {
                "id": check_id,
                "kind": "numerical",
                "status": "NOT_RUN_UPSTREAM_INVALID",
                "passed": False,
                "failure_status": str(
                    numerical_map.get(check_id, {}).get("failure_status", "INVALID_RUN")
                ),
                "failure_invalidates_run": bool(
                    numerical_map.get(check_id, {}).get(
                        "failure_invalidates_run", True
                    )
                ),
                "statement": str(
                    numerical_map.get(check_id, {}).get("criterion", reason)
                ),
                "details": {"not_completed_reason": reason},
            },
        )
        for check_id in NUMERICAL_IDS
    ]
    for record in audit.exact_records + audit.numerical_records:
        contract_key = f"contract|{record['id']}"
        if (
            contract_key in ledger.slots
            and ledger.slots[contract_key]["terminal_status"] is None
        ):
            passed = record.get("passed") is True
            ledger.finish(
                contract_key,
                "SUCCESS" if passed else "EVALUATION_FAILED",
                payload=record,
                error=None if passed else str(reason)[:8192],
            )
    ledger.fail_unfinished(reason)
    if force_freeze_contract_invalid:
        freeze_key = f"contract|{EXACT_IDS[0]}"
        if freeze_key in ledger.slots:
            # A final TOCTOU failure occurs after the ordinary contract records
            # may already have been terminalized.  The emitted invalid ledger
            # must agree with the top-level fail-closed override.
            ledger.slots[freeze_key]["terminal_status"] = "EVALUATION_FAILED"
            ledger.slots[freeze_key]["payload"] = json_ready(exact_records[0])
            ledger.slots[freeze_key]["error"] = str(reason)[:8192]
    try:
        runner_observed_sha256: str | None = sha256_bytes(SCRIPT_PATH.read_bytes())
        runner_observation_error: str | None = None
    except Exception as exc:
        runner_observed_sha256 = None
        runner_observation_error = f"{type(exc).__name__}: {exc}"[:4096]
    retained_slot_records = failure_provenance.get(
        "retained_completed_slot_records"
    )
    retained_slot_flags = failure_provenance.get("retained_completed_slot_flags")
    if not isinstance(retained_slot_records, dict):
        retained_slot_records = {}
    if not isinstance(retained_slot_flags, dict):
        retained_slot_flags = {}
    return {
        "schema": RESULT_SCHEMA,
        "phase": 44,
        "run_status": "INVALID_RUN",
        "exit_code": 2,
        "invalid_reason": str(reason)[:8192],
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
        "slot_records": retained_slot_records,
        "slot_flags": retained_slot_flags,
        "desired_outputs": expected_desired_outputs(),
        "required_fail_closed_outputs": expected_fail_closed_outputs(),
        "historical_statuses_must_remain": expected_historical_statuses(),
        "claim_status": {
            "phase44_local_arithmetic_diagnosis": None,
            "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
            "ODE_solver_noise_component": "NOT_TESTED_LOCAL_ONLY",
            "global_promotion": "PROHIBITED",
            "gate1_status": "OPEN_PARTIAL_PROGRESS",
        },
        "scientific_scope": {
            "local_only": True,
            "production_claim_valid": False,
            "root_ODE_time_integrated_tangent_evaluations": 0,
            "global_promotion": "PROHIBITED",
        },
        "provenance": {
            "manifest_commit": MANIFEST_COMMIT,
            "manifest_sha256": MANIFEST_SHA256,
            "runner_observed_sha256": runner_observed_sha256,
            "runner_observation_error": runner_observation_error,
            "late_provenance_failure_forced_freeze_contract_invalid": bool(
                force_freeze_contract_invalid
            ),
            "failure_observations": failure_provenance,
        },
    }


def p44_emergency_finite_invalid_result(reason: str) -> dict[str, Any]:
    clean_reason = str(reason).replace("\x00", "?")[:4096]
    try:
        runner_observed_sha256: str | None = sha256_bytes(SCRIPT_PATH.read_bytes())
        runner_observation_error: str | None = None
    except Exception as exc:
        runner_observed_sha256 = None
        runner_observation_error = f"{type(exc).__name__}: {exc}"[:4096]
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
    numerical_failures = (
        ("PHASE43_SOURCE_REFERENCE_OR_PLATFORM_DRIFT", True),
        ("SYMBOLIC_FORMULA_MISMATCH_SUPPORTED", False),
        ("HYBRID_DECOMPOSITION_INCOMPLETE_OR_INCONSISTENT", True),
        ("DECLARED_FLOAT64_FORWARD_ERROR_MODEL_NOT_UNIVERSALLY_SUPPORTED", False),
        ("PHASE43_MISMATCH_COHORT_MIXED_OR_UNRESOLVED", False),
        ("CONTRACTION_DIAGNOSTIC_LEDGER_INCOMPLETE", True),
        ("LOCAL_CAUSAL_LEDGER_INCOMPLETE", True),
    )
    numerical_records = [
        {
            "id": check_id,
            "kind": "numerical",
            "status": "NOT_RUN_UPSTREAM_INVALID",
            "passed": False,
            "failure_status": numerical_failures[index][0],
            "failure_invalidates_run": numerical_failures[index][1],
            "statement": clean_reason,
            "details": {"emergency_fallback": True},
        }
        for index, check_id in enumerate(NUMERICAL_IDS)
    ]
    return {
        "schema": RESULT_SCHEMA,
        "phase": 44,
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
        "desired_outputs": expected_desired_outputs(),
        "required_fail_closed_outputs": expected_fail_closed_outputs(),
        "historical_statuses_must_remain": expected_historical_statuses(),
        "claim_status": {
            "phase44_local_arithmetic_diagnosis": None,
            "integrated_tangent_evolution": "NOT_TESTED_LOCAL_ONLY",
            "global_promotion": "PROHIBITED",
            "gate1_status": "OPEN_PARTIAL_PROGRESS",
        },
        "provenance": {
            "manifest_commit": MANIFEST_COMMIT,
            "manifest_sha256": MANIFEST_SHA256,
            "runner_observed_sha256": runner_observed_sha256,
            "runner_observation_error": runner_observation_error,
            "emergency_minimal_provenance": True,
        },
        "emergency_fallback": True,
    }


def main() -> int:
    manifest: dict[str, Any] | None = None
    audit = Audit()
    ledger = SlotLedger()
    run_state: dict[str, Any] = {}
    try:
        raw = MANIFEST_PATH.read_bytes()
        manifest = strict_json_bytes(raw, label="Phase44 manifest")
        observed_sha = sha256_bytes(raw)
        if observed_sha != MANIFEST_SHA256:
            raise InvalidRun(
                f"Phase44 manifest SHA drift: {observed_sha} != {MANIFEST_SHA256}"
            )
        if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            raise InvalidRun("Phase44 manifest must end in exactly one LF")
        run_state["manifest_sha_verified"] = True
        return p44_run_production(manifest, audit, ledger, run_state)
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
                p44_invalid_result_skeleton(
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
            emergency = result_with_self_digest(
                p44_emergency_finite_invalid_result(emergency_reason)
            )
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
