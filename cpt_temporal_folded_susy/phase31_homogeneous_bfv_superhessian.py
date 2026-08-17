#!/usr/bin/env python3
"""Phase 31 -- homogeneous finite-cutoff BFV super-Hessian gate.

The frozen Phase-24/25 connected Euclidean Starobinsky interval is reused.
Its midpoint configuration action is first lifted back to the canonical
phase-space action

    sum_e [p_e (q_{e+1}-q_e) - h T H_E(q_{e+1/2}, p_e)].

The program then keeps the global proper-time modulus T separate and adds all
nonzero homogeneous proper-time-gauge BFV quartets in a hybrid
continuum-spectral truncation projected by midpoint quadrature.  It
checks momentum elimination, the phase-space/configuration Schur identity,
the proper-time-gauge canonical inertia, and the background-independent
nonzero-mode quartet factor.  A local p_a Faddeev--Popov bracket scan is also recorded, together
with the fact that using p_a as a clock would change the fixed-q endpoint
polarization.

Here ``super-Hessian`` refers only to the Z2 gauge/ghost grading of BFV, not
to supersymmetry or a supergravity Hessian.  This is only a finite-dimensional homogeneous quadratic control.  It does
not fix an absolute determinant-line phase, a global Picard--Lefschetz
intersection number, a continuum BFV measure, an inhomogeneous/SUGRA
superdeterminant, a physical probability, or a globally valid clock.  The
script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
import sympy as sp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase30_conformal_bfv_determinant_line as p30
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase30_conformal_bfv_determinant_line as p30


BASE_TIME = p30.BASE_TIME
CUTOFFS = (5, 9, 10, 11, 20, 40)


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


def starobinsky_symbolic(phi: sp.Expr) -> sp.Expr:
    return sp.Rational(3, 4) * (
        1 - sp.exp(-sp.sqrt(sp.Rational(2, 3)) * phi)
    ) ** 2


def hamiltonian_symbolic(
    scale: sp.Expr,
    phi: sp.Expr,
    momentum_scale: sp.Expr,
    momentum_phi: sp.Expr,
) -> sp.Expr:
    """Euclidean homogeneous Hamiltonian constraint used in Phase 28."""

    return (
        -momentum_scale**2 / (24 * sp.pi**2 * scale)
        + momentum_phi**2 / (4 * sp.pi**2 * scale**3)
        + 2
        * sp.pi**2
        * (3 * scale - scale**3 * starobinsky_symbolic(phi))
    )


def canonical_poisson(
    first: sp.Expr,
    second: sp.Expr,
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
) -> sp.Expr:
    """Canonical Poisson bracket for the finite homogeneous phase space."""

    return sp.simplify(
        sum(
            sp.diff(first, coordinate) * sp.diff(second, momentum)
            - sp.diff(first, momentum) * sp.diff(second, coordinate)
            for coordinate, momentum in zip(coordinates, momenta, strict=True)
        )
    )


@lru_cache(maxsize=1)
def phase_space_element_hessian() -> object:
    """Lambdified Hessian of one midpoint phase-space element.

    Variable order is (a_L, phi_L, a_R, phi_R, p_a, p_phi, T).
    """

    a_l, phi_l, a_r, phi_r, p_a, p_phi, proper_time, step = sp.symbols(
        "a_l phi_l a_r phi_r p_a p_phi T h", real=True
    )
    a_mid = (a_l + a_r) / 2
    phi_mid = (phi_l + phi_r) / 2
    constraint = hamiltonian_symbolic(a_mid, phi_mid, p_a, p_phi)
    element = (
        p_a * (a_r - a_l)
        + p_phi * (phi_r - phi_l)
        - step * proper_time * constraint
    )
    variables = (a_l, phi_l, a_r, phi_r, p_a, p_phi, proper_time)
    return sp.lambdify(
        (a_l, phi_l, a_r, phi_r, p_a, p_phi, proper_time, step),
        sp.hessian(element, variables),
        "numpy",
    )


@lru_cache(maxsize=1)
def hamiltonian_gradient() -> object:
    scale, phi, p_a, p_phi = sp.symbols("a phi p_a p_phi", real=True)
    constraint = hamiltonian_symbolic(scale, phi, p_a, p_phi)
    return sp.lambdify(
        (scale, phi, p_a, p_phi),
        [sp.diff(constraint, variable) for variable in (scale, phi, p_a, p_phi)],
        "numpy",
    )


def inertia(matrix: np.ndarray, *, zero_tolerance: float = 1e-9) -> dict[str, object]:
    eigenvalues = np.linalg.eigvalsh(0.5 * (matrix + matrix.T))
    scale = max(float(np.max(np.abs(eigenvalues))), 1.0)
    tolerance = zero_tolerance * scale
    return {
        "negative": int(np.count_nonzero(eigenvalues < -tolerance)),
        "zero": int(np.count_nonzero(np.abs(eigenvalues) <= tolerance)),
        "positive": int(np.count_nonzero(eigenvalues > tolerance)),
        "min_abs_eigenvalue": float(np.min(np.abs(eigenvalues))),
        "max_abs_eigenvalue": float(np.max(np.abs(eigenvalues))),
        "relative_min_abs_eigenvalue": float(
            np.min(np.abs(eigenvalues)) / max(np.max(np.abs(eigenvalues)), 1.0)
        ),
    }


def sampled_nodes_and_momenta(
    segment_count: int, data: dict[str, object]
) -> tuple[np.ndarray, np.ndarray]:
    dense = data["dense_solution"]
    node_times = np.linspace(0.0, BASE_TIME, segment_count + 1)
    nodes = np.asarray(dense(node_times))[[0, 2]].T
    step = 1.0 / segment_count
    momenta = np.zeros((segment_count, 2), dtype=float)
    for element_index in range(segment_count):
        left = nodes[element_index]
        right = nodes[element_index + 1]
        midpoint_scale = 0.5 * (left[0] + right[0])
        delta = right - left
        momenta[element_index, 0] = (
            -12.0
            * np.pi**2
            * midpoint_scale
            * delta[0]
            / (step * BASE_TIME)
        )
        momenta[element_index, 1] = (
            2.0
            * np.pi**2
            * midpoint_scale**3
            * delta[1]
            / (step * BASE_TIME)
        )
    return nodes, momenta


def q_index(node_index: int, component: int, segment_count: int) -> int | None:
    """Return the fixed-endpoint interior-q index, or None at a boundary."""

    if node_index == 0 or node_index == segment_count:
        return None
    return 2 * (node_index - 1) + component


def assemble_phase_space_control(
    segment_count: int, data: dict[str, object]
) -> dict[str, object]:
    """Assemble canonical and alpha=0 nonzero-mode BFV quadratic blocks."""

    nodes, momenta = sampled_nodes_and_momenta(segment_count, data)
    step = 1.0 / segment_count
    q_size = 2 * (segment_count - 1)
    p_size = 2 * segment_count
    canonical_size = q_size + p_size + 1
    proper_time_index = canonical_size - 1
    canonical = np.zeros((canonical_size, canonical_size), dtype=float)
    local_hessian = phase_space_element_hessian()

    momentum_residuals: list[float] = []
    discrete_constraint_residuals: list[float] = []
    for element_index in range(segment_count):
        left = nodes[element_index]
        right = nodes[element_index + 1]
        p_a, p_phi = momenta[element_index]
        midpoint_scale = 0.5 * (left[0] + right[0])
        midpoint_phi = 0.5 * (left[1] + right[1])
        delta = right - left
        discrete_constraint_residuals.append(
            abs(
                -p_a**2 / (24.0 * np.pi**2 * midpoint_scale)
                + p_phi**2 / (4.0 * np.pi**2 * midpoint_scale**3)
                + 2.0
                * np.pi**2
                * (
                    3.0 * midpoint_scale
                    - midpoint_scale**3 * p25.potential(midpoint_phi)
                )
            )
        )
        momentum_residuals.extend(
            [
                delta[0]
                + step * BASE_TIME * p_a / (12.0 * np.pi**2 * midpoint_scale),
                delta[1]
                - step
                * BASE_TIME
                * p_phi
                / (2.0 * np.pi**2 * midpoint_scale**3),
            ]
        )
        local = np.asarray(
            local_hessian(
                left[0],
                left[1],
                right[0],
                right[1],
                p_a,
                p_phi,
                BASE_TIME,
                step,
            ),
            dtype=float,
        )
        global_indices: list[int | None] = [
            q_index(element_index, 0, segment_count),
            q_index(element_index, 1, segment_count),
            q_index(element_index + 1, 0, segment_count),
            q_index(element_index + 1, 1, segment_count),
            q_size + 2 * element_index,
            q_size + 2 * element_index + 1,
            proper_time_index,
        ]
        for local_row, global_row in enumerate(global_indices):
            if global_row is None:
                continue
            for local_column, global_column in enumerate(global_indices):
                if global_column is None:
                    continue
                canonical[global_row, global_column] += local[
                    local_row, local_column
                ]

    # Direct configuration Hessian in x=(interior q,T), used as an independent
    # numerical target for exact Gaussian elimination of all element momenta.
    x_indices = list(range(q_size)) + [proper_time_index]
    p_indices = list(range(q_size, q_size + p_size))
    b_xx = canonical[np.ix_(x_indices, x_indices)]
    b_xp = canonical[np.ix_(x_indices, p_indices)]
    b_pp = canonical[np.ix_(p_indices, p_indices)]
    configuration_from_phase_space = b_xx - b_xp @ np.linalg.solve(
        b_pp, b_xp.T
    )

    configuration_direct = np.zeros((q_size + 1, q_size + 1), dtype=float)
    configuration_element = p30.element_hessian()
    configuration_time_index = q_size
    for element_index in range(segment_count):
        left = nodes[element_index]
        right = nodes[element_index + 1]
        local = np.asarray(
            configuration_element(
                left[0],
                left[1],
                right[0],
                right[1],
                BASE_TIME,
                step,
            ),
            dtype=float,
        )
        global_indices = [
            q_index(element_index, 0, segment_count),
            q_index(element_index, 1, segment_count),
            q_index(element_index + 1, 0, segment_count),
            q_index(element_index + 1, 1, segment_count),
            configuration_time_index,
        ]
        for local_row, global_row in enumerate(global_indices):
            if global_row is None:
                continue
            for local_column, global_column in enumerate(global_indices):
                if global_column is None:
                    continue
                configuration_direct[global_row, global_column] += local[
                    local_row, local_column
                ]

    field = configuration_direct[:-1, :-1]
    field_lapse = configuration_direct[:-1, -1]
    lapse_schur = float(
        configuration_direct[-1, -1]
        - field_lapse @ np.linalg.solve(field, field_lapse)
    )

    # Continuum nonconstant lapse harmonics are the cosine partners of
    # endpoint-vanishing sine modes, truncated at k=m-1 and projected here by
    # midpoint quadrature.  d=k*pi is not an exact derivative eigenvalue of
    # the q,p midpoint lattice.  T remains the separate k=0 modulus.
    nonzero_count = segment_count - 1
    mode_numbers = np.arange(1, segment_count, dtype=float)
    frequencies = np.pi * mode_numbers
    mode_values = np.sqrt(2.0) * np.cos(
        np.pi
        * np.outer(
            (np.arange(segment_count, dtype=float) + 0.5) / segment_count,
            mode_numbers,
        )
    )
    coupling = np.zeros((canonical_size, nonzero_count), dtype=float)
    gradient = hamiltonian_gradient()
    for element_index in range(segment_count):
        left = nodes[element_index]
        right = nodes[element_index + 1]
        midpoint = 0.5 * (left + right)
        p_a, p_phi = momenta[element_index]
        h_a, h_phi, h_pa, h_pphi = map(
            float, gradient(midpoint[0], midpoint[1], p_a, p_phi)
        )
        local_gradient = (0.5 * h_a, 0.5 * h_phi, 0.5 * h_a, 0.5 * h_phi)
        local_q_indices = (
            q_index(element_index, 0, segment_count),
            q_index(element_index, 1, segment_count),
            q_index(element_index + 1, 0, segment_count),
            q_index(element_index + 1, 1, segment_count),
        )
        for local_index, global_index in enumerate(local_q_indices):
            if global_index is not None:
                coupling[global_index] += (
                    -step * local_gradient[local_index] * mode_values[element_index]
                )
        coupling[q_size + 2 * element_index] += (
            -step * h_pa * mode_values[element_index]
        )
        coupling[q_size + 2 * element_index + 1] += (
            -step * h_pphi * mode_values[element_index]
        )

    frequency_matrix = np.diag(frequencies)
    zero_modes = np.zeros((nonzero_count, nonzero_count), dtype=float)
    full_bfv_bosonic = np.block(
        [
            [canonical, coupling, np.zeros_like(coupling)],
            [coupling.T, zero_modes, -frequency_matrix],
            [np.zeros_like(coupling.T), -frequency_matrix, zero_modes],
        ]
    )
    uncoupled_bfv_bosonic = np.block(
        [
            [canonical, np.zeros_like(coupling), np.zeros_like(coupling)],
            [np.zeros_like(coupling.T), zero_modes, -frequency_matrix],
            [np.zeros_like(coupling.T), -frequency_matrix, zero_modes],
        ]
    )

    canonical_sign, canonical_logdet = np.linalg.slogdet(canonical)
    full_sign, full_logdet = np.linalg.slogdet(full_bfv_bosonic)
    uncoupled_sign, uncoupled_logdet = np.linalg.slogdet(uncoupled_bfv_bosonic)
    gauge_log_magnitude = float(2.0 * np.sum(np.log(frequencies)))
    expected_gauge_sign = -1.0 if nonzero_count % 2 else 1.0
    ghost_pfaffian_log_magnitude = gauge_log_magnitude

    return {
        "segments": segment_count,
        "stationary_momentum_max_residual": float(
            np.max(np.abs(momentum_residuals))
        ),
        "sampled_midpoint_constraint_max_residual": float(
            np.max(discrete_constraint_residuals)
        ),
        "configuration_schur_relative_residual": float(
            np.linalg.norm(
                configuration_from_phase_space - configuration_direct, ord=2
            )
            / np.linalg.norm(configuration_direct, ord=2)
        ),
        "momentum_inertia": inertia(b_pp),
        "configuration_inertia": inertia(configuration_direct),
        "proper_time_canonical_inertia": inertia(canonical),
        "full_bfv_bosonic_inertia": inertia(full_bfv_bosonic),
        "proper_time_canonical_determinant_sign": float(canonical_sign),
        "full_bfv_bosonic_determinant_sign": float(full_sign),
        "expected_full_bfv_bosonic_determinant_sign": float(
            canonical_sign * expected_gauge_sign
        ),
        "gauge_factor_log_residual": float(
            full_logdet - canonical_logdet - gauge_log_magnitude
        ),
        "coupling_independence_log_residual": float(full_logdet - uncoupled_logdet),
        "coupling_independence_sign_match": bool(full_sign == uncoupled_sign),
        "bosonic_gauge_log_magnitude": float(full_logdet - canonical_logdet),
        "ghost_pfaffian_log_magnitude": ghost_pfaffian_log_magnitude,
        "bosonic_to_ghost_log_match_residual": float(
            (full_logdet - canonical_logdet - ghost_pfaffian_log_magnitude)
        ),
        "lapse_schur": lapse_schur,
        "coupling_norm": float(np.linalg.norm(coupling, ord=2)),
        "frequencies": frequencies.tolist(),
    }


def extrinsic_clock_scan(data: dict[str, object]) -> dict[str, object]:
    """Scan the local p_a FP bracket without changing endpoint polarization."""

    dense = data["dense_solution"]
    times = np.linspace(0.0, BASE_TIME, 1001)
    states = np.asarray(dense(times))
    scale, scale_velocity, phi, phi_velocity = states
    p_a = -12.0 * np.pi**2 * scale * scale_velocity
    p_phi = 2.0 * np.pi**2 * scale**3 * phi_velocity
    potential = np.asarray(p25.potential(phi), dtype=float)
    fp_direct = (
        -p_a**2 / (24.0 * np.pi**2 * scale**2)
        + 3.0 * p_phi**2 / (4.0 * np.pi**2 * scale**4)
        - 6.0 * np.pi**2 * (1.0 - scale**2 * potential)
    )
    fp_on_constraint = 2.0 * np.pi**2 * (
        -6.0 + scale**2 * phi_velocity**2 + 4.0 * scale**2 * potential
    )
    midpoint = len(times) // 2
    endpoint_legendre_shift = float(
        scale[-1] * p_a[-1] - scale[0] * p_a[0]
    )
    return {
        "sample_count": len(times),
        "min_FP_bracket": float(np.min(fp_direct)),
        "max_FP_bracket": float(np.max(fp_direct)),
        "neck_FP_bracket": float(fp_direct[midpoint]),
        "constraint_form_max_residual": float(
            np.max(np.abs(fp_direct - fp_on_constraint))
        ),
        "p_a_left": float(p_a[0]),
        "p_a_right": float(p_a[-1]),
        "p_a_min_step": float(np.min(np.diff(p_a))),
        "intrinsic_a_clock_bracket_at_neck": float(scale_velocity[midpoint]),
        "intrinsic_phi_clock_bracket_at_neck": float(phi_velocity[midpoint]),
        "fixed_q_to_mixed_pa_boundary_legendre_shift": endpoint_legendre_shift,
        "status": (
            "p_a is a regular local bulk clock on the recorded real saddle; "
            "enforcing it at the endpoints would change the fixed-(a,phi) "
            "kernel to a mixed boundary polarization"
        ),
    }


def exact_controls(audit: Audit) -> dict[str, object]:
    a, phi, p_a, p_phi, proper_time, step = sp.symbols(
        "a phi p_a p_phi T h", positive=True, real=True
    )
    delta_a, delta_phi = sp.symbols("Delta_a Delta_phi", real=True)
    constraint = hamiltonian_symbolic(a, phi, p_a, p_phi)
    element = p_a * delta_a + p_phi * delta_phi - step * proper_time * constraint
    stationary_p_a = -12 * sp.pi**2 * a * delta_a / (step * proper_time)
    stationary_p_phi = 2 * sp.pi**2 * a**3 * delta_phi / (
        step * proper_time
    )
    audit.exact(
        "P31.Hamiltonian.stationary_element_momenta",
        sp.simplify(sp.diff(element, p_a).subs(p_a, stationary_p_a)) == 0
        and sp.simplify(sp.diff(element, p_phi).subs(p_phi, stationary_p_phi))
        == 0,
        "the midpoint canonical element has the declared exact stationary momenta",
    )
    eliminated = sp.simplify(
        element.subs({p_a: stationary_p_a, p_phi: stationary_p_phi})
    )
    expected = 2 * sp.pi**2 * (
        (-6 * a * delta_a**2 + a**3 * delta_phi**2)
        / (2 * proper_time * step)
        + proper_time
        * step
        * (-3 * a + a**3 * starobinsky_symbolic(phi))
    )
    audit.exact(
        "P31.Hamiltonian.configuration_element_recovered",
        sp.simplify(eliminated - expected) == 0,
        "exact momentum elimination reproduces the Phase-30 midpoint configuration element",
    )

    x_1, x_2, m_1, m_2, c_11, c_12, c_22 = sp.symbols(
        "x1 x2 m1 m2 c11 c12 c22", nonzero=True, real=True
    )
    b_xx = sp.Matrix([[c_11, c_12], [c_12, c_22]])
    b_xp = sp.Matrix([[x_1, 0], [0, x_2]])
    b_pp = sp.diag(m_1, m_2)
    block = b_xx.row_join(b_xp).col_join(b_xp.T.row_join(b_pp))
    schur = b_xx - b_xp * b_pp.inv() * b_xp.T
    audit.exact(
        "P31.Hessian.momentum_Schur_determinant",
        sp.factor(block.det() - b_pp.det() * schur.det()) == 0,
        "the phase-space determinant factors into the momentum block and the configuration Schur complement",
    )

    lapse, primary = sp.symbols("N Pi", real=True)
    canonical_coordinates = (a, phi, lapse)
    canonical_momenta = (p_a, p_phi, primary)
    audit.exact(
        "P31.BFV.abelian_constraint_nilpotence",
        canonical_poisson(
            constraint, constraint, canonical_coordinates, canonical_momenta
        )
        == 0
        and canonical_poisson(
            constraint, primary, canonical_coordinates, canonical_momenta
        )
        == 0,
        "H_E and Pi form an Abelian one-constraint BFV algebra, so Omega=c H_E+rho Pi is classically nilpotent",
    )

    a_11, a_12, a_22, c_1, c_2, frequency = sp.symbols(
        "A11 A12 A22 C1 C2 d", nonzero=True, real=True
    )
    canonical = sp.Matrix([[a_11, a_12], [a_12, a_22]])
    coupling = sp.Matrix([c_1, c_2])
    bosonic = sp.BlockMatrix(
        [
            [canonical, coupling, sp.zeros(2, 1)],
            [coupling.T, sp.zeros(1, 1), sp.Matrix([[-frequency]])],
            [sp.zeros(1, 2), sp.Matrix([[-frequency]]), sp.zeros(1, 1)],
        ]
    ).as_explicit()
    audit.exact(
        "P31.BFV.bosonic_quartet_determinant",
        sp.factor(bosonic.det() + frequency**2 * canonical.det()) == 0,
        "one alpha=0 nonzero lapse-multiplier pair contributes -d^2 independently of its coupling to the proper-time-gauge canonical Hessian",
    )

    ghost = sp.Matrix(
        [
            [0, 0, 0, -frequency],
            [0, 0, -frequency, 0],
            [0, frequency, 0, 1],
            [frequency, 0, -1, 0],
        ]
    )
    ghost_pfaffian = (
        ghost[0, 1] * ghost[2, 3]
        - ghost[0, 2] * ghost[1, 3]
        + ghost[0, 3] * ghost[1, 2]
    )
    audit.exact(
        "P31.BFV.ghost_quartet_Pfaffian",
        sp.simplify(ghost_pfaffian - frequency**2) == 0
        and sp.simplify(ghost.det() - frequency**4) == 0,
        "the ordered first-order ghost quartet (c,barc,rho,barrho) has Pfaffian d^2",
    )
    coordinate = sp.symbols("s", real=True)
    mode_number = sp.symbols("k", integer=True, positive=True)
    sine_mode = sp.sqrt(2) * sp.sin(sp.pi * mode_number * coordinate)
    cosine_mode = sp.sqrt(2) * sp.cos(sp.pi * mode_number * coordinate)
    audit.exact(
        "P31.BFV.continuum_spectral_pair_derivative",
        sp.simplify(
            sp.diff(sine_mode, coordinate)
            - sp.pi * mode_number * cosine_mode
        )
        == 0,
        "the truncated continuum sine/cosine gauge pair has derivative eigenvalue d_k=k pi before midpoint projection",
    )
    audit.exact(
        "P31.BFV.global_lapse_mode_separation",
        sp.integrate(sp.cos(sp.pi * mode_number * coordinate), (coordinate, 0, 1))
        == 0,
        "the k>=1 cosine lapse modes have zero average, leaving T as a separate unpaired global modulus",
    )

    bracket = sp.simplify(-sp.diff(constraint, a))
    expected_bracket = (
        -p_a**2 / (24 * sp.pi**2 * a**2)
        + 3 * p_phi**2 / (4 * sp.pi**2 * a**4)
        - 6 * sp.pi**2 * (1 - a**2 * starobinsky_symbolic(phi))
    )
    scale_velocity, phi_velocity = sp.symbols("adot phidot", real=True)
    velocity_bracket = bracket.subs(
        {
            p_a: -12 * sp.pi**2 * a * scale_velocity,
            p_phi: 2 * sp.pi**2 * a**3 * phi_velocity,
        },
        simultaneous=True,
    )
    on_constraint = sp.simplify(
        velocity_bracket.subs(
            scale_velocity**2,
            1
            + a**2
            * (
                sp.Rational(1, 2) * phi_velocity**2
                - starobinsky_symbolic(phi)
            )
            / 3,
        )
    )
    target_on_constraint = 2 * sp.pi**2 * (
        -6
        + a**2 * phi_velocity**2
        + 4 * a**2 * starobinsky_symbolic(phi)
    )
    audit.exact(
        "P31.clock.pa_FP_bracket_identity",
        sp.simplify(bracket - expected_bracket) == 0
        and sp.simplify(on_constraint - target_on_constraint) == 0,
        "the extrinsic p_a clock bracket has the declared exact off-shell and on-constraint forms",
    )

    return {
        "Hamiltonian_constraint": (
            "H_E=-p_a^2/(24 pi^2 a)+p_phi^2/(4 pi^2 a^3)"
            "+2 pi^2(3a-a^3 V)"
        ),
        "BFV_charge": "Omega=c H_E+rho Pi",
        "gauge_fermion": "Psi_0=-N barrho",
        "nonzero_mode_bosonic_block": "[[A,C,0],[C^T,0,-D],[0,-D,0]]",
        "ghost_order": ["c", "barc", "rho", "barrho"],
        "mode_boundary_conditions": {
            "endpoint_vanishing_sine": ["c", "barc", "Pi"],
            "cosine": ["N", "rho", "barrho"],
        },
        "regulator_definition": (
            "continuum sine-cosine gauge harmonics truncated at k=m-1 and "
            "projected against the q-p midpoint discretization; d_k=k pi is "
            "not an exact derivative eigenvalue of that midpoint lattice"
        ),
        "global_modulus": "T is k=0 and is not divided out by the nonzero BFV quartets",
        "zero_mode_ledger": (
            "endpoint-vanishing c, barc, and Pi have no k=0 mode; the "
            "algebraic rho-barrho k=0 pair is eliminated and declared a "
            "background-independent unit only in the same-hybrid-regulator relative "
            "normalization"
        ),
        "super_Hessian_meaning": (
            "Z2 BFV gauge-ghost grading only; not a SUSY or SUGRA Hessian"
        ),
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    data = p30.base_trajectory()
    base = data["base"]
    curvature = float(data["curvature"])
    audit.numerical(
        "P31.saddle.frozen_phase30_control",
        abs(base.action - float(data["benchmark_action"])) < 2e-10
        and abs(base.constraint) < 2e-11
        and base.endpoint_residual < 2e-10
        and abs(curvature + 8.9231430383) < 5e-7,
        "the fixed-boundary Euclidean interval and negative global-lapse curvature are unchanged",
    )

    controls = [assemble_phase_space_control(count, data) for count in CUTOFFS]
    discrete_constraint_residuals = np.asarray(
        [
            item["sampled_midpoint_constraint_max_residual"]
            for item in controls
        ],
        dtype=float,
    )
    scaled_constraint_residuals = discrete_constraint_residuals * np.asarray(
        CUTOFFS, dtype=float
    ) ** 2
    audit.numerical(
        "P31.background.sampled_discrete_constraint_convergence",
        np.all(discrete_constraint_residuals > 0.0)
        and np.all(np.diff(discrete_constraint_residuals) < 0.0)
        and discrete_constraint_residuals[-1] < 2e-3
        and np.ptp(scaled_constraint_residuals)
        / np.mean(scaled_constraint_residuals)
        < 2e-3,
        "the sampled midpoint constraint is nonzero at every cutoff and decays as O(m^-2), exposing that the continuum saddle is not a new exact finite-lattice critical point",
    )
    audit.numerical(
        "P31.Hamiltonian.sampled_stationary_momenta",
        max(item["stationary_momentum_max_residual"] for item in controls)
        < 2e-16,
        "the sampled element momenta solve their discrete stationary equations to roundoff",
    )
    audit.numerical(
        "P31.Hessian.phase_to_configuration_Schur",
        max(item["configuration_schur_relative_residual"] for item in controls)
        < 5e-15,
        "eliminating all element momenta reproduces the independently assembled configuration-plus-T Hessian",
    )
    audit.numerical(
        "P31.Hessian.proper_time_canonical_inertia_and_parity",
        all(
            item["momentum_inertia"]["negative"] == item["segments"]
            and item["configuration_inertia"]["negative"] == item["segments"]
            and item["proper_time_canonical_inertia"]["negative"]
            == 2 * item["segments"]
            and item["proper_time_canonical_inertia"]["zero"] == 0
            and item["proper_time_canonical_determinant_sign"] == 1.0
            for item in controls
        ),
        "the momentum and configuration Schur blocks each carry m negative directions, while the unreduced proper-time-gauge canonical determinant stays positive for odd and even cutoffs",
    )
    audit.numerical(
        "P31.BFV.full_bosonic_inertia",
        all(
            item["full_bfv_bosonic_inertia"]["negative"]
            == 3 * item["segments"] - 1
            and item["full_bfv_bosonic_inertia"]["zero"] == 0
            and item["full_bfv_bosonic_determinant_sign"]
            == item["expected_full_bfv_bosonic_determinant_sign"]
            for item in controls
        ),
        "each nonzero lapse-multiplier pair adds one positive and one negative direction, so its finite-cutoff sign is kept separate from the proper-time-gauge canonical block",
    )
    audit.numerical(
        "P31.BFV.coupled_block_factorization",
        max(abs(item["gauge_factor_log_residual"]) for item in controls) < 5e-8
        and max(abs(item["coupling_independence_log_residual"]) for item in controls)
        < 5e-8
        and all(item["coupling_independence_sign_match"] for item in controls)
        and min(item["coupling_norm"] for item in controls) > 1e-3,
        "the actual nonzero lapse coupling is nontrivial but leaves the alpha=0 bosonic determinant factor exactly background-independent within numerical precision",
    )
    audit.numerical(
        "P31.BFV.same_regulator_relative_normalization",
        max(
            abs(item["bosonic_to_ghost_log_match_residual"])
            for item in controls
        )
        < 5e-8,
        "the bosonic gauge determinant and ghost Pfaffian are fixed d-dependent factors that each drop out of identical hybrid-regulator benchmark/reference ratios; no absolute within-amplitude unity is inferred",
    )
    audit.numerical(
        "P31.spectrum.no_finite_cutoff_zero_mode",
        all(
            item["momentum_inertia"]["zero"] == 0
            and item["configuration_inertia"]["zero"] == 0
            and item["proper_time_canonical_inertia"]["zero"] == 0
            and item["full_bfv_bosonic_inertia"]["zero"] == 0
            and item["proper_time_canonical_inertia"][
                "relative_min_abs_eigenvalue"
            ]
            > 1e-10
            for item in controls
        ),
        "no homogeneous eigenvalue is numerically zero at any recorded finite cutoff",
    )
    schur_values = [float(item["lapse_schur"]) for item in controls]
    audit.numerical(
        "P31.lapse.global_modulus_Schur_convergence",
        np.all(np.diff(schur_values) < 0)
        and abs(schur_values[-1] - curvature) < 7e-3,
        "the separately retained global T Schur complement converges toward the Phase-30 W_TT control",
    )

    clock = extrinsic_clock_scan(data)
    audit.numerical(
        "P31.clock.pa_local_bulk_regular",
        clock["min_FP_bracket"] > 100.0
        and abs(clock["neck_FP_bracket"] - 12.0 * np.pi**2) < 2e-9
        and clock["constraint_form_max_residual"] < 2e-8
        and clock["p_a_min_step"] > 0.0
        and abs(clock["intrinsic_a_clock_bracket_at_neck"]) < 2e-12
        and abs(clock["intrinsic_phi_clock_bracket_at_neck"]) < 2e-12
        and abs(clock["fixed_q_to_mixed_pa_boundary_legendre_shift"]) > 300.0,
        "p_a is a regular monotone bulk clock on this recorded saddle while intrinsic a and phi clocks vanish at the neck; its nonzero boundary Legendre shift forbids reusing the fixed-q kernel unchanged",
    )

    return {
        "base": {
            "T_star": BASE_TIME,
            "W_star": base.action,
            "W_TT": curvature,
            "boundary": np.asarray(data["boundary"], dtype=float).tolist(),
        },
        "cutoff_controls": controls,
        "extrinsic_clock_scan": clock,
        "quartet_interpretation": {
            "absolute_factor": "not assigned",
            "relative_statement": (
                "at fixed hybrid regulator, the nonzero quartet factor is independent "
                "of the background and cancels between benchmark and reference"
            ),
            "global_T": "retained as the unreduced proper-time integration modulus",
            "auxiliary_k0": (
                "omitted as a declared background-independent relative unit; "
                "no absolute zero-mode normalization is inferred"
            ),
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P31",
        "calculation": "homogeneous finite-cutoff BFV Z2-graded phase-space super-Hessian gate",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_phase30_configuration_Hessian_is_the_momentum_Schur_complement_of_the_canonical_phase_space_Hessian": "SUPPORTED_EXACTLY_AND_NUMERICALLY_AT_THE_RECORDED_CUTOFFS",
            "the_proper_time_gauge_canonical_q_p_T_determinant_sign_is_stable_across_recorded_odd_even_cutoffs": "SUPPORTED_IN_THE_FINITE_CUTOFF_HOMOGENEOUS_CONTROL",
            "the_nonzero_alpha0_BFV_quartet_factor_depends_on_the_background_lapse_coupling": "CONTRADICTED_BY_EXACT_BLOCK_FACTORIZATION",
            "the_nonzero_BFV_quartets_cancel_in_a_same_regulator_relative_normalization": "SUPPORTED_AS_A_RELATIVE_FINITE_DIMENSIONAL_IDENTITY_ONLY",
            "the_full_bosonic_BFV_cutoff_sign_equals_the_proper_time_gauge_canonical_determinant_line": "CONTRADICTED_BY_THE_ADDITIONAL_GAUGE_PAIR_PARITY",
            "pa_is_a_regular_local_bulk_clock_on_the_recorded_real_saddle": "SUPPORTED_BY_A_BOUNDED_NUMERICAL_SCAN",
            "the_fixed_q_seam_kernel_can_be_reinterpreted_as_a_global_pa_clock_kernel_without_boundary_terms": "CONTRADICTED_BY_THE_ENDPOINT_POLARIZATION_CHANGE",
            "the_absolute_BFV_contour_phase_or_global_PL_coefficient_is_fixed": "OPEN_NOT_DERIVED",
            "a_continuum_physical_probability_or_SUSY_seam_state_is_obtained": "OPEN_NOT_COMPUTED",
            "super_Hessian_here_is_a_SUSY_or_SUGRA_Hessian": "CONTRADICTED_BY_DEFINITION_IT_IS_ONLY_THE_BFV_Z2_GAUGE_GHOST_GRADING",
        },
        "scope_guard": {
            "computed": [
                "the frozen homogeneous proper-time-gauge canonical Hessian in (q,p,T)",
                "exact momentum elimination and finite-cutoff Schur complements",
                "all nonzero homogeneous alpha=0 lapse-multiplier and first-order ghost quartet blocks",
                "relative same-hybrid-regulator quartet cancellation and finite-cutoff inertia",
                "a bounded local p_a Faddeev--Popov bracket scan on the real saddle",
            ],
            "not_computed": [
                "an absolute BFV measure, contour orientation, or continuum determinant-line phase",
                "a global nonlinear Picard--Lefschetz cycle or integer intersection coefficient",
                "a global p_a clock theorem or a fixed-q-to-mixed-polarization kernel transform",
                "inhomogeneous graviton, scalar, chiralino, gravitino, and ghost harmonics",
                "a WDW physical trace, density matrix, Pin lift, flux distribution, or SUSY-breaking spectrum",
                "a constraint-reduced physical phase space or a SUSY/SUGRA super-Hessian",
            ],
        },
        "next_calculation": (
            "derive the determinant-line orientation from a regulated global lapse contour, "
            "then extend the relative BFV superdeterminant to inhomogeneous S3 harmonics "
            "before assigning any quantum seam weight"
        ),
    }
    print("PHASE31_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
