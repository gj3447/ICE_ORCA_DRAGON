#!/usr/bin/env python3
"""Phase 25 -- fixed-boundary lapse scan for the Phase-24 interval.

The executable keeps the two Phase-24 boundaries fixed, solves the *full*
fixed-lapse Euler--Lagrange boundary problem, and studies the Hamilton
principal function W(T).  It also integrates the variational equations,
continues one reflection-symmetric real branch to its first recorded fold,
and constructs a local constant-phase complex-T segment through T=0.7.

This is a bounded minisuperspace calculation.  It does not compute a global
Picard--Lefschetz intersection number, prove uniqueness of real branches, or
construct a gravitational density matrix.  The program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

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

    def numerical(self, check_id: str, condition: bool, statement: str) -> None:
        self._unique(check_id)
        if not condition:
            raise AssertionError(f"[NUMERIC FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")

    def _unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"duplicate check id: {check_id}")


SQRT_TWO_THIRDS = float(np.sqrt(2.0 / 3.0))
TWO_PI_SQUARED = float(2.0 * np.pi**2)


def potential(phi: complex | np.ndarray) -> complex | np.ndarray:
    return 0.75 * (1.0 - np.exp(-SQRT_TWO_THIRDS * phi)) ** 2


def potential_prime(phi: complex | np.ndarray) -> complex | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return 1.5 * SQRT_TWO_THIRDS * exponential * (1.0 - exponential)


def potential_second(phi: complex | np.ndarray) -> complex | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return -exponential + 2.0 * exponential**2


def action_lagrangian(state: np.ndarray) -> complex:
    scale, scale_velocity, phi, phi_velocity = state[:4]
    return TWO_PI_SQUARED * (
        -3.0 * scale * (scale_velocity**2 + 1.0)
        + scale**3 * (0.5 * phi_velocity**2 + potential(phi))
    )


def configuration_rhs(state: np.ndarray) -> np.ndarray:
    """Full off-constraint Euler--Lagrange flow in proper-time gauge."""

    scale, scale_velocity, phi, phi_velocity = state[:4]
    return np.asarray(
        [
            scale_velocity,
            (1.0 - scale_velocity**2) / (2.0 * scale)
            - scale * phi_velocity**2 / 4.0
            - scale * potential(phi) / 2.0,
            phi_velocity,
            potential_prime(phi)
            - 3.0 * scale_velocity * phi_velocity / scale,
        ],
        dtype=np.result_type(state.dtype, np.complex128)
        if np.iscomplexobj(state)
        else float,
    )


def variational_matrix(state: np.ndarray) -> np.ndarray:
    scale, scale_velocity, phi, phi_velocity = map(float, state[:4])
    return np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [
                -(1.0 - scale_velocity**2) / (2.0 * scale**2)
                - phi_velocity**2 / 4.0
                - potential(phi) / 2.0,
                -scale_velocity / scale,
                -scale * potential_prime(phi) / 2.0,
                -scale * phi_velocity / 2.0,
            ],
            [0.0, 0.0, 0.0, 1.0],
            [
                3.0 * scale_velocity * phi_velocity / scale**2,
                -3.0 * phi_velocity / scale,
                potential_second(phi),
                -3.0 * scale_velocity / scale,
            ],
        ],
        dtype=float,
    )


def constraint(state: np.ndarray) -> float:
    scale, scale_velocity, phi, phi_velocity = map(float, state[:4])
    return float(
        scale_velocity**2
        - 1.0
        - scale**2 * (0.5 * phi_velocity**2 - potential(phi)) / 3.0
    )


def energy(state: np.ndarray) -> float:
    return float(-6.0 * np.pi**2 * state[0] * constraint(state))


def real_flow(
    initial: np.ndarray,
    proper_length: float,
    *,
    monodromy: bool = False,
) -> tuple[np.ndarray, np.ndarray | None]:
    """Integrate the real flow, action, and optionally the 4x4 monodromy."""

    state0 = np.asarray(initial, dtype=float)
    if monodromy:
        augmented0 = np.concatenate([state0, [0.0], np.eye(4).ravel()])

        def rhs(_tau: float, augmented: np.ndarray) -> np.ndarray:
            state = augmented[:4]
            matrix = augmented[5:].reshape(4, 4)
            return np.concatenate(
                [
                    configuration_rhs(state),
                    [action_lagrangian(state)],
                    (variational_matrix(state) @ matrix).ravel(),
                ]
            )

    else:
        augmented0 = np.concatenate([state0, [0.0]])

        def rhs(_tau: float, augmented: np.ndarray) -> np.ndarray:
            state = augmented[:4]
            return np.concatenate(
                [configuration_rhs(state), [action_lagrangian(state)]]
            )

    solution = solve_ivp(
        rhs,
        (0.0, proper_length),
        augmented0,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=min(0.04, max(proper_length / 40.0, 2e-4)),
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]
    matrix = final[5:].reshape(4, 4) if monodromy else None
    return final[:5], matrix


def benchmark() -> tuple[np.ndarray, np.ndarray, float]:
    phi_center = 1.0
    half_length = 0.35
    scale_center = float(np.sqrt(3.0 / potential(phi_center)))
    half_final, _ = real_flow(
        np.array([scale_center, 0.0, phi_center, 0.0]), half_length
    )
    boundary = np.array(
        [half_final[0], half_final[2], half_final[0], half_final[2]]
    )
    left_velocity = -half_final[[1, 3]]
    return boundary, left_velocity, float(2.0 * half_final[4])


@dataclass(frozen=True)
class FixedTimeSolution:
    proper_length: float
    velocity: np.ndarray
    action: float
    endpoint_residual: float
    energy: float
    constraint: float
    velocity_monodromy: np.ndarray


def solve_fixed_time(
    proper_length: float,
    boundary: np.ndarray,
    velocity_guess: np.ndarray,
) -> FixedTimeSolution:
    left_scale, left_phi, right_scale, right_phi = boundary

    def residual(velocity: np.ndarray) -> np.ndarray:
        final, _ = real_flow(
            np.array([left_scale, velocity[0], left_phi, velocity[1]]),
            proper_length,
        )
        return final[[0, 2]] - np.array([right_scale, right_phi])

    root_result = root(residual, velocity_guess, method="hybr", tol=1e-11)
    residual_norm = float(np.linalg.norm(residual(root_result.x)))
    if residual_norm > 2e-8:
        raise RuntimeError(
            f"fixed-time BVP failed at T={proper_length}: {residual_norm}"
        )
    initial = np.array(
        [left_scale, root_result.x[0], left_phi, root_result.x[1]]
    )
    final, monodromy = real_flow(initial, proper_length, monodromy=True)
    assert monodromy is not None
    velocity_block = monodromy[np.ix_([0, 2], [1, 3])]
    return FixedTimeSolution(
        proper_length=proper_length,
        velocity=root_result.x.copy(),
        action=float(final[4]),
        endpoint_residual=residual_norm,
        energy=energy(initial),
        constraint=constraint(initial),
        velocity_monodromy=velocity_block,
    )


def midpoint_endpoint(
    center: np.ndarray,
    proper_length: float,
    *,
    monodromy: bool = False,
) -> tuple[np.ndarray, np.ndarray | None]:
    return real_flow(
        np.array([center[0], 0.0, center[1], 0.0]),
        proper_length / 2.0,
        monodromy=monodromy,
    )


def solve_symmetric_center(
    proper_length: float,
    boundary: np.ndarray,
    center_guess: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    target = boundary[:2]

    def residual(center: np.ndarray) -> np.ndarray:
        endpoint, _ = midpoint_endpoint(center, proper_length)
        return endpoint[[0, 2]] - target

    root_result = root(residual, center_guess, method="hybr", tol=1e-11)
    residual_norm = float(np.linalg.norm(residual(root_result.x)))
    if residual_norm > 2e-8:
        raise RuntimeError(
            f"symmetric continuation failed at T={proper_length}: "
            f"{residual_norm}"
        )
    endpoint, _ = midpoint_endpoint(root_result.x, proper_length)
    return root_result.x.copy(), endpoint


def center_jacobian(center: np.ndarray, proper_length: float) -> np.ndarray:
    _endpoint, monodromy = midpoint_endpoint(
        center, proper_length, monodromy=True
    )
    assert monodromy is not None
    return monodromy[np.ix_([0, 2], [0, 2])]


def locate_symmetric_fold(boundary: np.ndarray) -> dict[str, object]:
    target = boundary[:2]

    def residual(unknown: np.ndarray) -> np.ndarray:
        center = unknown[:2]
        proper_length = float(unknown[2])
        endpoint, _ = midpoint_endpoint(center, proper_length)
        jacobian = center_jacobian(center, proper_length)
        return np.array(
            [
                endpoint[0] - target[0],
                endpoint[2] - target[1],
                np.linalg.det(jacobian),
            ]
        )

    fold_root = root(
        residual, np.array([1.248, 0.10017, 9.78863]), tol=2e-11
    )
    if np.linalg.norm(residual(fold_root.x)) > 2e-8:
        raise RuntimeError("symmetric fold solve failed")
    center = fold_root.x[:2]
    proper_length = float(fold_root.x[2])
    endpoint, _ = midpoint_endpoint(center, proper_length)
    center_block = center_jacobian(center, proper_length)
    left_vectors, _center_singular_values, right_vectors = np.linalg.svd(
        center_block
    )
    left_null = left_vectors[:, -1]
    right_null = right_vectors[-1]
    half_length_derivative = configuration_rhs(endpoint[:4])[[0, 2]]
    # Singular vectors are defined only up to an overall sign.  The fold
    # gate uses invariant magnitudes so a BLAS sign convention cannot turn a
    # valid run into a false failure.
    fold_time_transversality = abs(
        float(left_null @ half_length_derivative)
    )
    second_step = 1e-3
    plus_endpoint, _ = midpoint_endpoint(
        center + second_step * right_null, proper_length
    )
    minus_endpoint, _ = midpoint_endpoint(
        center - second_step * right_null, proper_length
    )
    second_directional = (
        plus_endpoint[[0, 2]]
        - 2.0 * endpoint[[0, 2]]
        + minus_endpoint[[0, 2]]
    ) / second_step**2
    fold_quadratic_transversality = abs(
        float(left_null @ second_directional)
    )
    left_velocity = -endpoint[[1, 3]]
    fold_solution = solve_fixed_time(
        proper_length, boundary, left_velocity
    )
    fold_singular_values = np.linalg.svd(
        fold_solution.velocity_monodromy, compute_uv=False
    )

    branch_time = 9.78
    upper_center, upper_endpoint = solve_symmetric_center(
        branch_time, boundary, np.array([1.36, 0.092])
    )
    lower_center, lower_endpoint = solve_symmetric_center(
        branch_time, boundary, np.array([1.14, 0.110])
    )
    upper = solve_fixed_time(
        branch_time, boundary, -upper_endpoint[[1, 3]]
    )
    lower = solve_fixed_time(
        branch_time, boundary, -lower_endpoint[[1, 3]]
    )
    return {
        "center": center.tolist(),
        "proper_length": proper_length,
        "residual": residual(fold_root.x).tolist(),
        "center_jacobian": center_block.tolist(),
        "center_singular_values": np.linalg.svd(
            center_block, compute_uv=False
        ).tolist(),
        "right_null_vector": right_null.tolist(),
        "left_null_vector": left_null.tolist(),
        "half_length_transversality": fold_time_transversality,
        "quadratic_transversality": fold_quadratic_transversality,
        "full_velocity_monodromy_singular_values": fold_singular_values.tolist(),
        "full_velocity_monodromy_singular_ratio": float(
            fold_singular_values[1] / fold_singular_values[0]
        ),
        "bracket_time": branch_time,
        "bracket_centers": [upper_center.tolist(), lower_center.tolist()],
        "bracket_velocity_monodromy_determinants": [
            float(np.linalg.det(upper.velocity_monodromy)),
            float(np.linalg.det(lower.velocity_monodromy)),
        ],
        "bracket_actions": [upper.action, lower.action],
    }


def complex_flow(
    proper_length: complex,
    boundary: np.ndarray,
    velocity: np.ndarray,
) -> np.ndarray:
    """Integrate on s in [0,1], with d/ds = T d/dtau."""

    initial = np.array(
        [boundary[0], velocity[0], boundary[1], velocity[1], 0.0j],
        dtype=np.complex128,
    )

    def rhs(_s: float, augmented: np.ndarray) -> np.ndarray:
        state = augmented[:4]
        return proper_length * np.concatenate(
            [configuration_rhs(state), [action_lagrangian(state)]]
        )

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        initial,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=0.025,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1]


def constant_phase_point(
    imaginary_time: float,
    boundary: np.ndarray,
    guess: np.ndarray,
) -> tuple[np.ndarray, complex, np.ndarray]:
    """Solve endpoints plus Im W=0 at fixed Im T."""

    def residual(unknown: np.ndarray) -> np.ndarray:
        proper_length = complex(unknown[0], imaginary_time)
        velocity = np.array(
            [complex(unknown[1], unknown[2]), complex(unknown[3], unknown[4])]
        )
        final = complex_flow(proper_length, boundary, velocity)
        endpoint_delta = final[[0, 2]] - boundary[2:]
        return np.array(
            [
                endpoint_delta[0].real,
                endpoint_delta[0].imag,
                endpoint_delta[1].real,
                endpoint_delta[1].imag,
                final[4].imag,
            ]
        )

    root_result = root(residual, guess, method="hybr", tol=1e-11)
    residual_norm = float(np.linalg.norm(residual(root_result.x)))
    if residual_norm > 3e-8:
        raise RuntimeError(
            f"constant-phase solve failed at Im T={imaginary_time}: "
            f"{residual_norm}"
        )
    unknown = root_result.x
    proper_length = complex(unknown[0], imaginary_time)
    velocity = np.array(
        [complex(unknown[1], unknown[2]), complex(unknown[3], unknown[4])]
    )
    final = complex_flow(proper_length, boundary, velocity)
    return unknown.copy(), proper_length, final


def augmented_principal_gradient(
    boundary_and_time: np.ndarray,
    velocity_guess: np.ndarray,
) -> np.ndarray:
    """Return (partial_q W, partial_T W)=(-p_-,p_+,-E)."""

    boundary = np.asarray(boundary_and_time[:4], dtype=float)
    proper_length = float(boundary_and_time[4])
    left_scale, left_phi, right_scale, right_phi = boundary

    def residual(velocity: np.ndarray) -> np.ndarray:
        final, _ = real_flow(
            np.array([left_scale, velocity[0], left_phi, velocity[1]]),
            proper_length,
        )
        return final[[0, 2]] - np.array([right_scale, right_phi])

    root_result = root(residual, velocity_guess, method="hybr", tol=1e-11)
    if np.linalg.norm(residual(root_result.x)) > 2e-8:
        raise RuntimeError("augmented principal-gradient BVP failed")
    initial = np.array(
        [left_scale, root_result.x[0], left_phi, root_result.x[1]]
    )
    final, _ = real_flow(initial, proper_length)
    boundary_gradient = np.array(
        [
            12.0 * np.pi**2 * left_scale * root_result.x[0],
            -2.0 * np.pi**2 * left_scale**3 * root_result.x[1],
            -12.0 * np.pi**2 * right_scale * final[1],
            2.0 * np.pi**2 * right_scale**3 * final[3],
        ]
    )
    return np.concatenate([boundary_gradient, [-energy(initial)]])


def five_point_augmented_hessian(
    boundary: np.ndarray,
    proper_length: float,
    velocity_guess: np.ndarray,
    step: float,
) -> np.ndarray:
    base = np.concatenate([boundary, [proper_length]])
    identity = np.eye(5)
    hessian = np.empty((5, 5), dtype=float)
    for column in range(5):
        direction = identity[column]
        hessian[:, column] = (
            augmented_principal_gradient(
                base - 2.0 * step * direction, velocity_guess
            )
            - 8.0
            * augmented_principal_gradient(
                base - step * direction, velocity_guess
            )
            + 8.0
            * augmented_principal_gradient(
                base + step * direction, velocity_guess
            )
            - augmented_principal_gradient(
                base + 2.0 * step * direction, velocity_guess
            )
        ) / (12.0 * step)
    return hessian


def exact_controls(audit: Audit) -> dict[str, object]:
    scale, scale_dot, phi_dot, symbolic_v = sp.symbols(
        "a adot phidot V", real=True, finite=True
    )
    symbolic_constraint = (
        scale_dot**2
        - 1
        - scale**2 * (phi_dot**2 / 2 - symbolic_v) / 3
    )
    full_scale_eom = (
        (1 - scale_dot**2) / (2 * scale)
        - scale * phi_dot**2 / 4
        - scale * symbolic_v / 2
    )
    reduced_scale_eom = -scale * (phi_dot**2 + symbolic_v) / 3
    audit.exact(
        "P25.action.full_off_shell_scale_equation",
        sp.simplify(
            full_scale_eom
            - reduced_scale_eom
            + symbolic_constraint / (2 * scale)
        )
        == 0,
        "the fixed-lapse scan uses the full scale equation rather than its C=0 reduction",
    )

    lagrangian = 2 * sp.pi**2 * (
        -3 * scale * (scale_dot**2 + 1)
        + scale**3 * (phi_dot**2 / 2 + symbolic_v)
    )
    p_scale = sp.diff(lagrangian, scale_dot)
    p_phi = sp.diff(lagrangian, phi_dot)
    energy_expression = sp.expand(
        p_scale * scale_dot + p_phi * phi_dot - lagrangian
    )
    audit.exact(
        "P25.action.energy_constraint_identity",
        sp.simplify(
            energy_expression + 6 * sp.pi**2 * scale * symbolic_constraint
        )
        == 0,
        "the conserved fixed-lapse energy is E=-6 pi^2 a C",
    )
    audit.exact(
        "P25.action.HJ_time_derivative_sign",
        sp.simplify(-energy_expression - 6 * sp.pi**2 * scale * symbolic_constraint)
        == 0,
        "Hamilton-Jacobi gives dW/dT=-E=6 pi^2 a C",
    )

    phi, b = sp.symbols("phi b", real=True)
    symbolic_potential = sp.Rational(3, 4) * (1 - sp.exp(-b * phi)) ** 2
    audit.exact(
        "P25.jacobi.starobinsky_second_derivative",
        sp.simplify(
            sp.diff(symbolic_potential, phi, 2).subs(b**2, sp.Rational(2, 3))
            - (-sp.exp(-b * phi) + 2 * sp.exp(-2 * b * phi))
        )
        == 0,
        "the variational flow uses the exact Starobinsky V''",
    )

    mu, displacement = sp.symbols("mu y", positive=True, real=True)
    real_quadratic = -mu * displacement**2 / 2
    imaginary_quadratic = sp.simplify(
        -mu * (sp.I * displacement) ** 2 / 2
    )
    audit.exact(
        "P25.thimble.local_steepest_direction",
        real_quadratic < 0 and imaginary_quadratic > 0,
        "for W_TT<0, real delta T lowers Re W while imaginary delta T raises it",
    )
    return {
        "action": "W=2pi^2 integral[-3a(a_dot^2+1)+a^3(phi_dot^2/2+V)]d tau",
        "potential": "V=3/4[1-exp(-sqrt(2/3)phi)]^2",
        "time_identity": "dW/dT=-E=6pi^2 a C",
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, base_velocity, benchmark_action = benchmark()
    base = solve_fixed_time(0.7, boundary, base_velocity)
    audit.numerical(
        "P25.saddle.base_stationarity",
        base.endpoint_residual < 2e-10
        and abs(base.constraint) < 2e-11
        and abs(base.action - benchmark_action) < 2e-10,
        "the Phase-24 fixed boundary has a stationary fixed-lapse solution at T=0.7",
    )

    local_cache: dict[float, FixedTimeSolution] = {0.7: base}

    def local_solution(time: float) -> FixedTimeSolution:
        key = round(float(time), 12)
        if key not in local_cache:
            local_cache[key] = solve_fixed_time(time, boundary, base_velocity)
        return local_cache[key]

    derivative_errors = []
    derivative_samples = []
    derivative_step = 2e-4
    for time in (0.6, 0.8):
        minus = local_solution(time - derivative_step)
        plus = local_solution(time + derivative_step)
        center = local_solution(time)
        action_derivative = (plus.action - minus.action) / (
            2.0 * derivative_step
        )
        hj_derivative = -center.energy
        derivative_errors.append(abs(action_derivative - hj_derivative))
        derivative_samples.append(
            {
                "T": time,
                "finite_difference": action_derivative,
                "six_pi_squared_a_C": hj_derivative,
            }
        )
    audit.numerical(
        "P25.action.time_derivative_control",
        max(derivative_errors) < 2e-6,
        "finite differences of W(T) agree with dW/dT=6 pi^2 a C off shell",
    )

    curvature_step = 5e-3
    energies = [
        local_solution(0.7 + offset * curvature_step).energy
        for offset in (-2, -1, 1, 2)
    ]
    curvature = float(
        -(
            energies[0]
            - 8.0 * energies[1]
            + 8.0 * energies[2]
            - energies[3]
        )
        / (12.0 * curvature_step)
    )
    audit.numerical(
        "P25.saddle.negative_lapse_curvature",
        abs(curvature + 8.92314304) < 3e-7,
        f"the fixed-boundary lapse curvature is W_TT={curvature:.10f}<0",
    )
    below = local_solution(0.65)
    above = local_solution(0.75)
    audit.numerical(
        "P25.saddle.real_direction_is_not_descent",
        -below.energy > 0.0 and -above.energy < 0.0,
        "W rises toward T=0.7 from the left and falls to the right",
    )

    augmented_raw = five_point_augmented_hessian(
        boundary, 0.7, base_velocity, 1.25e-4
    )
    augmented_symmetry_residual = float(
        np.linalg.norm(augmented_raw - augmented_raw.T, ord=2)
        / np.linalg.norm(augmented_raw, ord=2)
    )
    augmented_hessian = 0.5 * (augmented_raw + augmented_raw.T)
    lapse_eliminated_hessian = (
        augmented_hessian[:4, :4]
        - np.outer(augmented_hessian[:4, 4], augmented_hessian[4, :4])
        / augmented_hessian[4, 4]
    )
    phase24_constrained_hessian = np.array(
        [
            [-177.349950952805, 1002.772290503440, 1013.888781405963, 949.305805860454],
            [1002.772290503440, 3467.690971368167, 949.305805863627, 888.836655031137],
            [1013.888781405963, 949.305805863627, -177.349950950806, 1002.772290517039],
            [949.305805860454, 888.836655031137, 1002.772290517039, 3467.690971380067],
        ]
    )
    schur_relative_residual = float(
        np.linalg.norm(
            lapse_eliminated_hessian - phase24_constrained_hessian, ord=2
        )
        / np.linalg.norm(phase24_constrained_hessian, ord=2)
    )
    audit.numerical(
        "P25.saddle.lapse_Schur_recovers_constrained_Hessian",
        augmented_symmetry_residual < 2e-10
        and abs(augmented_hessian[4, 4] - curvature) < 2e-8
        and schur_relative_residual < 1e-9,
        "the symmetric 5x5 (q,T) Hessian reduces to the Phase-24 constrained Hessian",
    )

    velocity_block = base.velocity_monodromy
    velocity_determinant = float(np.linalg.det(velocity_block))
    audit.numerical(
        "P25.jacobi.base_velocity_monodromy",
        np.allclose(
            velocity_block,
            np.array(
                [
                    [0.688639116937, -0.015272546281],
                    [0.007202850597, 0.690476842295],
                ]
            ),
            atol=3e-10,
            rtol=0.0,
        )
        and abs(velocity_determinant - 0.475599368812) < 4e-10,
        "the base Dirichlet shooting block is nonsingular",
    )
    momentum_velocity = np.diag(
        [
            -12.0 * np.pi**2 * boundary[0],
            2.0 * np.pi**2 * boundary[0] ** 3,
        ]
    )
    momentum_block = velocity_block @ np.linalg.inv(momentum_velocity)
    mixed_hessian = -np.linalg.inv(momentum_block)
    audit.numerical(
        "P25.jacobi.momentum_block_and_mixed_hessian",
        abs(np.linalg.det(momentum_block) + 1.25693827e-6) < 2e-14
        and np.linalg.svd(mixed_hessian, compute_uv=False)[1] > 600.0,
        "B_p=B_v(dv/dp) is invertible and K_+-=-B_p^{-1} on the fixed-T branch",
    )

    scan_times = [0.2, 0.7, 1.2, 2.0, 4.0, 6.0, 8.0, 9.0, 9.5, 9.7, 9.75, 9.78]
    center_guess = np.array([np.sqrt(3.0 / potential(1.0)), 1.0])
    branch_scan = []
    for time in scan_times:
        center_guess, half_endpoint = solve_symmetric_center(
            time, boundary, center_guess
        )
        solution = solve_fixed_time(
            time, boundary, -half_endpoint[[1, 3]]
        )
        singular_values = np.linalg.svd(
            solution.velocity_monodromy, compute_uv=False
        )
        branch_scan.append(
            {
                "T": time,
                "center": center_guess.tolist(),
                "W": solution.action,
                "dW_dT": -solution.energy,
                "det_Bv": float(np.linalg.det(solution.velocity_monodromy)),
                "Bv_singular_values": singular_values.tolist(),
                "endpoint_residual": solution.endpoint_residual,
            }
        )
    audit.numerical(
        "P25.branch.tracked_real_continuation",
        max(item["endpoint_residual"] for item in branch_scan) < 2e-8
        and all(item["center"][0] > 0.0 for item in branch_scan),
        "one reflection-symmetric real branch continues from T=0.2 to T=9.78",
    )

    fold = locate_symmetric_fold(boundary)
    fold_center_singulars = fold["center_singular_values"]
    fold_full_ratio = fold["full_velocity_monodromy_singular_ratio"]
    audit.numerical(
        "P25.caustic.symmetric_fold",
        abs(fold["proper_length"] - 9.78862557) < 3e-7
        and max(abs(value) for value in fold["residual"]) < 2e-8
        and fold_center_singulars[1] / fold_center_singulars[0] < 2e-8,
        "the tracked symmetric branch reaches a singular midpoint endpoint map at T_c",
    )
    audit.numerical(
        "P25.caustic.simple_fold_transversality",
        abs(fold["half_length_transversality"] - 0.51778265) < 3e-7
        and abs(fold["quadratic_transversality"] - 0.36861708) < 3e-7,
        "the fold has nonzero parameter and quadratic null-direction transversality",
    )
    bracket_determinants = fold["bracket_velocity_monodromy_determinants"]
    audit.numerical(
        "P25.caustic.two_branch_sign_bracket",
        bracket_determinants[0] * bracket_determinants[1] < 0.0
        and fold_full_ratio < 2e-7,
        "two real symmetric solutions at T=9.78 bracket the singular shooting block",
    )

    imaginary_times = [0.025, 0.05, 0.1, 0.2, 0.4]
    complex_guess = np.array(
        [0.7, base.velocity[0], 0.0, base.velocity[1], 0.0]
    )
    complex_points = []
    for imaginary_time in imaginary_times:
        complex_guess, proper_length, final = constant_phase_point(
            imaginary_time, boundary, complex_guess
        )
        complex_points.append(
            {
                "T": [proper_length.real, proper_length.imag],
                "W": [final[4].real, final[4].imag],
                "ReW_minus_W0": float(final[4].real - base.action),
            }
        )
    expected_real_times = np.array(
        [0.7001747501, 0.7006988672, 0.7027933498, 0.7111401293, 0.7440664322]
    )
    expected_action_rises = np.array(
        [0.0027890081, 0.0111623406, 0.0447501764, 0.1806062273, 0.7476684754]
    )
    real_times = np.array([item["T"][0] for item in complex_points])
    action_rises = np.array(
        [item["ReW_minus_W0"] for item in complex_points]
    )
    phase_residuals = np.array([abs(item["W"][1]) for item in complex_points])
    audit.numerical(
        "P25.thimble.local_constant_phase_segment",
        np.allclose(real_times, expected_real_times, atol=4e-8, rtol=0.0)
        and np.allclose(
            action_rises, expected_action_rises, atol=5e-8, rtol=0.0
        )
        and float(np.max(phase_residuals)) < 3e-9,
        "the local complex-T branch keeps Im W=0 while Re W increases",
    )

    return {
        "boundary_order": ["a_minus", "phi_minus", "a_plus", "phi_plus"],
        "boundary": boundary.tolist(),
        "base": {
            "T_star": 0.7,
            "velocity": base.velocity.tolist(),
            "W": base.action,
            "constraint": base.constraint,
            "dW_dT": -base.energy,
            "W_TT": curvature,
        },
        "time_derivative_samples": derivative_samples,
        "base_jacobi": {
            "B_velocity": velocity_block.tolist(),
            "det_B_velocity": velocity_determinant,
            "B_momentum": momentum_block.tolist(),
            "det_B_momentum": float(np.linalg.det(momentum_block)),
            "mixed_hessian": mixed_hessian.tolist(),
            "mixed_hessian_singular_values": np.linalg.svd(
                mixed_hessian, compute_uv=False
            ).tolist(),
        },
        "augmented_lapse_Hessian": {
            "coordinate_order": ["a_minus", "phi_minus", "a_plus", "phi_plus", "T"],
            "matrix": augmented_hessian.tolist(),
            "raw_symmetry_residual": augmented_symmetry_residual,
            "lapse_Schur_complement": lapse_eliminated_hessian.tolist(),
            "Phase24_relative_residual": schur_relative_residual,
        },
        "tracked_symmetric_real_branch": branch_scan,
        "symmetric_fold": fold,
        "local_constant_phase_segment": complex_points,
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P25",
        "calculation": "fixed-boundary lapse scan and local complex-T descent",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_model": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_Phase24_connected_solution_is_a_fixed_boundary_lapse_saddle": "SUPPORTED_FOR_THE_FROZEN_BENCHMARK",
            "the_real_lapse_direction_is_a_local_descent_for_exp_minus_W": "CONTRADICTED_BY_NEGATIVE_W_TT",
            "a_local_constant_phase_complex_T_descent_segment_exists": "SUPPORTED_ON_THE_RECORDED_BRANCH",
            "the_recorded_complex_segment_is_the_global_contributing_thimble": "OPEN_NOT_DERIVED",
            "the_tracked_symmetric_real_branch_reaches_a_Dirichlet_caustic": "SUPPORTED_ON_THE_RECORDED_CONTINUATION",
            "the_real_fixed_endpoint_BVP_is_unique_below_the_fold": "OPEN_NOT_TESTED",
            "the_fold_exhausts_all_real_or_complex_saddles": "OPEN_NOT_TESTED",
            "a_positive_quantum_gravitational_state_is_constructed": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "the full off-constraint Euler-Lagrange fixed-lapse flow",
                "W(T), dW/dT, and W_TT for the frozen Phase-24 boundaries",
                "one local constant-Im-W complex-T segment through T=0.7",
                "the real Jacobi monodromy and a bounded symmetric branch continuation",
                "a two-branch sign bracket and singular endpoint map at the recorded fold",
            ],
            "not_computed": [
                "a global Picard-Lefschetz flow or intersection number",
                "uniqueness or completeness of real, complex, or nonsymmetric branches",
                "the lapse measure, Faddeev-Popov determinant, or one-loop prefactor",
                "the full bulk fluctuation spectrum or Morse index",
                "a WDW inner product, positive density, entropy, Pin lift, or local SUGRA completion",
            ],
        },
        "next_calculation": (
            "integrate the global downward flow with singularity monitoring and "
            "compute its intersection with a specified lapse contour"
        ),
    }
    print("PHASE25_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
