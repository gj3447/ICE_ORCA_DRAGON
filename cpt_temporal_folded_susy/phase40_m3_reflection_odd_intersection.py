#!/usr/bin/env python3
"""Phase 40 -- m=3 reflection-odd local joint-intersection audit.

This executable adds the first reflection-odd history sector to the Phase-39
configuration-space pilot.  It freezes one three-segment midpoint action,
holds the delta=0 Hermitian flow metric fixed, applies the signed endpoint
probe

    phi_L = phi_b - delta/2,  phi_R = phi_b + delta/2,

and transports one local five-real-dimensional upward-chart patch to the
declared r=.3 cap piece.  The requested local orientation is computed from
the full ten-real-dimensional matrix

    sign det_R[V_Gamma, V_K].

The calculation is deliberately local.  It does not search the straight
arms, later cap reintersections, every saddle or upward component, or a
non-Stokes lateral chamber.  The bounded-chain sum, complete global signed
vector, and global_n_sigma therefore remain null.  The script writes no
files.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Callable

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root


INPUT_PATH = Path(__file__).with_name(
    "PHASE40_M3_REFLECTION_ODD_INTERSECTION_INPUTS.json"
)
INPUT_SHA256 = "60dfc9c31e45408c92b5fbcd1e1487bcd53b02a62ccf4ee71272f7c3dcc382ae"
INPUT_INITIAL_FREEZE_SHA256 = (
    "897c9788cf1b2706ddf6e2c75f56f4ac7da1eb0aea64ea01cb31971a35920426"
)
INPUT_INITIAL_FREEZE_COMMIT = "dd2a9d54b386dcc7bb090f446d5d32aad59743e7"
INPUT_AMENDED_IN_COMMIT = "a6b369e0a9518cd491f8116204ec67ab36fdf2a1"

SEGMENT_COUNT = 3
COMPLEX_DIMENSION = 5
AMBIENT_REAL_DIMENSION = 10
BASE_A = 3.5668031935672753
BASE_PHI = 1.0185809464006637
TIME_SCALE = 0.7
COORDINATE_SCALES = np.array(
    [BASE_A, BASE_PHI, BASE_A, BASE_PHI, TIME_SCALE], dtype=float
)
REFLECTION = np.array(
    [
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
    ],
    dtype=float,
)
DELTA_GRID = (-0.001, -0.0005, 0.0, 0.0005, 0.001)
PRIMARY_DELTAS = (-0.001, 0.0, 0.001)
CAP_RADIUS = 0.3
PRIMARY_SPHERE_RADIUS = 1.0e-4
CONTROL_SPHERE_RADII = (5.0e-5, 2.0e-4)
FLOW_TIME_MAX = 13.5
FLOW_NORM_MAX = 40.0
FIELD_WINDOW = 0.25
INTERSECTION_TOLERANCE = 2.0e-7
TRANSVERSALITY_MINIMUM = 2.0e-4


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

    def _unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"duplicate check id: {check_id}")

    def exact(self, check_id: str, condition: bool, statement: str) -> None:
        self._unique(check_id)
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[PASS] {check_id}: {statement}")

    def numerical(
        self, check_id: str, condition: bool, statement: str
    ) -> None:
        self._unique(check_id)
        if not condition:
            raise AssertionError(f"[NUMERIC FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")


@dataclass(frozen=True)
class SymbolicFamily:
    variables_z: tuple[sp.Symbol, ...]
    variables_w: tuple[sp.Symbol, ...]
    delta: sp.Symbol
    action_z: sp.Expr
    action_w: sp.Expr
    gradient_w: sp.Matrix
    hessian_w: sp.Matrix
    elements: tuple[sp.Expr, ...]


@dataclass(frozen=True)
class NumericModel:
    delta: float
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


@dataclass(frozen=True)
class SaddleData:
    delta: float
    saddle_w: np.ndarray
    saddle_z: np.ndarray
    action: complex
    gradient_max_abs: float
    hessian_w: np.ndarray
    hessian_eigenvalues: np.ndarray
    hessian_inertia: tuple[int, int, int]
    hessian_xi_eigenvalues: np.ndarray
    aligned_signed_subspace_frame_xi: np.ndarray
    launch_matrix_xi: np.ndarray
    signed_subspace_min_principal_overlap: float


def load_manifest() -> tuple[dict[str, object], bytes, str]:
    raw = INPUT_PATH.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    return json.loads(raw), raw, digest


@lru_cache(maxsize=1)
def build_symbolic_family() -> SymbolicFamily:
    a_1, phi_1, a_2, phi_2, proper_time = sp.symbols(
        "a_1 phi_1 a_2 phi_2 T"
    )
    w_variables = sp.symbols("w_a1 w_phi1 w_a2 w_phi2 w_T")
    delta = sp.symbols("delta", real=True)
    a_boundary, phi_boundary = sp.symbols(
        "a_boundary phi_boundary", real=True
    )
    step = sp.Rational(1, SEGMENT_COUNT)
    slope = sp.sqrt(sp.Rational(2, 3))

    def potential(phi: sp.Expr) -> sp.Expr:
        return sp.Rational(3, 4) * (1 - sp.exp(-slope * phi)) ** 2

    def element(
        left_a: sp.Expr,
        left_phi: sp.Expr,
        right_a: sp.Expr,
        right_phi: sp.Expr,
    ) -> sp.Expr:
        midpoint_a = (left_a + right_a) / 2
        midpoint_phi = (left_phi + right_phi) / 2
        delta_a = right_a - left_a
        delta_phi = right_phi - left_phi
        return 2 * sp.pi**2 * (
            (
                -6 * midpoint_a * delta_a**2
                + midpoint_a**3 * delta_phi**2
            )
            / (2 * proper_time * step)
            + proper_time
            * step
            * (
                -3 * midpoint_a
                + midpoint_a**3 * potential(midpoint_phi)
            )
        )

    left_phi = phi_boundary - delta / 2
    right_phi = phi_boundary + delta / 2
    elements = (
        element(a_boundary, left_phi, a_1, phi_1),
        element(a_1, phi_1, a_2, phi_2),
        element(a_2, phi_2, a_boundary, right_phi),
    )
    action_z = sp.expand(sum(elements))
    substitutions = {
        a_boundary: sp.Float(str(BASE_A), 50),
        phi_boundary: sp.Float(str(BASE_PHI), 50),
        a_1: sp.Float(str(BASE_A), 50) * w_variables[0],
        phi_1: sp.Float(str(BASE_PHI), 50) * w_variables[1],
        a_2: sp.Float(str(BASE_A), 50) * w_variables[2],
        phi_2: sp.Float(str(BASE_PHI), 50) * w_variables[3],
        proper_time: sp.Float(str(TIME_SCALE), 50) * w_variables[4],
    }
    action_w = action_z.subs(substitutions)
    gradient_w = sp.Matrix(
        [sp.diff(action_w, variable) for variable in w_variables]
    )
    hessian_w = sp.hessian(action_w, w_variables)
    return SymbolicFamily(
        variables_z=(a_1, phi_1, a_2, phi_2, proper_time),
        variables_w=w_variables,
        delta=delta,
        action_z=action_z,
        action_w=action_w,
        gradient_w=gradient_w,
        hessian_w=hessian_w,
        elements=elements,
    )


@lru_cache(maxsize=None)
def numeric_model(delta_value: float) -> NumericModel:
    family = build_symbolic_family()
    value = sp.Float(str(delta_value), 50)
    action = family.action_w.subs(family.delta, value)
    gradient = family.gradient_w.subs(family.delta, value)
    hessian = family.hessian_w.subs(family.delta, value)
    return NumericModel(
        delta=delta_value,
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
    model: NumericModel, seed_w: np.ndarray
) -> tuple[np.ndarray, dict[str, object]]:
    solution = root(
        lambda value: gradient_at(model, value).real,
        seed_w,
        jac=lambda value: hessian_at(model, value).real,
        method="hybr",
        options={"xtol": 1.0e-12},
    )
    if not solution.success:
        raise RuntimeError(
            f"delta={model.delta} saddle solve failed: {solution.message}"
        )
    high_precision = sp.nsolve(
        tuple(model.gradient_expr),
        build_symbolic_family().variables_w,
        tuple(float(value) for value in solution.x),
        tol=sp.Float("1e-48"),
        maxsteps=100,
        prec=70,
    )
    saddle_w = np.array([float(value) for value in high_precision])
    hessian = hessian_at(model, saddle_w).real
    eigenvalues = np.linalg.eigvalsh(hessian)
    action = action_at(model, saddle_w)
    gradient = gradient_at(model, saddle_w)
    return saddle_w, {
        "delta": model.delta,
        "saddle_z": (COORDINATE_SCALES * saddle_w).tolist(),
        "action": [action.real, action.imag],
        "gradient_max_abs": float(np.max(np.abs(gradient))),
        "hessian_eigenvalues": eigenvalues.tolist(),
        "hessian_inertia": {
            "negative": int(np.count_nonzero(eigenvalues < 0.0)),
            "positive": int(np.count_nonzero(eigenvalues > 0.0)),
            "zero": int(np.count_nonzero(np.abs(eigenvalues) <= 1.0e-9)),
        },
    }


def build_fixed_metric(saddle_zero_w: np.ndarray) -> FixedMetric:
    hessian = hessian_at(numeric_model(0.0), saddle_zero_w).real
    eigenvalues, eigenvectors = deterministic_oriented_eigenframe(hessian)
    linear_map = eigenvectors @ np.diag(
        1.0 / np.sqrt(np.abs(eigenvalues))
    )
    return FixedMetric(
        saddle_zero_w=saddle_zero_w,
        hessian_zero_w=hessian,
        eigenvalues_zero=eigenvalues,
        oriented_eigenvectors_zero=eigenvectors,
        linear_map=linear_map,
        inverse_metric_mobility_w=linear_map @ linear_map.T,
    )


def aligned_signed_takagi_frame(
    hessian_xi: np.ndarray, base_signs: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Return a gauge-fixed signed-subspace frame and its Takagi launch.

    Exact Morse whitening makes each sign block at delta=0 internally
    degenerate.  Individual eigenvectors are therefore not invariant there.
    We instead align each positive/negative spectral *subspace* to its frozen
    coordinate subspace by orthogonal Procrustes transport.  The matrix
    inverse square root inside that aligned subspace supplies the Morse
    normalization without reintroducing an arbitrary eigenvector gauge.
    """
    raw_values, raw_vectors = np.linalg.eigh(hessian_xi)
    aligned_frame = np.zeros_like(raw_vectors)
    launch_frame = np.zeros_like(raw_vectors, dtype=np.complex128)
    principal_overlaps: list[float] = []
    for sign in (-1, 1):
        targets = np.flatnonzero(base_signs == sign)
        sources = np.flatnonzero(np.sign(raw_values) == sign)
        if targets.size != sources.size:
            raise RuntimeError("Hessian inertia changed in the signed mutation")
        spectral_frame = raw_vectors[:, sources]
        reference_frame = np.eye(COMPLEX_DIMENSION)[:, targets]
        left, singular_values, right_transpose = np.linalg.svd(
            spectral_frame.T @ reference_frame
        )
        aligned = spectral_frame @ (left @ right_transpose)
        aligned_frame[:, targets] = aligned
        principal_overlaps.extend(singular_values.tolist())

        signed_restriction = sign * (
            aligned.T @ hessian_xi @ aligned
        )
        restriction_values, restriction_vectors = np.linalg.eigh(
            signed_restriction
        )
        if np.min(restriction_values) <= 0.0:
            raise RuntimeError("signed Hessian restriction is not positive")
        inverse_square_root = (
            restriction_vectors
            @ np.diag(1.0 / np.sqrt(restriction_values))
            @ restriction_vectors.T
        )
        phase = -1.0 + 0.0j if sign < 0 else 0.0 + 1.0j
        launch_frame[:, targets] = phase * aligned @ inverse_square_root

    if np.linalg.det(aligned_frame) <= 0.0:
        raise RuntimeError("aligned signed-subspace frame lost orientation")
    return (
        raw_values,
        aligned_frame,
        launch_frame,
        min(principal_overlaps),
    )


