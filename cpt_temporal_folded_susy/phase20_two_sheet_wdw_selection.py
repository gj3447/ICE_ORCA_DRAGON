#!/usr/bin/env python3
"""Phase 20 — bounded WDW initial-amplitude selection controls.

This executable tests a deliberately limited question: does the leading
constant-field de Sitter/WDW envelope single out the closed-Starobinsky
initial value phi/M_Pl=5.442969458?  It keeps the standard one-history WDW
weight separate from an additional independent-two-sheet tensor-product
assumption.  Neither envelope has a finite stationary point there.

The calculation is not an exact solution of the scalar-gravity WDW equation.
At the benchmark V' is small but nonzero, the turning point is outside the
ordinary WKB domain, and no CPT/Pin Hilbert-space sewing or local-SUGRA
wavefunction has been constructed.  A separate unit-explicit control derives
the conditional curvature/reheating conversion quoted for the classical
Phase 19 solution.  The program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import mpmath as mp
import numpy as np
import sympy as sp
from scipy import constants
from scipy.integrate import solve_ivp


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
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")

    def _check_unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")


def exact_zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.factor(expression)) == 0


def exact_wdw_controls(audit: Audit) -> dict[str, object]:
    varphi = sp.symbols("varphi", positive=True, finite=True, real=True)
    lam = sp.symbols("lambda", positive=True, finite=True, real=True)
    sheet_sign = sp.symbols("s", real=True)
    phase = sp.symbols("S_phase", real=True)
    normalization = sp.symbols("N", positive=True, real=True)
    b = sp.sqrt(sp.Rational(2, 3))
    exponential = sp.exp(-b * varphi)
    potential = sp.Rational(3, 4) * lam**2 * (1 - exponential) ** 2
    hemisphere_exponent = 16 * sp.pi**2 / (
        lam**2 * (1 - exponential) ** 2
    )

    audit.exact(
        "P20.WDW.hemisphere_action_normalization",
        exact_zero(hemisphere_exponent - 12 * sp.pi**2 / potential),
        "I=12 pi^2 M_Pl^4/V=16 pi^2/[lambda^2(1-exp(-b varphi))^2]",
    )

    derivative = sp.factor(sp.diff(hemisphere_exponent, varphi))
    derivative_target = -32 * sp.pi**2 * b * exponential / (
        lam**2 * (1 - exponential) ** 3
    )
    audit.exact(
        "P20.WDW.action_derivative",
        exact_zero(derivative - derivative_target),
        "the leading de Sitter exponent has the claimed exact derivative",
    )

    standard_log_slope = sp.diff(2 * sheet_sign * hemisphere_exponent, varphi)
    pair_log_slope = sp.diff(4 * sheet_sign * hemisphere_exponent, varphi)
    audit.exact(
        "P20.WDW.standard_history_weight_slope",
        exact_zero(standard_log_slope - 2 * sheet_sign * derivative_target),
        "the standard one-history WDW envelope exp(2 s I) has slope 2 s I'",
    )
    audit.exact(
        "P20.WDW.independent_pair_weight_slope",
        exact_zero(pair_log_slope - 4 * sheet_sign * derivative_target),
        "the additional independent-pair Born weight exp(4 s I) has slope 4 s I'",
    )
    audit.exact(
        "P20.WDW.pair_slope_factor_two",
        exact_zero(pair_log_slope - 2 * standard_log_slope),
        "the independent-pair convention doubles, but does not cancel, the standard slope",
    )
    audit.exact(
        "P20.WDW.no_finite_stationary_envelope",
        sp.solveset(
            derivative_target,
            varphi,
            domain=sp.Interval.open(0, sp.oo),
        )
        == sp.EmptySet,
        "I' has no zero at finite varphi>0, so neither sign has a finite envelope extremum",
    )
    audit.exact(
        "P20.WDW.asymptotic_zero_slope_only",
        sp.limit(derivative_target, varphi, sp.oo) == 0,
        "the envelope slope approaches zero only on the infinite-field plateau",
    )

    real_wavefunction = (
        normalization
        * sp.exp(sheet_sign * hemisphere_exponent)
        * (sp.exp(sp.I * phase) + sp.exp(-sp.I * phase))
    )
    real_probability = sp.expand_complex(real_wavefunction * sp.conjugate(real_wavefunction))
    audit.exact(
        "P20.WDW.conjugate_saddle_interference",
        exact_zero(
            real_probability
            - 4
            * normalization**2
            * sp.exp(2 * sheet_sign * hemisphere_exponent)
            * sp.cos(phase) ** 2
        ),
        "a coherent conjugate-saddle sum gives an order-one cos^2 phase modulation",
    )

    single_sheet_history_probability = sp.exp(
        2 * sheet_sign * hemisphere_exponent
    )
    independent_joint_probability = single_sheet_history_probability**2
    audit.exact(
        "P20.WDW.independent_pair_joint_probability",
        exact_zero(
            independent_joint_probability
            - sp.exp(4 * sheet_sign * hemisphere_exponent)
        ),
        "exp(4 s I) is the conditional tensor-product joint-probability convention",
    )

    constant_factor = sp.symbols("C", positive=True, real=True)
    audit.exact(
        "P20.WDW.constant_symmetrization_does_not_move_slope",
        exact_zero(
            sp.diff(sp.log(constant_factor) + 2 * sheet_sign * hemisphere_exponent, varphi)
            - standard_log_slope
        ),
        "a varphi-independent normalization factor cannot select a new peak",
    )

    epsilon_v = sp.factor(
        sp.Rational(1, 2) * (sp.diff(potential, varphi) / potential) ** 2
    )
    epsilon_target = sp.Rational(4, 3) * exponential**2 / (1 - exponential) ** 2
    audit.exact(
        "P20.WDW.starobinsky_epsilon",
        exact_zero(epsilon_v - epsilon_target),
        "epsilon_V=4 exp(-2b varphi)/[3(1-exp(-b varphi))^2]",
    )
    audit.exact(
        "P20.WDW.constant_field_is_not_exact_saddle",
        sp.solveset(
            sp.diff(potential, varphi),
            varphi,
            domain=sp.Interval.open(0, sp.oo),
        )
        == sp.EmptySet,
        "V' is nonzero at every finite varphi>0, so the constant-field hemisphere is an approximation",
    )

    # Cecotti stabilizer trajectory: derive D_S W, K^{S Sbar}, F^S, and V.
    T, Tb = sp.symbols("T Tb", positive=True, real=True)
    S, Sb = sp.symbols("S Sb")
    zeta, mass = sp.symbols("zeta M", positive=True, real=True)
    kahler_argument = T + Tb - S * Sb + zeta * (S * Sb) ** 2 / 3
    kahler = -3 * sp.log(kahler_argument)
    superpotential = 3 * mass * S * (T - 1)
    d_s_w = sp.diff(superpotential, S) + sp.diff(kahler, S) * superpotential
    metric_ss = sp.diff(kahler, S, Sb)
    path = {Tb: T, S: 0, Sb: 0}
    d_s_w_path = sp.simplify(d_s_w.subs(path))
    inverse_ss_path = sp.simplify(1 / metric_ss.subs(path))
    auxiliary_s = sp.simplify(
        -sp.exp(kahler.subs(path) / 2)
        * inverse_ss_path
        * d_s_w_path
    )
    cecotti_potential = sp.simplify(
        sp.exp(kahler.subs(path)) * inverse_ss_path * d_s_w_path**2
    )
    audit.exact(
        "P20.SUSY.cecotti_DSW",
        exact_zero(d_s_w_path - 3 * mass * (T - 1)),
        "D_S W=3M(T-1) on S=0 and real T",
    )
    audit.exact(
        "P20.SUSY.cecotti_inverse_metric",
        exact_zero(inverse_ss_path - 2 * T / 3),
        "K^{S Sbar}=2T/3 on the inflationary trajectory",
    )
    audit.exact(
        "P20.SUSY.cecotti_auxiliary",
        exact_zero(auxiliary_s + mass * (T - 1) / sp.sqrt(2 * T)),
        "F^S=-M(T-1)/sqrt(2T), up to the overall auxiliary convention",
    )
    audit.exact(
        "P20.SUSY.cecotti_potential",
        exact_zero(
            cecotti_potential
            - 3 * mass**2 * (T - 1) ** 2 / (4 * T**2)
        ),
        "the stabilizer F-term reproduces the Starobinsky trajectory potential",
    )
    audit.exact(
        "P20.SUSY.static_F_flat_point",
        sp.solve(auxiliary_s, T) == [1],
        "the positive-real static F-flat point on this trajectory is T=1, not the inflationary benchmark",
    )

    reheating_w = sp.symbols("w_reh", real=True)
    temperature_exponent = -2 + 8 / (3 * (1 + reheating_w))
    audit.exact(
        "P20.curvature.matterlike_temperature_exponent",
        exact_zero(temperature_exponent.subs(reheating_w, 0) - sp.Rational(2, 3)),
        "matterlike reheating gives |Omega_K0| proportional to T_reh^(2/3)",
    )

    return {
        "b": "sqrt(2/3)",
        "potential_over_MPl4": "3 lambda^2 (1-exp(-b varphi))^2/4",
        "positive_hemisphere_exponent": "I=12 pi^2 M_Pl^4/V",
        "standard_history_weight": "P proportional to exp(2 s I)",
        "conditional_independent_pair_weight": "P_pair proportional to exp(4 s I)",
        "sign_convention": "s=+1 Hartle-Hawking; s=-1 tunneling",
        "general_reheating_temperature_exponent": str(temperature_exponent),
        "scope_warning": (
            "I is the constant-field de Sitter hemisphere expression. At finite "
            "Starobinsky varphi it is a leading slow-roll control, not an exact "
            "complex scalar-gravity saddle or solved WDW wavefunction."
        ),
    }


def benchmark_wdw_controls(audit: Audit) -> dict[str, object]:
    mp.mp.dps = 80
    varphi_star = mp.mpf("5.442969458")
    lam = mp.mpf("1.3e-5")
    b = mp.sqrt(mp.mpf(2) / 3)
    h = mp.mpf("1e-7")

    def i_without_lambda(value: mp.mpf) -> mp.mpf:
        return 16 * mp.pi**2 / (1 - mp.e ** (-b * value)) ** 2

    i_prime_coefficient = -32 * mp.pi**2 * b * mp.e ** (-b * varphi_star) / (
        1 - mp.e ** (-b * varphi_star)
    ) ** 3
    standard_coefficient = -2 * i_prime_coefficient
    pair_coefficient = -4 * i_prime_coefficient
    standard_slope_hh = 2 * i_prime_coefficient / lam**2
    pair_slope_hh = 4 * i_prime_coefficient / lam**2
    standard_central = (
        2 * i_without_lambda(varphi_star + h)
        - 2 * i_without_lambda(varphi_star - h)
    ) / (2 * h)
    pair_central = (
        4 * i_without_lambda(varphi_star + h)
        - 4 * i_without_lambda(varphi_star - h)
    ) / (2 * h)

    t_star = mp.e ** (b * varphi_star)
    f_over_mass = -(t_star - 1) / mp.sqrt(2 * t_star)
    vprime_over_v = 2 * b * mp.e ** (-b * varphi_star) / (
        1 - mp.e ** (-b * varphi_star)
    )
    epsilon_v = vprime_over_v**2 / 2

    audit.numerical(
        "P20.numeric.standard_slope_coefficient",
        abs(standard_coefficient - mp.mpf("6.277009460746")) < mp.mpf("5e-13"),
        "the standard WDW log-slope coefficient is 6.277009460746/lambda^2",
    )
    audit.numerical(
        "P20.numeric.pair_slope_coefficient",
        abs(pair_coefficient - mp.mpf("12.554018921492")) < mp.mpf("5e-13"),
        "the conditional independent-pair coefficient is 12.554018921492/lambda^2",
    )
    audit.numerical(
        "P20.numeric.standard_central_difference",
        abs(standard_central - 2 * i_prime_coefficient) < mp.mpf("1e-11"),
        "an h=1e-7 central difference independently reproduces the standard slope",
    )
    audit.numerical(
        "P20.numeric.pair_central_difference",
        abs(pair_central - 4 * i_prime_coefficient) < mp.mpf("2e-11"),
        "an h=1e-7 central difference independently reproduces the pair slope",
    )
    audit.numerical(
        "P20.numeric.HH_and_tunneling_opposite_monotonicity",
        standard_slope_hh < 0 and -standard_slope_hh > 0,
        "the HH envelope decreases and the tunneling envelope increases at the benchmark",
    )
    audit.numerical(
        "P20.numeric.T_star",
        abs(t_star - mp.mpf("85.1288467223")) < mp.mpf("5e-11"),
        "T=exp(sqrt(2/3) varphi) gives T_star=85.1288467223",
    )
    audit.numerical(
        "P20.numeric.nonzero_F_star",
        abs(f_over_mass + mp.mpf("6.447503145")) < mp.mpf("5e-10"),
        "F^S/M=-6.447503145 at varphi_star, so the background is not F-flat",
    )
    audit.numerical(
        "P20.numeric.slow_roll_not_constant_field",
        abs(epsilon_v - mp.mpf("1.8838610e-4")) < mp.mpf("5e-11"),
        "epsilon_V is small but nonzero at the benchmark",
    )

    return {
        "varphi_star": mp.nstr(varphi_star, 12),
        "lambda_benchmark": mp.nstr(lam, 8),
        "T_star": mp.nstr(t_star, 15),
        "F_S_over_M": mp.nstr(f_over_mass, 15),
        "Vprime_over_V": mp.nstr(vprime_over_v, 15),
        "epsilon_V": mp.nstr(epsilon_v, 15),
        "standard_log_slope": {
            "formula_at_star": "-s 6.277009460746/lambda^2",
            "HH_at_lambda_benchmark": mp.nstr(standard_slope_hh, 12),
            "tunneling_at_lambda_benchmark": mp.nstr(-standard_slope_hh, 12),
        },
        "conditional_independent_pair_log_slope": {
            "formula_at_star": "-s 12.554018921492/lambda^2",
            "HH_at_lambda_benchmark": mp.nstr(pair_slope_hh, 12),
            "tunneling_at_lambda_benchmark": mp.nstr(-pair_slope_hh, 12),
        },
        "finite_difference_step": "1e-7",
    }


def integrate_phase19_starobinsky_endpoint(audit: Audit) -> dict[str, float]:
    """Recompute the conditional N=60 endpoint used by the curvature map."""

    b = float(np.sqrt(2.0 / 3.0))
    phi0 = 5.442969458

    def potential(phi: float) -> float:
        return 0.75 * (1.0 - np.exp(-b * phi)) ** 2

    def derivative(phi: float) -> float:
        return 1.5 * b * np.exp(-b * phi) * (1.0 - np.exp(-b * phi))

    a0 = float(np.sqrt(3.0 / potential(phi0)))

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        a, hubble, phi, velocity, e_folds = state
        return np.asarray(
            [
                a * hubble,
                -0.5 * velocity**2 + 1.0 / a**2,
                velocity,
                -3.0 * hubble * velocity - derivative(phi),
                hubble,
            ]
        )

    def end_acceleration(_time: float, state: np.ndarray) -> float:
        return (potential(state[2]) - state[3] ** 2) / 3.0

    end_acceleration.direction = -1
    end_acceleration.terminal = True
    solution = solve_ivp(
        rhs,
        (0.0, 1000.0),
        np.asarray([a0, 0.0, phi0, 0.0, 0.0]),
        method="DOP853",
        rtol=3e-12,
        atol=3e-14,
        max_step=0.02,
        events=end_acceleration,
    )
    if not solution.success or len(solution.t_events[0]) != 1:
        raise AssertionError("conditional Starobinsky endpoint integration failed")

    a_end, hubble_end, phi_end, velocity_end, n_acc = solution.y_events[0][0]
    rho_end_scaled = 0.5 * velocity_end**2 + potential(phi_end)
    constraint_relative = abs(
        hubble_end**2 + 1.0 / a_end**2 - rho_end_scaled / 3.0
    ) / (rho_end_scaled / 3.0)
    audit.numerical(
        "P20.numeric.phase19_Nacc_bridge",
        abs(n_acc - 60.0) < 2e-8,
        "the Phase 19 benchmark independently reaches 60 accelerated e-folds",
    )
    audit.numerical(
        "P20.numeric.phase19_rho_end_bridge",
        abs(rho_end_scaled - 0.1751668051) < 2e-10,
        "rho_end/(M_s^2 M_Pl^2)=0.1751668051 at the acceleration endpoint",
    )
    audit.numerical(
        "P20.numeric.phase19_constraint_bridge",
        constraint_relative < 2e-12,
        "the endpoint Friedmann constraint remains below 2e-12 relative error",
    )
    return {
        "mass_scale_times_a_bounce": a0,
        "N_acc": float(n_acc),
        "mass_scale_times_a_end": float(a_end),
        "phi_end": float(phi_end),
        "rho_end_over_Ms2_MPl2": float(rho_end_scaled),
        "constraint_relative_error": float(constraint_relative),
    }


def curvature_reheating_control(
    audit: Audit, endpoint: dict[str, float]
) -> dict[str, object]:
    """Evaluate one unit-explicit, assumption-heavy Omega_K conversion."""

    reduced_planck_mass_GeV = 2.435e18
    lambda_mass = 1.22e-5
    reheating_temperature_GeV = 1.0e9
    reheating_w = 0.0
    energy_dof_reheating = 106.75
    entropy_dof_reheating = 106.75
    entropy_dof_today = 3.909
    cmb_temperature_K = 2.7255
    hubble_today_km_s_Mpc = 67.4

    boltzmann_GeV_per_K = constants.Boltzmann / constants.electron_volt / 1e9
    hbar_GeV_s = constants.hbar / constants.electron_volt / 1e9
    megaparsec_m = constants.parsec * 1e6
    cmb_temperature_GeV = cmb_temperature_K * boltzmann_GeV_per_K
    hubble_today_s_inverse = (
        hubble_today_km_s_Mpc * 1000.0 / megaparsec_m
    )
    hubble_today_GeV = hubble_today_s_inverse * hbar_GeV_s

    mass_scale_GeV = lambda_mass * reduced_planck_mass_GeV
    a_bounce_GeV_inverse = (
        endpoint["mass_scale_times_a_bounce"] / mass_scale_GeV
    )
    rho_end_GeV4 = (
        endpoint["rho_end_over_Ms2_MPl2"]
        * mass_scale_GeV**2
        * reduced_planck_mass_GeV**2
    )
    rho_reheating_GeV4 = (
        np.pi**2
        * energy_dof_reheating
        * reheating_temperature_GeV**4
        / 30.0
    )
    reheating_expansion = (rho_end_GeV4 / rho_reheating_GeV4) ** (
        1.0 / (3.0 * (1.0 + reheating_w))
    )
    entropy_expansion = (
        reheating_temperature_GeV / cmb_temperature_GeV
    ) * (entropy_dof_reheating / entropy_dof_today) ** (1.0 / 3.0)
    a_end_GeV_inverse = (
        endpoint["mass_scale_times_a_end"] / mass_scale_GeV
    )
    a_today_GeV_inverse = (
        a_end_GeV_inverse
        * reheating_expansion
        * entropy_expansion
    )
    omega_k_abs = 1.0 / (a_today_GeV_inverse * hubble_today_GeV) ** 2
    target_abs_omega = 1.0e-3
    temperature_for_target_GeV = reheating_temperature_GeV * (
        target_abs_omega / omega_k_abs
    ) ** 1.5

    audit.numerical(
        "P20.numeric.curvature_reheating_coefficient",
        abs(omega_k_abs - 5.525801545e-4) < 2e-13,
        "the explicit 2.435e18 GeV convention gives |Omega_K0|=5.525802e-4 at T_reh=1e9 GeV",
    )
    audit.numerical(
        "P20.numeric.curvature_reheating_inverse",
        abs(temperature_for_target_GeV - 2.4344848e9) < 2e4,
        "|Omega_K0|=1e-3 corresponds conditionally to T_reh=2.434485e9 GeV",
    )
    audit.numerical(
        "P20.numeric.closed_curvature_sign",
        -omega_k_abs < 0,
        "k=+1 implies signed Omega_K0=-|Omega_K0|",
    )

    return {
        "measurement_model": (
            "a_today=a_b exp(N) (rho_end/rho_reh)^[1/(3(1+w))] "
            "(T_reh/T0) (g_s,reheat/g_s,0)^(1/3); "
            "Omega_K0=-1/(a_today H0)^2 for k=+1"
        ),
        "inputs": {
            "reduced_planck_mass_GeV": reduced_planck_mass_GeV,
            "M_s_over_M_Pl": lambda_mass,
            "N_acc": endpoint["N_acc"],
            "w_reh": reheating_w,
            "T_reh_GeV": reheating_temperature_GeV,
            "g_energy_reh": energy_dof_reheating,
            "g_entropy_reh": entropy_dof_reheating,
            "g_entropy_today": entropy_dof_today,
            "T0_K": cmb_temperature_K,
            "H0_km_s_Mpc": hubble_today_km_s_Mpc,
        },
        "unit_conversions": {
            "T0_GeV": f"{cmb_temperature_GeV:.12e}",
            "H0_GeV": f"{hubble_today_GeV:.12e}",
            "a_bounce_GeV_inverse": f"{a_bounce_GeV_inverse:.12e}",
            "rho_end_GeV4": f"{rho_end_GeV4:.12e}",
        },
        "conditional_relation": (
            "Omega_K0=-5.525802e-4 (T_reh/1e9 GeV)^(2/3)"
        ),
        "T_reh_for_abs_OmegaK0_1e_minus_3_GeV": (
            f"{temperature_for_target_GeV:.7e}"
        ),
        "sensitivities": {
            "d_ln_abs_OmegaK0_d_N": "-2",
            "mass_scale_power": "abs(Omega_K0) proportional to M_s^(2/3)",
            "H0_power": "abs(Omega_K0) proportional to H0^(-2)",
            "general_T_reh_power": "-2+8/[3(1+w_reh)]",
        },
        "scope_warning": (
            "This is a conditional conversion, not a prediction or curvature "
            "detection. It assumes the Phase 19 phi0/N endpoint, constant "
            "matterlike reheating, instantaneous thermalization at T_reh, entropy "
            "conservation, Standard-Model relativistic degrees of freedom, and the "
            "listed late-time parameters."
        ),
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_wdw_controls(audit)
    benchmark = benchmark_wdw_controls(audit)
    endpoint = integrate_phase19_starobinsky_endpoint(audit)
    curvature = curvature_reheating_control(audit, endpoint)

    result: dict[str, object] = {
        "phase": "P20",
        "calculation": "leading WDW envelope and conditional curvature-selection controls",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "leading_WDW_control": exact,
        "benchmark": benchmark,
        "phase19_endpoint_bridge": endpoint,
        "conditional_curvature_reheating": curvature,
        "claim_status": {
            "leading_de_Sitter_WDW_envelope_selects_phi_star": "CONTRADICTED",
            "independent_pair_weight_selects_phi_star": "CONTRADICTED_CONDITIONALLY",
            "fixed_factor_symmetrization_creates_peak": "CONTRADICTED",
            "general_coherent_interference_cannot_create_extrema": "NOT_CLAIMED",
            "Cecotti_background_at_phi_star_is_F_flat": "CONTRADICTED",
            "exact_CPT_two_sheet_SUGRA_WDW_state_selects_phi_star": "OPEN_NOT_COMPUTED",
            "curvature_reheating_relation_is_parameter_free_prediction": "CONTRADICTED",
        },
        "scope_guard": {
            "what_is_computed": [
                "constant-field de Sitter hemisphere exponent and its exact symbolic derivative",
                "standard one-history and additional independent-pair envelope conventions",
                "coherent conjugate-saddle interference identity",
                "Cecotti stabilizer F-term on the one-field trajectory",
                "one unit-explicit conditional Omega_K0/reheating conversion",
            ],
            "what_is_not_computed": [
                "the exact complex Starobinsky scalar-gravity saddle",
                "a WDW current, measure, normalization, or factor ordering",
                "a CPT/Pin sheet Hilbert-space inner product or sewing action",
                "the local-SUGRA wavefunction with gravitino and ghost sectors",
                "a boson-fermion-gravitino one-loop determinant",
                "a quantized four-form selection spectrum",
                "a curvature detection or a seam-selected reheating temperature",
            ],
            "central_interpretation": (
                "the naive leading envelope does not select 5.442969, but this is "
                "not an exact two-sheet WDW no-go"
            ),
        },
        "next_calculation": {
            "probability_level_stationary_condition_standard": (
                "d Gamma_seam^(P)/d varphi|star=-s 6.277009460746/lambda^2"
            ),
            "probability_level_stationary_condition_independent_pair": (
                "d Gamma_seam^(P)/d varphi|star=-s 12.554018921492/lambda^2"
            ),
            "warning": (
                "If Gamma is defined at amplitude level, the probability contains "
                "2 Re Gamma; the determinant convention must be fixed before comparing coefficients."
            ),
        },
    }
    print("PHASE20_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
