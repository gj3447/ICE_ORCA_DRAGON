#!/usr/bin/env python3
"""Regenerate a post-hoc Phase-41 fixed-root checkpoint for Phase 42.

This extractor imports a byte-pinned Phase-41 production module and replays
its deterministic prefix through the five primary local intersections.  It
then emits the full fixed-root data needed to audit the Phase-41 tangent map:
parameters, states, frames, scaled residuals, full 14x14 variational root
Jacobians, saddles, the fixed metric, and the frozen chart.

The checkpoint is regenerated after the original Phase-41 run.  The original
raw stdout was not archived, so this program explicitly does *not* assert
identity with any historical root vector or stdout byte stream.  It writes no
files.  Successful stdout consists of one ``CHECKPOINT_JSON=`` record;
progress from the imported calculation is redirected to stderr.
"""

from __future__ import annotations

import sys

# This must be set before either byte-pinned repository module is imported.
# The extractor is stdout-only and must not mutate repository __pycache__.
sys.dont_write_bytecode = True

import contextlib
import hashlib
import importlib.util
import json
import math
import os
import platform
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import scipy
import sympy as sp


CHECKPOINT_SCHEMA = "ice-phase42-fixed-root-checkpoint/v1"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PHASE41_DIRECTORY = Path(__file__).resolve().parent

SOURCE_PINS: dict[str, dict[str, str]] = {
    "phase41_script": {
        "path": "cpt_temporal_folded_susy/phase41_m4_two_source_intersection.py",
        "sha256": "377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530",
        "introduced_in_commit": "a31a8627b0e0e210dea96d1d69dad80ccaa6decd",
        "verification_role": "byte-pinned Python module imported by this extractor",
    },
    "phase41_manifest": {
        "path": "cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION_INPUTS.json",
        "sha256": "dc17f4d25e758946fe00fec0bb209462294d4d982b1f86b59c099b8de064c92e",
        "introduced_in_commit": "58181447b558fa204406b732badd5c2fd541bb47",
        "verification_role": "byte-pinned workflow input loaded by Phase 41",
    },
    "phase41_report": {
        "path": "cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION.md",
        "sha256": "9d67451e26838da1ee7e644bbbc4b619600391a96e0762d56aa8f164763f6e52",
        "introduced_in_commit": "a31a8627b0e0e210dea96d1d69dad80ccaa6decd",
        "verification_role": "byte-pinned scoped interpretation read for provenance only",
    },
    "pyproject": {
        "path": "pyproject.toml",
        "sha256": "ae68ad259121fb948c176b5b724db19c6f45ea48e8ad49d5b74a73e623067891",
        "introduced_in_commit": "5aa9be8904bd4dd6325ef7c826b47c9581be004f",
        "verification_role": "byte-pinned Python project contract",
    },
    "uv_lock": {
        "path": "uv.lock",
        "sha256": "8afebaf1d11eb0e31ee6398e4a88b2742acb887920a7ec12a5f3d581c1c99527",
        "introduced_in_commit": "5aa9be8904bd4dd6325ef7c826b47c9581be004f",
        "verification_role": "byte-pinned Python dependency lock",
    },
    "phase39_script": {
        "path": "cpt_temporal_folded_susy/phase39_finite_joint_intersection.py",
        "sha256": "0af21171e44a688a9dd0b19b2491954467c5ceb881a97852d0eb6135ea8fce54",
        "introduced_in_commit": "05b642eafd4dd10ecb69c345bb07bacb2c458bf4",
        "verification_role": "transitive byte-pinned module imported by Phase-41 chart construction",
    },
    "phase39_direction_report": {
        "path": "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md",
        "sha256": "0872eda0d526a707c3eb28a700ff1209d78a94a600419ee09609ac67d0047b70",
        "introduced_in_commit": "05b642eafd4dd10ecb69c345bb07bacb2c458bf4",
        "verification_role": "transitive chart-direction artifact hashed and read by Phase 41",
    },
    "phase39_manifest": {
        "path": "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json",
        "sha256": "b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4",
        "introduced_in_commit": "750d19e76827ce78c9322e9fac6b494ade1f2bbf",
        "verification_role": "transitive input read by Phase39 load_frozen_input",
    },
}

EXPECTED_RUNTIME: dict[str, Any] = {
    "python_implementation": "CPython",
    "python_version": "3.13.5",
    "python_build": ["main", "Jul 15 2026 20:25:40"],
    "python_compiler": "GCC 14.2.0",
    "numpy_version": "2.5.2",
    "scipy_version": "1.18.0",
    "sympy_version": "1.14.0",
    "platform": "Linux-7.0.14-5-pve-x86_64-with-glibc2.41",
    "system": "Linux",
    "release": "7.0.14-5-pve",
    "machine": "x86_64",
    "byteorder": "little",
    "libc": ["glibc", "2.41"],
    "numpy_blas": {
        "name": "scipy-openblas",
        "version": "0.3.34.0.0",
        "openblas_configuration": (
            "OpenBLAS 0.3.34.0.0  USE64BITINT DYNAMIC_ARCH "
            "NO_AFFINITY Haswell MAX_THREADS=64"
        ),
    },
    "numpy_lapack": {
        "name": "scipy-openblas",
        "version": "0.3.34.0.0",
        "openblas_configuration": (
            "OpenBLAS 0.3.34.0.0  USE64BITINT DYNAMIC_ARCH "
            "NO_AFFINITY Haswell MAX_THREADS=64"
        ),
    },
    "scipy_blas": {
        "name": "scipy-openblas",
        "version": "0.3.31.dev",
        "openblas_configuration": (
            "OpenBLAS 0.3.31.dev DYNAMIC_ARCH NO_AFFINITY "
            "SkylakeX MAX_THREADS=64"
        ),
        "has_ilp64": False,
    },
    "scipy_lapack": {
        "name": "scipy-openblas",
        "version": "0.3.31.dev",
        "openblas_configuration": (
            "OpenBLAS 0.3.31.dev DYNAMIC_ARCH NO_AFFINITY "
            "SkylakeX MAX_THREADS=64"
        ),
        "has_ilp64": False,
    },
    "thread_environment": {
        "OPENBLAS_NUM_THREADS": None,
        "OMP_NUM_THREADS": None,
        "MKL_NUM_THREADS": None,
        "VECLIB_MAXIMUM_THREADS": None,
        "NUMEXPR_NUM_THREADS": None,
    },
}

TARGET_POINTS: dict[str, tuple[float, float]] = {
    "shared_zero": (0.0, 0.0),
    "phi_plus": (0.0, 0.001),
    "a_plus": (0.001, 0.0),
}

ALL_SADDLE_POINTS: tuple[tuple[str, tuple[float, float]], ...] = (
    ("shared_zero", (0.0, 0.0)),
    ("phi_plus_half", (0.0, 0.0005)),
    ("phi_plus", (0.0, 0.001)),
    ("phi_minus_half", (0.0, -0.0005)),
    ("phi_minus", (0.0, -0.001)),
    ("a_plus_half", (0.0005, 0.0)),
    ("a_plus", (0.001, 0.0)),
    ("a_minus_half", (-0.0005, 0.0)),
    ("a_minus", (-0.001, 0.0)),
)

# Rounded, nonselecting compatibility witnesses transcribed from the pinned
# Phase-41 report.  These are checked only after the frozen Phase-41 pipeline
# has independently regenerated its results; they are not solver seeds and do
# not select a root or orientation.
DISCLOSED_PHASE41_WITNESSES: dict[str, object] = {
    "chi_half": np.array(
        [
            [4.641563772e-4, 1.789434943e-3],
            [5.176662239e-3, -1.063148730e-3],
        ],
        dtype=float,
    ),
    "chi_half_singular_values": np.array(
        [5.28567e-3, 1.84589e-3], dtype=float
    ),
    "E_step_spectral": 6.52667e-6,
    "E_solver_spectral": 2.43e-12,
    "sigma_min_over_10_E_rank": 28.2823,
    "source_reversal_max": 1.76e-16,
    "reflection_physical_max_abs": {
        "phi": 1.385e-12,
        "a": 6.058e-12,
    },
}