def make_saddle_data(
    model: NumericModel,
    saddle_w: np.ndarray,
    fixed: FixedMetric,
) -> SaddleData:
    hessian_w = hessian_at(model, saddle_w).real
    hessian_values = np.linalg.eigvalsh(hessian_w)
    base_signs = np.sign(fixed.eigenvalues_zero).astype(int)
    hessian_xi = fixed.linear_map.T @ hessian_w @ fixed.linear_map
    if model.delta == 0.0:
        xi_values = base_signs.astype(float)
        xi_vectors = np.eye(COMPLEX_DIMENSION)
        phases = np.diag(
            [
                (-1.0 + 0.0j) if value < 0.0 else 1.0j
                for value in xi_values
            ]
        )
        launch_matrix = phases
        match_overlap = 1.0
    else:
        (
            xi_values,
            xi_vectors,
            launch_matrix,
            match_overlap,
        ) = aligned_signed_takagi_frame(
            hessian_xi,
            base_signs,
        )
    action = action_at(model, saddle_w)
    return SaddleData(
        delta=model.delta,
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
        hessian_xi_eigenvalues=xi_values,
        aligned_signed_subspace_frame_xi=xi_vectors,
        launch_matrix_xi=launch_matrix,
        signed_subspace_min_principal_overlap=match_overlap,
    )


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
    if np.any(norms == 0.0):
        raise RuntimeError("zero tangent column")
    return matrix / norms, norms


def matrix_orientation(matrix: np.ndarray) -> dict[str, object]:
    normalized, norms = normalize_columns(matrix)
    sign, log_abs = np.linalg.slogdet(normalized)
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    return {
        "sign": int(np.sign(sign)),
        "log_abs_normalized_determinant": float(log_abs),
        "normalized_singular_values": singular_values.tolist(),
        "normalized_sigma_min": float(singular_values[-1]),
        "normalized_condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
        "column_norms": norms.tolist(),
    }


def oriented_chart() -> tuple[np.ndarray, np.ndarray, float]:
    center = np.array(
        [0.0, -0.25249094, 0.96759926, 0.0, 0.0], dtype=float
    )
    center /= np.linalg.norm(center)
    tangent = np.column_stack(
        [
            np.array([1.0, 0.0, 0.0, 0.0, 0.0]),
            np.array([0.0, -center[2], center[1], 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 0.0, 1.0]),
        ]
    )
    determinant = float(np.linalg.det(np.column_stack([tangent, center])))
    if determinant < 0.0:
        tangent[:, -1] *= -1.0
        determinant *= -1.0
    return center, tangent, determinant


CHART_CENTER, CHART_TANGENT, CHART_ORIENTATION = oriented_chart()


