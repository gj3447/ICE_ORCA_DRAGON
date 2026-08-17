#!/usr/bin/env python3
"""Phase 36 -- local Airy/Gauss--Manin fold connection.

The script fixes exact identities in a declared local contour basis at the
simple Dirichlet fold of Phases 33--35 and independently continues both real
stationary roots around small upper/lower semicircles in the complex
proper-time plane.  The exact layer distinguishes integration cycles, their
inverse-transpose upward duals, Stokes basis changes, and the relative
endpoint-determinant half phase.  The numerical layer only identifies which
complex BVP root is reached by each lateral continuation.

The CW and CCW ordered bases use different companion cycles, so their first
dual vectors are different lateralized basis elements.  The calculation does
not transport one common incoming physical dual through both continuations.

This is a local, finite-dimensional connection calculation.  It neither
chooses the upper rather than lower lateral continuation nor computes a full
BFV/SUGRA determinant, complete relative cycle, global intersection number,
WDW state, initial-value peak, or SUSY scale.  The script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.optimize import root

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase33_fold_airy_uniformization as p33
    from . import phase34_directed_fold_dual_continuation as p34
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase33_fold_airy_uniformization as p33
    import phase34_directed_fold_dual_continuation as p34


RADIUS_CONFIGS = ((2.0e-4, 25), (1.0e-3, 25), (5.0e-3, 33))
DETERMINANT_SAMPLE_COUNT = 9


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


def pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def matrix_pairs(matrix: np.ndarray) -> list[list[list[float]]]:
    return [[pair(complex(value)) for value in row] for row in matrix]


def exact_controls(audit: Audit) -> dict[str, object]:
    t, z = sp.symbols("t z", positive=True, real=True)
    airy_exponent = t**3 / 3 - z * t
    tracked_saddle = sp.sqrt(z)
    other_saddle = -sp.sqrt(z)
    audit.exact(
        "P36.canonical.positive_t_is_decaying_Ai_saddle",
        sp.diff(airy_exponent, t).subs(t, tracked_saddle) == 0
        and sp.diff(airy_exponent, t).subs(t, other_saddle) == 0
        and sp.simplify(
            airy_exponent.subs(t, tracked_saddle)
            + sp.Rational(2, 3) * z ** sp.Rational(3, 2)
        )
        == 0,
        "for f=t^3/3-zt, t=+sqrt(z) is stationary and has exponent -2 z^(3/2)/3; identifying it with the tracked x>0 sheet uses the separately declared x-to-u-to-t chart",
    )

    # Contour-chain coordinates use (Gamma_U,Gamma_L).  The three decay-ray
    # contours obey Gamma_0+Gamma_L+Gamma_U=0.
    gamma_u = sp.Matrix([1, 0])
    gamma_l = sp.Matrix([0, 1])
    gamma_0 = -gamma_u - gamma_l
    audit.exact(
        "P36.contours.three_ray_relation",
        gamma_0 + gamma_l + gamma_u == sp.zeros(2, 1),
        "the oriented decay-ray contours obey Gamma_0+Gamma_L+Gamma_U=0",
    )

    arm_from_airy = sp.Matrix(
        [[-1, -sp.I], [-1, sp.I]]
    ) / 2
    airy_from_arm = sp.Matrix([[-1, -1], [sp.I, -sp.I]])
    audit.exact(
        "P36.contours.declared_Airy_arm_matrix",
        sp.simplify(arm_from_airy * airy_from_arm) == sp.eye(2)
        and sp.simplify(airy_from_arm * arm_from_airy) == sp.eye(2)
        and airy_from_arm[0, :] == sp.Matrix([[-1, -1]]),
        "the declared arm-order (U,L) and (Ai,Bi) matrices are exact inverses and encode Ai=-J_U-J_L",
    )

    gauss_manin = sp.Matrix([[-1, -1], [0, 1]])
    audit.exact(
        "P36.Gauss_Manin.CW_cycle_map",
        gauss_manin**2 == sp.eye(2)
        and gauss_manin * sp.Matrix([1, 0]) == sp.Matrix([-1, 0]),
        "for CW bases (Gamma_0,Gamma_L)_in and (Gamma_U,Gamma_L)_out, G=[[-1,-1],[0,1]] and G inverse equals G",
    )

    cw_in = sp.Matrix.vstack(gamma_0.T, gamma_l.T)
    cw_out = sp.Matrix.vstack(gamma_u.T, gamma_l.T)
    ccw_in = sp.Matrix.vstack(gamma_0.T, gamma_u.T)
    ccw_out = sp.Matrix.vstack(gamma_l.T, gamma_u.T)
    audit.exact(
        "P36.Gauss_Manin.CW_CCW_ordered_bases",
        cw_in == gauss_manin * cw_out
        and ccw_in == gauss_manin * ccw_out,
        "the same G acts on the frozen CW order (Gamma_0,Gamma_L)->(Gamma_U,Gamma_L) and CCW order (Gamma_0,Gamma_U)->(Gamma_L,Gamma_U)",
    )

    dual_map = gauss_manin.inv().T
    audit.exact(
        "P36.Gauss_Manin.inverse_transpose_pairing",
        dual_map == sp.Matrix([[-1, 0], [-1, 1]])
        and sp.simplify(gauss_manin.T * dual_map) == sp.eye(2),
        "dual bases transform by G^(-T), preserving the pairing in each separately declared ordered lateral basis",
    )

    # A dual basis depends on the complete ordered cycle basis, not only on
    # its first element Gamma_0.  CW and CCW use different companion cycles,
    # so their first dual vectors are distinct elements in the common
    # (K_U,K_L) coordinates.  This is basis dependence, not transport of one
    # fixed incoming physical dual to two different arms.
    cw_in_dual = cw_in.inv().T
    ccw_in_dual = ccw_in.inv().T
    audit.exact(
        "P36.lateral.CW_CCW_basis_label_dependence",
        cw_in_dual[0, :] == sp.Matrix([[-1, 0]])
        and ccw_in_dual[0, :] == sp.Matrix([[0, -1]])
        and cw_in_dual[0, :] != ccw_in_dual[0, :]
        and cw_in * cw_in_dual.T == sp.eye(2)
        and ccw_in * ccw_in_dual.T == sp.eye(2),
        "the first dual of Gamma_0 is -K_U in the (Gamma_0,Gamma_L) basis and -K_L in the (Gamma_0,Gamma_U) basis; these are different lateralized dual conventions, not one transported dual",
    )

    e_minus = gamma_l
    e_plus = -gamma_u
    stokes_down = sp.Matrix([[1, 0], [1, 1]])
    stokes_up = sp.Matrix([[1, -1], [0, 1]])
    audit.exact(
        "P36.Stokes.enhanced_lateral_matrices",
        e_plus == gamma_0 + gamma_l
        and e_minus == gamma_l
        and stokes_down * sp.Matrix.vstack(gamma_0.T, gamma_l.T)
        == sp.Matrix.vstack(gamma_0.T, e_plus.T)
        and stokes_down.det() == 1
        and stokes_up.det() == 1
        and stokes_up == stokes_down.inv().T,
        "for E_-=Gamma_L and E_+=-Gamma_U=Gamma_0+Gamma_L, S_down=[[1,0],[1,1]] and S_up=S_down^(-T)",
    )

    upper_sqrt = sp.exp(-sp.I * sp.pi / 4)
    lower_sqrt = sp.exp(sp.I * sp.pi / 4)
    sqrt_transport = sp.diag(upper_sqrt, lower_sqrt)
    inverse_sqrt_transport = sp.diag(1 / upper_sqrt, 1 / lower_sqrt)
    audit.exact(
        "P36.detline.declared_fold_half_phase_basis",
        sp.simplify(upper_sqrt**2 + sp.I) == 0
        and sp.simplify(lower_sqrt**2 - sp.I) == 0
        and sp.simplify(sqrt_transport * inverse_sqrt_transport) == sp.eye(2),
        "in the declared leading-fold arm order (U,L), sqrt(det) has phases (e^-i pi/4,e^+i pi/4) and the inverse-sqrt endpoint factor has the opposite half phases",
    )

    zeta, hard_determinant = sp.symbols(
        "zeta d_hat", positive=True, real=True
    )
    canonical_u = sp.symbols("u", real=True)
    canonical_phase = canonical_u**3 / 3 - zeta * canonical_u
    tracked_u = -sp.sqrt(zeta)
    soft_factor = -sp.diff(canonical_phase, canonical_u, 2).subs(
        canonical_u, tracked_u
    ) / 2
    full_determinant = hard_determinant * soft_factor
    separate_prefactor = 1 / sp.sqrt(full_determinant)
    factorized_prefactor = (
        1 / sp.sqrt(hard_determinant) / zeta ** sp.Rational(1, 4)
    )
    audit.exact(
        "P36.uniformization.conditional_soft_hard_factorization",
        sp.simplify(soft_factor - sp.sqrt(zeta)) == 0
        and sp.simplify(full_determinant / soft_factor - hard_determinant)
        == 0
        and sp.simplify(separate_prefactor - factorized_prefactor) == 0,
        "conditional on d=sqrt(zeta)*d_hat, the separate-saddle inverse square root factorizes as d_hat^(-1/2)*zeta^(-1/4); using CFU without duplicating this soft factor is bookkeeping, not a derivation of the hard Airy/Airy-prime coefficients",
    )

    identity = sp.eye(2)
    permutation = sp.Matrix([[0, 1], [1, 0]])
    bare_cw = sp.exp(sp.I * sp.pi / 4) * permutation
    bare_ccw = sp.exp(-sp.I * sp.pi / 4) * identity
    lateral_ratio = sp.simplify(bare_cw * bare_ccw.inv())
    audit.exact(
        "P36.detline.formal_bare_root_ratio_under_declared_lift",
        lateral_ratio == sp.I * permutation
        and sp.simplify(lateral_ratio**2 + sp.eye(2)) == sp.zeros(2),
        "in the declared leading-fold inverse-sqrt trivialization, the formal root-basis lateral ratio is iP and its square is -I; this is neither the finite-radius BVP value nor the Gauss--Manin cycle matrix G",
    )

    fold_time = sp.Rational(9788625568, 10**9)
    fold_patch_radius = sp.Integer(1)
    largest_phase32_cap = sp.Rational(1, 10)
    audit.exact(
        "P36.scope.fold_patch_disjoint_from_Phase32_origin_caps",
        fold_time - fold_patch_radius - largest_phase32_cap > 0,
        "the declared radius-one fold patch is disjoint from every recorded Phase-32 origin cap with |T|<=0.1",
    )

    return {
        "canonical_exponent": "f(t,z)=t^3/3-z t, integrand exp(f); physical soft x maps through u=-alpha x and t=-u",
        "decay_rays": {"D_minus": "arg t=-pi/3", "D_plus": "arg t=+pi/3", "D_pi": "arg t=pi"},
        "contours": {
            "Gamma_0": "D_minus -> D_plus",
            "Gamma_L": "D_plus -> D_pi",
            "Gamma_U": "D_pi -> D_minus",
            "relation": "Gamma_0+Gamma_L+Gamma_U=0",
        },
        "Airy_integrals": {
            "J_0": "Ai(z)",
            "J_L": "omega Ai(omega z)",
            "J_U": "omega^2 Ai(omega^2 z)",
            "omega": "exp(2 pi i/3)",
        },
        "arm_order": ["U", "L"],
        "arm_from_Ai_Bi": [["-1/2", "-i/2"], ["-1/2", "+i/2"]],
        "Ai_Bi_from_arm": [["-1", "-1"], ["+i", "-i"]],
        "Gauss_Manin_G": [[-1, -1], [0, 1]],
        "Gauss_Manin_basis_orders": {
            "CW": "(Gamma_0,Gamma_L)_in -> (Gamma_U,Gamma_L)_out",
            "CCW": "(Gamma_0,Gamma_U)_in -> (Gamma_L,Gamma_U)_out",
        },
        "dual_G_inverse_transpose": [[-1, 0], [-1, 1]],
        "CW_first_dual_in_basis_Gamma0_GammaL": "-K_U",
        "CCW_first_dual_in_basis_Gamma0_GammaU": "-K_L",
        "dual_warning": "these are distinct lateralized dual-basis elements, not two images of one common transported physical dual",
        "Stokes_down": [[1, 0], [1, 1]],
        "Stokes_up": [[1, -1], [0, 1]],
        "determinant_half_phase": {
            "sqrt_arm_order_U_L": ["epsilon_U exp(-i pi/4)", "epsilon_L exp(+i pi/4)"],
            "inverse_sqrt_arm_order_U_L": ["epsilon_U exp(+i pi/4)", "epsilon_L exp(-i pi/4)"],
            "epsilon_U_L": "independent relative signs remain unresolved by the endpoint determinant alone",
        },
        "uniformization_double_counting_guard": (
            "conditional on d=sqrt(zeta)*d_hat, the soft factor belongs in the "
            "CFU uniformization rather than being multiplied twice; the hard "
            "quotient and the even/odd Airy/Airy-prime amplitudes are not constructed here"
        ),
    }


def center_to_vector(center: np.ndarray) -> np.ndarray:
    return np.array(
        [center[0].real, center[0].imag, center[1].real, center[1].imag]
    )


def vector_to_center(vector: np.ndarray) -> np.ndarray:
    return np.array(
        [complex(vector[0], vector[1]), complex(vector[2], vector[3])]
    )


def prescribed_endpoint_residual(
    vector: np.ndarray, proper_length: complex, boundary: np.ndarray
) -> np.ndarray:
    center = vector_to_center(vector)
    half_final = p34.symmetric_half_flow(proper_length, center)
    difference = half_final[[0, 2]] - boundary[:2]
    return np.array(
        [
            difference[0].real,
            difference[0].imag,
            difference[1].real,
            difference[1].imag,
        ]
    )


def solve_prescribed_center(
    proper_length: complex, boundary: np.ndarray, guess: np.ndarray
) -> tuple[np.ndarray, float]:
    solved = root(
        lambda vector: prescribed_endpoint_residual(
            vector, proper_length, boundary
        ),
        center_to_vector(guess),
        method="hybr",
        tol=1e-11,
        options={"maxfev": 800},
    )
    residual = float(
        np.linalg.norm(
            prescribed_endpoint_residual(solved.x, proper_length, boundary)
        )
    )
    if (
        not np.all(np.isfinite(solved.x))
        or not np.isfinite(residual)
        or residual > 2e-8
    ):
        raise RuntimeError(
            f"prescribed complex-T BVP failed at T={proper_length}: "
            f"{residual}; {solved.message}"
        )
    return vector_to_center(solved.x), residual


def light_record(
    proper_length: complex,
    center: np.ndarray,
    boundary: np.ndarray,
    fold_center: np.ndarray,
    right_null: np.ndarray,
) -> dict[str, object]:
    half_final = p34.symmetric_half_flow(proper_length, center)
    return {
        "T": proper_length,
        "center": center.copy(),
        "soft": complex(right_null @ (center - fold_center)),
        "action": complex(2.0 * half_final[4]),
        "velocity": -half_final[[1, 3]],
    }


def add_determinant_data(
    record: dict[str, object], boundary: np.ndarray
) -> dict[str, object]:
    final, monodromy = p34.full_flow_and_variation(
        complex(record["T"]), boundary, np.asarray(record["velocity"])
    )
    block = monodromy[np.ix_([0, 2], [1, 3])]
    singular_values = np.linalg.svd(block, compute_uv=False)
    enriched = record.copy()
    enriched.update(
        {
            "determinant": complex(np.linalg.det(block)),
            "sigma_min": float(singular_values[-1]),
            "full_endpoint_residual": float(
                np.linalg.norm(final[[0, 2]] - boundary[2:])
            ),
        }
    )
    return enriched


def unwrap_phase(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if len(values) == 0 or np.any(np.abs(values) == 0.0):
        raise ValueError("phase lift requires a nonempty nonzero path")
    phases = np.empty(len(values), dtype=float)
    increments = np.empty(max(0, len(values) - 1), dtype=float)
    phases[0] = float(np.angle(values[0]))
    for index in range(1, len(values)):
        increment = float(np.angle(values[index] / values[index - 1]))
        increments[index - 1] = increment
        phases[index] = phases[index - 1] + increment
    return phases, increments


def continuous_power(values: np.ndarray, power: float) -> np.ndarray:
    phases, _increments = unwrap_phase(values)
    return np.exp(power * (np.log(np.abs(values)) + 1.0j * phases))


def determinant_indices(point_count: int) -> np.ndarray:
    return np.unique(
        np.rint(
            np.linspace(0, point_count - 1, DETERMINANT_SAMPLE_COUNT)
        ).astype(int)
    )


def continue_semicircle(
    start_center: np.ndarray,
    lateral_sign: int,
    radius: float,
    point_count: int,
    boundary: np.ndarray,
    fold_time: float,
    fold_center: np.ndarray,
    right_null: np.ndarray,
) -> tuple[list[dict[str, object]], float]:
    angles = np.linspace(lateral_sign * np.pi, 0.0, point_count)
    center = np.asarray(start_center, dtype=np.complex128)
    first_time = complex(fold_time - radius, 0.0)
    records = [
        light_record(
            first_time, center, boundary, fold_center, right_null
        )
    ]
    max_root_residual = 0.0
    for angle in angles[1:]:
        proper_length = fold_time + radius * np.exp(1.0j * angle)
        center, residual = solve_prescribed_center(
            proper_length, boundary, center
        )
        max_root_residual = max(max_root_residual, residual)
        records.append(
            light_record(
                proper_length, center, boundary, fold_center, right_null
            )
        )

    selected = set(determinant_indices(point_count).tolist())
    for index in selected:
        records[index] = add_determinant_data(records[index], boundary)
    return records, max_root_residual


def route_summary(
    paths: list[list[dict[str, object]]],
    root_residuals: list[float],
    boundary: np.ndarray,
    fold_time: float,
) -> dict[str, object]:
    point_count = len(paths[0])
    selected = determinant_indices(point_count)
    path_summaries: list[dict[str, object]] = []
    for incoming_index, records in enumerate(paths):
        determinant_values = np.array(
            [complex(records[index]["determinant"]) for index in selected]
        )
        determinant_phases, increments = unwrap_phase(determinant_values)
        end = records[-1]
        path_summaries.append(
            {
                "incoming_index": incoming_index,
                "end_soft": pair(complex(end["soft"])),
                "end_center": [pair(complex(value)) for value in end["center"]],
                "end_action": pair(complex(end["action"])),
                "end_det_Bv": pair(determinant_values[-1]),
                "det_phase_start": float(determinant_phases[0]),
                "det_phase_end": float(determinant_phases[-1]),
                "det_phase_rotation": float(
                    determinant_phases[-1] - determinant_phases[0]
                ),
                "max_sampled_det_phase_increment": float(
                    max(abs(increments))
                ),
                "min_sampled_sigma_Bv": float(
                    min(float(records[index]["sigma_min"]) for index in selected)
                ),
                "max_full_endpoint_residual": float(
                    max(
                        float(records[index]["full_endpoint_residual"])
                        for index in selected
                    )
                ),
                "max_root_residual": float(root_residuals[incoming_index]),
            }
        )

    action_gap = np.array(
        [
            complex(paths[1][index]["action"])
            - complex(paths[0][index]["action"])
            for index in range(point_count)
        ]
    )
    gap_phases, gap_increments = unwrap_phase(action_gap)
    zeta = continuous_power(0.75 * action_gap, 2.0 / 3.0)
    x_values = np.array(
        [fold_time - complex(paths[0][index]["T"]) for index in range(point_count)]
    )
    zeta_ratios = zeta / x_values
    return {
        "paths": path_summaries,
        "action_gap_start": pair(action_gap[0]),
        "action_gap_end": pair(action_gap[-1]),
        "action_gap_phase_rotation": float(gap_phases[-1] - gap_phases[0]),
        "max_action_gap_phase_increment": float(max(abs(gap_increments))),
        "zeta_over_Tc_minus_T": {
            "start": pair(zeta_ratios[0]),
            "midpoint": pair(zeta_ratios[point_count // 2]),
            "endpoint": pair(zeta_ratios[-1]),
            "path_mean": pair(complex(np.mean(zeta_ratios))),
            "max_deviation_from_path_mean": float(
                np.max(np.abs(zeta_ratios - np.mean(zeta_ratios)))
            ),
        },
    }


def recorded_phase25_sheet(
    boundary: np.ndarray, target_time: float
) -> np.ndarray:
    center = np.array([np.sqrt(3.0 / p25.potential(1.0)), 1.0])
    center, _endpoint = p25.solve_symmetric_center(0.7, boundary, center)
    for proper_length in np.linspace(0.7, target_time, 24)[1:]:
        center, _endpoint = p25.solve_symmetric_center(
            float(proper_length), boundary, center
        )
    return center


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, _velocity, _action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    right_null = p34.deterministic_right_null(
        np.asarray(fold["right_null_vector"], dtype=float)
    )

    smallest_radius = RADIUS_CONFIGS[0][0]
    real_small = p33.solve_two_branches(boundary, fold, smallest_radius)
    recorded_center = recorded_phase25_sheet(
        boundary, fold_time - smallest_radius
    )
    real_soft = [
        float(right_null @ (np.asarray(branch["center"]) - fold_center))
        for branch in real_small
    ]
    recorded_soft = float(right_null @ (recorded_center - fold_center))
    audit.numerical(
        "P36.branch.tracked_real_sheet_identification",
        real_soft[0] < 0.0 < real_soft[1]
        and recorded_soft > 0.0
        and np.linalg.norm(recorded_center - np.asarray(real_small[1]["center"]))
        < 2e-9
        and float(real_small[0]["det_Bv"]) < 0.0
        < float(real_small[1]["det_Bv"]),
        "a fresh Phase-36 continuation using the Phase-25 solver and seed identifies incoming I_+ by positive physical soft coordinate and endpoint determinant; its Ai label additionally uses the frozen sign chart",
    )

    radius_records: list[dict[str, object]] = []
    for radius, point_count in RADIUS_CONFIGS:
        real_branches = p33.solve_two_branches(boundary, fold, radius)
        centers = [
            np.asarray(branch["center"], dtype=np.complex128)
            for branch in real_branches
        ]
        start_soft = [
            float(right_null @ (center.real - fold_center))
            for center in centers
        ]
        lateral_results: dict[str, object] = {}
        for lateral_sign, name in ((1, "upper_T_CW"), (-1, "lower_T_CCW")):
            paths: list[list[dict[str, object]]] = []
            root_residuals: list[float] = []
            for center in centers:
                records, residual = continue_semicircle(
                    center,
                    lateral_sign,
                    radius,
                    point_count,
                    boundary,
                    fold_time,
                    fold_center,
                    right_null,
                )
                paths.append(records)
                root_residuals.append(residual)
            lateral_results[name] = route_summary(
                paths, root_residuals, boundary, fold_time
            )
        radius_records.append(
            {
                "radius": radius,
                "point_count_per_path": point_count,
                "determinant_sample_count_per_path": int(
                    len(determinant_indices(point_count))
                ),
                "incoming_order": ["I_minus_soft", "I_plus_tracked_Ai"],
                "start_soft": start_soft,
                "start_det_Bv": [
                    float(branch["det_Bv"]) for branch in real_branches
                ],
                "laterals": lateral_results,
            }
        )

    def lateral(record: dict[str, object], name: str) -> dict[str, object]:
        return record["laterals"][name]

    audit.numerical(
        "P36.BVP.twelve_path_residuals",
        max(
            path["max_root_residual"]
            for record in radius_records
            for name in ("upper_T_CW", "lower_T_CCW")
            for path in lateral(record, name)["paths"]
        )
        < 2e-10
        and max(
            path["max_full_endpoint_residual"]
            for record in radius_records
            for name in ("upper_T_CW", "lower_T_CCW")
            for path in lateral(record, name)["paths"]
        )
        < 8e-8,
        "all twelve upper/lower prescribed-complex-T root paths solve the half BVP and independently reintegrated sampled full endpoint problem",
    )

    mapping_passes = []
    for record in radius_records:
        upper_paths = lateral(record, "upper_T_CW")["paths"]
        lower_paths = lateral(record, "lower_T_CCW")["paths"]
        upper_signs = [np.sign(path["end_soft"][1]) for path in upper_paths]
        lower_signs = [np.sign(path["end_soft"][1]) for path in lower_paths]
        mapping_passes.append(
            upper_signs == [1.0, -1.0]
            and lower_signs == [-1.0, 1.0]
        )
    audit.numerical(
        "P36.BVP.lateral_root_permutations",
        all(mapping_passes),
        "in BVP-root order (O_minus Im soft<0,O_plus Im soft>0) versus (I_minus,I_plus), upper-T/CW gives P and lower-T/CCW gives I; these root permutations are distinct from the cycle matrix G",
    )

    smallest = radius_records[0]
    upper_small = lateral(smallest, "upper_T_CW")
    lower_small = lateral(smallest, "lower_T_CCW")
    audit.numerical(
        "P36.BVP.tracked_root_lateral_sheet_mapping",
        upper_small["paths"][1]["end_soft"][1] < 0.0
        and lower_small["paths"][1]["end_soft"][1] > 0.0,
        "the tracked I_plus/Ai root reaches the P34 upper U arm through the upper-T/CW bypass and the lower L arm through the lower-T/CCW bypass",
    )

    audit.numerical(
        "P36.CFU.action_gap_winding",
        max(
            abs(lateral(record, "upper_T_CW")["action_gap_phase_rotation"] + 1.5 * np.pi)
            for record in radius_records
        )
        < 2e-6
        and max(
            abs(lateral(record, "lower_T_CCW")["action_gap_phase_rotation"] - 1.5 * np.pi)
            for record in radius_records
        )
        < 2e-6,
        "the oriented two-root action gap winds by -3pi/2 on upper-T/CW and +3pi/2 on lower-T/CCW continuation",
    )

    smallest_ratios = upper_small["zeta_over_Tc_minus_T"]
    path_deviations = [
        lateral(record, "upper_T_CW")["zeta_over_Tc_minus_T"]["max_deviation_from_path_mean"]
        for record in radius_records
    ]
    audit.numerical(
        "P36.CFU.complex_canonical_coordinate",
        abs(smallest_ratios["path_mean"][0] - 16.94791) < 2e-4
        and abs(smallest_ratios["path_mean"][1]) < 1e-4
        and path_deviations[0] < path_deviations[1] < path_deviations[2]
        and path_deviations[0] < 1e-4,
        "three finite radii of the sampled action-gap lift are consistent with one locally analytic CFU coordinate and a real-positive zeta/(Tc-T) coefficient near 16.94791; this is not an analyticity or limit proof",
    )

    def rotations(record: dict[str, object], name: str) -> list[float]:
        return [
            float(path["det_phase_rotation"])
            for path in lateral(record, name)["paths"]
        ]

    upper_rotations = [rotations(record, "upper_T_CW") for record in radius_records]
    lower_rotations = [rotations(record, "lower_T_CCW") for record in radius_records]
    upper_errors = [
        max(abs(value + np.pi / 2.0) for value in values)
        for values in upper_rotations
    ]
    lower_errors = [
        max(abs(value - np.pi / 2.0) for value in values)
        for values in lower_rotations
    ]
    audit.numerical(
        "P36.detline.finite_radius_half_phase_consistency",
        upper_errors[0] < upper_errors[1] < upper_errors[2]
        and lower_errors[0] < lower_errors[1] < lower_errors[2]
        and upper_errors[0] < 0.011
        and lower_errors[0] < 0.011
        and abs(np.mean(upper_rotations[0]) + np.pi / 2.0) < 2e-9
        and abs(np.mean(lower_rotations[0]) - np.pi / 2.0) < 2e-9,
        "the errors decrease across three recorded radii and the smallest finite radius is within 0.011 of the declared opposite fold half phases; this is not a certified zero-radius limit",
    )

    audit.numerical(
        "P36.detline.no_sampled_semicircle_zero",
        min(
            path["min_sampled_sigma_Bv"]
            for record in radius_records
            for name in ("upper_T_CW", "lower_T_CCW")
            for path in lateral(record, name)["paths"]
        )
        > 0.05
        and max(
            path["max_sampled_det_phase_increment"]
            for record in radius_records
            for name in ("upper_T_CW", "lower_T_CCW")
            for path in lateral(record, name)["paths"]
        )
        < 0.25,
        "nine-point determinant tables on every semicircle are nonzero and have unambiguous principal phase increments (not a proof between samples or on other sheets)",
    )

    upper_end = np.asarray(upper_small["paths"][1]["end_center"])
    lower_end = np.asarray(lower_small["paths"][1]["end_center"])
    upper_complex = upper_end[:, 0] + 1.0j * upper_end[:, 1]
    lower_complex = lower_end[:, 0] + 1.0j * lower_end[:, 1]
    audit.numerical(
        "P36.BVP.CW_CCW_conjugate_sampled_regular_roots",
        np.linalg.norm(lower_complex - np.conjugate(upper_complex)) < 2e-10
        and upper_small["paths"][1]["min_sampled_sigma_Bv"] > 0.05
        and lower_small["paths"][1]["min_sampled_sigma_Bv"] > 0.05,
        "the CW/U and CCW/L continuations of the tracked BVP root are distinct conjugate solutions with nonzero sampled endpoint blocks; both local root-sheet laterals survive the recorded gates",
    )

    return {
        "boundary": boundary.tolist(),
        "fold": {
            "T_c": fold_time,
            "center": fold_center.tolist(),
            "right_null_oriented": right_null.tolist(),
        },
        "Phase36_recomputed_sheet_using_Phase25_solver_and_seed": {
            "center": recorded_center.tolist(),
            "physical_soft": recorded_soft,
            "incoming_label": "I_plus_tracked_Ai",
        },
        "BVP_root_basis": {
            "incoming_order": ["I_minus_physical_soft", "I_plus_tracked_Ai"],
            "outgoing_order": ["O_minus_Im_soft", "O_plus_Im_soft"],
            "upper_T_CW_root_map": [[0, 1], [1, 0]],
            "lower_T_CCW_root_map": [[1, 0], [0, 1]],
            "warning": "these analytic root permutations are not the Gauss-Manin contour matrix G or an intersection coefficient",
        },
        "radius_records": radius_records,
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P36",
        "calculation": "declared local Airy contour-basis identities with prescribed-complex-T BVP lateral tests",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_exact_declared_local_Airy_contour_basis_identities_are_fixed": "SUPPORTED_IN_THE_SEPARATELY_ORDERED_LATERAL_BASES",
            "the_tracked_real_Ai_root_has_regular_CW_U_and_CCW_L_continuations": "SUPPORTED_ON_THREE_FINITE_SEMICIRCLE_RADII",
            "Phase32_below_origin_plus_Phase35_relative_det_transport_is_by_itself_sufficient_to_select_U_over_L": "CONTRADICTED_WITHIN_THE_RECORDED_LOCAL_GATES_BOTH_ROOT_SHEET_LATERALS_SURVIVE",
            "one_common_incoming_upward_dual_was_transported_through_both_laterals": "OPEN_NOT_COMPUTED_THE_TWO_FIRST_DUALS_BELONG_TO_DIFFERENT_LATERALIZED_BASES",
            "the_absolute_determinant_signs_epsilon_U_L_are_fixed": "OPEN_REQUIRES_ORIENTED_ORIGINAL_CYCLE_AND_REGULATOR",
            "the_regular_hard_determinant_quotient_and_CFU_Airy_Airy_prime_coefficients_are_constructed": "OPEN_THE_CONDITIONAL_SOFT_FACTOR_BOOKKEEPING_DOES_NOT_DERIVE_THEM",
            "one_lateral_is_selected_by_a_complete_original_relative_cycle": "OPEN_NOT_COMPUTED",
            "the_global_PL_intersection_coefficient_n_sigma_is_fixed": "OPEN_REQUIRES_ALL_JOINT_DUALS_GOOD_ENDS_AND_ORIENTATIONS",
            "a_full_BFV_SUGRA_or_physical_quantum_state_is_obtained": "OPEN_OUT_OF_SCOPE",
        },
        "scope_guard": {
            "computed": [
                "the exact three-ray Airy contour relation and Ai/Bi-to-arm matrix",
                "the algebra of the separately ordered CW and CCW cycle bases and their inverse-transpose dual bases",
                "the fact that the first dual vectors in those two lateralized bases are different basis elements, not transport of one common dual",
                "the enhanced lateral Stokes matrices in one frozen convention",
                "declared leading-fold endpoint-determinant half-phase conventions with unresolved signs and finite-radius consistency tests",
                "twelve prescribed-complex-T BVP root paths on three shrinking semicircle radii",
                "the BVP-root permutation, action-gap winding, CFU coordinate fit, and sampled determinant phase",
            ],
            "not_computed": [
                "transport of one specified incoming physical upward dual or realization of the formal K_U and K_L cycles by the BVP roots",
                "a choice between the upper/CW and lower/CCW lateral continuations",
                "absolute determinant signs, unsampled zeros, other sheets, inhomogeneous modes, or good ends",
                "the regular hard determinant quotient and the even/odd CFU amplitudes needed by an absolute Airy/Airy-prime uniform kernel",
                "a full joint field-lapse flow or regularized BFV/SUGRA superdeterminant",
                "complete relative cycles, a global intersection coefficient, WDW state, initial-value peak, or SUSY scale",
            ],
        },
        "next_calculation": (
            "lift the complete declared original lapse-field relative cycle into the Airy chart, "
            "transport its regulated determinant orientation to all good ends, and only then pair it with every upward dual"
        ),
    }
    print("PHASE36_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
