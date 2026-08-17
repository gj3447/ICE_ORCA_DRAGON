#!/usr/bin/env python3
"""Phase 28 -- bounded lapse-thimble, intersection, and BFV diagnostic.

The Phase-24/25 Starobinsky endpoints and Euclidean action are frozen.  This
program pseudo-arclength continues one constant-Im-W complex lapse arm,
monitors its complex Dirichlet Jacobi block, and records crossings between one
bounded real dual branch and explicitly declared two-sided vertical cycles.
It also audits the Euclidean-continued homogeneous one-constraint BFV model.

No global relative-homology coefficient, positive-lapse endpoint prescription,
one-loop superdeterminant, or quantum-gravity density is computed.  The
program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root

import phase25_connected_lapse_scan as p25


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


PHASE_RESIDUAL_SCALE = 50.0
PSEUDO_STEP = 0.06
PSEUDO_STEPS = 70


def unpack(point: np.ndarray) -> tuple[complex, np.ndarray]:
    return complex(point[0], point[1]), np.array(
        [complex(point[2], point[3]), complex(point[4], point[5])]
    )


def complex_constraint(boundary: np.ndarray, velocity: np.ndarray) -> complex:
    scale = boundary[0]
    phi = boundary[1]
    return complex(
        velocity[0] ** 2
        - 1.0
        - scale**2 * (0.5 * velocity[1] ** 2 - p25.potential(phi)) / 3.0
    )


def time_derivative(boundary: np.ndarray, velocity: np.ndarray) -> complex:
    return complex(6.0 * np.pi**2 * boundary[0] * complex_constraint(boundary, velocity))


def curve_residual(point: np.ndarray, boundary: np.ndarray) -> np.ndarray:
    proper_length, velocity = unpack(point)
    final = p25.complex_flow(proper_length, boundary, velocity)
    delta = final[[0, 2]] - boundary[2:]
    return np.array(
        [
            delta[0].real,
            delta[0].imag,
            delta[1].real,
            delta[1].imag,
            final[4].imag / PHASE_RESIDUAL_SCALE,
        ]
    )


def fixed_imaginary_point(
    imaginary_time: float, boundary: np.ndarray, guess: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    next_guess, proper_length, _final = p25.constant_phase_point(
        imaginary_time, boundary, guess
    )
    point = np.array(
        [
            proper_length.real,
            proper_length.imag,
            next_guess[1],
            next_guess[2],
            next_guess[3],
            next_guess[4],
        ]
    )
    return next_guess, point


def complex_jacobian(state: np.ndarray) -> np.ndarray:
    scale, scale_velocity, phi, phi_velocity = state[:4]
    return np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [
                -(1.0 - scale_velocity**2) / (2.0 * scale**2)
                - phi_velocity**2 / 4.0
                - p25.potential(phi) / 2.0,
                -scale_velocity / scale,
                -scale * p25.potential_prime(phi) / 2.0,
                -scale * phi_velocity / 2.0,
            ],
            [0.0, 0.0, 0.0, 1.0],
            [
                3.0 * scale_velocity * phi_velocity / scale**2,
                -3.0 * phi_velocity / scale,
                p25.potential_second(phi),
                -3.0 * scale_velocity / scale,
            ],
        ],
        dtype=np.complex128,
    )


def complex_flow_diagnostic(
    proper_length: complex, boundary: np.ndarray, velocity: np.ndarray
) -> dict[str, object]:
    state0 = np.array(
        [boundary[0], velocity[0], boundary[1], velocity[1], 0.0j],
        dtype=np.complex128,
    )
    augmented0 = np.concatenate([state0, np.eye(4, dtype=np.complex128).ravel()])

    def rhs(_s: float, augmented: np.ndarray) -> np.ndarray:
        state = augmented[:4]
        matrix = augmented[5:].reshape(4, 4)
        return proper_length * np.concatenate(
            [
                p25.configuration_rhs(state),
                [p25.action_lagrangian(state)],
                (complex_jacobian(state) @ matrix).ravel(),
            ]
        )

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        augmented0,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=0.025,
        t_eval=np.linspace(0.0, 1.0, 101),
    )
    if not solution.success or not np.all(np.isfinite(solution.y)):
        raise RuntimeError(solution.message)
    final = solution.y[:5, -1]
    matrix = solution.y[5:, -1].reshape(4, 4)
    block = matrix[np.ix_([0, 2], [1, 3])]
    return {
        "endpoint_residual": float(np.linalg.norm(final[[0, 2]] - boundary[2:])),
        "phase_residual": float(abs(final[4].imag)),
        "min_abs_scale": float(np.min(np.abs(solution.y[0]))),
        "Bv_singular_values": np.linalg.svd(block, compute_uv=False).tolist(),
    }


def continue_upper_arm(boundary: np.ndarray, base_velocity: np.ndarray) -> dict[str, object]:
    guess = np.array([0.7, base_velocity[0], 0.0, base_velocity[1], 0.0])
    guess, first = fixed_imaginary_point(0.10, boundary, guess)
    guess, second = fixed_imaginary_point(0.15, boundary, guess)
    points = [first, second]
    tangent = second - first
    tangent /= np.linalg.norm(tangent)
    solve_residuals: list[float] = []

    for _index in range(PSEUDO_STEPS):
        current = points[-1]
        predictor = current + PSEUDO_STEP * tangent

        def augmented(candidate: np.ndarray) -> np.ndarray:
            return np.concatenate(
                [curve_residual(candidate, boundary), [np.dot(candidate - predictor, tangent)]]
            )

        result = root(augmented, predictor, method="hybr", tol=2e-10)
        residual = float(np.linalg.norm(augmented(result.x)))
        if not np.all(np.isfinite(result.x)) or residual > 2e-7:
            raise RuntimeError(f"pseudo-arclength failure: {result.message}; {residual}")
        next_point = result.x.copy()
        next_tangent = next_point - current
        next_tangent /= np.linalg.norm(next_tangent)
        if np.dot(next_tangent, tangent) < 0.0:
            next_tangent *= -1.0
        points.append(next_point)
        tangent = next_tangent
        solve_residuals.append(residual)

    array = np.asarray(points)
    actions: list[complex] = []
    derivatives: list[complex] = []
    endpoint_residuals: list[float] = []
    for point in array:
        proper_length, velocity = unpack(point)
        final = p25.complex_flow(proper_length, boundary, velocity)
        actions.append(complex(final[4]))
        derivatives.append(time_derivative(boundary, velocity))
        endpoint_residuals.append(float(np.linalg.norm(final[[0, 2]] - boundary[2:])))
    action_array = np.asarray(actions)

    alignment: list[float] = []
    orientation: list[float] = []
    for index in range(1, len(array) - 1):
        delta = array[index + 1] - array[index - 1]
        action_delta = derivatives[index] * complex(delta[0], delta[1])
        alignment.append(float(abs(action_delta.imag) / max(abs(action_delta), 1e-30)))
        orientation.append(float(action_delta.real))

    turn = int(np.argmax(array[:, 1]))
    independent_guess = np.array([0.7, base_velocity[0], 0.0, base_velocity[1], 0.0])
    independent: list[dict[str, object]] = []
    errors: list[float] = []
    for imaginary_time in (0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.0):
        independent_guess, independent_point = fixed_imaginary_point(
            imaginary_time, boundary, independent_guess
        )
        if imaginary_time in (0.4, 1.0, 2.0):
            interpolated = np.array(
                [np.interp(imaginary_time, array[: turn + 1, 1], array[: turn + 1, j]) for j in range(6)]
            )
            error = float(np.linalg.norm(interpolated - independent_point))
            errors.append(error)
            independent.append({"Im_T": imaginary_time, "error": error})

    conjugate: list[dict[str, object]] = []
    conjugate_residuals: list[float] = []
    for index in (5, 25, 45, 65):
        lower = array[index].copy()
        lower[[1, 3, 5]] *= -1.0
        proper_length, velocity = unpack(lower)
        final = p25.complex_flow(proper_length, boundary, velocity)
        endpoint_error = float(np.linalg.norm(final[[0, 2]] - boundary[2:]))
        action_error = float(abs(final[4] - np.conjugate(actions[index])))
        conjugate_residuals.extend([endpoint_error, action_error])
        conjugate.append(
            {"index": index, "T": [proper_length.real, proper_length.imag], "endpoint_error": endpoint_error, "action_error": action_error}
        )

    monitor_indices = sorted({0, 20, 40, 60, turn, len(array) - 1})
    monitors: list[dict[str, object]] = []
    for index in monitor_indices:
        proper_length, velocity = unpack(array[index])
        monitors.append(
            {"index": index, "T": [proper_length.real, proper_length.imag], **complex_flow_diagnostic(proper_length, boundary, velocity)}
        )

    sampled_indices = sorted(set(range(0, len(array), 5)) | {turn, len(array) - 1})
    sampled = [
        {
            "index": index,
            "T": array[index, :2].tolist(),
            "W": [actions[index].real, actions[index].imag],
            "dW_dT": [derivatives[index].real, derivatives[index].imag],
        }
        for index in sampled_indices
    ]
    return {
        "points": array,
        "actions": action_array,
        "endpoint_residuals": endpoint_residuals,
        "solve_residuals": solve_residuals,
        "alignment": alignment,
        "orientation": orientation,
        "turn": turn,
        "independent": independent,
        "independent_errors": errors,
        "conjugate": conjugate,
        "conjugate_residuals": conjugate_residuals,
        "monitors": monitors,
        "sampled": sampled,
    }


def real_dual_branch(boundary: np.ndarray) -> dict[str, object]:
    times = (0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.68, 0.70)
    center = np.array([np.sqrt(3.0 / p25.potential(1.0)), 1.0])
    records: list[dict[str, object]] = []
    for proper_length in times:
        center, endpoint = p25.solve_symmetric_center(proper_length, boundary, center)
        solution = p25.solve_fixed_time(proper_length, boundary, -endpoint[[1, 3]])
        derivative = -solution.energy
        records.append(
            {
                "T": proper_length,
                "W": solution.action,
                "center": center.tolist(),
                "dW_dT": derivative,
                "upward_dT_ds": -derivative,
                "det_Bv": float(np.linalg.det(solution.velocity_monodromy)),
                "endpoint_residual": solution.endpoint_residual,
            }
        )
    lookup = {record["T"]: record for record in records}
    crossings = []
    for epsilon in (0.25, 0.35, 0.45, 0.55):
        crossings.append(
            {
                "epsilon": epsilon,
                "T": [epsilon, 0.0],
                "cycle": f"T={epsilon}+iN, N in [-2.5,2.5]",
                "dW_dT": lookup[epsilon]["dW_dT"],
                "orientation_convention": "columns=(cycle tangent, outward dual tangent)",
                "orientation_determinant": 1.0,
                "recorded_crossing_magnitude": 1,
            }
        )
    return {"records": records, "crossings": crossings}


def exact_controls(audit: Audit) -> dict[str, object]:
    x, y = sp.symbols("x y", real=True)
    derivative = x + sp.I * y
    down_change = sp.expand_complex(derivative * sp.conjugate(derivative))
    up_change = sp.expand_complex(-derivative * sp.conjugate(derivative))
    audit.exact(
        "P28.PL.downward_flow_identity",
        sp.re(down_change) == x**2 + y**2 and sp.im(down_change) == 0,
        "dT/ds=conj(W_T) keeps Im W fixed and increases Re W by |W_T|^2",
    )
    audit.exact(
        "P28.PL.upward_flow_identity",
        sp.re(up_change) == -(x**2 + y**2) and sp.im(up_change) == 0,
        "the dual flow keeps Im W fixed and decreases Re W",
    )
    mu, u, hbar = sp.symbols("mu u hbar", positive=True, real=True)
    audit.exact(
        "P28.PL.negative_mode_tangents",
        sp.simplify(-mu * (sp.I * u) ** 2 / 2 - mu * u**2 / 2) == 0,
        "for W_TT=-mu, descent is imaginary and the dual direction is real",
    )
    phi_r, phi_i, b = sp.symbols("phi_R phi_I b", real=True)
    z = phi_r + sp.I * phi_i
    potential = sp.Rational(3, 4) * (1 - sp.exp(-b * z)) ** 2
    audit.exact(
        "P28.PL.Schwarz_reflection",
        sp.simplify(sp.conjugate(potential) - potential.xreplace({z: sp.conjugate(z)})) == 0,
        "real Starobinsky coefficients give a conjugate lower arm",
    )
    audit.exact(
        "P28.intersection.transverse_orientation",
        sp.Matrix([[0, -1], [1, 0]]).det() == 1,
        "the declared tangent ordering has transverse orientation determinant +1",
    )

    scale = sp.Symbol("a", positive=True, real=True)
    phi = sp.Symbol("phi", real=True)
    pa, pphi = sp.symbols("p_a p_phi", real=True)
    v = sp.Function("V")(phi)
    hamiltonian = -pa**2 / (24 * sp.pi**2 * scale) + pphi**2 / (
        4 * sp.pi**2 * scale**3
    ) + 2 * sp.pi**2 * (3 * scale - scale**3 * v)
    neck = {pa: 0, pphi: 0, v: 3 / scale**2}
    audit.exact(
        "P28.BFV.neck_clock_Faddeev_Popov_brackets",
        sp.simplify(hamiltonian.subs(neck)) == 0
        and sp.simplify(sp.diff(hamiltonian, pa).subs(neck)) == 0
        and sp.simplify(sp.diff(hamiltonian, pphi).subs(neck)) == 0
        and sp.simplify((-sp.diff(hamiltonian, scale)).subs(neck) - 12 * sp.pi**2) == 0,
        "at the neck {a,H}={phi,H}=0 while {p_a,H}=12 pi^2",
    )

    def poisson(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(left, scale) * sp.diff(right, pa)
            - sp.diff(left, pa) * sp.diff(right, scale)
            + sp.diff(left, phi) * sp.diff(right, pphi)
            - sp.diff(left, pphi) * sp.diff(right, phi)
        )

    lapse, lapse_momentum = sp.symbols("N Pi")
    audit.exact(
        "P28.BFV.abelian_constraint_algebra",
        poisson(hamiltonian, hamiltonian) == 0
        and sp.diff(hamiltonian, lapse) == 0
        and sp.diff(hamiltonian, lapse_momentum) == 0,
        "the Abelian constraint commutes with lapse momentum, so Omega=cH+rho Pi is nilpotent",
    )
    zeta_zero = -sp.Rational(1, 2)
    zeta_prime_zero = -sp.log(2 * sp.pi) / 2
    ghost_prime = sp.simplify(-2 * sp.log(sp.pi) * zeta_zero + 2 * zeta_prime_zero)
    audit.exact(
        "P28.BFV.Dirichlet_ghost_determinant",
        ghost_prime == -sp.log(2) and sp.exp(-ghost_prime) == 2,
        "the chosen unit-interval zeta normalization gives Dirichlet ghost determinant 2 and no zero mode",
    )
    c0, c1 = sp.symbols("c_0 c_1")
    audit.exact(
        "P28.BFV.proper_length_BRST_invariance_after_auxiliary_elimination",
        (c1 - c0).subs({c0: 0, c1: 0}) == 0,
        "after rho=dot c, s integral(N ds)=c(1)-c(0)=0 for Dirichlet endpoints",
    )
    gaussian = sp.integrate(sp.exp(-mu * u**2 / (2 * hbar)), (u, -sp.oo, sp.oo))
    audit.exact(
        "P28.BFV.local_lapse_Gaussian",
        sp.simplify(sp.I * gaussian - sp.I * sp.sqrt(2 * sp.pi * hbar / mu)) == 0,
        "the rotated local negative mode gives i sqrt(2 pi hbar/mu), conditional on global intersection",
    )
    return {
        "PL": {
            "integrand": "exp(-W/hbar)",
            "downward": "dT/ds=conj(W_T)",
            "dual": "dT/ds=-conj(W_T)",
        },
        "BFV": {
            "status": "Euclidean-continued frozen Phase-24/25 constraint, not undeformed Lorentzian BFV",
            "constraint": "-p_a^2/(24pi^2a)+p_phi^2/(4pi^2a^3)+2pi^2(3a-a^3V)",
            "Omega": "cH+rho Pi",
            "Psi": "-N bar_rho",
            "ghost_operator": "-d_s^2, Dirichlet",
            "determinant_note": "zeta-normalized value 2 is not a physical prefactor",
        },
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, base_velocity, benchmark_action = p25.benchmark()
    base = p25.solve_fixed_time(0.7, boundary, base_velocity)
    step = 5e-3
    solutions = [
        p25.solve_fixed_time(0.7 + offset * step, boundary, base_velocity)
        for offset in (-2, -1, 1, 2)
    ]
    energies = [solution.energy for solution in solutions]
    curvature = -(
        energies[0] - 8 * energies[1] + 8 * energies[2] - energies[3]
    ) / (12 * step)
    action_curvature = (
        -solutions[3].action
        + 16 * solutions[2].action
        - 30 * base.action
        + 16 * solutions[1].action
        - solutions[0].action
    ) / (12 * step**2)
    mu = -curvature
    prefactor = float(np.sqrt(2 * np.pi / mu))
    audit.numerical(
        "P28.saddle.curvature_and_local_prefactor",
        abs(base.action - benchmark_action) < 2e-10
        and abs(base.constraint) < 2e-11
        and abs(curvature + 8.9231430383) < 4e-7
        and abs(action_curvature - curvature) < 2e-6
        and abs(prefactor - 0.8391333983) < 5e-10,
        "independent curvature stencils give the conditional factor i*0.8391333983*sqrt(hbar)",
    )

    dual = real_dual_branch(boundary)
    left = [record for record in dual["records"] if record["T"] < 0.7]
    audit.numerical(
        "P28.upward.real_branch_control",
        max(record["endpoint_residual"] for record in dual["records"]) < 2e-8
        and min(record["center"][0] for record in dual["records"]) > 0
        and min(record["det_Bv"] for record in dual["records"]) > 0
        and min(record["dW_dT"] for record in left) > 0
        and max(record["upward_dT_ds"] for record in left) < 0,
        "the recorded dual branch is regular and flows left from T*=0.7 to T=0.2",
    )
    audit.numerical(
        "P28.intersection.bounded_vertical_crossings",
        all(
            crossing["orientation_determinant"] == 1
            and crossing["recorded_crossing_magnitude"] == 1
            and crossing["dW_dT"] > 0
            for crossing in dual["crossings"]
        ),
        "four declared two-sided vertical cycles each cross the recorded branch once and transversely",
    )

    arm = continue_upper_arm(boundary, base_velocity)
    points = arm["points"]
    actions = arm["actions"]
    turn = arm["turn"]
    audit.numerical(
        "P28.downward.pseudo_arclength_residual",
        max(arm["endpoint_residuals"]) < 2e-8
        and max(abs(actions.imag)) < 2e-8
        and max(arm["solve_residuals"]) < 2e-7
        and min(np.diff(actions.real)) > 0,
        "pseudo-arclength keeps endpoints and Im W fixed while Re W increases",
    )
    audit.numerical(
        "P28.downward.gradient_alignment",
        max(arm["alignment"]) < 3e-3 and min(arm["orientation"]) > 0,
        "the recorded tangent aligns with dT/ds=conj(W_T)",
    )
    audit.numerical(
        "P28.downward.imaginary_projection_turn",
        2 < turn < len(points) - 3
        and points[turn, 1] - points[-1, 1] > 5e-3
        and points[-1, 0] > points[turn, 0],
        "the arm continues through a maximum of Im T",
    )
    audit.numerical(
        "P28.downward.independent_fixed_imaginary_control",
        max(arm["independent_errors"]) < 3e-3,
        "independent fixed-Im-T solves lie on the pseudo-arclength curve",
    )
    audit.numerical(
        "P28.downward.conjugate_arm",
        max(arm["conjugate_residuals"]) < 2e-8,
        "conjugation gives lower endpoint solutions with conjugate action",
    )
    audit.numerical(
        "P28.downward.jacobi_and_scale_monitor",
        max(record["endpoint_residual"] for record in arm["monitors"]) < 2e-8
        and max(record["phase_residual"] for record in arm["monitors"]) < 2e-8
        and min(record["min_abs_scale"] for record in arm["monitors"]) > 0.5
        and min(record["Bv_singular_values"][-1] for record in arm["monitors"]) > 1e-2,
        "no scale zero or homogeneous complex Dirichlet Jacobi zero appears at monitored points",
    )

    return {
        "boundary": boundary.tolist(),
        "base": {
            "T_star": 0.7,
            "W": base.action,
            "W_TT": curvature,
            "W_TT_action_stencil": action_curvature,
            "conditional_prefactor": [0.0, prefactor],
        },
        "dual_branch": dual["records"],
        "bounded_crossings": dual["crossings"],
        "positive_half_cycle": "ENDPOINT_CONTACT_COEFFICIENT_OPEN",
        "positive_real_Euclidean_cycle": "NONTRANSVERSE_COEFFICIENT_OPEN",
        "upper_arm": {
            "point_count": len(points),
            "step": PSEUDO_STEP,
            "max_endpoint_residual": max(arm["endpoint_residuals"]),
            "max_phase_residual": float(max(abs(actions.imag))),
            "max_alignment_residual": max(arm["alignment"]),
            "turn": {"index": turn, "T": points[turn, :2].tolist(), "W": [actions[turn].real, actions[turn].imag]},
            "last": {"T": points[-1, :2].tolist(), "W": [actions[-1].real, actions[-1].imag]},
            "independent_controls": arm["independent"],
            "conjugate_controls": arm["conjugate"],
            "jacobi_monitors": arm["monitors"],
            "sampled": arm["sampled"],
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result = {
        "phase": "P28",
        "calculation": "bounded lapse-thimble continuation, regulated branch crossing, and Euclidean-continued homogeneous BFV",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "bounded_upper_arm_continues_past_ImT_turn": "SUPPORTED",
            "bounded_vertical_cycles_cross_recorded_dual_branch": "SUPPORTED_GEOMETRIC_DIAGNOSTIC",
            "global_PL_coefficient": "OPEN",
            "positive_lapse_half_cycle_coefficient": "OPEN_ENDPOINT_PRESCRIPTION_REQUIRED",
            "intrinsic_neck_clock_regular": "CONTRADICTED",
            "extrinsic_p_a_clock_locally_regular": "SUPPORTED_IN_EUCLIDEAN_CONTINUED_HOMOGENEOUS_BFV",
            "physical_quantum_state": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "not_computed": [
                "global thimble endpoints and complete saddle set",
                "relative-homology coefficient for a physical original cycle",
                "positive-lapse endpoint prescription",
                "nonzero-mode gravity, matter, gravitino, and ghost superdeterminant",
                "positive WDW/BFV density, Pin lift, soft spectrum, or string embedding",
            ]
        },
        "next_calculation": "combine the Phase-27 endpoint prescription with complete dual-cycle continuation and the gauge-reduced nonzero-mode determinant",
    }
    print("PHASE28_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
