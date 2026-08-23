#!/usr/bin/env python3
"""Phase 51: one frozen nonlinear m=5 Gamma--K local continuation.

The calculation starts from the independently archived Phase-42 ``phi_plus``
R14 root, adds the two Phase-50 stabilizer directions, and follows the full
R18 Gamma--K equation over the Phase-50 action/metric bridge.  Every K point
is obtained by integrating the nonlinear downward holomorphic-gradient flow;
the transported tangent plane by itself is never used as an intersection.

The program writes no files.  Progress goes to stderr and exactly one
``RESULT_JSON=...`` record goes to stdout.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import platform
import sys
import traceback
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

sys.dont_write_bytecode = True

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json"
)
PHASE41_SOURCE_PATH = SCRIPT_PATH.with_name(
    "phase41_m4_two_source_intersection.py"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE49_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_RESULT.json"
)
PHASE50_SOURCE_PATH = SCRIPT_PATH.with_name(
    "phase50_m4_m5_joint_saddle_homotopy.py"
)
PHASE50_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE50_M4_M5_JOINT_SADDLE_HOMOTOPY_RESULT.json"
)

# Replaced only after the frozen manifest has its own commit.
INPUT_COMMIT = "80dda66aa57276de6e3940c35e58e89d34d28721"
INPUT_SHA256 = "0e9191d5c98cc1a56d7ffbcdd98ac02558457b87b6abf518ff754fbf4af7bd87"

RESULT_SCHEMA = "ice-phase51-m5-gamma-k-local-continuation/v1"
RESULT_PREFIX = "RESULT_JSON="
M4_DIMENSION = 7
M5_DIMENSION = 9
REAL_DIMENSION = 18
CSE_EXACT_LEDGER: list[dict[str, Any]] = []


class InvalidRun(RuntimeError):
    """A frozen input, exact convention, or serialization invariant failed."""


class NumericalFailure(RuntimeError):
    """A declared numerical operation failed without proving nonexistence."""


def progress(message: str) -> None:
    print(f"[Phase51] {message}", file=sys.stderr, flush=True)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path.name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def load_unique_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            output[key] = value
        return output

    payload = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(
            InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
        ),
    )
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")
    return payload, raw


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            array = np.asarray(value, dtype=np.complex128)
            return {
                "shape": list(array.shape),
                "complex128_pairs": [
                    [float(item.real), float(item.imag)]
                    for item in array.reshape(-1)
                ],
            }
        return np.asarray(value).tolist()
    if isinstance(value, np.complexfloating):
        return [float(value.real), float(value.imag)]
    if isinstance(value, np.floating):
        result = float(value)
        if not math.isfinite(result):
            raise InvalidRun("attempted to retain a nonfinite NumPy float")
        return result
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, complex):
        return [float(value.real), float(value.imag)]
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise InvalidRun("attempted to retain a nonfinite float")
    return value


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    output = dict(payload)
    output["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(output)
    ).hexdigest()
    return output


def verify_self_digest(payload: Mapping[str, Any], *, label: str) -> str:
    keys = (
        "result_payload_sha256_without_self",
        "checkpoint_payload_sha256_without_self",
    )
    key = next((candidate for candidate in keys if candidate in payload), None)
    if key is None:
        raise InvalidRun(f"{label} has no self-excluding digest")
    expected = str(payload[key])
    without = dict(payload)
    without.pop(key, None)
    observed = hashlib.sha256(canonical_bytes(without)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


def require(mapping: Mapping[str, Any], key: str, *, where: str) -> Any:
    if key not in mapping:
        raise InvalidRun(f"missing {where}.{key}")
    return mapping[key]


def finite_float(value: Any, *, label: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise InvalidRun(f"nonfinite {label}")
    return result


def finite_vector(value: Any, length: int, *, label: str) -> np.ndarray:
    result = np.asarray(value, dtype=float)
    if result.shape != (length,) or not np.all(np.isfinite(result)):
        raise InvalidRun(f"invalid {label}; expected finite shape {(length,)}")
    return result


def decode_array(record: Any, *, label: str) -> np.ndarray:
    if not isinstance(record, Mapping):
        result = np.asarray(record)
        if not np.all(np.isfinite(result)):
            raise InvalidRun(f"nonfinite array: {label}")
        return result
    shape = tuple(int(value) for value in require(record, "shape", where=label))
    values = require(record, "values", where=label)
    if record.get("complex_encoding") is not None:
        pairs = np.asarray(values, dtype=float)
        if pairs.shape != shape + (2,):
            raise InvalidRun(f"complex-pair shape drift: {label}")
        result = pairs[..., 0] + 1.0j * pairs[..., 1]
    else:
        result = np.asarray(values, dtype=float)
        if result.shape != shape:
            raise InvalidRun(f"array shape drift: {label}")
    if not np.all(np.isfinite(result)):
        raise InvalidRun(f"nonfinite array: {label}")
    return result


def interleaved(vector: np.ndarray) -> np.ndarray:
    values = np.asarray(vector, dtype=np.complex128).reshape(-1)
    result = np.empty(2 * values.size, dtype=float)
    result[0::2] = values.real
    result[1::2] = values.imag
    return result


def real_frame(frame: np.ndarray) -> np.ndarray:
    values = np.asarray(frame, dtype=np.complex128)
    result = np.empty((2 * values.shape[0], values.shape[1]), dtype=float)
    result[0::2, :] = values.real
    result[1::2, :] = values.imag
    return result


def symmetric_power(matrix: np.ndarray, exponent: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(np.asarray(matrix, dtype=float))
    if float(np.min(values)) <= 0.0:
        raise InvalidRun("mobility is not SPD")
    return (vectors * values**exponent) @ vectors.T


def geodesic_spd(left: np.ndarray, right: np.ndarray, value: float) -> np.ndarray:
    left_half = symmetric_power(left, 0.5)
    left_inverse_half = symmetric_power(left, -0.5)
    relative = left_inverse_half @ right @ left_inverse_half
    return left_half @ symmetric_power(relative, float(value)) @ left_half


def deterministic_oriented_eigenframe(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(
        0.5 * (np.asarray(matrix, dtype=float) + np.asarray(matrix, dtype=float).T)
    )
    for column in range(vectors.shape[1]):
        pivot = int(np.argmax(np.abs(vectors[:, column])))
        if vectors[pivot, column] < 0.0:
            vectors[:, column] *= -1.0
    if float(np.linalg.det(vectors)) < 0.0:
        vectors[:, -1] *= -1.0
    return values, vectors


def deterministic_oriented_null_frame(center: np.ndarray) -> tuple[np.ndarray, float]:
    unit = np.asarray(center, dtype=float).reshape(M5_DIMENSION)
    unit /= np.linalg.norm(unit)
    columns: list[np.ndarray] = []
    for index in range(M5_DIMENSION):
        candidate = np.eye(M5_DIMENSION)[:, index].copy()
        candidate -= unit * float(unit @ candidate)
        for known in columns:
            candidate -= known * float(known @ candidate)
        norm = float(np.linalg.norm(candidate))
        if norm > 1.0e-12:
            columns.append(candidate / norm)
        if len(columns) == M5_DIMENSION - 1:
            break
    if len(columns) != M5_DIMENSION - 1:
        raise InvalidRun("failed to construct deterministic S8 null frame")
    tangent = np.column_stack(columns)
    determinant = float(np.linalg.det(np.column_stack([tangent, unit])))
    if determinant < 0.0:
        tangent[:, 0] *= -1.0
        determinant *= -1.0
    if determinant <= 0.0:
        raise InvalidRun("S8 chart is not positively oriented")
    return tangent, determinant


def normalized_orientation(frame: np.ndarray) -> dict[str, Any]:
    matrix = np.asarray(frame, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise InvalidRun("orientation matrix is not square")
    norms = np.linalg.norm(matrix, axis=0)
    if np.any(norms <= 0.0) or not np.all(np.isfinite(norms)):
        return {
            "sign": 0,
            "normalized_sigma_min": 0.0,
            "normalized_condition_number": None,
            "column_norms": norms,
        }
    normalized = matrix / norms
    singular = np.linalg.svd(normalized, compute_uv=False)
    sign, logdet = np.linalg.slogdet(normalized)
    return {
        "sign": int(sign),
        "log_abs_normalized_determinant": float(logdet),
        "normalized_sigma_min": float(singular[-1]),
        "normalized_condition_number": float(singular[0] / singular[-1]),
        "normalized_singular_values": singular,
        "column_norms": norms,
    }


def complex_linear_real_map(matrix: np.ndarray) -> np.ndarray:
    """Realify a complex-linear map in the repository's interleaved order."""
    values = np.asarray(matrix, dtype=np.complex128)
    if values.shape != (M5_DIMENSION, M5_DIMENSION):
        raise InvalidRun("ambient complex map is not 9x9")
    output = np.empty((REAL_DIMENSION, REAL_DIMENSION), dtype=float)
    output[0::2, 0::2] = values.real
    output[0::2, 1::2] = -values.imag
    output[1::2, 0::2] = values.imag
    output[1::2, 1::2] = values.real
    return output


