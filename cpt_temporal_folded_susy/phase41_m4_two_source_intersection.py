#!/usr/bin/env python3
"""Phase 41 -- m=4 two-source local joint-intersection production audit.

This executable consumes the separately committed Phase-41 input manifest.
It builds one four-segment midpoint action, solves the independently continued
signed ``delta_a`` and ``delta_phi`` saddle grids, fixes one zero-source
positive Hermitian flow metric, and tests one finite-radius, finite-time
seven-real-dimensional upward chart against the declared Gaussian-lift cap in
all fourteen real configuration coordinates.

The calculation is deliberately fail-closed.  A missing root, a failed
finite-difference plateau, or launch-surface sensitivity is emitted with the
typed failure status frozen in the manifest; no desired orientation sign or
rank is supplied.  Straight arms, cap reintersections, a global upward-cycle
census, Stokes data, relative good ends, the physical original cycle, and the
BFV/Pfaffian/Pin line remain absent.  Consequently every bounded-chain,
global, continuum, and quantum-gravity output remains null.  The script
writes no files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root


INPUT_PATH = Path(__file__).with_name(
    "PHASE41_M4_TWO_SOURCE_INTERSECTION_INPUTS.json"
)
INPUT_SHA256 = "dc17f4d25e758946fe00fec0bb209462294d4d982b1f86b59c099b8de064c92e"
INPUT_COMMIT = "58181447b558fa204406b732badd5c2fd541bb47"

SEGMENT_COUNT = 4
COMPLEX_DIMENSION = 7
AMBIENT_REAL_DIMENSION = 14
BASE_A = 3.5668031935672753
BASE_PHI = 1.0185809464006637
TIME_SCALE = 0.7
COORDINATE_SCALES = np.array(
    [
        BASE_A,
        BASE_PHI,
        BASE_A,
        BASE_PHI,
        BASE_A,
        BASE_PHI,
        TIME_SCALE,
    ],
    dtype=float,
)
REFLECTION = np.array(
    [
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ],
    dtype=float,
)
SOURCE_GRID = (-0.001, -0.0005, 0.0, 0.0005, 0.001)
SOURCE_HALF = 0.0005
SOURCE_FULL = 0.001
CAP_RADIUS = 0.3
PRIMARY_SPHERE_RADIUS = 1.0e-4
CONTROL_SPHERE_RADII = (5.0e-5, 2.0e-4)
FIELD_WINDOW = 0.25
CHART_WINDOW = 0.6
FLOW_TIME_MIN = 0.1
FLOW_TIME_MAX = 13.5
FLOW_NORM_MAX = 40.0


class ExactContractError(RuntimeError):
    """An exact frozen-input or symbolic invariant failed."""


class NumericalRunError(RuntimeError):
    """A numerical result cannot be serialized or classified validly."""


@dataclass
class Audit:
    exact_records: list[dict[str, object]] = field(default_factory=list)
    numerical_records: list[dict[str, object]] = field(default_factory=list)

    def _unique(self, check_id: str) -> None:
        ids = {
            str(record["id"])
            for record in self.exact_records + self.numerical_records
        }
        if check_id in ids:
            raise ExactContractError(f"duplicate contract id: {check_id}")

    def exact(
        self,
        check_id: str,
        condition: bool,
        statement: str,
        *,
        details: dict[str, object] | None = None,
    ) -> None:
        self._unique(check_id)
        record: dict[str, object] = {
            "id": check_id,
            "kind": "exact",
            "status": "PASS" if condition else "INVALID_RUN",
            "passed": bool(condition),
            "failure_status": "INVALID_RUN",
            "statement": statement,
        }
        if details is not None:
            record["details"] = details
        self.exact_records.append(record)
        if not condition:
            raise ExactContractError(f"[FAIL] {check_id}: {statement}")
        print(f"[PASS] {check_id}: {statement}", flush=True)

    def numerical(
        self,
        check_id: str,
        condition: bool,
        statement: str,
        *,
        failure_status: str,
        details: dict[str, object] | None = None,
    ) -> None:
        self._unique(check_id)
        status = "PASS" if condition else failure_status
        record: dict[str, object] = {
            "id": check_id,
            "kind": "numerical",
            "status": status,
            "passed": bool(condition),
            "failure_status": failure_status,
            "statement": statement,
        }
        if details is not None:
            record["details"] = details
        self.numerical_records.append(record)
        prefix = "NUMERIC PASS" if condition else "NUMERIC FAIL-CLOSED"
        print(f"[{prefix}] {check_id} [{status}]: {statement}", flush=True)

    @property
    def exact_passed(self) -> int:
        return sum(bool(record["passed"]) for record in self.exact_records)

    @property
    def numerical_passed(self) -> int:
        return sum(bool(record["passed"]) for record in self.numerical_records)


@dataclass(frozen=True)
class SymbolicFamily:
    variables_z: tuple[sp.Symbol, ...]
    variables_w: tuple[sp.Symbol, ...]
    boundary_a: sp.Symbol
    boundary_phi: sp.Symbol
    delta_a: sp.Symbol
    delta_phi: sp.Symbol
    action_z: sp.Expr
    action_w: sp.Expr
    gradient_w: sp.Matrix
    hessian_w: sp.Matrix
    elements: tuple[sp.Expr, ...]


@dataclass(frozen=True)
class NumericModel:
    delta_a: float
    delta_phi: float
    action_expr: sp.Expr
    gradient_expr: sp.Matrix
    hessian_expr: sp.Matrix
    action_function: Callable[..., object]
    gradient_function: Callable[..., object]
    hessian_function: Callable[..., object]


@dataclass(frozen=True)
class FixedMetric:
    saddle_zero_w: np.ndarray
    hessian_zero_w: np.ndarray
    eigenvalues_zero: np.ndarray
    oriented_eigenvectors_zero: np.ndarray
    linear_map: np.ndarray
    inverse_metric_mobility_w: np.ndarray
    metric_tensor_w: np.ndarray
    xi_reflection: np.ndarray


@dataclass(frozen=True)
class SaddleData:
    delta_a: float
    delta_phi: float
    saddle_w: np.ndarray
    saddle_z: np.ndarray
    action: complex
    gradient_max_abs: float
    hessian_w: np.ndarray
    hessian_eigenvalues: np.ndarray
    hessian_inertia: tuple[int, int, int]
    hessian_xi: np.ndarray
    hessian_xi_eigenvalues: np.ndarray
    aligned_signed_frame_xi: np.ndarray
    signed_restrictions: dict[int, np.ndarray]
    signed_projectors: dict[int, np.ndarray]
    signed_subspace_min_principal_overlap: float

    def launch_matrix(self, shape_lambda: float) -> np.ndarray:
        if shape_lambda not in (0.0, 0.5, 1.0):
            raise ValueError("shape lambda must be one of 0, 1/2, 1")
        result = np.zeros(
            (COMPLEX_DIMENSION, COMPLEX_DIMENSION),
            dtype=np.complex128,
        )
        base_signs = np.sign(self.hessian_xi_eigenvalues).astype(int)
        for sign in (-1, 1):
            indices = np.flatnonzero(base_signs == sign)
            frame = self.aligned_signed_frame_xi[:, indices]
            restriction = self.signed_restrictions[sign]
            values, vectors = np.linalg.eigh(restriction)
            if np.min(values) <= 0.0:
                raise RuntimeError("signed Hessian restriction is not positive")
            shape = (
                vectors
                @ np.diag(values ** (-0.5 * shape_lambda))
                @ vectors.T
            )
            phase = -1.0 + 0.0j if sign < 0 else 0.0 + 1.0j
            result[:, indices] = phase * frame @ shape
        return result


@dataclass(frozen=True)
class Chart:
    center: np.ndarray
    tangent: np.ndarray
    orientation_determinant: float
    provenance: dict[str, object]

    def direction(self, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        values = np.asarray(parameters, dtype=float).reshape(6)
        vector = self.center + self.tangent @ values
        norm = float(np.linalg.norm(vector))
        if norm == 0.0:
            raise RuntimeError("chart vector vanished")
        omega = vector / norm
        derivative = (
            (np.eye(COMPLEX_DIMENSION) - np.outer(omega, omega))
            @ self.tangent
            / norm
        )
        return omega, derivative


def load_manifest() -> tuple[dict[str, object], bytes, str]:
    raw = INPUT_PATH.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    return json.loads(raw), raw, digest


def midpoint_element(
    left_a: sp.Expr,
    left_phi: sp.Expr,
    right_a: sp.Expr,
    right_phi: sp.Expr,
    proper_time: sp.Expr,
    step: sp.Expr,
) -> sp.Expr:
    midpoint_a = (left_a + right_a) / 2
    midpoint_phi = (left_phi + right_phi) / 2
    difference_a = right_a - left_a
    difference_phi = right_phi - left_phi
    slope = sp.sqrt(sp.Rational(2, 3))
    potential = sp.Rational(3, 4) * (
        1 - sp.exp(-slope * midpoint_phi)
    ) ** 2
    return 2 * sp.pi**2 * (
        (
            -6 * midpoint_a * difference_a**2
            + midpoint_a**3 * difference_phi**2
        )
        / (2 * proper_time * step)
        + proper_time
        * step
        * (-3 * midpoint_a + midpoint_a**3 * potential)
    )


@lru_cache(maxsize=1)
def build_symbolic_family() -> SymbolicFamily:
    variables_z = sp.symbols("a_1 phi_1 a_2 phi_2 a_3 phi_3 T")
    variables_w = sp.symbols(
        "w_a1 w_phi1 w_a2 w_phi2 w_a3 w_phi3 w_T"
    )
    boundary_a, boundary_phi = sp.symbols(
        "a_boundary phi_boundary", real=True
    )
    delta_a, delta_phi = sp.symbols("delta_a delta_phi", real=True)
    proper_time = variables_z[-1]
    left = (
        boundary_a * (1 - delta_a / 2),
        boundary_phi - delta_phi / 2,
    )
    right = (
        boundary_a * (1 + delta_a / 2),
        boundary_phi + delta_phi / 2,
    )
    nodes = (
        left,
        (variables_z[0], variables_z[1]),
        (variables_z[2], variables_z[3]),
        (variables_z[4], variables_z[5]),
        right,
    )
    step = sp.Rational(1, SEGMENT_COUNT)
    elements = tuple(
        midpoint_element(
            nodes[index][0],
            nodes[index][1],
            nodes[index + 1][0],
            nodes[index + 1][1],
            proper_time,
            step,
        )
        for index in range(SEGMENT_COUNT)
    )
    action_z = sp.expand(sum(elements))
    substitutions: dict[sp.Symbol, sp.Expr] = {
        boundary_a: sp.Float(str(BASE_A), 50),
        boundary_phi: sp.Float(str(BASE_PHI), 50),
    }
    for index, variable in enumerate(variables_z):
        substitutions[variable] = (
            sp.Float(str(COORDINATE_SCALES[index]), 50)
            * variables_w[index]
        )
    action_w = action_z.subs(substitutions)
    gradient_w = sp.Matrix(
        [sp.diff(action_w, variable) for variable in variables_w]
    )
    hessian_w = sp.hessian(action_w, variables_w)
    return SymbolicFamily(
        variables_z=variables_z,
        variables_w=variables_w,
        boundary_a=boundary_a,
        boundary_phi=boundary_phi,
        delta_a=delta_a,
        delta_phi=delta_phi,
        action_z=action_z,
        action_w=action_w,
        gradient_w=gradient_w,
        hessian_w=hessian_w,
        elements=elements,
    )


@lru_cache(maxsize=None)
def numeric_model(delta_a_value: float, delta_phi_value: float) -> NumericModel:
    family = build_symbolic_family()
    substitutions = {
        family.delta_a: sp.Float(str(delta_a_value), 50),
        family.delta_phi: sp.Float(str(delta_phi_value), 50),
    }
    action = family.action_w.subs(substitutions)
    gradient = family.gradient_w.subs(substitutions)
    hessian = family.hessian_w.subs(substitutions)
    return NumericModel(
        delta_a=float(delta_a_value),
        delta_phi=float(delta_phi_value),
        action_expr=action,
        gradient_expr=gradient,
        hessian_expr=hessian,
        action_function=sp.lambdify((family.variables_w,), action, "numpy"),
        gradient_function=sp.lambdify(
            (family.variables_w,), gradient, "numpy"
        ),
        hessian_function=sp.lambdify(
            (family.variables_w,), hessian, "numpy"
        ),
    )


def action_at(model: NumericModel, w: np.ndarray) -> complex:
    return complex(model.action_function(tuple(w)))


def gradient_at(model: NumericModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.gradient_function(tuple(w)), dtype=np.complex128
    ).reshape(COMPLEX_DIMENSION)


def hessian_at(model: NumericModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.hessian_function(tuple(w)), dtype=np.complex128
    ).reshape(COMPLEX_DIMENSION, COMPLEX_DIMENSION)


def deterministic_oriented_eigenframe(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    for column in range(eigenvectors.shape[1]):
        pivot = int(np.argmax(np.abs(eigenvectors[:, column])))
        if eigenvectors[pivot, column] < 0.0:
            eigenvectors[:, column] *= -1.0
    if np.linalg.det(eigenvectors) < 0.0:
        eigenvectors[:, -1] *= -1.0
    return eigenvalues, eigenvectors


def solve_real_saddle(
    model: NumericModel,
    seed_w: np.ndarray,
    *,
    root_tolerance: float = 1.0e-12,
) -> tuple[np.ndarray, dict[str, object]]:
    solution = root(
        lambda value: gradient_at(model, value).real,
        seed_w,
        jac=lambda value: hessian_at(model, value).real,
        method="hybr",
        options={"xtol": root_tolerance},
    )
    candidate = np.asarray(solution.x, dtype=float)
    residual = gradient_at(model, candidate)
    if (not solution.success) and np.max(np.abs(residual)) > 1.0e-8:
        raise RuntimeError(
            "saddle solve failed at "
            f"({model.delta_a:+.4g},{model.delta_phi:+.4g}): "
            f"{solution.message}"
        )
    hessian = hessian_at(model, candidate).real
    eigenvalues = np.linalg.eigvalsh(hessian)
    action = action_at(model, candidate)
    return candidate, {
        "delta_a": model.delta_a,
        "delta_phi": model.delta_phi,
        "solver_success": bool(solution.success),
        "solver_message": str(solution.message),
        "root_tolerance": root_tolerance,
        "saddle_w": candidate.tolist(),
        "saddle_z": (COORDINATE_SCALES * candidate).tolist(),
        "action": [float(action.real), float(action.imag)],
        "gradient_max_abs": float(np.max(np.abs(residual))),
        "hessian_eigenvalues": eigenvalues.tolist(),
        "hessian_min_abs_eigenvalue": float(np.min(np.abs(eigenvalues))),
        "hessian_inertia": {
            "negative": int(np.count_nonzero(eigenvalues < 0.0)),
            "positive": int(np.count_nonzero(eigenvalues > 0.0)),
            "zero": int(np.count_nonzero(np.abs(eigenvalues) <= 1.0e-9)),
        },
    }


def build_fixed_metric(saddle_zero_w: np.ndarray) -> FixedMetric:
    hessian = hessian_at(numeric_model(0.0, 0.0), saddle_zero_w).real
    eigenvalues, eigenvectors = deterministic_oriented_eigenframe(hessian)
    linear_map = eigenvectors @ np.diag(1.0 / np.sqrt(np.abs(eigenvalues)))
    mobility = linear_map @ linear_map.T
    xi_reflection = np.linalg.solve(linear_map, REFLECTION @ linear_map)
    return FixedMetric(
        saddle_zero_w=saddle_zero_w,
        hessian_zero_w=hessian,
        eigenvalues_zero=eigenvalues,
        oriented_eigenvectors_zero=eigenvectors,
        linear_map=linear_map,
        inverse_metric_mobility_w=mobility,
        metric_tensor_w=np.linalg.inv(mobility),
        xi_reflection=xi_reflection,
    )


def aligned_signed_data(
    hessian_xi: np.ndarray,
    base_signs: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    dict[int, np.ndarray],
    dict[int, np.ndarray],
    float,
]:
    raw_values, raw_vectors = np.linalg.eigh(hessian_xi)
    aligned_frame = np.zeros_like(raw_vectors)
    restrictions: dict[int, np.ndarray] = {}
    projectors: dict[int, np.ndarray] = {}
    principal_overlaps: list[float] = []
    for sign in (-1, 1):
        targets = np.flatnonzero(base_signs == sign)
        sources = np.flatnonzero(np.sign(raw_values) == sign)
        if targets.size != sources.size:
            raise RuntimeError("Hessian inertia changed on a signed source arm")
        spectral_frame = raw_vectors[:, sources]
        reference_frame = np.eye(COMPLEX_DIMENSION)[:, targets]
        left, singular_values, right_transpose = np.linalg.svd(
            spectral_frame.T @ reference_frame
        )
        aligned = spectral_frame @ (left @ right_transpose)
        aligned_frame[:, targets] = aligned
        principal_overlaps.extend(singular_values.tolist())
        restriction = sign * (aligned.T @ hessian_xi @ aligned)
        restrictions[sign] = restriction
        projectors[sign] = aligned @ aligned.T
    if np.linalg.det(aligned_frame) < 0.0:
        # A single column flip changes the full orientation.  The signed
        # restriction is recomputed in that gauge; its positivity and the
        # invariant projector are unchanged.
        first_block = np.flatnonzero(base_signs < 0)
        if first_block.size < 1:
            raise RuntimeError("cannot repair aligned-frame orientation")
        aligned_frame[:, first_block[0]] *= -1.0
        block = aligned_frame[:, first_block]
        restrictions[-1] = -(block.T @ hessian_xi @ block)
    if np.linalg.det(aligned_frame) <= 0.0:
        raise RuntimeError("aligned signed-subspace frame lost orientation")
    return (
        raw_values,
        aligned_frame,
        restrictions,
        projectors,
        min(principal_overlaps),
    )


def make_saddle_data(
    model: NumericModel,
    saddle_w: np.ndarray,
    fixed: FixedMetric,
) -> SaddleData:
    hessian_w = hessian_at(model, saddle_w).real
    hessian_values = np.linalg.eigvalsh(hessian_w)
    hessian_xi = fixed.linear_map.T @ hessian_w @ fixed.linear_map
    base_signs = np.sign(fixed.eigenvalues_zero).astype(int)
    if model.delta_a == 0.0 and model.delta_phi == 0.0:
        xi_values = base_signs.astype(float)
        aligned_frame = np.eye(COMPLEX_DIMENSION)
        restrictions = {
            sign: np.eye(np.count_nonzero(base_signs == sign))
            for sign in (-1, 1)
        }
        projectors = {
            sign: np.diag((base_signs == sign).astype(float))
            for sign in (-1, 1)
        }
        overlap = 1.0
    else:
        (
            xi_values,
            aligned_frame,
            restrictions,
            projectors,
            overlap,
        ) = aligned_signed_data(hessian_xi, base_signs)
    action = action_at(model, saddle_w)
    return SaddleData(
        delta_a=model.delta_a,
        delta_phi=model.delta_phi,
        saddle_w=saddle_w,
        saddle_z=COORDINATE_SCALES * saddle_w,
        action=action,
        gradient_max_abs=float(
            np.max(np.abs(gradient_at(model, saddle_w)))
        ),
        hessian_w=hessian_w,
        hessian_eigenvalues=hessian_values,
        hessian_inertia=(
            int(np.count_nonzero(hessian_values < 0.0)),
            int(np.count_nonzero(hessian_values > 0.0)),
            int(np.count_nonzero(np.abs(hessian_values) <= 1.0e-9)),
        ),
        hessian_xi=hessian_xi,
        hessian_xi_eigenvalues=xi_values,
        aligned_signed_frame_xi=aligned_frame,
        signed_restrictions=restrictions,
        signed_projectors=projectors,
        signed_subspace_min_principal_overlap=overlap,
    )


def source_point(source: str, value: float) -> tuple[float, float]:
    if source == "a_only":
        return float(value), 0.0
    if source == "phi_only":
        return 0.0, float(value)
    raise ValueError(f"unknown source axis: {source}")


def point_label(point: tuple[float, float]) -> str:
    return f"da={point[0]:+.4g},dp={point[1]:+.4g}"


def solve_signed_saddle_grids(
    manifest: dict[str, object],
    *,
    root_tolerance: float,
    zero_seed_override: np.ndarray | None = None,
) -> tuple[
    dict[tuple[float, float], np.ndarray],
    dict[tuple[float, float], dict[str, object]],
]:
    disclosed = np.asarray(
        manifest["known_before_freeze"]["symmetric_m4_saddle_z_approximate"],
        dtype=float,
    )
    zero_seed = disclosed / COORDINATE_SCALES
    if zero_seed_override is not None:
        zero_seed = np.asarray(zero_seed_override, dtype=float)
    zero, zero_record = solve_real_saddle(
        numeric_model(0.0, 0.0),
        zero_seed,
        root_tolerance=root_tolerance,
    )
    saddles: dict[tuple[float, float], np.ndarray] = {(0.0, 0.0): zero}
    records: dict[tuple[float, float], dict[str, object]] = {
        (0.0, 0.0): zero_record
    }
    for source in ("phi_only", "a_only"):
        for sign in (1.0, -1.0):
            running_seed = zero.copy()
            for magnitude in (SOURCE_HALF, SOURCE_FULL):
                point = source_point(source, sign * magnitude)
                running_seed, record = solve_real_saddle(
                    numeric_model(*point),
                    running_seed,
                    root_tolerance=root_tolerance,
                )
                saddles[point] = running_seed
                records[point] = record
    return saddles, records


def odd_output(
    saddle: SaddleData,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    odd = np.array(
        [
            (saddle.saddle_z[4] - saddle.saddle_z[0]) / np.sqrt(2.0),
            (saddle.saddle_z[5] - saddle.saddle_z[1]) / np.sqrt(2.0),
        ],
        dtype=float,
    )
    anchor = np.array(
        [
            BASE_A * saddle.delta_a / (2.0 * np.sqrt(2.0)),
            saddle.delta_phi / (2.0 * np.sqrt(2.0)),
        ],
        dtype=float,
    )
    normalized = (odd - anchor) / np.array([BASE_A, BASE_PHI])
    return odd, anchor, normalized


def susceptibility_from_saddles(
    saddles: dict[tuple[float, float], SaddleData]
) -> dict[str, object]:
    outputs = {point: odd_output(data)[2] for point, data in saddles.items()}
    matrices: dict[str, np.ndarray] = {}
    reversal_residuals: dict[str, float] = {}
    for name, magnitude in (("half", SOURCE_HALF), ("full", SOURCE_FULL)):
        columns: list[np.ndarray] = []
        source_residuals: list[float] = []
        for source in ("a_only", "phi_only"):
            plus = source_point(source, magnitude)
            minus = source_point(source, -magnitude)
            normalized_step = magnitude if source == "a_only" else magnitude / BASE_PHI
            columns.append((outputs[plus] - outputs[minus]) / (2.0 * normalized_step))
            source_residuals.append(
                float(np.max(np.abs(outputs[plus] + outputs[minus])))
            )
        matrices[name] = np.column_stack(columns)
        reversal_residuals[name] = max(source_residuals)
    return {
        "outputs": {point_label(key): value.tolist() for key, value in outputs.items()},
        "chi_half": matrices["half"],
        "chi_full": matrices["full"],
        "reversal_residuals": reversal_residuals,
    }


def interleaved(vector: np.ndarray) -> np.ndarray:
    values = np.asarray(vector, dtype=np.complex128).reshape(-1)
    result = np.empty(2 * values.size, dtype=float)
    result[0::2] = values.real
    result[1::2] = values.imag
    return result


def real_frame(complex_frame: np.ndarray) -> np.ndarray:
    frame = np.asarray(complex_frame, dtype=np.complex128)
    return np.column_stack(
        [interleaved(frame[:, index]) for index in range(frame.shape[1])]
    )


def normalize_columns(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(matrix, axis=0)
    if np.any(norms <= 0.0):
        raise RuntimeError("zero tangent column")
    return matrix / norms, norms


def matrix_orientation(matrix: np.ndarray) -> dict[str, object]:
    normalized, norms = normalize_columns(matrix)
    sign, log_abs = np.linalg.slogdet(normalized)
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    finite_log_abs: float | None = (
        float(log_abs) if np.isfinite(log_abs) else None
    )
    finite_condition: float | None = (
        float(singular_values[0] / singular_values[-1])
        if singular_values[-1] > 0.0
        else None
    )
    return {
        "sign": int(np.sign(sign)),
        "log_abs_normalized_determinant": finite_log_abs,
        "normalized_singular_values": singular_values.tolist(),
        "normalized_sigma_min": float(singular_values[-1]),
        "normalized_condition_number": finite_condition,
        "column_norms": norms.tolist(),
    }


def field_mode_column(values: Iterable[sp.Expr], field: int) -> sp.Matrix:
    result = sp.zeros(COMPLEX_DIMENSION, 1)
    for node, value in enumerate(values):
        result[2 * node + field] = value
    return result


def exact_contracts(
    audit: Audit,
    manifest: dict[str, object],
    digest: str,
) -> dict[str, object]:
    family = build_symbolic_family()
    declared_exact = [
        record["id"] for record in manifest["completion_contracts"]["exact"]
    ]
    required_ids = [
        "P41.action.single_scalar_four_elements",
        "P41.action.holomorphic_off_T_zero",
        "P41.reflection.two_source_covariance",
        "P41.modes.DST_and_nested_orientation",
        "P41.nesting.affine_cycle_not_action",
        "P41.orientation.middle_dimension_and_root_parity",
        "P41.guard.incomplete_data_force_global_nulls",
    ]
    input_contract = (
        digest == INPUT_SHA256
        and declared_exact == required_ids
        and manifest["phase"] == 41
        and manifest["freeze_kind"]
        == "post_feasibility_workflow_input_freeze"
        and manifest["is_preregistration"] is False
        and manifest["is_scientific_evidence"] is False
        and manifest["prohibited_result_inputs"]["desired_direct_orientation_sign"]
        is None
    )
    audit.exact(
        required_ids[0],
        input_contract
        and len(family.elements) == 4
        and len(family.variables_z) == COMPLEX_DIMENSION
        and family.action_z == sp.expand(sum(family.elements))
        and family.gradient_w
        == sp.Matrix(
            [
                sp.diff(family.action_w, variable)
                for variable in family.variables_w
            ]
        )
        and family.hessian_w
        == sp.hessian(family.action_w, family.variables_w),
        "the byte-pinned post-feasibility manifest drives one S4 scalar, four midpoint elements, and the production seven-gradient/seven-Hessian",
        details={"manifest_sha256": digest, "manifest_commit": INPUT_COMMIT},
    )

    proper_time = family.variables_z[-1]
    residue = sp.cancel(
        sp.limit(proper_time * family.action_z, proper_time, 0)
    )
    audit.exact(
        required_ids[1],
        not family.action_z.has(sp.conjugate)
        and residue != 0
        and residue.equals(0) is False,
        "S4 has no conjugation off T=0 and its simple-pole residue is a nonzero symbolic polynomial",
        details={"residue_operation_count": int(sp.count_ops(residue))},
    )

    reflection_z = {
        family.variables_z[0]: family.variables_z[4],
        family.variables_z[1]: family.variables_z[5],
        family.variables_z[4]: family.variables_z[0],
        family.variables_z[5]: family.variables_z[1],
        family.delta_a: -family.delta_a,
        family.delta_phi: -family.delta_phi,
    }
    reflection_w = {
        family.variables_w[0]: family.variables_w[4],
        family.variables_w[1]: family.variables_w[5],
        family.variables_w[4]: family.variables_w[0],
        family.variables_w[5]: family.variables_w[1],
        family.delta_a: -family.delta_a,
        family.delta_phi: -family.delta_phi,
    }
    reflection_symbolic = sp.Matrix(REFLECTION.astype(int))
    action_covariance = (
        sp.simplify(family.action_z.xreplace(reflection_z) - family.action_z)
        == 0
    )
    gradient_z = sp.Matrix(
        [sp.diff(family.action_z, variable) for variable in family.variables_z]
    )
    hessian_z = sp.hessian(family.action_z, family.variables_z)
    gradient_covariance = all(
        sp.simplify(value) == 0
        for value in gradient_z.xreplace(reflection_z)
        - reflection_symbolic * gradient_z
    )
    hessian_covariance = all(
        sp.simplify(value) == 0
        for value in hessian_z.xreplace(reflection_z)
        - reflection_symbolic * hessian_z * reflection_symbolic
    )
    audit.exact(
        required_ids[2],
        action_covariance and gradient_covariance and hessian_covariance,
        "S4, its full gradient, and its Hessian obey joint two-source reflection covariance",
    )

    sqrt_two = sp.sqrt(2)
    time_column = sp.zeros(COMPLEX_DIMENSION, 1)
    time_column[-1] = 1
    dst_vectors = (
        (sp.Rational(1, 2), 1 / sqrt_two, sp.Rational(1, 2)),
        (1 / sqrt_two, 0, -1 / sqrt_two),
        (sp.Rational(1, 2), -1 / sqrt_two, sp.Rational(1, 2)),
    )
    nested_vectors = (
        (1 / sp.sqrt(6), 2 / sp.sqrt(6), 1 / sp.sqrt(6)),
        (1 / sqrt_two, 0, -1 / sqrt_two),
        (1 / sp.sqrt(3), -1 / sp.sqrt(3), 1 / sp.sqrt(3)),
    )
    dst = sp.Matrix.hstack(
        field_mode_column(dst_vectors[0], 0),
        field_mode_column(dst_vectors[0], 1),
        time_column,
        field_mode_column(dst_vectors[1], 0),
        field_mode_column(dst_vectors[1], 1),
        field_mode_column(dst_vectors[2], 0),
        field_mode_column(dst_vectors[2], 1),
    )
    nested = sp.Matrix.hstack(
        field_mode_column(nested_vectors[0], 0),
        field_mode_column(nested_vectors[0], 1),
        time_column,
        field_mode_column(nested_vectors[1], 0),
        field_mode_column(nested_vectors[1], 1),
        field_mode_column(nested_vectors[2], 0),
        field_mode_column(nested_vectors[2], 1),
    )
    parity = sp.diag(1, 1, 1, -1, -1, 1, 1)
    transition = sp.simplify(dst.inv() * nested)
    audit.exact(
        required_ids[3],
        sp.simplify(dst.det()) == 1
        and sp.simplify(nested.det()) == 1
        and sp.simplify(dst.T * reflection_symbolic * dst - parity)
        == sp.zeros(COMPLEX_DIMENSION)
        and sp.simplify(nested.T * reflection_symbolic * nested - parity)
        == sp.zeros(COMPLEX_DIMENSION)
        and sp.simplify(transition.det()) == 1,
        "the frozen DST and nested bases are positively oriented, have parity +++--++, and have positive transition determinant",
    )

    coarse_a, coarse_phi = sp.symbols("a_coarse phi_coarse")
    left = (
        family.boundary_a * (1 - family.delta_a / 2),
        family.boundary_phi - family.delta_phi / 2,
    )
    right = (
        family.boundary_a * (1 + family.delta_a / 2),
        family.boundary_phi + family.delta_phi / 2,
    )
    interior = (
        ((left[0] + coarse_a) / 2, (left[1] + coarse_phi) / 2),
        (coarse_a, coarse_phi),
        ((coarse_a + right[0]) / 2, (coarse_phi + right[1]) / 2),
    )
    prolong_substitution = {
        family.variables_z[0]: interior[0][0],
        family.variables_z[1]: interior[0][1],
        family.variables_z[2]: interior[1][0],
        family.variables_z[3]: interior[1][1],
        family.variables_z[4]: interior[2][0],
        family.variables_z[5]: interior[2][1],
    }
    action_four_on_prolongation = family.action_z.subs(
        prolong_substitution, simultaneous=True
    )
    action_two = midpoint_element(
        left[0],
        left[1],
        coarse_a,
        coarse_phi,
        proper_time,
        sp.Rational(1, 2),
    ) + midpoint_element(
        coarse_a,
        coarse_phi,
        right[0],
        right[1],
        proper_time,
        sp.Rational(1, 2),
    )
    nonnesting_witness = sp.simplify(
        (action_four_on_prolongation - action_two).subs(
            {
                family.boundary_a: 3,
                family.boundary_phi: 1,
                family.delta_a: 0,
                family.delta_phi: 0,
                coarse_a: 4,
                coarse_phi: 1,
                proper_time: 1,
            }
        )
    )
    anchor_quarters = sp.Matrix(
        [
            (3 * left[0] + right[0]) / 4,
            (3 * left[1] + right[1]) / 4,
            (left[0] + right[0]) / 2,
            (left[1] + right[1]) / 2,
            (left[0] + 3 * right[0]) / 4,
            (left[1] + 3 * right[1]) / 4,
        ]
    )
    midpoint_anchor = sp.Matrix(
        [(left[0] + right[0]) / 2, (left[1] + right[1]) / 2]
    )
    prolonged_anchor = sp.Matrix(
        [
            (left[0] + midpoint_anchor[0]) / 2,
            (left[1] + midpoint_anchor[1]) / 2,
            midpoint_anchor[0],
            midpoint_anchor[1],
            (midpoint_anchor[0] + right[0]) / 2,
            (midpoint_anchor[1] + right[1]) / 2,
        ]
    )
    cap_embedding = sp.Matrix(
        [
            [sp.Rational(1, 2), 0],
            [0, sp.Rational(1, 2)],
            [1, 0],
            [0, 1],
            [sp.Rational(1, 2), 0],
            [0, sp.Rational(1, 2)],
        ]
    )
    center_restriction = sp.Matrix(
        [[0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0]]
    )
    audit.exact(
        required_ids[4],
        center_restriction * cap_embedding == sp.eye(2)
        and sp.simplify(anchor_quarters - prolonged_anchor) == sp.zeros(6, 1)
        and nonnesting_witness != 0
        and nonnesting_witness.equals(0) is False,
        "the affine retraction, anchors, and cap deviations nest exactly while an exact rational witness proves S4 composed with I is not S2",
        details={"action_nonnesting_witness": str(nonnesting_witness)},
    )

    audit.exact(
        required_ids[5],
        COMPLEX_DIMENSION == 2 * (SEGMENT_COUNT - 1) + 1
        and AMBIENT_REAL_DIMENSION == 2 * COMPLEX_DIMENSION
        and (-1) ** COMPLEX_DIMENSION == -1,
        "Gamma and K each have real dimension seven in R14 and seven negated K columns reverse the root determinant",
    )

    required_nulls = manifest["required_fail_closed_outputs"]
    false_keys = [
        key
        for key, value in required_nulls.items()
        if isinstance(value, bool) and key != "gate1_status"
    ]
    null_keys = [
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "quantum_gravity_explanation",
    ]
    audit.exact(
        required_ids[6],
        all(required_nulls[key] is False for key in false_keys)
        and all(required_nulls[key] is None for key in null_keys)
        and required_nulls["gate1_status"] == "OPEN_PARTIAL_PROGRESS",
        "incomplete chain, census, Stokes, nonlinear-manifold, end, and physical-cycle data force all bounded/global outputs to null",
        details={"false_keys": false_keys, "null_keys": null_keys},
    )
    return {
        "DST_basis": dst,
        "nested_basis": nested,
        "basis_transition": transition,
        "action_nonnesting_witness": nonnesting_witness,
    }


def deterministic_oriented_null_frame(center: np.ndarray) -> tuple[np.ndarray, float]:
    unit = np.asarray(center, dtype=float).reshape(COMPLEX_DIMENSION)
    unit = unit / np.linalg.norm(unit)
    columns: list[np.ndarray] = []
    for index in range(COMPLEX_DIMENSION):
        candidate = np.eye(COMPLEX_DIMENSION)[:, index].copy()
        candidate -= unit * float(unit @ candidate)
        for known in columns:
            candidate -= known * float(known @ candidate)
        norm = float(np.linalg.norm(candidate))
        if norm > 1.0e-12:
            columns.append(candidate / norm)
        if len(columns) == COMPLEX_DIMENSION - 1:
            break
    if len(columns) != COMPLEX_DIMENSION - 1:
        raise RuntimeError("failed to construct deterministic S6 tangent frame")
    tangent = np.column_stack(columns)
    determinant = float(np.linalg.det(np.column_stack([tangent, unit])))
    if determinant < 0.0:
        tangent[:, 0] *= -1.0
        determinant *= -1.0
    if determinant <= 0.0:
        raise RuntimeError("S6 chart frame is not positively oriented")
    return tangent, determinant


def build_nested_chart(
    manifest: dict[str, object],
    zero_saddle: SaddleData,
    fixed: FixedMetric,
) -> Chart:
    direction_input = manifest["upward_chart"]["phase39_direction_source"]
    repository_root = Path(__file__).resolve().parents[1]
    artifact_path = repository_root / str(direction_input["artifact"])
    script_path = repository_root / str(direction_input["script"])
    artifact_digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    script_digest = hashlib.sha256(script_path.read_bytes()).hexdigest()
    if artifact_digest != direction_input["artifact_sha256"]:
        raise ExactContractError("Phase39 direction artifact hash drifted")
    if script_digest != direction_input["script_sha256"]:
        raise ExactContractError("Phase39 direction script hash drifted")

    phase39_spec = importlib.util.spec_from_file_location(
        "ice_phase39_finite_joint_intersection", script_path
    )
    if phase39_spec is None or phase39_spec.loader is None:
        raise ExactContractError("cannot load the byte-pinned Phase39 script")
    phase39 = importlib.util.module_from_spec(phase39_spec)
    sys.modules[phase39_spec.name] = phase39
    phase39_spec.loader.exec_module(phase39)

    frozen39 = phase39.load_frozen_input()
    model39 = phase39.build_symbolic_model()
    morse39, _record39 = phase39.solve_main_saddle(frozen39, model39)
    omega39 = phase39.omega_equatorial(
        float(direction_input["alpha"]), float(direction_input["beta"])
    )[0]
    xi_direction39 = morse39.upward_frame_xi @ omega39
    physical_direction39 = (
        np.diag(frozen39.coordinate_scales)
        @ morse39.whitening
        @ xi_direction39
    )
    prolonged_physical = np.array(
        [
            physical_direction39[0] / 2.0,
            physical_direction39[1] / 2.0,
            physical_direction39[0],
            physical_direction39[1],
            physical_direction39[0] / 2.0,
            physical_direction39[1] / 2.0,
            physical_direction39[2],
        ],
        dtype=np.complex128,
    )
    direction_w = prolonged_physical / COORDINATE_SCALES
    direction_xi = np.linalg.solve(fixed.linear_map, direction_w)
    direction_real = interleaved(direction_xi)
    launch_zero = zero_saddle.launch_matrix(1.0)
    launch_real = real_frame(launch_zero)
    projector = launch_real @ np.linalg.solve(
        launch_real.T @ launch_real, launch_real.T
    )
    projected = projector @ direction_real
    overlap_ratio = float(
        np.linalg.norm(projected) / np.linalg.norm(direction_real)
    )
    if overlap_ratio < 0.05:
        raise RuntimeError(
            "nested Phase39 direction has insufficient m4 upward overlap"
        )
    coefficients = np.linalg.lstsq(launch_real, projected, rcond=None)[0]
    coefficients /= np.linalg.norm(coefficients)
    overlap = float(interleaved(launch_zero @ coefficients) @ direction_real)
    if overlap < 0.0:
        coefficients *= -1.0
        overlap *= -1.0
    tangent, determinant = deterministic_oriented_null_frame(coefficients)
    return Chart(
        center=coefficients,
        tangent=tangent,
        orientation_determinant=determinant,
        provenance={
            "phase39_artifact_sha256": artifact_digest,
            "phase39_script_sha256": script_digest,
            "phase39_alpha": float(direction_input["alpha"]),
            "phase39_beta": float(direction_input["beta"]),
            "projection_overlap_ratio": overlap_ratio,
            "positive_physical_overlap": overlap,
            "center": coefficients.tolist(),
            "det_B_center": determinant,
        },
    )


def xi_to_w(
    saddle: SaddleData, fixed: FixedMetric, xi: np.ndarray
) -> np.ndarray:
    return saddle.saddle_w + fixed.linear_map @ xi


def flow_xi(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    xi: np.ndarray,
) -> np.ndarray:
    return -np.conjugate(
        fixed.linear_map.T
        @ gradient_at(model, xi_to_w(saddle, fixed, xi))
    )


def hessian_xi(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    xi: np.ndarray,
) -> np.ndarray:
    return (
        fixed.linear_map.T
        @ hessian_at(model, xi_to_w(saddle, fixed, xi))
        @ fixed.linear_map
    )


def integrate_chart(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    chart_parameters: np.ndarray,
    flow_time: float,
    sphere_radius: float,
    shape_lambda: float,
    *,
    with_tangent: bool,
    method: str,
) -> tuple[np.ndarray, np.ndarray | None, dict[str, object]]:
    if not FLOW_TIME_MIN <= flow_time <= FLOW_TIME_MAX:
        raise RuntimeError("flow time left the frozen interval")
    omega, derivative = chart.direction(chart_parameters)
    launch = saddle.launch_matrix(shape_lambda)
    initial_xi = sphere_radius * (launch @ omega)
    strict = method == "DOP853"
    if not with_tangent:
        solution = solve_ivp(
            lambda _time, xi: flow_xi(model, saddle, fixed, xi),
            (0.0, flow_time),
            initial_xi,
            method=method,
            rtol=2.0e-10 if strict else 2.0e-7,
            atol=2.0e-12 if strict else 2.0e-9,
            max_step=0.04 if strict else 0.06,
        )
        if not solution.success:
            raise RuntimeError(str(solution.message))
        xi_norm_max = float(np.max(np.linalg.norm(solution.y, axis=0)))
        if xi_norm_max >= FLOW_NORM_MAX:
            raise RuntimeError("trajectory exceeded the frozen xi-norm cap")
        final_xi = solution.y[:, -1]
        state_z = COORDINATE_SCALES * xi_to_w(saddle, fixed, final_xi)
        return state_z, None, {
            "solver_method": method,
            "solver_steps": int(solution.t.size),
            "xi_norm_max": xi_norm_max,
        }

    tangent_initial = sphere_radius * (launch @ derivative)
    augmented_initial = np.concatenate(
        [initial_xi, tangent_initial.reshape(-1)]
    )

    def augmented_rhs(_time: float, augmented: np.ndarray) -> np.ndarray:
        xi = augmented[:COMPLEX_DIMENSION]
        tangent = augmented[COMPLEX_DIMENSION:].reshape(
            COMPLEX_DIMENSION, COMPLEX_DIMENSION - 1
        )
        tangent_derivative = -np.conjugate(
            hessian_xi(model, saddle, fixed, xi) @ tangent
        )
        return np.concatenate(
            [
                flow_xi(model, saddle, fixed, xi),
                tangent_derivative.reshape(-1),
            ]
        )

    solution = solve_ivp(
        augmented_rhs,
        (0.0, flow_time),
        augmented_initial,
        method=method,
        rtol=8.0e-11 if strict else 2.0e-7,
        atol=8.0e-13 if strict else 2.0e-9,
        max_step=0.025 if strict else 0.06,
    )
    if not solution.success:
        raise RuntimeError(str(solution.message))
    xi_norm_max = float(
        np.max(np.linalg.norm(solution.y[:COMPLEX_DIMENSION], axis=0))
    )
    if xi_norm_max >= FLOW_NORM_MAX:
        raise RuntimeError("trajectory exceeded the frozen xi-norm cap")
    final = solution.y[:, -1]
    final_xi = final[:COMPLEX_DIMENSION]
    tangent_xi = final[COMPLEX_DIMENSION:].reshape(
        COMPLEX_DIMENSION, COMPLEX_DIMENSION - 1
    )
    linear_z = np.diag(COORDINATE_SCALES) @ fixed.linear_map
    state_z = COORDINATE_SCALES * xi_to_w(saddle, fixed, final_xi)
    tangent_z = linear_z @ tangent_xi
    time_tangent_z = linear_z @ flow_xi(
        model, saddle, fixed, final_xi
    )
    return state_z, np.column_stack([tangent_z, time_tangent_z]), {
        "solver_method": method,
        "solver_steps": int(solution.t.size),
        "xi_norm_max": xi_norm_max,
    }


def endpoint_values(model: NumericModel) -> tuple[np.ndarray, np.ndarray]:
    left = np.array(
        [
            BASE_A * (1.0 - model.delta_a / 2.0),
            BASE_PHI - model.delta_phi / 2.0,
        ]
    )
    right = np.array(
        [
            BASE_A * (1.0 + model.delta_a / 2.0),
            BASE_PHI + model.delta_phi / 2.0,
        ]
    )
    return left, right


def cap_anchor(model: NumericModel) -> np.ndarray:
    left, right = endpoint_values(model)
    values: list[float] = []
    for node in (1, 2, 3):
        point = (1.0 - node / 4.0) * left + (node / 4.0) * right
        values.extend(point.tolist())
    return np.asarray(values, dtype=float)


def gamma_cap(
    model: NumericModel,
    y_values: np.ndarray,
    psi: float,
) -> tuple[np.ndarray, np.ndarray]:
    fields = np.asarray(y_values, dtype=float).reshape(6)
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    phases = np.array(
        [phase_a, phase_phi, phase_a, phase_phi, phase_a, phase_phi],
        dtype=np.complex128,
    )
    state = np.concatenate(
        [
            cap_anchor(model) + phases * fields,
            [CAP_RADIUS * np.exp(1.0j * psi)],
        ]
    )
    tangent = np.zeros(
        (COMPLEX_DIMENSION, COMPLEX_DIMENSION), dtype=np.complex128
    )
    tangent[:6, :6] = np.diag(phases)
    tangent[:6, 6] = 0.5j * phases * fields
    tangent[6, 6] = 1.0j * state[6]
    return state, tangent


def residual_and_variational_jacobian(
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    sphere_radius: float,
    shape_lambda: float,
    method: str,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    dict[str, object],
]:
    gamma_state, gamma_tangent = gamma_cap(
        model, parameters[:6], float(parameters[6])
    )
    k_state, k_tangent, integration = integrate_chart(
        model,
        saddle,
        fixed,
        chart,
        parameters[7:13],
        float(parameters[13]),
        sphere_radius,
        shape_lambda,
        with_tangent=True,
        method=method,
    )
    if k_tangent is None:
        raise AssertionError("variational tangent integration was omitted")
    gamma_frame = real_frame(gamma_tangent)
    k_frame = real_frame(k_tangent)
    residual = interleaved(
        (gamma_state - k_state) / COORDINATE_SCALES
    )
    row_scales = np.repeat(1.0 / COORDINATE_SCALES, 2)
    jacobian = row_scales[:, np.newaxis] * np.column_stack(
        [gamma_frame, -k_frame]
    )
    return (
        residual,
        jacobian,
        gamma_state,
        k_state,
        gamma_frame,
        k_frame,
        integration,
    )


def state_only_residual(
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    sphere_radius: float,
    shape_lambda: float,
    *,
    k_cache: dict[tuple[float, ...], np.ndarray] | None = None,
) -> np.ndarray:
    gamma_state = gamma_cap(model, parameters[:6], float(parameters[6]))[0]
    k_key = tuple(float(value) for value in parameters[7:14])
    k_state: np.ndarray
    if k_cache is not None and k_key in k_cache:
        k_state = k_cache[k_key]
    else:
        k_state = integrate_chart(
            model,
            saddle,
            fixed,
            chart,
            parameters[7:13],
            float(parameters[13]),
            sphere_radius,
            shape_lambda,
            with_tangent=False,
            method="DOP853",
        )[0]
        if k_cache is not None:
            k_cache[k_key] = k_state
    return interleaved((gamma_state - k_state) / COORDINATE_SCALES)


def parameter_bounds() -> tuple[np.ndarray, np.ndarray]:
    lower = np.array(
        [-FIELD_WINDOW] * 6
        + [-np.pi / 2.0]
        + [-CHART_WINDOW] * 6
        + [FLOW_TIME_MIN],
        dtype=float,
    )
    upper = np.array(
        [FIELD_WINDOW] * 6
        + [np.pi / 2.0]
        + [CHART_WINDOW] * 6
        + [FLOW_TIME_MAX],
        dtype=float,
    )
    return lower, upper


def phase39_prolongated_seed() -> np.ndarray:
    y_a = 2.5068120355594645e-18
    y_phi = -0.00048786614557231537
    parameters = np.zeros(2 * COMPLEX_DIMENSION, dtype=float)
    parameters[:6] = np.array(
        [y_a / 2.0, y_phi / 2.0, y_a, y_phi, y_a / 2.0, y_phi / 2.0]
    )
    # Phase39 parameter order is (y_a,y_phi,psi,alpha,beta,time): psi is
    # distinct from the frozen equatorial beta used to reconstruct the K
    # center direction.
    parameters[6] = -1.7194650462251107e-15
    parameters[7:13] = 0.0
    parameters[13] = 10.577953591073094
    return parameters


def initial_candidate_result(
    model: NumericModel,
    sphere_radius: float,
    shape_lambda: float,
    *,
    status: str,
    message: str,
) -> dict[str, object]:
    return {
        "delta_a": model.delta_a,
        "delta_phi": model.delta_phi,
        "sphere_radius": sphere_radius,
        "shape_lambda": shape_lambda,
        "status": status,
        "accepted": False,
        "message": message,
        "parameters": None,
        "intersection_z": None,
        "physical_residual_max_abs": None,
        "gamma_rank": None,
        "k_rank": None,
        "direct_orientation": None,
        "assembled_root_jacobian_orientation": None,
        "finite_difference_control": None,
        "orientation_controls": None,
        "flow_ledger": None,
        "window_margins": None,
    }


def build_overlap_control(
    chart: Chart,
    chart_parameters: np.ndarray,
    gamma_frame: np.ndarray,
    k_frame: np.ndarray,
    direct_sign: int,
    *,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    primary_k_state: np.ndarray,
    flow_time: float,
    sphere_radius: float,
    shape_lambda: float,
) -> dict[str, object]:
    omega, derivative_old = chart.direction(chart_parameters)
    overlap_seed = chart.center + 0.1 * chart.tangent[:, 0]
    overlap_center = overlap_seed / np.linalg.norm(overlap_seed)
    overlap_tangent, overlap_det = deterministic_oriented_null_frame(
        overlap_center
    )
    overlap_chart = Chart(
        center=overlap_center,
        tangent=overlap_tangent,
        orientation_determinant=overlap_det,
        provenance={"kind": "deterministic_overlap_control"},
    )
    denominator = float(omega @ overlap_center)
    if denominator <= 0.0:
        raise RuntimeError("candidate is outside the overlap-chart hemisphere")
    overlap_parameters = overlap_tangent.T @ omega / denominator
    omega_overlap, derivative_new = overlap_chart.direction(overlap_parameters)
    transition = np.linalg.lstsq(derivative_old, derivative_new, rcond=None)[0]
    transition_orientation = matrix_orientation(transition)
    k_transform = np.eye(COMPLEX_DIMENSION)
    k_transform[:6, :6] = transition
    expected_transformed_k = k_frame @ k_transform
    overlap_state, overlap_k_tangent, overlap_integration = integrate_chart(
        model,
        saddle,
        fixed,
        overlap_chart,
        overlap_parameters,
        flow_time,
        sphere_radius,
        shape_lambda,
        with_tangent=True,
        method="DOP853",
    )
    if overlap_k_tangent is None:
        raise RuntimeError("overlap chart omitted its transported tangent")
    overlap_k_frame = real_frame(overlap_k_tangent)
    overlap_orientation = matrix_orientation(
        np.column_stack([gamma_frame, overlap_k_frame])
    )
    corrected_sign = int(
        overlap_orientation["sign"] * transition_orientation["sign"]
    )
    cap_state_distance = float(
        np.linalg.norm(
            interleaved(
                (overlap_state - primary_k_state) / COORDINATE_SCALES
            )
        )
    )
    chart_margin = float(
        CHART_WINDOW - np.max(np.abs(overlap_parameters))
    )
    tangent_transport_relative_error = float(
        np.linalg.norm(overlap_k_frame - expected_transformed_k, ord=2)
        / max(np.linalg.norm(overlap_k_frame, ord=2), 1.0e-30)
    )
    passed = bool(
        chart_margin >= 0.01
        and cap_state_distance <= 5.0e-5
        and transition_orientation["normalized_sigma_min"] >= 1.0e-4
        and corrected_sign == direct_sign
    )
    return {
        "status": "PASS" if passed else "OVERLAP_CHART_CONTROL_FAILED",
        "passed": passed,
        "overlap_chart_parameters": overlap_parameters.tolist(),
        "overlap_chart_margin": chart_margin,
        "overlap_chart_margin_passed": bool(chart_margin >= 0.01),
        "direction_state_distance": float(
            np.linalg.norm(omega_overlap - omega)
        ),
        "strict_overlap_integration": overlap_integration,
        "transported_tangent_relative_operator_error": (
            tangent_transport_relative_error
        ),
        "strict_reintegrated_normalized_cap_state_distance": cap_state_distance,
        "cap_state_match_passed": bool(cap_state_distance <= 5.0e-5),
        "transition_orientation": transition_orientation,
        "transition_sigma_min_passed": bool(
            transition_orientation["normalized_sigma_min"] >= 1.0e-4
        ),
        "raw_overlap_sign": overlap_orientation["sign"],
        "determinant_corrected_sign": corrected_sign,
        "agrees_with_primary": bool(corrected_sign == direct_sign),
    }


def first_cap_event(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    chart_parameters: np.ndarray,
    sphere_radius: float,
    shape_lambda: float,
    *,
    time_limit: float,
) -> dict[str, object]:
    omega = chart.direction(chart_parameters)[0]
    initial_xi = sphere_radius * (saddle.launch_matrix(shape_lambda) @ omega)

    def cap_event(_time: float, xi: np.ndarray) -> float:
        state_z = COORDINATE_SCALES * xi_to_w(saddle, fixed, xi)
        return float(abs(state_z[-1]) - CAP_RADIUS)

    cap_event.terminal = True  # type: ignore[attr-defined]
    cap_event.direction = -1.0  # type: ignore[attr-defined]
    solution = solve_ivp(
        lambda _time, xi: flow_xi(model, saddle, fixed, xi),
        (0.0, time_limit),
        initial_xi,
        events=cap_event,
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.04,
    )
    if not solution.success:
        return {
            "status": "INTEGRATION_FAILED",
            "message": str(solution.message),
            "event_count": 0,
        }
    if len(solution.t_events[0]) == 0:
        return {
            "status": "NO_CAP_EVENT",
            "message": "no |T|=.3 event before the frozen time limit",
            "event_count": 0,
            "xi_norm_max": float(np.max(np.linalg.norm(solution.y, axis=0))),
        }
    event_time = float(solution.t_events[0][0])
    event_xi = np.asarray(solution.y_events[0][0], dtype=np.complex128)
    state_z = COORDINATE_SCALES * xi_to_w(saddle, fixed, event_xi)
    return {
        "status": "FIRST_CAP_EVENT",
        "message": str(solution.message),
        "event_count": int(len(solution.t_events[0])),
        "event_time": event_time,
        "event_state_z": state_z,
        "radius_residual": float(abs(abs(state_z[-1]) - CAP_RADIUS)),
        "xi_norm_max": float(np.max(np.linalg.norm(solution.y, axis=0))),
    }


def deterministic_center_hit_seed(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
) -> tuple[np.ndarray, dict[str, object]]:
    event = first_cap_event(
        model,
        saddle,
        fixed,
        chart,
        np.zeros(6),
        PRIMARY_SPHERE_RADIUS,
        1.0,
        time_limit=FLOW_TIME_MAX,
    )
    if event["status"] != "FIRST_CAP_EVENT":
        raise RuntimeError("frozen nested center has no deterministic first-cap seed")
    state = np.asarray(event["event_state_z"], dtype=np.complex128)
    psi = float(np.angle(state[-1]))
    anchor = cap_anchor(model)
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    phases = np.array(
        [phase_a, phase_phi, phase_a, phase_phi, phase_a, phase_phi]
    )
    # Least-squares projection of the first-hit state onto the declared real-y
    # cap fibre.  This is only a deterministic root seed; the full R14 solve
    # retains all fourteen equations and may fail closed.
    y_values = np.real(np.conjugate(phases) * (state[:6] - anchor))
    parameters = np.zeros(2 * COMPLEX_DIMENSION, dtype=float)
    parameters[:6] = y_values
    parameters[6] = psi
    parameters[7:13] = 0.0
    parameters[13] = float(event["event_time"])
    return parameters, {
        "source": "first cap event on the frozen nested center direction",
        "event_time": float(event["event_time"]),
        "event_radius_residual": float(event["radius_residual"]),
        "projected_y": y_values.tolist(),
        "psi": psi,
        "unprojected_scaled_cap_residual": float(
            np.max(
                np.abs(
                    interleaved(
                        (gamma_cap(model, y_values, psi)[0] - state)
                        / COORDINATE_SCALES
                    )
                )
            )
        ),
        "phase39_affine_seed_recorded_as_negative_control": (
            phase39_prolongated_seed().tolist()
        ),
    }


def flow_ledger(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    parameters: np.ndarray,
    sphere_radius: float,
    shape_lambda: float,
) -> dict[str, object]:
    omega = chart.direction(parameters[7:13])[0]
    initial_xi = sphere_radius * (
        saddle.launch_matrix(shape_lambda) @ omega
    )
    flow_time = float(parameters[13])
    times = np.linspace(0.0, flow_time, 101)
    solution = solve_ivp(
        lambda _time, xi: flow_xi(model, saddle, fixed, xi),
        (0.0, flow_time),
        initial_xi,
        t_eval=times,
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.04,
    )
    if not solution.success:
        raise RuntimeError(str(solution.message))
    actions = np.array(
        [
            action_at(model, xi_to_w(saddle, fixed, solution.y[:, index]))
            for index in range(solution.y.shape[1])
        ]
    )
    xi_norms = np.linalg.norm(solution.y, axis=0)
    first_event = first_cap_event(
        model,
        saddle,
        fixed,
        chart,
        parameters[7:13],
        sphere_radius,
        shape_lambda,
        time_limit=min(FLOW_TIME_MAX, flow_time + 0.05),
    )
    event_time_difference = None
    event_state_distance = None
    if first_event["status"] == "FIRST_CAP_EVENT":
        event_time_difference = abs(
            float(first_event["event_time"]) - flow_time
        )
        event_state = np.asarray(
            first_event["event_state_z"], dtype=np.complex128
        )
        candidate_state = gamma_cap(
            model, parameters[:6], float(parameters[6])
        )[0]
        event_state_distance = float(
            np.linalg.norm(
                interleaved(
                    (event_state - candidate_state) / COORDINATE_SCALES
                )
            )
        )
    return {
        "sample_count": int(times.size),
        "ReS_start": float(actions.real[0]),
        "ReS_end": float(actions.real[-1]),
        "ReS_max_positive_step": float(np.max(np.diff(actions.real))),
        "ImS_max_drift": float(
            np.max(np.abs(actions.imag - actions.imag[0]))
        ),
        "xi_norm_max": float(np.max(xi_norms)),
        "xi_norm_margin": float(FLOW_NORM_MAX - np.max(xi_norms)),
        "first_cap_event_status": first_event["status"],
        "first_cap_radius_residual": first_event.get("radius_residual"),
        "first_cap_time_difference": event_time_difference,
        "first_cap_normalized_state_distance": event_state_distance,
    }


def window_margins(parameters: np.ndarray, xi_norm_max: float) -> dict[str, float]:
    return {
        "minimum_y_margin": float(
            FIELD_WINDOW - np.max(np.abs(parameters[:6]))
        ),
        "psi_margin": float(np.pi / 2.0 - abs(parameters[6])),
        "minimum_chart_margin": float(
            CHART_WINDOW - np.max(np.abs(parameters[7:13]))
        ),
        "flow_time_lower_margin": float(parameters[13] - FLOW_TIME_MIN),
        "flow_time_upper_margin": float(FLOW_TIME_MAX - parameters[13]),
        "flow_norm_margin": float(FLOW_NORM_MAX - xi_norm_max),
    }


def solve_intersection(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    initial: np.ndarray,
    sphere_radius: float,
    shape_lambda: float,
    *,
    mode_bases: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray | None, dict[str, object]]:
    lower, upper = parameter_bounds()
    seed = np.minimum(np.maximum(np.asarray(initial, dtype=float), lower + 1e-8), upper - 1e-8)
    coarse_cache: dict[str, object] = {}

    def evaluate_cached(
        parameters: np.ndarray,
        method: str,
        cache: dict[str, object],
    ) -> tuple[object, ...]:
        known = cache.get("parameters")
        if known is None or not np.array_equal(parameters, known):
            cache["parameters"] = parameters.copy()
            cache["evaluation"] = residual_and_variational_jacobian(
                parameters,
                model,
                saddle,
                fixed,
                chart,
                sphere_radius,
                shape_lambda,
                method,
            )
        return cache["evaluation"]  # type: ignore[return-value]

    try:
        coarse = least_squares(
            lambda parameters: evaluate_cached(
                parameters, "BDF", coarse_cache
            )[0],
            seed,
            jac=lambda parameters: evaluate_cached(
                parameters, "BDF", coarse_cache
            )[1],
            bounds=(lower, upper),
            x_scale="jac",
            ftol=2.0e-10,
            xtol=2.0e-10,
            gtol=2.0e-10,
            max_nfev=60,
        )
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
        return None, initial_candidate_result(
            model,
            sphere_radius,
            shape_lambda,
            status="NO_ROOT_FOUND_IN_FROZEN_SEARCH",
            message=f"coarse BDF solve failed: {error}",
        )

    accurate_cache: dict[str, object] = {}
    parameters = np.asarray(coarse.x, dtype=float)
    newton_history: list[dict[str, float]] = []
    refined = False
    try:
        for _iteration in range(7):
            residual, jacobian = evaluate_cached(
                parameters, "DOP853", accurate_cache
            )[:2]
            residual_array = np.asarray(residual, dtype=float)
            jacobian_array = np.asarray(jacobian, dtype=float)
            residual_max = float(np.max(np.abs(residual_array)))
            newton_history.append(
                {
                    "scaled_residual_max_abs": residual_max,
                    "jacobian_condition_number": float(
                        np.linalg.cond(jacobian_array)
                    ),
                }
            )
            if residual_max < 2.0e-8:
                refined = True
                break
            correction = np.linalg.solve(jacobian_array, -residual_array)
            accepted_step = False
            for damping in (1.0, 0.5, 0.25, 0.125):
                proposed = parameters + damping * correction
                if np.all(proposed > lower) and np.all(proposed < upper):
                    parameters = proposed
                    accurate_cache.clear()
                    accepted_step = True
                    break
            if not accepted_step:
                raise RuntimeError("strict Newton correction left frozen box")
        evaluation = evaluate_cached(parameters, "DOP853", accurate_cache)
        if not refined:
            final_residual_max = float(
                np.max(np.abs(np.asarray(evaluation[0], dtype=float)))
            )
            newton_history.append(
                {
                    "scaled_residual_max_abs": final_residual_max,
                    "jacobian_condition_number": float(
                        np.linalg.cond(np.asarray(evaluation[1], dtype=float))
                    ),
                }
            )
            refined = final_residual_max < 2.0e-8
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
        failed = initial_candidate_result(
            model,
            sphere_radius,
            shape_lambda,
            status="NO_ROOT_FOUND_IN_FROZEN_SEARCH",
            message=f"strict DOP853 refinement failed: {error}",
        )
        failed["coarse_solver_success"] = bool(coarse.success)
        failed["coarse_solver_message"] = str(coarse.message)
        failed["strict_Newton_history"] = newton_history
        return None, failed

    (
        scaled_residual,
        dop_jacobian,
        gamma_state,
        k_state,
        gamma_frame,
        k_frame,
        integration,
    ) = evaluation
    physical_residual = interleaved(gamma_state - k_state)
    direct = matrix_orientation(np.column_stack([gamma_frame, k_frame]))
    root_orientation = matrix_orientation(
        np.column_stack([gamma_frame, -k_frame])
    )
    reverse_gamma = matrix_orientation(
        np.column_stack(
            [
                gamma_frame
                @ np.diag([-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
                k_frame,
            ]
        )
    )
    reverse_k = matrix_orientation(
        np.column_stack(
            [
                gamma_frame,
                k_frame
                @ np.diag([-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
            ]
        )
    )
    # Nodal-to-mode maps act on ambient rows.  Gamma/K columns are cap/chart
    # parameters and must never receive a field-mode basis transformation.
    dst_basis, nested_basis = mode_bases
    combined_frame = np.column_stack([gamma_frame, k_frame])
    dst_coordinate_map = np.kron(dst_basis.T, np.eye(2))
    nested_coordinate_map = np.kron(nested_basis.T, np.eye(2))
    dst_orientation = matrix_orientation(dst_coordinate_map @ combined_frame)
    nested_orientation = matrix_orientation(
        nested_coordinate_map @ combined_frame
    )
    complex_transition = np.linalg.solve(dst_basis, nested_basis)
    try:
        overlap = build_overlap_control(
            chart,
            parameters[7:13],
            gamma_frame,
            k_frame,
            int(direct["sign"]),
            model=model,
            saddle=saddle,
            fixed=fixed,
            primary_k_state=k_state,
            flow_time=float(parameters[13]),
            sphere_radius=sphere_radius,
            shape_lambda=shape_lambda,
        )
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
        overlap = {
            "status": "OVERLAP_CHART_CONTROL_FAILED",
            "passed": False,
            "message": str(error),
        }
    try:
        ledger = flow_ledger(
            model,
            saddle,
            fixed,
            chart,
            parameters,
            sphere_radius,
            shape_lambda,
        )
    except RuntimeError as error:
        ledger = {"status": "PATH_LEDGER_FAILED", "message": str(error)}
    xi_norm_max = float(integration["xi_norm_max"])
    margins = window_margins(parameters, xi_norm_max)
    margins_passed = bool(
        margins["minimum_y_margin"] >= 0.005
        and margins["psi_margin"] >= 0.005
        and margins["minimum_chart_margin"] >= 0.01
        and margins["flow_time_lower_margin"] >= 0.02
        and margins["flow_time_upper_margin"] >= 0.02
        and margins["flow_norm_margin"] >= 0.1
    )
    accepted = bool(
        refined
        and np.max(np.abs(physical_residual)) < 2.0e-7
        and np.linalg.matrix_rank(gamma_frame) == COMPLEX_DIMENSION
        and np.linalg.matrix_rank(k_frame) == COMPLEX_DIMENSION
        and direct["normalized_sigma_min"] > 2.0e-4
        and margins_passed
    )
    status = "PASS" if accepted else "NO_ROOT_FOUND_OR_NONTRANSVERSE_IN_FROZEN_SEARCH"
    result: dict[str, object] = {
        "delta_a": model.delta_a,
        "delta_phi": model.delta_phi,
        "sphere_radius": sphere_radius,
        "shape_lambda": shape_lambda,
        "status": status,
        "accepted": accepted,
        "message": (
            "strict-map candidate met local residual/rank/transversality thresholds"
            if accepted
            else "candidate did not meet all frozen local thresholds"
        ),
        "coarse_solver_success": bool(coarse.success),
        "coarse_solver_message": str(coarse.message),
        "coarse_solver_nfev": int(coarse.nfev),
        "strict_refinement_success": refined,
        "strict_Newton_history": newton_history,
        "parameters": parameters.tolist(),
        "intersection_z": [
            [float(value.real), float(value.imag)] for value in gamma_state
        ],
        "scaled_residual_max_abs": float(np.max(np.abs(scaled_residual))),
        "physical_residual_max_abs": float(
            np.max(np.abs(physical_residual))
        ),
        "physical_residual_norm": float(np.linalg.norm(physical_residual)),
        "gamma_rank": int(np.linalg.matrix_rank(gamma_frame)),
        "k_rank": int(np.linalg.matrix_rank(k_frame)),
        "direct_orientation": direct,
        "assembled_root_jacobian_orientation": root_orientation,
        "variational_scaled_root_jacobian": np.asarray(
            dop_jacobian, dtype=float
        ).tolist(),
        "orientation_controls": {
            "root_parity_passed": bool(
                root_orientation["sign"] == -direct["sign"]
            ),
            "reverse_Gamma_first_parameter_sign": reverse_gamma["sign"],
            "reverse_K_first_parameter_sign": reverse_k["sign"],
            "DST_complex_basis_determinant": float(
                np.linalg.det(dst_basis)
            ),
            "nested_complex_basis_determinant": float(
                np.linalg.det(nested_basis)
            ),
            "DST_to_nested_complex_transition_determinant": float(
                np.linalg.det(complex_transition)
            ),
            "realified_DST_row_map_determinant": float(
                np.linalg.det(dst_coordinate_map)
            ),
            "realified_nested_row_map_determinant": float(
                np.linalg.det(nested_coordinate_map)
            ),
            "DST_coordinate_sign": dst_orientation["sign"],
            "nested_coordinate_sign": nested_orientation["sign"],
            "ambient_row_basis_sign_agrees": bool(
                dst_orientation["sign"] == direct["sign"]
                and nested_orientation["sign"] == direct["sign"]
            ),
            "overlap_chart": overlap,
        },
        "flow_ledger": ledger,
        "window_margins": margins,
        "window_margins_passed": margins_passed,
        "integration": integration,
        "finite_difference_control": None,
    }
    return parameters, result


def finite_difference_control(
    manifest: dict[str, object],
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    sphere_radius: float,
    shape_lambda: float,
    variational_jacobian: np.ndarray,
    direct_sign: int,
) -> dict[str, object]:
    policy = manifest["intersection_protocol"]["finite_difference_step_policy"]
    proposed: list[tuple[float, ...]] = []
    proposed.extend(
        [tuple(float(v) for v in policy["Gamma_field_y_columns"])] * 6
    )
    proposed.append(tuple(float(v) for v in policy["Gamma_psi_column"]))
    proposed.append(tuple(float(v) for v in policy["K_u1_column"]))
    proposed.extend(
        [tuple(float(v) for v in policy["K_u2_through_u6_columns"])] * 5
    )
    proposed.append(tuple(float(v) for v in policy["K_flow_time_column"]))
    if len(proposed) != 2 * COMPLEX_DIMENSION:
        raise ExactContractError("finite-difference policy has wrong dimension")

    k_cache: dict[tuple[float, ...], np.ndarray] = {}
    chosen_columns: list[np.ndarray] = []
    chosen_steps: list[float] = []
    plateau_differences: list[float] = []
    per_column: list[dict[str, object]] = []
    for index, ladder in enumerate(proposed):
        evaluations: list[tuple[float, np.ndarray]] = []
        errors: list[dict[str, object]] = []
        for step in ladder:
            plus = parameters.copy()
            minus = parameters.copy()
            plus[index] += step
            minus[index] -= step
            try:
                plus_residual = state_only_residual(
                    plus,
                    model,
                    saddle,
                    fixed,
                    chart,
                    sphere_radius,
                    shape_lambda,
                    k_cache=k_cache,
                )
                minus_residual = state_only_residual(
                    minus,
                    model,
                    saddle,
                    fixed,
                    chart,
                    sphere_radius,
                    shape_lambda,
                    k_cache=k_cache,
                )
                evaluations.append(
                    (step, (plus_residual - minus_residual) / (2.0 * step))
                )
            except RuntimeError as error:
                errors.append({"step": step, "error": str(error)})
        adjacent: tuple[
            tuple[float, np.ndarray], tuple[float, np.ndarray]
        ] | None = None
        for first, second in zip(evaluations[:-1], evaluations[1:]):
            first_index = ladder.index(first[0])
            second_index = ladder.index(second[0])
            if second_index == first_index + 1:
                adjacent = (first, second)
                break
        if adjacent is None:
            return {
                "status": "TANGENT_CONTROL_FAILED",
                "passed": False,
                "message": f"no adjacent FD pair survived for column {index}",
                "failed_column": index,
                "errors": errors,
            }
        (step_one, column_one), (step_two, column_two) = adjacent
        plateau = float(
            np.linalg.norm(column_one - column_two)
            / max(np.linalg.norm(column_one), 1.0e-30)
        )
        chosen_columns.append(column_one)
        chosen_steps.append(step_one)
        plateau_differences.append(plateau)
        per_column.append(
            {
                "index": index,
                "chosen_steps": [step_one, step_two],
                "plateau_relative_difference": plateau,
                "earlier_failures": errors,
            }
        )
    finite_difference = np.column_stack(chosen_columns)
    orientation = matrix_orientation(finite_difference)
    variational = np.asarray(variational_jacobian, dtype=float)
    relative_error = float(
        np.linalg.norm(finite_difference - variational, ord=2)
        / np.linalg.norm(variational, ord=2)
    )
    maximum_plateau = max(plateau_differences)
    passed = bool(
        orientation["sign"] == -direct_sign
        and relative_error < 0.02
        and maximum_plateau < 0.02
    )
    return {
        "status": "PASS" if passed else "TANGENT_CONTROL_FAILED",
        "passed": passed,
        "finite_difference_orientation": orientation,
        "expected_root_sign": -direct_sign,
        "FD_to_variational_relative_operator_error": relative_error,
        "maximum_adjacent_step_relative_change": maximum_plateau,
        "chosen_steps": chosen_steps,
        "per_column": per_column,
    }


def state_from_result(result: dict[str, object]) -> np.ndarray | None:
    raw = result.get("intersection_z")
    if raw is None:
        return None
    return np.array([complex(*value) for value in raw], dtype=np.complex128)


def normalized_state_distance(
    left: dict[str, object], right: dict[str, object]
) -> float | None:
    left_state = state_from_result(left)
    right_state = state_from_result(right)
    if left_state is None or right_state is None:
        return None
    return float(
        np.linalg.norm(
            interleaved((left_state - right_state) / COORDINATE_SCALES)
        )
    )


def map_launch_direction_to_shape(
    saddle: SaddleData,
    source_chart: Chart,
    source_parameters: np.ndarray,
    source_lambda: float,
    target_lambda: float,
) -> tuple[Chart, dict[str, object]]:
    source_omega = source_chart.direction(source_parameters)[0]
    source_vector = interleaved(
        saddle.launch_matrix(source_lambda) @ source_omega
    )
    target_real = real_frame(saddle.launch_matrix(target_lambda))
    target_projector = target_real @ np.linalg.solve(
        target_real.T @ target_real, target_real.T
    )
    projected = target_projector @ source_vector
    projection_ratio = float(
        np.linalg.norm(projected) / np.linalg.norm(source_vector)
    )
    coefficients = np.linalg.lstsq(target_real, projected, rcond=None)[0]
    coefficients /= np.linalg.norm(coefficients)
    overlap = float((target_real @ coefficients) @ source_vector)
    if overlap < 0.0:
        coefficients *= -1.0
        overlap *= -1.0
    tangent, determinant = deterministic_oriented_null_frame(coefficients)
    return Chart(
        center=coefficients,
        tangent=tangent,
        orientation_determinant=determinant,
        provenance={
            "kind": "launch-shape positive-overlap map",
            "source_lambda": source_lambda,
            "target_lambda": target_lambda,
            "projection_ratio": projection_ratio,
            "positive_overlap": overlap,
        },
    ), {
        "projection_ratio": projection_ratio,
        "positive_overlap": overlap,
        "target_center": coefficients.tolist(),
        "target_det_B_center": determinant,
    }


def solve_radius_controls(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    primary_parameters: np.ndarray,
    primary_result: dict[str, object],
    mode_bases: tuple[np.ndarray, np.ndarray],
) -> dict[str, object]:
    controls: dict[str, object] = {}
    all_passed = True
    primary_sign = primary_result["direct_orientation"]["sign"]
    for radius in CONTROL_SPHERE_RADII:
        seed = primary_parameters.copy()
        seed[13] += np.log(PRIMARY_SPHERE_RADIUS / radius)
        parameters, result = solve_intersection(
            model,
            saddle,
            fixed,
            chart,
            seed,
            radius,
            1.0,
            mode_bases=mode_bases,
        )
        distance = normalized_state_distance(primary_result, result)
        passed = bool(
            parameters is not None
            and result["accepted"]
            and result.get("window_margins_passed") is True
            and result["direct_orientation"]["sign"] == primary_sign
            and distance is not None
            and distance <= 5.0e-5
        )
        controls[str(radius)] = {
            "passed": passed,
            "normalized_ambient_cap_state_distance": distance,
            "result": result,
        }
        all_passed = all_passed and passed
    return {"passed": all_passed, "controls": controls}


def solve_shape_control(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    primary_chart: Chart,
    primary_parameters: np.ndarray,
    primary_result: dict[str, object],
    mode_bases: tuple[np.ndarray, np.ndarray],
) -> dict[str, object]:
    primary_sign = primary_result["direct_orientation"]["sign"]

    def attempt(
        source_chart: Chart,
        source_parameters: np.ndarray,
        source_lambda: float,
        target_lambda: float,
    ) -> tuple[np.ndarray | None, Chart, dict[str, object], dict[str, object]]:
        target_chart, mapping = map_launch_direction_to_shape(
            saddle,
            source_chart,
            source_parameters[7:13],
            source_lambda,
            target_lambda,
        )
        seed = source_parameters.copy()
        seed[7:13] = 0.0
        parameters, result = solve_intersection(
            model,
            saddle,
            fixed,
            target_chart,
            seed,
            PRIMARY_SPHERE_RADIUS,
            target_lambda,
            mode_bases=mode_bases,
        )
        return parameters, target_chart, mapping, result

    lambda_zero_parameters, lambda_zero_chart, map_zero, lambda_zero = attempt(
        primary_chart, primary_parameters, 1.0, 0.0
    )
    zero_distance = normalized_state_distance(primary_result, lambda_zero)
    zero_passed = bool(
        lambda_zero_parameters is not None
        and lambda_zero["accepted"]
        and lambda_zero.get("window_margins_passed") is True
        and lambda_zero["direct_orientation"]["sign"] == primary_sign
        and zero_distance is not None
        and zero_distance <= 5.0e-5
    )
    result: dict[str, object] = {
        "passed": zero_passed,
        "lambda_zero": {
            "mapping": map_zero,
            "normalized_ambient_cap_state_distance": zero_distance,
            "result": lambda_zero,
        },
        "lambda_half_bridge_triggered": False,
        "lambda_half_bridge": None,
        "lambda_zero_after_bridge": None,
    }
    if zero_passed:
        return result

    half_parameters, half_chart, map_half, half_result = attempt(
        primary_chart, primary_parameters, 1.0, 0.5
    )
    half_distance = normalized_state_distance(primary_result, half_result)
    half_passed = bool(
        half_parameters is not None
        and half_result["accepted"]
        and half_result.get("window_margins_passed") is True
        and half_result["direct_orientation"]["sign"] == primary_sign
        and half_distance is not None
        and half_distance <= 5.0e-5
    )
    result["lambda_half_bridge_triggered"] = True
    result["lambda_half_bridge"] = {
        "passed": half_passed,
        "mapping": map_half,
        "normalized_ambient_cap_state_distance": half_distance,
        "result": half_result,
    }
    if not half_passed or half_parameters is None:
        return result

    bridged_parameters, _bridged_chart, map_bridged, bridged_result = attempt(
        half_chart, half_parameters, 0.5, 0.0
    )
    bridged_distance = normalized_state_distance(primary_result, bridged_result)
    bridged_passed = bool(
        bridged_parameters is not None
        and bridged_result["accepted"]
        and bridged_result.get("window_margins_passed") is True
        and bridged_result["direct_orientation"]["sign"] == primary_sign
        and bridged_distance is not None
        and bridged_distance <= 5.0e-5
    )
    result["lambda_zero_after_bridge"] = {
        "passed": bridged_passed,
        "mapping": map_bridged,
        "normalized_ambient_cap_state_distance": bridged_distance,
        "result": bridged_result,
    }
    result["passed"] = bridged_passed
    return result


def relative_operator_error(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.linalg.norm(left - right, ord=2)
        / max(np.linalg.norm(right, ord=2), 1.0e-30)
    )


def saddle_grid_diagnostics(
    saddle_records: dict[tuple[float, float], dict[str, object]],
    saddle_data: dict[tuple[float, float], SaddleData],
) -> dict[str, object]:
    expected_points = {(0.0, 0.0)} | {
        source_point(source, sign * magnitude)
        for source in ("phi_only", "a_only")
        for sign in (-1.0, 1.0)
        for magnitude in (SOURCE_HALF, SOURCE_FULL)
    }
    point_checks: dict[str, object] = {}
    point_passed = True
    for point in sorted(expected_points):
        record = saddle_records[point]
        passed = bool(
            float(record["gradient_max_abs"]) <= 1.0e-9
            and float(record["hessian_min_abs_eigenvalue"]) >= 1.0e-3
            and record["hessian_inertia"]
            == {"negative": 4, "positive": 3, "zero": 0}
        )
        point_checks[point_label(point)] = {
            "passed": passed,
            "gradient_max_abs": record["gradient_max_abs"],
            "hessian_min_abs_eigenvalue": record[
                "hessian_min_abs_eigenvalue"
            ],
            "hessian_inertia": record["hessian_inertia"],
            "solver_success": record["solver_success"],
        }
        point_passed = point_passed and passed

    reflection_checks: dict[str, object] = {}
    reflection_passed = True
    for source in ("phi_only", "a_only"):
        for magnitude in (SOURCE_HALF, SOURCE_FULL):
            plus = saddle_data[source_point(source, magnitude)]
            minus = saddle_data[source_point(source, -magnitude)]
            saddle_error = float(
                np.max(np.abs(minus.saddle_w - REFLECTION @ plus.saddle_w))
            )
            action_error = float(abs(minus.action - plus.action))
            hessian_error = relative_operator_error(
                minus.hessian_w, REFLECTION @ plus.hessian_w @ REFLECTION
            )
            passed = bool(
                saddle_error <= 2.0e-8
                and action_error <= 2.0e-8
                and hessian_error <= 2.0e-7
            )
            label = f"{source}:half" if magnitude == SOURCE_HALF else f"{source}:full"
            reflection_checks[label] = {
                "passed": passed,
                "saddle_normalized_max_abs": saddle_error,
                "action_max_abs": action_error,
                "hessian_relative_operator_error": hessian_error,
            }
            reflection_passed = reflection_passed and passed
    return {
        "passed": bool(
            set(saddle_records) == expected_points
            and set(saddle_data) == expected_points
            and point_passed
            and reflection_passed
        ),
        "unique_point_count": len(saddle_records),
        "independent_arm_policy": (
            "positive and negative saddle arms were each started at the one "
            "shared zero saddle and continued half then full"
        ),
        "point_checks": point_checks,
        "reflection_checks": reflection_checks,
    }


def metric_geometry_diagnostics(
    fixed: FixedMetric,
    saddle_data: dict[tuple[float, float], SaddleData],
) -> dict[str, object]:
    q = fixed.xi_reflection
    q_orthogonality = float(
        np.linalg.norm(q.T @ q - np.eye(COMPLEX_DIMENSION), ord=2)
    )
    q_involution = float(
        np.linalg.norm(q @ q - np.eye(COMPLEX_DIMENSION), ord=2)
    )
    mobility_reflection = relative_operator_error(
        REFLECTION
        @ fixed.inverse_metric_mobility_w
        @ REFLECTION,
        fixed.inverse_metric_mobility_w,
    )
    base_signs = np.sign(fixed.eigenvalues_zero).astype(int)
    pair_checks: dict[str, object] = {}
    maximum_projector_error = 0.0
    maximum_frame_error = 0.0
    for source in ("phi_only", "a_only"):
        for magnitude in (SOURCE_HALF, SOURCE_FULL):
            plus = saddle_data[source_point(source, magnitude)]
            minus = saddle_data[source_point(source, -magnitude)]
            signed_checks: dict[str, object] = {}
            for sign in (-1, 1):
                indices = np.flatnonzero(base_signs == sign)
                projector_error = relative_operator_error(
                    minus.signed_projectors[sign],
                    q.T @ plus.signed_projectors[sign] @ q,
                )
                expected = q.T @ plus.aligned_signed_frame_xi[:, indices]
                actual = minus.aligned_signed_frame_xi[:, indices]
                left, _singular, right_transpose = np.linalg.svd(
                    expected.T @ actual
                )
                procrustes = left @ right_transpose
                frame_error = relative_operator_error(
                    expected @ procrustes, actual
                )
                maximum_projector_error = max(
                    maximum_projector_error, projector_error
                )
                maximum_frame_error = max(maximum_frame_error, frame_error)
                signed_checks[str(sign)] = {
                    "projector_relative_operator_error": projector_error,
                    "block_Procrustes_frame_relative_operator_error": (
                        frame_error
                    ),
                }
            pair_checks[
                f"{source}:{'half' if magnitude == SOURCE_HALF else 'full'}"
            ] = signed_checks

    takagi_checks: dict[str, float] = {}
    maximum_takagi_error = 0.0
    for point, data in saddle_data.items():
        launch = data.launch_matrix(1.0)
        error = float(
            np.linalg.norm(
                launch.T @ data.hessian_xi @ launch
                + np.eye(COMPLEX_DIMENSION),
                ord=2,
            )
        )
        takagi_checks[point_label(point)] = error
        maximum_takagi_error = max(maximum_takagi_error, error)

    passed = bool(
        q_orthogonality <= 2.0e-7
        and q_involution <= 2.0e-7
        and mobility_reflection <= 2.0e-7
        and maximum_projector_error <= 2.0e-7
        and maximum_frame_error <= 2.0e-7
        and maximum_takagi_error <= 2.0e-7
    )
    return {
        "passed": passed,
        "one_shared_linear_map_sha256": hashlib.sha256(
            np.ascontiguousarray(fixed.linear_map).tobytes()
        ).hexdigest(),
        "source_rewhitening_performed": False,
        "launch_shape_changes_flow_mobility": False,
        "xi_reflection_determinant": float(np.linalg.det(q)),
        "xi_reflection_orthogonality_residual": q_orthogonality,
        "xi_reflection_involution_residual": q_involution,
        "fixed_mobility_reflection_relative_operator_error": (
            mobility_reflection
        ),
        "signed_projector_max_relative_operator_error": (
            maximum_projector_error
        ),
        "transported_frame_max_block_Procrustes_error": maximum_frame_error,
        "lambda_one_Takagi_max_spectral_residual": maximum_takagi_error,
        "pair_checks": pair_checks,
        "lambda_one_Takagi_checks": takagi_checks,
        "fixed_zero_Hw_eigenvalues": fixed.eigenvalues_zero.tolist(),
    }


def safe_intersection_solve(
    label: str,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    chart: Chart,
    seed: np.ndarray,
    sphere_radius: float,
    shape_lambda: float,
    mode_bases: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray | None, dict[str, object]]:
    print(
        f"[R14] {label}: da={model.delta_a:+.4g}, "
        f"dp={model.delta_phi:+.4g}, rho={sphere_radius:.1e}, "
        f"lambda={shape_lambda:g}",
        flush=True,
    )
    try:
        return solve_intersection(
            model,
            saddle,
            fixed,
            chart,
            seed,
            sphere_radius,
            shape_lambda,
            mode_bases=mode_bases,
        )
    except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
        return None, initial_candidate_result(
            model,
            sphere_radius,
            shape_lambda,
            status="NO_ROOT_FOUND_IN_FROZEN_SEARCH",
            message=f"{label} raised inside frozen solve: {error}",
        )


def solve_primary_intersections(
    manifest: dict[str, object],
    saddle_data: dict[tuple[float, float], SaddleData],
    fixed: FixedMetric,
    chart: Chart,
    mode_bases: tuple[np.ndarray, np.ndarray],
) -> tuple[
    dict[str, np.ndarray],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, object],
]:
    parameters: dict[str, np.ndarray] = {}
    results: dict[str, dict[str, object]] = {}
    intermediate: dict[str, dict[str, object]] = {}
    zero_model = numeric_model(0.0, 0.0)
    zero_seed, seed_record = deterministic_center_hit_seed(
        zero_model, saddle_data[(0.0, 0.0)], fixed, chart
    )
    zero_parameters, zero_result = safe_intersection_solve(
        "shared_zero",
        zero_model,
        saddle_data[(0.0, 0.0)],
        fixed,
        chart,
        zero_seed,
        PRIMARY_SPHERE_RADIUS,
        1.0,
        mode_bases,
    )
    results["shared_zero"] = zero_result
    if zero_parameters is None or not zero_result["accepted"]:
        for label, point in (
            ("phi_minus", (0.0, -SOURCE_FULL)),
            ("phi_plus", (0.0, SOURCE_FULL)),
            ("a_minus", (-SOURCE_FULL, 0.0)),
            ("a_plus", (SOURCE_FULL, 0.0)),
        ):
            results[label] = initial_candidate_result(
                numeric_model(*point),
                PRIMARY_SPHERE_RADIUS,
                1.0,
                status="NO_ROOT_FOUND_IN_FROZEN_SEARCH",
                message="shared-zero frozen seed did not produce an accepted root",
            )
        return parameters, results, intermediate, seed_record
    parameters["shared_zero"] = zero_parameters

    for source, prefix in (("phi_only", "phi"), ("a_only", "a")):
        half_point = source_point(source, SOURCE_HALF)
        half_parameters, half_result = safe_intersection_solve(
            f"{prefix}_plus_half",
            numeric_model(*half_point),
            saddle_data[half_point],
            fixed,
            chart,
            zero_parameters.copy(),
            PRIMARY_SPHERE_RADIUS,
            1.0,
            mode_bases,
        )
        intermediate[f"{prefix}_plus_half"] = half_result
        plus_point = source_point(source, SOURCE_FULL)
        if half_parameters is not None and half_result["accepted"]:
            plus_parameters, plus_result = safe_intersection_solve(
                f"{prefix}_plus",
                numeric_model(*plus_point),
                saddle_data[plus_point],
                fixed,
                chart,
                half_parameters.copy(),
                PRIMARY_SPHERE_RADIUS,
                1.0,
                mode_bases,
            )
        else:
            plus_parameters = None
            plus_result = initial_candidate_result(
                numeric_model(*plus_point),
                PRIMARY_SPHERE_RADIUS,
                1.0,
                status="NO_ROOT_FOUND_IN_FROZEN_SEARCH",
                message="positive half-step continuation failed closed",
            )
        results[f"{prefix}_plus"] = plus_result
        if plus_parameters is not None and plus_result["accepted"]:
            parameters[f"{prefix}_plus"] = plus_parameters

        # The negative full endpoint starts again from the common zero.  It is
        # neither copied from the positive solution nor supplied by reflection.
        minus_point = source_point(source, -SOURCE_FULL)
        minus_parameters, minus_result = safe_intersection_solve(
            f"{prefix}_minus",
            numeric_model(*minus_point),
            saddle_data[minus_point],
            fixed,
            chart,
            zero_parameters.copy(),
            PRIMARY_SPHERE_RADIUS,
            1.0,
            mode_bases,
        )
        results[f"{prefix}_minus"] = minus_result
        if minus_parameters is not None and minus_result["accepted"]:
            parameters[f"{prefix}_minus"] = minus_parameters

    return parameters, results, intermediate, seed_record


def candidate_reflection_diagnostics(
    primary_results: dict[str, dict[str, object]],
) -> dict[str, object]:
    checks: dict[str, object] = {}
    all_passed = True
    for prefix in ("phi", "a"):
        plus = primary_results[f"{prefix}_plus"]
        minus = primary_results[f"{prefix}_minus"]
        plus_state = state_from_result(plus)
        minus_state = state_from_result(minus)
        if plus_state is None or minus_state is None:
            physical_error = None
            normalized_error = None
            same_sign = False
            passed = False
        else:
            reflected_difference = minus_state - REFLECTION @ plus_state
            physical_error = float(np.max(np.abs(reflected_difference)))
            normalized_error = float(
                np.max(
                    np.abs(
                        interleaved(
                            reflected_difference / COORDINATE_SCALES
                        )
                    )
                )
            )
            plus_orientation = plus.get("direct_orientation")
            minus_orientation = minus.get("direct_orientation")
            same_sign = bool(
                plus_orientation is not None
                and minus_orientation is not None
                and plus_orientation["sign"] == minus_orientation["sign"]
            )
            passed = bool(physical_error <= 2.0e-6 and same_sign)
        checks[prefix] = {
            "passed": passed,
            "physical_reflection_max_abs": physical_error,
            "normalized_reflection_max_abs": normalized_error,
            "same_declared_direct_sign": same_sign,
            "negative_endpoint_seeded_independently_from_zero": True,
        }
        all_passed = all_passed and passed
    return {"passed": all_passed, "sources": checks}


def orientation_result_passed(result: dict[str, object]) -> bool:
    direct = result.get("direct_orientation")
    root_result = result.get("assembled_root_jacobian_orientation")
    controls = result.get("orientation_controls")
    if direct is None or root_result is None or controls is None:
        return False
    overlap = controls.get("overlap_chart")
    return bool(
        result.get("accepted") is True
        and root_result["sign"] == -direct["sign"]
        and controls["reverse_Gamma_first_parameter_sign"]
        == -direct["sign"]
        and controls["reverse_K_first_parameter_sign"] == -direct["sign"]
        and controls["ambient_row_basis_sign_agrees"] is True
        and overlap is not None
        and overlap.get("passed") is True
    )


def path_result_passed(result: dict[str, object]) -> bool:
    ledger = result.get("flow_ledger")
    margins = result.get("window_margins")
    if not isinstance(ledger, dict) or not isinstance(margins, dict):
        return False
    event_distance = ledger.get("first_cap_normalized_state_distance")
    return bool(
        ledger.get("ReS_max_positive_step", np.inf) <= 5.0e-8
        and ledger.get("ImS_max_drift", np.inf) <= 5.0e-8
        and ledger.get("xi_norm_margin", -np.inf) >= 0.1
        and ledger.get("first_cap_event_status") == "FIRST_CAP_EVENT"
        and ledger.get("first_cap_radius_residual", np.inf) <= 2.0e-7
        and event_distance is not None
        and event_distance <= 5.0e-5
        and result.get("window_margins_passed") is True
    )


def json_ready(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        result = float(value)
        if not np.isfinite(result):
            raise NumericalRunError("non-finite float reached RESULT_JSON")
        return result
    if isinstance(value, (np.complexfloating, complex)):
        result = complex(value)
        if not np.isfinite(result.real) or not np.isfinite(result.imag):
            raise NumericalRunError("non-finite complex reached RESULT_JSON")
        return [float(result.real), float(result.imag)]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def production_main() -> bool:
    manifest, _raw, digest = load_manifest()
    audit = Audit()
    exact_data = exact_contracts(audit, manifest, digest)
    mode_bases = (
        np.asarray(exact_data["DST_basis"], dtype=float),
        np.asarray(exact_data["nested_basis"], dtype=float),
    )

    print("[STAGE] solving shared and independently continued signed saddle grids", flush=True)
    saddle_w, saddle_records = solve_signed_saddle_grids(
        manifest, root_tolerance=1.0e-12
    )
    fixed = build_fixed_metric(saddle_w[(0.0, 0.0)])
    saddle_data = {
        point: make_saddle_data(numeric_model(*point), value, fixed)
        for point, value in saddle_w.items()
    }
    saddle_diagnostics = saddle_grid_diagnostics(
        saddle_records, saddle_data
    )
    audit.numerical(
        "P41.saddles.two_source_signed_grids",
        bool(saddle_diagnostics["passed"]),
        "all nine independently continued two-source grid saddles are resolved, nondegenerate, inertia-matched, and reflection-paired",
        failure_status="SOURCE_SCOPED_INCONCLUSIVE",
        details=saddle_diagnostics,
    )

    print("[STAGE] computing anchor-subtracted two-source response and solver control", flush=True)
    response_primary = susceptibility_from_saddles(saddle_data)
    control_w, control_records = solve_signed_saddle_grids(
        manifest,
        root_tolerance=5.0e-10,
        zero_seed_override=saddle_w[(0.0, 0.0)],
    )
    control_data = {
        point: make_saddle_data(numeric_model(*point), value, fixed)
        for point, value in control_w.items()
    }
    control_saddle_diagnostics = saddle_grid_diagnostics(
        control_records, control_data
    )
    response_control = susceptibility_from_saddles(control_data)
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
    response_rank_contract_passed = bool(
        stable_rank_two
        and reversal_max <= 1.0e-7
        and control_saddle_diagnostics["passed"]
    )
    response_details = {
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
    }
    audit.numerical(
        "P41.response.anchor_subtracted_two_source_matrix",
        response_rank_contract_passed,
        "the reported half-step susceptibility is tested against source reversal, step drift, and the independent predeclared solver-tolerance repeat without forcing its rank",
        failure_status="STABLE_NUMERICAL_RANK_TWO_NOT_SUPPORTED",
        details=response_details,
    )

    metric_details = metric_geometry_diagnostics(fixed, saddle_data)
    audit.numerical(
        "P41.metric.one_fixed_mobility_two_sources",
        bool(metric_details["passed"]),
        "one zero-source mobility is held fixed while signed projectors, transported frames, reflection, and every lambda-one Takagi identity are checked",
        failure_status="INVALID_RUN",
        details=metric_details,
    )

    chart = build_nested_chart(manifest, saddle_data[(0.0, 0.0)], fixed)
    print("[STAGE] solving five primary full-R14 candidates", flush=True)
    (
        primary_parameters,
        primary_results,
        intermediate_results,
        seed_record,
    ) = solve_primary_intersections(
        manifest, saddle_data, fixed, chart, mode_bases
    )
    reflection_candidates = candidate_reflection_diagnostics(primary_results)
    five_accepted = bool(
        set(primary_results)
        == {"shared_zero", "phi_minus", "phi_plus", "a_minus", "a_plus"}
        and all(result.get("accepted") is True for result in primary_results.values())
        and reflection_candidates["passed"]
    )
    audit.numerical(
        "P41.intersections.five_primary_full_R14_candidates",
        five_accepted,
        "the shared, signed phi, and signed a endpoints are independently solved in all R14 equations with frozen residual, rank, transversality, reflection, and window criteria",
        failure_status="NO_ROOT_FOUND_OR_NONTRANSVERSE_IN_FROZEN_SEARCH",
        details={
            "primary_results": primary_results,
            "positive_half_step_continuations": intermediate_results,
            "candidate_reflection_controls": reflection_candidates,
            "seed_provenance": seed_record,
        },
    )

    orientation_checks = {
        label: orientation_result_passed(result)
        for label, result in primary_results.items()
    }
    orientation_passed = bool(
        all(orientation_checks.values()) and reflection_candidates["passed"]
    )
    separate_signs = {
        label: (
            None
            if result.get("direct_orientation") is None
            else result["direct_orientation"]["sign"]
        )
        for label, result in primary_results.items()
    }
    audit.numerical(
        "P41.orientation.direct_root_and_basis_controls",
        orientation_passed,
        "within m4, direct/root parity, single Gamma/K reversals, correctly row-acting DST/nested coordinate maps, and strict overlap-chart transport are audited without a desired sign",
        failure_status="INVALID_ORIENTATION_RESULT",
        details={
            "per_primary_pass": orientation_checks,
            "separately_measured_m4_signs": separate_signs,
            "phase40_phi_declared_coordinate_sign": 1,
            "m3_m4_comparison_scope": (
                "descriptive separately audited signs only; grids are "
                "nonnested and no common determinant line is constructed"
            ),
        },
    )

    print("[STAGE] running three full finite-difference tangent controls", flush=True)
    finite_difference_results: dict[str, object] = {}
    for label in ("shared_zero", "phi_plus", "a_plus"):
        result = primary_results[label]
        parameters = primary_parameters.get(label)
        if parameters is None or not result.get("accepted"):
            control: dict[str, object] = {
                "status": "TANGENT_CONTROL_FAILED",
                "passed": False,
                "message": "primary candidate unavailable",
            }
        else:
            point = (float(result["delta_a"]), float(result["delta_phi"]))
            try:
                control = finite_difference_control(
                    manifest,
                    parameters,
                    numeric_model(*point),
                    saddle_data[point],
                    fixed,
                    chart,
                    PRIMARY_SPHERE_RADIUS,
                    1.0,
                    np.asarray(
                        result["variational_scaled_root_jacobian"],
                        dtype=float,
                    ),
                    int(result["direct_orientation"]["sign"]),
                )
            except (RuntimeError, ValueError, np.linalg.LinAlgError) as error:
                control = {
                    "status": "TANGENT_CONTROL_FAILED",
                    "passed": False,
                    "message": str(error),
                }
        finite_difference_results[label] = control
        primary_results[label]["finite_difference_control"] = control
    fd_passed = all(
        bool(control.get("passed"))
        for control in finite_difference_results.values()
    )
    audit.numerical(
        "P41.tangent.three_full_FD_controls",
        fd_passed,
        "the full strict-map residual Jacobian is audited at shared_zero, phi_plus, and a_plus using the first adjacent surviving frozen FD pair",
        failure_status="TANGENT_CONTROL_FAILED",
        details=finite_difference_results,
    )

    print("[STAGE] running frozen radius and launch-shape controls", flush=True)
    radius_results: dict[str, object] = {}
    for label in ("shared_zero", "phi_plus", "a_plus"):
        result = primary_results[label]
        parameters = primary_parameters.get(label)
        if parameters is None or not result.get("accepted"):
            radius_results[label] = {
                "passed": False,
                "status": "LAUNCH_SHAPE_SENSITIVE_OR_INCONCLUSIVE",
                "message": "primary candidate unavailable",
            }
            continue
        point = (float(result["delta_a"]), float(result["delta_phi"]))
        radius_results[label] = solve_radius_controls(
            numeric_model(*point),
            saddle_data[point],
            fixed,
            chart,
            parameters,
            result,
            mode_bases,
        )
    shape_results: dict[str, object] = {}
    for label in ("phi_plus", "a_plus"):
        result = primary_results[label]
        parameters = primary_parameters.get(label)
        if parameters is None or not result.get("accepted"):
            shape_results[label] = {
                "passed": False,
                "status": "LAUNCH_SHAPE_SENSITIVE_OR_INCONCLUSIVE",
                "message": "primary candidate unavailable",
            }
            continue
        point = (float(result["delta_a"]), float(result["delta_phi"]))
        shape_results[label] = solve_shape_control(
            numeric_model(*point),
            saddle_data[point],
            fixed,
            chart,
            parameters,
            result,
            mode_bases,
        )
    launch_passed = bool(
        all(bool(value.get("passed")) for value in radius_results.values())
        and all(bool(value.get("passed")) for value in shape_results.values())
    )
    audit.numerical(
        "P41.launch.radius_and_shape_controls",
        launch_passed,
        "radius and aligned launch-shape mutations must return the same normalized cap state, not merely repeat a determinant sign",
        failure_status="LAUNCH_SHAPE_SENSITIVE_OR_INCONCLUSIVE",
        details={
            "radius_controls_including_primary_as_base": radius_results,
            "launch_shape_controls": shape_results,
            "metric_homotopy_tested": False,
        },
    )

    path_checks = {
        label: path_result_passed(result)
        for label, result in primary_results.items()
    }
    audit.numerical(
        "P41.path.first_cap_and_flow_box",
        all(path_checks.values()),
        "every primary tracked path has monotone sampled ReS, stable ImS, frozen-box margins, and an independently re-integrated matching first cap event",
        failure_status="PATH_OR_CAP_CLASSIFICATION_FAILED",
        details={
            "per_primary_pass": path_checks,
            "per_primary_ledgers": {
                label: {
                    "flow_ledger": result.get("flow_ledger"),
                    "window_margins": result.get("window_margins"),
                }
                for label, result in primary_results.items()
            },
        },
    )

    completion_ledger = dict(manifest["required_fail_closed_outputs"])
    manifest_false_keys = {
        key
        for key, value in manifest["required_fail_closed_outputs"].items()
        if isinstance(value, bool)
    }
    output_false_keys = {
        key
        for key, value in completion_ledger.items()
        if value is False
    }
    expected_null = {
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "quantum_gravity_explanation",
    }
    guard_passed = bool(
        output_false_keys == manifest_false_keys
        and all(
            completion_ledger[key] is False for key in manifest_false_keys
        )
        and all(completion_ledger[key] is None for key in expected_null)
        and completion_ledger["gate1_status"] == "OPEN_PARTIAL_PROGRESS"
    )
    audit.numerical(
        "P41.guard.no_global_integer",
        guard_passed,
        "all sixteen incomplete-data flags remain false, six promoted outputs remain null, and Gate 1 remains open",
        failure_status="INVALID_RUN",
        details=completion_ledger,
    )

    invalid_run = any(
        record["status"] == "INVALID_RUN" for record in audit.numerical_records
    )
    phi_scoped = bool(
        not invalid_run
        and saddle_diagnostics["passed"]
        and metric_details["passed"]
        and all(
            primary_results[label].get("accepted")
            and orientation_checks[label]
            and path_checks[label]
            for label in ("shared_zero", "phi_minus", "phi_plus")
        )
        and reflection_candidates["sources"]["phi"]["passed"]
        and finite_difference_results["shared_zero"].get("passed")
        and finite_difference_results["phi_plus"].get("passed")
        and radius_results["shared_zero"].get("passed")
        and radius_results["phi_plus"].get("passed")
        and shape_results["phi_plus"].get("passed")
    )
    a_scoped = bool(
        not invalid_run
        and saddle_diagnostics["passed"]
        and metric_details["passed"]
        and all(
            primary_results[label].get("accepted")
            and orientation_checks[label]
            and path_checks[label]
            for label in ("shared_zero", "a_minus", "a_plus")
        )
        and reflection_candidates["sources"]["a"]["passed"]
        and finite_difference_results["shared_zero"].get("passed")
        and finite_difference_results["a_plus"].get("passed")
        and radius_results["shared_zero"].get("passed")
        and radius_results["a_plus"].get("passed")
        and shape_results["a_plus"].get("passed")
    )
    rank_scoped = bool(
        not invalid_run
        and saddle_diagnostics["passed"]
        and response_rank_contract_passed
    )
    output = {
        "phase": 41,
        "gate": 1,
        "run_status": "INVALID_RUN" if invalid_run else "VALID_TYPED_RUN",
        "calculation": "m=4 two-source finite local joint-intersection production audit",
        "input_manifest": {
            "path": str(INPUT_PATH),
            "sha256": digest,
            "introduced_in_commit": INPUT_COMMIT,
            "freeze_kind": manifest["freeze_kind"],
            "is_preregistration": manifest["is_preregistration"],
            "is_scientific_evidence": manifest["is_scientific_evidence"],
            "pre_freeze_R14_sign": "UNKNOWN_NOT_RETAINED",
        },
        "completion_contract_counts": {
            "exact_total": len(audit.exact_records),
            "exact_passed": audit.exact_passed,
            "numerical_total": len(audit.numerical_records),
            "numerical_passed": audit.numerical_passed,
        },
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "model": {
            "segment_count": SEGMENT_COUNT,
            "complex_dimension": COMPLEX_DIMENSION,
            "ambient_real_dimension": AMBIENT_REAL_DIMENSION,
            "source_dimension": 2,
            "fixed_mobility": True,
            "source_rewhitening": False,
        },
        "saddles": {
            point_label(point): {
                **record,
                "fixed_metric_Hxi_eigenvalues": saddle_data[
                    point
                ].hessian_xi_eigenvalues,
                "signed_subspace_min_principal_overlap": saddle_data[
                    point
                ].signed_subspace_min_principal_overlap,
            }
            for point, record in saddle_records.items()
        },
        "response": response_details,
        "fixed_metric_and_launch": metric_details,
        "upward_chart": chart.provenance,
        "primary_local_candidates": primary_results,
        "positive_half_step_continuation_candidates": intermediate_results,
        "candidate_reflection_controls": reflection_candidates,
        "finite_difference_controls": finite_difference_results,
        "radius_controls": radius_results,
        "launch_shape_controls": shape_results,
        "completion_ledger": completion_ledger,
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "cutoff_limit": None,
        "continuum_limit": None,
        "quantum_gravity_explanation": None,
        "claim_status": {
            "phi_only_local_m4_robustness": (
                "SUPPORTED_WITHIN_FROZEN_LOCAL_PROTOCOL"
                if phi_scoped
                else "INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL"
            ),
            "a_only_local_m4_robustness": (
                "SUPPORTED_WITHIN_FROZEN_LOCAL_PROTOCOL"
                if a_scoped
                else "INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL"
            ),
            "two_source_stable_numerical_rank": (
                "RANK_TWO_SUPPORTED_WITHIN_FROZEN_NORMALIZATION"
                if rank_scoped
                else "STABLE_NUMERICAL_RANK_TWO_NOT_SUPPORTED"
            ),
            "exact_algebraic_response_rank": "NOT_PROVED",
            "m3_m4_sign_relation": (
                "DESCRIPTIVE_SEPARATELY_AUDITED_COMPARISON_ONLY"
            ),
            "common_cross_cutoff_determinant_line": "NOT_CONSTRUCTED",
            "global_Picard_Lefschetz_promotion": "PROHIBITED",
            "Gate_1": "OPEN_PARTIAL_PROGRESS",
            "SUSY_quantum_gravity_or_cosmology_claim": "NOT_LICENSED",
        },
        "scope_guard": {
            "computed": [
                "one explicit four-segment midpoint configuration action",
                "two independent signed endpoint-source saddle grids",
                "one fixed zero-source Hermitian mobility",
                "finite-radius finite-time local full-R14 cap candidates in one frozen chart",
                "local orientation, tangent, radius, shape, and path controls",
            ],
            "not_computed": [
                "straight arms or later cap reintersections",
                "continuous direction coverage or root exhaustion",
                "complete nonlinear upward manifolds or saddle census",
                "Stokes chamber, connecting flows, or all relative good ends",
                "a derived physical original cycle or global intersection integer",
                "cross-cutoff determinant line, cutoff limit, or continuum limit",
                "BFV ghosts, Pfaffian/Pin line, fermions, gravitino, or spinorial charge",
                "quantum gravity, SUSY breaking, cosmological prediction, or particle poles",
            ],
        },
        "next_calculation": (
            "complete the original chain, direction/root census, Stokes and "
            "relative-end data before any Gate-1 global coefficient"
        ),
    }
    ready = json_ready(output)
    print("RESULT_JSON=" + json.dumps(ready, sort_keys=True))
    print(
        f"Completed {audit.exact_passed}/7 exact and "
        f"{audit.numerical_passed}/9 numerical contracts; "
        f"Gate 1 remains OPEN_PARTIAL_PROGRESS.",
        flush=True,
    )
    return not invalid_run


def emit_typed_numerical_failure(error: Exception) -> None:
    """Emit every frozen numerical slot when a stage cannot be completed.

    No alternate seed, chart, source path, or desired result is introduced.
    This emergency path is deliberately conservative: even work completed
    before the exception is not promoted without the rest of the production
    ledger.  Exact/hash failures remain hard errors and never enter here.
    """

    manifest, _raw, digest = load_manifest()
    audit = Audit()
    exact_contracts(audit, manifest, digest)
    failure_summary = {
        "exception_type": type(error).__name__,
        "exception_message": str(error)[:2000],
        "fallback_seed_or_chart_used": False,
        "partial_numerical_results_promoted": False,
    }
    for contract in manifest["completion_contracts"]["numerical"]:
        audit.numerical(
            str(contract["id"]),
            False,
            "the production numerical ledger could not be completed; this slot is conservatively fail-closed without a replacement input",
            failure_status=str(contract["failure_status"]),
            details=failure_summary,
        )
    completion = dict(manifest["required_fail_closed_outputs"])
    output = {
        "phase": 41,
        "gate": 1,
        "run_status": "INVALID_RUN_INCOMPLETE_NUMERICAL_STAGE",
        "calculation": "m=4 two-source finite local joint-intersection production audit",
        "input_manifest": {
            "path": str(INPUT_PATH),
            "sha256": digest,
            "introduced_in_commit": INPUT_COMMIT,
            "freeze_kind": manifest["freeze_kind"],
        },
        "terminal_numerical_failure": failure_summary,
        "completion_contract_counts": {
            "exact_total": len(audit.exact_records),
            "exact_passed": audit.exact_passed,
            "numerical_total": len(audit.numerical_records),
            "numerical_passed": audit.numerical_passed,
        },
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "model": None,
        "saddles": {},
        "response": None,
        "fixed_metric_and_launch": None,
        "upward_chart": None,
        "primary_local_candidates": {},
        "positive_half_step_continuation_candidates": {},
        "candidate_reflection_controls": None,
        "finite_difference_controls": {},
        "radius_controls": {},
        "launch_shape_controls": {},
        "completion_ledger": completion,
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "cutoff_limit": None,
        "continuum_limit": None,
        "quantum_gravity_explanation": None,
        "claim_status": {
            "phi_only_local_m4_robustness": "INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL",
            "a_only_local_m4_robustness": "INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL",
            "two_source_stable_numerical_rank": "INCONCLUSIVE_IN_INCOMPLETE_RUN",
            "exact_algebraic_response_rank": "NOT_PROVED",
            "m3_m4_sign_relation": (
                "NOT_CLASSIFIED_IN_INCOMPLETE_RUN"
            ),
            "common_cross_cutoff_determinant_line": "NOT_CONSTRUCTED",
            "global_Picard_Lefschetz_promotion": "PROHIBITED",
            "Gate_1": "OPEN_PARTIAL_PROGRESS",
            "SUSY_quantum_gravity_or_cosmology_claim": "NOT_LICENSED",
        },
    }
    print("RESULT_JSON=" + json.dumps(json_ready(output), sort_keys=True))
    print(
        "Completed a typed INVALID_RUN fallback with 7 exact and 9 "
        "fail-closed numerical contract records; Gate 1 remains open.",
        flush=True,
    )


def main() -> None:
    try:
        run_is_valid = production_main()
        if not run_is_valid:
            raise SystemExit(2)
    except ExactContractError:
        raise
    except Exception as error:
        emit_typed_numerical_failure(error)
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
