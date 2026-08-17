#!/usr/bin/env python3
"""Phase 24 — connected Euclidean Starobinsky interval Hessian.

This executable constructs one real connected S^3 x I minisuperspace saddle
for the canonical Starobinsky scalar, differentiates its constrained Hamilton
principal function with respect to both boundaries, and audits the mixed
boundary Hessian.  Endpoint variations are solved together with the proper
length so that the Hamiltonian constraint remains zero.  A fixed-length
mutant is evaluated separately.

The calculation establishes a nonfactorizing classical Dirichlet-to-Neumann
response and the Hamilton-Jacobi null direction of its 2 x 2 mixed block.  It
does not construct a two-universe density matrix, a Picard-Lefschetz contour,
an inhomogeneous fluctuation determinant, a Pin lift, or local supergravity.
The conditional scalar Gaussian is reported only with both boundary scale
factors fixed.  The full real-boundary Hessian is indefinite.  The program
writes no files.
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
        self._check_unique(check_id)
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[PASS] {check_id}: {statement}")

    def numerical(self, check_id: str, condition: bool, statement: str) -> None:
        self._check_unique(check_id)
        if not condition:
            raise AssertionError(f"[NUMERIC FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")

    def _check_unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")


SQRT_TWO_THIRDS = float(np.sqrt(2.0 / 3.0))
TWO_PI_SQUARED = float(2.0 * np.pi**2)


def potential(phi: float | np.ndarray) -> float | np.ndarray:
    """Starobinsky potential with reduced M_P=M=1."""

    return 0.75 * (1.0 - np.exp(-SQRT_TWO_THIRDS * phi)) ** 2


def potential_prime(phi: float | np.ndarray) -> float | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return 1.5 * SQRT_TWO_THIRDS * exponential * (1.0 - exponential)


def euclidean_rhs(_tau: float, state: np.ndarray) -> np.ndarray:
    """Full off-constraint Euclidean Euler--Lagrange flow plus the action."""

    scale, scale_velocity, phi, phi_velocity, _action = state
    lagrangian = TWO_PI_SQUARED * (
        -3.0 * scale * (scale_velocity**2 + 1.0)
        + scale**3 * (0.5 * phi_velocity**2 + potential(phi))
    )
    return np.array(
        [
            scale_velocity,
            (1.0 - scale_velocity**2) / (2.0 * scale)
            - scale * phi_velocity**2 / 4.0
            - scale * potential(phi) / 2.0,
            phi_velocity,
            potential_prime(phi)
            - 3.0 * scale_velocity * phi_velocity / scale,
            lagrangian,
        ],
        dtype=float,
    )


def constraint(state: np.ndarray) -> float:
    scale, scale_velocity, phi, phi_velocity = state[:4]
    return float(
        scale_velocity**2
        - 1.0
        - scale**2 * (0.5 * phi_velocity**2 - potential(phi)) / 3.0
    )


@dataclass(frozen=True)
class BoundarySolution:
    action: float
    gradient: np.ndarray
    shooting_data: np.ndarray
    final_state: np.ndarray
    bvp_residual: float
    constraint_residual: float


def integrate_state(
    initial_state: np.ndarray,
    proper_length: float,
    *,
    rtol: float = 2e-13,
    atol: float = 2e-15,
) -> np.ndarray:
    solution = solve_ivp(
        euclidean_rhs,
        (0.0, proper_length),
        initial_state,
        method="DOP853",
        rtol=rtol,
        atol=atol,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1]


def midpoint_benchmark() -> tuple[np.ndarray, np.ndarray, float]:
    """Return q0, the left shooting data, and I0.

    phi_center=1 and total proper length T0=0.7 are explicit calibration
    inputs.  They are not selected by CPT, the saddle, or inflation data.
    """

    phi_center = 1.0
    half_length = 0.35
    scale_center = np.sqrt(3.0 / potential(phi_center))
    half_final = integrate_state(
        np.array([scale_center, 0.0, phi_center, 0.0, 0.0]),
        half_length,
    )
    scale_boundary, scale_velocity, phi_boundary, phi_velocity, half_action = (
        half_final
    )
    boundary = np.array(
        [scale_boundary, phi_boundary, scale_boundary, phi_boundary],
        dtype=float,
    )
    left_shooting = np.array(
        [-scale_velocity, -phi_velocity, 2.0 * half_length], dtype=float
    )
    return boundary, left_shooting, float(2.0 * half_action)


def canonical_gradient(
    left_scale: float,
    left_phi: float,
    left_scale_velocity: float,
    left_phi_velocity: float,
    final_state: np.ndarray,
) -> np.ndarray:
    """Hamilton-Jacobi gradient (-p_-, p_+) after the GHY reduction."""

    right_scale, right_scale_velocity, _right_phi, right_phi_velocity = (
        final_state[:4]
    )
    return np.array(
        [
            12.0 * np.pi**2 * left_scale * left_scale_velocity,
            -2.0 * np.pi**2 * left_scale**3 * left_phi_velocity,
            -12.0 * np.pi**2 * right_scale * right_scale_velocity,
            2.0 * np.pi**2 * right_scale**3 * right_phi_velocity,
        ],
        dtype=float,
    )


def solve_constrained_boundaries(
    boundary: np.ndarray,
    shooting_guess: np.ndarray,
) -> BoundarySolution:
    """Solve both endpoint conditions while varying the proper length.

    The three shooting unknowns are the two left endpoint velocities and the
    proper length.  The third equation is the Hamiltonian constraint.
    """

    left_scale, left_phi, right_scale, right_phi = map(float, boundary)

    def residual(shooting: np.ndarray) -> np.ndarray:
        left_scale_velocity, left_phi_velocity, proper_length = shooting
        final_state = integrate_state(
            np.array(
                [
                    left_scale,
                    left_scale_velocity,
                    left_phi,
                    left_phi_velocity,
                    0.0,
                ]
            ),
            proper_length,
            rtol=1e-12,
            atol=1e-14,
        )
        return np.array(
            [
                final_state[0] - right_scale,
                final_state[2] - right_phi,
                constraint(
                    np.array(
                        [
                            left_scale,
                            left_scale_velocity,
                            left_phi,
                            left_phi_velocity,
                        ]
                    )
                ),
            ]
        )

    root_result = root(residual, shooting_guess, method="hybr", tol=1e-12)
    residual_vector = residual(root_result.x)
    residual_norm = float(np.linalg.norm(residual_vector))
    if (
        not np.all(np.isfinite(root_result.x))
        or residual_norm > 2e-9
        or root_result.x[2] <= 0.0
    ):
        raise RuntimeError(
            f"constrained shooting failed: {root_result.message}; "
            f"residual={residual_vector.tolist()}"
        )

    left_scale_velocity, left_phi_velocity, proper_length = root_result.x
    final_state = integrate_state(
        np.array(
            [
                left_scale,
                left_scale_velocity,
                left_phi,
                left_phi_velocity,
                0.0,
            ]
        ),
        proper_length,
    )
    gradient = canonical_gradient(
        left_scale,
        left_phi,
        left_scale_velocity,
        left_phi_velocity,
        final_state,
    )
    return BoundarySolution(
        action=float(final_state[4]),
        gradient=gradient,
        shooting_data=root_result.x.copy(),
        final_state=final_state,
        bvp_residual=float(np.linalg.norm(residual_vector[:2])),
        constraint_residual=max(
            abs(
                constraint(
                    np.array(
                        [
                            left_scale,
                            left_scale_velocity,
                            left_phi,
                            left_phi_velocity,
                        ]
                    )
                )
            ),
            abs(constraint(final_state)),
        ),
    )


def solve_fixed_length_boundaries(
    boundary: np.ndarray,
    velocity_guess: np.ndarray,
    proper_length: float,
) -> BoundarySolution:
    """Fixed-length comparison which does not impose H=0 off the base point."""

    left_scale, left_phi, right_scale, right_phi = map(float, boundary)

    def residual(velocities: np.ndarray) -> np.ndarray:
        final_state = integrate_state(
            np.array(
                [left_scale, velocities[0], left_phi, velocities[1], 0.0]
            ),
            proper_length,
            rtol=1e-12,
            atol=1e-14,
        )
        return np.array(
            [final_state[0] - right_scale, final_state[2] - right_phi]
        )

    root_result = root(residual, velocity_guess, method="hybr", tol=1e-12)
    residual_vector = residual(root_result.x)
    residual_norm = float(np.linalg.norm(residual_vector))
    if not np.all(np.isfinite(root_result.x)) or residual_norm > 2e-9:
        raise RuntimeError(
            f"fixed-length shooting failed: {root_result.message}; "
            f"residual={residual_vector.tolist()}"
        )
    final_state = integrate_state(
        np.array(
            [left_scale, root_result.x[0], left_phi, root_result.x[1], 0.0]
        ),
        proper_length,
    )
    gradient = canonical_gradient(
        left_scale,
        left_phi,
        root_result.x[0],
        root_result.x[1],
        final_state,
    )
    return BoundarySolution(
        action=float(final_state[4]),
        gradient=gradient,
        shooting_data=np.array(
            [root_result.x[0], root_result.x[1], proper_length]
        ),
        final_state=final_state,
        bvp_residual=float(np.linalg.norm(residual_vector)),
        constraint_residual=max(
            abs(
                constraint(
                    np.array(
                        [
                            left_scale,
                            root_result.x[0],
                            left_phi,
                            root_result.x[1],
                        ]
                    )
                )
            ),
            abs(constraint(final_state)),
        ),
    )


def five_point_hessian(
    boundary: np.ndarray,
    step: float,
    gradient_function,
) -> np.ndarray:
    hessian = np.empty((4, 4), dtype=float)
    identity = np.eye(4)
    for column in range(4):
        direction = identity[column]
        minus_two = gradient_function(boundary - 2.0 * step * direction)
        minus_one = gradient_function(boundary - step * direction)
        plus_one = gradient_function(boundary + step * direction)
        plus_two = gradient_function(boundary + 2.0 * step * direction)
        hessian[:, column] = (
            minus_two - 8.0 * minus_one + 8.0 * plus_one - plus_two
        ) / (12.0 * step)
    return hessian


def exact_controls(audit: Audit) -> dict[str, object]:
    phi, b = sp.symbols("phi b", real=True, positive=True)
    symbolic_potential = sp.Rational(3, 4) * (1 - sp.exp(-b * phi)) ** 2
    symbolic_derivative = sp.Rational(3, 2) * b * sp.exp(-b * phi) * (
        1 - sp.exp(-b * phi)
    )
    audit.exact(
        "P24.action.starobinsky_derivative",
        sp.simplify(sp.diff(symbolic_potential, phi) - symbolic_derivative)
        == 0,
        "the recorded Starobinsky derivative follows from the frozen potential",
    )

    scale, scale_dot, phi_dot = sp.symbols(
        "a adot phidot", real=True, finite=True
    )
    lagrangian = 2 * sp.pi**2 * (
        -3 * scale * (scale_dot**2 + 1)
        + scale**3 * (sp.Rational(1, 2) * phi_dot**2 + symbolic_potential)
    )
    audit.exact(
        "P24.action.canonical_momenta",
        sp.diff(lagrangian, scale_dot) == -12 * sp.pi**2 * scale * scale_dot
        and sp.diff(lagrangian, phi_dot)
        == 2 * sp.pi**2 * scale**3 * phi_dot,
        "the endpoint Hamilton-Jacobi gradient uses the canonical momenta of the reduced action",
    )

    symbolic_v, scale_ddot = sp.symbols(
        "V addot", real=True, finite=True
    )
    scale_lagrangian = 2 * sp.pi**2 * (
        -3 * scale * (scale_dot**2 + 1)
        + scale**3 * (sp.Rational(1, 2) * phi_dot**2 + symbolic_v)
    )
    scale_euler_lagrange = sp.expand(
        sp.diff(sp.diff(scale_lagrangian, scale_dot), scale) * scale_dot
        + sp.diff(sp.diff(scale_lagrangian, scale_dot), scale_dot)
        * scale_ddot
        - sp.diff(scale_lagrangian, scale)
    )
    full_scale_eom = (
        (1 - scale_dot**2) / (2 * scale)
        - scale * phi_dot**2 / 4
        - scale * symbolic_v / 2
    )
    symbolic_constraint = (
        scale_dot**2
        - 1
        - scale**2 * (phi_dot**2 / 2 - symbolic_v) / 3
    )
    reduced_scale_eom = -scale * (phi_dot**2 + symbolic_v) / 3
    audit.exact(
        "P24.action.off_shell_scale_equation",
        sp.simplify(
            scale_euler_lagrange.subs(scale_ddot, full_scale_eom)
        )
        == 0
        and sp.simplify(
            full_scale_eom
            - reduced_scale_eom
            + symbolic_constraint / (2 * scale)
        )
        == 0,
        "the action yields the full scale-factor equation, which differs from its constraint-reduced form by -C/(2a)",
    )

    jm_entries = sp.symbols("jm0:4", real=True)
    jp_entries = sp.symbols("jp0:4", real=True)
    k_entries = sp.symbols("k0:4", real=True)
    left_jacobian = sp.Matrix(2, 2, jm_entries)
    right_jacobian = sp.Matrix(2, 2, jp_entries)
    mixed = sp.Matrix(2, 2, k_entries)
    transformed = left_jacobian.T * mixed * right_jacobian
    recovered_mixed = sp.simplify(
        left_jacobian.T.inv() * transformed * right_jacobian.inv()
    )
    audit.exact(
        "P24.hessian.mixed_block_bilinear_transform",
        sp.factor(
            transformed.det()
            - left_jacobian.det() * mixed.det() * right_jacobian.det()
        )
        == 0
        and sp.simplify(recovered_mixed - mixed).is_zero_matrix is True,
        "the mixed-Hessian bitensor law preserves rank under invertible separate endpoint Jacobians",
    )

    precision_coupling = sp.symbols("kappa", positive=True)
    schmidt_magnitude = precision_coupling / (
        1 + sp.sqrt(1 - precision_coupling**2)
    )
    audit.exact(
        "P24.gaussian.schmidt_relation",
        sp.simplify(
            2 * schmidt_magnitude / (1 + schmidt_magnitude**2)
            - precision_coupling
        )
        == 0,
        "the conditional two-mode Gaussian precision coupling obeys kappa=2|t|/(1+|t|^2)",
    )
    unit_precision = sp.Matrix(
        [[1, precision_coupling], [precision_coupling, 1]]
    )
    position_covariance = sp.simplify(unit_precision.inv() / 2)
    position_correlation = sp.simplify(
        position_covariance[0, 1] / position_covariance[0, 0]
    )
    audit.exact(
        "P24.gaussian.precision_covariance_sign",
        position_correlation == -precision_coupling,
        "a positive off-diagonal precision coupling gives the opposite-sign position covariance correlation",
    )
    return {
        "potential": "V(phi)=3/4[1-exp(-sqrt(2/3)phi)]^2",
        "units": "reduced M_P=M=1",
        "action": (
            "I_E=2pi^2 integral[-3a(a_dot^2+1)+"
            "a^3(phi_dot^2/2+V)]d tau"
        ),
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, shooting_guess, midpoint_action = midpoint_benchmark()
    base = solve_constrained_boundaries(boundary, shooting_guess)

    audit.numerical(
        "P24.saddle.midpoint_constraint",
        abs(constraint(np.array([np.sqrt(3.0 / potential(1.0)), 0, 1, 0])))
        < 2e-14,
        "the explicit phi_center=1 calibration seed satisfies the Euclidean constraint",
    )
    audit.numerical(
        "P24.saddle.connected_boundary_values",
        np.allclose(
            boundary,
            np.array(
                [3.56680319, 1.01858095, 3.56680319, 1.01858095]
            ),
            atol=6e-9,
            rtol=0,
        ),
        f"the connected interval gives q0={boundary.tolist()}",
    )
    audit.numerical(
        "P24.saddle.on_shell_action",
        abs(base.action - 1.406690542834) < 3e-10
        and abs(base.action - midpoint_action) < 3e-11,
        f"the full connected action is I0={base.action:.15f}",
    )
    audit.numerical(
        "P24.saddle.bvp_and_constraint_residuals",
        base.bvp_residual < 2e-9 and base.constraint_residual < 2e-11,
        "the boundary-value and Hamiltonian-constraint residuals are below tolerance",
    )

    constrained_gradient = lambda q: solve_constrained_boundaries(
        q, shooting_guess
    ).gradient
    steps = (1.0e-3, 5.0e-4, 2.5e-4, 1.25e-4)
    raw_hessians = [
        five_point_hessian(boundary, step, constrained_gradient)
        for step in steps
    ]
    hessians = [0.5 * (hessian + hessian.T) for hessian in raw_hessians]
    singular_pairs = [
        np.linalg.svd(hessian[:2, 2:], compute_uv=False)
        for hessian in hessians
    ]
    ratios = [float(pair[1] / pair[0]) for pair in singular_pairs]
    observed_orders = [
        float(np.log(ratios[index] / ratios[index + 1]) / np.log(2.0))
        for index in range(len(ratios) - 1)
    ]
    raw_richardson_hessian = (
        16.0 * raw_hessians[-1] - raw_hessians[-2]
    ) / 15.0
    raw_symmetry_residual = float(
        np.max(
            np.abs(raw_richardson_hessian - raw_richardson_hessian.T)
        )
        / np.linalg.norm(raw_richardson_hessian, ord=2)
    )
    richardson_hessian = 0.5 * (
        raw_richardson_hessian + raw_richardson_hessian.T
    )
    cross_block = richardson_hessian[:2, 2:]
    singular_values = np.linalg.svd(cross_block, compute_uv=False)
    full_eigenvalues = np.linalg.eigvalsh(richardson_hessian)

    audit.numerical(
        "P24.hessian.fourth_order_rank_convergence",
        min(observed_orders) > 3.7 and ratios[-1] < 3e-10,
        "the spurious second mixed singular value converges away at fourth order; "
        f"ratios={ratios}, orders={observed_orders}",
    )
    audit.numerical(
        "P24.hessian.symmetry",
        raw_symmetry_residual < 2e-10,
        "the independently differentiated raw Hamilton principal Hessian is symmetric within numerical tolerance; "
        f"relative residual={raw_symmetry_residual:.3e}",
    )

    left_velocity = base.shooting_data[:2]
    right_velocity = base.final_state[[1, 3]]
    left_null_residual = float(
        np.linalg.norm(left_velocity @ cross_block)
        / (
            np.linalg.norm(left_velocity)
            * np.linalg.norm(cross_block, ord=2)
        )
    )
    right_null_residual = float(
        np.linalg.norm(cross_block @ right_velocity)
        / (
            np.linalg.norm(right_velocity)
            * np.linalg.norm(cross_block, ord=2)
        )
    )
    audit.numerical(
        "P24.hessian.HJ_constraint_null_vectors",
        max(left_null_residual, right_null_residual) < 2e-10,
        "v_minus is a left null vector and v_plus is a right null vector of K_+-; "
        f"normalized residuals=({left_null_residual:.3e},{right_null_residual:.3e})",
    )
    audit.numerical(
        "P24.hessian.constraint_reduced_rank_one",
        singular_values[0] > 1e3
        and singular_values[1] / singular_values[0] < 3e-10,
        "the nonzero constrained mixed response survives while the constraint-null singular value vanishes; "
        f"sigma={singular_values.tolist()}",
    )

    fixed_velocity_guess = shooting_guess[:2]
    fixed_gradient = lambda q: solve_fixed_length_boundaries(
        q, fixed_velocity_guess, 0.7
    ).gradient
    fixed_hessian_raw = five_point_hessian(
        boundary, 2.5e-4, fixed_gradient
    )
    fixed_hessian = 0.5 * (fixed_hessian_raw + fixed_hessian_raw.T)
    fixed_singular_values = np.linalg.svd(
        fixed_hessian[:2, 2:], compute_uv=False
    )
    audit.numerical(
        "P24.hessian.fixed_length_mutant_full_rank",
        fixed_singular_values[1] > 500,
        "holding T=0.7 fixed instead of imposing H=0 leaves a full-rank mixed block; "
        f"sigma={fixed_singular_values.tolist()}",
    )

    scalar_precision = richardson_hessian[np.ix_([1, 3], [1, 3])]
    scalar_eigenvalues = np.linalg.eigvalsh(scalar_precision)
    normalized_precision_coupling = float(
        scalar_precision[0, 1]
        / np.sqrt(scalar_precision[0, 0] * scalar_precision[1, 1])
    )
    scalar_covariance = 0.5 * np.linalg.inv(scalar_precision)
    position_correlation = float(
        scalar_covariance[0, 1]
        / np.sqrt(scalar_covariance[0, 0] * scalar_covariance[1, 1])
    )
    schmidt_magnitude = float(
        normalized_precision_coupling
        / (
            1.0
            + np.sqrt(1.0 - normalized_precision_coupling**2)
        )
    )
    conditional_entropy = float(
        -np.log(1.0 - schmidt_magnitude**2)
        - schmidt_magnitude**2
        / (1.0 - schmidt_magnitude**2)
        * np.log(schmidt_magnitude**2)
    )
    audit.numerical(
        "P24.gaussian.fixed_scale_scalar_positive",
        scalar_eigenvalues[0] > 0,
        "with both boundary scale factors fixed, the scalar 2x2 precision is positive",
    )
    audit.numerical(
        "P24.gaussian.conditional_parameters",
        abs(normalized_precision_coupling - 0.25631946) < 2e-7
        and abs(position_correlation + 0.25631946) < 2e-7
        and abs(schmidt_magnitude - 0.13033687) < 2e-7
        and abs(conditional_entropy - 0.0875594) < 2e-7,
        "the fixed-scale Gaussian separates its positive precision coupling, negative position correlation, Schmidt magnitude, and conditional entropy",
    )

    negative_modes = int(np.count_nonzero(full_eigenvalues < 0.0))
    audit.numerical(
        "P24.contour.full_boundary_hessian_indefinite",
        negative_modes == 2,
        "the real-boundary Hessian has two negative eigenvalues and is not a positive density kernel",
    )

    scale_indices = [0, 2]
    scalar_indices = [1, 3]
    scale_block = richardson_hessian[np.ix_(scale_indices, scale_indices)]
    scalar_block = richardson_hessian[np.ix_(scalar_indices, scalar_indices)]
    scalar_scale = richardson_hessian[np.ix_(scalar_indices, scale_indices)]
    schur_precision = (
        scalar_block
        - scalar_scale @ np.linalg.inv(scale_block) @ scalar_scale.T
    )
    schur_eigenvalues = np.linalg.eigvalsh(schur_precision)
    audit.numerical(
        "P24.contour.real_scale_integration_not_positive",
        schur_eigenvalues[0] < 0.0 < schur_eigenvalues[1],
        "naively integrating the scale factors on the real contour gives an indefinite scalar Schur complement",
    )

    factorized_cross_block = np.zeros((2, 2))
    audit.numerical(
        "P24.factorization.connected_response_nonzero",
        np.linalg.norm(cross_block, ord=2) > 1e3
        and np.linalg.norm(factorized_cross_block, ord=2) == 0,
        "the connected interval has a nonzero mixed response whereas a factorized endpoint action has none",
    )

    return {
        "benchmark_inputs": {
            "phi_center": 1.0,
            "base_proper_length": 0.7,
            "note": "calibration inputs, not selected observables",
        },
        "boundary_order": ["a_minus", "phi_minus", "a_plus", "phi_plus"],
        "q0": boundary.tolist(),
        "I0": base.action,
        "gradient": base.gradient.tolist(),
        "base_shooting": base.shooting_data.tolist(),
        "base_final_velocities": base.final_state[[1, 3]].tolist(),
        "bvp_residual": base.bvp_residual,
        "constraint_residual": base.constraint_residual,
        "finite_difference": {
            "stencil": "five-point first derivative of the Hamilton-Jacobi gradient",
            "steps": list(steps),
            "small_to_large_singular_ratios": ratios,
            "observed_orders": observed_orders,
            "richardson": "H=(16 H(h/2)-H(h))/15 from the two smallest steps",
        },
        "constrained_hessian": richardson_hessian.tolist(),
        "raw_hessian_symmetry_residual": raw_symmetry_residual,
        "cross_block": cross_block.tolist(),
        "cross_singular_values": singular_values.tolist(),
        "HJ_null_residuals": [left_null_residual, right_null_residual],
        "full_boundary_hessian_eigenvalues": full_eigenvalues.tolist(),
        "fixed_length_cross_singular_values": fixed_singular_values.tolist(),
        "conditional_fixed_scale_scalar": {
            "precision": scalar_precision.tolist(),
            "position_covariance": scalar_covariance.tolist(),
            "eigenvalues": scalar_eigenvalues.tolist(),
            "normalized_precision_coupling": normalized_precision_coupling,
            "position_correlation": position_correlation,
            "schmidt_magnitude": schmidt_magnitude,
            "entropy_nats": conditional_entropy,
            "interpretation": "flat-measure two-real-mode toy with delta a_+=delta a_-=0",
        },
        "real_contour_scalar_schur": {
            "precision": schur_precision.tolist(),
            "eigenvalues": schur_eigenvalues.tolist(),
            "interpretation": "indefinite; not a normalized real Gaussian",
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    frozen_model = exact_controls(audit)
    numerics = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P24",
        "calculation": "connected Euclidean Starobinsky interval Hessian",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_model": frozen_model,
        "numerical_controls": numerics,
        "claim_status": {
            "a_connected_real_minisuperspace_interval_saddle_exists": "SUPPORTED_FOR_THE_FROZEN_BENCHMARK",
            "the_connected_principal_function_has_nonzero_cross_boundary_response": "SUPPORTED_FOR_THE_FROZEN_BENCHMARK",
            "the_constrained_homogeneous_mixed_block_has_one_nonzero_classical_response_direction": "SUPPORTED_BY_HJ_IDENTITY_AND_NUMERICAL_CONVERGENCE",
            "the_small_mixed_singular_value_is_a_physical_mode": "CONTRADICTED_BY_FOURTH_ORDER_CONVERGENCE",
            "the_fixed_scale_scalar_subblock_defines_a_conditional_positive_Gaussian": "SUPPORTED_ONLY_IN_THE_RECORDED_FLAT_MEASURE_CONTROL",
            "the_conditional_entropy_is_full_gravitational_seam_entanglement": "OPEN_NOT_DERIVED",
            "the_real_boundary_Hessian_defines_a_positive_normalizable_real_Gaussian_precision": "CONTRADICTED_BY_TWO_NEGATIVE_EIGENVALUES",
            "the_saddle_is_selected_by_a_gravitational_thimble": "OPEN_NOT_COMPUTED",
            "the_saddle_selects_phi0_or_a_SUSY_breaking_scale": "CONTRADICTED_BY_SUPPLIED_BENCHMARK_INPUTS",
            "a_full_Pin_local_SUGRA_seam_state_is_constructed": "OPEN_NOT_COMPUTED",
        },
        "scope_guard": {
            "what_is_computed": [
                "one real O(4)-homogeneous canonical scalar-gravity saddle on S3 x I",
                "the reduced action after the standard Dirichlet gravitational boundary reduction",
                "constraint-preserving endpoint variations with the proper length solved as a modulus",
                "the 4x4 Hamilton principal Hessian and its 2x2 mixed block",
                "Hamilton-Jacobi left and right null directions",
                "a fixed-proper-length mutant",
                "a conditional scalar Gaussian after fixing both endpoint scale factors",
            ],
            "what_is_not_computed": [
                "a Picard-Lefschetz intersection number or dominant contour",
                "the gauge-fixed bulk fluctuation Morse spectrum",
                "Faddeev-Popov or BRST ghosts and one-loop determinants",
                "inhomogeneous scalar, vector, tensor, chiralino, or gravitino modes",
                "a two-universe Hilbert-space factorization or Choi state prescription",
                "a physical WDW inner product, positive density, or entropy",
                "a CPT/Pin lift, flux sum, membrane transition, or local SUGRA completion",
                "selection of phi0, e-folds, curvature radius, or SUSY-breaking scale",
            ],
        },
        "next_calculation": {
            "contour": (
                "construct the lapse/conformal Picard-Lefschetz thimble and the "
                "gauge-fixed primed bulk fluctuation operator"
            ),
            "state": (
                "specify an outgoing/outgoing or Choi reflection prescription, "
                "physical boundary measure, and test whether the resulting kernel is trace class"
            ),
            "local_sugra": (
                "only then add the gravitino-Goldstino-ghost Calderon blocks and test BRST Ward identities"
            ),
        },
    }
    print("PHASE24_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
