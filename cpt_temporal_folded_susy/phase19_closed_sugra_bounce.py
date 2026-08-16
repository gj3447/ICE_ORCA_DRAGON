#!/usr/bin/env python3
"""Phase 19 — shift-symmetric SUGRA potentials and closed-FRW bounces.

This executable separates three questions that are easy to conflate:

1. whether the displayed Kähler potentials and superpotentials reproduce the
   quadratic and Starobinsky one-field potentials;
2. whether the time-symmetric k=+1 Friedmann initial data admit 50--60
   accelerated e-fold solutions; and
3. whether the temporal construction predicts the remaining free datum
   phi_0.  The first two questions pass below.  The third remains open: phi_0
   is solved backwards from a requested N_acc and is not selected by CPT/Pin.

Exact identities use SymPy.  Closed-FRW trajectories use SciPy DOP853 with
the Friedmann constraint monitored independently.  The program writes no
files and uses reduced Planck units M_Pl=1.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

    def exact(self, check_id: str, condition: bool, message: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {message}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": message}
        )
        print(f"[PASS] {check_id}: {message}")

    def numerical(self, check_id: str, condition: bool, message: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {message}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": message}
        )
        print(f"[NUMERIC PASS] {check_id}: {message}")


def exact_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(exact_zero(entry) for entry in value)
    return sp.simplify(sp.factor(value)) == 0


def sugra_potential(
    kahler: sp.Expr,
    superpotential: sp.Expr,
    conjugate_superpotential: sp.Expr,
    fields: list[sp.Symbol],
    conjugates: list[sp.Symbol],
) -> tuple[sp.Expr, sp.Matrix, sp.Matrix]:
    """Return the F-term potential, Kähler metric, and its exact inverse."""

    metric = sp.Matrix(
        [[sp.diff(kahler, field, bar) for bar in conjugates] for field in fields]
    )
    inverse = sp.simplify(metric.inv())
    covariant = sp.Matrix(
        [
            sp.diff(superpotential, field)
            + sp.diff(kahler, field) * superpotential
            for field in fields
        ]
    )
    conjugate_covariant = sp.Matrix(
        [
            sp.diff(conjugate_superpotential, bar)
            + sp.diff(kahler, bar) * conjugate_superpotential
            for bar in conjugates
        ]
    )
    # metric rows are holomorphic and columns antiholomorphic, while the
    # ordinary matrix inverse has rows antiholomorphic and columns
    # holomorphic.  Transpose it for K^{i bar(j)} in D_i K^{i bar(j)} D_bar(j).
    potential = sp.exp(kahler) * (
        (covariant.T * inverse.T * conjugate_covariant)[0]
        - 3 * superpotential * conjugate_superpotential
    )
    return sp.simplify(potential), metric, inverse


def exact_sugra_controls(audit: Audit) -> dict[str, object]:
    """Derive both inflationary trajectories without inserting target V."""

    phi, beta = sp.symbols("phi beta", real=True)
    mass, scale, zeta = sp.symbols("m M zeta", positive=True, real=True)
    Phi, Phib, S, Sb = sp.symbols("Phi Phib S Sb")

    # Shift-symmetric stabilizer model.
    kahler_shift = (
        -sp.Rational(1, 2) * (Phi - Phib) ** 2
        + S * Sb
        - zeta * (S * Sb) ** 2
    )
    superpotential_shift = mass * S * Phi
    conjugate_shift = mass * Sb * Phib
    potential_shift, metric_shift, inverse_shift = sugra_potential(
        kahler_shift,
        superpotential_shift,
        conjugate_shift,
        [Phi, S],
        [Phib, Sb],
    )
    shift_path = {
        Phi: phi / sp.sqrt(2),
        Phib: phi / sp.sqrt(2),
        S: 0,
        Sb: 0,
    }
    shift_potential = sp.simplify(potential_shift.subs(shift_path))
    audit.exact(
        "P19.shift.canonical_inflaton_metric",
        exact_zero(metric_shift[0, 0] - 1),
        "K_{Phi Phibar}=1 gives a canonical real inflaton on the trajectory",
    )
    audit.exact(
        "P19.shift.quadratic_potential",
        exact_zero(shift_potential - mass**2 * phi**2 / 2),
        "the source-local F-term potential is V=m^2 phi^2/2",
    )

    beta_substitution = {
        Phi: (phi + sp.I * beta) / sp.sqrt(2),
        Phib: (phi - sp.I * beta) / sp.sqrt(2),
        S: 0,
        Sb: 0,
    }
    beta_mass_squared = sp.simplify(
        sp.diff(potential_shift.subs(beta_substitution), beta, 2).subs(beta, 0)
    )
    potential_hubble_scale_squared = sp.simplify(shift_potential / 3)
    audit.exact(
        "P19.shift.orthogonal_inflaton_mass",
        exact_zero(
            beta_mass_squared - (mass**2 + 6 * potential_hubble_scale_squared)
        ),
        "m_ImPhi^2=m^2+6H_V^2 with H_V^2:=V/3",
    )

    stabilizer_mass_squared = sp.simplify(
        sp.diff(potential_shift, S, Sb).subs(shift_path)
        / metric_shift[1, 1].subs(shift_path)
    )
    audit.exact(
        "P19.shift.stabilizer_mass",
        exact_zero(
            stabilizer_mass_squared
            - (mass**2 + 12 * zeta * potential_hubble_scale_squared)
        ),
        "m_S^2=m^2+12 zeta H_V^2 for either real stabilizer component",
    )
    audit.exact(
        "P19.shift.hubble_heavy_sufficient_benchmark",
        sp.simplify(
            (
                mass**2
                + 12
                * sp.Rational(1, 12)
                * potential_hubble_scale_squared
            )
            - potential_hubble_scale_squared
        ).is_positive
        is True,
        "zeta=1/12 is a sufficient m_S^2>H_V^2 benchmark at finite phi",
    )

    gravitino_mass_squared_shift = sp.simplify(
        (sp.exp(kahler_shift) * superpotential_shift * conjugate_shift).subs(
            shift_path
        )
    )
    auxiliary_s_squared = sp.simplify(
        (
            sp.exp(kahler_shift)
            * inverse_shift[1, 1] ** 2
            * (
                sp.diff(superpotential_shift, S)
                + sp.diff(kahler_shift, S) * superpotential_shift
            )
            * (
                sp.diff(conjugate_shift, Sb)
                + sp.diff(kahler_shift, Sb) * conjugate_shift
            )
        ).subs(shift_path)
    )
    audit.exact(
        "P19.shift.gravitino_mass_on_path",
        exact_zero(gravitino_mass_squared_shift),
        "W=0 implies m_3/2=0 on S=0",
    )
    audit.exact(
        "P19.shift.stabilizer_F_order_parameter",
        exact_zero(auxiliary_s_squared - mass**2 * phi**2 / 2),
        "|F^S|=m|phi|/sqrt(2), up to the auxiliary sign convention",
    )
    audit.exact(
        "P19.shift.susy_minkowski_endpoint",
        exact_zero(shift_potential.subs(phi, 0))
        and exact_zero(auxiliary_s_squared.subs(phi, 0)),
        "the phi=0 endpoint has V=F^S=0",
    )

    # Improved Cecotti/no-scale model.
    T, Tb = sp.symbols("T Tb", positive=True, real=True)
    no_scale_argument = T + Tb - S * Sb + zeta * (S * Sb) ** 2 / 3
    kahler_no_scale = -3 * sp.log(no_scale_argument)
    superpotential_no_scale = 3 * scale * S * (T - 1)
    conjugate_no_scale = 3 * scale * Sb * (Tb - 1)
    potential_no_scale, metric_no_scale, _ = sugra_potential(
        kahler_no_scale,
        superpotential_no_scale,
        conjugate_no_scale,
        [T, S],
        [Tb, Sb],
    )
    t_path = {Tb: T, S: 0, Sb: 0}
    no_scale_t_potential = sp.factor(potential_no_scale.subs(t_path))
    b = sp.sqrt(sp.Rational(2, 3))
    no_scale_phi_potential = sp.simplify(
        no_scale_t_potential.subs(T, sp.exp(b * phi))
    )
    starobinsky_target = (
        sp.Rational(3, 4) * scale**2 * (1 - sp.exp(-b * phi)) ** 2
    )
    audit.exact(
        "P19.noscale.starobinsky_potential",
        exact_zero(no_scale_phi_potential - starobinsky_target),
        "the improved Cecotti trajectory gives the Starobinsky potential",
    )
    canonical_t_coefficient = sp.simplify(
        metric_no_scale[0, 0]
        .subs(t_path)
        .subs(T, sp.exp(b * phi))
        * sp.diff(sp.exp(b * phi), phi) ** 2
    )
    audit.exact(
        "P19.noscale.canonical_log_modulus",
        exact_zero(canonical_t_coefficient - sp.Rational(1, 2)),
        "T=exp(sqrt(2/3) phi) gives the canonical real kinetic coefficient 1/2",
    )

    no_scale_s_mass_squared = sp.factor(
        sp.diff(potential_no_scale, S, Sb).subs(t_path)
        / metric_no_scale[1, 1].subs(t_path)
    )
    no_scale_s_mass_target = scale**2 * (
        4 * T * (T - 1) ** 2 * zeta - 3 * T**2 + 6 * T + 3
    ) / (6 * T**2)
    audit.exact(
        "P19.noscale.stabilizer_hessian_mass",
        exact_zero(no_scale_s_mass_squared - no_scale_s_mass_target),
        "the degenerate real S Hessian reproduces the exact T-dependent mass",
    )

    # For T>=1, a nonnegative S Hessian requires zeta above the maximum
    # of 3(T^2-2T-1)/[4T(T-1)^2] where its numerator is positive.
    t_critical = 2 + sp.sqrt(3)
    zeta_hessian_threshold = sp.simplify(
        3
        * (t_critical**2 - 2 * t_critical - 1)
        / (4 * t_critical * (t_critical - 1) ** 2)
    )
    zeta_hessian_target = (-15 + 9 * sp.sqrt(3)) / 4
    audit.exact(
        "P19.noscale.global_hessian_threshold",
        exact_zero(zeta_hessian_threshold - zeta_hessian_target),
        "the potential-Hessian stability threshold is (-15+9 sqrt(3))/4",
    )
    audit.exact(
        "P19.noscale.one_sixth_is_sufficient",
        sp.simplify(sp.Rational(1, 6) - zeta_hessian_threshold).is_positive
        is True,
        "zeta=1/6 is a conservative sufficient stability benchmark",
    )

    gravitino_mass_squared_no_scale = sp.simplify(
        (
            sp.exp(kahler_no_scale)
            * superpotential_no_scale
            * conjugate_no_scale
        ).subs(t_path)
    )
    d_s_w_squared = sp.simplify(
        (
            sp.exp(kahler_no_scale)
            * (
                sp.diff(superpotential_no_scale, S)
                + sp.diff(kahler_no_scale, S) * superpotential_no_scale
            )
            * (
                sp.diff(conjugate_no_scale, Sb)
                + sp.diff(kahler_no_scale, Sb) * conjugate_no_scale
            )
        ).subs(t_path)
    )
    audit.exact(
        "P19.noscale.gravitino_mass_on_path",
        exact_zero(gravitino_mass_squared_no_scale),
        "W=0 and m_3/2=0 on S=0",
    )
    audit.exact(
        "P19.noscale.nonzero_F_direction",
        exact_zero(
            d_s_w_squared
            - 9 * scale**2 * (T - 1) ** 2 / (8 * T**3)
        ),
        "D_S W is nonzero for T>1 even though W vanishes",
    )

    # Closed k=+1 time-symmetric initial data.
    V0 = sp.symbols("V_0", positive=True, real=True)
    a0 = sp.sqrt(3 / V0)
    audit.exact(
        "P19.bounce.friedmann_constraint_at_turning_point",
        exact_zero(1 / a0**2 - V0 / 3),
        "H_0=phidot_0=0 fixes a_0=sqrt(3/V_0) for k=+1",
    )
    audit.exact(
        "P19.bounce.local_minimum_of_scale_factor",
        sp.simplify(1 / a0**2).is_positive is True,
        "dot H_0=1/a_0^2>0 makes the symmetric turning point a local bounce",
    )

    return {
        "units": "reduced Planck units M_Pl=1",
        "shift_symmetric": {
            "K": "-(Phi-Phibar)^2/2 + S*Sbar - zeta*(S*Sbar)^2",
            "W": "m*S*Phi",
            "trajectory": "S=0, Im(Phi)=0, phi=sqrt(2) Re(Phi)",
            "V": "m^2 phi^2/2",
            "mass_scale_definition": "H_V^2:=V/3, distinct from the closed-FRW H(t)^2",
            "m_ImPhi_squared": "m^2+6H_V^2",
            "m_S_squared": "m^2+12 zeta H_V^2",
            "Hubble_heavy_sufficient_benchmark": "zeta>=1/12",
            "F_S_magnitude": "m |phi|/sqrt(2)",
            "m_3_over_2": "0 on S=0",
        },
        "improved_cecotti_no_scale": {
            "K": "-3 log[T+Tbar-S*Sbar+(zeta/3)(S*Sbar)^2]",
            "W": "3 M S (T-1)",
            "trajectory": "S=0, T=exp(sqrt(2/3) phi) real",
            "V": "3 M^2 [1-exp(-sqrt(2/3) phi)]^2/4",
            "full_T_ge_1_stability_threshold_exact": str(
                zeta_hessian_target
            ),
            "full_T_ge_1_stability_threshold_decimal": str(
                sp.N(zeta_hessian_target, 12)
            ),
            "conservative_stability_benchmark": "zeta>1/6",
            "source_caveat": (
                "Kallosh-Linde arXiv:1306.3214 reports zeta>0.15 for "
                "stability and zeta about 0.5 for m_S^2 at least H_V^2; "
            "1/6 is sufficient for stability, not a universal heavy-field threshold"
            ),
        },
    }


@dataclass(frozen=True)
class InflationModel:
    model_id: str
    potential: Callable[[float], float]
    derivative: Callable[[float], float]
    root_brackets: dict[int, tuple[float, float]]
    expected_phi0: dict[int, float]
    expected_scaled_a0: dict[int, float]


def integrate_closed_bounce(
    model: InflationModel,
    phi0: float,
) -> dict[str, float]:
    """Integrate from the symmetric bounce to the end of acceleration."""

    potential0 = model.potential(phi0)
    a0 = float(np.sqrt(3.0 / potential0))

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        a, hubble, inflaton, velocity, e_folds = state
        return np.asarray(
            [
                a * hubble,
                -0.5 * velocity**2 + 1.0 / a**2,
                velocity,
                -3.0 * hubble * velocity - model.derivative(inflaton),
                hubble,
            ],
            dtype=float,
        )

    def end_of_acceleration(_time: float, state: np.ndarray) -> float:
        return (model.potential(state[2]) - state[3] ** 2) / 3.0

    end_of_acceleration.direction = -1
    end_of_acceleration.terminal = True

    def maximum_hubble(_time: float, state: np.ndarray) -> float:
        return -0.5 * state[3] ** 2 + 1.0 / state[0] ** 2

    maximum_hubble.direction = -1
    maximum_hubble.terminal = False

    solution = solve_ivp(
        rhs,
        (0.0, 1000.0),
        np.asarray([a0, 0.0, phi0, 0.0, 0.0]),
        method="DOP853",
        rtol=2e-13,
        atol=2e-15,
        max_step=0.02,
        events=(end_of_acceleration, maximum_hubble),
        dense_output=True,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise AssertionError(
            f"closed-FRW integration failed for {model.model_id}: {solution.message}"
        )

    a_values, h_values, phi_values, velocity_values, n_values = solution.y
    density_over_three = (
        0.5 * velocity_values**2
        + np.asarray([model.potential(value) for value in phi_values])
    ) / 3.0
    constraint_residual = (
        h_values**2 + 1.0 / a_values**2 - density_over_three
    )
    relative_constraint = float(
        np.max(np.abs(constraint_residual) / density_over_three)
    )
    h_event_times = solution.t_events[1]
    if len(h_event_times) != 1:
        raise AssertionError(
            f"expected one H maximum for {model.model_id}, got {len(h_event_times)}"
        )
    h_maximum = float(solution.sol(h_event_times[0])[1])

    return {
        "phi0": float(phi0),
        "scaled_a0": a0,
        "N_acc": float(n_values[-1]),
        "scaled_H_max": h_maximum,
        "constraint_max_relative_error": relative_constraint,
        "end_time_scaled": float(solution.t[-1]),
    }


def solve_bounce_table(audit: Audit) -> dict[str, object]:
    sqrt_two_thirds = float(np.sqrt(2.0 / 3.0))
    quadratic = InflationModel(
        model_id="quadratic_shift_symmetric",
        potential=lambda value: 0.5 * value**2,
        derivative=lambda value: value,
        root_brackets={50: (13.5, 14.6), 55: (14.2, 15.3), 60: (14.8, 16.2)},
        expected_phi0={50: 14.21160, 55: 14.89638, 60: 15.55123},
        expected_scaled_a0={50: 0.172358, 55: 0.164435, 60: 0.157511},
    )
    starobinsky = InflationModel(
        model_id="improved_cecotti_starobinsky",
        potential=lambda value: 0.75
        * (1.0 - np.exp(-sqrt_two_thirds * value)) ** 2,
        derivative=lambda value: 1.5
        * sqrt_two_thirds
        * np.exp(-sqrt_two_thirds * value)
        * (1.0 - np.exp(-sqrt_two_thirds * value)),
        root_brackets={50: (5.0, 5.4), 55: (5.1, 5.6), 60: (5.2, 5.7)},
        expected_phi0={50: 5.23270, 55: 5.34237, 60: 5.44297},
        expected_scaled_a0={50: 2.02829, 55: 2.02583, 60: 2.02377},
    )

    tables: dict[str, list[dict[str, object]]] = {}
    for model in (quadratic, starobinsky):
        rows: list[dict[str, object]] = []
        for target in (50, 55, 60):
            lower, upper = model.root_brackets[target]

            def residual(initial_phi: float) -> float:
                return integrate_closed_bounce(model, initial_phi)["N_acc"] - target

            phi0 = brentq(residual, lower, upper, xtol=2e-10, rtol=2e-12)
            observed = integrate_closed_bounce(model, phi0)
            audit.numerical(
                f"P19.{model.model_id}.Nacc_{target}",
                abs(observed["N_acc"] - target) < 2e-7,
                f"a time-symmetric closed solution reaches N_acc={target}",
            )
            audit.numerical(
                f"P19.{model.model_id}.table_phi0_{target}",
                abs(phi0 - model.expected_phi0[target]) < 6e-5,
                "the independently solved phi_0 reproduces the supplied table",
            )
            audit.numerical(
                f"P19.{model.model_id}.table_a0_{target}",
                abs(observed["scaled_a0"] - model.expected_scaled_a0[target])
                < 7e-6,
                "the dimensionless curvature radius reproduces the supplied table",
            )
            audit.numerical(
                f"P19.{model.model_id}.friedmann_constraint_{target}",
                observed["constraint_max_relative_error"] < 1e-12,
                "the redundant Friedmann constraint stays below 1e-12 relative error",
            )
            rows.append(
                {
                    "target_accelerated_e_folds": target,
                    "phi0_solved_from_target": f"{phi0:.8f}",
                    "mass_scale_times_a0": f"{observed['scaled_a0']:.8f}",
                    "N_acc_observed": f"{observed['N_acc']:.9f}",
                    "H_max_over_mass_scale": f"{observed['scaled_H_max']:.9f}",
                    "constraint_max_relative_error": (
                        f"{observed['constraint_max_relative_error']:.3e}"
                    ),
                }
            )
        tables[model.model_id] = rows

    quadratic_60 = tables[quadratic.model_id][-1]
    starobinsky_60 = tables[starobinsky.model_id][-1]
    m_benchmark = 6e-6
    M_benchmark = 1.3e-5
    benchmarks = {
        "quadratic_60": {
            "input_mass_m_over_MPl": f"{m_benchmark:.1e}",
            "a0_in_MPl_inverse": f"{float(quadratic_60['mass_scale_times_a0']) / m_benchmark:.6e}",
            "H_max_over_MPl": f"{float(quadratic_60['H_max_over_mass_scale']) * m_benchmark:.6e}",
        },
        "starobinsky_60": {
            "input_mass_M_over_MPl": f"{M_benchmark:.1e}",
            "a0_in_MPl_inverse": f"{float(starobinsky_60['mass_scale_times_a0']) / M_benchmark:.6e}",
            "H_max_over_MPl": f"{float(starobinsky_60['H_max_over_mass_scale']) * M_benchmark:.6e}",
        },
    }
    return {"tables": tables, "conditional_scale_benchmarks": benchmarks}


def slow_roll_predictions(audit: Audit) -> dict[str, object]:
    """Compute model predictions; these do not use the bounce N_acc as N_*."""

    rows: dict[str, list[dict[str, str]]] = {"quadratic": [], "starobinsky": []}
    b = np.sqrt(2.0 / 3.0)

    phi_end_star = np.log(1.0 + 2.0 / np.sqrt(3.0)) / b

    def star_N(phi_value: float) -> float:
        return (
            (np.exp(b * phi_value) - np.exp(b * phi_end_star)) / (2.0 * b**2)
            - (phi_value - phi_end_star) / (2.0 * b)
        )

    for horizon_e_folds in (50, 55, 60):
        phi_quadratic = np.sqrt(4.0 * horizon_e_folds + 2.0)
        epsilon_quadratic = 2.0 / phi_quadratic**2
        eta_quadratic = epsilon_quadratic
        ns_quadratic = 1.0 - 6.0 * epsilon_quadratic + 2.0 * eta_quadratic
        r_quadratic = 16.0 * epsilon_quadratic
        audit.numerical(
            f"P19.slowroll.quadratic_r_exceeds_current_N{horizon_e_folds}",
            r_quadratic > 0.036 and r_quadratic > 0.034,
            "quadratic slow-roll r exceeds both BK18 0.036 and the 2026 combined 0.034 limit",
        )
        rows["quadratic"].append(
            {
                "N_star": str(horizon_e_folds),
                "n_s_first_order": f"{ns_quadratic:.7f}",
                "r_first_order": f"{r_quadratic:.7f}",
            }
        )

        phi_star = brentq(
            lambda value: star_N(value) - horizon_e_folds,
            phi_end_star,
            8.0,
        )
        exponential = np.exp(-b * phi_star)
        epsilon_star = (4.0 / 3.0) * exponential**2 / (1.0 - exponential) ** 2
        eta_star = (
            -(4.0 / 3.0)
            * exponential
            * (1.0 - 2.0 * exponential)
            / (1.0 - exponential) ** 2
        )
        ns_star = 1.0 - 6.0 * epsilon_star + 2.0 * eta_star
        r_star = 16.0 * epsilon_star
        audit.numerical(
            f"P19.slowroll.starobinsky_r_below_current_N{horizon_e_folds}",
            r_star < 0.034,
            "Starobinsky slow-roll r lies below the 2026 combined limit",
        )
        rows["starobinsky"].append(
            {
                "N_star": str(horizon_e_folds),
                "phi_star": f"{phi_star:.7f}",
                "n_s_first_order": f"{ns_star:.7f}",
                "r_first_order": f"{r_star:.7f}",
            }
        )
    return {
        "important_distinction": (
            "N_star is the pivot-to-end slow-roll count; it is not automatically "
            "identical to the bounce-to-end N_acc used in the existence table"
        ),
        "published_comparison": (
            "BICEP/Keck XIII (BK18), arXiv:2110.00483, reports "
            "r_0.05<0.036 at 95% confidence; the 2026 combined analysis "
            "arXiv:2512.10613v2 reports r<0.034"
        ),
        "tables": rows,
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact_models = exact_sugra_controls(audit)
    bounce_results = solve_bounce_table(audit)
    observables = slow_roll_predictions(audit)

    result: dict[str, object] = {
        "phase": "P19",
        "calculation": "shift-symmetric/no-scale SUGRA plus closed-FRW bounce control",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "models": exact_models,
        "closed_bounce": {
            "equations": {
                "constraint": "H^2+1/a^2=(phidot^2/2+V)/3",
                "Raychaudhuri": "dot(H)=-phidot^2/2+1/a^2",
                "Klein_Gordon": "ddot(phi)+3H phidot+V_phi=0",
            },
            "CPT_compatible_bosonic_initial_data": (
                "a and phi even; H and phidot odd; H0=phidot0=0"
            ),
            "results": bounce_results,
        },
        "slow_roll_observables": observables,
        "claim_status": {
            "shift_symmetric_quadratic_potential_exists": "SUPPORTED_EXACT",
            "improved_Cecotti_Starobinsky_potential_exists": "SUPPORTED_EXACT",
            "closed_time_symmetric_50_to_60_efold_solutions_exist": (
                "SUPPORTED_NUMERICALLY_FOR_THE_DISPLAYED_MODELS"
            ),
            "quadratic_model_is_compatible_with_BK18_r_limit": "CONTRADICTED",
            "Starobinsky_model_has_viable_tree_level_ns_r": (
                "SUPPORTED_AT_FIRST_ORDER_SLOW_ROLL"
            ),
            "CPT_or_Pin_selects_phi0": "OPEN_NOT_DERIVED",
            "full_CPT_Pin_SUGRA_state_or_seam": "OPEN_NOT_CONSTRUCTED",
        },
        "scope_guard": {
            "what_is_proved": [
                "two exact one-field F-term trajectories",
                "classical homogeneous k=+1 time-symmetric bounce solutions",
                "conditional radii and Hubble scales after choosing a mass scale and target N_acc",
                "first-order single-field slow-roll observables",
            ],
            "what_is_not_proved": [
                "a CPT/Pin rule selecting phi0",
                "a full fermionic/off-shell seam or quantum cosmological state",
                "perturbation evolution through the bounce",
                "reheating or a mapping from N_acc to the observed pivot N_star",
                "a parameter-free prediction of universe size",
                "a present-day SUSY spectrum or temporal-seam Goldstino",
            ],
            "central_interpretation": (
                "the calculation establishes conditional existence, not initial-data selection"
            ),
        },
    }
    print("PHASE19_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