DISCLOSED_PHASE41_TOLERANCES: dict[str, float] = {
    "chi_half_max_abs": 1.0e-12,
    "chi_half_singular_values_max_abs": 5.0e-9,
    "E_step_abs": 1.0e-11,
    "E_solver_abs": 1.0e-14,
    "sigma_ratio_abs": 1.0e-4,
    "source_reversal_abs": 1.0e-18,
    "reflection_physical_abs": 1.0e-15,
}


class CheckpointError(RuntimeError):
    """The pinned checkpoint cannot be regenerated faithfully."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_bytes(commit: str, relative_path: str) -> bytes:
    process = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace")[:1000]
        raise CheckpointError(
            f"cannot read pinned Git blob {commit}:{relative_path}: {message}"
        )
    return process.stdout


def git_text(*arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if process.returncode != 0:
        raise CheckpointError(
            f"git {' '.join(arguments)} failed: {process.stderr[:1000]}"
        )
    return process.stdout.strip()


def verify_source_pins() -> dict[str, object]:
    observed: dict[str, object] = {}
    head = git_text("rev-parse", "HEAD")
    for name, pin in SOURCE_PINS.items():
        path = REPOSITORY_ROOT / pin["path"]
        current_raw = path.read_bytes()
        current_digest = sha256_bytes(current_raw)
        if current_digest != pin["sha256"]:
            raise CheckpointError(
                f"{name} byte drift: expected {pin['sha256']}, got {current_digest}"
            )
        committed_raw = git_bytes(pin["introduced_in_commit"], pin["path"])
        committed_digest = sha256_bytes(committed_raw)
        if committed_digest != pin["sha256"]:
            raise CheckpointError(
                f"{name} introduction-commit blob does not match its byte pin"
            )
        ancestor = subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                pin["introduced_in_commit"],
                "HEAD",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if ancestor.returncode != 0:
            raise CheckpointError(
                f"{name} introduction commit is not an ancestor of HEAD"
            )
        observed[name] = {
            **pin,
            "observed_sha256": current_digest,
            "introduction_commit_blob_sha256": committed_digest,
            "current_bytes_match": True,
            "commit_blob_matches": True,
            "introduction_commit_is_ancestor_of_HEAD": True,
        }
    return {"git_HEAD": head, "files": observed}


def observed_extractor_provenance() -> dict[str, object]:
    relative_path = str(Path(__file__).resolve().relative_to(REPOSITORY_ROOT))
    raw = Path(__file__).read_bytes()
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative_path],
        cwd=REPOSITORY_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if not tracked:
        raise CheckpointError(
            "checkpoint extractor must be committed before numerical replay"
        )
    dirty_status = git_text("status", "--porcelain=v1", "--", relative_path)
    if dirty_status:
        raise CheckpointError(
            "checkpoint extractor must be clean before numerical replay"
        )
    latest_commit = git_text("log", "-1", "--format=%H", "--", relative_path)
    if not latest_commit:
        raise CheckpointError("checkpoint extractor has no committed path history")
    current_digest = sha256_bytes(raw)
    committed_digest = sha256_bytes(git_bytes(latest_commit, relative_path))
    if committed_digest != current_digest:
        raise CheckpointError(
            "checkpoint extractor bytes do not match their latest committed blob"
        )
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", latest_commit, "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if ancestor.returncode != 0:
        raise CheckpointError("checkpoint extractor commit is not an ancestor of HEAD")
    return {
        "path": relative_path,
        "observed_sha256": current_digest,
        "git_tracked": True,
        "git_clean_for_path": True,
        "latest_path_commit": latest_commit,
        "latest_commit_blob_sha256": committed_digest,
        "latest_commit_blob_matches_current_bytes": True,
        "latest_path_commit_is_ancestor_of_HEAD": True,
        "hard_self_pin_performed": True,
        "two_stage_protocol": "commit extractor first; run and capture checkpoint second",
        "future_binding_required": (
            "after capture, the Phase-42 manifest must pin this committed "
            "extractor and the captured CHECKPOINT_JSON before production"
        ),
    }


def repository_pycache_snapshot() -> dict[str, dict[str, object]]:
    excluded = {".git", ".venv", "node_modules"}
    snapshot: dict[str, dict[str, object]] = {}
    paths = list(REPOSITORY_ROOT.rglob("*.pyc")) + list(
        REPOSITORY_ROOT.rglob("*.pyo")
    )
    for path in sorted(set(paths)):
        relative = path.relative_to(REPOSITORY_ROOT)
        if any(part in excluded for part in relative.parts):
            continue
        stat = path.stat()
        snapshot[str(relative)] = {
            "sha256": sha256_bytes(path.read_bytes()),
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
    return snapshot


def backend_fingerprint(configuration: dict[str, object], kind: str) -> dict[str, object]:
    build_dependencies = configuration.get("Build Dependencies")
    if not isinstance(build_dependencies, dict):
        raise CheckpointError("runtime build-dependency metadata is unavailable")
    backend = build_dependencies.get(kind)
    if not isinstance(backend, dict):
        raise CheckpointError(f"runtime {kind} metadata is unavailable")
    result: dict[str, object] = {
        "name": backend.get("name"),
        "version": backend.get("version"),
        "openblas_configuration": backend.get("openblas configuration"),
    }
    if "has ilp64" in backend:
        result["has_ilp64"] = bool(backend["has ilp64"])
    return result


def verify_runtime() -> dict[str, object]:
    numpy_configuration = np.show_config(mode="dicts")
    scipy_configuration = scipy.show_config(mode="dicts")
    if not isinstance(numpy_configuration, dict) or not isinstance(
        scipy_configuration, dict
    ):
        raise CheckpointError("runtime configuration is not machine-readable")
    observed: dict[str, object] = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build": list(platform.python_build()),
        "python_compiler": platform.python_compiler(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "sympy_version": sp.__version__,
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
            name: os.environ.get(name)
            for name in EXPECTED_RUNTIME["thread_environment"]
        },
    }
    expected_executable = (REPOSITORY_ROOT / ".venv/bin/python").resolve()
    observed_executable = Path(sys.executable).resolve()
    if observed_executable != expected_executable:
        raise CheckpointError(
            f"wrong Python executable: expected {expected_executable}, got {observed_executable}"
        )
    if observed != EXPECTED_RUNTIME:
        raise CheckpointError(
            "runtime fingerprint drifted: "
            + json.dumps(
                {"expected": EXPECTED_RUNTIME, "observed": observed},
                sort_keys=True,
            )
        )
    return {
        "verified": True,
        "python_executable": str(observed_executable),
        "strict_fingerprint": observed,
    }


def import_phase41() -> ModuleType:
    module_path = REPOSITORY_ROOT / SOURCE_PINS["phase41_script"]["path"]
    digest_before = sha256_bytes(module_path.read_bytes())
    if digest_before != SOURCE_PINS["phase41_script"]["sha256"]:
        raise CheckpointError("Phase-41 module drifted before import")
    module_name = "ice_phase41_m4_checkpoint_source"
    specification = importlib.util.spec_from_file_location(module_name, module_path)
    if specification is None or specification.loader is None:
        raise CheckpointError("cannot construct the pinned Phase-41 module spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    digest_after = sha256_bytes(module_path.read_bytes())
    if digest_after != digest_before:
        raise CheckpointError("Phase-41 module changed during import")
    if module.INPUT_SHA256 != SOURCE_PINS["phase41_manifest"]["sha256"]:
        raise CheckpointError("Phase-41 embedded manifest hash pin drifted")
    if module.INPUT_COMMIT != SOURCE_PINS["phase41_manifest"]["introduced_in_commit"]:
        raise CheckpointError("Phase-41 embedded manifest commit pin drifted")
    return module


def canonical_array_sha256(array: np.ndarray) -> tuple[str, str]:
    values = np.asarray(array)
    if values.dtype.kind == "c":
        dtype = np.dtype("<c16")
    elif values.dtype.kind in ("f", "i", "u", "b"):
        dtype = np.dtype("<f8")
    else:
        raise CheckpointError(f"unsupported checkpoint array dtype {values.dtype}")
    canonical = np.ascontiguousarray(values, dtype=dtype)
    return sha256_bytes(canonical.tobytes(order="C")), dtype.str


class ShapeLedger:
    """Central fail-closed shape and finiteness ledger."""

    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}

    def require(
        self,
        label: str,
        array: object,
        expected_shape: tuple[int, ...],
    ) -> np.ndarray:
        if label in self.records:
            raise CheckpointError(f"duplicate critical-shape label: {label}")
        values = np.asarray(array)
        actual_shape = tuple(int(value) for value in values.shape)
        numeric = values.dtype.kind in ("b", "i", "u", "f", "c")
        finite = bool(numeric and np.all(np.isfinite(values)))
        shape_matches = actual_shape == expected_shape
        record: dict[str, object] = {
            "expected_shape": list(expected_shape),
            "actual_shape": list(actual_shape),
            "runtime_dtype": str(values.dtype),
            "shape_matches": shape_matches,
            "finite_numeric": finite,
            "passed": bool(shape_matches and finite),
        }
        if finite:
            record["canonical_little_endian_sha256"] = (
                canonical_array_sha256(values)[0]
            )
        self.records[label] = record
        if not record["passed"]:
            raise CheckpointError(
                f"critical array {label} expected {expected_shape}, got "
                f"{actual_shape}, dtype={values.dtype}, finite={finite}"
            )
        return values

    def payload(self) -> dict[str, object]:
        return {
            "fail_closed": True,
            "all_passed": all(
                bool(record["passed"]) for record in self.records.values()
            ),
            "checked_array_count": len(self.records),
            "records": self.records,
        }


def array_payload(array: np.ndarray, *, convention: str) -> dict[str, object]:
    values = np.asarray(array)
    if not np.all(np.isfinite(values)):
        raise CheckpointError(f"non-finite array reached checkpoint: {convention}")
    digest, canonical_dtype = canonical_array_sha256(values)
    return {
        "shape": list(values.shape),
        "runtime_dtype": str(values.dtype),
        "canonical_little_endian_dtype": canonical_dtype,
        "canonical_little_endian_sha256": digest,
        "complex_encoding": "terminal [real,imag] pairs" if np.iscomplexobj(values) else None,
        "convention": convention,
        "values": values,
    }


def json_ready(value: object) -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, (np.floating, float)):
        result = float(value)
        if not math.isfinite(result):
            raise CheckpointError("non-finite float reached CHECKPOINT_JSON")
        return result
    if isinstance(value, (np.complexfloating, complex)):
        result = complex(value)
        if not math.isfinite(result.real) or not math.isfinite(result.imag):
            raise CheckpointError("non-finite complex reached CHECKPOINT_JSON")
        return [float(result.real), float(result.imag)]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    raise CheckpointError(
        f"unsupported object in CHECKPOINT_JSON: {type(value).__name__}"
    )


def replay_phase41_prefix(
    phase41: ModuleType,
) -> dict[str, object]:
    manifest, raw_manifest, manifest_digest = phase41.load_manifest()
    if manifest_digest != SOURCE_PINS["phase41_manifest"]["sha256"]:
        raise CheckpointError("Phase-41 manifest drifted at replay time")
    if sha256_bytes(raw_manifest) != manifest_digest:
        raise CheckpointError("Phase-41 manifest digest is internally inconsistent")
    direction_source = manifest["upward_chart"]["phase39_direction_source"]
    expected_direction_source = {
        "script": SOURCE_PINS["phase39_script"]["path"],
        "script_sha256": SOURCE_PINS["phase39_script"]["sha256"],
        "script_commit": SOURCE_PINS["phase39_script"][
            "introduced_in_commit"
        ],
        "artifact": SOURCE_PINS["phase39_direction_report"]["path"],
        "artifact_sha256": SOURCE_PINS["phase39_direction_report"][
            "sha256"
        ],
        "artifact_commit": SOURCE_PINS["phase39_direction_report"][
            "introduced_in_commit"
        ],
    }
    if any(
        direction_source.get(key) != value
        for key, value in expected_direction_source.items()
    ):
        raise CheckpointError("Phase-41 declarations for Phase-39 chart inputs drifted")

    audit = phase41.Audit()
    exact_data = phase41.exact_contracts(audit, manifest, manifest_digest)
    if len(audit.exact_records) != 7 or audit.exact_passed != 7:
        raise CheckpointError("Phase-41 exact 7/7 prefix did not reproduce")
    mode_bases = (
        np.asarray(exact_data["DST_basis"], dtype=float),
        np.asarray(exact_data["nested_basis"], dtype=float),
    )

    saddle_w, saddle_records = phase41.solve_signed_saddle_grids(
        manifest, root_tolerance=1.0e-12
    )
    fixed = phase41.build_fixed_metric(saddle_w[(0.0, 0.0)])
    saddle_data = {
        point: phase41.make_saddle_data(
            phase41.numeric_model(*point), value, fixed
        )
        for point, value in saddle_w.items()
    }
    saddle_diagnostics = phase41.saddle_grid_diagnostics(
        saddle_records, saddle_data
    )
    audit.numerical(
        "P41.saddles.two_source_signed_grids",
        bool(saddle_diagnostics["passed"]),
        "all nine independently continued two-source grid saddles are resolved, nondegenerate, inertia-matched, and reflection-paired",
        failure_status="SOURCE_SCOPED_INCONCLUSIVE",
        details=saddle_diagnostics,
    )
    if not saddle_diagnostics["passed"]:
        raise CheckpointError("Phase-41 saddle grid failed its frozen diagnostics")

    # Preserve the production call order, including the independent solver-
    # tolerance repeat, before metric diagnostics and chart construction.
    response_primary = phase41.susceptibility_from_saddles(saddle_data)
    control_w, control_records = phase41.solve_signed_saddle_grids(
        manifest,
        root_tolerance=5.0e-10,
        zero_seed_override=saddle_w[(0.0, 0.0)],
    )
    control_data = {
        point: phase41.make_saddle_data(
            phase41.numeric_model(*point), value, fixed
        )
        for point, value in control_w.items()
    }
    control_saddle_diagnostics = phase41.saddle_grid_diagnostics(
        control_records, control_data
    )
    response_control = phase41.susceptibility_from_saddles(control_data)
    chi_half = np.asarray(response_primary["chi_half"], dtype=float)
    chi_full = np.asarray(response_primary["chi_full"], dtype=float)
    chi_half_control = np.asarray(response_control["chi_half"], dtype=float)
    chi_full_control = np.asarray(response_control["chi_full"], dtype=float)
    e_step = float(np.linalg.norm(chi_half - chi_full, ord=2))
    e_solver = max(
        float(np.linalg.norm(chi_half - chi_half_control, ord=2)),
        float(np.linalg.norm(chi_full - chi_full_control, ord=2)),
    )
    e_rank = e_step + e_solver
    singular_half = np.linalg.svd(chi_half, compute_uv=False)
    singular_full = np.linalg.svd(chi_full, compute_uv=False)
    reversal_max = max(response_primary["reversal_residuals"].values())
    stable_rank_two = bool(singular_half[-1] > 10.0 * e_rank)
    response_passed = bool(
        stable_rank_two
        and reversal_max <= 1.0e-7
        and control_saddle_diagnostics["passed"]
    )
    response_replay = {
        "reported_chi_is": "chi_half at h=.0005, not the pre-freeze chi_full spot",
        "control_repeat_arm_policy": (
            "the 5e-10 repeat re-solves one shared zero then independently "
            "continues each signed axis zero-to-half-to-full; target roots "
            "from the primary grid are not warm starts"
        ),
        "row_order": ["a_odd_over_a_b", "phi_odd_over_phi_b"],
        "column_order": ["delta_a", "delta_phi_over_phi_b"],
        "chi_half": chi_half,
        "chi_full": chi_full,
        "chi_half_control_root_tolerance_5e-10": chi_half_control,
        "chi_full_control_root_tolerance_5e-10": chi_full_control,
        "chi_half_singular_values": singular_half,
        "chi_full_singular_values": singular_full,
        "chi_half_determinant": float(np.linalg.det(chi_half)),
        "E_step_spectral": e_step,
        "E_solver_spectral": e_solver,
        "E_rank_nonrigorous": e_rank,
        "sigma_min_over_10_E_rank": float(
            singular_half[-1] / max(10.0 * e_rank, 1.0e-300)
        ),
        "reversal_residuals": response_primary["reversal_residuals"],
        "anchor_subtracted_outputs": response_primary["outputs"],
        "stable_numerical_rank_two_supported": stable_rank_two,
        "exact_algebraic_rank_deficiency_proved": False,
        "control_solver_records": control_records,
        "control_grid_saddle_diagnostics": control_saddle_diagnostics,
        "passed": response_passed,
    }
    audit.numerical(
        "P41.response.anchor_subtracted_two_source_matrix",
        response_passed,
        "the reported half-step susceptibility is tested against source reversal, step drift, and the independent predeclared solver-tolerance repeat without forcing its rank",
        failure_status="STABLE_NUMERICAL_RANK_TWO_NOT_SUPPORTED",
        details=response_replay,
    )
    if not response_passed:
        raise CheckpointError("Phase-41 response prefix did not reproduce")

    metric_diagnostics = phase41.metric_geometry_diagnostics(fixed, saddle_data)
    audit.numerical(
        "P41.metric.one_fixed_mobility_two_sources",
        bool(metric_diagnostics["passed"]),
        "one zero-source mobility is held fixed while signed projectors, transported frames, reflection, and every lambda-one Takagi identity are checked",
        failure_status="INVALID_RUN",
        details=metric_diagnostics,
    )
    if not metric_diagnostics["passed"]:
        raise CheckpointError("Phase-41 fixed metric failed its diagnostics")

    chart = phase41.build_nested_chart(
        manifest, saddle_data[(0.0, 0.0)], fixed
    )
    phase39 = sys.modules.get("ice_phase39_finite_joint_intersection")
    if phase39 is None:
        raise CheckpointError("Phase-39 transitive module was not imported")
    if (
        Path(phase39.__file__).resolve()
        != (REPOSITORY_ROOT / SOURCE_PINS["phase39_script"]["path"]).resolve()
        or Path(phase39.INPUT_PATH).resolve()
        != (REPOSITORY_ROOT / SOURCE_PINS["phase39_manifest"]["path"]).resolve()
        or phase39.INPUT_INTRODUCED_IN_COMMIT
        != SOURCE_PINS["phase39_manifest"]["introduced_in_commit"]
    ):
        raise CheckpointError("Phase-39 transitive runtime dependency drifted")
    (
        primary_parameters,
        primary_results,
        intermediate_results,
        seed_record,
    ) = phase41.solve_primary_intersections(
        manifest, saddle_data, fixed, chart, mode_bases
    )
    candidate_reflection_diagnostics = (
        phase41.candidate_reflection_diagnostics(primary_results)
    )
    expected_primary_labels = {
        "shared_zero",
        "phi_minus",
        "phi_plus",
        "a_minus",
        "a_plus",
    }
    all_five_accepted = bool(
        set(primary_results) == expected_primary_labels
        and set(primary_parameters) == expected_primary_labels
        and all(
            primary_results[label].get("accepted") is True
            for label in expected_primary_labels
        )
        and candidate_reflection_diagnostics["passed"] is True
    )
    if not all_five_accepted:
        raise CheckpointError(
            "the five-primary accepted/reflection Phase-41 prefix did not reproduce"
        )
    for label in TARGET_POINTS:
        result = primary_results.get(label)
        if (
            result is None
            or result.get("accepted") is not True
            or label not in primary_parameters
        ):
            raise CheckpointError(
                f"required Phase-41 primary {label} was not accepted"
            )

    return {
        "manifest": manifest,
        "audit": audit,
        "exact_data": exact_data,
        "mode_bases": mode_bases,
        "saddle_w": saddle_w,
        "saddle_records": saddle_records,
        "saddle_data": saddle_data,
        "saddle_diagnostics": saddle_diagnostics,
        "control_saddle_diagnostics": control_saddle_diagnostics,
        "response_replay": response_replay,
        "fixed": fixed,
        "metric_diagnostics": metric_diagnostics,
        "chart": chart,
        "primary_parameters": primary_parameters,
        "primary_results": primary_results,
        "intermediate_results": intermediate_results,
        "seed_record": seed_record,
        "candidate_reflection_diagnostics": candidate_reflection_diagnostics,
        "all_five_accepted_with_reflection": all_five_accepted,
        "phase39_dependency_closure": {
            "verified": True,
            "repository_files_actually_loaded_or_hashed": [
                SOURCE_PINS["phase39_script"]["path"],
                SOURCE_PINS["phase39_direction_report"]["path"],
                SOURCE_PINS["phase39_manifest"]["path"],
            ],
            "further_repository_executable_imports_observed": False,
            "phase39_embedded_input_commit": (
                phase39.INPUT_INTRODUCED_IN_COMMIT
            ),
        },
    }


def complex_state_from_pairs(values: object, *, label: str) -> np.ndarray:
    pairs = np.asarray(values, dtype=float)
    if pairs.shape != (7, 2) or not np.all(np.isfinite(pairs)):
        raise CheckpointError(f"{label} is not a finite seven-complex state")
    return pairs[:, 0] + 1.0j * pairs[:, 1]


def validate_static_critical_shapes(
    phase41: ModuleType,
    replay: dict[str, object],
    ledger: ShapeLedger,
) -> None:
    fixed = replay["fixed"]
    chart = replay["chart"]
    exact_data = replay["exact_data"]
    ledger.require("coordinates.scales", phase41.COORDINATE_SCALES, (7,))
    ledger.require(
        "coordinates.row_scales",
        np.repeat(1.0 / phase41.COORDINATE_SCALES, 2),
        (14,),
    )
    ledger.require(
        "modes.DST", np.asarray(exact_data["DST_basis"], dtype=float), (7, 7)
    )
    ledger.require(
        "modes.nested",
        np.asarray(exact_data["nested_basis"], dtype=float),
        (7, 7),
    )
    ledger.require(
        "modes.transition",
        np.asarray(exact_data["basis_transition"], dtype=float),
        (7, 7),
    )
    ledger.require("reflection.w", phase41.REFLECTION, (7, 7))
    ledger.require(
        "reflection.R14", np.kron(phase41.REFLECTION, np.eye(2)), (14, 14)
    )

    fixed_arrays = {
        "saddle_zero_w": (fixed.saddle_zero_w, (7,)),
        "hessian_zero_w": (fixed.hessian_zero_w, (7, 7)),
        "eigenvalues_zero": (fixed.eigenvalues_zero, (7,)),
        "oriented_eigenvectors_zero": (
            fixed.oriented_eigenvectors_zero,
            (7, 7),
        ),
        "linear_map": (fixed.linear_map, (7, 7)),
        "linear_map_z_from_xi": (
            np.diag(phase41.COORDINATE_SCALES) @ fixed.linear_map,
            (7, 7),
        ),
        "inverse_metric_mobility_w": (
            fixed.inverse_metric_mobility_w,
            (7, 7),
        ),
        "metric_tensor_w": (fixed.metric_tensor_w, (7, 7)),
        "xi_reflection": (fixed.xi_reflection, (7, 7)),
    }
    for name, (values, shape) in fixed_arrays.items():
        ledger.require(f"fixed.{name}", values, shape)
    ledger.require("chart.center", chart.center, (7,))
    ledger.require("chart.tangent", chart.tangent, (7, 6))

    saddle_data = replay["saddle_data"]
    for label, point in ALL_SADDLE_POINTS:
        data = saddle_data[point]
        prefix = f"saddle.{label}"
        arrays = {
            "w": (data.saddle_w, (7,)),
            "z": (data.saddle_z, (7,)),
            "hessian_w": (data.hessian_w, (7, 7)),
            "hessian_eigenvalues": (data.hessian_eigenvalues, (7,)),
            "hessian_xi": (data.hessian_xi, (7, 7)),
            "hessian_xi_eigenvalues": (
                data.hessian_xi_eigenvalues,
                (7,),
            ),
            "aligned_signed_frame_xi": (
                data.aligned_signed_frame_xi,
                (7, 7),
            ),
            "negative_restriction": (data.signed_restrictions[-1], (4, 4)),
            "positive_restriction": (data.signed_restrictions[1], (3, 3)),
            "negative_projector": (data.signed_projectors[-1], (7, 7)),
            "positive_projector": (data.signed_projectors[1], (7, 7)),
            "launch_lambda_0": (data.launch_matrix(0.0), (7, 7)),
            "launch_lambda_0.5": (data.launch_matrix(0.5), (7, 7)),
            "launch_lambda_1": (data.launch_matrix(1.0), (7, 7)),
        }
        for name, (values, shape) in arrays.items():
            ledger.require(f"{prefix}.{name}", values, shape)

    primary_parameters = replay["primary_parameters"]
    primary_results = replay["primary_results"]
    for label in ("shared_zero", "phi_minus", "phi_plus", "a_minus", "a_plus"):
        result = primary_results[label]
        ledger.require(
            f"primary.{label}.parameters", primary_parameters[label], (14,)
        )
        ledger.require(
            f"primary.{label}.variational_scaled_root_jacobian",
            result["variational_scaled_root_jacobian"],
            (14, 14),
        )
        ledger.require(
            f"primary.{label}.intersection_state_z",
            complex_state_from_pairs(
                result["intersection_z"], label=f"primary {label} intersection_z"
            ),
            (7,),
        )


def validate_disclosed_phase41_compatibility(
    replay: dict[str, object],
) -> dict[str, object]:
    """Fail closed on the scoped, published Phase-41 reproduction witnesses."""

    primary_results = replay["primary_results"]
    expected_labels = (
        "shared_zero",
        "phi_minus",
        "phi_plus",
        "a_minus",
        "a_plus",
    )
    orientation_records: dict[str, dict[str, object]] = {}
    for label in expected_labels:
        result = primary_results[label]
        direct_sign = int(result["direct_orientation"]["sign"])
        root_sign = int(
            result["assembled_root_jacobian_orientation"]["sign"]
        )
        passed = bool(direct_sign == 1 and root_sign == -1)
        orientation_records[label] = {
            "direct_sign": direct_sign,
            "required_direct_sign": 1,
            "root_sign": root_sign,
            "required_root_sign": -1,
            "passed": passed,
        }
        if not passed:
            raise CheckpointError(
                f"{label} did not reproduce the disclosed Phase-41 +1/-1 signs"
            )

    reflection = replay["candidate_reflection_diagnostics"]
    reflection_records: dict[str, dict[str, object]] = {}
    expected_reflections = DISCLOSED_PHASE41_WITNESSES[
        "reflection_physical_max_abs"
    ]
    reflection_tolerance = DISCLOSED_PHASE41_TOLERANCES[
        "reflection_physical_abs"
    ]
    for source in ("phi", "a"):
        source_record = reflection["sources"][source]
        physical_error = float(source_record["physical_reflection_max_abs"])
        normalized_error = float(
            source_record["normalized_reflection_max_abs"]
        )
        disclosed_value = float(expected_reflections[source])
        disclosed_difference = abs(physical_error - disclosed_value)
        passed = bool(
            source_record["passed"] is True
            and physical_error <= 2.0e-6
            and math.isfinite(normalized_error)
            and source_record["same_declared_direct_sign"] is True
            and source_record[
                "negative_endpoint_seeded_independently_from_zero"
            ]
            is True
            and disclosed_difference <= reflection_tolerance
        )
        reflection_records[source] = {
            "regenerated_summary": source_record,
            "pinned_report_rounded_physical_max_abs": disclosed_value,
            "absolute_difference": disclosed_difference,
            "nonselecting_rounding_tolerance": reflection_tolerance,
            "passed": passed,
        }
        if not passed:
            raise CheckpointError(
                f"{source} reflection summary did not reproduce the disclosed Phase-41 witness"
            )
    if reflection["passed"] is not True:
        raise CheckpointError("combined Phase-41 candidate reflection did not pass")

    response = replay["response_replay"]
    disclosed_chi = np.asarray(
        DISCLOSED_PHASE41_WITNESSES["chi_half"], dtype=float
    )
    disclosed_singular = np.asarray(
        DISCLOSED_PHASE41_WITNESSES["chi_half_singular_values"], dtype=float
    )
    regenerated_chi = np.asarray(response["chi_half"], dtype=float)
    regenerated_singular = np.asarray(
        response["chi_half_singular_values"], dtype=float
    )
    response_differences = {
        "chi_half_max_abs": float(
            np.max(np.abs(regenerated_chi - disclosed_chi))
        ),
        "chi_half_singular_values_max_abs": float(
            np.max(np.abs(regenerated_singular - disclosed_singular))
        ),
        "E_step_abs": abs(
            float(response["E_step_spectral"])
            - float(DISCLOSED_PHASE41_WITNESSES["E_step_spectral"])
        ),
        "E_solver_abs": abs(
            float(response["E_solver_spectral"])
            - float(DISCLOSED_PHASE41_WITNESSES["E_solver_spectral"])
        ),
        "sigma_ratio_abs": abs(
            float(response["sigma_min_over_10_E_rank"])
            - float(
                DISCLOSED_PHASE41_WITNESSES[
                    "sigma_min_over_10_E_rank"
                ]
            )
        ),
        "source_reversal_abs": abs(
            max(float(value) for value in response["reversal_residuals"].values())
            - float(DISCLOSED_PHASE41_WITNESSES["source_reversal_max"])
        ),
    }
    response_rounding_passed = all(
        response_differences[name] <= DISCLOSED_PHASE41_TOLERANCES[name]
        for name in response_differences
    )
    response_structural_passed = bool(
        response["passed"] is True
        and response["stable_numerical_rank_two_supported"] is True
        and response["exact_algebraic_rank_deficiency_proved"] is False
        and max(
            float(value) for value in response["reversal_residuals"].values()
        )
        <= 1.0e-7
        and response["control_grid_saddle_diagnostics"]["passed"] is True
    )
    if not response_rounding_passed or not response_structural_passed:
        raise CheckpointError(
            "response metrics did not reproduce the disclosed Phase-41 scoped witnesses"
        )

    return {
        "passed": True,
        "role": (
            "post-solve compatibility check against rounded values in the "
            "byte-pinned Phase-41 report; not a seed, root selector, or "
            "desired-outcome input"
        ),
        "historical_stdout_or_vector_identity_established": False,
        "all_five_orientation_signs": orientation_records,
        "signed_source_reflection_summaries": reflection_records,
        "response": {
            "regenerated": response,
            "pinned_report_rounded_witnesses": (
                DISCLOSED_PHASE41_WITNESSES
            ),
            "absolute_differences": response_differences,
            "nonselecting_rounding_tolerances": (
                DISCLOSED_PHASE41_TOLERANCES
            ),
            "structural_contract_passed": response_structural_passed,
            "rounded_report_compatibility_passed": response_rounding_passed,
        },
    }


def verify_pre_emit_TOCTOU_guard(context: dict[str, object]) -> None:
    """Recheck every long-run provenance input immediately before stdout."""

    if sys.dont_write_bytecode is not True:
        raise CheckpointError("sys.dont_write_bytecode changed during replay")
    source_end = verify_source_pins()
    extractor_end = observed_extractor_provenance()
    runtime_end = verify_runtime()
    pycache_end = repository_pycache_snapshot()
    comparisons = {
        "source_pins_HEAD_and_commit_blobs": source_end == context["source"],
        "extractor_self_blob_and_HEAD": extractor_end == context["extractor"],
        "runtime_fingerprint": runtime_end == context["runtime"],
        "repository_pycache_snapshot": pycache_end == context["pycache"],
    }
    failed = [name for name, passed in comparisons.items() if not passed]
    if failed:
        raise CheckpointError(
            "pre-emit TOCTOU guard detected drift in: " + ", ".join(failed)
        )


def saddle_payload(
    phase41: ModuleType,
    label: str,
    point: tuple[float, float],
    replay: dict[str, object],
) -> dict[str, object]:
    saddle_records = replay["saddle_records"]
    saddle_data = replay["saddle_data"]
    record = saddle_records[point]  # type: ignore[index]
    data = saddle_data[point]  # type: ignore[index]
    return {
        "label": label,
        "source_point": {"delta_a": point[0], "delta_phi": point[1]},
        "solver_record": record,
        "saddle_w": array_payload(
            data.saddle_w, convention="dimensionless w coordinates"
        ),
        "saddle_z": array_payload(
            data.saddle_z, convention="physical z = COORDINATE_SCALES * w"
        ),
        "action": data.action,
        "gradient_max_abs": data.gradient_max_abs,
        "hessian_w": array_payload(
            data.hessian_w, convention="real Hessian in dimensionless w coordinates"
        ),
        "hessian_eigenvalues": array_payload(
            data.hessian_eigenvalues, convention="ascending eigvalsh(H_w)"
        ),
        "hessian_inertia": data.hessian_inertia,
        "hessian_xi": array_payload(
            data.hessian_xi, convention="L.T @ H_w @ L"
        ),
        "hessian_xi_eigenvalues": array_payload(
            data.hessian_xi_eigenvalues,
            convention="Phase-41 signed-subspace eigenvalue order",
        ),
        "aligned_signed_frame_xi": array_payload(
            data.aligned_signed_frame_xi,
            convention="orientation-controlled signed-subspace frame in xi",
        ),
        "signed_restrictions": {
            "negative": array_payload(
                data.signed_restrictions[-1],
                convention="-F_minus.T @ H_xi @ F_minus",
            ),
            "positive": array_payload(
                data.signed_restrictions[1],
                convention="F_plus.T @ H_xi @ F_plus",
            ),
        },
        "signed_projectors": {
            "negative": array_payload(
                data.signed_projectors[-1],
                convention="negative signed-subspace projector in xi",
            ),
            "positive": array_payload(
                data.signed_projectors[1],
                convention="positive signed-subspace projector in xi",
            ),
        },
        "signed_subspace_min_principal_overlap": (
            data.signed_subspace_min_principal_overlap
        ),
        "launch_matrices": {
            "lambda_0": array_payload(
                data.launch_matrix(0.0),
                convention="Phase-41 signed launch matrix, shape_lambda=0",
            ),
            "lambda_0.5": array_payload(
                data.launch_matrix(0.5),
                convention="Phase-41 signed launch matrix, shape_lambda=0.5",
            ),
            "lambda_1": array_payload(
                data.launch_matrix(1.0),
                convention="Phase-41 primary signed launch matrix, shape_lambda=1",
            ),
        },
    }


def target_intersection_payload(
    phase41: ModuleType,
    label: str,
    point: tuple[float, float],
    replay: dict[str, object],
    shape_ledger: ShapeLedger,
) -> dict[str, object]:
    parameters = np.asarray(
        replay["primary_parameters"][label], dtype=float  # type: ignore[index]
    )
    shape_ledger.require(f"target.{label}.parameters", parameters, (14,))
    result = replay["primary_results"][label]  # type: ignore[index]
    if parameters.shape != (14,):
        raise CheckpointError(f"{label} parameter vector is not length 14")
    recorded_parameters = np.asarray(result["parameters"], dtype=float)
    if not np.array_equal(parameters, recorded_parameters):
        raise CheckpointError(f"{label} parameter/result vectors differ")
    model = phase41.numeric_model(*point)
    saddle = replay["saddle_data"][point]  # type: ignore[index]
    fixed = replay["fixed"]
    chart = replay["chart"]
    (
        scaled_residual,
        regenerated_jacobian,
        gamma_state,
        k_state,
        gamma_frame,
        k_frame,
        integration,
    ) = phase41.residual_and_variational_jacobian(
        parameters,
        model,
        saddle,
        fixed,
        chart,
        float(result["sphere_radius"]),
        float(result["shape_lambda"]),
        "DOP853",
    )
    authoritative_jacobian = np.asarray(
        result["variational_scaled_root_jacobian"], dtype=float
    )
    shape_ledger.require(
        f"target.{label}.authoritative_J", authoritative_jacobian, (14, 14)
    )
    if authoritative_jacobian.shape != (14, 14):
        raise CheckpointError(f"{label} stored variational Jacobian is not 14x14")
    if regenerated_jacobian.shape != (14, 14):
        raise CheckpointError(f"{label} regenerated variational Jacobian is not 14x14")
    shape_ledger.require(
        f"target.{label}.regenerated_J", regenerated_jacobian, (14, 14)
    )
    shape_ledger.require(
        f"target.{label}.scaled_residual", scaled_residual, (14,)
    )
    shape_ledger.require(f"target.{label}.gamma_state_z", gamma_state, (7,))
    shape_ledger.require(f"target.{label}.k_state_z", k_state, (7,))
    shape_ledger.require(
        f"target.{label}.gamma_frame_z", gamma_frame, (14, 7)
    )
    shape_ledger.require(f"target.{label}.k_frame_z", k_frame, (14, 7))
    jacobian_difference = float(
        np.max(np.abs(regenerated_jacobian - authoritative_jacobian))
    )
    if jacobian_difference > 5.0e-11:
        raise CheckpointError(
            f"{label} regenerated Jacobian differs from the Phase-41 result by {jacobian_difference}"
        )
    row_scales = np.repeat(1.0 / phase41.COORDINATE_SCALES, 2)
    assembled = row_scales[:, np.newaxis] * np.column_stack(
        [gamma_frame, -k_frame]
    )
    assembly_error = float(
        np.max(np.abs(assembled - regenerated_jacobian))
    )
    if assembly_error > 5.0e-14:
        raise CheckpointError(f"{label} [scaled Gamma,-scaled K] assembly drifted")
    omega, direction_derivative = chart.direction(parameters[7:13])
    launch_matrix = saddle.launch_matrix(float(result["shape_lambda"]))
    initial_xi = float(result["sphere_radius"]) * (launch_matrix @ omega)
    physical_residual = phase41.interleaved(gamma_state - k_state)
    shape_ledger.require(f"target.{label}.chart_u", parameters[7:13], (6,))
    shape_ledger.require(f"target.{label}.omega", omega, (7,))
    shape_ledger.require(
        f"target.{label}.domega_du", direction_derivative, (7, 6)
    )
    shape_ledger.require(
        f"target.{label}.launch_matrix", launch_matrix, (7, 7)
    )
    shape_ledger.require(f"target.{label}.initial_xi", initial_xi, (7,))
    shape_ledger.require(
        f"target.{label}.physical_residual", physical_residual, (14,)
    )
    recorded_gamma_state = np.asarray(
        [complex(value[0], value[1]) for value in result["intersection_z"]],
        dtype=np.complex128,
    )
    shape_ledger.require(
        f"target.{label}.recorded_gamma_state_z",
        recorded_gamma_state,
        (7,),
    )
    gamma_state_difference = float(
        np.max(np.abs(gamma_state - recorded_gamma_state))
    )
    regenerated_scaled_max = float(np.max(np.abs(scaled_residual)))
    regenerated_physical_max = float(np.max(np.abs(physical_residual)))
    regenerated_physical_norm = float(np.linalg.norm(physical_residual))
    residual_summary_difference = max(
        abs(regenerated_scaled_max - float(result["scaled_residual_max_abs"])),
        abs(regenerated_physical_max - float(result["physical_residual_max_abs"])),
        abs(regenerated_physical_norm - float(result["physical_residual_norm"])),
    )
    if gamma_state_difference > 5.0e-11:
        raise CheckpointError(
            f"{label} regenerated Gamma state differs from the Phase-41 result"
        )
    if residual_summary_difference > 5.0e-11:
        raise CheckpointError(
            f"{label} regenerated residual summary differs from the Phase-41 result"
        )
    direct_orientation = phase41.matrix_orientation(
        np.column_stack([gamma_frame, k_frame])
    )
    root_orientation = phase41.matrix_orientation(
        np.column_stack([gamma_frame, -k_frame])
    )
    if direct_orientation["sign"] != result["direct_orientation"]["sign"]:
        raise CheckpointError(f"{label} direct orientation sign drifted")
    if (
        root_orientation["sign"]
        != result["assembled_root_jacobian_orientation"]["sign"]
    ):
        raise CheckpointError(f"{label} root orientation sign drifted")
    return {
        "source_point": {"delta_a": point[0], "delta_phi": point[1]},
        "accepted": True,
        "phase41_primary_result": result,
        "parameter_vector": array_payload(
            parameters,
            convention=(
                "[y_a1,y_phi1,y_a2,y_phi2,y_a3,y_phi3,psi,"
                "u1,u2,u3,u4,u5,u6,flow_time]"
            ),
        ),
        "variational_scaled_root_jacobian": array_payload(
            authoritative_jacobian,
            convention=(
                "row-scaled residual Jacobian [scaled V_Gamma, -scaled V_K]; "
                "column 13 is -scaled K flow-time tangent"
            ),
        ),
        "post_solve_strict_DOP853_reevaluation": {
            "historical_cached_endpoint_identity_claimed": False,
            "regenerated_vs_recorded_J_max_abs": jacobian_difference,
            "explicit_block_assembly_max_abs": assembly_error,
            "regenerated_vs_recorded_Gamma_state_max_abs": (
                gamma_state_difference
            ),
            "regenerated_vs_recorded_residual_summary_max_abs": (
                residual_summary_difference
            ),
            "scaled_residual_interleaved": array_payload(
                scaled_residual,
                convention="interleaved (Gamma_z-K_z)/COORDINATE_SCALES",
            ),
            "physical_residual_interleaved": array_payload(
                physical_residual,
                convention="interleaved Gamma_z-K_z",
            ),
            "gamma_state_z": array_payload(
                gamma_state,
                convention="Gamma cap state in physical z coordinates",
            ),
            "k_state_z": array_payload(
                k_state,
                convention="strict DOP853 K-flow endpoint in physical z coordinates",
            ),
            "gamma_frame_z": array_payload(
                gamma_frame,
                convention="unscaled physical real Gamma tangent frame, R14xR7",
            ),
            "k_frame_z": array_payload(
                k_frame,
                convention="unscaled physical real K tangent frame, R14xR7",
            ),
            "regenerated_scaled_root_jacobian": array_payload(
                regenerated_jacobian,
                convention="positive row scaling applied to [Gamma,-K]",
            ),
            "direct_orientation_unscaled": direct_orientation,
            "root_orientation_unscaled": root_orientation,
            "integration": integration,
        },
        "chart_at_root": {
            "parameters_u": array_payload(
                parameters[7:13], convention="six local chart parameters"
            ),
            "omega": array_payload(
                omega, convention="normalized S6 launch direction"
            ),
            "direction_derivative": array_payload(
                direction_derivative,
                convention="d omega / d u in the frozen chart",
            ),
            "launch_matrix": array_payload(
                launch_matrix,
                convention=f"signed launch matrix at shape_lambda={result['shape_lambda']}",
            ),
            "initial_xi": array_payload(
                initial_xi,
                convention="sphere_radius * launch_matrix @ omega",
            ),
        },
        "orientation_semantics": {
            "direct_matrix": "unscaled physical [V_Gamma,V_K]",
            "root_matrix": "unscaled physical [V_Gamma,-V_K]",
            "stored_J_matrix": "positive row-scaled [V_Gamma,-V_K]",
            "signs_survive_positive_row_scaling": True,
            "normalized_singular_spectra_survive_row_scaling": False,
        },
        "residual_summary": {
            "scaled_max_abs": result["scaled_residual_max_abs"],
            "physical_max_abs": result["physical_residual_max_abs"],
            "physical_norm": result["physical_residual_norm"],
        },
        "window_margins": result["window_margins"],
        "window_margins_passed": result["window_margins_passed"],
        "flow_ledger": result["flow_ledger"],
    }


def build_checkpoint() -> tuple[dict[str, object], dict[str, object]]:
    if sys.dont_write_bytecode is not True:
        raise CheckpointError("bytecode generation must be disabled before replay")
    pycache_provenance = repository_pycache_snapshot()
    source_provenance = verify_source_pins()
    extractor_provenance = observed_extractor_provenance()
    runtime_provenance = verify_runtime()
    guard_context: dict[str, object] = {
        "source": source_provenance,
        "extractor": extractor_provenance,
        "runtime": runtime_provenance,
        "pycache": pycache_provenance,
    }
    phase41 = import_phase41()
    with contextlib.redirect_stdout(sys.stderr):
        replay = replay_phase41_prefix(phase41)

    shape_ledger = ShapeLedger()
    validate_static_critical_shapes(phase41, replay, shape_ledger)
    disclosed_compatibility = validate_disclosed_phase41_compatibility(
        replay
    )

    fixed = replay["fixed"]
    chart = replay["chart"]
    exact_data = replay["exact_data"]
    dst = np.asarray(exact_data["DST_basis"], dtype=float)
    nested = np.asarray(exact_data["nested_basis"], dtype=float)
    transition = np.asarray(exact_data["basis_transition"], dtype=float)
    reflection_real = np.kron(phase41.REFLECTION, np.eye(2))
    row_scales = np.repeat(1.0 / phase41.COORDINATE_SCALES, 2)

    saddles = {
        label: saddle_payload(phase41, label, point, replay)
        for label, point in ALL_SADDLE_POINTS
    }
    target_intersections = {
        label: target_intersection_payload(
            phase41, label, point, replay, shape_ledger
        )
        for label, point in TARGET_POINTS.items()
    }
    shape_ledger_payload = shape_ledger.payload()
    if (
        shape_ledger_payload["all_passed"] is not True
        or shape_ledger_payload["checked_array_count"] != 204
    ):
        raise CheckpointError(
            "critical-array ledger is incomplete or contains a failed shape"
        )
    all_primary_parameters = {
        label: array_payload(
            values,
            convention=(
                "[six Gamma y, psi, six chart u, flow_time] in the "
                "Phase-41 frozen parameterization"
            ),
        )
        for label, values in replay["primary_parameters"].items()
    }
    completion_ledger = dict(
        replay["manifest"]["required_fail_closed_outputs"]
    )
    false_count = sum(value is False for value in completion_ledger.values())
    required_null_keys = (
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "quantum_gravity_explanation",
    )
    if (
        false_count != 16
        or any(completion_ledger[key] is not None for key in required_null_keys)
        or completion_ledger.get("gate1_status") != "OPEN_PARTIAL_PROGRESS"
    ):
        raise CheckpointError("Phase-41 fail-closed completion ledger drifted")

    checkpoint: dict[str, object] = {
        "schema": CHECKPOINT_SCHEMA,
        "phase": 42,
        "source_phase": 41,
        "checkpoint_status": "POST_HOC_REGENERATED_CHECKPOINT",
        "scientific_provenance": {
            "post_hoc_regenerated": True,
            "is_original_phase41_stdout": False,
            "historical_phase41_stdout_archived": False,
            "historical_stdout_identity_verified": False,
            "historical_root_vector_identity_verified": False,
            "historical_stdout_sha256": None,
            "phase42_manifest_consumed_by_this_extractor": False,
            "phase42_manifest_pin_deferred_until_checkpoint_capture": True,
            "statement": (
                "This checkpoint was regenerated from byte-pinned committed "
                "Phase-41 sources after the production run. It is suitable "
                "as a new Phase-42 input only after its own output is captured "
                "and pinned; it does not retroactively identify the unarchived "
                "historical stdout or cached in-memory root."
            ),
        },
        "source_and_lock_provenance": source_provenance,
        "extractor_provenance": extractor_provenance,
        "runtime_provenance": runtime_provenance,
        "repository_write_and_TOCTOU_policy": {
            "sys_dont_write_bytecode": True,
            "file_write_policy": "stdout/stderr only; no repository file writes",
            "repository_pycache_snapshot_start_count": len(
                pycache_provenance
            ),
            "repository_pycache_must_be_byte_and_metadata_identical_at_emit": True,
            "source_bytes_commits_ancestry_HEAD_self_blob_and_runtime_must_be_identical_at_emit": True,
            "pre_emit_guard_passed_if_and_only_if_CHECKPOINT_JSON_is_emitted": True,
            "drift_policy": "stderr CHECKPOINT_ERROR, exit 2, no checkpoint stdout",
        },
        "replay_contract": {
            "stdout_policy": "one CHECKPOINT_JSON record; imported progress is stderr",
            "file_write_policy": "no files written",
            "call_order": [
                "load_manifest",
                "exact_contracts (7/7 required)",
                "solve_signed_saddle_grids(root_tolerance=1e-12)",
                "build_fixed_metric(shared_zero)",
                "make_saddle_data(primary grid)",
                "saddle_grid_diagnostics",
                "susceptibility_from_saddles(primary)",
                "solve_signed_saddle_grids(root_tolerance=5e-10, shared-zero override)",
                "make_saddle_data(control grid)",
                "saddle_grid_diagnostics(control)",
                "susceptibility_from_saddles(control)",
                "metric_geometry_diagnostics",
                "build_nested_chart",
                "solve_primary_intersections",
                "candidate_reflection_diagnostics",
                "post-solve strict DOP853 extraction at shared_zero/phi_plus/a_plus",
            ],
            "required_accepted_targets": list(TARGET_POINTS),
            "primary_sphere_radius": phase41.PRIMARY_SPHERE_RADIUS,
            "shape_lambda": 1.0,
            "exact_records": replay["audit"].exact_records,
            "prefix_numerical_records": replay["audit"].numerical_records,
            "saddle_grid_diagnostics": replay["saddle_diagnostics"],
            "control_saddle_grid_diagnostics": replay[
                "control_saddle_diagnostics"
            ],
            "response_replay": replay["response_replay"],
            "fixed_metric_diagnostics": replay["metric_diagnostics"],
            "phase39_transitive_dependency_closure": replay[
                "phase39_dependency_closure"
            ],
            "disclosed_phase41_compatibility": disclosed_compatibility,
        },
        "critical_array_shape_and_finiteness_ledger": shape_ledger_payload,
        "coordinate_and_orientation_conventions": {
            "complex_dimension": phase41.COMPLEX_DIMENSION,
            "ambient_real_dimension": phase41.AMBIENT_REAL_DIMENSION,
            "complex_coordinate_order": [
                "a1",
                "phi1",
                "a2",
                "phi2",
                "a3",
                "phi3",
                "T",
            ],
            "realification_order": (
                "interleaved [Re a1,Im a1,Re phi1,Im phi1,...,Re T,Im T]"
            ),
            "parameter_order": [
                "y_a1",
                "y_phi1",
                "y_a2",
                "y_phi2",
                "y_a3",
                "y_phi3",
                "psi",
                "u1",
                "u2",
                "u3",
                "u4",
                "u5",
                "u6",
                "flow_time",
            ],
            "coordinate_scales": array_payload(
                phase41.COORDINATE_SCALES,
                convention="z = COORDINATE_SCALES * w",
            ),
            "row_scales": array_payload(
                row_scales,
                convention="interleaved residual row scale 1/COORDINATE_SCALES",
            ),
            "cap_radius": phase41.CAP_RADIUS,
            "primary_sphere_radius": phase41.PRIMARY_SPHERE_RADIUS,
            "primary_shape_lambda": 1.0,
            "stored_variational_J": (
                "row_scales[:,None] * column_stack([V_Gamma,-V_K]); "
                "the last column is -scaled K flow-time tangent"
            ),
        },
        "mode_and_reflection_maps": {
            "DST_basis": array_payload(
                dst, convention="Phase-41 positively oriented DST basis"
            ),
            "nested_basis": array_payload(
                nested, convention="Phase-41 positively oriented nested basis"
            ),
            "DST_to_nested_transition": array_payload(
                transition, convention="solve(DST,nested)"
            ),
            "reflection_w": array_payload(
                phase41.REFLECTION,
                convention="node reflection in seven complex w coordinates",
            ),
            "reflection_R14_interleaved": array_payload(
                reflection_real,
                convention="kron(reflection_w,I2) in interleaved R14",
            ),
        },
        "fixed_metric": {
            "saddle_zero_w": array_payload(
                fixed.saddle_zero_w, convention="shared zero saddle in w"
            ),
            "hessian_zero_w": array_payload(
                fixed.hessian_zero_w, convention="shared-zero H_w"
            ),
            "eigenvalues_zero": array_payload(
                fixed.eigenvalues_zero, convention="ascending eigvalsh(H_w0)"
            ),
            "oriented_eigenvectors_zero": array_payload(
                fixed.oriented_eigenvectors_zero,
                convention="det-positive deterministic H_w0 eigenframe",
            ),
            "linear_map": array_payload(
                fixed.linear_map,
                convention="L=O*abs(Lambda)^(-1/2), maps xi to w",
            ),
            "linear_map_z_from_xi": array_payload(
                np.diag(phase41.COORDINATE_SCALES) @ fixed.linear_map,
                convention="diag(COORDINATE_SCALES) @ L",
            ),
            "inverse_metric_mobility_w": array_payload(
                fixed.inverse_metric_mobility_w,
                convention="M=L@L.T, held fixed for all sources",
            ),
            "metric_tensor_w": array_payload(
                fixed.metric_tensor_w, convention="inverse(M)"
            ),
            "xi_reflection": array_payload(
                fixed.xi_reflection,
                convention="solve(L, REFLECTION@L)",
            ),
            "diagnostics": replay["metric_diagnostics"],
        },
        "upward_chart": {
            "center": array_payload(
                chart.center, convention="normalized coefficient center on S6"
            ),
            "tangent": array_payload(
                chart.tangent,
                convention="det-positive 7x6 tangent frame at chart center",
            ),
            "orientation_determinant": chart.orientation_determinant,
            "provenance": chart.provenance,
        },
        "saddles": saddles,
        "primary_intersections": {
            "all_parameter_vectors": all_primary_parameters,
            "all_phase41_results": replay["primary_results"],
            "positive_half_step_continuations": replay[
                "intermediate_results"
            ],
            "deterministic_seed_record": replay["seed_record"],
            "candidate_reflection_diagnostics": replay[
                "candidate_reflection_diagnostics"
            ],
            "phase42_fixed_root_targets": target_intersections,
        },
        "phase41_fail_closed_completion_ledger": completion_ledger,
        "scope_guard": {
            "checkpoint_contains": [
                "post-hoc regenerated Phase-41 deterministic prefix",
                "nine primary saddle records and full local saddle tensors",
                "one fixed mobility and reflection maps",
                "the frozen chart center, tangent, and Phase-39 provenance",
                "all five local primary result records and parameter vectors",
                "full strict-map states, frames, residuals, and 14x14 J at three Phase-42 targets",
            ],
            "checkpoint_does_not_establish": [
                "identity with unarchived Phase-41 stdout or cached root bytes",
                "finite-difference tangent convergence",
                "source robustness or a cross-cutoff determinant line",
                "global arms, reintersections, root exhaustion, or good ends",
                "a physical original cycle or global intersection integer",
                "cutoff/continuum limits, BFV/Pfaffian/Pin data, SUSY, or quantum gravity",
            ],
        },
    }
    ready_without_digest = json_ready(checkpoint)
    canonical_without_digest = json.dumps(
        ready_without_digest,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    checkpoint["checkpoint_payload_sha256_without_self"] = sha256_bytes(
        canonical_without_digest
    )
    return checkpoint, guard_context


def main() -> None:
    try:
        checkpoint, guard_context = build_checkpoint()
        ready = json_ready(checkpoint)
        encoded = json.dumps(
            ready,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        verify_pre_emit_TOCTOU_guard(guard_context)
    except Exception as error:
        print(
            "CHECKPOINT_ERROR="
            + json.dumps(
                {
                    "status": "INVALID_CHECKPOINT_RUN",
                    "error_type": type(error).__name__,
                    "message": str(error)[:4000],
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(2) from error
    print("CHECKPOINT_JSON=" + encoded, flush=True)


if __name__ == "__main__":
    main()