def chart_direction(parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vector = CHART_CENTER + CHART_TANGENT @ parameters
    norm = np.linalg.norm(vector)
    omega = vector / norm
    derivative = (
        (np.eye(COMPLEX_DIMENSION) - np.outer(omega, omega))
        @ CHART_TANGENT
        / norm
    )
    return omega, derivative


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
    chart_parameters: np.ndarray,
    flow_time: float,
    sphere_radius: float,
    *,
    with_tangent: bool,
    method: str,
) -> tuple[np.ndarray, np.ndarray | None]:
    omega, derivative = chart_direction(chart_parameters)
    initial_xi = sphere_radius * (saddle.launch_matrix_xi @ omega)
    if not with_tangent:
        solution = solve_ivp(
            lambda _time, xi: flow_xi(model, saddle, fixed, xi),
            (0.0, flow_time),
            initial_xi,
            method=method,
            rtol=2.0e-9 if method == "BDF" else 2.0e-12,
            atol=2.0e-11 if method == "BDF" else 2.0e-14,
            max_step=0.03 if method == "BDF" else 0.02,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        if np.max(np.linalg.norm(solution.y, axis=0)) >= FLOW_NORM_MAX:
            raise RuntimeError("trajectory exceeded the frozen xi-norm cap")
        final_xi = solution.y[:, -1]
        return (
            COORDINATE_SCALES * xi_to_w(saddle, fixed, final_xi),
            None,
        )

    tangent_initial = sphere_radius * (
        saddle.launch_matrix_xi @ derivative
    )
    augmented_initial = np.concatenate(
        [initial_xi, tangent_initial.reshape(-1)]
    )

    def right_hand_side(_time: float, augmented: np.ndarray) -> np.ndarray:
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
        right_hand_side,
        (0.0, flow_time),
        augmented_initial,
        method=method,
        rtol=2.0e-8 if method == "BDF" else 8.0e-11,
        atol=2.0e-10 if method == "BDF" else 8.0e-13,
        max_step=0.03 if method == "BDF" else 0.025,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    if (
        np.max(
            np.linalg.norm(solution.y[:COMPLEX_DIMENSION], axis=0)
        )
        >= FLOW_NORM_MAX
    ):
        raise RuntimeError("trajectory exceeded the frozen xi-norm cap")
    final = solution.y[:, -1]
    final_xi = final[:COMPLEX_DIMENSION]
    tangent_xi = final[COMPLEX_DIMENSION:].reshape(
        COMPLEX_DIMENSION, COMPLEX_DIMENSION - 1
    )
    linear_z = np.diag(COORDINATE_SCALES) @ fixed.linear_map
    state_z = COORDINATE_SCALES * xi_to_w(saddle, fixed, final_xi)
    tangent_z = linear_z @ tangent_xi
    flow_tangent_z = linear_z @ flow_xi(
        model, saddle, fixed, final_xi
    )
    return state_z, np.column_stack([tangent_z, flow_tangent_z])


def anchor(delta_value: float) -> np.ndarray:
    return np.array(
        [
            BASE_A,
            BASE_PHI - delta_value / 6.0,
            BASE_A,
            BASE_PHI + delta_value / 6.0,
        ]
    )


def gamma_cap(
    delta_value: float, y_values: np.ndarray, psi: float
) -> tuple[np.ndarray, np.ndarray]:
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    phases = np.array(
        [phase_a, phase_phi, phase_a, phase_phi], dtype=np.complex128
    )
    state = np.concatenate(
        [
            anchor(delta_value) + phases * y_values,
            [CAP_RADIUS * np.exp(1.0j * psi)],
        ]
    )
    tangent = np.zeros(
        (COMPLEX_DIMENSION, COMPLEX_DIMENSION), dtype=np.complex128
    )
    tangent[:4, :4] = np.diag(phases)
    tangent[:4, 4] = 0.5j * phases * y_values
    tangent[4, 4] = 1.0j * state[4]
    return state, tangent


def residual_and_variational_jacobian(
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    sphere_radius: float,
    method: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    gamma_state, gamma_tangent = gamma_cap(
        model.delta, parameters[:4], parameters[4]
    )
    k_state, k_tangent = integrate_chart(
        model,
        saddle,
        fixed,
        parameters[5:9],
        parameters[9],
        sphere_radius,
        with_tangent=True,
        method=method,
    )
    if k_tangent is None:
        raise AssertionError("tangent integration unexpectedly omitted")
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
    )


def state_only_residual(
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    sphere_radius: float,
) -> np.ndarray:
    gamma_state = gamma_cap(
        model.delta, parameters[:4], parameters[4]
    )[0]
    k_state = integrate_chart(
        model,
        saddle,
        fixed,
        parameters[5:9],
        parameters[9],
        sphere_radius,
        with_tangent=False,
        method="DOP853",
    )[0]
    return interleaved(
        (gamma_state - k_state) / COORDINATE_SCALES
    )


def independent_finite_difference_jacobian(
    parameters: np.ndarray,
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    sphere_radius: float,
) -> tuple[np.ndarray, list[float], list[float]]:
    proposed = (
        (2.0e-6, 5.0e-7),
        (2.0e-6, 5.0e-7),
        (2.0e-6, 5.0e-7),
        (2.0e-6, 5.0e-7),
        (2.0e-6, 5.0e-7),
        (2.0e-5, 1.0e-5),
        (2.0e-6, 5.0e-7, 1.0e-7),
        (2.0e-6, 5.0e-7, 1.0e-7),
        (2.0e-6, 5.0e-7, 1.0e-7),
        (5.0e-6, 1.0e-6, 2.0e-7),
    )
    columns: list[np.ndarray] = []
    steps: list[float] = []
    ladder_relative_differences: list[float] = []
    for index, candidate_steps in enumerate(proposed):
        candidate_columns: list[np.ndarray] = []
        surviving_steps: list[float] = []
        for step in candidate_steps:
            plus = parameters.copy()
            minus = parameters.copy()
            plus[index] += step
            minus[index] -= step
            try:
                column = (
                    state_only_residual(
                        plus, model, saddle, fixed, sphere_radius
                    )
                    - state_only_residual(
                        minus, model, saddle, fixed, sphere_radius
                    )
                ) / (2.0 * step)
            except RuntimeError:
                continue
            candidate_columns.append(column)
            surviving_steps.append(step)
            if len(candidate_columns) == 2:
                break
        if len(candidate_columns) < 2:
            raise RuntimeError(
                "fewer than two finite-difference steps survived for "
                f"parameter {index}"
            )
        columns.append(candidate_columns[0])
        steps.append(surviving_steps[0])
        ladder_relative_differences.append(
            float(
                np.linalg.norm(candidate_columns[0] - candidate_columns[1])
                / max(np.linalg.norm(candidate_columns[0]), 1.0e-30)
            )
        )
    return np.column_stack(columns), steps, ladder_relative_differences


def flow_ledger(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    parameters: np.ndarray,
    sphere_radius: float,
) -> dict[str, float | int]:
    omega = chart_direction(parameters[5:9])[0]
    initial = sphere_radius * (saddle.launch_matrix_xi @ omega)
    times = np.linspace(0.0, float(parameters[9]), 81)
    solution = solve_ivp(
        lambda _time, xi: flow_xi(model, saddle, fixed, xi),
        (0.0, float(parameters[9])),
        initial,
        t_eval=times,
        method="DOP853",
        rtol=1.0e-9,
        atol=1.0e-11,
        max_step=0.03,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    actions = np.array(
        [
            action_at(model, xi_to_w(saddle, fixed, solution.y[:, index]))
            for index in range(solution.y.shape[1])
        ]
    )
    states_z = np.array(
        [
            COORDINATE_SCALES
            * xi_to_w(saddle, fixed, solution.y[:, index])
            for index in range(solution.y.shape[1])
        ]
    )
    lapse_moduli = np.abs(states_z[:, -1])
    xi_norms = np.linalg.norm(solution.y, axis=0)
    return {
        "sample_count": int(times.size),
        "ReS_start": float(actions.real[0]),
        "ReS_end": float(actions.real[-1]),
        "ReS_max_positive_step": float(np.max(np.diff(actions.real))),
        "ImS_max_drift": float(
            np.max(np.abs(actions.imag - actions.imag[0]))
        ),
        "xi_norm_max": float(np.max(xi_norms)),
        "prior_sample_min_abs_T": float(np.min(lapse_moduli[:-1])),
        "end_abs_T": float(lapse_moduli[-1]),
        "sampled_no_prior_cap_crossing": bool(
            np.min(lapse_moduli[:-1]) > CAP_RADIUS
            and abs(lapse_moduli[-1] - CAP_RADIUS) < 2.0e-7
        ),
    }


def initial_intersection_parameters() -> np.ndarray:
    return np.array(
        [
            0.0,
            -0.0007806956058995507,
            0.0,
            -0.0007806956058995507,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            10.341404004084012,
        ]
    )


def solve_intersection(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    initial: np.ndarray,
    sphere_radius: float,
    *,
    compute_fd: bool,
) -> tuple[np.ndarray, dict[str, object]]:
    lower = np.array(
        [-FIELD_WINDOW] * 4
        + [-1.4]
        + [-0.6] * 4
        + [max(7.0, float(initial[9]) - 2.0)]
    )
    upper = np.array(
        [FIELD_WINDOW] * 4
        + [1.4]
        + [0.6] * 4
        + [min(FLOW_TIME_MAX, float(initial[9]) + 2.0)]
    )

    coarse_cache: dict[str, object] = {}

    def coarse_evaluation(parameters: np.ndarray) -> tuple[np.ndarray, ...]:
        cached_parameters = coarse_cache.get("parameters")
        if cached_parameters is None or not np.array_equal(
            parameters, cached_parameters
        ):
            coarse_cache["parameters"] = parameters.copy()
            coarse_cache["evaluation"] = residual_and_variational_jacobian(
                parameters,
                model,
                saddle,
                fixed,
                sphere_radius,
                "BDF",
            )
        return coarse_cache["evaluation"]  # type: ignore[return-value]

    coarse_solution = least_squares(
        lambda parameters: coarse_evaluation(parameters)[0],
        initial,
        jac=lambda parameters: coarse_evaluation(parameters)[1],
        bounds=(lower, upper),
        x_scale="jac",
        ftol=2.0e-11,
        xtol=2.0e-11,
        gtol=2.0e-11,
        max_nfev=60,
    )
    accurate_cache: dict[str, object] = {}

    def accurate_evaluation(
        parameters: np.ndarray,
    ) -> tuple[np.ndarray, ...]:
        cached_parameters = accurate_cache.get("parameters")
        if cached_parameters is None or not np.array_equal(
            parameters, cached_parameters
        ):
            accurate_cache["parameters"] = parameters.copy()
            accurate_cache["evaluation"] = (
                residual_and_variational_jacobian(
                    parameters,
                    model,
                    saddle,
                    fixed,
                    sphere_radius,
                    "DOP853",
                )
            )
        return accurate_cache["evaluation"]  # type: ignore[return-value]

    parameters = coarse_solution.x.copy()
    accurate_newton_history: list[dict[str, float]] = []
    accurate_refinement_success = False
    for _iteration in range(4):
        accurate_residual, accurate_jacobian = accurate_evaluation(
            parameters
        )[:2]
        residual_max = float(np.max(np.abs(accurate_residual)))
        accurate_newton_history.append(
            {
                "scaled_residual_max_abs": residual_max,
                "jacobian_condition_number": float(
                    np.linalg.cond(accurate_jacobian)
                ),
            }
        )
        if residual_max < 2.0e-8:
            accurate_refinement_success = True
            break
        correction = np.linalg.solve(
            accurate_jacobian, -accurate_residual
        )
        proposed_parameters = parameters + correction
        if np.any(proposed_parameters <= lower) or np.any(
            proposed_parameters >= upper
        ):
            raise RuntimeError(
                "accurate DOP853 Newton correction left the frozen chart box"
            )
        parameters = proposed_parameters
    (
        scaled_residual,
        dop_jacobian,
        gamma_state,
        k_state,
        gamma_frame,
        k_frame,
    ) = accurate_evaluation(parameters)
    joined = np.column_stack([gamma_frame, k_frame])
    direct_orientation = matrix_orientation(joined)
    root_orientation = matrix_orientation(
        np.column_stack([gamma_frame, -k_frame])
    )
    independent_fd = None
    finite_difference_steps = None
    finite_difference_ladder_relative_differences = None
    fd_orientation = None
    fd_relative_error = None
    if compute_fd:
        (
            independent_fd,
            finite_difference_steps,
            finite_difference_ladder_relative_differences,
        ) = (
            independent_finite_difference_jacobian(
                parameters, model, saddle, fixed, sphere_radius
            )
        )
        fd_orientation = matrix_orientation(independent_fd)
        fd_relative_error = float(
            np.linalg.norm(independent_fd - dop_jacobian, ord=2)
            / np.linalg.norm(dop_jacobian, ord=2)
        )
    reversed_gamma = matrix_orientation(
        np.column_stack(
            [gamma_frame @ np.diag([-1.0, 1.0, 1.0, 1.0, 1.0]), k_frame]
        )
    )
    reversed_k = matrix_orientation(
        np.column_stack(
            [gamma_frame, k_frame @ np.diag([-1.0, 1.0, 1.0, 1.0, 1.0])]
        )
    )
    ledger = flow_ledger(model, saddle, fixed, parameters, sphere_radius)
    physical_residual = interleaved(gamma_state - k_state)
    result: dict[str, object] = {
        "delta": model.delta,
        "cap_radius": CAP_RADIUS,
        "sphere_radius": sphere_radius,
        "least_squares_success": bool(
            coarse_solution.success and accurate_refinement_success
        ),
        "least_squares_message": {
            "coarse_BDF": str(coarse_solution.message),
            "refined_DOP853": (
                "strict-map Newton residual target reached"
                if accurate_refinement_success
                else "strict-map Newton residual target not reached"
            ),
        },
        "least_squares_nfev": {
            "coarse_BDF": int(coarse_solution.nfev),
            "refined_DOP853": len(accurate_newton_history),
        },
        "accurate_DOP853_Newton_history": accurate_newton_history,
        "parameters": parameters.tolist(),
        "intersection_z": [
            [float(value.real), float(value.imag)] for value in gamma_state
        ],
        "K_minus_Gamma_norm": float(np.linalg.norm(k_state - gamma_state)),
        "scaled_residual_max_abs": float(
            np.max(np.abs(scaled_residual))
        ),
        "physical_residual_max_abs": float(
            np.max(np.abs(physical_residual))
        ),
        "gamma_rank": int(np.linalg.matrix_rank(gamma_frame)),
        "k_rank": int(np.linalg.matrix_rank(k_frame)),
        "direct_orientation": direct_orientation,
        "assembled_root_jacobian_orientation": root_orientation,
        "independent_finite_difference_orientation": fd_orientation,
        "independent_fd_to_DOP853_variational_relative_error": (
            fd_relative_error
        ),
        "finite_difference_steps": finite_difference_steps,
        "finite_difference_ladder_relative_differences": (
            finite_difference_ladder_relative_differences
        ),
        "root_jacobian_parity_passed": (
            root_orientation["sign"] == -direct_orientation["sign"]
            and (
                fd_orientation is None
                or fd_orientation["sign"] == -direct_orientation["sign"]
            )
        ),
        "orientation_mutations": {
            "reverse_Gamma_first_parameter_sign": reversed_gamma["sign"],
            "reverse_K_first_parameter_sign": reversed_k["sign"],
        },
        "flow_ledger": ledger,
        "window_margins": {
            "minimum_y_margin": float(
                FIELD_WINDOW - np.max(np.abs(parameters[:4]))
            ),
            "psi_margin": float(1.4 - abs(parameters[4])),
            "minimum_chart_margin": float(
                0.6 - np.max(np.abs(parameters[5:9]))
            ),
            "flow_time_margin": float(FLOW_TIME_MAX - parameters[9]),
        },
        "mode_orientation_corrected_sign": direct_orientation["sign"],
        "nodal_to_mode_basis_determinant": 1,
        "m4_or_continuum_result": None,
    }
    return parameters, result


def solve_odd_clamp(
    model: NumericModel,
    saddle: SaddleData,
    fixed: FixedMetric,
    full_parameters: np.ndarray,
) -> dict[str, object]:
    # CHART_TANGENT columns 0 and 3 are the two delta-zero odd directions.
    free_indices = np.array([0, 1, 2, 3, 4, 6, 7, 9])
    initial = full_parameters[free_indices]
    lower = np.array(
        [-FIELD_WINDOW] * 4 + [-1.4, -0.6, -0.6, 7.0]
    )
    upper = np.array(
        [FIELD_WINDOW] * 4 + [1.4, 0.6, 0.6, FLOW_TIME_MAX]
    )

    def unpack(values: np.ndarray) -> np.ndarray:
        parameters = np.zeros(10)
        parameters[free_indices] = values
        return parameters

    coarse_cache: dict[str, object] = {}

    def evaluate(
        values: np.ndarray, method: str, cache: dict[str, object]
    ) -> tuple[np.ndarray, np.ndarray]:
        cached_values = cache.get("values")
        if cached_values is None or not np.array_equal(
            values, cached_values
        ):
            residual, jacobian = residual_and_variational_jacobian(
                unpack(values),
                model,
                saddle,
                fixed,
                PRIMARY_SPHERE_RADIUS,
                method,
            )[:2]
            cache["values"] = values.copy()
            cache["residual"] = residual
            cache["jacobian"] = jacobian[:, free_indices]
        return (
            cache["residual"],  # type: ignore[return-value]
            cache["jacobian"],  # type: ignore[return-value]
        )

    coarse_solution = least_squares(
        lambda values: evaluate(values, "BDF", coarse_cache)[0],
        initial,
        jac=lambda values: evaluate(values, "BDF", coarse_cache)[1],
        bounds=(lower, upper),
        x_scale="jac",
        ftol=2.0e-10,
        xtol=2.0e-10,
        gtol=2.0e-10,
        max_nfev=50,
    )

    accurate_cache: dict[str, object] = {}
    accurate_solution = least_squares(
        lambda values: evaluate(values, "DOP853", accurate_cache)[0],
        coarse_solution.x,
        jac=lambda values: evaluate(values, "DOP853", accurate_cache)[1],
        bounds=(lower, upper),
        x_scale="jac",
        ftol=2.0e-10,
        xtol=2.0e-10,
        gtol=2.0e-10,
        max_nfev=12,
    )
    residual = evaluate(accurate_solution.x, "DOP853", accurate_cache)[0]
    physical_residual = residual * np.repeat(COORDINATE_SCALES, 2)
    return {
        "odd_chart_coordinates_clamped": [0, 3],
        "least_squares_success": bool(accurate_solution.success),
        "least_squares_nfev": {
            "coarse_BDF": int(coarse_solution.nfev),
            "accurate_DOP853": int(accurate_solution.nfev),
        },
        "parameters": unpack(accurate_solution.x).tolist(),
        "accurate_optimality": float(accurate_solution.optimality),
        "accurate_cost": float(accurate_solution.cost),
        "scaled_residual_max_abs": float(np.max(np.abs(residual))),
        "scaled_residual_norm": float(np.linalg.norm(residual)),
        "physical_residual_max_abs": float(
            np.max(np.abs(physical_residual))
        ),
        "is_equivalent_to_full_candidate_within_tolerance": bool(
            np.max(np.abs(physical_residual)) < INTERSECTION_TOLERANCE
        ),
    }


def exact_checks(audit: Audit, manifest: dict[str, object], digest: str) -> None:
    family = build_symbolic_family()
    audit.exact(
        "P40.input.frozen_manifest_contract",
        digest == INPUT_SHA256
        and manifest["freeze_kind"]
        == "post_feasibility_workflow_input_freeze"
        and manifest["is_preregistration"] is False
        and manifest["is_scientific_evidence"] is False,
        "the separately committed post-feasibility manifest fixes the m=3 signed-mutation calculation without being relabelled as preregistration or evidence",
    )
    audit.exact(
        "P40.action.single_scalar_three_midpoint_elements",
        len(family.elements) == 3
        and len(family.variables_z) == COMPLEX_DIMENSION
        and family.action_z == sp.expand(sum(family.elements)),
        "one symbolic S3 scalar is exactly the sum of three midpoint elements on five complex variables",
    )
    audit.exact(
        "P40.action.gradient_and_hessian_same_scalar",
        family.gradient_w
        == sp.Matrix(
            [
                sp.diff(family.action_w, variable)
                for variable in family.variables_w
            ]
        )
        and family.hessian_w
        == sp.hessian(family.action_w, family.variables_w),
        "every production gradient and Hessian entry is differentiated from the same symbolic action scalar",
    )
    audit.exact(
        "P40.action.holomorphic_with_simple_T_zero_pole",
        not family.action_z.has(sp.conjugate)
        and sp.limit(
            family.variables_z[-1] * family.action_z,
            family.variables_z[-1],
            0,
        )
        != 0,
        "S3 contains no hidden conjugation and its simple-pole residue polynomial at the excluded T=0 divisor is not identically zero",
    )
    reflection_map = {
        family.variables_z[0]: family.variables_z[2],
        family.variables_z[1]: family.variables_z[3],
        family.variables_z[2]: family.variables_z[0],
        family.variables_z[3]: family.variables_z[1],
        family.delta: -family.delta,
    }
    reflected_action = family.action_z.xreplace(reflection_map)
    audit.exact(
        "P40.reflection.action_signed_delta_covariance",
        sp.simplify(reflected_action - family.action_z) == 0,
        "the three-segment action obeys S3(Rz;-delta)=S3(z;delta) exactly",
    )
    w_reflection_map = {
        family.variables_w[0]: family.variables_w[2],
        family.variables_w[1]: family.variables_w[3],
        family.variables_w[2]: family.variables_w[0],
        family.variables_w[3]: family.variables_w[1],
        family.delta: -family.delta,
    }
    reflected_gradient = family.gradient_w.xreplace(w_reflection_map)
    reflected_hessian = family.hessian_w.xreplace(w_reflection_map)
    reflection_symbolic = sp.Matrix(REFLECTION.astype(int))
    audit.exact(
        "P40.reflection.gradient_signed_delta_covariance",
        all(
            sp.simplify(value) == 0
            for value in reflected_gradient
            - reflection_symbolic * family.gradient_w
        ),
        "the full five-component gradient transforms covariantly under signed endpoint reversal",
    )
    audit.exact(
        "P40.reflection.hessian_signed_delta_covariance",
        all(
            sp.simplify(value) == 0
            for value in reflected_hessian
            - reflection_symbolic
            * family.hessian_w
            * reflection_symbolic
        ),
        "the full five-by-five Hessian transforms by R H(delta) R under signed endpoint reversal",
    )
    sqrt_two = sp.sqrt(2)
    mode_basis = sp.Matrix(
        [
            [1 / sqrt_two, 0, 0, -1 / sqrt_two, 0],
            [0, 1 / sqrt_two, 0, 0, -1 / sqrt_two],
            [1 / sqrt_two, 0, 0, 1 / sqrt_two, 0],
            [0, 1 / sqrt_two, 0, 0, 1 / sqrt_two],
            [0, 0, 1, 0, 0],
        ]
    )
    audit.exact(
        "P40.modes.oriented_DST_reflection_parity",
        sp.simplify(mode_basis.det()) == 1
        and sp.simplify(
            mode_basis.T * reflection_symbolic * mode_basis
            - sp.diag(1, 1, 1, -1, -1)
        )
        == sp.zeros(5),
        "the declared DST-I even-even-T-odd-odd basis has determinant +1 and reflection parity diag(+,+,+,-,-)",
    )
    a_symmetric, phi_symmetric = sp.symbols("a_symmetric phi_symmetric")
    symmetric_substitution = {
        family.delta: 0,
        family.variables_w[2]: family.variables_w[0],
        family.variables_w[3]: family.variables_w[1],
    }
    hessian_mode = sp.simplify(
        mode_basis.T
        * family.hessian_w.subs(symmetric_substitution)
        * mode_basis
    )
    audit.exact(
        "P40.modes.delta_zero_even_odd_block_separation",
        hessian_mode[:3, 3:] == sp.zeros(3, 2)
        and hessian_mode[3:, :3] == sp.zeros(2, 3),
        "at equal endpoints and a reflection-symmetric history the full Hessian separates exactly into three even and two odd directions",
    )
    audit.exact(
        "P40.orientation.full_middle_dimension_and_root_parity",
        COMPLEX_DIMENSION == 2 * (SEGMENT_COUNT - 1) + 1
        and AMBIENT_REAL_DIMENSION == 2 * COMPLEX_DIMENSION
        and (-1) ** COMPLEX_DIMENSION == -1,
        "Gamma and K each have middle dimension five in R10 and [V_Gamma,-V_K] has the opposite sign from [V_Gamma,V_K]",
    )
    gradient_real = sp.symbols(
        f"gradient_real_0:{COMPLEX_DIMENSION}", real=True
    )
    gradient_imag = sp.symbols(
        f"gradient_imag_0:{COMPLEX_DIMENSION}", real=True
    )
    flow_action_derivative = sp.expand(
        sum(
            (real + sp.I * imag) * (-real + sp.I * imag)
            for real, imag in zip(gradient_real, gradient_imag)
        )
    )
    expected_flow_derivative = -sum(
        real**2 + imag**2
        for real, imag in zip(gradient_real, gradient_imag)
    )
    audit.exact(
        "P40.flow.holomorphic_dual_flow_identity",
        sp.simplify(flow_action_derivative - expected_flow_derivative) == 0
        and sp.im(flow_action_derivative) == 0,
        "for holomorphic S and dot(xi)=-conjugate(gradient S), dS/dt is exactly minus the squared gradient norm and is real",
    )
    required = manifest["required_fail_closed_outputs"]
    audit.exact(
        "P40.guard.incomplete_data_force_null_global_outputs",
        required["straight_arm_intersections_searched"] is False
        and required["cap_reintersections_searched"] is False
        and required["root_exhaustion_proved"] is False
        and required["non_Stokes_chamber_certified"] is False
        and required["bounded_chain_signed_sum"] is None
        and required["complete_global_signed_intersection_vector"] is None
        and required["global_n_sigma"] is None,
        "the frozen contract refuses every bounded-chain or global integer while the chain, census, Stokes, and end data are incomplete",
    )


def main() -> None:
    audit = Audit()
    manifest, _raw, digest = load_manifest()
    exact_checks(audit, manifest, digest)

    seed_z = np.array([3.584, 1.0, 3.584, 1.0, 0.745])
    seed_w = seed_z / COORDINATE_SCALES
    saddle_w_by_delta: dict[float, np.ndarray] = {}
    saddle_records: dict[float, dict[str, object]] = {}
    saddle_zero_w, record_zero = solve_real_saddle(
        numeric_model(0.0), seed_w
    )
    saddle_w_by_delta[0.0] = saddle_zero_w
    saddle_records[0.0] = record_zero
    for sign in (1.0, -1.0):
        running_seed = saddle_zero_w.copy()
        for magnitude in (0.0005, 0.001):
            delta_value = sign * magnitude
            running_seed, record = solve_real_saddle(
                numeric_model(delta_value), running_seed
            )
            saddle_w_by_delta[delta_value] = running_seed
            saddle_records[delta_value] = record

    fixed = build_fixed_metric(saddle_zero_w)
    saddle_data = {
        delta_value: make_saddle_data(
            numeric_model(delta_value), saddle_w_by_delta[delta_value], fixed
        )
        for delta_value in DELTA_GRID
    }
    audit.numerical(
        "P40.saddle.signed_delta_grid_joint_roots",
        all(
            item.gradient_max_abs < 1.0e-9
            and item.hessian_inertia == (3, 2, 0)
            for item in saddle_data.values()
        ),
        "all five signed-delta values have numerically resolved nondegenerate five-equation saddles with inertia (3-,2+)",
    )
    reflection_saddle_residuals = []
    reflection_action_residuals = []
    reflection_hessian_residuals = []
    for magnitude in (0.0005, 0.001):
        plus = saddle_data[magnitude]
        minus = saddle_data[-magnitude]
        reflection_saddle_residuals.append(
            float(np.max(np.abs(minus.saddle_w - REFLECTION @ plus.saddle_w)))
        )
        reflection_action_residuals.append(abs(minus.action - plus.action))
        reflection_hessian_residuals.append(
            float(
                np.linalg.norm(
                    minus.hessian_w - REFLECTION @ plus.hessian_w @ REFLECTION,
                    ord=2,
                )
                / np.linalg.norm(plus.hessian_w, ord=2)
            )
        )
    audit.numerical(
        "P40.reflection.saddles_actions_and_hessians_match",
        max(reflection_saddle_residuals) < 2.0e-11
        and max(reflection_action_residuals) < 2.0e-10
        and max(reflection_hessian_residuals) < 2.0e-11,
        "the independently solved signed branches match under node reflection in their saddles, actions, and Hessians",
    )
    mode_basis_numeric = np.array(
        [
            [1 / np.sqrt(2), 0, 0, -1 / np.sqrt(2), 0],
            [0, 1 / np.sqrt(2), 0, 0, -1 / np.sqrt(2)],
            [1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2), 0],
            [0, 1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)],
            [0, 0, 1, 0, 0],
        ]
    )
    hessian_mode_zero = (
        mode_basis_numeric.T
        @ saddle_data[0.0].hessian_w
        @ mode_basis_numeric
    )
    even_odd_cross_norm = float(np.linalg.norm(hessian_mode_zero[:3, 3:]))
    odd_block_eigenvalues = np.linalg.eigvalsh(hessian_mode_zero[3:, 3:])
    audit.numerical(
        "P40.modes.first_reflection_odd_block_is_resolved",
        even_odd_cross_norm < 2.0e-8
        and np.min(np.abs(odd_block_eigenvalues)) > 100.0,
        "the m=3 delta-zero Hessian numerically resolves one a/phi reflection-odd block with a nonzero spectral gap",
    )
    metric_reflection_residual = float(
        np.linalg.norm(
            fixed.inverse_metric_mobility_w
            - REFLECTION
            @ fixed.inverse_metric_mobility_w
            @ REFLECTION,
            ord=2,
        )
    )
    reflection_xi = np.linalg.solve(
        fixed.linear_map, REFLECTION @ fixed.linear_map
    )
    reflection_xi_orthogonality_residual = float(
        np.linalg.norm(
            reflection_xi.T @ reflection_xi
            - np.eye(COMPLEX_DIMENSION),
            ord=2,
        )
    )
    signed_projector_reflection_residuals: list[float] = []
    for magnitude in (0.0005, 0.001):
        plus = saddle_data[magnitude]
        minus = saddle_data[-magnitude]
        for sign in (-1, 1):
            indices = np.flatnonzero(
                np.sign(fixed.eigenvalues_zero) == sign
            )
            plus_frame = plus.aligned_signed_subspace_frame_xi[:, indices]
            minus_frame = minus.aligned_signed_subspace_frame_xi[:, indices]
            plus_projector = plus_frame @ plus_frame.T
            minus_projector = minus_frame @ minus_frame.T
            signed_projector_reflection_residuals.append(
                float(
                    np.linalg.norm(
                        minus_projector
                        - reflection_xi
                        @ plus_projector
                        @ reflection_xi.T,
                        ord=2,
                    )
                )
            )
    takagi_normalization_residuals = []
    for delta_value, item in saddle_data.items():
        hessian_xi_value = (
            fixed.linear_map.T
            @ item.hessian_w
            @ fixed.linear_map
        )
        takagi_normalization_residuals.append(
            float(
                np.linalg.norm(
                    item.launch_matrix_xi.T
                    @ hessian_xi_value
                    @ item.launch_matrix_xi
                    + np.eye(COMPLEX_DIMENSION),
                    ord=2,
                )
            )
        )
    audit.numerical(
        "P40.metric.delta_zero_metric_is_fixed_and_reflection_covariant",
        metric_reflection_residual < 1.0e-14
        and reflection_xi_orthogonality_residual < 1.0e-12
        and max(signed_projector_reflection_residuals) < 1.0e-10
        and max(takagi_normalization_residuals) < 1.0e-10
        and all(
            item.signed_subspace_min_principal_overlap > 0.999999
            for delta_value, item in saddle_data.items()
            if delta_value != 0.0
        ),
        "one delta-zero Morse-whitened Hermitian metric is fixed while signed projectors reflect covariantly and each Morse launch frame satisfies J-transpose H J=-I",
    )

    def odd_amplitude(item: SaddleData) -> np.ndarray:
        return np.array(
            [
                (item.saddle_z[2] - item.saddle_z[0]) / np.sqrt(2.0),
                (item.saddle_z[3] - item.saddle_z[1]) / np.sqrt(2.0),
            ]
        )

    odd_grid = {
        delta_value: odd_amplitude(saddle_data[delta_value])
        for delta_value in DELTA_GRID
    }
    anchor_odd_grid = {
        delta_value: np.array(
            [0.0, delta_value / (3.0 * np.sqrt(2.0))]
        )
        for delta_value in DELTA_GRID
    }
    anchor_subtracted_odd_grid = {
        delta_value: odd_grid[delta_value] - anchor_odd_grid[delta_value]
        for delta_value in DELTA_GRID
    }
    odd_reflection_residual = max(
        float(np.max(np.abs(odd_grid[-value] + odd_grid[value])))
        for value in (0.0005, 0.001)
    )
    susceptibility_full = odd_grid[0.001] / 0.001
    susceptibility_half = odd_grid[0.0005] / 0.0005
    susceptibility_relative_difference = float(
        np.linalg.norm(susceptibility_full - susceptibility_half)
        / np.linalg.norm(susceptibility_full)
    )
    audit.numerical(
        "P40.mutation.phi_source_exposes_sign_reversing_odd_response",
        np.linalg.norm(odd_grid[0.001]) > 1.0e-6
        and np.linalg.norm(anchor_subtracted_odd_grid[0.001]) > 1.0e-6
        and odd_reflection_residual < 2.0e-11
        and susceptibility_relative_difference < 0.01,
        "the declared rank-one phi endpoint source excites a nonzero tracked odd response, including a nonzero anchor-subtracted component, that reverses with delta and is locally linear on the frozen grid",
    )

    intersection_parameters: dict[float, np.ndarray] = {}
    intersection_results: dict[float, dict[str, object]] = {}
    center_parameters, center_result = solve_intersection(
        numeric_model(0.0),
        saddle_data[0.0],
        fixed,
        initial_intersection_parameters(),
        PRIMARY_SPHERE_RADIUS,
        compute_fd=True,
    )
    intersection_parameters[0.0] = center_parameters
    intersection_results[0.0] = center_result
    for sign in (1.0, -1.0):
        running_parameters = center_parameters
        for magnitude in (0.0005, 0.001):
            delta_value = sign * magnitude
            running_parameters, result = solve_intersection(
                numeric_model(delta_value),
                saddle_data[delta_value],
                fixed,
                running_parameters,
                PRIMARY_SPHERE_RADIUS,
                compute_fd=magnitude == 0.001,
            )
            intersection_parameters[delta_value] = running_parameters
            intersection_results[delta_value] = result

    for delta_value in PRIMARY_DELTAS:
        diagnostic = intersection_results[delta_value]
        print(
            "[INFO] P40.intersection.diagnostic "
            + json.dumps(
                {
                    "delta": delta_value,
                    "least_squares_success": diagnostic[
                        "least_squares_success"
                    ],
                    "physical_residual_max_abs": diagnostic[
                        "physical_residual_max_abs"
                    ],
                    "gamma_rank": diagnostic["gamma_rank"],
                    "k_rank": diagnostic["k_rank"],
                    "direct_sign": diagnostic["direct_orientation"]["sign"],
                    "normalized_sigma_min": diagnostic[
                        "direct_orientation"
                    ]["normalized_sigma_min"],
                    "fd_to_variational_relative_error": diagnostic[
                        "independent_fd_to_DOP853_variational_relative_error"
                    ],
                    "fd_ladder_max_relative_difference": max(
                        diagnostic[
                            "finite_difference_ladder_relative_differences"
                        ]
                    ),
                    "fd_ladder_relative_differences": diagnostic[
                        "finite_difference_ladder_relative_differences"
                    ],
                    "parameters": intersection_parameters[
                        delta_value
                    ].tolist(),
                },
                sort_keys=True,
            )
        )

    for delta_value in PRIMARY_DELTAS:
        result = intersection_results[delta_value]
        label = (
            "zero"
            if delta_value == 0.0
            else ("plus" if delta_value > 0 else "minus")
        )
        audit.numerical(
            f"P40.intersection.{label}_delta_full_ten_real_candidate",
            result["least_squares_success"]
            and result["physical_residual_max_abs"]
            < INTERSECTION_TOLERANCE
            and result["gamma_rank"] == COMPLEX_DIMENSION
            and result["k_rank"] == COMPLEX_DIMENSION,
            f"delta={delta_value:+.4g} has one numerically resolved candidate in all ten real coordinates between the declared cap piece and finite-time K chart patch",
        )
        direct = result["direct_orientation"]
        audit.numerical(
            f"P40.orientation.{label}_delta_direct_transversality",
            direct["sign"] != 0
            and direct["normalized_sigma_min"] > TRANSVERSALITY_MINIMUM
            and result["root_jacobian_parity_passed"]
            and result["orientation_mutations"][
                "reverse_Gamma_first_parameter_sign"
            ]
            == -direct["sign"]
            and result["orientation_mutations"][
                "reverse_K_first_parameter_sign"
            ]
            == -direct["sign"],
            f"delta={delta_value:+.4g} has a nonzero direct R10 determinant, the odd five-column root-Jacobian parity, and both orientation-reversal controls",
        )
        audit.numerical(
            f"P40.tangent.{label}_delta_independent_FD_control",
            result["independent_finite_difference_orientation"]["sign"]
            == -direct["sign"]
            and result[
                "independent_fd_to_DOP853_variational_relative_error"
            ]
            < 0.02
            and max(
                result[
                    "finite_difference_ladder_relative_differences"
                ]
            )
            < 0.02,
            f"delta={delta_value:+.4g} a two-step central-difference ladder of the actual residual agrees in sign and matrix norm with the DOP853 variational frame",
        )
        flow = result["flow_ledger"]
        audit.numerical(
            f"P40.flow.{label}_delta_Morse_control",
            flow["ReS_end"] < flow["ReS_start"]
            and flow["ReS_max_positive_step"] < 2.0e-8
            and flow["ImS_max_drift"] < 2.0e-7
            and flow["xi_norm_max"] < FLOW_NORM_MAX
            and flow["sampled_no_prior_cap_crossing"],
            f"delta={delta_value:+.4g} sampled upward flow makes Re(S) nonincreasing, preserves Im(S), stays inside the xi-norm cap, and has no sampled earlier |T|=r crossing",
        )

    plus_state = np.array(
        [complex(*value) for value in intersection_results[0.001]["intersection_z"]]
    )
    minus_state = np.array(
        [complex(*value) for value in intersection_results[-0.001]["intersection_z"]]
    )
    candidate_reflection_residual = float(
        np.max(np.abs(minus_state - REFLECTION @ plus_state))
    )
    primary_signs = [
        intersection_results[value]["direct_orientation"]["sign"]
        for value in PRIMARY_DELTAS
    ]
    audit.numerical(
        "P40.reflection.signed_local_candidates_match",
        candidate_reflection_residual < 2.0e-6
        and primary_signs[0] == primary_signs[2],
        "the plus/minus endpoint probes return reflection-matched cap candidates with the same declared local orientation sign",
    )
    audit.numerical(
        "P40.intersection.sampled_five_point_continuation_same_recorded_sign",
        len(
            {
                intersection_results[value]["direct_orientation"]["sign"]
                for value in DELTA_GRID
            }
        )
        == 1
        and all(
            intersection_results[value]["physical_residual_max_abs"]
            < INTERSECTION_TOLERANCE
            for value in DELTA_GRID
        ),
        "the sequentially continued five-point delta grid has one common local sign and resolved residual at every sampled point, without asserting a continuous branch theorem",
    )

    radius_results: dict[float, dict[str, object]] = {}
    for radius in CONTROL_SPHERE_RADII:
        radius_seed = intersection_parameters[0.001].copy()
        radius_seed[9] += np.log(PRIMARY_SPHERE_RADIUS / radius)
        parameters, result = solve_intersection(
            numeric_model(0.001),
            saddle_data[0.001],
            fixed,
            radius_seed,
            radius,
            compute_fd=False,
        )
        radius_results[radius] = result
    audit.numerical(
        "P40.intersection.three_radius_local_sign_control",
        all(
            result["direct_orientation"]["sign"] == primary_signs[-1]
            and result["direct_orientation"]["normalized_sigma_min"]
            > TRANSVERSALITY_MINIMUM
            and result["physical_residual_max_abs"]
            < INTERSECTION_TOLERANCE
            for result in radius_results.values()
        ),
        "the delta=+.001 tracked candidate retains its local sign and transverse gap on the frozen half/base/double launch-radius ladder",
    )
    clamp_result = solve_odd_clamp(
        numeric_model(0.001),
        saddle_data[0.001],
        fixed,
        intersection_parameters[0.001],
    )
    audit.numerical(
        "P40.mutation.K_launch_odd_coordinate_clamp_local_fit",
        clamp_result["least_squares_success"]
        and clamp_result["accurate_optimality"] < 1.0e-7
        and clamp_result["is_equivalent_to_full_candidate_within_tolerance"]
        is False
        and clamp_result["scaled_residual_max_abs"]
        > 10.0
        * intersection_results[0.001]["scaled_residual_max_abs"],
        "the converged local fit with both frozen K-launch odd coordinates clamped fails the candidate tolerance and gives a same-unit residual worsening; it is not a full odd-sector ablation",
    )

    audit.numerical(
        "P40.guard.local_higher_cutoff_data_do_not_emit_global_integer",
        manifest["required_fail_closed_outputs"][
            "bounded_chain_signed_sum"
        ]
        is None
        and manifest["required_fail_closed_outputs"][
            "complete_global_signed_intersection_vector"
        ]
        is None
        and manifest["required_fail_closed_outputs"]["global_n_sigma"]
        is None,
        "the successful higher-cutoff local ledger leaves every bounded-chain and global Picard-Lefschetz integer null",
    )

    saddle_payload = {
        str(delta_value): {
            **saddle_records[delta_value],
            "odd_mode_amplitudes": odd_grid[delta_value].tolist(),
            "fixed_metric_Hxi_eigenvalues": saddle_data[
                delta_value
            ].hessian_xi_eigenvalues.tolist(),
            "signed_subspace_min_principal_overlap": saddle_data[
                delta_value
            ].signed_subspace_min_principal_overlap,
        }
        for delta_value in DELTA_GRID
    }
    result = {
        "phase": 40,
        "gate": "Gate 1 -- original joint cycle and signed global intersections",
        "calculation": "m=3 signed-endpoint reflection-odd local joint-intersection audit",
        "input_manifest": {
            "path": str(INPUT_PATH.relative_to(Path.cwd())),
            "sha256": digest,
            "introduced_in_commit": INPUT_INITIAL_FREEZE_COMMIT,
            "initial_freeze_sha256": INPUT_INITIAL_FREEZE_SHA256,
            "amended_in_commit": INPUT_AMENDED_IN_COMMIT,
            "amendment_clock_note": (
                "the manifest's declared amended_at_utc is later than the "
                "actual amendment commit timestamp; both raw values are "
                "preserved rather than silently rewritten"
            ),
            "freeze_kind": manifest["freeze_kind"],
            "is_preregistration": manifest["is_preregistration"],
            "is_scientific_evidence": manifest["is_scientific_evidence"],
        },
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "model": {
            "segment_count": SEGMENT_COUNT,
            "complex_dimension": COMPLEX_DIMENSION,
            "ambient_real_dimension": AMBIENT_REAL_DIMENSION,
            "endpoint_source": "phi-only antisymmetric signed delta",
            "endpoint_source_rank": 1,
            "full_reflection_odd_field_sector_dimension": 2,
            "full_odd_sector_probed": False,
            "flow_geometry": (
                "one delta-zero positive Hermitian metric, equivalently its "
                "inverse-metric mobility L0 L0^T, fixed across the signed grid"
            ),
            "launch_geometry": (
                "delta-dependent Morse-normalized ellipsoids inside "
                "Procrustes-aligned signed spectral subspaces"
            ),
        },
        "saddles": saddle_payload,
        "reflection_controls": {
            "saddle_max_abs": max(reflection_saddle_residuals),
            "action_max_abs": max(reflection_action_residuals),
            "hessian_max_relative": max(reflection_hessian_residuals),
            "candidate_max_abs": candidate_reflection_residual,
            "metric_operator_residual": metric_reflection_residual,
            "xi_reflection_orthogonality_residual": (
                reflection_xi_orthogonality_residual
            ),
            "signed_projector_max_residual": max(
                signed_projector_reflection_residuals
            ),
            "Takagi_J_transpose_H_J_plus_I_max_residual": max(
                takagi_normalization_residuals
            ),
            "odd_amplitude_max_abs": odd_reflection_residual,
        },
        "mode_ledger": {
            "mode_order": manifest["reflection_and_mode_conventions"][
                "mode_order"
            ],
            "nodal_to_mode_basis_determinant": 1,
            "delta_zero_even_odd_cross_norm": even_odd_cross_norm,
            "delta_zero_odd_block_eigenvalues": (
                odd_block_eigenvalues.tolist()
            ),
            "odd_susceptibility_at_full_grid": susceptibility_full.tolist(),
            "anchor_subtracted_odd_amplitudes": {
                str(value): anchor_subtracted_odd_grid[value].tolist()
                for value in DELTA_GRID
            },
            "half_to_full_susceptibility_relative_difference": (
                susceptibility_relative_difference
            ),
        },
        "primary_local_candidates": {
            str(value): intersection_results[value]
            for value in PRIMARY_DELTAS
        },
        "intermediate_sampled_continuation_candidates": {
            str(value): intersection_results[value]
            for value in (-0.0005, 0.0005)
        },
        "sphere_radius_controls_at_plus_delta": {
            str(value): radius_results[value] for value in CONTROL_SPHERE_RADII
        },
        "K_launch_odd_coordinate_clamp_local_fit": clamp_result,
        "completion_ledger": {
            "m4_computed": False,
            "cutoff_convergence_proved": False,
            "straight_arm_intersections_searched": False,
            "cap_reintersections_searched": False,
            "continuous_direction_coverage_proved": False,
            "root_exhaustion_proved": False,
            "exact_nonlinear_upward_manifold_certified": False,
            "all_saddles_and_upward_components_complete": False,
            "non_Stokes_chamber_certified": False,
            "all_relative_good_ends_classified": False,
            "physical_original_cycle_derived": False,
            "BFV_Pfaffian_Pin_orientation_computed": False,
        },
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "gate_status": {
            "Gate_1": "OPEN_PARTIAL_M3_REFLECTION_ODD_LOCAL_PROGRESS",
            "Gate_2": "EXPLORATORY_CALCULATION_ALLOWED_BUT_PHYSICAL_PROMOTION_DEPENDS_ON_GATE_1",
            "Gate_3": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_2_TYPED_OUTPUT",
            "Gate_4": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_3_TYPED_OUTPUT",
            "Gate_5": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_4_TYPED_OUTPUT",
        },
        "claim_status": {
            "the_declared_phi_source_exposes_a_nonzero_sign_reversing_tracked_odd_response": "SUPPORTED_NUMERICALLY_FOR_ONE_FROZEN_M3_BRANCH_AND_RANK_ONE_SOURCE",
            "the_frozen_m3_cap_piece_has_sampled_local_full_R10_candidates_across_the_five_point_signed_grid": "SUPPORTED_NUMERICALLY_WITHIN_ONE_FIXED_METRIC_AND_DELTA_DEPENDENT_MORSE_LAUNCH_CHARTS",
            "the_m3_result_establishes_m4_or_continuum_cutoff_stability": "OPEN_M4_AND_CONTINUUM_NOT_COMPUTED",
            "the_local_m3_candidates_license_inference_to_the_bounded_chain_or_global_intersection_vector": "INFERENCE_BLOCKED_BY_INCOMPLETE_TYPED_DATA",
        },
        "scope_guard": {
            "computed": [
                "one explicit nonlinear three-segment midpoint configuration action on C^4 times C-star_T",
                "one signed phi-endpoint mutation grid and exact delta-reflection covariance",
                "the first two-dimensional a/phi reflection-odd Hessian block and one tracked rank-one-source response with its linear-anchor component separated",
                "one delta-zero positive Hermitian metric held fixed across all endpoint mutations",
                "one delta-dependent Morse-normalized finite-radius finite-time five-real-dimensional upward-chart patch per sampled delta",
                "five sequentially sampled local ten-real-dimensional cap-piece candidates, with full controls at delta=-.001,0,+.001",
                "one converged continued-seed local fit after clamping the two frozen K-launch odd coordinates; this is not a full odd-sector ablation",
            ],
            "not_computed": [
                "m=4 or any continuum/cutoff convergence statement",
                "the second independent endpoint-source direction needed to probe the full odd field sector",
                "the entire bounded cap-plus-straight-arm chain or later cap reintersections",
                "continuous chart coverage, root exhaustion, an exact nonlinear complete upward manifold, or every saddle/component",
                "a non-Stokes lateral chamber, connecting flows and jumps, or every relative good end",
                "a proof that the Gaussian-lift candidate is the physical original cycle",
                "a bounded-chain signed sum, global Picard-Lefschetz vector, or global n_sigma",
                "canonical momenta, BFV ghosts, fermions, gravitino, inhomogeneous modes, Pfaffian/Pin data, spinorial charge, order parameter, particle poles, state, or quantum gravity",
            ],
        },
        "next_calculation": "run the orientation-matched m=4 parity/cutoff control, including both phi-only and an independent a-only endpoint source, before attempting m=5 chain, Stokes, and relative-end completion",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    print(
        f"All {audit.exact_passed} exact checks and "
        f"{audit.numerical_passed} numerical checks passed."
    )


if __name__ == "__main__":
    main()
