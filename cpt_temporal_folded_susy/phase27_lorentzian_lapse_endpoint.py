#!/usr/bin/env python3
"""Phase 27 -- Lorentzian lapse Wick map and the zero-lapse endpoint.

This bounded executable freezes the Phase-24/25 homogeneous Starobinsky model,
declares its standard Lorentzian continuation, derives the associated
Lorentzian-to-Euclidean lapse rotation, and checks the equal-boundary
short-time action, Jacobi map, and Van Vleck scaling.  It also separates the
positive-lapse Green-function source identity from full-line group averaging.

The signed classical W sheet is only a control.  The script does not compute a
Faddeev--Popov measure, a gauge-fixed one-loop determinant, a global Lefschetz
intersection number, or a positive quantum-gravity state.  It writes no files.
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


def potential(phi: float | np.ndarray) -> float | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return 0.75 * (1.0 - exponential) ** 2


def potential_prime(phi: float | np.ndarray) -> float | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return 1.5 * SQRT_TWO_THIRDS * exponential * (1.0 - exponential)


def potential_second(phi: float | np.ndarray) -> float | np.ndarray:
    exponential = np.exp(-SQRT_TWO_THIRDS * phi)
    return -exponential + 2.0 * exponential**2


def configuration_metric(scale: float) -> np.ndarray:
    return np.diag([-6.0 * scale, scale**3])


def euclidean_potential(scale: float, phi: float) -> float:
    return float(-3.0 * scale + scale**3 * potential(phi))


def euclidean_potential_gradient(scale: float, phi: float) -> np.ndarray:
    return np.array(
        [
            -3.0 + 3.0 * scale**2 * potential(phi),
            scale**3 * potential_prime(phi),
        ]
    )


def euclidean_lagrangian(state: np.ndarray) -> float:
    scale, scale_velocity, phi, phi_velocity = state[:4]
    return float(
        TWO_PI_SQUARED
        * (
            -3.0 * scale * (scale_velocity**2 + 1.0)
            + scale**3 * (0.5 * phi_velocity**2 + potential(phi))
        )
    )


def configuration_rhs(state: np.ndarray) -> np.ndarray:
    """Full off-constraint Euclidean Euler--Lagrange flow."""

    scale, scale_velocity, phi, phi_velocity = state[:4]
    return np.array(
        [
            scale_velocity,
            (1.0 - scale_velocity**2) / (2.0 * scale)
            - scale * phi_velocity**2 / 4.0
            - scale * potential(phi) / 2.0,
            phi_velocity,
            potential_prime(phi)
            - 3.0 * scale_velocity * phi_velocity / scale,
        ]
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
        ]
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
    state0 = np.asarray(initial, dtype=float)
    if monodromy:
        augmented0 = np.concatenate([state0, [0.0], np.eye(4).ravel()])

        def rhs(_tau: float, augmented: np.ndarray) -> np.ndarray:
            state = augmented[:4]
            matrix = augmented[5:].reshape(4, 4)
            return np.concatenate(
                [
                    configuration_rhs(state),
                    [euclidean_lagrangian(state)],
                    (variational_matrix(state) @ matrix).ravel(),
                ]
            )

    else:
        augmented0 = np.concatenate([state0, [0.0]])

        def rhs(_tau: float, augmented: np.ndarray) -> np.ndarray:
            state = augmented[:4]
            return np.concatenate(
                [configuration_rhs(state), [euclidean_lagrangian(state)]]
            )

    absolute_length = abs(float(proper_length))
    solution = solve_ivp(
        rhs,
        (0.0, proper_length),
        augmented0,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=min(0.02, max(absolute_length / 40.0, 2e-5)),
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


def short_time_velocity(boundary: np.ndarray, proper_length: float) -> np.ndarray:
    scale, phi = boundary[:2]
    metric = configuration_metric(scale)
    force = np.linalg.solve(
        metric, euclidean_potential_gradient(scale, phi)
    )
    return -0.5 * proper_length * force


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
    if not np.all(np.isfinite(root_result.x)) or residual_norm > 2e-9:
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


def observed_orders(errors: np.ndarray) -> np.ndarray:
    return np.log(errors[:-1] / errors[1:]) / np.log(2.0)


def exact_controls(audit: Audit) -> dict[str, object]:
    lapse, time, kinetic, symbolic_u = sp.symbols(
        "N T K U", nonzero=True
    )
    lorentzian_density = kinetic / lapse - lapse * symbolic_u
    euclidean_density = kinetic / time + time * symbolic_u
    wick_substitution = sp.simplify(
        lorentzian_density.subs(lapse, -sp.I * time)
    )
    audit.exact(
        "P27.action.lapse_Wick_map",
        sp.simplify(wick_substitution - sp.I * euclidean_density) == 0,
        "N_L=-iT_E maps the declared Lorentzian density to i times the frozen Euclidean density",
    )
    audit.exact(
        "P27.action.exponent_Wick_map",
        sp.simplify(sp.I * wick_substitution + euclidean_density) == 0,
        "the Wick map gives exp(i S_L)=exp(-I_E)",
    )

    w0, w1, w2 = sp.symbols("w0 w1 w2")
    local_w = w0 + w1 * time + w2 * time**2 / 2
    local_s = sp.I * local_w.subs(time, sp.I * lapse)
    audit.exact(
        "P27.action.principal_derivative_map",
        sp.simplify(
            sp.diff(local_s, lapse)
            + sp.diff(local_w, time).subs(time, sp.I * lapse)
        )
        == 0
        and sp.simplify(sp.diff(local_s, lapse, 2) + sp.I * w2) == 0,
        "S_N=-W_T and S_NN=-i W_TT on corresponding analytic branches",
    )
    audit.exact(
        "P27.action.signed_classical_oddness",
        sp.simplify(euclidean_density.subs(time, -time) + euclidean_density)
        == 0,
        "the fixed-s Euclidean action changes sign under T to -T",
    )

    tau, force_squared, potential_zero = sp.symbols(
        "tau F2 U0", positive=True
    )
    kinetic_correction = (
        force_squared * (tau - time / 2) ** 2 / 2
    )
    linear_potential_correction = (
        force_squared * tau * (tau - time) / 2
    )
    correction = sp.integrate(
        kinetic_correction + linear_potential_correction,
        (tau, 0, time),
    )
    short_action = potential_zero * time + correction
    audit.exact(
        "P27.short_time.equal_boundary_action",
        sp.simplify(
            short_action
            - potential_zero * time
            + force_squared * time**3 / 24
        )
        == 0,
        "the equal-boundary action is U0 T-F2 T^3/24 through cubic order",
    )

    scale, normalization = sp.symbols("a M", positive=True)
    metric = sp.diag(-6 * scale, scale**3)
    velocity_jacobian = time * sp.eye(2)
    momentum_jacobian = sp.simplify(
        velocity_jacobian * (normalization * metric).inv()
    )
    mixed_hessian = sp.simplify(-momentum_jacobian.inv())
    audit.exact(
        "P27.short_time.Jacobi_Van_Vleck_map",
        mixed_hessian == sp.simplify(-normalization * metric / time),
        "B_v=T I and B_p=T(MG)^-1 imply W_+-=-MG/T",
    )
    audit.exact(
        "P27.short_time.conformal_determinant_sign",
        sp.simplify(
            sp.det(-mixed_hessian)
            + 6 * normalization**2 * scale**4 / time**2
        )
        == 0,
        "the raw two-coordinate Van Vleck determinant is negative and scales as T^-2",
    )

    spectral_value = sp.symbols("lambda", real=True)
    group_time = sp.symbols("N", real=True)
    regulator = sp.symbols("eps", real=True, positive=True)
    fixed_lapse_kernel = sp.exp(-sp.I * group_time * spectral_value)
    audit.exact(
        "P27.operator.fixed_lapse_constraint_evolution",
        sp.simplify(
            sp.I * sp.diff(fixed_lapse_kernel, group_time)
            - spectral_value * fixed_lapse_kernel
        )
        == 0,
        "the spectral fixed-lapse kernel obeys i d_N K=lambda K",
    )
    half_line_resolvent = -sp.I / (spectral_value - sp.I * regulator)
    audit.exact(
        "P27.operator.positive_half_line_resolvent",
        sp.simplify(
            (spectral_value - sp.I * regulator) * half_line_resolvent
            + sp.I
        )
        == 0,
        "the damped positive half-line is a sourced resolvent, not a constraint projector",
    )
    audit.exact(
        "P27.operator.full_line_constraint_support",
        sp.integrate(
            spectral_value
            * sp.DiracDelta(spectral_value)
            * (1 + spectral_value),
            (spectral_value, -1, 1),
        )
        == 0,
        "the full-line group average is supported on the constraint surface",
    )

    positive_parameter = sp.symbols("x", positive=True)
    lower_lateral = sp.I * (positive_parameter - sp.I * regulator)
    upper_lateral = sp.I * (positive_parameter + sp.I * regulator)
    audit.exact(
        "P27.contour.lateral_Wick_side",
        sp.re(lower_lateral) == regulator
        and sp.re(upper_lateral) == -regulator,
        "N-i0 maps to the right of the upper-imaginary T ray and N+i0 to its left",
    )

    flow_real, flow_imag = sp.symbols("u v", real=True)
    symbolic_gradient = flow_real + sp.I * flow_imag
    descent_change = sp.expand(
        symbolic_gradient * sp.conjugate(symbolic_gradient)
    )
    audit.exact(
        "P27.flow.exp_minus_W_monotonicity",
        sp.im(descent_change) == 0
        and sp.re(descent_change) == flow_real**2 + flow_imag**2,
        "dT/ds=conj(W_T) keeps Im W fixed and increases Re W",
    )

    return {
        "Lorentzian_action": "S_L=2pi^2 integral[(G_AB q_s^A q_s^B)/(2N)-N U] ds",
        "Euclidean_action": "I_E=2pi^2 integral[(G_AB q_s^A q_s^B)/(2T)+T U] ds",
        "Wick_map": "N_L=-i T_E; T_E=i N_L; S_cl(N)=i W(iN)",
        "configuration_metric": "G=diag(-6a,a^3)",
        "Euclidean_potential": "U=-3a+a^3 V(phi)",
        "potential": "V=3/4[1-exp(-sqrt(2/3)phi)]^2",
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, base_velocity, benchmark_action = benchmark()
    base = solve_fixed_time(0.7, boundary, base_velocity)
    audit.numerical(
        "P27.benchmark.Phase24_25_endpoint",
        np.allclose(
            boundary,
            np.array(
                [
                    3.5668031935672753,
                    1.0185809464006637,
                    3.5668031935672753,
                    1.0185809464006637,
                ]
            ),
            atol=3e-13,
            rtol=0.0,
        )
        and abs(base.action - benchmark_action) < 2e-10
        and abs(base.constraint) < 2e-11,
        "the frozen endpoint and T=0.7 saddle reproduce the Phase-24/25 benchmark",
    )

    scale, phi = boundary[:2]
    metric = configuration_metric(scale)
    gradient = euclidean_potential_gradient(scale, phi)
    force = np.linalg.solve(metric, gradient)
    force_squared = float(gradient @ force)
    potential_zero = euclidean_potential(scale, phi)
    linear_coefficient = TWO_PI_SQUARED * potential_zero
    cubic_coefficient = -TWO_PI_SQUARED * force_squared / 24.0
    predicted_velocity_per_time = -0.5 * force

    short_times = np.array([0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625])
    short_solutions = [
        solve_fixed_time(
            float(time), boundary, short_time_velocity(boundary, float(time))
        )
        for time in short_times
    ]
    action_over_time = np.array(
        [solution.action / solution.proper_length for solution in short_solutions]
    )
    cubic_estimates = np.array(
        [
            (solution.action - linear_coefficient * solution.proper_length)
            / solution.proper_length**3
            for solution in short_solutions
        ]
    )
    linear_errors = np.abs(action_over_time - linear_coefficient)
    cubic_errors = np.abs(cubic_estimates - cubic_coefficient)
    linear_orders = observed_orders(linear_errors)
    cubic_orders = observed_orders(cubic_errors)
    audit.numerical(
        "P27.short_time.action_linear_cubic_convergence",
        linear_errors[-1] < 8e-5
        and cubic_errors[-1] < 2e-5
        and np.min(linear_orders[-3:]) > 1.95
        and np.min(cubic_orders[-3:]) > 1.95,
        "W/T converges quadratically to 2pi^2 U0 and its cubic coefficient converges to -2pi^2 F2/24",
    )

    velocity_per_time = np.array(
        [solution.velocity / solution.proper_length for solution in short_solutions]
    )
    velocity_errors = np.linalg.norm(
        velocity_per_time - predicted_velocity_per_time, axis=1
    )
    velocity_orders = observed_orders(velocity_errors)
    audit.numerical(
        "P27.short_time.initial_velocity_convergence",
        velocity_errors[-1] < 2e-6
        and np.min(velocity_orders[-3:]) > 1.9,
        "the equal-boundary initial velocity obeys v_-=-T G^-1 grad(U)/2+O(T^3)",
    )

    scaled_velocity_blocks = np.array(
        [
            solution.velocity_monodromy / solution.proper_length
            for solution in short_solutions
        ]
    )
    jacobi_errors = np.array(
        [np.linalg.norm(block - np.eye(2), ord=2) for block in scaled_velocity_blocks]
    )
    jacobi_orders = observed_orders(jacobi_errors)
    determinant_ratios = np.array(
        [
            np.linalg.det(solution.velocity_monodromy)
            / solution.proper_length**2
            for solution in short_solutions
        ]
    )
    audit.numerical(
        "P27.short_time.velocity_Jacobi_scaling",
        jacobi_errors[-1] < 5e-6
        and abs(determinant_ratios[-1] - 1.0) < 5e-6
        and np.min(jacobi_orders[-3:]) > 1.9,
        "B_v/T tends to the identity and det(B_v)/T^2 tends to one",
    )

    momentum_velocity = TWO_PI_SQUARED * metric
    predicted_momentum_determinant = float(
        np.linalg.det(np.linalg.inv(momentum_velocity))
    )
    predicted_scaled_mixed = -momentum_velocity
    momentum_determinant_ratios = []
    scaled_mixed_hessians = []
    for solution in short_solutions:
        momentum_block = solution.velocity_monodromy @ np.linalg.inv(
            momentum_velocity
        )
        mixed_hessian = -np.linalg.inv(momentum_block)
        momentum_determinant_ratios.append(
            np.linalg.det(momentum_block) / solution.proper_length**2
        )
        scaled_mixed_hessians.append(
            solution.proper_length * mixed_hessian
        )
    momentum_determinant_ratios_array = np.asarray(
        momentum_determinant_ratios
    )
    scaled_mixed_hessians_array = np.asarray(scaled_mixed_hessians)
    mixed_errors = np.array(
        [
            np.linalg.norm(matrix - predicted_scaled_mixed, ord=2)
            / np.linalg.norm(predicted_scaled_mixed, ord=2)
            for matrix in scaled_mixed_hessians_array
        ]
    )
    audit.numerical(
        "P27.short_time.momentum_Van_Vleck_scaling",
        abs(
            momentum_determinant_ratios_array[-1]
            - predicted_momentum_determinant
        )
        < 2e-11
        and mixed_errors[-1] < 5e-6,
        "det(B_p)/T^2 and T W_+- converge to their metric-controlled short-time limits",
    )

    negative_base = solve_fixed_time(-0.7, boundary, -base_velocity)
    audit.numerical(
        "P27.signed_branch.paired_stationary_actions",
        abs(negative_base.action + base.action) < 2e-10
        and abs(negative_base.constraint) < 2e-11
        and np.linalg.norm(negative_base.velocity + base.velocity) < 2e-10,
        "the signed raw classical branch has paired stationary points at T=+-0.7 with opposite actions",
    )

    connecting_times = np.array(
        [-0.65, -0.4, -0.2, -0.1, 0.1, 0.2, 0.4, 0.65]
    )
    connecting_solutions = [
        solve_fixed_time(
            float(time), boundary, short_time_velocity(boundary, float(time))
        )
        for time in connecting_times
    ]
    connecting_derivatives = np.array(
        [-solution.energy for solution in connecting_solutions]
    )
    signed_action_residuals = []
    for index in range(len(connecting_times) // 2):
        signed_action_residuals.append(
            abs(
                connecting_solutions[index].action
                + connecting_solutions[-index - 1].action
            )
        )
    audit.numerical(
        "P27.signed_branch.raw_W_Stokes_candidate",
        np.min(connecting_derivatives) > 0.0
        and max(signed_action_residuals) < 2e-9,
        "the recorded signed raw-W interval is odd with W_T>0 between the paired saddles",
    )

    short_endpoint_speed = float(-short_solutions[-1].energy)
    audit.numerical(
        "P27.endpoint.zero_lapse_is_not_a_saddle",
        abs(short_endpoint_speed - linear_coefficient) < 3e-4
        and linear_coefficient > 0.0,
        "the raw-W dual reaches T=0 with finite nonzero speed rather than a critical endpoint",
    )

    van_vleck_determinant_coefficient = float(
        np.linalg.det(momentum_velocity)
    )
    van_vleck_magnitude_coefficient = float(
        np.sqrt(abs(van_vleck_determinant_coefficient))
    )
    return {
        "boundary_order": ["a_minus", "phi_minus", "a_plus", "phi_plus"],
        "boundary": boundary.tolist(),
        "base": {
            "T_star": 0.7,
            "N_star": [0.0, -0.7],
            "W": base.action,
            "constraint": base.constraint,
            "paired_negative_T_action": negative_base.action,
        },
        "short_time_coefficients": {
            "U0": potential_zero,
            "gradU_Ginv_gradU": force_squared,
            "W_linear": linear_coefficient,
            "W_cubic": cubic_coefficient,
            "predicted_velocity_per_T": predicted_velocity_per_time.tolist(),
            "det_Bp_over_T2": predicted_momentum_determinant,
            "det_minus_W_cross_times_T2": van_vleck_determinant_coefficient,
            "abs_sqrt_Van_Vleck_times_abs_T": van_vleck_magnitude_coefficient,
        },
        "short_time_table": [
            {
                "T": float(solution.proper_length),
                "W": solution.action,
                "W_over_T": action_over_time[index],
                "cubic_estimate": cubic_estimates[index],
                "velocity": solution.velocity.tolist(),
                "det_Bv_over_T2": determinant_ratios[index],
                "det_Bp_over_T2": momentum_determinant_ratios_array[index],
                "relative_T_Wcross_error": mixed_errors[index],
            }
            for index, solution in enumerate(short_solutions)
        ],
        "convergence": {
            "linear_orders": linear_orders.tolist(),
            "cubic_orders": cubic_orders.tolist(),
            "velocity_orders": velocity_orders.tolist(),
            "Jacobi_orders": jacobi_orders.tolist(),
        },
        "signed_raw_W_control": {
            "times": connecting_times.tolist(),
            "actions": [
                solution.action for solution in connecting_solutions
            ],
            "dW_dT": connecting_derivatives.tolist(),
            "max_odd_action_residual": max(signed_action_residuals),
            "interpretation": "candidate raw-W Stokes connection only; the prefactored zero-lapse domain is not computed",
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P27",
        "calculation": "Lorentzian lapse Wick map and equal-boundary zero-lapse endpoint",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_model": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_declared_Lorentzian_continuation_has_Wick_map_NL_minus_i_TE": "SUPPORTED_EXACTLY",
            "positive_real_Lorentzian_lapse_maps_to_positive_real_Euclidean_T": "CONTRADICTED_BY_T_EQUALS_iN",
            "equal_boundary_W_to_zero_removes_the_zero_lapse_kernel_singularity": "CONTRADICTED_BY_VAN_VLECK_T_INVERSE",
            "the_signed_raw_W_sheet_has_paired_stationary_points": "SUPPORTED_FOR_THE_FROZEN_BENCHMARK",
            "the_signed_raw_W_control_is_a_heteroclinic_of_the_full_prefactored_integrand": "OPEN_NOT_DERIVED",
            "the_positive_lapse_half_line_is_a_sourced_resolvent": "SUPPORTED_AT_THE_SPECTRAL_OPERATOR_LEVEL",
            "the_positive_lapse_half_line_is_a_WDW_projector_or_positive_state": "CONTRADICTED_AS_A_PROJECTOR_AND_NOT_DERIVED_AS_A_STATE",
            "a_lateral_zero_lapse_bypass_fixes_the_global_PL_intersection_number": "OPEN_NOT_DERIVED",
            "a_global_n_sigma_has_been_computed": "OPEN_NOT_COMPUTED",
        },
        "scope_guard": {
            "computed": [
                "the frozen Euclidean model, its explicitly declared Lorentzian continuation, and their exact Wick map",
                "the equal-boundary short-time classical action through cubic order",
                "the raw two-coordinate Jacobi, momentum, and Van Vleck short-time scaling",
                "a bounded signed raw-W continuation through T=0",
                "spectral proxy identities separating a positive half-line resolvent from full-line constraint support",
            ],
            "not_computed": [
                "the Faddeev-Popov measure or a gauge-fixed bulk one-loop determinant",
                "the conformal-factor integration cycle or determinant phase",
                "a zero-lapse-uniform full configuration-space kernel",
                "a global Picard-Lefschetz flow, Stokes matrix, or intersection number",
                "the physical WDW rigging-map domain or inner product",
                "a positive density, probability, entropy, Pin lift, or local SUGRA completion",
            ],
        },
        "source_scope": {
            "Halliwell_1988": "BFV minisuperspace lapse range and Wheeler-DeWitt boundary identity; DOI 10.1103/PhysRevD.38.2468",
            "Teitelboim_1983": "positive proper time and causal versus gauge-invariant objects; DOI 10.1103/PhysRevLett.50.705",
            "Marolf_1995": "single-constraint refined algebraic quantization and group averaging; arXiv gr-qc/9508015",
            "Gutzwiller_1967": "Van Vleck, Jacobi, and caustic semiclassics; DOI 10.1063/1.1705112",
            "Gibbons_Hawking_Perry_1978": "indefinite Euclidean gravitational action and conformal contour; DOI 10.1016/0550-3213(78)90161-X",
            "Banihashemi_Jacobson_2025": "below-origin lapse contour after momentum integration in its stated gravitational setup; DOI 10.1103/PhysRevD.111.066014; it does not determine this model's n_sigma",
        },
        "next_calculation": (
            "derive the BFV/FP measure and the zero-lapse-uniform determinant, "
            "then count lateral relative intersections on the full complex BVP surface"
        ),
    }
    print("PHASE27_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
