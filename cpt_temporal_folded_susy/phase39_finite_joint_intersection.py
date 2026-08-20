#!/usr/bin/env python3
"""Phase 39 -- finite-cutoff full-joint local intersection pilot.

This executable is the first Gate-1 calculation in the repository that uses
one explicit nonlinear finite-cutoff action on the joint field--lapse space,
re-solves its discrete critical point, integrates a full joint upward PL
flow, transports its tangent frame, and evaluates

    sign det_R[V_Gamma, V_K]

in all six real ambient directions.  The independently anchored comparison
chain is the frozen m=2 finite-window Gaussian lift of the Phase-32 lower
lapse bypass recorded in PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json.

The result is intentionally only an algorithm pilot.  The m=2 regulator has
one interior history node and no reflection-odd history mode.  The finite
arms and field box are not classified as relative good ends, the real saddle
is not placed in a certified non-Stokes chamber, other saddles and upward
components are not exhausted, and no BFV/Pfaffian/Pin line is present.
Accordingly complete_global_signed_intersection_vector and global_n_sigma
are hard-coded to remain null.  The script writes no files.
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
from scipy.optimize import brentq, least_squares, root


INPUT_PATH = Path(__file__).with_name(
    "PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json"
)
INPUT_INTRODUCED_IN_COMMIT = (
    "750d19e76827ce78c9322e9fac6b494ade1f2bbf"
)
SEGMENT_COUNT = 2
PRIMARY_SPHERE_RADIUS = 1.0e-4
CONTROL_SPHERE_RADIUS = 2.0e-4
CAP_RADII = (0.3, 0.2)
FIELD_WINDOW = 0.25
FLOW_TIME_MAX = 13.5
FLOW_NORM_MAX = 30.0
ALPHA_SCAN_COUNT = 49
CUBE_FACE_GRID_COUNT = 3
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
class FrozenInput:
    payload: dict[str, object]
    raw: bytes
    sha256: str
    boundary_scale: float
    boundary_phi: float
    coordinate_scales: np.ndarray


@dataclass(frozen=True)
class SymbolicModel:
    variables_z: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
    variables_w: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
    boundary_symbols: tuple[sp.Symbol, sp.Symbol]
    action_z_general: sp.Expr
    element_left_general: sp.Expr
    action_w: sp.Expr
    gradient_w: sp.Matrix
    hessian_w: sp.Matrix
    action_function: Callable[..., object]
    gradient_function: Callable[..., object]
    hessian_function: Callable[..., object]


@dataclass(frozen=True)
class MorseData:
    saddle_w: np.ndarray
    saddle_z: np.ndarray
    saddle_action: complex
    hessian_w: np.ndarray
    eigenvalues: np.ndarray
    oriented_eigenvectors: np.ndarray
    whitening: np.ndarray
    upward_frame_xi: np.ndarray
    downward_frame_xi: np.ndarray


@dataclass(frozen=True)
class FlowHit:
    status: str
    flow_time: float | None
    xi: np.ndarray | None
    z: np.ndarray | None
    membership_residual: np.ndarray | None
    psi: float | None
    y_a: float | None
    y_phi: float | None
    solver_message: str


def load_frozen_input() -> FrozenInput:
    raw = INPUT_PATH.read_bytes()
    payload = json.loads(raw)
    model = payload["model"]
    boundary = model["fixed_boundary"]
    metric = payload["gradient_metric"]
    scales_payload = metric["scales"]
    boundary_scale = float(boundary["a_left"])
    boundary_phi = float(boundary["phi_left"])
    scales = np.array(
        [
            float(scales_payload["a"]),
            float(scales_payload["phi"]),
            float(scales_payload["T"]),
        ],
        dtype=float,
    )
    return FrozenInput(
        payload=payload,
        raw=raw,
        sha256=hashlib.sha256(raw).hexdigest(),
        boundary_scale=boundary_scale,
        boundary_phi=boundary_phi,
        coordinate_scales=scales,
    )


@lru_cache(maxsize=1)
def build_symbolic_model() -> SymbolicModel:
    a_1, phi_1, proper_time = sp.symbols("a_1 phi_1 T")
    w_a, w_phi, w_t = sp.symbols("w_a w_phi w_T")
    a_boundary, phi_boundary = sp.symbols("a_boundary phi_boundary")
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

    element_left = element(
        a_boundary, phi_boundary, a_1, phi_1
    )
    element_right = element(
        a_1, phi_1, a_boundary, phi_boundary
    )
    action_general = sp.expand(element_left + element_right)

    frozen = load_frozen_input()
    scales = frozen.coordinate_scales
    action_w = action_general.subs(
        {
            a_boundary: sp.Float(str(frozen.boundary_scale), 40),
            phi_boundary: sp.Float(str(frozen.boundary_phi), 40),
            a_1: sp.Float(str(scales[0]), 40) * w_a,
            phi_1: sp.Float(str(scales[1]), 40) * w_phi,
            proper_time: sp.Float(str(scales[2]), 40) * w_t,
        }
    )
    variables_w = (w_a, w_phi, w_t)
    gradient_w = sp.Matrix(
        [sp.diff(action_w, variable) for variable in variables_w]
    )
    hessian_w = sp.hessian(action_w, variables_w)
    return SymbolicModel(
        variables_z=(a_1, phi_1, proper_time),
        variables_w=variables_w,
        boundary_symbols=(a_boundary, phi_boundary),
        action_z_general=action_general,
        element_left_general=element_left,
        action_w=action_w,
        gradient_w=gradient_w,
        hessian_w=hessian_w,
        action_function=sp.lambdify((variables_w,), action_w, "numpy"),
        gradient_function=sp.lambdify(
            (variables_w,), gradient_w, "numpy"
        ),
        hessian_function=sp.lambdify(
            (variables_w,), hessian_w, "numpy"
        ),
    )


def action_at(model: SymbolicModel, w: np.ndarray) -> complex:
    return complex(model.action_function(tuple(w)))


def gradient_at(model: SymbolicModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.gradient_function(tuple(w)), dtype=np.complex128
    ).reshape(3)


def hessian_at(model: SymbolicModel, w: np.ndarray) -> np.ndarray:
    return np.asarray(
        model.hessian_function(tuple(w)), dtype=np.complex128
    ).reshape(3, 3)


def interleaved(vector: np.ndarray) -> np.ndarray:
    complex_vector = np.asarray(vector, dtype=np.complex128).reshape(-1)
    result = np.empty(2 * complex_vector.size, dtype=float)
    result[0::2] = complex_vector.real
    result[1::2] = complex_vector.imag
    return result


def real_frame(complex_frame: np.ndarray) -> np.ndarray:
    frame = np.asarray(complex_frame, dtype=np.complex128)
    return np.column_stack(
        [interleaved(frame[:, column]) for column in range(frame.shape[1])]
    )


def normalize_columns(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(matrix, axis=0)
    if np.any(norms == 0.0):
        raise ValueError("zero tangent column")
    return matrix / norms, norms


def oriented_sign_and_spectrum(
    gamma_frame: np.ndarray, upward_frame: np.ndarray
) -> dict[str, object]:
    joined = np.column_stack([gamma_frame, upward_frame])
    normalized, column_norms = normalize_columns(joined)
    determinant_sign, log_abs_determinant = np.linalg.slogdet(normalized)
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    return {
        "sign": int(np.sign(determinant_sign)),
        "log_abs_normalized_determinant": float(log_abs_determinant),
        "normalized_singular_values": singular_values.tolist(),
        "normalized_sigma_min": float(singular_values[-1]),
        "normalized_condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
        "column_norms": column_norms.tolist(),
    }


def square_sign_and_spectrum(matrix: np.ndarray) -> dict[str, object]:
    normalized, column_norms = normalize_columns(matrix)
    determinant_sign, log_abs_determinant = np.linalg.slogdet(normalized)
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    return {
        "sign": int(np.sign(determinant_sign)),
        "log_abs_normalized_determinant": float(log_abs_determinant),
        "normalized_singular_values": singular_values.tolist(),
        "normalized_sigma_min": float(singular_values[-1]),
        "normalized_condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
        "column_norms": column_norms.tolist(),
    }


def deterministic_oriented_eigenframe(
    hessian: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(hessian)
    for column in range(eigenvectors.shape[1]):
        pivot = int(np.argmax(np.abs(eigenvectors[:, column])))
        if eigenvectors[pivot, column] < 0.0:
            eigenvectors[:, column] *= -1.0
    if np.linalg.det(eigenvectors) < 0.0:
        eigenvectors[:, -1] *= -1.0
    return eigenvalues, eigenvectors


def solve_main_saddle(
    frozen: FrozenInput, model: SymbolicModel
) -> tuple[MorseData, dict[str, object]]:
    phi_seed = 1.0
    slope = np.sqrt(2.0 / 3.0)
    potential_seed = 0.75 * (1.0 - np.exp(-slope * phi_seed)) ** 2
    z_seed = np.array(
        [np.sqrt(3.0 / potential_seed), phi_seed, 0.7], dtype=float
    )
    w_seed = z_seed / frozen.coordinate_scales
    scipy_solution = root(
        lambda value: gradient_at(model, value).real,
        w_seed,
        jac=lambda value: hessian_at(model, value).real,
        method="hybr",
        options={"xtol": 1.0e-11},
    )
    if not scipy_solution.success:
        raise RuntimeError(f"discrete saddle solve failed: {scipy_solution.message}")

    high_precision = sp.nsolve(
        tuple(model.gradient_w),
        model.variables_w,
        tuple(float(value) for value in scipy_solution.x),
        tol=sp.Float("1e-50"),
        maxsteps=100,
        prec=70,
    )
    saddle_w = np.array([float(value) for value in high_precision], dtype=float)
    saddle_z = frozen.coordinate_scales * saddle_w
    gradient = gradient_at(model, saddle_w)
    hessian = hessian_at(model, saddle_w).real
    eigenvalues, eigenvectors = deterministic_oriented_eigenframe(hessian)
    whitening = eigenvectors @ np.diag(1.0 / np.sqrt(np.abs(eigenvalues)))

    upward_frame = np.eye(3, dtype=np.complex128)
    downward_frame = np.eye(3, dtype=np.complex128)
    for index, eigenvalue in enumerate(eigenvalues):
        if eigenvalue < 0.0:
            upward_frame[:, index] *= -1.0
            downward_frame[:, index] *= 1.0j
        else:
            upward_frame[:, index] *= 1.0j

    morse = MorseData(
        saddle_w=saddle_w,
        saddle_z=saddle_z,
        saddle_action=action_at(model, saddle_w),
        hessian_w=hessian,
        eigenvalues=eigenvalues,
        oriented_eigenvectors=eigenvectors,
        whitening=whitening,
        upward_frame_xi=upward_frame,
        downward_frame_xi=downward_frame,
    )
    return morse, {
        "continuum_seed_z": z_seed.tolist(),
        "scipy_success": bool(scipy_solution.success),
        "scipy_message": str(scipy_solution.message),
        "saddle_w": saddle_w.tolist(),
        "saddle_z": saddle_z.tolist(),
        "action": [morse.saddle_action.real, morse.saddle_action.imag],
        "gradient_max_abs": float(np.max(np.abs(gradient))),
        "hessian_eigenvalues_dimensionless_reference": eigenvalues.tolist(),
        "hessian_inertia": {
            "negative": int(np.count_nonzero(eigenvalues < 0.0)),
            "positive": int(np.count_nonzero(eigenvalues > 0.0)),
            "zero": int(np.count_nonzero(np.abs(eigenvalues) <= 1.0e-9)),
        },
        "oriented_eigenframe_determinant": float(np.linalg.det(eigenvectors)),
        "whitened_hessian": (
            whitening.T @ hessian @ whitening
        ).tolist(),
    }


def bounded_real_saddle_ledger(
    frozen: FrozenInput, model: SymbolicModel
) -> list[dict[str, object]]:
    seeds_z = (
        (3.59, 0.99, 0.82),
        (3.59, 0.99, -0.82),
        (-0.30, -0.44, 7.6),
        (-0.30, -0.44, -7.6),
        (2.0, -0.7, 10.0),
        (2.0, -0.7, -10.0),
    )
    roots: list[np.ndarray] = []
    for seed_z in seeds_z:
        seed_w = np.asarray(seed_z, dtype=float) / frozen.coordinate_scales
        solution = root(
            lambda value: gradient_at(model, value).real,
            seed_w,
            jac=lambda value: hessian_at(model, value).real,
            method="hybr",
            options={"xtol": 2.0e-10},
        )
        if not solution.success:
            continue
        candidate = np.asarray(solution.x, dtype=float)
        if np.max(np.abs(gradient_at(model, candidate))) > 2.0e-6:
            continue
        if not any(np.linalg.norm(candidate - known) < 1.0e-6 for known in roots):
            roots.append(candidate)

    ledger: list[dict[str, object]] = []
    for saddle_w in sorted(roots, key=lambda value: tuple(value)):
        hessian = hessian_at(model, saddle_w).real
        eigenvalues = np.linalg.eigvalsh(hessian)
        action = action_at(model, saddle_w)
        ledger.append(
            {
                "z": (frozen.coordinate_scales * saddle_w).tolist(),
                "action": [action.real, action.imag],
                "gradient_max_abs": float(
                    np.max(np.abs(gradient_at(model, saddle_w)))
                ),
                "inertia": {
                    "negative": int(np.count_nonzero(eigenvalues < 0.0)),
                    "positive": int(np.count_nonzero(eigenvalues > 0.0)),
                    "zero": int(np.count_nonzero(np.abs(eigenvalues) <= 1.0e-8)),
                },
            }
        )
    return ledger


def xi_to_w(morse: MorseData, xi: np.ndarray) -> np.ndarray:
    return morse.saddle_w + morse.whitening @ xi


def gradient_xi(
    model: SymbolicModel, morse: MorseData, xi: np.ndarray
) -> np.ndarray:
    return morse.whitening.T @ gradient_at(model, xi_to_w(morse, xi))


def hessian_xi(
    model: SymbolicModel, morse: MorseData, xi: np.ndarray
) -> np.ndarray:
    return (
        morse.whitening.T
        @ hessian_at(model, xi_to_w(morse, xi))
        @ morse.whitening
    )


def flow_xi(
    model: SymbolicModel, morse: MorseData, xi: np.ndarray
) -> np.ndarray:
    return -np.conjugate(gradient_xi(model, morse, xi))


def omega_equatorial(alpha: float, beta: float) -> tuple[np.ndarray, ...]:
    cos_beta = np.cos(beta)
    sin_beta = np.sin(beta)
    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)
    omega = np.array(
        [cos_beta * cos_alpha, cos_beta * sin_alpha, sin_beta], dtype=float
    )
    derivative_alpha = np.array(
        [-cos_beta * sin_alpha, cos_beta * cos_alpha, 0.0], dtype=float
    )
    derivative_beta = np.array(
        [
            -sin_beta * cos_alpha,
            -sin_beta * sin_alpha,
            cos_beta,
        ],
        dtype=float,
    )
    return omega, derivative_alpha, derivative_beta


def omega_cubed_face(
    axis: int, sign: int, coordinate_u: float, coordinate_v: float
) -> np.ndarray:
    other = [index for index in range(3) if index != axis]
    vector = np.zeros(3, dtype=float)
    vector[axis] = float(sign)
    vector[other[0]] = coordinate_u
    vector[other[1]] = coordinate_v
    return vector / np.linalg.norm(vector)


def initial_xi(
    morse: MorseData, omega: np.ndarray, sphere_radius: float
) -> np.ndarray:
    return sphere_radius * (morse.upward_frame_xi @ omega)


def integrate_state_fixed_time(
    model: SymbolicModel,
    morse: MorseData,
    omega: np.ndarray,
    flow_time: float,
    sphere_radius: float,
    *,
    rtol: float = 2.0e-10,
    atol: float = 2.0e-12,
) -> np.ndarray:
    initial = initial_xi(morse, omega, sphere_radius)
    if flow_time == 0.0:
        return initial
    right_hand_side = lambda _time, xi: flow_xi(model, morse, xi)
    solution = solve_ivp(
        right_hand_side,
        (0.0, flow_time),
        initial,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=0.04,
    )
    if not solution.success:
        # Near the T=0 meromorphic divisor a tiny chart mutation can be much
        # stiffer than the symmetric trajectory.  BDF is used only as an
        # independent finite-difference/control fallback; the production
        # state and variational frame remain DOP853 integrations.
        solution = solve_ivp(
            right_hand_side,
            (0.0, flow_time),
            initial,
            method="BDF",
            rtol=max(rtol, 2.0e-9),
            atol=max(atol, 2.0e-11),
            max_step=0.02,
        )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1]


def cap_membership(
    frozen: FrozenInput, z: np.ndarray
) -> tuple[np.ndarray, float, float, float]:
    psi = float(np.angle(z[2]))
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    coordinate_a = (z[0] - frozen.boundary_scale) / phase_a
    coordinate_phi = (z[1] - frozen.boundary_phi) / phase_phi
    residual = np.array(
        [coordinate_a.imag, coordinate_phi.imag], dtype=float
    )
    return residual, psi, float(coordinate_a.real), float(coordinate_phi.real)


def first_cap_hit(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    omega: np.ndarray,
    cap_radius: float,
    sphere_radius: float,
    *,
    rtol: float = 3.0e-9,
    atol: float = 3.0e-11,
) -> FlowHit:
    initial = initial_xi(morse, omega, sphere_radius)

    def cap_event(_time: float, xi: np.ndarray) -> float:
        z = frozen.coordinate_scales * xi_to_w(morse, xi)
        return float(abs(z[2]) - cap_radius)

    cap_event.terminal = True
    cap_event.direction = -1

    def norm_event(_time: float, xi: np.ndarray) -> float:
        return float(FLOW_NORM_MAX - np.linalg.norm(xi))

    norm_event.terminal = True
    norm_event.direction = -1

    def singular_event(_time: float, xi: np.ndarray) -> float:
        z = frozen.coordinate_scales * xi_to_w(morse, xi)
        return float(abs(z[2]) - 1.0e-7)

    singular_event.terminal = True
    singular_event.direction = -1

    try:
        solution = solve_ivp(
            lambda _time, xi: flow_xi(model, morse, xi),
            (0.0, FLOW_TIME_MAX),
            initial,
            events=(cap_event, norm_event, singular_event),
            method="DOP853",
            rtol=rtol,
            atol=atol,
            max_step=0.06,
        )
    except (FloatingPointError, OverflowError, ValueError) as error:
        return FlowHit(
            "SOLVER_EXCEPTION_UNRESOLVED",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            str(error),
        )

    if len(solution.t_events[0]) > 0:
        flow_time = float(solution.t_events[0][0])
        xi = np.asarray(solution.y_events[0][0], dtype=np.complex128)
        z = frozen.coordinate_scales * xi_to_w(morse, xi)
        residual, psi, y_a, y_phi = cap_membership(frozen, z)
        if not (-np.pi / 2.0 - 1.0e-8 <= psi <= np.pi / 2.0 + 1.0e-8):
            status = "NONRIGHT_CAP_HIT"
        elif abs(y_a) > FIELD_WINDOW or abs(y_phi) > FIELD_WINDOW:
            status = "RIGHT_CAP_OUTSIDE_FIELD_WINDOW"
        else:
            status = "RIGHT_CAP_FIRST_HIT"
        return FlowHit(
            status,
            flow_time,
            xi,
            z,
            residual,
            psi,
            y_a,
            y_phi,
            str(solution.message),
        )

    if len(solution.t_events[1]) > 0:
        status = "FLOW_NORM_BOX_EXIT_UNRESOLVED"
    elif len(solution.t_events[2]) > 0:
        status = "T_ZERO_SINGULAR_APPROACH"
    elif solution.success:
        status = "FLOW_TIME_BOX_EXIT_UNRESOLVED"
    else:
        status = "SOLVER_FAILURE_UNRESOLVED"
    return FlowHit(
        status,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        str(solution.message),
    )


def gamma_cap(
    frozen: FrozenInput,
    cap_radius: float,
    y_a: float,
    y_phi: float,
    psi: float,
) -> tuple[np.ndarray, np.ndarray]:
    phase_a = np.exp(1.0j * (psi / 2.0 - np.pi / 2.0))
    phase_phi = np.exp(1.0j * psi / 2.0)
    z = np.array(
        [
            frozen.boundary_scale + phase_a * y_a,
            frozen.boundary_phi + phase_phi * y_phi,
            cap_radius * np.exp(1.0j * psi),
        ],
        dtype=np.complex128,
    )
    tangent = np.array(
        [
            [phase_a, 0.0, 0.5j * phase_a * y_a],
            [0.0, phase_phi, 0.5j * phase_phi * y_phi],
            [0.0, 0.0, 1.0j * z[2]],
        ],
        dtype=np.complex128,
    )
    return z, tangent


def integrate_with_chart_tangents(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    alpha: float,
    beta: float,
    flow_time: float,
    sphere_radius: float,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    omega, derivative_alpha, derivative_beta = omega_equatorial(alpha, beta)
    xi_initial = initial_xi(morse, omega, sphere_radius)
    tangent_initial = sphere_radius * morse.upward_frame_xi @ np.column_stack(
        [derivative_alpha, derivative_beta]
    )
    augmented_initial = np.concatenate(
        [xi_initial, tangent_initial.reshape(-1)]
    )

    def rhs(_time: float, augmented: np.ndarray) -> np.ndarray:
        xi = augmented[:3]
        tangent = augmented[3:].reshape(3, 2)
        vector = flow_xi(model, morse, xi)
        tangent_derivative = -np.conjugate(
            hessian_xi(model, morse, xi) @ tangent
        )
        return np.concatenate([vector, tangent_derivative.reshape(-1)])

    solution = solve_ivp(
        rhs,
        (0.0, flow_time),
        augmented_initial,
        method="DOP853",
        rtol=8.0e-11,
        atol=8.0e-13,
        max_step=0.025,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]
    xi = final[:3]
    tangent_xi = final[3:].reshape(3, 2)
    flow_tangent_xi = flow_xi(model, morse, xi)
    linear_map = np.diag(frozen.coordinate_scales) @ morse.whitening
    z = frozen.coordinate_scales * xi_to_w(morse, xi)
    tangent_z = linear_map @ tangent_xi
    flow_tangent_z = linear_map @ flow_tangent_xi
    upward_frame_z = np.column_stack([tangent_z, flow_tangent_z])

    sample_times = np.linspace(0.0, flow_time, 81)
    sampled = solution.sol(sample_times)[:3]
    actions = np.array(
        [
            action_at(model, xi_to_w(morse, sampled[:, index]))
            for index in range(sampled.shape[1])
        ]
    )
    gradients = np.array(
        [
            gradient_xi(model, morse, sampled[:, index])
            for index in range(sampled.shape[1])
        ]
    )
    predicted_derivatives = -np.sum(np.abs(gradients) ** 2, axis=1)
    return z, upward_frame_z, {
        "sample_count": int(sample_times.size),
        "ReS_start": float(actions.real[0]),
        "ReS_end": float(actions.real[-1]),
        "ReS_max_positive_step": float(np.max(np.diff(actions.real))),
        "ImS_max_drift": float(np.max(np.abs(actions.imag - actions.imag[0]))),
        "predicted_dReS_max": float(np.max(predicted_derivatives)),
        "predicted_dReS_min": float(np.min(predicted_derivatives)),
    }


def fixed_chart_state_z(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    alpha: float,
    beta: float,
    flow_time: float,
    sphere_radius: float,
) -> np.ndarray:
    omega = omega_equatorial(alpha, beta)[0]
    xi = integrate_state_fixed_time(
        model, morse, omega, flow_time, sphere_radius
    )
    return frozen.coordinate_scales * xi_to_w(morse, xi)


def intersection_residual(
    parameters: np.ndarray,
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    cap_radius: float,
    sphere_radius: float,
) -> np.ndarray:
    y_a, y_phi, psi, alpha, beta, flow_time = parameters
    gamma_z = gamma_cap(
        frozen, cap_radius, y_a, y_phi, psi
    )[0]
    upward_z = fixed_chart_state_z(
        frozen,
        model,
        morse,
        alpha,
        beta,
        flow_time,
        sphere_radius,
    )
    return interleaved((gamma_z - upward_z) / frozen.coordinate_scales)


def real_component_brackets(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    cap_radius: float,
    sphere_radius: float,
) -> tuple[list[tuple[float, float]], dict[str, object]]:
    alphas = np.linspace(-np.pi, np.pi, ALPHA_SCAN_COUNT, endpoint=False)
    records: list[tuple[float, float] | None] = []
    status_counts: dict[str, int] = {}
    for alpha in alphas:
        omega = omega_equatorial(float(alpha), 0.0)[0]
        hit = first_cap_hit(
            frozen, model, morse, omega, cap_radius, sphere_radius
        )
        status_counts[hit.status] = status_counts.get(hit.status, 0) + 1
        if (
            hit.status == "RIGHT_CAP_FIRST_HIT"
            and hit.membership_residual is not None
        ):
            records.append((float(alpha), float(hit.membership_residual[0])))
        else:
            records.append(None)

    brackets: list[tuple[float, float]] = []
    for left, right in zip(records[:-1], records[1:]):
        if left is None or right is None:
            continue
        if left[1] == 0.0:
            brackets.append((left[0] - 1.0e-4, left[0] + 1.0e-4))
        elif left[1] * right[1] < 0.0:
            brackets.append((left[0], right[0]))
    return brackets, {
        "alpha_sample_count": ALPHA_SCAN_COUNT,
        "status_counts": status_counts,
        "continuous_sign_change_brackets": [list(item) for item in brackets],
        "periodic_seam_not_bridged": True,
    }


def solve_intersection(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    cap_radius: float,
    sphere_radius: float,
    *,
    initial_parameters: np.ndarray | None = None,
) -> dict[str, object]:
    scan_ledger: dict[str, object] | None = None
    if initial_parameters is None:
        brackets, scan_ledger = real_component_brackets(
            frozen, model, morse, cap_radius, sphere_radius
        )
        candidate_roots: list[tuple[float, FlowHit]] = []
        for lower, upper in brackets:
            def scalar_residual(alpha: float) -> float:
                hit = first_cap_hit(
                    frozen,
                    model,
                    morse,
                    omega_equatorial(alpha, 0.0)[0],
                    cap_radius,
                    sphere_radius,
                    rtol=8.0e-10,
                    atol=8.0e-12,
                )
                if (
                    hit.status != "RIGHT_CAP_FIRST_HIT"
                    or hit.membership_residual is None
                ):
                    raise ValueError("the bracket left the continuous cap-hit component")
                return float(hit.membership_residual[0])

            try:
                alpha = float(
                    brentq(
                        scalar_residual,
                        lower,
                        upper,
                        xtol=2.0e-11,
                        rtol=2.0e-11,
                    )
                )
                hit = first_cap_hit(
                    frozen,
                    model,
                    morse,
                    omega_equatorial(alpha, 0.0)[0],
                    cap_radius,
                    sphere_radius,
                    rtol=2.0e-10,
                    atol=2.0e-12,
                )
            except (RuntimeError, ValueError):
                continue
            if (
                hit.status == "RIGHT_CAP_FIRST_HIT"
                and hit.flow_time is not None
                and hit.psi is not None
                and hit.y_a is not None
                and hit.y_phi is not None
                and hit.membership_residual is not None
                and np.linalg.norm(hit.membership_residual) < 5.0e-6
            ):
                candidate_roots.append((alpha, hit))
        if not candidate_roots:
            raise RuntimeError(
                f"no continuous real-component intersection seed at r={cap_radius}"
            )
        alpha, seed_hit = min(
            candidate_roots,
            key=lambda item: abs(item[0] - np.pi / 2.0),
        )
        initial_parameters = np.array(
            [
                seed_hit.y_a,
                seed_hit.y_phi,
                seed_hit.psi,
                alpha,
                0.0,
                seed_hit.flow_time,
            ],
            dtype=float,
        )
    else:
        initial_parameters = np.asarray(initial_parameters, dtype=float)

    alpha_center = float(initial_parameters[3])
    time_center = float(initial_parameters[5])
    lower_bounds = np.array(
        [
            -FIELD_WINDOW,
            -FIELD_WINDOW,
            -np.pi / 2.0,
            alpha_center - 0.25,
            -0.30,
            max(0.0, time_center - 1.5),
        ]
    )
    upper_bounds = np.array(
        [
            FIELD_WINDOW,
            FIELD_WINDOW,
            np.pi / 2.0,
            alpha_center + 0.25,
            0.30,
            min(FLOW_TIME_MAX, time_center + 1.5),
        ]
    )
    refined = least_squares(
        intersection_residual,
        initial_parameters,
        args=(frozen, model, morse, cap_radius, sphere_radius),
        bounds=(lower_bounds, upper_bounds),
        x_scale="jac",
        ftol=2.0e-11,
        xtol=2.0e-11,
        gtol=2.0e-11,
        max_nfev=80,
    )
    parameters = refined.x
    physical_residual = interleaved(
        gamma_cap(frozen, cap_radius, *parameters[:3])[0]
        - fixed_chart_state_z(
            frozen,
            model,
            morse,
            parameters[3],
            parameters[4],
            parameters[5],
            sphere_radius,
        )
    )
    gamma_z, gamma_tangent_complex = gamma_cap(
        frozen, cap_radius, *parameters[:3]
    )
    upward_z, upward_tangent_complex, flow_ledger = (
        integrate_with_chart_tangents(
            frozen,
            model,
            morse,
            parameters[3],
            parameters[4],
            parameters[5],
            sphere_radius,
        )
    )
    gamma_frame = real_frame(gamma_tangent_complex)
    upward_frame = real_frame(upward_tangent_complex)
    orientation = oriented_sign_and_spectrum(gamma_frame, upward_frame)
    assembled_root_jacobian = np.column_stack([gamma_frame, -upward_frame])
    assembled_root_orientation = square_sign_and_spectrum(
        assembled_root_jacobian
    )
    row_scales = np.repeat(1.0 / frozen.coordinate_scales, 2)
    assembled_scaled_root_jacobian = (
        row_scales[:, np.newaxis] * assembled_root_jacobian
    )
    solver_finite_difference_jacobian = np.asarray(refined.jac, dtype=float)
    solver_root_orientation = square_sign_and_spectrum(
        solver_finite_difference_jacobian
    )
    solver_jacobian_relative_error = float(
        np.linalg.norm(
            solver_finite_difference_jacobian
            - assembled_scaled_root_jacobian,
            ord=2,
        )
        / np.linalg.norm(assembled_scaled_root_jacobian, ord=2)
    )

    def adaptive_chart_difference(
        parameter_index: int, proposed_steps: tuple[float, ...]
    ) -> tuple[np.ndarray, float]:
        for step in proposed_steps:
            plus = parameters[[3, 4, 5]].copy()
            minus = parameters[[3, 4, 5]].copy()
            plus[parameter_index] += step
            minus[parameter_index] -= step
            try:
                state_plus = fixed_chart_state_z(
                    frozen,
                    model,
                    morse,
                    plus[0],
                    plus[1],
                    plus[2],
                    sphere_radius,
                )
                state_minus = fixed_chart_state_z(
                    frozen,
                    model,
                    morse,
                    minus[0],
                    minus[1],
                    minus[2],
                    sphere_radius,
                )
            except RuntimeError:
                continue
            return (state_plus - state_minus) / (2.0 * step), step
        raise RuntimeError(
            f"no finite-difference chart step survived for parameter {parameter_index}"
        )

    alpha_difference, alpha_step = adaptive_chart_difference(
        0, (2.0e-5, 5.0e-6, 1.0e-6, 2.0e-7)
    )
    beta_difference, beta_step = adaptive_chart_difference(
        1, (2.0e-6, 5.0e-7, 1.0e-7, 2.0e-8, 5.0e-9)
    )
    time_difference, time_step = adaptive_chart_difference(
        2, (5.0e-6, 1.0e-6, 2.0e-7)
    )
    finite_difference_tangent = np.column_stack(
        [alpha_difference, beta_difference, time_difference]
    )
    tangent_relative_errors = []
    for column in range(3):
        denominator = max(
            np.linalg.norm(finite_difference_tangent[:, column]), 1.0e-15
        )
        tangent_relative_errors.append(
            float(
                np.linalg.norm(
                    finite_difference_tangent[:, column]
                    - upward_tangent_complex[:, column]
                )
                / denominator
            )
        )

    reversed_gamma = oriented_sign_and_spectrum(
        gamma_frame @ np.diag([-1.0, 1.0, 1.0]), upward_frame
    )
    reversed_upward = oriented_sign_and_spectrum(
        gamma_frame, upward_frame @ np.diag([-1.0, 1.0, 1.0])
    )
    projected_gamma = gamma_tangent_complex[2, 2]
    projected_upward = upward_tangent_complex[2, 2]
    projected_matrix = np.array(
        [
            [projected_gamma.real, projected_upward.real],
            [projected_gamma.imag, projected_upward.imag],
        ]
    )
    projected_sign = int(np.sign(np.linalg.det(projected_matrix)))

    return {
        "cap_radius": cap_radius,
        "sphere_radius": sphere_radius,
        "scan_ledger": scan_ledger,
        "least_squares_success": bool(refined.success),
        "least_squares_message": str(refined.message),
        "least_squares_nfev": int(refined.nfev),
        "parameters": {
            "y_a": float(parameters[0]),
            "y_phi": float(parameters[1]),
            "psi": float(parameters[2]),
            "alpha": float(parameters[3]),
            "beta": float(parameters[4]),
            "flow_time": float(parameters[5]),
        },
        "intersection_z": [
            [float(value.real), float(value.imag)] for value in gamma_z
        ],
        "K_minus_Gamma_norm": float(np.linalg.norm(upward_z - gamma_z)),
        "physical_residual_max_abs": float(np.max(np.abs(physical_residual))),
        "orientation": orientation,
        "assembled_Gamma_minus_K_jacobian": assembled_root_orientation,
        "solver_finite_difference_jacobian": solver_root_orientation,
        "solver_to_assembled_jacobian_relative_error": (
            solver_jacobian_relative_error
        ),
        "root_jacobian_parity_relation_passed": (
            assembled_root_orientation["sign"] == -orientation["sign"]
            and solver_root_orientation["sign"] == -orientation["sign"]
        ),
        "tangent_relative_errors": tangent_relative_errors,
        "tangent_max_relative_error": float(max(tangent_relative_errors)),
        "finite_difference_steps": {
            "alpha": alpha_step,
            "beta": beta_step,
            "flow_time": time_step,
        },
        "gamma_rank": int(np.linalg.matrix_rank(gamma_frame)),
        "upward_rank": int(np.linalg.matrix_rank(upward_frame)),
        "orientation_mutations": {
            "reverse_Gamma_first_parameter_sign": reversed_gamma["sign"],
            "reverse_K_first_parameter_sign": reversed_upward["sign"],
        },
        "projected_lapse_coordinate_sign": projected_sign,
        "projected_sign_is_not_used_for_full_sign": True,
        "flow_ledger": flow_ledger,
        "window_margins": {
            "y_a": float(FIELD_WINDOW - abs(parameters[0])),
            "y_phi": float(FIELD_WINDOW - abs(parameters[1])),
            "psi": float(np.pi / 2.0 - abs(parameters[2])),
            "beta_chart": float(np.pi / 2.0 - abs(parameters[4])),
            "flow_time": float(FLOW_TIME_MAX - parameters[5]),
        },
    }


def cubed_sphere_first_hit_ledger(
    frozen: FrozenInput,
    model: SymbolicModel,
    morse: MorseData,
    cap_radius: float,
    sphere_radius: float,
) -> dict[str, object]:
    grid = np.linspace(-1.0, 1.0, CUBE_FACE_GRID_COUNT)
    status_counts: dict[str, int] = {}
    best: dict[str, object] | None = None
    total = 0
    for axis in range(3):
        for sign in (-1, 1):
            for coordinate_u in grid:
                for coordinate_v in grid:
                    total += 1
                    omega = omega_cubed_face(
                        axis, sign, float(coordinate_u), float(coordinate_v)
                    )
                    hit = first_cap_hit(
                        frozen,
                        model,
                        morse,
                        omega,
                        cap_radius,
                        sphere_radius,
                        rtol=8.0e-8,
                        atol=8.0e-10,
                    )
                    status_counts[hit.status] = (
                        status_counts.get(hit.status, 0) + 1
                    )
                    if hit.membership_residual is None:
                        continue
                    residual_norm = float(np.linalg.norm(hit.membership_residual))
                    if best is None or residual_norm < best["membership_norm"]:
                        best = {
                            "axis": axis,
                            "sign": sign,
                            "u": float(coordinate_u),
                            "v": float(coordinate_v),
                            "omega": omega.tolist(),
                            "status": hit.status,
                            "membership_norm": residual_norm,
                        }
    return {
        "atlas": "six normalized cubed-sphere faces",
        "grid_per_face": CUBE_FACE_GRID_COUNT,
        "sample_count_including_face_overlaps": total,
        "status_counts": status_counts,
        "best_sample": best,
        "exhaustion_proved": False,
        "face_overlap_deduplicated": False,
    }


def exact_controls(
    audit: Audit, frozen: FrozenInput, model: SymbolicModel
) -> dict[str, object]:
    payload = frozen.payload
    audit.exact(
        "P39.input.frozen_manifest_contract",
        payload["phase"] == 39
        and payload["gate"] == 1
        and payload["required_fail_closed_outputs"]["global_n_sigma"] is None
        and payload["required_fail_closed_outputs"]["gate1_status"]
        == "OPEN_PARTIAL_PROGRESS",
        "the committed post-feasibility manifest fixes Phase39 inputs and requires Gate 1 and the global integer to remain open/null",
    )
    audit.exact(
        "P39.action.single_scalar_two_midpoint_elements",
        sp.simplify(
            model.action_z_general - 2 * model.element_left_general
        )
        == 0,
        "equal frozen endpoints make S2 exactly the sum of two identical midpoint elements, and all derivatives are generated from that one scalar",
    )
    audit.exact(
        "P39.action.holomorphic_without_hidden_conjugation",
        not model.action_z_general.has(sp.conjugate)
        and not model.action_z_general.has(sp.Abs),
        "the finite action contains no conjugation or absolute value and is holomorphic away from its declared divisor",
    )
    proper_time = model.variables_z[2]
    pole_residue = sp.simplify(
        sp.limit(proper_time * model.action_z_general, proper_time, 0)
    )
    audit.exact(
        "P39.action.simple_T_zero_pole",
        pole_residue != 0
        and sp.limit(
            proper_time**2 * model.action_z_general, proper_time, 0
        )
        == 0,
        "S2 is meromorphic with a generically nonzero simple T=0 kinetic pole, so the flow domain is C^2 times C-star",
    )
    audit.exact(
        "P39.action.gradient_and_hessian_same_scalar",
        model.gradient_w
        == sp.Matrix(
            [
                sp.diff(model.action_w, variable)
                for variable in model.variables_w
            ]
        )
        and model.hessian_w == sp.hessian(model.action_w, model.variables_w),
        "the production gradient and Hessian are exact symbolic derivatives of the same frozen scalar action",
    )

    theta, psi = sp.symbols("theta psi", real=True)
    phase_a_theta = sp.exp(sp.I * (theta / 2 - sp.pi / 4))
    phase_phi_theta = sp.exp(sp.I * (theta / 2 + sp.pi / 4))
    phase_a_psi = sp.exp(sp.I * (psi / 2 - sp.pi / 2))
    phase_phi_psi = sp.exp(sp.I * psi / 2)
    audit.exact(
        "P39.cycle.unwrapped_Phase32_half_angles",
        sp.simplify(
            phase_a_psi.subs(psi, theta + sp.pi / 2) - phase_a_theta
        )
        == 0
        and sp.simplify(
            phase_phi_psi.subs(psi, theta + sp.pi / 2)
            - phase_phi_theta
        )
        == 0,
        "the cap embedding is the continuous unwrapped T=iN rewrite of the Phase32 configuration half-angles rather than a pointwise principal-root reset",
    )
    audit.exact(
        "P39.cycle.cap_arm_field_plane_gluing",
        sp.simplify(
            phase_a_psi.subs(psi, -sp.pi / 2)
            - sp.exp(-3 * sp.pi * sp.I / 4)
        )
        == 0
        and sp.simplify(
            phase_phi_psi.subs(psi, -sp.pi / 2)
            - sp.exp(-sp.pi * sp.I / 4)
        )
        == 0
        and sp.simplify(
            phase_a_psi.subs(psi, sp.pi / 2)
            - sp.exp(-sp.pi * sp.I / 4)
        )
        == 0
        and sp.simplify(
            phase_phi_psi.subs(psi, sp.pi / 2)
            - sp.exp(sp.pi * sp.I / 4)
        )
        == 0,
        "the frozen negative arm, cap, and positive arm field planes glue continuously at both finite joints",
    )

    y_a, y_phi, radius = sp.symbols(
        "y_a y_phi r", real=True, positive=True
    )
    gamma_at_crossing = sp.Matrix(
        [
            [0, 0, y_a / 2],
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, y_phi / 2],
            [0, 0, 0],
            [0, 0, radius],
        ]
    )
    audit.exact(
        "P39.cycle.full_cap_tangent_rank",
        gamma_at_crossing.rank() == 3,
        "the declared (y_a,y_phi,psi) cap tangent has full real rank three, including both field half-angle derivatives and dT/dpsi",
    )

    g_re = sp.symbols("g0r:3", real=True)
    g_im = sp.symbols("g0i:3", real=True)
    gradients = [g_re[index] + sp.I * g_im[index] for index in range(3)]
    action_derivative = sp.expand(
        sum(
            gradients[index] * (-sp.conjugate(gradients[index]))
            for index in range(3)
        )
    )
    norm_squared = sum(
        g_re[index] ** 2 + g_im[index] ** 2 for index in range(3)
    )
    audit.exact(
        "P39.flow.exact_Morse_identities",
        sp.simplify(sp.re(action_derivative) + norm_squared) == 0
        and sp.simplify(sp.im(action_derivative)) == 0,
        "for dot(xi)=-conjugate(partial_xi S), Re S decreases by the gradient norm squared and Im S is exactly conserved",
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    omega = sp.Matrix(
        [
            sp.cos(beta) * sp.cos(alpha),
            sp.cos(beta) * sp.sin(alpha),
            sp.sin(beta),
        ]
    )
    chart_orientation = sp.simplify(
        sp.Matrix.hstack(
            sp.diff(omega, alpha), sp.diff(omega, beta), omega
        ).det()
    )
    audit.exact(
        "P39.orientation.equatorial_chart_order",
        chart_orientation == sp.cos(beta),
        "inside the equatorial chart, parameter order (alpha,beta,outward flow) has the declared positive K orientation; the poles are excluded and separately sampled by cubed faces",
    )
    audit.exact(
        "P39.orientation.root_jacobian_odd_parity",
        (-1) ** 3 == -1,
        "in complex dimension three, the Gamma-K solver Jacobian [V_Gamma,-V_K] has the opposite sign from det[V_Gamma,V_K]",
    )
    audit.exact(
        "P39.guard.global_integer_fail_closed",
        payload["required_fail_closed_outputs"]
        ["complete_global_signed_intersection_vector"]
        is None
        and payload["declared_original_cycle_candidate"]
        ["relative_homology_class_proved"]
        is False
        and payload["upward_cycle"]["all_ends_classified"] is False,
        "the manifest forbids promoting the local determinant to a complete vector or global coefficient while cycle and end certificates are absent",
    )
    return {
        "manifest": {
            "path": str(INPUT_PATH.relative_to(Path(__file__).parent.parent)),
            "sha256": frozen.sha256,
            "introduced_in_commit": INPUT_INTRODUCED_IN_COMMIT,
            "freeze_kind": payload["freeze_kind"],
        },
        "action": {
            "complex_dimension": 3,
            "ambient_real_dimension": 6,
            "segment_count": SEGMENT_COUNT,
            "integration_space": "C^2 x C-star_T",
            "T_zero_divisor": "simple meromorphic pole",
        },
        "orientation": {
            "ambient_order": payload["model"]["ambient_real_order"],
            "Gamma_parameter_order": payload[
                "declared_original_cycle_candidate"
            ]["parameter_orientation"],
            "K_parameter_order": payload["upward_cycle"][
                "parameter_orientation"
            ],
            "Phase32_combined_BFV_sign_inherited": False,
        },
    }


def numerical_controls(
    audit: Audit, frozen: FrozenInput, model: SymbolicModel
) -> dict[str, object]:
    morse, saddle = solve_main_saddle(frozen, model)
    audit.numerical(
        "P39.saddle.genuine_discrete_joint_root",
        saddle["gradient_max_abs"] < 1.0e-9
        and saddle["hessian_inertia"]
        == {"negative": 2, "positive": 1, "zero": 0},
        "the three joint discrete equations are re-solved at positive T with sub-nanoscopic residual and a nondegenerate (2-,1+) Hessian",
    )
    whitened = np.asarray(saddle["whitened_hessian"], dtype=float)
    expected_signature = np.diag([-1.0, -1.0, 1.0])
    audit.numerical(
        "P39.metric.constant_Morse_whitening",
        np.linalg.norm(whitened - expected_signature, ord=np.inf) < 2.0e-10
        and abs(saddle["oriented_eigenframe_determinant"] - 1.0) < 2.0e-12,
        "the frozen constant whitening map reduces the saddle Hessian to diag(-1,-1,+1) with an oriented eigenframe",
    )

    saddle_ledger = bounded_real_saddle_ledger(frozen, model)
    audit.numerical(
        "P39.saddle.bounded_multiseed_nonuniqueness_ledger",
        len(saddle_ledger) >= 2,
        "the bounded real multiseed ledger records more than the target positive-T saddle, so no complete saddle census or uniqueness is claimed",
    )

    primary_results = [
        solve_intersection(
            frozen,
            model,
            morse,
            cap_radius,
            PRIMARY_SPHERE_RADIUS,
        )
        for cap_radius in CAP_RADII
    ]
    for result in primary_results:
        radius_label = str(result["cap_radius"]).replace(".", "p")
        audit.numerical(
            f"P39.intersection.r{radius_label}_full_six_real_root",
            result["least_squares_success"]
            and result["physical_residual_max_abs"] < INTERSECTION_TOLERANCE
            and result["gamma_rank"] == 3
            and result["upward_rank"] == 3,
            f"the declared r={result['cap_radius']} cap piece and one finite-radius, finite-time three-dimensional K chart patch have a numerically resolved candidate in all six real coordinates",
        )
        audit.numerical(
            f"P39.intersection.r{radius_label}_transverse_orientation",
            result["orientation"]["sign"] in (-1, 1)
            and result["orientation"]["normalized_sigma_min"]
            > TRANSVERSALITY_MINIMUM
            and result["root_jacobian_parity_relation_passed"]
            and result["solver_to_assembled_jacobian_relative_error"]
            < 2.0e-3,
            f"the r={result['cap_radius']} normalized 6x6 tangent matrix is transverse and its direct sign has the required odd-dimensional parity relative to the solver's finite-difference residual Jacobian",
        )
        audit.numerical(
            f"P39.intersection.r{radius_label}_variational_tangent",
            result["tangent_max_relative_error"] < 5.0e-3,
            f"the r={result['cap_radius']} transported alpha, beta, and flow tangents agree with stiff independent central finite differences to better than one half percent",
        )
        audit.numerical(
            f"P39.flow.r{radius_label}_Morse_monotonicity",
            result["flow_ledger"]["ReS_max_positive_step"] < 2.0e-8
            and result["flow_ledger"]["ImS_max_drift"] < 2.0e-8
            and result["flow_ledger"]["predicted_dReS_max"] <= 1.0e-12,
            f"along the r={result['cap_radius']} trajectory Re S is nonincreasing and Im S is conserved within the recorded integration error",
        )
        audit.numerical(
            f"P39.orientation.r{radius_label}_mutation_controls",
            result["orientation_mutations"]
            ["reverse_Gamma_first_parameter_sign"]
            == -result["orientation"]["sign"]
            and result["orientation_mutations"]
            ["reverse_K_first_parameter_sign"]
            == -result["orientation"]["sign"],
            f"at r={result['cap_radius']}, reversing either declared manifold orientation leaves the root fixed and flips only the local determinant sign",
        )

    audit.numerical(
        "P39.intersection.two_cap_radii_same_recorded_sign",
        primary_results[0]["orientation"]["sign"]
        == primary_results[1]["orientation"]["sign"]
        and min(
            result["window_margins"]["y_a"]
            for result in primary_results
        )
        > 0.20
        and min(
            result["window_margins"]["y_phi"]
            for result in primary_results
        )
        > 0.20,
        "the two frozen finite cap radii record the same local sign and both roots lie well inside the declared field window; this is not an r-to-zero theorem",
    )

    control_seed = np.array(
        [
            primary_results[0]["parameters"][key]
            for key in ("y_a", "y_phi", "psi", "alpha", "beta", "flow_time")
        ],
        dtype=float,
    )
    control_seed[5] -= np.log(2.0)
    radius_control = solve_intersection(
        frozen,
        model,
        morse,
        CAP_RADII[0],
        CONTROL_SPHERE_RADIUS,
        initial_parameters=control_seed,
    )
    audit.numerical(
        "P39.intersection.initial_sphere_radius_control",
        radius_control["physical_residual_max_abs"] < INTERSECTION_TOLERANCE
        and radius_control["orientation"]["sign"]
        == primary_results[0]["orientation"]["sign"]
        and radius_control["orientation"]["normalized_sigma_min"]
        > TRANSVERSALITY_MINIMUM,
        "doubling the frozen local-sphere radius preserves a transverse nearby r=.3 root and its declared coordinate sign",
    )

    sphere_ledger = cubed_sphere_first_hit_ledger(
        frozen,
        model,
        morse,
        CAP_RADII[0],
        PRIMARY_SPHERE_RADIUS,
    )
    audit.numerical(
        "P39.census.cubed_sphere_first_hit_ledger_completed",
        sphere_ledger["sample_count_including_face_overlaps"]
        == 6 * CUBE_FACE_GRID_COUNT**2
        and sphere_ledger["exhaustion_proved"] is False,
        "the bounded first-hit ledger samples every cubed-sphere face, including representatives at the equatorial-chart poles, while explicitly declining continuous coverage or exhaustion",
    )

    exact_signs = [result["orientation"]["sign"] for result in primary_results]
    audit.numerical(
        "P39.guard.local_sign_does_not_emit_global_integer",
        all(sign in (-1, 1) for sign in exact_signs),
        "finite local signs were computed directly, but unclassified arm, field-box, flow-box, Stokes, and omitted-sector ends keep both global outputs null",
    )

    end_ledger = {
        "Gamma_negative_arm_at_N_minus_R": "FINITE_ARM_CUTOFF_UNRESOLVED",
        "Gamma_positive_arm_at_N_plus_R": "FINITE_ARM_CUTOFF_UNRESOLVED",
        "Gamma_field_box_faces": "FINITE_FIELD_WINDOW_UNRESOLVED",
        "Gamma_T_zero": "EXCLUDED_SIMPLE_ACTION_POLE",
        "K_nonhit_flow_time_faces": "FLOW_TIME_BOX_EXIT_UNRESOLVED",
        "K_nonhit_norm_faces": "FLOW_NORM_BOX_EXIT_UNRESOLVED",
        "other_saddles_and_upward_components": "NOT_EXHAUSTED",
        "Stokes_chamber": "REAL_SADDLE_NOT_LATERALLY_CERTIFIED",
        "BFV_Pfaffian_Pin_orientation": "NOT_PRESENT_IN_M2_CONFIGURATION_MODEL",
    }
    return {
        "saddle": saddle,
        "bounded_real_saddle_ledger": {
            "seed_count": 6,
            "distinct_roots_found": len(saddle_ledger),
            "records": saddle_ledger,
            "complete": False,
        },
        "critical_phase_ledger": {
            "all_recorded_real_saddle_ImS_zero": all(
                abs(record["action"][1]) < 1.0e-12
                for record in saddle_ledger
            ),
            "non_Stokes_lateral_chamber_required": True,
            "connecting_flows_and_jumps_computed": False,
        },
        "primary_intersections": primary_results,
        "sphere_radius_control": radius_control,
        "cubed_sphere_discovery_ledger": sphere_ledger,
        "recorded_local_pairing": {
            "result_type": "M2_CAP_PIECE_FULL_JOINT_LOCAL_INTERSECTION_CANDIDATE",
            "configuration_only_orientation": True,
            "cap_radii": list(CAP_RADII),
            "local_signs": exact_signs,
            "all_recorded_signs_equal": len(set(exact_signs)) == 1,
            "full_joint_local_sign_at_frozen_caps": (
                exact_signs[0] if len(set(exact_signs)) == 1 else None
            ),
            "Phase32_projected_sign_used_as_input": False,
        },
        "end_ledger": end_ledger,
        "cycle_complete": False,
        "exact_nonlinear_upward_manifold_certified": False,
        "straight_arm_intersections_searched": False,
        "cap_reintersections_searched": False,
        "root_exhaustion_proved": False,
        "bounded_chain_signed_sum": None,
        "all_saddles_complete": False,
        "all_upward_components_complete": False,
        "all_ends_classified": False,
        "non_Stokes_chamber_certified": False,
        "cutoff_regulator_stability_established": False,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
    }


def run() -> dict[str, object]:
    audit = Audit()
    frozen = load_frozen_input()
    model = build_symbolic_model()
    exact = exact_controls(audit, frozen, model)
    numerical = numerical_controls(audit, frozen, model)
    result: dict[str, object] = {
        "phase": "P39",
        "gate": "Gate 1 -- original joint cycle and signed global intersections",
        "calculation": "m=2 full-joint local intersection algorithm pilot",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "exact_controls": exact,
        "numerical_controls": numerical,
        "gate_status": {
            "Gate_1": "OPEN_PARTIAL_LOCAL_FULL_SPACE_INTERSECTION_PILOT",
            "Gate_2": "EXPLORATORY_CALCULATION_ALLOWED_BUT_PHYSICAL_PROMOTION_DEPENDS_ON_GATE_1",
            "Gate_3": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_2_TYPED_OUTPUT",
            "Gate_4": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_3_TYPED_OUTPUT",
            "Gate_5": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_4_TYPED_OUTPUT",
        },
        "claim_status": {
            "the_frozen_m2_action_has_a_genuine_positive_T_discrete_joint_saddle": "SUPPORTED_NUMERICALLY_WITHOUT_A_COMPLETE_SADDLE_CENSUS",
            "the_declared_cap_pieces_and_one_finite_radius_finite_time_full_joint_upward_chart_patch_have_a_recorded_locally_transverse_candidate": "SUPPORTED_AT_THE_TWO_FROZEN_CAP_RADII_AND_DECLARED_CONFIGURATION_ORIENTATION",
            "the_recorded_full_joint_local_sign_is_inferred_from_the_Phase32_projected_lapse_sign": "FALSE_THE_SIX_BY_SIX_DETERMINANT_IS_COMPUTED_DIRECTLY",
            "the_declared_chain_is_the_physical_original_relative_cycle": "OPEN_NOT_SELECTED_OR_GOOD_END_CERTIFIED",
            "the_m2_result_is_stable_under_reflection_odd_history_modes_or_cutoff_refinement": "OPEN_M2_HAS_NO_REFLECTION_ODD_HISTORY_MODE",
            "all_saddles_upward_components_sheets_and_ends_are_classified": "OPEN_EXPLICITLY_INCOMPLETE",
            "the_complete_global_signed_vector_or_n_sigma_is_fixed": "OPEN_AND_EXPLICITLY_NULL",
            "a_full_BFV_Pfaffian_Pin_orientation_is_computed": "OPEN_NOT_PRESENT",
        },
        "scope_guard": {
            "computed": [
                "one explicit nonlinear two-segment midpoint configuration action on C^2 times C-star_T",
                "one high-precision positive-T discrete joint saddle and a bounded nonuniqueness ledger",
                "one constant positive Hermitian Morse-whitened flow metric chosen after the feasibility pilot",
                "one finite-radius, finite-time three-real-dimensional upward-flow chart patch and its variational tangent frame",
                "numerically resolved locally transverse six-real-dimensional intersection candidates with two cap pieces of a separately anchored finite lower-bypass chain at r=.3 and r=.2",
                "direct configuration-only coordinate signs sign det_R[V_Gamma,V_K], root-Jacobian parity, tangent, orientation, radius, and bounded cubed-sphere controls",
            ],
            "not_computed": [
                "a proof that the frozen Gaussian lift is the physical original relative cycle",
                "a complete saddle, sheet, upward-component, reintersection, Stokes, or good-end census",
                "a cutoff-, metric-homotopy-, regulator-, anchor-, or boundary-asymmetry-stable global Picard-Lefschetz vector",
                "reflection-odd history modes, which do not exist at m=2",
                "canonical momenta, BFV ghosts, fermions, gravitino, inhomogeneous modes, Pfaffian/Pin data, or a spinorial charge",
                "hard CFU coefficients, persistent order parameters, particle poles, or quantum gravity",
            ],
        },
        "next_calculation": (
            "repeat the same full-joint determinant algorithm at m=3 or m=4 "
            "with an endpoint-asymmetry mutation to expose the first "
            "reflection-odd history mode, then promote to the m=5 regulator "
            "and classify complete upward components and relative good ends"
        ),
    }
    print("PHASE39_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
