#!/usr/bin/env python3
"""Phase 30 -- coupled conformal field--lapse contour and determinant-line gate.

The frozen Phase-24/25 connected Starobinsky interval is used as a bounded
homogeneous control.  The executable distinguishes four objects that cannot
be interchanged:

* the two-sided real-lapse identity kernel and its side-dependent Maslov data;
* a local holomorphic conformal cycle at nonzero complex lapse;
* the coupled field--lapse Gaussian thimble after completing the square; and
* the global Picard--Lefschetz intersection coefficient.

It also time-slices the homogeneous quadratic action.  A naked Hessian ratio
fails to stabilize against a constant-principal reference over the recorded
refinements, whereas one declared midpoint configuration measure makes the
relative magnitude approach the Jacobi/Van-Vleck datum.
No BFV ghost complex, full four-dimensional determinant, global intersection
number, WDW density, Pin structure, or SUGRA state is claimed.  The script
writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25


HBAR = 1.0
BASE_TIME = 0.7
SLICE_COUNTS = (10, 20, 40, 80, 160, 320)
CONTOUR_COUNTS = (10, 20, 40, 80, 160)
ORIENTATION_COUNTS = (9, 10, 11, 19, 20, 21)


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


@lru_cache(maxsize=1)
def element_hessian() -> object:
    """Return a lambdified midpoint-element Hessian in (q_L,q_R,T).

    The parameter interval is s in [0,1], with h=1/n.  The action is

      2 pi^2 int ds [ G_AB qdot^A qdot^B/(2T) + T U(q) ],

    G=diag(-6a,a^3), U=-3a+a^3 V(phi).
    """

    a_l, phi_l, a_r, phi_r, proper_time, step = sp.symbols(
        "a_l phi_l a_r phi_r T h", positive=True, real=True
    )
    a_mid = (a_l + a_r) / 2
    phi_mid = (phi_l + phi_r) / 2
    delta_a = a_r - a_l
    delta_phi = phi_r - phi_l
    slope = sp.sqrt(sp.Rational(2, 3))
    potential = sp.Rational(3, 4) * (1 - sp.exp(-slope * phi_mid)) ** 2
    element = 2 * sp.pi**2 * (
        (
            -6 * a_mid * delta_a**2
            + a_mid**3 * delta_phi**2
        )
        / (2 * proper_time * step)
        + proper_time
        * step
        * (-3 * a_mid + a_mid**3 * potential)
    )
    variables = (a_l, phi_l, a_r, phi_r, proper_time)
    return sp.lambdify(
        (a_l, phi_l, a_r, phi_r, proper_time, step),
        sp.hessian(element, variables),
        "numpy",
    )


def base_trajectory() -> dict[str, object]:
    boundary, velocity, benchmark_action = p25.benchmark()
    base = p25.solve_fixed_time(BASE_TIME, boundary, velocity)
    solution = solve_ivp(
        lambda _time, state: p25.configuration_rhs(state),
        (0.0, BASE_TIME),
        np.array([boundary[0], velocity[0], boundary[1], velocity[1]]),
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=0.01,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(solution.message)

    momentum_velocity = np.diag(
        [
            -12.0 * np.pi**2 * boundary[0],
            2.0 * np.pi**2 * boundary[0] ** 3,
        ]
    )
    momentum_block = base.velocity_monodromy @ np.linalg.inv(momentum_velocity)
    mixed_hessian = -np.linalg.inv(momentum_block)
    augmented_raw = p25.five_point_augmented_hessian(
        boundary, BASE_TIME, velocity, 1.25e-4
    )
    augmented_hessian = 0.5 * (augmented_raw + augmented_raw.T)
    finite_difference_mixed_hessian = augmented_hessian[:2, 2:4]

    step = 5e-3
    nearby = [
        p25.solve_fixed_time(BASE_TIME + offset * step, boundary, velocity)
        for offset in (-2, -1, 1, 2)
    ]
    energies = [item.energy for item in nearby]
    curvature = -(
        energies[0] - 8 * energies[1] + 8 * energies[2] - energies[3]
    ) / (12 * step)

    return {
        "boundary": boundary,
        "velocity": velocity,
        "benchmark_action": benchmark_action,
        "base": base,
        "dense_solution": solution.sol,
        "momentum_velocity": momentum_velocity,
        "momentum_block": momentum_block,
        "mixed_hessian": mixed_hessian,
        "finite_difference_mixed_hessian": finite_difference_mixed_hessian,
        "curvature": float(curvature),
    }


def assemble_discrete_control(
    segment_count: int,
    data: dict[str, object],
    *,
    contour_diagnostics: bool,
) -> dict[str, object]:
    boundary = np.asarray(data["boundary"], dtype=float)
    dense = data["dense_solution"]
    step = 1.0 / segment_count
    node_times = np.linspace(0.0, BASE_TIME, segment_count + 1)
    nodes = np.asarray(dense(node_times))[[0, 2]].T
    midpoint_scales = np.asarray(
        dense((np.arange(segment_count) + 0.5) * BASE_TIME / segment_count)
    )[0]

    full_size = 2 * (segment_count + 1) + 1
    lapse_index = full_size - 1
    joint = np.zeros((full_size, full_size), dtype=float)
    local_hessian = element_hessian()
    for element_index in range(segment_count):
        local = np.asarray(
            local_hessian(
                nodes[element_index, 0],
                nodes[element_index, 1],
                nodes[element_index + 1, 0],
                nodes[element_index + 1, 1],
                BASE_TIME,
                step,
            ),
            dtype=float,
        )
        indices = [
            2 * element_index,
            2 * element_index + 1,
            2 * element_index + 2,
            2 * element_index + 3,
            lapse_index,
        ]
        joint[np.ix_(indices, indices)] += local

    kept = list(range(2, 2 * segment_count)) + [lapse_index]
    reduced_joint = joint[np.ix_(kept, kept)]
    field_hessian = reduced_joint[:-1, :-1]
    mixing = reduced_joint[:-1, -1]
    bare_lapse = float(reduced_joint[-1, -1])
    field_solution = np.linalg.solve(field_hessian, mixing)
    schur = float(bare_lapse - mixing @ field_solution)

    reference = np.zeros((2 * (segment_count + 1),) * 2, dtype=float)
    endpoint_metric = np.diag([-6.0 * boundary[0], boundary[0] ** 3])
    kinetic = 2.0 * np.pi**2 * endpoint_metric / (BASE_TIME * step)
    reference_element = np.block([[kinetic, -kinetic], [-kinetic, kinetic]])
    for element_index in range(segment_count):
        indices = [
            2 * element_index,
            2 * element_index + 1,
            2 * element_index + 2,
            2 * element_index + 3,
        ]
        reference[np.ix_(indices, indices)] += reference_element
    reference_interior = reference[2:-2, 2:-2]

    sign, logdet = np.linalg.slogdet(field_hessian)
    reference_sign, reference_logdet = np.linalg.slogdet(reference_interior)
    raw_determinant_ratio = float(np.exp(logdet - reference_logdet))
    raw_amplitude_ratio = float(np.exp(-0.5 * (logdet - reference_logdet)))
    canonical_slice_factor = float(
        np.prod((midpoint_scales / boundary[0]) ** 2)
    )
    canonical_amplitude_ratio = raw_amplitude_ratio * canonical_slice_factor

    field_negative_count = int(
        np.count_nonzero(np.linalg.eigvalsh(field_hessian) < 0)
    )
    result: dict[str, object] = {
        "segments": segment_count,
        "raw_determinant_ratio": raw_determinant_ratio,
        "raw_amplitude_ratio": raw_amplitude_ratio,
        "canonical_slice_factor": canonical_slice_factor,
        "canonical_amplitude_ratio": canonical_amplitude_ratio,
        "determinant_sign": float(sign),
        "reference_determinant_sign": float(reference_sign),
        "relative_determinant_sign": float(sign * reference_sign),
        "field_negative_count": field_negative_count,
        "schur": schur,
    }

    if contour_diagnostics:
        eigenvalues, eigenvectors = np.linalg.eigh(field_hessian)
        spectral_phases = np.where(eigenvalues < 0.0, -1.0j, 1.0 + 0.0j)
        spectral_rotation = eigenvectors @ np.diag(spectral_phases)

        direct = np.zeros(reduced_joint.shape, dtype=np.complex128)
        direct[:-1, :-1] = spectral_rotation
        direct[-1, -1] = 1.0j
        direct_hessian = direct.T @ reduced_joint @ direct
        direct_real_eigenvalues = np.linalg.eigvalsh(np.real(direct_hessian))

        fibered = np.zeros(reduced_joint.shape, dtype=np.complex128)
        fibered[:-1, :-1] = spectral_rotation
        fibered[:-1, -1] = -1.0j * field_solution
        fibered[-1, -1] = 1.0j
        fibered_hessian = fibered.T @ reduced_joint @ fibered
        fibered_real_eigenvalues = np.linalg.eigvalsh(np.real(fibered_hessian))
        result.update(
            {
                "direct_product_negative_count": int(
                    np.count_nonzero(direct_real_eigenvalues < -1e-9)
                ),
                "direct_product_min_eigenvalue": float(
                    direct_real_eigenvalues[0]
                ),
                "fibered_min_eigenvalue": float(fibered_real_eigenvalues[0]),
                "fibered_cross_residual": float(
                    np.linalg.norm(fibered_hessian[:-1, -1])
                ),
            }
        )
    return result


def jacobi_scan(data: dict[str, object]) -> dict[str, object]:
    boundary = np.asarray(data["boundary"], dtype=float)
    center = np.array([np.sqrt(3.0 / p25.potential(1.0)), 1.0])
    records: list[dict[str, float]] = []
    for proper_time in np.linspace(0.02, BASE_TIME, 18):
        center, midpoint_endpoint = p25.solve_symmetric_center(
            float(proper_time), boundary, center
        )
        solution = p25.solve_fixed_time(
            float(proper_time), boundary, -midpoint_endpoint[[1, 3]]
        )
        singular_values = np.linalg.svd(
            solution.velocity_monodromy, compute_uv=False
        )
        records.append(
            {
                "T": float(proper_time),
                "det_Bv": float(np.linalg.det(solution.velocity_monodromy)),
                "det_Bv_over_T2": float(
                    np.linalg.det(solution.velocity_monodromy) / proper_time**2
                ),
                "min_singular_value": float(singular_values[-1]),
                "W_T": float(-solution.energy),
            }
        )
    return {"records": records}


def exact_controls(audit: Audit) -> dict[str, object]:
    mu_g, mu_s, radius = sp.symbols("mu_g mu_s rho", positive=True, real=True)
    angle = sp.symbols("theta", real=True)
    theta_g = angle / 2 - sp.pi / 4
    theta_s = angle / 2 + sp.pi / 4
    lapse = radius * sp.exp(sp.I * angle)
    gravity_coefficient = sp.simplify(
        sp.I * (-mu_g) * sp.exp(2 * sp.I * theta_g) / (2 * lapse)
    )
    scalar_coefficient = sp.simplify(
        sp.I * mu_s * sp.exp(2 * sp.I * theta_s) / (2 * lapse)
    )
    audit.exact(
        "P30.contour.coupled_principal_rays",
        gravity_coefficient == -mu_g / (2 * radius)
        and scalar_coefficient == -mu_s / (2 * radius)
        and sp.simplify(theta_s - theta_g) == sp.pi / 2,
        "the lapse-dependent gravity and scalar rays make both principal Gaussians decaying",
    )

    jacobian = sp.exp(sp.I * (theta_g + theta_s))
    gaussian_product = 2 * sp.pi * radius / sp.sqrt(mu_g * mu_s)
    holomorphic_prefactor = sp.sqrt(mu_g * mu_s) / (2 * sp.pi * lapse)
    audit.exact(
        "P30.contour.local_holomorphic_normalization",
        sp.simplify(
            holomorphic_prefactor * jacobian * gaussian_product
        )
        == 1,
        "the coupled complex Gaussian is identity-normalized on its local holomorphic cycle",
    )
    audit.exact(
        "P30.contour.Euclidean_conformal_ray",
        sp.simplify(theta_g.subs(angle, -sp.pi / 2) + sp.pi / 2) == 0
        and theta_s.subs(angle, -sp.pi / 2) == 0,
        "at N=-iT the gravity fluctuation is imaginary while the scalar remains real",
    )

    sign = sp.symbols("sigma", real=True)
    gravity_maslov = sp.exp(-sp.I * sign * sp.pi / 4)
    scalar_maslov = sp.exp(sp.I * sign * sp.pi / 4)
    audit.exact(
        "P30.Maslov.real_side_phase_cancellation",
        sp.simplify(gravity_maslov * scalar_maslov) == 1,
        "the opposite-sign one-dimensional Fresnel phases cancel on either real-lapse side",
    )
    c = sp.symbols("C", positive=True, real=True)
    audit.exact(
        "P30.Maslov.single_holomorphic_sheet_left_sign",
        sp.simplify(c / radius - c / sp.Abs(radius)) == 0
        and sp.simplify(c / (-radius) + c / sp.Abs(-radius)) == 0,
        "C/N agrees with the positive-real identity branch but gives minus the required C/|N| on the negative real side",
    )

    ell, source, bare = sp.symbols("ell j A", nonzero=True, real=True)
    block = sp.Matrix([[ell, source], [source, bare]])
    schur = sp.simplify(bare - source**2 / ell)
    audit.exact(
        "P30.schur.field_lapse_completion",
        sp.factor(block.det() - ell * schur) == 0,
        "the coupled determinant factors only after the field-dependent lapse shift",
    )
    xi, u = sp.symbols("xi u", real=True)
    eta = xi - sp.I * u * source / ell
    nu = sp.I * u
    quadratic = sp.expand(
        ell * eta**2 / 2 + source * eta * nu + bare * nu**2 / 2
    )
    audit.exact(
        "P30.contour.fibered_completion_identity",
        sp.simplify(
            quadratic - ell * xi**2 / 2 + schur * u**2 / 2
        )
        == 0,
        "the lapse-dependent field shift removes the mixed term and rotates negative Schur curvature to positive",
    )

    audit.exact(
        "P30.lapse.Wick_and_thimble_jacobians",
        sp.simplify((-sp.I) * sp.I) == 1,
        "dN=-i dT and the local lapse thimble dT=i du have cancelling Jacobians",
    )

    scale, scale_0 = sp.symbols("a_e a_0", positive=True, real=True)
    metric_det = sp.Abs((-6 * scale) * scale**3)
    metric_det_0 = sp.Abs((-6 * scale_0) * scale_0**3)
    audit.exact(
        "P30.determinant.declared_midpoint_measure_power",
        sp.simplify(sp.sqrt(metric_det / metric_det_0) - (scale / scale_0) ** 2)
        == 0,
        "the declared midpoint configuration measure contributes the exact per-slice factor (a_e/a_0)^2",
    )

    regulator = sp.symbols("delta", positive=True, real=True)
    height = sp.symbols("y", real=True)
    audit.exact(
        "P30.PL.shifted_rays_share_pointwise_open_limit",
        sp.limit(regulator + sp.I * height, regulator, 0, dir="+")
        == sp.I * height
        and sp.limit(-regulator + sp.I * height, regulator, 0, dir="+")
        == sp.I * height,
        "left- and right-shifted rays have the same pointwise limit away from the unresolved endpoint",
    )
    return {
        "principal_cycle": {
            "N": "rho exp(i theta)",
            "delta_a": "exp[i(theta/2-pi/4)] R",
            "delta_phi": "exp[i(theta/2+pi/4)] R",
        },
        "real_lapse_prefactor": "sqrt(mu_g mu_s)/(2 pi hbar |N|)",
        "holomorphic_local_prefactor": "sqrt(mu_g mu_s)/(2 pi hbar N)",
        "fibered_contour": "nu=i u; eta=R xi-i u L_D^{-1}j",
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    data = base_trajectory()
    base = data["base"]
    boundary = np.asarray(data["boundary"], dtype=float)
    momentum_block = np.asarray(data["momentum_block"], dtype=float)
    mixed_hessian = np.asarray(data["mixed_hessian"], dtype=float)
    finite_difference_mixed_hessian = np.asarray(
        data["finite_difference_mixed_hessian"], dtype=float
    )
    curvature = float(data["curvature"])

    audit.numerical(
        "P30.saddle.frozen_stationary_control",
        abs(base.action - float(data["benchmark_action"])) < 2e-10
        and abs(base.constraint) < 2e-11
        and base.endpoint_residual < 2e-10
        and abs(curvature + 8.9231430383) < 5e-7,
        "the frozen interval is stationary and has the converged negative lapse curvature",
    )
    audit.numerical(
        "P30.Jacobi.momentum_endpoint_identity",
        np.linalg.norm(mixed_hessian @ momentum_block + np.eye(2)) < 2e-10
        and np.linalg.norm(
            mixed_hessian - finite_difference_mixed_hessian, ord=2
        )
        / np.linalg.norm(finite_difference_mixed_hessian, ord=2)
        < 1e-10
        and abs(np.linalg.det(momentum_block) + 1.256938271194875e-6)
        < 3e-15,
        "the canonical endpoint identity W_-+=-B_p^{-1} agrees with an independent boundary finite-difference Hessian",
    )

    scan = jacobi_scan(data)
    scan_records = scan["records"]
    sampled_derivatives = [record["W_T"] for record in scan_records]
    audit.numerical(
        "P30.Jacobi.sampled_no_caustic_to_saddle",
        min(record["det_Bv"] for record in scan_records) > 0
        and min(record["min_singular_value"] for record in scan_records) > 0
        and min(sampled_derivatives[:-1]) > 0
        and np.all(np.diff(sampled_derivatives) < 0),
        "the sampled real branch from T=.02 to .7 has no fixed-T Dirichlet zero and reaches the lapse saddle monotonically",
    )

    slice_controls = [
        assemble_discrete_control(
            count,
            data,
            contour_diagnostics=count in CONTOUR_COUNTS,
        )
        for count in SLICE_COUNTS
    ]
    contour_controls = [
        item for item in slice_controls if "direct_product_negative_count" in item
    ]
    slice_by_count = {
        int(item["segments"]): item for item in slice_controls
    }
    orientation_controls = [
        slice_by_count[count]
        if count in slice_by_count
        else assemble_discrete_control(count, data, contour_diagnostics=False)
        for count in ORIENTATION_COUNTS
    ]

    endpoint_ratio = float(np.linalg.det(base.velocity_monodromy) / BASE_TIME**2)
    endpoint_factor = float(endpoint_ratio ** (-0.5))
    canonical_values = [
        float(item["canonical_amplitude_ratio"]) for item in slice_controls
    ]
    raw_ratios = [float(item["raw_determinant_ratio"]) for item in slice_controls]
    audit.numerical(
        "P30.determinant.declared_midpoint_measure_convergence",
        raw_ratios[-1] > 50.0
        and np.all(np.diff(raw_ratios) > 0)
        and max(canonical_values) < endpoint_factor
        and np.all(np.diff(canonical_values) > 0)
        and abs(canonical_values[-1] - endpoint_factor) < 3e-5,
        "the naked magnitude ratio grows rapidly across the recorded cutoffs while the declared midpoint measure converges to the endpoint Van-Vleck magnitude",
    )
    audit.numerical(
        "P30.determinant.cutoff_parity_phase_obstruction",
        all(
            item["field_negative_count"] == item["segments"] - 1
            and item["determinant_sign"]
            == (-1.0 if (item["segments"] - 1) % 2 else 1.0)
            and item["relative_determinant_sign"] == 1.0
            for item in orientation_controls
        ),
        "the absolute field-determinant sign alternates with cutoff parity even though the declared reference magnitude ratio stays positive, so the continuum determinant-line phase remains open",
    )

    schur_values = [float(item["schur"]) for item in slice_controls]
    audit.numerical(
        "P30.schur.discrete_bulk_lapse_convergence",
        np.all(np.diff(schur_values) < 0)
        and abs(schur_values[-1] - curvature) < 5e-4,
        "the discrete field-lapse Schur complement through 320 slices converges to W_TT",
    )
    audit.numerical(
        "P30.contour.direct_product_fails",
        all(item["direct_product_negative_count"] == 1 for item in contour_controls)
        and all(item["direct_product_min_eigenvalue"] < -1 for item in contour_controls),
        "the tested standard independent field and lapse rotations leave one negative direction at every tested cutoff",
    )
    audit.numerical(
        "P30.contour.fibered_cycle_passes",
        all(item["fibered_min_eigenvalue"] > 0 for item in contour_controls)
        and max(item["fibered_cross_residual"] for item in contour_controls)
        < 5e-8,
        "the Schur-shifted fibered contour removes the mixed term and has positive real quadratic form",
    )

    determinant_magnitude = float(np.sqrt(abs(np.linalg.det(mixed_hessian))))
    fixed_time_prefactor = determinant_magnitude / (2 * np.pi)
    lapse_factor = float(np.sqrt(2 * np.pi / abs(curvature)))
    local_flat_prefactor = fixed_time_prefactor * lapse_factor
    local_flat_weight = local_flat_prefactor * float(np.exp(-base.action))
    audit.numerical(
        "P30.prefactor.conditional_local_magnitude",
        abs(endpoint_factor - 1.01502655703120) < 3e-12
        and abs(fixed_time_prefactor - 141.9590736591) < 2e-10
        and abs(lapse_factor - 0.8391333983) < 2e-10
        and abs(local_flat_weight - 29.1793909650) < 2e-9,
        "the flat-endpoint Van-Vleck magnitude and lapse Gaussian give the conditional local-flat weight, while the separate relative endpoint factor is recorded only as a control",
    )

    phases = np.array([-np.pi / 2, -np.pi / 4, 0.0, np.pi / 3])
    mu_g = abs(2 * np.pi**2 * (-6 * boundary[0]))
    mu_s = abs(2 * np.pi**2 * boundary[0] ** 3)
    radius = 0.37
    normalization_samples = []
    for angle in phases:
        theta_g = angle / 2 - np.pi / 4
        theta_s = angle / 2 + np.pi / 4
        jacobian = np.exp(1j * (theta_g + theta_s))
        gaussian = 2 * np.pi * radius / np.sqrt(mu_g * mu_s)
        prefactor = np.sqrt(mu_g * mu_s) / (
            2 * np.pi * radius * np.exp(1j * angle)
        )
        normalization_samples.append(prefactor * jacobian * gaussian)
    audit.numerical(
        "P30.contour.complex_principal_normalization",
        max(abs(value - 1) for value in normalization_samples) < 2e-15,
        "the coupled principal Gaussian remains normalized along four complex-lapse angles",
    )

    return {
        "base": {
            "T_star": BASE_TIME,
            "W_star": base.action,
            "W_TT": curvature,
            "boundary": boundary.tolist(),
        },
        "Jacobi": {
            "det_Bp": float(np.linalg.det(momentum_block)),
            "det_mixed_hessian": float(np.linalg.det(mixed_hessian)),
            "finite_difference_relative_residual": float(
                np.linalg.norm(
                    mixed_hessian - finite_difference_mixed_hessian, ord=2
                )
                / np.linalg.norm(finite_difference_mixed_hessian, ord=2)
            ),
            "endpoint_ratio": endpoint_ratio,
            "endpoint_relative_factor": endpoint_factor,
            "scan": scan_records,
        },
        "time_slicing": slice_controls,
        "determinant_line_orientation": {
            "records": orientation_controls,
            "status": "absolute cutoff parity alternates; the declared relative reference cancels the finite-lattice sign but does not derive a continuum Maslov phase",
        },
        "prefactor": {
            "fixed_time_endpoint_magnitude": fixed_time_prefactor,
            "lapse_Gaussian": lapse_factor,
            "local_flat_prefactor": local_flat_prefactor,
            "local_flat_weight_hbar1": local_flat_weight,
            "status": "conditional on determinant orientation, BFV normalization, and global intersection coefficient",
        },
        "endpoint_regulator_status": {
            "common_pointwise_open_limit": "positive imaginary T ray",
            "intersection_number": None,
            "reason": "the contact at T=0 is a singular non-transverse endpoint and no complete dual cycle was computed",
        },
        "complex_normalization_samples": [
            [float(value.real), float(value.imag)]
            for value in normalization_samples
        ],
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P30",
        "calculation": "coupled conformal field-lapse contour and determinant-line gate",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "a_finite_cutoff_local_coupled_field_lapse_Gaussian_cycle_exists": "SUPPORTED_IN_THE_FROZEN_HOMOGENEOUS_QUADRATIC_CONTROL",
            "the_tested_standard_independent_field_and_lapse_Wick_rotations_are_sufficient": "CONTRADICTED_BY_THE_MIXED_HESSIAN",
            "the_declared_midpoint_measure_normalized_endpoint_magnitude_has_a_recorded_limit": "SUPPORTED_NUMERICALLY_IN_THE_RECORDED_TIME_SLICING",
            "the_absolute_lattice_determinant_sign_has_a_cutoff_independent_limit": "CONTRADICTED_BY_ODD_EVEN_CUTOFF_PARITY",
            "the_naked_bulk_Hessian_ratio_is_the_physical_functional_determinant": "CONTRADICTED_BY_STRONG_RECORDED_CUTOFF_DEPENDENCE_AND_MISSING_PHASE",
            "one_holomorphic_lapse_sheet_gives_the_identity_kernel_on_both_real_sides": "CONTRADICTED_BY_THE_MASLOV_ORIENTATION_JUMP",
            "the_positive_half_lapse_ray_fixes_an_integer_PL_coefficient": "OPEN_ENDPOINT_AND_GLOBAL_DUAL_CYCLE_NOT_DERIVED",
            "the_full_physical_PL_coefficient_for_the_connected_saddle_is_fixed": "OPEN_NOT_DERIVED",
            "a_positive_trace_class_seam_state_or_initial_value_is_selected": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "the frozen homogeneous a-phi principal and midpoint quadratic forms",
                "a coupled lapse-dependent conformal principal cycle",
                "the discrete field-lapse Schur complement and fibered Gaussian contour",
                "declared midpoint configuration-measure convergence to an endpoint Van-Vleck magnitude",
                "a conditional local-flat endpoint-plus-lapse prefactor magnitude",
                "the common pointwise open limit of two shifted endpoint rays",
            ],
            "not_computed": [
                "an absolute zeta determinant or cutoff-independent determinant phase",
                "the full BFV phase-space ghost/gauge super-Hessian and the inhomogeneous graviton, scalar, fermion, and gravitino spectra",
                "a complete global relative-homology cycle or all complex saddles",
                "the positive-half-lapse endpoint coefficient after a physical regulator",
                "a WDW physical trace, density matrix, Pin lift, or initial-value distribution",
            ],
        },
        "next_calculation": (
            "construct the finite-cutoff homogeneous BFV phase-space super-Hessian, "
            "track its determinant line through N=0, and then compute all upward-thimble intersections before "
            "taking regulator and mode-cutoff limits"
        ),
    }
    print("PHASE30_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