def frame_transition(
    reference: np.ndarray,
    candidate: np.ndarray,
    *,
    ambient: np.ndarray | None = None,
) -> dict[str, Any]:
    """Retain gauge transition and subspace-overlap diagnostics for two R18x9 frames."""
    left = np.asarray(reference, dtype=float)
    right = np.asarray(candidate, dtype=float)
    if left.shape != (REAL_DIMENSION, M5_DIMENSION) or right.shape != left.shape:
        raise InvalidRun("tangent transition requires two R18x9 frames")
    if ambient is not None:
        ambient_array = np.asarray(ambient, dtype=float)
        if ambient_array.shape != (REAL_DIMENSION, REAL_DIMENSION):
            raise InvalidRun("ambient tangent map is not R18 square")
        left = ambient_array @ left
    coefficients = np.linalg.lstsq(left, right, rcond=None)[0]
    fit_residual = float(
        np.linalg.norm(left @ coefficients - right)
        / max(np.linalg.norm(right), 1.0e-30)
    )
    left_q = np.linalg.qr(left, mode="reduced")[0]
    right_q = np.linalg.qr(right, mode="reduced")[0]
    principal = np.linalg.svd(left_q.T @ right_q, compute_uv=False)
    return {
        "transition_orientation": normalized_orientation(coefficients),
        "minimum_principal_overlap": float(principal[-1]),
        "principal_overlaps": principal,
        "relative_fit_residual": fit_residual,
        "transition_matrix": coefficients,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)

    def add_exact(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "exact",
            "passed": bool(passed),
            "status": "PASS" if passed else "INVALID_RUN",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.exact.append(record)
        if not passed:
            raise InvalidRun(f"{check_id}: {statement}")

    def add_numerical(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "passed": bool(passed),
            "status": "PASS" if passed else "INCONCLUSIVE",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.numerical.append(record)


@dataclass(frozen=True)
class LongCallableSet:
    dimension: int
    action_plain: Callable[..., object]
    joint_cse: Callable[..., object]
    joint_plain: Callable[..., object]

    def evaluate(
        self, values: np.ndarray, *, plain: bool
    ) -> tuple[np.clongdouble, np.ndarray, np.ndarray]:
        function = self.joint_plain if plain else self.joint_cse
        raw = np.asarray(function(tuple(values)), dtype=np.clongdouble).reshape(
            self.dimension + self.dimension**2
        )
        action = np.clongdouble(self.action_plain(tuple(values)))
        return (
            action,
            raw[: self.dimension],
            raw[self.dimension :].reshape(self.dimension, self.dimension),
        )


@dataclass(frozen=True)
class LongEvaluator:
    source_label: str
    delta_a: float
    delta_phi: float
    anchor4: np.ndarray
    anchor5: np.ndarray
    inverse_basis_long: np.ndarray
    kappa_a: np.longdouble
    kappa_phi: np.longdouble
    m4: LongCallableSet
    m5: LongCallableSet

    def _lifted(self, w5: np.ndarray, *, plain: bool = False) -> tuple[Any, np.ndarray, np.ndarray]:
        w_long = np.asarray(w5, dtype=np.clongdouble).reshape(M5_DIMENSION)
        coordinates = self.inverse_basis_long @ (
            w_long - np.asarray(self.anchor5, dtype=np.clongdouble)
        )
        w4 = np.asarray(self.anchor4, dtype=np.clongdouble) + coordinates[:7]
        action4, gradient4, hessian4 = self.m4.evaluate(w4, plain=plain)
        action = (
            action4
            + np.clongdouble(0.5) * self.kappa_a * coordinates[7] ** 2
            + np.clongdouble(0.5) * self.kappa_phi * coordinates[8] ** 2
        )
        gradient_c = np.concatenate(
            [
                gradient4,
                np.asarray(
                    [
                        self.kappa_a * coordinates[7],
                        self.kappa_phi * coordinates[8],
                    ],
                    dtype=np.clongdouble,
                ),
            ]
        )
        hessian_c = np.zeros((9, 9), dtype=np.clongdouble)
        hessian_c[:7, :7] = hessian4
        hessian_c[7, 7] = self.kappa_a
        hessian_c[8, 8] = self.kappa_phi
        gradient = self.inverse_basis_long.T @ gradient_c
        hessian = self.inverse_basis_long.T @ hessian_c @ self.inverse_basis_long
        return action, gradient, hessian

    def evaluate(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> tuple[np.clongdouble, np.ndarray, np.ndarray]:
        action0, gradient0, hessian0 = self._lifted(w5, plain=plain)
        w_long = np.asarray(w5, dtype=np.clongdouble).reshape(M5_DIMENSION)
        action1, gradient1, hessian1 = self.m5.evaluate(w_long, plain=plain)
        lam = np.longdouble(lambda_value)
        complement = np.longdouble(1.0) - lam
        return (
            np.clongdouble(complement * action0 + lam * action1),
            np.asarray(complement * gradient0 + lam * gradient1, dtype=np.clongdouble),
            np.asarray(complement * hessian0 + lam * hessian1, dtype=np.clongdouble),
        )


@dataclass(frozen=True)
class Chart8:
    center: np.ndarray
    tangent: np.ndarray
    orientation_determinant: float

    def direction(self, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        values = np.asarray(parameters, dtype=float).reshape(8)
        vector = self.center + self.tangent @ values
        norm = float(np.linalg.norm(vector))
        if norm <= 0.0:
            raise NumericalFailure("S8 chart vector vanished")
        omega = vector / norm
        derivative = (
            (np.eye(M5_DIMENSION) - np.outer(omega, omega))
            @ self.tangent
            / norm
        )
        return omega, derivative


@dataclass(frozen=True)
class Numerics:
    method: str
    state_rtol: float
    state_atol: float
    state_max_step: float
    tangent_rtol: float
    tangent_atol: float
    tangent_max_step: float
    newton_max_iterations: int
    newton_target_max_abs: float
    line_search_minimum: float
    saddle_tolerance: float
    saddle_maxfev: int
    ledger_samples: int


@dataclass(frozen=True)
class Thresholds:
    saddle_reproduction_distance: float
    saddle_gradient_max_abs: float
    saddle_hessian_min_abs_eigenvalue: float
    physical_residual_max_abs: float
    scaled_residual_max_abs: float
    normalized_sigma_min: float
    field_margin: float
    psi_margin: float
    chart_margin: float
    flow_time_margin: float
    flow_norm_max: float
    flow_norm_margin: float
    factor_identity_relative: float
    lambda0_launch_replay_relative: float
    path_state_distance: float
    reflection_state_distance: float
    reflection_action_absolute: float
    mutation_state_distance: float
    fd_operator_error: float
    fd_max_column_error: float
    fd_plateau: float
    outer_tangent_resolved_error: float
    outer_tangent_adjacent_error: float
    action_real_positive_step: float
    action_imag_drift: float
    first_cap_radius_residual: float
    first_cap_time_difference: float
    first_cap_state_distance: float
    cse_rhs_relative_error: float
    cse_hessian_action_relative_error: float
    cse_endpoint_state_relative_error: float
    cse_scaled_residual_absolute_difference: float


@dataclass(frozen=True)
class Bounds:
    lower: np.ndarray
    upper: np.ndarray

    def margins(self, parameters: np.ndarray, xi_norm_max: float) -> dict[str, float]:
        p = np.asarray(parameters, dtype=float)
        per_parameter = np.minimum(p - self.lower, self.upper - p)
        return {
            "minimum_field_margin": float(np.min(per_parameter[:8])),
            "psi_margin": float(per_parameter[8]),
            "minimum_chart_margin": float(np.min(per_parameter[9:17])),
            "flow_time_margin": float(per_parameter[17]),
            "flow_norm_margin": float(xi_norm_max),
            "per_parameter": per_parameter,
        }

    def contains(self, parameters: np.ndarray) -> bool:
        p = np.asarray(parameters, dtype=float)
        return bool(np.all(p > self.lower) and np.all(p < self.upper))


@dataclass
class Node:
    source: "SourceContext"
    lambda_value: float
    saddle_w: np.ndarray
    mobility: np.ndarray
    factor: np.ndarray
    factor_inverse: np.ndarray
    launch_w: np.ndarray
    sphere_radius: float
    shape_key: str
    launch_record: dict[str, Any]

    def xi_to_w_long(self, xi: np.ndarray) -> np.ndarray:
        return np.asarray(self.saddle_w, dtype=np.clongdouble) + np.asarray(
            self.factor, dtype=np.longdouble
        ) @ np.asarray(xi, dtype=np.clongdouble)

    def rhs_long(self, xi: np.ndarray, *, plain: bool = False) -> np.ndarray:
        w = self.xi_to_w_long(xi)
        _action, gradient, _hessian = self.source.evaluator.evaluate(
            self.lambda_value, w, plain=plain
        )
        return -np.conjugate(
            np.asarray(self.factor.T, dtype=np.longdouble) @ gradient
        )


@dataclass
class SourceContext:
    label: str
    delta_a: float
    delta_phi: float
    evaluator: LongEvaluator
    chart: Chart8
    p42_seed: np.ndarray
    p50_saddles: dict[float, np.ndarray]
    scales5: np.ndarray
    prolongation: np.ndarray
    added_mode: np.ndarray
    reflection5: np.ndarray
    mobility0: np.ndarray
    mobility1: np.ndarray
    factor0: np.ndarray
    reference_signed_frame: np.ndarray
    p42_launch_by_shape: dict[str, np.ndarray]
    cap_radius: float
    radius_primary: float
    numerics: Numerics
    thresholds: Thresholds
    bounds: Bounds
    _saddle_cache: dict[float, np.ndarray] = field(default_factory=dict)
    _saddle_records: dict[float, dict[str, Any]] = field(default_factory=dict)

    def saddle(self, lambda_value: float) -> np.ndarray:
        key = round(float(lambda_value), 14)
        if key in self._saddle_cache:
            return self._saddle_cache[key].copy()
        pinned_candidate: np.ndarray | None = None
        if key in self.p50_saddles:
            candidate = self.p50_saddles[key].copy()
            pinned_candidate = candidate.copy()
        else:
            known = sorted(self.p50_saddles)
            below = max((item for item in known if item < key), default=known[0])
            above = min((item for item in known if item > key), default=known[-1])
            if above == below:
                candidate = self.p50_saddles[below].copy()
            else:
                weight = (key - below) / (above - below)
                candidate = (
                    (1.0 - weight) * self.p50_saddles[below]
                    + weight * self.p50_saddles[above]
                )

        def values(w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
            _action, gradient, hessian = self.evaluator.evaluate(key, w)
            return (
                np.asarray(gradient.real, dtype=float),
                np.asarray(hessian.real, dtype=float),
            )

        solved = root(
            lambda w: values(w)[0],
            candidate,
            jac=lambda w: values(w)[1],
            method="hybr",
            options={
                "xtol": self.numerics.saddle_tolerance,
                "maxfev": self.numerics.saddle_maxfev,
            },
        )
        candidate = np.asarray(solved.x, dtype=float)
        gradient, hessian = values(candidate)
        residual = float(np.max(np.abs(gradient)))
        eigenvalues = np.linalg.eigvalsh(hessian)
        inertia = {
            "negative": int(np.count_nonzero(eigenvalues < 0.0)),
            "positive": int(np.count_nonzero(eigenvalues > 0.0)),
            "zero": int(np.count_nonzero(eigenvalues == 0.0)),
        }
        pinned_distance = (
            None
            if pinned_candidate is None
            else float(np.linalg.norm(candidate - pinned_candidate))
        )
        accepted = bool(
            solved.success
            and
            np.all(np.isfinite(candidate))
            and residual <= self.thresholds.saddle_gradient_max_abs
            and float(np.min(np.abs(eigenvalues)))
            >= self.thresholds.saddle_hessian_min_abs_eigenvalue
            and inertia == {"negative": 5, "positive": 4, "zero": 0}
            and (
                pinned_distance is None
                or pinned_distance <= self.thresholds.saddle_reproduction_distance
            )
        )
        self._saddle_records[key] = {
            "lambda": key,
            "solver_success": bool(solved.success),
            "solver_message": str(solved.message),
            "nfev": int(solved.nfev),
            "gradient_max_abs": residual,
            "hessian_min_abs_eigenvalue": float(np.min(np.abs(eigenvalues))),
            "hessian_inertia": inertia,
            "distance_to_pinned_phase50": pinned_distance,
            "accepted": accepted,
        }
        if not accepted:
            raise NumericalFailure(
                f"{self.label} saddle solve failed at lambda={key}: "
                f"success={solved.success}, residual={residual:.3e}, "
                f"p50_distance={pinned_distance}"
            )
        self._saddle_cache[key] = candidate.copy()
        return candidate

    def node(
        self,
        lambda_value: float,
        *,
        radius: float | None = None,
        shape_key: str = "lambda_1",
    ) -> Node:
        shape_exponents = {
            "lambda_0": 0.0,
            "lambda_0.5": 0.5,
            "lambda_1": 1.0,
        }
        if shape_key not in shape_exponents:
            raise InvalidRun(f"unknown launch shape: {shape_key}")
        lam = float(lambda_value)
        mobility = geodesic_spd(self.mobility0, self.mobility1, lam)
        mobility_sqrt = symmetric_power(mobility, 0.5)
        factor = (
            mobility_sqrt
            @ symmetric_power(self.mobility0, -0.5)
            @ self.factor0
        )
        if lam == 0.0:
            # The frozen path defines exact return to A0.  Avoid introducing a
            # gratuitous principal-square-root round trip at this endpoint.
            factor = self.factor0.copy()
        factor_inverse = np.linalg.inv(factor)
        _action, _gradient, hessian_long = self.evaluator.evaluate(
            lam, self.saddle(lam)
        )
        hessian = np.asarray(hessian_long.real, dtype=float)
        hessian_imag = float(np.max(np.abs(np.asarray(hessian_long.imag, dtype=float))))
        if hessian_imag > self.thresholds.cse_rhs_relative_error:
            raise NumericalFailure("real-saddle Hessian acquired an imaginary part")
        hessian_xi = factor.T @ hessian @ factor
        eigenvalues, raw_frame = deterministic_oriented_eigenframe(hessian_xi)
        negative = np.flatnonzero(eigenvalues < 0.0)
        positive = np.flatnonzero(eigenvalues > 0.0)
        if negative.size != 5 or positive.size != 4:
            raise NumericalFailure(
                f"local launch inertia drifted at lambda={lam}: "
                f"negative={negative.size}, positive={positive.size}"
            )
        coefficient_negative = np.array([0, 1, 2, 3, 7], dtype=int)
        coefficient_positive = np.array([4, 5, 6, 8], dtype=int)
        signed_frame = np.zeros((9, 9), dtype=float)
        overlaps: dict[str, float] = {}
        rotations: dict[str, np.ndarray] = {}
        alignment_data: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}
        for name, eig_indices, coefficient_indices in (
            ("negative", negative, coefficient_negative),
            ("positive", positive, coefficient_positive),
        ):
            raw = raw_frame[:, eig_indices]
            reference = self.reference_signed_frame[:, coefficient_indices]
            left, singular, right_t = np.linalg.svd(raw.T @ reference)
            rotation = left @ right_t
            aligned = raw @ rotation
            signed_frame[:, coefficient_indices] = aligned
            overlaps[name] = float(np.min(singular))
            rotations[name] = rotation
            alignment_data[name] = (
                raw,
                left,
                singular,
                right_t,
                coefficient_indices,
            )
        orientation_repaired_block: str | None = None
        if float(np.linalg.det(signed_frame)) < 0.0:
            orientation_repaired_block = min(
                alignment_data,
                key=lambda key: float(alignment_data[key][2][-1]),
            )
            raw, left, singular, right_t, coefficient_indices = alignment_data[
                orientation_repaired_block
            ]
            correction = np.eye(singular.size)
            correction[-1, -1] = -1.0
            rotation = left @ correction @ right_t
            signed_frame[:, coefficient_indices] = raw @ rotation
            rotations[orientation_repaired_block] = rotation
        launch_coefficient = np.zeros((9, 9), dtype=np.complex128)
        shape_exponent = shape_exponents[shape_key]
        for sign, coefficient_indices, phase in (
            (-1, coefficient_negative, -1.0 + 0.0j),
            (1, coefficient_positive, 0.0 + 1.0j),
        ):
            block = signed_frame[:, coefficient_indices]
            restriction = sign * (block.T @ hessian_xi @ block)
            shape = symmetric_power(restriction, -0.5 * shape_exponent)
            launch_coefficient[:, coefficient_indices] = phase * block @ shape
        recomputed_launch_coefficient = launch_coefficient.copy()
        if lam == 0.0:
            # P42 is the immutable source-specific endpoint gauge.  The nodal
            # eigenspace calculation above remains retained as an independent
            # replay diagnostic, while production uses the frozen endpoint.
            launch_coefficient = self.p42_launch_by_shape[shape_key].copy()
        launch = factor @ launch_coefficient
        if float(np.linalg.det(signed_frame)) <= 0.0:
            raise NumericalFailure("determinant-aware signed-frame alignment reversed orientation")
        return Node(
            source=self,
            lambda_value=lam,
            saddle_w=self.saddle(lam),
            mobility=mobility,
            factor=factor,
            factor_inverse=factor_inverse,
            launch_w=launch,
            sphere_radius=self.radius_primary if radius is None else float(radius),
            shape_key=shape_key,
            launch_record={
                "shape_exponent": shape_exponent,
                "hessian_xi_eigenvalues": eigenvalues,
                "hessian_inertia": {
                    "negative": int(negative.size),
                    "positive": int(positive.size),
                    "zero": int(9 - negative.size - positive.size),
                },
                "direct_to_lambda0_min_principal_overlaps": overlaps,
                "Procrustes_rotations": rotations,
                "orientation_repaired_block": orientation_repaired_block,
                "signed_frame_determinant": float(np.linalg.det(signed_frame)),
                "lambda0_immutable_launch_used": bool(lam == 0.0),
                "lambda0_recomputed_coefficient_relative_residual": (
                    float(
                        np.linalg.norm(
                            recomputed_launch_coefficient
                            - self.p42_launch_by_shape[shape_key]
                        )
                        / np.linalg.norm(self.p42_launch_by_shape[shape_key])
                    )
                    if lam == 0.0
                    else None
                ),
                "factor_relative_residual": float(
                    np.linalg.norm(factor @ factor.T - mobility)
                    / np.linalg.norm(mobility)
                ),
                "hessian_imag_max_abs": hessian_imag,
            },
        )


def make_callable_set(expressions: tuple[sp.Expr, sp.Matrix, sp.Matrix], variables: Sequence[sp.Symbol]) -> LongCallableSet:
    action, gradient, hessian = expressions
    arguments = (tuple(variables),)
    dimension = len(variables)
    outputs = tuple([*list(gradient), *list(hessian)])
    replacements, reduced = sp.cse(outputs, order="canonical")
    reconstructed = list(reduced)
    for symbol, replacement in reversed(replacements):
        reconstructed = [
            expression.xreplace({symbol: replacement})
            for expression in reconstructed
        ]
    exact = all(
        rebuilt == original or sp.expand(rebuilt - original) == 0
        for rebuilt, original in zip(reconstructed, outputs)
    )
    CSE_EXACT_LEDGER.append(
        {
            "dimension": dimension,
            "output_count": len(outputs),
            "replacement_count": len(replacements),
            "exact_back_substitution": bool(exact),
        }
    )
    canonical_cse = lambda expressions: sp.cse(expressions, order="canonical")
    return LongCallableSet(
        dimension=dimension,
        action_plain=sp.lambdify(arguments, action, modules="numpy", cse=False),
        joint_cse=sp.lambdify(arguments, outputs, modules="numpy", cse=canonical_cse),
        joint_plain=sp.lambdify(arguments, outputs, modules="numpy", cse=False),
    )


@lru_cache(maxsize=None)
def build_long_evaluator(
    source_label: str,
    delta_a: float,
    delta_phi: float,
    kappa_a: float,
    kappa_phi: float,
    basis_bytes: bytes,
) -> LongEvaluator:
    del basis_bytes  # cache identity; the Phase-50 basis is reconstructed below.
    phase41 = load_module(f"ice_phase41_for_phase51_{source_label}", PHASE41_SOURCE_PATH)
    phase50 = load_module(f"ice_phase50_for_phase51_{source_label}", PHASE50_SOURCE_PATH)
    embedding = phase50.build_embedding()
    model4 = phase41.numeric_model(float(delta_a), float(delta_phi))
    model5 = phase50.m5_numeric_model(float(delta_a), float(delta_phi))
    m4 = make_callable_set(
        (model4.action_expr, model4.gradient_expr, model4.hessian_expr),
        phase41.build_symbolic_family().variables_w,
    )
    m5_family = phase50.build_m5_symbolic_family()
    m5 = make_callable_set(
        (model5.action_expr, model5.gradient_expr, model5.hessian_expr),
        m5_family.variables_w,
    )
    return LongEvaluator(
        source_label=source_label,
        delta_a=float(delta_a),
        delta_phi=float(delta_phi),
        anchor4=phase50.anchor_w(phase41, 4, delta_a, delta_phi),
        anchor5=phase50.anchor_w(phase41, 5, delta_a, delta_phi),
        inverse_basis_long=np.asarray(embedding.inverse_basis, dtype=np.longdouble),
        kappa_a=np.longdouble(kappa_a),
        kappa_phi=np.longdouble(kappa_phi),
        m4=m4,
        m5=m5,
    )


def gamma_cap(
    source: SourceContext, parameters: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(parameters, dtype=float).reshape(9)
    coarse = values[:6]
    eta_a, eta_phi, psi = float(values[6]), float(values[7]), float(values[8])
    left = np.array(
        [
            source.scales5[0] * (1.0 - source.delta_a / 2.0),
            source.scales5[1] - source.delta_phi / 2.0,
        ],
        dtype=float,
    )
    right = np.array(
        [
            source.scales5[0] * (1.0 + source.delta_a / 2.0),
            source.scales5[1] + source.delta_phi / 2.0,
        ],
        dtype=float,
    )
    anchor = np.concatenate(
        [
            (1.0 - node / 5.0) * left + (node / 5.0) * right
            for node in range(1, 5)
        ]
    )
    coarse_a = coarse[0::2]
    coarse_phi = coarse[1::2]
    fine_a = source.prolongation @ coarse_a + source.added_mode * eta_a
    fine_phi = source.prolongation @ coarse_phi + source.added_mode * eta_phi
    deviations = np.empty(8, dtype=float)
    deviations[0::2] = fine_a
    deviations[1::2] = fine_phi
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    phases = np.array([phase_a, phase_phi] * 4, dtype=np.complex128)
    state = np.concatenate(
        [
            anchor + phases * deviations,
            [source.cap_radius * np.exp(1.0j * psi)],
        ]
    )
    tangent = np.zeros((M5_DIMENSION, M5_DIMENSION), dtype=np.complex128)
    for coarse_index in range(3):
        tangent[0:8:2, 2 * coarse_index] = phase_a * source.prolongation[:, coarse_index]
        tangent[1:8:2, 2 * coarse_index + 1] = phase_phi * source.prolongation[:, coarse_index]
    tangent[0:8:2, 6] = phase_a * source.added_mode
    tangent[1:8:2, 7] = phase_phi * source.added_mode
    tangent[:8, 8] = 0.5j * phases * deviations
    tangent[8, 8] = 1.0j * state[8]
    return state, tangent


def integrate_k(
    node: Node,
    chart_parameters: np.ndarray,
    flow_time: float,
    *,
    with_tangent: bool,
    t_eval: np.ndarray | None = None,
    event: bool = False,
    plain_backend: bool = False,
) -> tuple[np.ndarray, np.ndarray | None, dict[str, Any], Any]:
    source = node.source
    if not source.bounds.lower[17] <= flow_time <= source.bounds.upper[17]:
        raise NumericalFailure("flow time left the frozen interval")
    omega, derivative = source.chart.direction(chart_parameters)
    launch_xi = np.asarray(node.factor_inverse, dtype=np.longdouble) @ np.asarray(
        node.launch_w, dtype=np.clongdouble
    )
    initial_xi = np.clongdouble(node.sphere_radius) * (
        launch_xi @ np.asarray(omega, dtype=np.longdouble)
    )
    initial_tangent = np.clongdouble(node.sphere_radius) * (
        launch_xi @ np.asarray(derivative, dtype=np.longdouble)
    )
    factor_long = np.asarray(node.factor, dtype=np.longdouble)

    def state_rhs(_time: float, xi: np.ndarray) -> np.ndarray:
        xi_long = np.asarray(xi, dtype=np.clongdouble)
        state_long = np.asarray(node.saddle_w, dtype=np.clongdouble) + factor_long @ xi_long
        _action, gradient, _hessian = source.evaluator.evaluate(
            node.lambda_value, state_long, plain=plain_backend
        )
        derivative_long = -np.conjugate(factor_long.T @ gradient)
        # The sole precision boundary required by scipy.integrate.solve_ivp.
        return np.asarray(derivative_long, dtype=np.complex128)

    events: Any = None
    if event:
        def cap_event(_time: float, xi: np.ndarray) -> float:
            state = np.asarray(node.saddle_w, dtype=np.complex128) + np.asarray(
                node.factor, dtype=float
            ) @ np.asarray(xi, dtype=np.complex128)
            return float(abs(source.scales5[-1] * state[-1]) - source.cap_radius)

        cap_event.terminal = True  # type: ignore[attr-defined]
        cap_event.direction = -1.0  # type: ignore[attr-defined]
        events = cap_event

    if not with_tangent:
        solution = solve_ivp(
            state_rhs,
            (0.0, float(flow_time)),
            np.asarray(initial_xi, dtype=np.complex128),
            method=source.numerics.method,
            rtol=source.numerics.state_rtol,
            atol=source.numerics.state_atol,
            max_step=source.numerics.state_max_step,
            t_eval=t_eval,
            events=events,
        )
        if not solution.success:
            raise NumericalFailure(str(solution.message))
        xi_norm_max = float(np.max(np.linalg.norm(solution.y, axis=0)))
        if xi_norm_max >= source.thresholds.flow_norm_max:
            raise NumericalFailure("trajectory exceeded the frozen xi-norm cap")
        final_w = node.saddle_w + node.factor @ solution.y[:, -1]
        state_z = source.scales5 * final_w
        return state_z, None, {
            "solver_method": source.numerics.method,
            "solver_steps": int(solution.t.size),
            "xi_norm_max": xi_norm_max,
        }, solution

    augmented_initial = np.concatenate(
        [np.asarray(initial_xi, dtype=np.complex128), initial_tangent.reshape(-1)]
    )

    def tangent_rhs(_time: float, augmented: np.ndarray) -> np.ndarray:
        long = np.asarray(augmented, dtype=np.clongdouble)
        xi = long[:M5_DIMENSION]
        tangent = long[M5_DIMENSION:].reshape(M5_DIMENSION, M5_DIMENSION - 1)
        state = np.asarray(node.saddle_w, dtype=np.clongdouble) + factor_long @ xi
        _action, gradient, hessian = source.evaluator.evaluate(
            node.lambda_value, state, plain=plain_backend
        )
        state_derivative = -np.conjugate(factor_long.T @ gradient)
        hessian_xi = factor_long.T @ hessian @ factor_long
        tangent_derivative = -np.conjugate(hessian_xi @ tangent)
        combined = np.concatenate([state_derivative, tangent_derivative.reshape(-1)])
        # The sole precision boundary required by scipy.integrate.solve_ivp.
        return np.asarray(combined, dtype=np.complex128)

    solution = solve_ivp(
        tangent_rhs,
        (0.0, float(flow_time)),
        augmented_initial,
        method=source.numerics.method,
        rtol=source.numerics.tangent_rtol,
        atol=source.numerics.tangent_atol,
        max_step=source.numerics.tangent_max_step,
    )
    if not solution.success:
        raise NumericalFailure(str(solution.message))
    final = solution.y[:, -1]
    final_xi = final[:M5_DIMENSION]
    tangent_xi = final[M5_DIMENSION:].reshape(M5_DIMENSION, M5_DIMENSION - 1)
    xi_norm_max = float(
        np.max(np.linalg.norm(solution.y[:M5_DIMENSION, :], axis=0))
    )
    if xi_norm_max >= source.thresholds.flow_norm_max:
        raise NumericalFailure("trajectory exceeded the frozen xi-norm cap")
    final_w = node.saddle_w + node.factor @ final_xi
    state_z = source.scales5 * final_w
    tangent_z = source.scales5[:, np.newaxis] * (
        node.factor @ tangent_xi
    )
    time_tangent_z = source.scales5 * (
        node.factor
        @ np.asarray(node.rhs_long(final_xi), dtype=np.complex128)
    )
    return (
        state_z,
        np.column_stack([tangent_z, time_tangent_z]),
        {
            "solver_method": source.numerics.method,
            "solver_steps": int(solution.t.size),
            "xi_norm_max": xi_norm_max,
        },
        solution,
    )


def evaluate_root(
    node: Node, parameters: np.ndarray, *, with_tangent: bool
) -> dict[str, Any]:
    p = np.asarray(parameters, dtype=float).reshape(REAL_DIMENSION)
    gamma_state, gamma_tangent = gamma_cap(node.source, p[:9])
    k_state, k_tangent, integration, _solution = integrate_k(
        node,
        p[9:17],
        float(p[17]),
        with_tangent=with_tangent,
    )
    residual_z = gamma_state - k_state
    residual = interleaved(residual_z / node.source.scales5)
    output: dict[str, Any] = {
        "residual": residual,
        "gamma_state_z": gamma_state,
        "k_state_z": k_state,
        "physical_residual_max_abs": float(np.max(np.abs(residual_z))),
        "scaled_residual_max_abs": float(np.max(np.abs(residual))),
        "scaled_residual_norm": float(np.linalg.norm(residual)),
        "integration": integration,
    }
    if with_tangent:
        if k_tangent is None:
            raise AssertionError("variational tangent integration was omitted")
        gamma_frame = real_frame(gamma_tangent)
        k_frame = real_frame(k_tangent)
        row_scales = np.repeat(1.0 / node.source.scales5, 2)
        jacobian = row_scales[:, np.newaxis] * np.column_stack(
            [gamma_frame, -k_frame]
        )
        output.update(
            {
                "jacobian": jacobian,
                "gamma_frame": gamma_frame,
                "k_frame": k_frame,
            }
        )
    return output


def solve_root(
    node: Node,
    seed: np.ndarray,
    *,
    label: str,
) -> tuple[np.ndarray | None, dict[str, Any]]:
    source = node.source
    parameters = np.asarray(seed, dtype=float).reshape(REAL_DIMENSION).copy()
    if not source.bounds.contains(parameters):
        return None, {
            "status": "INCONCLUSIVE",
            "message": "seed left frozen parameter bounds",
            "label": label,
        }
    history: list[dict[str, Any]] = []
    evaluation: dict[str, Any] | None = None
    for iteration in range(source.numerics.newton_max_iterations + 1):
        try:
            evaluation = evaluate_root(node, parameters, with_tangent=True)
        except (NumericalFailure, FloatingPointError, ValueError) as error:
            return None, {
                "status": "INCONCLUSIVE",
                "message": str(error),
                "label": label,
                "history": history,
            }
        residual = np.asarray(evaluation["residual"], dtype=float)
        jacobian = np.asarray(evaluation["jacobian"], dtype=float)
        maximum = float(np.max(np.abs(residual)))
        history.append(
            {
                "iteration": iteration,
                "scaled_residual_max_abs": maximum,
                "jacobian_condition_number": float(np.linalg.cond(jacobian)),
            }
        )
        if maximum <= source.numerics.newton_target_max_abs:
            break
        if iteration >= source.numerics.newton_max_iterations:
            return None, {
                "status": "INCONCLUSIVE",
                "message": "damped Newton iteration limit",
                "label": label,
                "history": history,
            }
        step = np.linalg.lstsq(jacobian, -residual, rcond=None)[0]
        baseline = float(np.linalg.norm(residual))
        damping = 1.0
        accepted = False
        while damping >= source.numerics.line_search_minimum:
            trial = parameters + damping * step
            if source.bounds.contains(trial):
                try:
                    trial_evaluation = evaluate_root(node, trial, with_tangent=False)
                    trial_norm = float(np.linalg.norm(trial_evaluation["residual"]))
                except (NumericalFailure, FloatingPointError, ValueError):
                    trial_norm = math.inf
                if trial_norm < baseline:
                    parameters = trial
                    accepted = True
                    break
            damping *= 0.5
        history[-1]["accepted_damping"] = damping if accepted else None
        if not accepted:
            return None, {
                "status": "INCONCLUSIVE",
                "message": "damped Newton line search failed",
                "label": label,
                "history": history,
            }
    if evaluation is None:
        raise AssertionError("root evaluation was not performed")
    gamma_frame = np.asarray(evaluation["gamma_frame"], dtype=float)
    k_frame = np.asarray(evaluation["k_frame"], dtype=float)
    direct = normalized_orientation(np.column_stack([gamma_frame, k_frame]))
    root_orientation = normalized_orientation(np.asarray(evaluation["jacobian"], dtype=float))
    gamma_rank = int(np.linalg.matrix_rank(gamma_frame))
    k_rank = int(np.linalg.matrix_rank(k_frame))
    per_margin = np.minimum(parameters - source.bounds.lower, source.bounds.upper - parameters)
    margins = {
        "minimum_field_margin": float(np.min(per_margin[:8])),
        "psi_margin": float(per_margin[8]),
        "minimum_chart_margin": float(np.min(per_margin[9:17])),
        "flow_time_margin": float(per_margin[17]),
        "flow_norm_margin": float(
            source.thresholds.flow_norm_max - evaluation["integration"]["xi_norm_max"]
        ),
    }
    accepted = bool(
        evaluation["physical_residual_max_abs"]
        <= source.thresholds.physical_residual_max_abs
        and evaluation["scaled_residual_max_abs"]
        <= source.thresholds.scaled_residual_max_abs
        and gamma_rank == M5_DIMENSION
        and k_rank == M5_DIMENSION
        and direct["sign"] != 0
        and root_orientation["sign"] == -direct["sign"]
        and direct["normalized_sigma_min"]
        >= source.thresholds.normalized_sigma_min
        and margins["minimum_field_margin"] >= source.thresholds.field_margin
        and margins["psi_margin"] >= source.thresholds.psi_margin
        and margins["minimum_chart_margin"] >= source.thresholds.chart_margin
        and margins["flow_time_margin"] >= source.thresholds.flow_time_margin
        and margins["flow_norm_margin"] >= source.thresholds.flow_norm_margin
    )
    return parameters, {
        "status": "PASS" if accepted else "INCONCLUSIVE",
        "accepted": accepted,
        "label": label,
        "lambda": node.lambda_value,
        "parameters": parameters,
        "intersection_z": evaluation["gamma_state_z"],
        "physical_residual_max_abs": evaluation["physical_residual_max_abs"],
        "scaled_residual_max_abs": evaluation["scaled_residual_max_abs"],
        "scaled_residual_norm": evaluation["scaled_residual_norm"],
        "gamma_rank": gamma_rank,
        "k_rank": k_rank,
        "direct_orientation": direct,
        "root_jacobian_orientation": root_orientation,
        "gamma_frame": gamma_frame,
        "k_frame": k_frame,
        "variational_scaled_root_jacobian": evaluation["jacobian"],
        "integration": evaluation["integration"],
        "window_margins": margins,
        "newton_history": history,
        "sphere_radius": node.sphere_radius,
        "launch_shape": node.shape_key,
        "launch_construction": node.launch_record,
        "saddle_reproduction": source._saddle_records[
            round(float(node.lambda_value), 14)
        ],
    }


def solve_path(
    source: SourceContext,
    nodes: Sequence[float],
    seed: np.ndarray,
    *,
    label: str,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    roots: dict[float, np.ndarray] = {}
    previous = np.asarray(seed, dtype=float).copy()
    requested = [float(value) for value in nodes]
    for index, lambda_value in enumerate(requested):
        lam = float(lambda_value)
        try:
            solved, record = solve_root(
                source.node(lam), previous, label=f"{label}:lambda={lam:.12g}"
            )
        except (NumericalFailure, FloatingPointError, ValueError) as error:
            solved = None
            record = {
                "status": "INCONCLUSIVE",
                "accepted": False,
                "label": f"{label}:lambda={lam:.12g}",
                "lambda": lam,
                "message": str(error),
            }
        records.append(record)
        if solved is None or not record.get("accepted", False):
            for unattempted in requested[index + 1 :]:
                records.append(
                    {
                        "status": "INCONCLUSIVE",
                        "accepted": False,
                        "label": f"{label}:lambda={unattempted:.12g}",
                        "lambda": unattempted,
                        "message": "not attempted after the preceding frozen path node failed",
                    }
                )
            return {
                "status": "INCONCLUSIVE",
                "completed": False,
                "requested_node_count": len(requested),
                "attempted_node_count": index + 1,
                "retained_node_count": len(records),
                "requested_lambdas": requested,
                "terminated_at": lam,
                "records": records,
                "roots": roots,
            }
        roots[round(lam, 14)] = solved.copy()
        previous = solved
        progress(
            f"{label} lambda={lam:.4f}: residual="
            f"{record['scaled_residual_max_abs']:.3e}, "
            f"sigma={record['direct_orientation']['normalized_sigma_min']:.3e}"
        )
    return {
        "status": "PASS",
        "completed": True,
        "requested_node_count": len(requested),
        "attempted_node_count": len(requested),
        "retained_node_count": len(records),
        "requested_lambdas": requested,
        "terminated_at": None,
        "records": records,
        "roots": roots,
        "endpoint_parameters": previous,
    }


def state_only_residual(
    node: Node,
    parameters: np.ndarray,
    k_cache: dict[tuple[float, ...], np.ndarray] | None = None,
) -> np.ndarray:
    p = np.asarray(parameters, dtype=float)
    gamma = gamma_cap(node.source, p[:9])[0]
    key = tuple(float(value) for value in p[9:18])
    if k_cache is not None and key in k_cache:
        k_state = k_cache[key]
    else:
        k_state = integrate_k(
            node, p[9:17], float(p[17]), with_tangent=False
        )[0]
        if k_cache is not None:
            k_cache[key] = k_state
    return interleaved((gamma - k_state) / node.source.scales5)


def finite_difference_jacobian_control(
    node: Node,
    parameters: np.ndarray,
    variational: np.ndarray,
    ladders: Sequence[Sequence[float]],
) -> dict[str, Any]:
    if len(ladders) != REAL_DIMENSION or any(len(item) != 2 for item in ladders):
        raise InvalidRun("root FD policy must contain two steps for each R18 column")
    cache: dict[tuple[float, ...], np.ndarray] = {}
    first_columns: list[np.ndarray] = []
    second_columns: list[np.ndarray] = []
    plateaus: list[float] = []
    records: list[dict[str, Any]] = []
    for index, raw_steps in enumerate(ladders):
        columns: list[np.ndarray] = []
        steps = [finite_float(value, label=f"FD step {index}") for value in raw_steps]
        for step in steps:
            if step <= 0.0:
                raise InvalidRun("FD steps must be positive")
            plus = np.asarray(parameters, dtype=float).copy()
            minus = np.asarray(parameters, dtype=float).copy()
            plus[index] += step
            minus[index] -= step
            if not node.source.bounds.contains(plus) or not node.source.bounds.contains(minus):
                raise NumericalFailure(f"FD column {index} left parameter bounds")
            columns.append(
                (state_only_residual(node, plus, cache) - state_only_residual(node, minus, cache))
                / (2.0 * step)
            )
        plateau = float(
            np.linalg.norm(columns[0] - columns[1])
            / max(np.linalg.norm(columns[0]), 1.0e-30)
        )
        first_columns.append(columns[0])
        second_columns.append(columns[1])
        plateaus.append(plateau)
        records.append(
            {
                "column": index,
                "steps": steps,
                "adjacent_step_relative_change": plateau,
            }
        )
    fd_first = np.column_stack(first_columns)
    fd_second = np.column_stack(second_columns)
    variational_array = np.asarray(variational, dtype=float)
    relative_error = float(
        np.linalg.norm(fd_first - variational_array, ord=2)
        / max(np.linalg.norm(variational_array, ord=2), 1.0e-30)
    )
    column_errors = [
        float(
            np.linalg.norm(fd_first[:, index] - variational_array[:, index])
            / max(np.linalg.norm(variational_array[:, index]), 1.0e-30)
        )
        for index in range(REAL_DIMENSION)
    ]
    for record, error in zip(records, column_errors):
        record["FD_to_variational_relative_error"] = error
    maximum_column_error = float(max(column_errors))
    maximum_plateau = float(max(plateaus))
    orientation = normalized_orientation(fd_first)
    expected_sign = normalized_orientation(variational_array)["sign"]
    passed = bool(
        relative_error <= node.source.thresholds.fd_operator_error
        and maximum_column_error <= node.source.thresholds.fd_max_column_error
        and maximum_plateau <= node.source.thresholds.fd_plateau
        and orientation["sign"] == expected_sign
    )
    return {
        "status": "PASS" if passed else "INCONCLUSIVE",
        "passed": passed,
        "lambda": node.lambda_value,
        "FD_to_variational_relative_operator_error": relative_error,
        "maximum_column_FD_to_variational_relative_error": maximum_column_error,
        "maximum_adjacent_step_relative_change": maximum_plateau,
        "finite_difference_orientation": orientation,
        "expected_root_orientation_sign": expected_sign,
        "per_column": records,
        "larger_step_FD_matrix": fd_first,
        "smaller_step_FD_matrix": fd_second,
        "variational_matrix": variational_array,
        "second_step_matrix_relative_to_first": float(
            np.linalg.norm(fd_second - fd_first, ord=2)
            / max(np.linalg.norm(fd_first, ord=2), 1.0e-30)
        ),
    }


def flow_ledger(node: Node, parameters: np.ndarray) -> dict[str, Any]:
    source = node.source
    flow_time = float(parameters[17])
    times = np.linspace(0.0, flow_time, source.numerics.ledger_samples)
    state_z, _tangent, integration, solution = integrate_k(
        node,
        parameters[9:17],
        flow_time,
        with_tangent=False,
        t_eval=times,
    )
    actions = np.asarray(
        [
            source.evaluator.evaluate(
                node.lambda_value,
                node.xi_to_w_long(solution.y[:, index]),
            )[0]
            for index in range(solution.y.shape[1])
        ],
        dtype=np.clongdouble,
    )
    event_limit = min(source.bounds.upper[17], flow_time + source.thresholds.flow_time_margin)
    _event_state, _none, event_integration, event_solution = integrate_k(
        node,
        parameters[9:17],
        event_limit,
        with_tangent=False,
        event=True,
    )
    event_status = "NO_CAP_EVENT"
    radius_residual: float | None = None
    time_difference: float | None = None
    state_distance: float | None = None
    if event_solution.t_events and len(event_solution.t_events[0]) > 0:
        event_status = "FIRST_CAP_EVENT"
        event_time = float(event_solution.t_events[0][0])
        event_xi = np.asarray(
            event_solution.y_events[0][0], dtype=np.complex128
        )
        event_w = node.xi_to_w_long(event_xi)
        event_z = source.scales5 * event_w
        gamma_z = gamma_cap(source, parameters[:9])[0]
        radius_residual = float(abs(abs(event_z[-1]) - source.cap_radius))
        time_difference = abs(event_time - flow_time)
        state_distance = float(
            np.linalg.norm(interleaved((event_z - gamma_z) / source.scales5))
        )
    real_steps = np.diff(actions.real.astype(np.longdouble))
    return {
        "sample_count": int(times.size),
        "ReS_start": float(actions.real[0]),
        "ReS_end": float(actions.real[-1]),
        "ReS_max_positive_step": float(np.max(real_steps)),
        "ImS_max_drift": float(np.max(np.abs(actions.imag - actions.imag[0]))),
        "xi_norm_max": integration["xi_norm_max"],
        "xi_norm_margin": float(
            source.thresholds.flow_norm_max - integration["xi_norm_max"]
        ),
        "first_cap_event_status": event_status,
        "first_cap_radius_residual": radius_residual,
        "first_cap_time_difference": time_difference,
        "first_cap_normalized_state_distance": state_distance,
        "event_integration": event_integration,
        "endpoint_state_match": float(
            np.linalg.norm(interleaved((state_z - gamma_cap(source, parameters[:9])[0]) / source.scales5))
        ),
    }


def ledger_passed(ledger: Mapping[str, Any], thresholds: Thresholds) -> bool:
    try:
        return bool(
            ledger["ReS_max_positive_step"]
            <= thresholds.action_real_positive_step
            and ledger["ImS_max_drift"] <= thresholds.action_imag_drift
            and ledger["xi_norm_margin"] >= thresholds.flow_norm_margin
            and ledger["first_cap_event_status"] == "FIRST_CAP_EVENT"
            and ledger["first_cap_radius_residual"]
            <= thresholds.first_cap_radius_residual
            and ledger["first_cap_time_difference"]
            <= thresholds.first_cap_time_difference
            and ledger["first_cap_normalized_state_distance"]
            <= thresholds.first_cap_state_distance
        )
    except (KeyError, TypeError):
        return False


def safe_flow_ledger(node: Node, parameters: np.ndarray) -> dict[str, Any]:
    try:
        record = flow_ledger(node, parameters)
        record["passed"] = ledger_passed(record, node.source.thresholds)
        record["status"] = "PASS" if record["passed"] else "INCONCLUSIVE"
        return record
    except (NumericalFailure, FloatingPointError, ValueError) as error:
        return {
            "status": "INCONCLUSIVE",
            "passed": False,
            "lambda": node.lambda_value,
            "message": str(error),
        }


def path_flow_ledgers(
    source: SourceContext,
    path: Mapping[str, Any],
    *,
    label: str,
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for record in path.get("records", []):
        lam = float(record.get("lambda", 0.0))
        key = f"lambda={lam:.12g}"
        if not record.get("accepted", False):
            output[key] = {
                "status": "INCONCLUSIVE",
                "passed": False,
                "lambda": lam,
                "message": "path node was not accepted; ledger was not run",
            }
            continue
        progress(f"building {label} first-cap/action ledger at lambda={lam:.4f}")
        try:
            output[key] = safe_flow_ledger(
                source.node(
                    lam,
                    radius=float(record.get("sphere_radius", source.radius_primary)),
                    shape_key=str(record.get("launch_shape", "lambda_1")),
                ),
                np.asarray(record["parameters"], dtype=float),
            )
        except (NumericalFailure, FloatingPointError, ValueError) as error:
            output[key] = {
                "status": "INCONCLUSIVE",
                "passed": False,
                "lambda": lam,
                "message": str(error),
            }
    return output


def outer_tangent_control(
    source: SourceContext,
    center_parameters: np.ndarray,
    steps: Sequence[float],
) -> dict[str, Any]:
    if len(steps) != 2:
        raise InvalidRun("outer tangent control requires exactly two lambda steps")
    center_node = source.node(0.5)
    center_eval = evaluate_root(center_node, center_parameters, with_tangent=True)
    jacobian = np.asarray(center_eval["jacobian"], dtype=float)
    records: list[dict[str, Any]] = []
    derivatives: list[np.ndarray] = []
    for raw_step in steps:
        step = finite_float(raw_step, label="outer tangent step")
        if step <= 0.0:
            raise InvalidRun("outer tangent steps must be positive")
        plus_node = source.node(0.5 + step)
        minus_node = source.node(0.5 - step)
        f_plus = state_only_residual(plus_node, center_parameters)
        f_minus = state_only_residual(minus_node, center_parameters)
        partial_lambda = (f_plus - f_minus) / (2.0 * step)
        implicit = np.linalg.lstsq(jacobian, -partial_lambda, rcond=None)[0]
        plus_root, plus_record = solve_root(
            plus_node,
            center_parameters + step * implicit,
            label=f"outer-plus-h={step:.3g}",
        )
        minus_root, minus_record = solve_root(
            minus_node,
            center_parameters - step * implicit,
            label=f"outer-minus-h={step:.3g}",
        )
        if (
            plus_root is None
            or minus_root is None
            or not plus_record.get("accepted", False)
            or not minus_record.get("accepted", False)
        ):
            return {
                "status": "INCONCLUSIVE",
                "passed": False,
                "message": "outer re-solve failed",
                "step": step,
                "plus": plus_record,
                "minus": minus_record,
            }
        resolved = (plus_root - minus_root) / (2.0 * step)
        error = float(
            np.linalg.norm(resolved - implicit)
            / max(np.linalg.norm(implicit), 1.0e-30)
        )
        derivatives.append(implicit)
        plus_ledger = safe_flow_ledger(plus_node, plus_root)
        minus_ledger = safe_flow_ledger(minus_node, minus_root)
        records.append(
            {
                "step": step,
                "implicit_tangent": implicit,
                "resolved_central_tangent": resolved,
                "relative_error": error,
                "plus_residual": plus_record["scaled_residual_max_abs"],
                "minus_residual": minus_record["scaled_residual_max_abs"],
                "plus_root_record": plus_record,
                "minus_root_record": minus_record,
                "plus_flow_ledger": plus_ledger,
                "minus_flow_ledger": minus_ledger,
            }
        )
    adjacent = float(
        np.linalg.norm(derivatives[0] - derivatives[1])
        / max(np.linalg.norm(derivatives[0]), 1.0e-30)
    )
    maximum = max(float(record["relative_error"]) for record in records)
    passed = bool(
        maximum <= source.thresholds.outer_tangent_resolved_error
        and adjacent <= source.thresholds.outer_tangent_adjacent_error
        and all(
            record["plus_flow_ledger"].get("passed", False)
            and record["minus_flow_ledger"].get("passed", False)
            for record in records
        )
    )
    return {
        "status": "PASS" if passed else "INCONCLUSIVE",
        "passed": passed,
        "lambda": 0.5,
        "maximum_resolved_relative_error": maximum,
        "adjacent_step_implicit_tangent_relative_change": adjacent,
        "records": records,
    }


def map_shape_seed(
    source: SourceContext, primary_parameters: np.ndarray, shape_key: str
) -> np.ndarray:
    primary = source.node(1.0, shape_key="lambda_1")
    control = source.node(1.0, shape_key=shape_key)
    omega = source.chart.direction(np.asarray(primary_parameters)[9:17])[0]
    physical_direction = primary.launch_w @ omega
    coefficients = np.linalg.lstsq(
        real_frame(control.launch_w), interleaved(physical_direction), rcond=None
    )[0]
    coefficient_norm = float(np.linalg.norm(coefficients))
    if coefficient_norm <= 0.0:
        raise NumericalFailure("shape-control direction projection vanished")
    coefficients /= coefficient_norm
    center_overlap = float(source.chart.center @ coefficients)
    if center_overlap < 0.0:
        coefficients *= -1.0
        center_overlap *= -1.0
    if center_overlap <= 1.0e-12:
        raise NumericalFailure("shape-control direction left the frozen S8 chart")
    chart_parameters = source.chart.tangent.T @ coefficients / center_overlap
    seed = np.asarray(primary_parameters, dtype=float).copy()
    seed[9:17] = chart_parameters
    if not source.bounds.contains(seed):
        raise NumericalFailure("shape-control mapped seed left frozen bounds")
    return seed


def cse_validation(source: SourceContext, lambdas: Sequence[float]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    maximum_rhs = 0.0
    maximum_hessian_action = 0.0
    probe = np.arange(1, M5_DIMENSION + 1, dtype=np.longdouble)
    probe /= np.linalg.norm(probe)
    for lam in lambdas:
        node = source.node(float(lam))
        initial_w = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.clongdouble(
            node.sphere_radius
        ) * (
            np.asarray(node.launch_w, dtype=np.clongdouble)
            @ np.asarray(source.chart.center, dtype=np.longdouble)
        )
        cse = source.evaluator.evaluate(float(lam), initial_w, plain=False)
        plain = source.evaluator.evaluate(float(lam), initial_w, plain=True)
        component_errors: list[float] = []
        for left, right in zip(cse, plain):
            left_array = np.asarray(left, dtype=np.clongdouble)
            right_array = np.asarray(right, dtype=np.clongdouble)
            error = float(
                np.linalg.norm(left_array - right_array)
                / max(float(np.linalg.norm(right_array)), 1.0e-30)
            )
            component_errors.append(error)
        factor = np.asarray(node.factor, dtype=np.longdouble)
        cse_rhs = -np.conjugate(factor.T @ cse[1])
        plain_rhs = -np.conjugate(factor.T @ plain[1])
        rhs_error = float(
            np.linalg.norm(cse_rhs - plain_rhs)
            / max(float(np.linalg.norm(plain_rhs)), 1.0e-30)
        )
        cse_hessian_action = factor.T @ cse[2] @ factor @ probe
        plain_hessian_action = factor.T @ plain[2] @ factor @ probe
        hessian_action_error = float(
            np.linalg.norm(cse_hessian_action - plain_hessian_action)
            / max(float(np.linalg.norm(plain_hessian_action)), 1.0e-30)
        )
        maximum_rhs = max(maximum_rhs, rhs_error)
        maximum_hessian_action = max(
            maximum_hessian_action, hessian_action_error
        )
        records.append(
            {
                "point": "declared_center_launch_initial_state",
                "lambda": float(lam),
                "action_gradient_hessian_relative_errors": component_errors,
                "cse_dtypes": [str(np.asarray(value).dtype) for value in cse],
                "state_formation_dtype": str(np.asarray(initial_w).dtype),
                "rhs_contraction_dtype": str(np.asarray(cse_rhs).dtype),
                "hessian_action_dtype": str(
                    np.asarray(cse_hessian_action).dtype
                ),
                "rhs_relative_error": rhs_error,
                "hessian_action_relative_error": hessian_action_error,
            }
        )
    dtype_pass = all(
        record["state_formation_dtype"] == "complex256"
        and record["rhs_contraction_dtype"] == "complex256"
        and record["hessian_action_dtype"] == "complex256"
        and all(dtype == "complex256" for dtype in record["cse_dtypes"])
        for record in records
    )
    numeric_pass = bool(
        maximum_rhs <= source.thresholds.cse_rhs_relative_error
        and maximum_hessian_action
        <= source.thresholds.cse_hessian_action_relative_error
    )
    return {
        "status": "PASS" if numeric_pass else "INCONCLUSIVE",
        "passed": numeric_pass,
        "numeric_pair_passed": numeric_pass,
        "dtype_contract_passed": dtype_pass,
        "maximum_rhs_relative_error": maximum_rhs,
        "maximum_hessian_action_relative_error": maximum_hessian_action,
        "records": records,
    }


def cse_trajectory_validation(
    source: SourceContext,
    node: Node,
    parameters: np.ndarray,
    fractions: Sequence[float],
) -> dict[str, Any]:
    """Independently reintegrate one solved K trajectory with both backends."""
    p = np.asarray(parameters, dtype=float).reshape(REAL_DIMENSION)
    values = np.asarray(
        [finite_float(value, label="CSE trajectory fraction") for value in fractions],
        dtype=float,
    )
    if (
        values.shape != (5,)
        or not np.array_equal(values, np.asarray([0.0, 0.25, 0.5, 0.75, 1.0]))
    ):
        raise InvalidRun("paired trajectory fractions drifted")
    times = values * float(p[17])
    cse_state, _none, cse_integration, cse_solution = integrate_k(
        node,
        p[9:17],
        float(p[17]),
        with_tangent=False,
        t_eval=times,
        plain_backend=False,
    )
    plain_state, _none2, plain_integration, plain_solution = integrate_k(
        node,
        p[9:17],
        float(p[17]),
        with_tangent=False,
        t_eval=times,
        plain_backend=True,
    )
    cse_states = np.column_stack(
        [
            np.asarray(source.scales5, dtype=np.longdouble)
            * node.xi_to_w_long(cse_solution.y[:, index])
            for index in range(cse_solution.y.shape[1])
        ]
    )
    plain_states = np.column_stack(
        [
            np.asarray(source.scales5, dtype=np.longdouble)
            * node.xi_to_w_long(plain_solution.y[:, index])
            for index in range(plain_solution.y.shape[1])
        ]
    )
    state_relative_errors = [
        float(
            np.linalg.norm(cse_states[:, index] - plain_states[:, index])
            / max(float(np.linalg.norm(plain_states[:, index])), 1.0e-30)
        )
        for index in range(values.size)
    ]
    endpoint_relative = state_relative_errors[-1]
    gamma_state = gamma_cap(source, p[:9])[0]
    cse_residual = interleaved(
        (gamma_state - np.asarray(cse_state, dtype=np.complex128)) / source.scales5
    )
    plain_residual = interleaved(
        (gamma_state - np.asarray(plain_state, dtype=np.complex128)) / source.scales5
    )
    residual_absolute_difference = float(
        np.max(np.abs(cse_residual - plain_residual))
    )
    residual_relative_descriptive = float(
        np.linalg.norm(cse_residual - plain_residual)
        / max(np.linalg.norm(plain_residual), 1.0e-30)
    )
    point_records: list[dict[str, Any]] = []
    maximum_rhs = 0.0
    maximum_hessian_action = 0.0
    probe = np.arange(1, M5_DIMENSION + 1, dtype=np.longdouble)
    probe /= np.linalg.norm(probe)
    factor = np.asarray(node.factor, dtype=np.longdouble)
    for index, fraction in enumerate(values):
        state_w = node.xi_to_w_long(cse_solution.y[:, index])
        cse_values = source.evaluator.evaluate(node.lambda_value, state_w, plain=False)
        plain_values = source.evaluator.evaluate(node.lambda_value, state_w, plain=True)
        cse_rhs = -np.conjugate(factor.T @ cse_values[1])
        plain_rhs = -np.conjugate(factor.T @ plain_values[1])
        rhs_error = float(
            np.linalg.norm(cse_rhs - plain_rhs)
            / max(float(np.linalg.norm(plain_rhs)), 1.0e-30)
        )
        cse_hessian_action = factor.T @ cse_values[2] @ factor @ probe
        plain_hessian_action = factor.T @ plain_values[2] @ factor @ probe
        hessian_action_error = float(
            np.linalg.norm(cse_hessian_action - plain_hessian_action)
            / max(float(np.linalg.norm(plain_hessian_action)), 1.0e-30)
        )
        maximum_rhs = max(maximum_rhs, rhs_error)
        maximum_hessian_action = max(
            maximum_hessian_action, hessian_action_error
        )
        point_records.append(
            {
                "fraction": float(fraction),
                "state_relative_error_between_reintegrations": state_relative_errors[index],
                "same_point_rhs_relative_error": rhs_error,
                "same_point_hessian_action_relative_error": hessian_action_error,
                "state_dtype": str(np.asarray(state_w).dtype),
                "rhs_dtype": str(np.asarray(cse_rhs).dtype),
                "hessian_action_dtype": str(
                    np.asarray(cse_hessian_action).dtype
                ),
            }
        )
    passed = bool(
        max(state_relative_errors)
        <= source.thresholds.cse_endpoint_state_relative_error
        and endpoint_relative
        <= source.thresholds.cse_endpoint_state_relative_error
        and residual_absolute_difference
        <= source.thresholds.cse_scaled_residual_absolute_difference
        and maximum_rhs <= source.thresholds.cse_rhs_relative_error
        and maximum_hessian_action
        <= source.thresholds.cse_hessian_action_relative_error
    )
    return {
        "status": "PASS" if passed else "INCONCLUSIVE",
        "passed": passed,
        "lambda": node.lambda_value,
        "fractions": values,
        "points": point_records,
        "maximum_trajectory_state_relative_error": float(
            max(state_relative_errors)
        ),
        "endpoint_state_relative_error": endpoint_relative,
        "scaled_residual_absolute_difference": residual_absolute_difference,
        "scaled_residual_relative_error_descriptive_only": residual_relative_descriptive,
        "maximum_same_point_rhs_relative_error": maximum_rhs,
        "maximum_same_point_hessian_action_relative_error": maximum_hessian_action,
        "CSE_endpoint_state_z": cse_state,
        "nonCSE_endpoint_state_z": plain_state,
        "CSE_integration": cse_integration,
        "nonCSE_integration": plain_integration,
    }


def parse_numerics(manifest: Mapping[str, Any]) -> Numerics:
    raw = require(manifest, "fixed_numerics", where="manifest")
    integration = require(raw, "integration", where="fixed_numerics")
    state = require(integration, "state", where="fixed_numerics.integration")
    tangent = require(integration, "tangent", where="fixed_numerics.integration")
    newton = require(raw, "damped_newton", where="fixed_numerics")
    saddle = require(raw, "saddle_solver", where="fixed_numerics")
    return Numerics(
        method=str(require(integration, "method", where="fixed_numerics.integration")),
        state_rtol=finite_float(require(state, "rtol", where="state"), label="state rtol"),
        state_atol=finite_float(require(state, "atol", where="state"), label="state atol"),
        state_max_step=finite_float(require(state, "max_step", where="state"), label="state max_step"),
        tangent_rtol=finite_float(require(tangent, "rtol", where="tangent"), label="tangent rtol"),
        tangent_atol=finite_float(require(tangent, "atol", where="tangent"), label="tangent atol"),
        tangent_max_step=finite_float(require(tangent, "max_step", where="tangent"), label="tangent max_step"),
        newton_max_iterations=int(require(newton, "max_iterations", where="damped_newton")),
        newton_target_max_abs=finite_float(require(newton, "target_scaled_residual_max_abs", where="damped_newton"), label="Newton target"),
        line_search_minimum=finite_float(require(newton, "minimum_damping", where="damped_newton"), label="minimum damping"),
        saddle_tolerance=finite_float(require(saddle, "xtol", where="saddle_solver"), label="saddle xtol"),
        saddle_maxfev=int(require(saddle, "maxfev", where="saddle_solver")),
        ledger_samples=int(require(raw, "flow_ledger_sample_count", where="fixed_numerics")),
    )


def parse_thresholds(manifest: Mapping[str, Any]) -> Thresholds:
    raw = require(manifest, "thresholds", where="manifest")
    chart = require(manifest, "launch_chart", where="manifest")

    def value(key: str) -> float:
        return finite_float(require(raw, key, where="thresholds"), label=key)

    return Thresholds(
        saddle_reproduction_distance=value("phase50_saddle_reproduction_distance_max"),
        saddle_gradient_max_abs=value("saddle_gradient_max_abs"),
        saddle_hessian_min_abs_eigenvalue=value("saddle_hessian_min_abs_eigenvalue"),
        physical_residual_max_abs=value("physical_residual_max_abs"),
        scaled_residual_max_abs=value("scaled_residual_max_abs"),
        normalized_sigma_min=value("normalized_transversality_sigma_min"),
        field_margin=value("minimum_y_margin"),
        psi_margin=value("minimum_psi_margin"),
        chart_margin=value("minimum_u_margin"),
        flow_time_margin=value("minimum_flow_time_margin"),
        flow_norm_max=finite_float(
            require(chart, "flow_norm_max", where="launch_chart"),
            label="flow_norm_max",
        ),
        flow_norm_margin=value("minimum_flow_norm_margin"),
        factor_identity_relative=value("factor_identity_relative_max"),
        lambda0_launch_replay_relative=value("lambda0_launch_replay_relative_max"),
        path_state_distance=value("mesh_reverse_cap_state_distance_max"),
        reflection_state_distance=value("reflection_cap_state_distance_max"),
        reflection_action_absolute=value("reflection_action_absolute_max"),
        mutation_state_distance=value("endpoint_control_cap_state_distance_max"),
        fd_operator_error=value("full_J_FD_variational_operator_relative_max"),
        fd_max_column_error=value("full_J_FD_max_column_relative_max"),
        fd_plateau=value("full_J_FD_adjacent_relative_max"),
        outer_tangent_resolved_error=value("path_tangent_implicit_resolved_relative_max"),
        outer_tangent_adjacent_error=value("path_tangent_adjacent_relative_max"),
        action_real_positive_step=value("ReS_max_positive_sample_increment"),
        action_imag_drift=value("ImS_max_drift"),
        first_cap_radius_residual=value("first_cap_radius_residual_max"),
        first_cap_time_difference=value("first_cap_time_difference_max"),
        first_cap_state_distance=value("first_cap_endpoint_state_distance_max"),
        cse_rhs_relative_error=value("CSE_nonCSE_rhs_relative_max"),
        cse_hessian_action_relative_error=value("CSE_nonCSE_hessian_action_relative_max"),
        cse_endpoint_state_relative_error=value("CSE_nonCSE_endpoint_state_relative_max"),
        cse_scaled_residual_absolute_difference=value(
            "CSE_nonCSE_scaled_residual_absolute_difference_max"
        ),
    )


def parse_bounds(manifest: Mapping[str, Any]) -> Bounds:
    common = require(manifest, "gamma_and_root_map", where="manifest")
    bounds = require(common, "parameter_bounds", where="gamma_and_root_map")
    lower = finite_vector(require(bounds, "lower", where="parameter_bounds"), REAL_DIMENSION, label="lower bounds")
    upper = finite_vector(require(bounds, "upper", where="parameter_bounds"), REAL_DIMENSION, label="upper bounds")
    if np.any(lower >= upper):
        raise InvalidRun("parameter bounds are not ordered")
    return Bounds(lower=lower, upper=upper)


def validate_inputs(
    manifest: Mapping[str, Any], audit: Audit
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if INPUT_SHA256 == "MANIFEST_PENDING" or INPUT_COMMIT == "MANIFEST_PENDING":
        raise InvalidRun("Phase51 manifest digest/commit placeholders were not replaced")
    observed_manifest = sha256_path(INPUT_PATH)
    audit.add_exact(
        "P51.input.manifest_hash",
        observed_manifest == INPUT_SHA256,
        "the frozen Phase51 manifest matches its post-freeze SHA-256",
        {"observed": observed_manifest, "expected": INPUT_SHA256, "commit": INPUT_COMMIT},
    )
    audit.add_exact(
        "P51.input.schema",
        manifest.get("schema") == "ice-phase51-m5-gamma-k-local-continuation-inputs/v1"
        and manifest.get("phase") == 51,
        "manifest schema and phase are exact",
    )
    platform_spec = require(
        require(manifest, "evaluator", where="manifest"),
        "platform",
        where="evaluator",
    )
    observed_platform = {
        "clongdouble_itemsize": int(np.dtype(np.clongdouble).itemsize),
        "longdouble_itemsize": int(np.dtype(np.longdouble).itemsize),
        "longdouble_mantissa_bits_excluding_implicit": int(
            np.finfo(np.longdouble).nmant
        ),
        "longdouble_epsilon": str(np.finfo(np.longdouble).eps),
    }
    audit.add_exact(
        "P51.evaluator.clongdouble_platform",
        all(
            str(observed_platform[key]) == str(platform_spec[key])
            for key in observed_platform
        ),
        "the runtime long-double representation matches the frozen P49-compatible platform contract",
        {"observed": observed_platform, "expected": platform_spec},
    )
    observed: dict[str, Any] = {}
    pinned = require(manifest, "pinned_inputs", where="manifest")
    for label, specification in pinned.items():
        path = REPO_ROOT / str(require(specification, "path", where=f"pinned_inputs.{label}"))
        digest = sha256_path(path)
        expected = str(require(specification, "sha256", where=f"pinned_inputs.{label}"))
        if digest != expected:
            raise InvalidRun(f"pinned input hash drift: {label}")
        observed[label] = {
            "path": str(specification["path"]),
            "commit": str(require(specification, "commit", where=f"pinned_inputs.{label}")),
            "sha256": digest,
            "role": specification.get("role"),
        }
    p42, _ = load_unique_json(PHASE42_CHECKPOINT_PATH)
    p49, _ = load_unique_json(PHASE49_RESULT_PATH)
    p50, _ = load_unique_json(PHASE50_RESULT_PATH)
    verify_self_digest(p42, label="Phase42 checkpoint")
    verify_self_digest(p49, label="Phase49 result")
    verify_self_digest(p50, label="Phase50 result")
    readiness = bool(
        p42.get("checkpoint_status") == "POST_HOC_REGENERATED_CHECKPOINT"
        and p49.get("run_status") == "VALID_RUN"
        and p49.get("classification")
        == "FULL_FLOW_CLONGDOUBLE_STATE_MAP_REPAIR_SUPPORTED"
        and p50.get("run_status") == "VALID_RUN"
        and p50.get("classification")
        == "LOCAL_STABILIZED_M4_M5_SADDLE_UPWARD_PLANE_TRANSPORT_SUPPORTED_ON_FROZEN_PATHS"
    )
    audit.add_exact(
        "P51.input.upstream_readiness",
        readiness,
        "P42 checkpoint, P49 precision repair, and P50 bridge are accepted upstream inputs",
    )
    required_outputs = require(manifest, "required_outputs", where="manifest")
    null_keys = (
        "required_independent_contradiction_certificate",
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
    )
    false_keys = (
        "contradicted_output_allowed",
        "straight_arm_intersections_searched",
        "cap_reintersections_searched",
        "continuous_direction_coverage_proved",
        "root_exhaustion_proved",
        "all_saddles_and_upward_components_complete",
        "non_Stokes_chamber_certified",
        "all_relative_good_ends_classified",
        "physical_original_cycle_derived",
        "common_determinant_line_constructed",
    )
    classification = require(manifest, "classification", where="manifest")
    audit.add_exact(
        "P51.guard.global_nulls",
        all(required_outputs.get(key) is None for key in null_keys)
        and all(required_outputs.get(key) is False for key in false_keys)
        and required_outputs.get("global_promotion") == "PROHIBITED"
        and classification.get("global_promotion_allowed") is False
        and classification.get("contradicted_selectable_by_runner") is False,
        "global, physical, and contradiction outputs remain explicitly prohibited/null",
    )
    return observed, p42, p49, p50


def build_chart(p42: Mapping[str, Any]) -> Chart8:
    chart4 = require(p42, "upward_chart", where="Phase42")
    center4 = decode_array(require(chart4, "center", where="upward_chart"), label="P42 chart center")
    tangent4 = decode_array(require(chart4, "tangent", where="upward_chart"), label="P42 chart tangent")
    if center4.shape != (7,) or tangent4.shape != (7, 6):
        raise InvalidRun("P42 chart dimensions drifted")
    center = np.concatenate([np.asarray(center4, dtype=float), [0.0, 0.0]])
    tangent = np.zeros((9, 8), dtype=float)
    tangent[:7, :6] = tangent4
    tangent[7, 6] = 1.0
    tangent[8, 7] = 1.0
    determinant = float(np.linalg.det(np.column_stack([tangent, center])))
    if determinant <= 0.0 or np.linalg.norm(tangent.T @ tangent - np.eye(8)) > 1.0e-10:
        raise InvalidRun("extended S8 chart lost positive orientation/orthonormality")
    return Chart8(center=center, tangent=tangent, orientation_determinant=determinant)


def p42_parameter_seed(p42: Mapping[str, Any], label: str) -> np.ndarray:
    record = p42["primary_intersections"]["all_phase41_results"][label]
    old = finite_vector(record["parameters"], 14, label=f"P42 {label} parameters")
    output = np.zeros(18, dtype=float)
    output[:6] = old[:6]
    output[6:8] = 0.0
    output[8] = old[6]
    output[9:15] = old[7:13]
    output[15:17] = 0.0
    output[17] = old[13]
    return output


def source_context(
    label: str,
    manifest: Mapping[str, Any],
    p42: Mapping[str, Any],
    p50: Mapping[str, Any],
    phase50: ModuleType,
    numerics: Numerics,
    thresholds: Thresholds,
    bounds: Bounds,
) -> SourceContext:
    embedding = phase50.build_embedding()
    source_point = p50["points"][label]["source_point"]
    delta_a, delta_phi = (float(source_point[0]), float(source_point[1]))
    phase50_manifest, _ = load_unique_json(
        SCRIPT_PATH.with_name("PHASE50_M4_M5_JOINT_SADDLE_HOMOTOPY_INPUTS.json")
    )
    stabilizer = require(
        require(phase50_manifest, "action_homotopy", where="Phase50 manifest"),
        "added_mode_stabilizers",
        where="Phase50 action_homotopy",
    )
    kappa_a = finite_float(require(stabilizer, "kappa_a", where="stabilizer"), label="kappa_a")
    kappa_phi = finite_float(require(stabilizer, "kappa_phi", where="stabilizer"), label="kappa_phi")
    basis_bytes = np.asarray(embedding.basis, dtype="<f8").tobytes()
    evaluator = build_long_evaluator(
        label, delta_a, delta_phi, kappa_a, kappa_phi, basis_bytes
    )
    p50_records = p50["points"][label]["nominal"]["fine_forward"]["records"]
    saddles = {
        round(float(record["lambda"]), 14): finite_vector(
            record["w5"], 9, label=f"P50 {label} saddle"
        )
        for record in p50_records
    }
    mobility0 = np.asarray(p50["shared_metric_paths"]["mobility0"], dtype=float)
    mobility1 = np.asarray(p50["shared_metric_paths"]["mobility1"], dtype=float)
    fixed_l4 = decode_array(p42["fixed_metric"]["linear_map"], label="P42 L4")
    factor_block = np.zeros((9, 9), dtype=float)
    factor_block[:7, :7] = fixed_l4
    factor_block[7, 7] = 1.0 / np.sqrt(abs(kappa_a))
    factor_block[8, 8] = 1.0 / np.sqrt(abs(kappa_phi))
    factor0 = embedding.basis @ factor_block
    aligned4 = decode_array(
        p42["saddles"][label]["aligned_signed_frame_xi"],
        label=f"P42 {label} aligned signed frame",
    )
    if aligned4.shape != (7, 7) or np.max(np.abs(np.asarray(aligned4).imag)) > 0.0:
        raise InvalidRun(f"P42 {label} signed frame shape/type drift")
    reference_signed_frame = np.zeros((9, 9), dtype=float)
    reference_signed_frame[:7, :7] = np.asarray(aligned4.real, dtype=float)
    reference_signed_frame[7, 7] = 1.0
    reference_signed_frame[8, 8] = 1.0
    p42_launch_by_shape: dict[str, np.ndarray] = {}
    for shape_key in ("lambda_0", "lambda_0.5", "lambda_1"):
        launch4 = decode_array(
            p42["saddles"][label]["launch_matrices"][shape_key],
            label=f"P42 {label} launch {shape_key}",
        )
        launch_coefficient = np.zeros((9, 9), dtype=np.complex128)
        launch_coefficient[:7, :7] = launch4
        launch_coefficient[7, 7] = -1.0
        launch_coefficient[8, 8] = 1.0j
        p42_launch_by_shape[shape_key] = launch_coefficient
    production = require(manifest, "launch_chart", where="manifest")
    radius = finite_float(
        require(production, "launch_radius", where="launch_chart"),
        label="primary sphere radius",
    )
    common = require(
        manifest,
        "gamma_and_root_map",
        where="manifest",
    )
    cap_radius = finite_float(
        require(common, "cap_radius", where="gamma_and_root_map"),
        label="cap radius",
    )
    phase41 = load_module(f"ice_phase41_constants_{label}", PHASE41_SOURCE_PATH)
    scales5 = phase50.coordinate_scales(phase41, 5)
    return SourceContext(
        label=label,
        delta_a=delta_a,
        delta_phi=delta_phi,
        evaluator=evaluator,
        chart=build_chart(p42),
        p42_seed=p42_parameter_seed(p42, label),
        p50_saddles=saddles,
        scales5=scales5,
        prolongation=embedding.field_prolongation,
        added_mode=embedding.added_mode,
        reflection5=embedding.reflection_m5,
        mobility0=mobility0,
        mobility1=mobility1,
        factor0=factor0,
        reference_signed_frame=reference_signed_frame,
        p42_launch_by_shape=p42_launch_by_shape,
        cap_radius=cap_radius,
        radius_primary=radius,
        numerics=numerics,
        thresholds=thresholds,
        bounds=bounds,
    )


def path_comparisons(
    left: Mapping[str, Any], right: Mapping[str, Any], scales: np.ndarray
) -> dict[str, dict[str, Any]]:
    left_records = {
        round(float(record["lambda"]), 14): record
        for record in left.get("records", [])
        if record.get("accepted")
    }
    right_records = {
        round(float(record["lambda"]), 14): record
        for record in right.get("records", [])
        if record.get("accepted")
    }
    output: dict[str, dict[str, Any]] = {}
    for value in sorted(set(left_records) & set(right_records)):
        left_record = left_records[value]
        right_record = right_records[value]
        left_state = np.asarray(left_record["intersection_z"], dtype=np.complex128)
        right_state = np.asarray(right_record["intersection_z"], dtype=np.complex128)
        gamma_transition = frame_transition(
            left_record["gamma_frame"], right_record["gamma_frame"]
        )
        k_transition = frame_transition(
            left_record["k_frame"], right_record["k_frame"]
        )
        gauge_sign = (
            gamma_transition["transition_orientation"]["sign"]
            * k_transition["transition_orientation"]["sign"]
        )
        corrected_direct_agrees = bool(
            right_record["direct_orientation"]["sign"] * gauge_sign
            == left_record["direct_orientation"]["sign"]
        )
        corrected_root_agrees = bool(
            right_record["root_jacobian_orientation"]["sign"] * gauge_sign
            == left_record["root_jacobian_orientation"]["sign"]
        )
        output[f"lambda={value:.12g}"] = {
            "normalized_state_distance": float(
                np.linalg.norm(interleaved((left_state - right_state) / scales))
            ),
            "raw_parameter_distance_diagnostic": float(
                np.linalg.norm(
                    np.asarray(left_record["parameters"], dtype=float)
                    - np.asarray(right_record["parameters"], dtype=float)
                )
            ),
            "direct_orientation_sign_agrees": bool(
                left_record["direct_orientation"]["sign"]
                == right_record["direct_orientation"]["sign"]
            ),
            "root_orientation_sign_agrees": bool(
                left_record["root_jacobian_orientation"]["sign"]
                == right_record["root_jacobian_orientation"]["sign"]
            ),
            "gamma_tangent_transition": gamma_transition,
            "K_tangent_transition": k_transition,
            "determinant_corrected_direct_sign_agrees": corrected_direct_agrees,
            "determinant_corrected_root_sign_agrees": corrected_root_agrees,
        }
    return output


def reflected_state_distances(
    plus_path: Mapping[str, Any],
    minus_path: Mapping[str, Any],
    plus_source: SourceContext,
    minus_source: SourceContext,
) -> dict[str, dict[str, Any]]:
    plus_records = {
        round(float(record["lambda"]), 14): record
        for record in plus_path["records"] if record.get("accepted")
    }
    minus_records = {
        round(float(record["lambda"]), 14): record
        for record in minus_path["records"] if record.get("accepted")
    }
    output: dict[str, dict[str, Any]] = {}
    ambient = complex_linear_real_map(plus_source.reflection5)
    ambient_orientation = normalized_orientation(ambient)
    for value in sorted(set(plus_records) & set(minus_records)):
        plus = np.asarray(plus_records[value]["intersection_z"], dtype=np.complex128)
        minus = np.asarray(minus_records[value]["intersection_z"], dtype=np.complex128)
        reflected = plus_source.reflection5 @ plus
        plus_saddle = plus_source.saddle(value)
        minus_saddle = minus_source.saddle(value)
        plus_action = plus_source.evaluator.evaluate(value, plus_saddle)[0]
        minus_action = minus_source.evaluator.evaluate(value, minus_saddle)[0]
        gamma_transition = frame_transition(
            plus_records[value]["gamma_frame"],
            minus_records[value]["gamma_frame"],
            ambient=ambient,
        )
        k_transition = frame_transition(
            plus_records[value]["k_frame"],
            minus_records[value]["k_frame"],
            ambient=ambient,
        )
        gauge_sign = (
            gamma_transition["transition_orientation"]["sign"]
            * k_transition["transition_orientation"]["sign"]
        )
        expected_factor = ambient_orientation["sign"]
        corrected_direct_agrees = bool(
            minus_records[value]["direct_orientation"]["sign"] * gauge_sign
            == expected_factor * plus_records[value]["direct_orientation"]["sign"]
        )
        corrected_root_agrees = bool(
            minus_records[value]["root_jacobian_orientation"]["sign"] * gauge_sign
            == expected_factor
            * plus_records[value]["root_jacobian_orientation"]["sign"]
        )
        output[f"lambda={value:.12g}"] = {
            "normalized_cap_state_distance": float(
                np.linalg.norm(
                    interleaved((reflected - minus) / plus_source.scales5)
                )
            ),
            "normalized_saddle_distance": float(
                np.linalg.norm(
                    plus_source.reflection5 @ plus_saddle - minus_saddle
                )
            ),
            "saddle_action_absolute_difference": float(
                abs(plus_action - minus_action)
            ),
            "direct_orientation_sign_agrees": bool(
                plus_records[value]["direct_orientation"]["sign"]
                == minus_records[value]["direct_orientation"]["sign"]
            ),
            "root_orientation_sign_agrees": bool(
                plus_records[value]["root_jacobian_orientation"]["sign"]
                == minus_records[value]["root_jacobian_orientation"]["sign"]
            ),
            "plus_normalized_sigma_min": plus_records[value]["direct_orientation"]["normalized_sigma_min"],
            "minus_normalized_sigma_min": minus_records[value]["direct_orientation"]["normalized_sigma_min"],
            "ambient_reflection_orientation": ambient_orientation,
            "gamma_tangent_transition": gamma_transition,
            "K_tangent_transition": k_transition,
            "determinant_corrected_direct_sign_agrees": corrected_direct_agrees,
            "determinant_corrected_root_sign_agrees": corrected_root_agrees,
        }
    return output


def run() -> dict[str, Any]:
    audit = Audit()
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    observed_inputs, p42, p49, p50 = validate_inputs(manifest, audit)
    numerics = parse_numerics(manifest)
    thresholds = parse_thresholds(manifest)
    bounds = parse_bounds(manifest)
    phase50 = load_module("ice_phase50_for_phase51_runtime", PHASE50_SOURCE_PATH)
    controls = require(manifest, "controls", where="manifest")
    continuation = require(manifest, "continuation", where="manifest")
    fine_nodes = [finite_float(value, label="fine lambda") for value in require(continuation, "fine_forward", where="continuation")]
    coarse_nodes = [finite_float(value, label="coarse lambda") for value in require(continuation, "coarse_forward", where="continuation")]
    reverse_nodes = [finite_float(value, label="reverse lambda") for value in require(continuation, "fine_reverse", where="continuation")]
    if fine_nodes != sorted(fine_nodes) or coarse_nodes != sorted(coarse_nodes) or reverse_nodes != sorted(reverse_nodes, reverse=True):
        raise InvalidRun("continuation meshes have the wrong directions")
    if len(fine_nodes) != 17 or len(coarse_nodes) != 9 or len(reverse_nodes) != 17:
        raise InvalidRun("continuation mesh counts drifted from fine17/coarse9/reverse17")

    progress("building complex-safe CSE clongdouble evaluators")
    plus = source_context(
        "phi_plus", manifest, p42, p50, phase50, numerics, thresholds, bounds
    )
    minus = source_context(
        "phi_minus", manifest, p42, p50, phase50, numerics, thresholds, bounds
    )
    audit.add_exact(
        "P51.chart.S8_orientation",
        plus.chart.orientation_determinant > 0.0
        and minus.chart.orientation_determinant > 0.0,
        "the Phase42 S6 chart plus two stabilizer axes is a positive S8 chart",
        {"determinant": plus.chart.orientation_determinant},
    )
    expected_parameter_order = [
        "y_a1", "y_phi1", "y_a2", "y_phi2", "y_a3", "y_phi3",
        "y_added_a", "y_added_phi", "psi",
        "u1", "u2", "u3", "u4", "u5", "u6",
        "u_added_a", "u_added_phi", "flow_time",
    ]
    gamma_spec = require(manifest, "gamma_and_root_map", where="manifest")
    model_spec = require(manifest, "model_path", where="manifest")
    audit.add_exact(
        "P51.coordinates.orders_and_scales",
        require(gamma_spec, "root_parameter_order", where="gamma_and_root_map")
        == expected_parameter_order
        and np.array_equal(
            finite_vector(
                require(model_spec, "coordinate_scales", where="model_path"),
                9,
                label="manifest coordinate scales",
            ),
            plus.scales5,
        )
        and abs(plus.cap_radius - 0.3) == 0.0,
        "the R18 parameter order, m5 coordinate scales, and cap radius are frozen exactly",
    )
    audit.add_exact(
        "P51.evaluator.CSE_symbolic_reconstruction",
        len(CSE_EXACT_LEDGER) == 4
        and all(record["exact_back_substitution"] for record in CSE_EXACT_LEDGER),
        "joint canonical CSE outputs back-substitute exactly to every action/gradient/Hessian expression",
        {"callable_sets": CSE_EXACT_LEDGER},
    )
    factor_residuals = []
    launch_residuals = []
    for source in (plus, minus):
        for lam in (0.0, 0.5, 1.0):
            node = source.node(lam)
            factor_residuals.append(
                float(
                    np.linalg.norm(
                        node.factor @ node.factor.T - node.mobility
                    )
                    / np.linalg.norm(node.mobility)
                )
            )
        node0 = source.node(0.0)
        expected_launch0 = source.factor0 @ source.p42_launch_by_shape["lambda_1"]
        launch_residuals.append(
            float(
                np.linalg.norm(node0.launch_w - expected_launch0)
                / np.linalg.norm(expected_launch0)
            )
        )
    audit.add_exact(
        "P51.launch.common_factor_identity",
        max(factor_residuals) <= thresholds.factor_identity_relative
        and max(launch_residuals) <= thresholds.lambda0_launch_replay_relative
        and all(float(np.linalg.det(source.factor0)) > 0.0 for source in (plus, minus)),
        "the real common factor obeys A_t A_t^T=M_t and its separate source-specific launch gauge returns the P42 lift at t=0",
        {
            "factor_relative_residuals": factor_residuals,
            "lambda0_launch_relative_residuals": launch_residuals,
        },
    )

    evaluator_spec = require(manifest, "evaluator", where="manifest")
    cse_lambdas = require(evaluator_spec, "paired_lambdas", where="evaluator")
    cse_controls = {
        source.label: cse_validation(source, cse_lambdas)
        for source in (plus, minus)
    }
    if not all(
        record["dtype_contract_passed"] for record in cse_controls.values()
    ):
        raise InvalidRun("CSE evaluator left the frozen clongdouble dtype contract")
    audit.add_exact(
        "P51.evaluator.CSE_equivalence",
        True,
        "CSE production evaluation retains the frozen clongdouble dtype contract",
        {
            label: {
                "maximum_rhs_relative_error": value[
                    "maximum_rhs_relative_error"
                ],
                "maximum_hessian_action_relative_error": value[
                    "maximum_hessian_action_relative_error"
                ],
                "dtype_contract_passed": value["dtype_contract_passed"],
            }
            for label, value in cse_controls.items()
        },
    )

    progress("continuing independent phi_plus fine/coarse paths")
    plus_fine = solve_path(plus, fine_nodes, plus.p42_seed, label="phi_plus:fine")
    plus_coarse = solve_path(plus, coarse_nodes, plus.p42_seed, label="phi_plus:coarse")
    plus_reverse: dict[str, Any]
    if plus_fine.get("completed"):
        plus_reverse = solve_path(
            plus,
            reverse_nodes,
            np.asarray(plus_fine["endpoint_parameters"], dtype=float),
            label="phi_plus:reverse",
        )
    else:
        plus_reverse = {
            "status": "INCONCLUSIVE",
            "completed": False,
            "message": "fine path did not supply a reverse seed",
            "requested_node_count": len(reverse_nodes),
            "attempted_node_count": 0,
            "retained_node_count": len(reverse_nodes),
            "requested_lambdas": reverse_nodes,
            "records": [
                {
                    "status": "INCONCLUSIVE",
                    "accepted": False,
                    "lambda": lam,
                    "message": "not attempted because fine-forward supplied no endpoint seed",
                }
                for lam in reverse_nodes
            ],
            "roots": {},
        }
    progress("continuing independent reflected phi_minus fine path")
    minus_fine = solve_path(minus, fine_nodes, minus.p42_seed, label="phi_minus:fine")

    coarse_fine = path_comparisons(plus_fine, plus_coarse, plus.scales5)
    reverse_fine = path_comparisons(plus_fine, plus_reverse, plus.scales5)
    reflection_distances = reflected_state_distances(
        plus_fine, minus_fine, plus, minus
    )
    fine_forward_pass = bool(
        plus_fine.get("completed") and minus_fine.get("completed")
    )
    coarse_reverse_pass = bool(
        plus_coarse.get("completed")
        and plus_reverse.get("completed")
        and len(coarse_fine) == len(coarse_nodes)
        and len(reverse_fine) == len(reverse_nodes)
        and max(
            value["normalized_state_distance"] for value in coarse_fine.values()
        ) <= thresholds.path_state_distance
        and max(
            value["normalized_state_distance"] for value in reverse_fine.values()
        ) <= thresholds.path_state_distance
        and all(
            value["determinant_corrected_direct_sign_agrees"]
            and value["determinant_corrected_root_sign_agrees"]
            for value in list(coarse_fine.values()) + list(reverse_fine.values())
        )
    )
    reflection_pass = bool(
        len(reflection_distances) == len(fine_nodes)
        and max(
            value["normalized_cap_state_distance"]
            for value in reflection_distances.values()
        ) <= thresholds.reflection_state_distance
        and max(
            value["normalized_saddle_distance"]
            for value in reflection_distances.values()
        ) <= thresholds.saddle_reproduction_distance
        and max(
            value["saddle_action_absolute_difference"]
            for value in reflection_distances.values()
        ) <= thresholds.reflection_action_absolute
        and all(
            value["determinant_corrected_direct_sign_agrees"]
            and value["determinant_corrected_root_sign_agrees"]
            for value in reflection_distances.values()
        )
    )
    path_controls_pass = bool(
        fine_forward_pass and coarse_reverse_pass and reflection_pass
    )
    audit.add_numerical(
        "P51.continuation.fine_coarse_reverse_reflection",
        path_controls_pass,
        "fine17/coarse9/reverse17 agree and an independently solved reflected fine17 path agrees in state space",
        {
            "maximum_coarse_fine_state_distance": max(
                (value["normalized_state_distance"] for value in coarse_fine.values()),
                default=None,
            ),
            "maximum_reverse_fine_state_distance": max(
                (value["normalized_state_distance"] for value in reverse_fine.values()),
                default=None,
            ),
            "maximum_reflection_state_distance": max(
                (
                    value["normalized_cap_state_distance"]
                    for value in reflection_distances.values()
                ),
                default=None,
            ),
        },
    )

    fd_controls: dict[str, Any] = {
        f"lambda={lam:.1f}": {
            "status": "INCONCLUSIVE",
            "passed": False,
            "lambda": lam,
            "message": "primary fine path incomplete",
        }
        for lam in (0.0, 0.5, 1.0)
    }
    flow_ledgers: dict[str, Any] = {
        "phi_plus:fine": path_flow_ledgers(
            plus, plus_fine, label="phi_plus:fine"
        ),
        "phi_plus:coarse": path_flow_ledgers(
            plus, plus_coarse, label="phi_plus:coarse"
        ),
        "phi_plus:reverse": path_flow_ledgers(
            plus, plus_reverse, label="phi_plus:reverse"
        ),
        "phi_minus:fine": path_flow_ledgers(
            minus, minus_fine, label="phi_minus:fine"
        ),
        "endpoint_controls": {},
    }
    outer_control: dict[str, Any] = {
        "status": "INCONCLUSIVE",
        "passed": False,
        "message": "primary fine path incomplete",
    }
    mutations_spec = require(controls, "endpoint", where="controls")
    radius_values = [
        finite_float(value, label="radius control")
        for value in require(
            mutations_spec, "radius_controls", where="controls.endpoint"
        )
    ]
    shape_values = [
        finite_float(value, label="shape control")
        for value in require(
            mutations_spec, "shape_controls", where="controls.endpoint"
        )
    ]
    mutations: dict[str, Any] = {}
    for control_radius in radius_values:
        factor = control_radius / plus.radius_primary
        mutations[f"radius_factor={factor:g}"] = {
            "status": "INCONCLUSIVE",
            "accepted": False,
            "mutation_passed": False,
            "message": "primary fine path incomplete",
        }
    for shape_float in shape_values:
        shape_key = f"lambda_{shape_float:g}"
        mutations[f"shape={shape_key}"] = {
            "status": "INCONCLUSIVE",
            "accepted": False,
            "mutation_passed": False,
            "message": "primary fine path incomplete",
        }
    flow_ledgers["endpoint_controls"] = {
        key: {
            "status": "INCONCLUSIVE",
            "passed": False,
            "message": "endpoint control root was not accepted",
        }
        for key in mutations
    }
    trajectory_fractions = require(
        evaluator_spec, "paired_trajectory_fractions", where="evaluator"
    )
    cse_trajectory_controls: dict[str, Any] = {
        f"lambda={lam:.1f}": {
            "status": "INCONCLUSIVE",
            "passed": False,
            "lambda": lam,
            "message": "primary fine path incomplete",
        }
        for lam in (0.0, 0.5, 1.0)
    }
    if plus_fine.get("completed"):
        root_map = plus_fine["roots"]
        fd_spec = require(controls, "full_J_FD", where="controls")
        fd_steps = require(fd_spec, "steps", where="controls.full_J_FD")
        gamma_steps = require(fd_steps, "Gamma_y_and_psi", where="full_J_FD.steps")
        chart_steps = require(
            fd_steps,
            "K_old_u1_through_u6_and_added_u",
            where="full_J_FD.steps",
        )
        time_steps = require(fd_steps, "K_flow_time", where="full_J_FD.steps")
        ladders = [gamma_steps] * 9 + [chart_steps] * 8 + [time_steps]
        for lam in (0.0, 0.5, 1.0):
            key = round(lam, 14)
            parameters = root_map[key]
            record = next(
                item for item in plus_fine["records"]
                if round(float(item["lambda"]), 14) == key
            )
            progress(f"running two-step R18 finite differences at lambda={lam:.1f}")
            try:
                fd_controls[f"lambda={lam:.1f}"] = finite_difference_jacobian_control(
                    plus.node(lam),
                    parameters,
                    np.asarray(
                        record["variational_scaled_root_jacobian"], dtype=float
                    ),
                    ladders,
                )
            except (NumericalFailure, FloatingPointError, ValueError) as error:
                fd_controls[f"lambda={lam:.1f}"] = {
                    "status": "INCONCLUSIVE",
                    "passed": False,
                    "lambda": lam,
                    "message": str(error),
                }
            progress(
                f"independently reintegrating CSE/non-CSE trajectory at lambda={lam:.1f}"
            )
            try:
                cse_trajectory_controls[
                    f"lambda={lam:.1f}"
                ] = cse_trajectory_validation(
                    plus,
                    plus.node(lam),
                    parameters,
                    trajectory_fractions,
                )
            except (NumericalFailure, FloatingPointError, ValueError) as error:
                cse_trajectory_controls[f"lambda={lam:.1f}"] = {
                    "status": "INCONCLUSIVE",
                    "passed": False,
                    "lambda": lam,
                    "message": str(error),
                }
        outer_steps = require(
            require(controls, "path_tangent", where="controls"),
            "steps",
            where="path_tangent",
        )
        progress("running the lambda=0.5 outer implicit-tangent control")
        try:
            outer_control = outer_tangent_control(
                plus, root_map[round(0.5, 14)], outer_steps
            )
        except (NumericalFailure, FloatingPointError, ValueError) as error:
            outer_control = {
                "status": "INCONCLUSIVE",
                "passed": False,
                "message": str(error),
            }

        endpoint = root_map[round(1.0, 14)]
        primary_endpoint_record = next(
            record
            for record in plus_fine["records"]
            if round(float(record["lambda"]), 14) == round(1.0, 14)
        )
        for control_radius in radius_values:
            factor = control_radius / plus.radius_primary
            radius_seed = endpoint.copy()
            radius_seed[17] += math.log(plus.radius_primary / control_radius)
            control_node = plus.node(1.0, radius=control_radius)
            try:
                solved, record = solve_root(
                    control_node,
                    radius_seed,
                    label=f"endpoint-radius-{factor:g}",
                )
            except (NumericalFailure, FloatingPointError, ValueError) as error:
                solved = None
                record = {
                    "status": "INCONCLUSIVE",
                    "accepted": False,
                    "message": str(error),
                }
            distance = None
            if solved is not None and record.get("accepted"):
                distance = float(
                    np.linalg.norm(
                        interleaved(
                            (
                                np.asarray(record["intersection_z"], dtype=np.complex128)
                                - np.asarray(primary_endpoint_record["intersection_z"], dtype=np.complex128)
                            )
                            / plus.scales5
                        )
                    )
                )
            record["normalized_state_distance_to_primary"] = distance
            comparison: dict[str, Any] | None = None
            if solved is not None and record.get("accepted"):
                comparison = path_comparisons(
                    {"records": [primary_endpoint_record]},
                    {"records": [record]},
                    plus.scales5,
                ).get("lambda=1")
            record["same_candidate_tangent_comparison"] = comparison
            ledger = (
                safe_flow_ledger(control_node, solved)
                if solved is not None and record.get("accepted")
                else {
                    "status": "INCONCLUSIVE",
                    "passed": False,
                    "message": "mutation root was not accepted",
                }
            )
            record["flow_ledger"] = ledger
            record["mutation_passed"] = bool(
                record.get("accepted")
                and distance is not None
                and distance <= thresholds.mutation_state_distance
                and comparison is not None
                and comparison["determinant_corrected_direct_sign_agrees"]
                and comparison["determinant_corrected_root_sign_agrees"]
                and ledger.get("passed", False)
            )
            mutations[f"radius_factor={factor:g}"] = record
            flow_ledgers["endpoint_controls"][
                f"radius_factor={factor:g}"
            ] = ledger
        for shape_float in shape_values:
            shape_key = f"lambda_{shape_float:g}"
            control_node = plus.node(1.0, shape_key=shape_key)
            try:
                shape_seed = map_shape_seed(plus, endpoint, shape_key)
                solved, record = solve_root(
                    control_node,
                    shape_seed,
                    label=f"endpoint-shape-{shape_key}",
                )
            except (NumericalFailure, FloatingPointError, ValueError) as error:
                solved = None
                record = {
                    "status": "INCONCLUSIVE",
                    "accepted": False,
                    "message": str(error),
                }
            distance = None
            if solved is not None and record.get("accepted"):
                distance = float(
                    np.linalg.norm(
                        interleaved(
                            (
                                np.asarray(record["intersection_z"], dtype=np.complex128)
                                - np.asarray(primary_endpoint_record["intersection_z"], dtype=np.complex128)
                            )
                            / plus.scales5
                        )
                    )
                )
            record["normalized_state_distance_to_primary"] = distance
            comparison = None
            if solved is not None and record.get("accepted"):
                comparison = path_comparisons(
                    {"records": [primary_endpoint_record]},
                    {"records": [record]},
                    plus.scales5,
                ).get("lambda=1")
            record["same_candidate_tangent_comparison"] = comparison
            ledger = (
                safe_flow_ledger(control_node, solved)
                if solved is not None and record.get("accepted")
                else {
                    "status": "INCONCLUSIVE",
                    "passed": False,
                    "message": "mutation root was not accepted",
                }
            )
            record["flow_ledger"] = ledger
            record["mutation_passed"] = bool(
                record.get("accepted")
                and distance is not None
                and distance <= thresholds.mutation_state_distance
                and comparison is not None
                and comparison["determinant_corrected_direct_sign_agrees"]
                and comparison["determinant_corrected_root_sign_agrees"]
                and ledger.get("passed", False)
            )
            mutations[f"shape={shape_key}"] = record
            flow_ledgers["endpoint_controls"][f"shape={shape_key}"] = ledger

    fd_pass = bool(
        fd_controls and all(value.get("passed", False) for value in fd_controls.values())
    )
    mutation_pass = bool(
        mutations
        and all(value.get("mutation_passed", False) for value in mutations.values())
    )
    cse_trajectory_pass = bool(
        all(value.get("numeric_pair_passed", False) for value in cse_controls.values())
        and
        cse_trajectory_controls
        and all(
            value.get("passed", False)
            for value in cse_trajectory_controls.values()
        )
    )

    def all_ledgers_pass(path_label: str, expected_count: int) -> bool:
        records = flow_ledgers[path_label]
        return bool(
            len(records) == expected_count
            and all(value.get("passed", False) for value in records.values())
        )

    fine_forward_pass = bool(
        fine_forward_pass
        and all_ledgers_pass("phi_plus:fine", len(fine_nodes))
        and all_ledgers_pass("phi_minus:fine", len(fine_nodes))
    )
    coarse_reverse_pass = bool(
        coarse_reverse_pass
        and all_ledgers_pass("phi_plus:coarse", len(coarse_nodes))
        and all_ledgers_pass("phi_plus:reverse", len(reverse_nodes))
    )

    saddle_records: dict[str, Any] = {}
    saddle_pass = True
    for source in (plus, minus):
        source_records: dict[str, Any] = {}
        for lam in fine_nodes:
            record = source._saddle_records.get(round(lam, 14))
            source_records[f"lambda={lam:.12g}"] = record
            saddle_pass = bool(
                saddle_pass
                and record is not None
                and record.get("accepted", False)
                and record.get("distance_to_pinned_phase50") is not None
                and record["distance_to_pinned_phase50"]
                <= thresholds.saddle_reproduction_distance
            )
        saddle_records[source.label] = source_records

    lambda0_lifts: dict[str, Any] = {}
    lambda0_pass = True
    for lift_label, source, path in (
        ("phi_plus:fine", plus, plus_fine),
        ("phi_plus:coarse", plus, plus_coarse),
        ("phi_minus:fine", minus, minus_fine),
    ):
        record = next(
            (
                item
                for item in path.get("records", [])
                if round(float(item.get("lambda", -1.0)), 14) == 0.0
            ),
            None,
        )
        distance = None
        parameter_distance = None
        if record is not None and record.get("accepted", False):
            expected_state = gamma_cap(source, source.p42_seed[:9])[0]
            distance = float(
                np.linalg.norm(
                    interleaved(
                        (
                            np.asarray(record["intersection_z"], dtype=np.complex128)
                            - expected_state
                        )
                        / source.scales5
                    )
                )
            )
            parameter_distance = float(
                np.linalg.norm(
                    np.asarray(record["parameters"], dtype=float)
                    - source.p42_seed
                )
            )
        passed = bool(
            record is not None
            and record.get("accepted", False)
            and distance is not None
            and distance <= thresholds.path_state_distance
        )
        lambda0_pass = bool(lambda0_pass and passed)
        lambda0_lifts[lift_label] = {
            "passed": passed,
            "normalized_cap_state_distance_to_embedded_P42_seed": distance,
            "parameter_distance_to_embedded_P42_seed": parameter_distance,
        }

    required_outputs = require(manifest, "required_outputs", where="manifest")
    null_keys = (
        "required_independent_contradiction_certificate",
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
    )
    false_keys = (
        "contradicted_output_allowed",
        "straight_arm_intersections_searched",
        "cap_reintersections_searched",
        "continuous_direction_coverage_proved",
        "root_exhaustion_proved",
        "all_saddles_and_upward_components_complete",
        "non_Stokes_chamber_certified",
        "all_relative_good_ends_classified",
        "physical_original_cycle_derived",
        "common_determinant_line_constructed",
    )
    guard_pass = bool(
        all(required_outputs.get(key) is None for key in null_keys)
        and all(required_outputs.get(key) is False for key in false_keys)
        and required_outputs.get("global_promotion") == "PROHIBITED"
        and required_outputs.get("gate1") == "OPEN_PARTIAL_PROGRESS"
        and manifest["classification"]["contradicted_selectable_by_runner"]
        is False
    )

    contract = Audit()
    source_contract = bool(
        require(continuation, "source_order", where="continuation")
        == ["phi_plus", "phi_minus"]
        and (plus.delta_a, plus.delta_phi) == (0.0, 0.001)
        and (minus.delta_a, minus.delta_phi) == (0.0, -0.001)
    )
    coordinate_contract = bool(
        require(gamma_spec, "root_parameter_order", where="gamma_and_root_map")
        == expected_parameter_order
        and np.array_equal(
            finite_vector(
                require(model_spec, "coordinate_scales", where="model_path"),
                9,
                label="manifest coordinate scales",
            ),
            plus.scales5,
        )
        and plus.cap_radius == 0.3
        and finite_float(
            require(
                require(manifest, "launch_chart", where="manifest"),
                "primary_shape_exponent",
                where="launch_chart",
            ),
            label="primary shape exponent",
        )
        == 1.0
    )
    factor_contract = bool(
        max(factor_residuals) <= thresholds.factor_identity_relative
        and max(launch_residuals) <= thresholds.lambda0_launch_replay_relative
    )
    cse_exact_contract = bool(
        len(CSE_EXACT_LEDGER) == 4
        and all(record["exact_back_substitution"] for record in CSE_EXACT_LEDGER)
        and all(
            record["dtype_contract_passed"] for record in cse_controls.values()
        )
    )
    orientation_contract = bool(
        plus.chart.orientation_determinant > 0.0
        and minus.chart.orientation_determinant > 0.0
        and M5_DIMENSION % 2 == 1
        and all(
            source.node(lam).launch_record["signed_frame_determinant"] > 0.0
            for source in (plus, minus)
            for lam in (0.0, 0.5, 1.0)
        )
    )
    contract.add_exact(
        "P51.inputs.byte_pins_and_manifest_before_runner",
        bool(all(record["passed"] for record in audit.exact)),
        "the frozen manifest, upstream byte pins, self-digests, readiness labels, and platform inputs validate before the runner",
        {"manifest_commit": INPUT_COMMIT, "validated_pins": list(observed_inputs)},
    )
    contract.add_exact(
        "P51.action.Phase50_diagonal_path_identity",
        bool(
            source_contract
            and all(
                record.get("passed", False)
                for record in p50["shared_metric_paths"]["records"]["geodesic"]
            )
        ),
        "the two frozen sources use the pinned Phase50 action and affine-invariant metric on the diagonal lambda=mu path",
        {"sources": [[plus.delta_a, plus.delta_phi], [minus.delta_a, minus.delta_phi]]},
    )
    contract.add_exact(
        "P51.cap.R18_middle_dimension_and_common_coordinate_lambda0_lift",
        bool(coordinate_contract and factor_contract),
        "the R18 Gamma--K map, common A_lambda factor, cap, and source-specific lambda=0 P42 launch lift match the frozen conventions",
        {
            "factor_relative_residuals": factor_residuals,
            "lambda0_launch_relative_residuals": launch_residuals,
        },
    )
    contract.add_exact(
        "P51.evaluator.CSE_symbolic_reconstruction_and_clongdouble_contract",
        cse_exact_contract,
        "canonical joint CSE reconstructs exactly and the clongdouble state/RHS/Hessian-action contract agrees with the non-CSE evaluator",
        {"symbolic": CSE_EXACT_LEDGER, "paired_points": cse_controls},
    )
    contract.add_exact(
        "P51.orientation.orders_chart_and_odd_K_parity",
        orientation_contract,
        "the frozen orders and positive S8/signed-frame gauges are retained and nine K columns imply odd root/direct determinant parity",
    )
    contract.add_exact(
        "P51.guard.local_scope_forces_global_nulls",
        guard_pass,
        "local workbench scope keeps contradiction, global, cutoff, continuum, and physical promotion fields null or prohibited",
    )

    contract.add_numerical(
        "P51.saddles.Phase50_reproduction",
        saddle_pass,
        "both sources reproduce every common Phase50 saddle with the frozen inertia and residual gates",
        {"records": saddle_records},
    )
    contract.add_numerical(
        "P51.intersections.lambda0_lifts",
        lambda0_pass,
        "both independently solved lambda=0 R18 intersections replay the embedded Phase42 local candidates",
        lambda0_lifts,
    )
    contract.add_numerical(
        "P51.intersections.fine_forward_both_sources",
        fine_forward_pass,
        "independent phi_plus and phi_minus fine17 paths retain accepted roots and complete action/first-cap ledgers",
    )
    contract.add_numerical(
        "P51.intersections.coarse_and_reverse",
        coarse_reverse_pass,
        "the independent phi_plus coarse9 and reverse17 paths match fine17 ambient states with corrected tangent gauges and complete ledgers",
    )
    contract.add_numerical(
        "P51.reflection.independent_phi_pair",
        reflection_pass,
        "independently solved reflected fine paths agree in saddle, action, cap state, transversality, and determinant-corrected orientation",
    )
    contract.add_numerical(
        "P51.derivative.full_J_at_0_half_1",
        fd_pass,
        "two complete frozen-step R18 state-map finite-difference matrices agree with the variational Jacobian at lambda 0, 0.5, and 1",
    )
    contract.add_numerical(
        "P51.tangent.lambda_half",
        bool(outer_control.get("passed", False)),
        "the lambda=0.5 implicit tangent agrees with four independently accepted off-node roots and their path ledgers",
    )
    contract.add_numerical(
        "P51.evaluator.CSE_nonCSE_pairs",
        cse_trajectory_pass,
        "non-CSE reintegration of the three solved central phi_plus trajectories agrees at all frozen fractions, endpoints, and residuals",
    )
    contract.add_numerical(
        "P51.endpoint.radius_and_shape",
        mutation_pass,
        "both radius and both launch-shape controls retain accepted same-candidate states, corrected orientations, and first-cap/action ledgers",
    )
    contract.add_numerical(
        "P51.guard.classification_and_nulls",
        guard_pass,
        "the runner can select only the frozen supported or inconclusive local label and retains every global/null guard",
    )
    declared_checks = require(manifest, "checks", where="manifest")
    if [record["id"] for record in contract.exact] != require(
        declared_checks, "exact", where="checks"
    ):
        raise InvalidRun("emitted exact check slots drifted from the frozen manifest")
    if [record["id"] for record in contract.numerical] != require(
        declared_checks, "numerical", where="checks"
    ):
        raise InvalidRun("emitted numerical check slots drifted from the frozen manifest")

    all_numerical = all(record["passed"] for record in contract.numerical)
    classification_spec = require(manifest, "classification", where="manifest")
    supported_label = str(require(classification_spec, "supported_label", where="classification"))
    inconclusive_label = str(require(classification_spec, "inconclusive_label", where="classification"))
    classification = supported_label if all_numerical else inconclusive_label
    promoted = None
    if all_numerical and plus_fine.get("completed"):
        promoted = {
            "source": "phi_plus",
            "lambda": 1.0,
            "parameters": plus_fine["roots"][round(1.0, 14)],
            "intersection_z": plus_fine["records"][-1]["intersection_z"],
            "direct_orientation_sign": plus_fine["records"][-1]["direct_orientation"]["sign"],
            "root_jacobian_orientation_sign": plus_fine["records"][-1]["root_jacobian_orientation"]["sign"],
            "scope": "one frozen local m=5 Gamma--K candidate on the declared bridge",
        }
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 51,
        "run_status": "VALID_RUN",
        "classification": classification,
        "input_provenance": {
            "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "manifest_commit": INPUT_COMMIT,
            "runner_path": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "runner_sha256": sha256_path(SCRIPT_PATH),
            "phase42_checkpoint_self_digest": p42.get(
                "checkpoint_payload_sha256_without_self"
            ),
            "phase49_result_self_digest": p49.get(
                "result_payload_sha256_without_self"
            ),
            "phase50_result_self_digest": p50.get(
                "result_payload_sha256_without_self"
            ),
            "pinned_inputs": observed_inputs,
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
            "clongdouble_itemsize_bytes": int(np.dtype(np.clongdouble).itemsize),
            "longdouble_itemsize_bytes": int(np.dtype(np.longdouble).itemsize),
            "longdouble_mantissa_bits_excluding_implicit": int(
                np.finfo(np.longdouble).nmant
            ),
            "longdouble_epsilon": str(np.finfo(np.longdouble).eps),
            "platform": platform.platform(),
        },
        "exact_checks": contract.exact,
        "numerical_checks": contract.numerical,
        "internal_validation_subchecks": {
            "exact": audit.exact,
            "numerical": audit.numerical,
        },
        "evaluator_validation": {
            "same_point_source_lambda_pairs": cse_controls,
            "phi_plus_solved_trajectory_reintegrations": cse_trajectory_controls,
        },
        "saddle_reproduction": saddle_records,
        "lambda0_lifts": lambda0_lifts,
        "primary_phi_plus": {
            "fine_forward": plus_fine,
            "coarse_forward": plus_coarse,
            "fine_reverse": plus_reverse,
            "coarse_fine_state_comparisons": coarse_fine,
            "fine_reverse_state_comparisons": reverse_fine,
        },
        "independent_phi_minus_reflection": {
            "fine_forward": minus_fine,
            "fine_node_reflection_comparisons": reflection_distances,
        },
        "finite_difference_controls": fd_controls,
        "outer_lambda_tangent_control": outer_control,
        "flow_ledgers": flow_ledgers,
        "endpoint_mutations": mutations,
        "promoted_output": promoted,
        "gate1": required_outputs["gate1"],
        "global_promotion": required_outputs["global_promotion"],
        **{key: required_outputs[key] for key in null_keys},
        **{key: required_outputs[key] for key in false_keys},
        "computed_facts_scope": (
            "A local R18 continuation with nonlinear K flow, residual, rank, "
            "transversality, path, reflection, tangent, first-cap, and declared mutation controls."
        ),
        "not_computed": [
            "global thimble or end classification",
            "global Picard-Lefschetz coefficient",
            "cutoff removal",
            "a physics claim",
            "nonexistence when a solver or control is inconclusive",
        ],
        "interpretation_boundary": {
            "scope": require(manifest, "scope", where="manifest"),
            "global_promotion": require(
                require(manifest, "required_outputs", where="manifest"),
                "global_promotion",
                where="required_outputs",
            ),
        },
    }
    return with_self_digest(payload)


def failure_payload(error: Exception) -> dict[str, Any]:
    return with_self_digest(
        {
            "schema": RESULT_SCHEMA,
            "phase": 51,
            "run_status": "INVALID_RUN",
            "classification": "INVALID_RUN",
            "failure": {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(limit=8),
            },
            "interpretation_boundary": (
                "A failed solver/integrator/control is not evidence that the "
                "local intersection is absent."
            ),
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate frozen inputs and build both symbolic evaluators without running continuations",
    )
    arguments = parser.parse_args()
    try:
        if arguments.validate_only:
            audit = Audit()
            manifest, raw = load_unique_json(INPUT_PATH)
            observed, p42, _p49, p50 = validate_inputs(manifest, audit)
            phase50 = load_module("ice_phase50_for_phase51_validate", PHASE50_SOURCE_PATH)
            numerics = parse_numerics(manifest)
            thresholds = parse_thresholds(manifest)
            bounds = parse_bounds(manifest)
            contexts = [
                source_context(label, manifest, p42, p50, phase50, numerics, thresholds, bounds)
                for label in ("phi_plus", "phi_minus")
            ]
            diagnostics: dict[str, Any] = {}
            paired_lambdas = require(
                require(manifest, "evaluator", where="manifest"),
                "paired_lambdas",
                where="evaluator",
            )
            for context in contexts:
                nodes = [context.node(float(value)) for value in paired_lambdas]
                factor_residuals = [
                    float(
                        np.linalg.norm(node.factor @ node.factor.T - node.mobility)
                        / np.linalg.norm(node.mobility)
                    )
                    for node in nodes
                ]
                node0 = nodes[0]
                expected_launch = (
                    context.factor0 @ context.p42_launch_by_shape["lambda_1"]
                )
                launch_residual = float(
                    np.linalg.norm(node0.launch_w - expected_launch)
                    / np.linalg.norm(expected_launch)
                )
                evaluator_control = cse_validation(context, paired_lambdas)
                if (
                    max(factor_residuals) > thresholds.factor_identity_relative
                    or launch_residual
                    > thresholds.lambda0_launch_replay_relative
                    or not evaluator_control["dtype_contract_passed"]
                ):
                    raise InvalidRun(
                        f"{context.label} validate-only exact node/evaluator contract failed"
                    )
                diagnostics[context.label] = {
                    "factor_relative_residuals": factor_residuals,
                    "lambda0_launch_relative_residual": launch_residual,
                    "signed_frame_determinants": [
                        node.launch_record["signed_frame_determinant"]
                        for node in nodes
                    ],
                    "evaluator_pair_control": evaluator_control,
                }
            output = with_self_digest(
                {
                    "schema": RESULT_SCHEMA,
                    "phase": 51,
                    "run_status": "VALIDATION_ONLY",
                    "manifest_sha256": hashlib.sha256(raw).hexdigest(),
                    "pinned_inputs": observed,
                    "sources": [context.label for context in contexts],
                    "exact_checks": audit.exact,
                    "node_and_evaluator_diagnostics": diagnostics,
                }
            )
        else:
            output = run()
        print(RESULT_PREFIX + json.dumps(json_ready(output), sort_keys=True, allow_nan=False))
        return 0 if output["run_status"] in ("VALID_RUN", "VALIDATION_ONLY") else 1
    except InvalidRun as error:
        output = failure_payload(error)
        print(RESULT_PREFIX + json.dumps(json_ready(output), sort_keys=True, allow_nan=False))
        return 2
    except Exception as error:
        # Every declared scientific non-pass is caught in its pre-enumerated
        # slot.  Anything reaching this boundary is an implementation/run
        # failure, never evidence about the local candidate.
        output = failure_payload(error)
        print(RESULT_PREFIX + json.dumps(json_ready(output), sort_keys=True, allow_nan=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
