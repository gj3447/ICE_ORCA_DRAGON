#!/usr/bin/env python3
"""Phase 37 -- closed simple-fold root and reduced half-form holonomy.

The exact layer keeps root sheets, Airy solutions, relative cycles, Stokes
data, and a conditional boson/fermion sheet-intertwiner witness as distinct
typed objects.  The numerical layer continues both Phase-33 BVP roots around
the same closed complex-proper-time loop, returning to one fixed basepoint.
It then lifts the sampled reduced endpoint determinant continuously instead
of resetting a principal square root on each sample.

This calculation can detect a local root-cover permutation and a sampled
reduced determinant half-form holonomy.  It does not identify either object
with a physical relative cycle, a spacetime Pin lift, a fermion Pfaffian, a
BFV cohomology class, a conserved supercharge, or a quantum state.  The
script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase33_fold_airy_uniformization as p33
    from . import phase34_directed_fold_dual_continuation as p34
    from . import phase36_airy_gauss_manin_connection as p36
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase33_fold_airy_uniformization as p33
    import phase34_directed_fold_dual_continuation as p34
    import phase36_airy_gauss_manin_connection as p36


RADIUS_CONFIGS = ((2.0e-4, 49), (1.0e-3, 49), (5.0e-3, 65))
DETERMINANT_SAMPLE_COUNT = 13
REFINEMENT_POINT_COUNT = 25
NONENCLOSING_POINT_COUNT = 33
DIRECT_TWO_TURN_POINT_COUNT = 97


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


def exact_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(sp.simplify(entry) == 0 for entry in value)
    return sp.simplify(value) == 0


def pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def matrix_pairs(matrix: np.ndarray) -> list[list[list[float]]]:
    return [[pair(complex(value)) for value in row] for row in matrix]


def exact_matrix_payload(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.simplify(value)) for value in row] for row in matrix.tolist()]


def exact_invariants(matrix: sp.MatrixBase) -> dict[str, object]:
    lam = sp.Symbol("lambda")
    return {
        "trace": str(sp.simplify(matrix.trace())),
        "determinant": str(sp.simplify(matrix.det())),
        "characteristic_polynomial": str(
            sp.factor(matrix.charpoly(lam).as_expr())
        ),
        "square": exact_matrix_payload(sp.simplify(matrix**2)),
        "fourth_power": exact_matrix_payload(sp.simplify(matrix**4)),
    }


def exact_controls(audit: Audit) -> dict[str, object]:
    identity = sp.eye(2)
    root_swap = sp.Matrix([[0, 1], [1, 0]])
    airy_solution_monodromy = identity
    gauss_manin = sp.Matrix([[-1, -1], [0, 1]])
    stokes_down = sp.Matrix([[1, 0], [1, 1]])
    half_form_ccw = sp.Matrix([[0, 1], [-1, 0]])
    half_form_cw = half_form_ccw.inv()

    audit.exact(
        "P37.root_cover.closed_loop_swap",
        root_swap**2 == identity
        and root_swap.trace() == 0
        and root_swap.det() == -1,
        "the u^2=z root local system exchanges its two roots after one enclosing loop and returns after two",
    )

    z = sp.Symbol("z")
    loop_factor = sp.exp(2 * sp.pi * sp.I)
    audit.exact(
        "P37.Airy.full_solution_is_single_valued",
        sp.simplify(loop_factor - 1) == 0
        and sp.simplify(sp.airyai(loop_factor * z) - sp.airyai(z)) == 0
        and sp.simplify(sp.airybi(loop_factor * z) - sp.airybi(z)) == 0
        and airy_solution_monodromy == identity,
        "Ai and Bi are single-valued at the ordinary point z=0, so root exchange is not full Airy-solution monodromy",
    )

    audit.exact(
        "P37.detline.closed_half_form_lift",
        half_form_ccw.trace() == 0
        and half_form_ccw.det() == 1
        and half_form_ccw**2 == -identity
        and half_form_ccw**4 == identity,
        "the declared canonical representative of a continuously lifted soft inverse square root has order four: one loop exchanges roots and two loops give the central sign -I",
    )
    audit.exact(
        "P37.detline.reverse_loop_is_inverse",
        half_form_cw * half_form_ccw == identity
        and half_form_ccw * half_form_cw == identity
        and half_form_cw == -half_form_ccw,
        "reversing the oriented loop inverts the half-form transport",
    )

    u, v = sp.symbols("u v", nonzero=True)
    rephase = sp.diag(u, v)
    rephased = sp.simplify(rephase * half_form_ccw * rephase.inv())
    audit.exact(
        "P37.detline.constant_rephasing_conjugacy",
        sp.simplify(rephased.trace()) == half_form_ccw.trace()
        and sp.simplify(rephased.det()) == half_form_ccw.det()
        and exact_zero(rephased**2 + identity)
        and rephased.charpoly().as_expr()
        == half_form_ccw.charpoly().as_expr(),
        "constant sheet rephasing changes raw off-diagonal entries only by conjugation and preserves trace, determinant, characteristic polynomial, and the central square",
    )

    principal_reset_mutant = root_swap
    audit.exact(
        "P37.mutation.principal_reset_loses_central_sign",
        principal_reset_mutant**2 == identity
        and half_form_ccw**2 == -identity
        and principal_reset_mutant**2 != half_form_ccw**2,
        "resetting a principal square root at each sample collapses the half-form lift to the root permutation and incorrectly loses the two-turn sign",
    )

    change = sp.Matrix([[1, 0], [-1, -1]])
    audit.exact(
        "P37.types.conjugate_matrices_need_not_be_same_object",
        change * root_swap * change.inv() == gauss_manin
        and root_swap != gauss_manin
        and root_swap != stokes_down
        and gauss_manin != stokes_down,
        "P and the Phase-36 Gauss-Manin G are conjugate as matrices but remain different typed maps; the unipotent Stokes map is different again",
    )

    epsilon_u, epsilon_l = sp.symbols("epsilon_U epsilon_L")
    open_lateral_lift = (
        sp.I * sp.diag(epsilon_u, epsilon_l) * root_swap
    )
    audit.exact(
        "P37.open_laterals.independent_signs_do_not_fix_closed_lift",
        exact_zero(
            open_lateral_lift**2
            + epsilon_u * epsilon_l * identity
        )
        and sp.simplify(open_lateral_lift.det() - epsilon_u * epsilon_l)
        == 0
        and (open_lateral_lift.subs({epsilon_u: 1, epsilon_l: 1})) ** 2
        == -identity
        and (open_lateral_lift.subs({epsilon_u: 1, epsilon_l: -1})) ** 2
        == identity,
        "independently reset open-lateral signs allow both order-four and order-two matrices, which is why a single connected closed-loop lift is extra information",
    )

    nonenclosing_root = identity
    nonenclosing_half_form = identity
    audit.exact(
        "P37.control.nonenclosing_loop_is_trivial",
        nonenclosing_root == identity and nonenclosing_half_form == identity,
        "the local winding-zero control has neither root exchange nor half-form phase",
    )

    contour_candidates = sp.Matrix.hstack(
        sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1])
    )
    audit.exact(
        "P37.scope.monodromy_does_not_choose_contour_vector",
        contour_candidates.rank() == 2
        and half_form_ccw.eigenvals() == {sp.I: 1, -sp.I: 1},
        "the local monodromy has two eigendirections and supplies no physical relative-cycle vector or intersection coefficient",
    )

    # Phase-17 negative control: a bare root swap commutes with the
    # parity-controlled basis change that maps local to exchange charges.
    fermion_parity = sp.diag(1, -1)
    even_projector = (identity + fermion_parity) / 2
    odd_projector = (identity - fermion_parity) / 2
    lowering = sp.Matrix([[0, 1], [0, 0]])
    controlled_change = sp.kronecker_product(
        identity, even_projector
    ) + sp.kronecker_product(root_swap, odd_projector)
    local_charge = sp.kronecker_product(identity, lowering)
    exchange_charge = sp.kronecker_product(root_swap, lowering)
    common_root_holonomy = sp.kronecker_product(root_swap, identity)
    audit.exact(
        "P37.Phase17.root_swap_does_not_break_basis_equivalence",
        controlled_change.H * controlled_change == sp.eye(4)
        and controlled_change * local_charge * controlled_change.H
        == exchange_charge
        and exact_zero(
            controlled_change * common_root_holonomy
            - common_root_holonomy * controlled_change
        ),
        "a common root-swap holonomy preserves the Phase-17 parity-controlled equivalence between local and sheet-exchange charge matrices",
    )

    sheet_sign = sp.diag(1, -1)
    anchored_source = sp.kronecker_product(sheet_sign, identity)
    transformed_source = sp.simplify(
        controlled_change * anchored_source * controlled_change.H
    )
    audit.exact(
        "P37.conditional.physical_sheet_anchor_can_forbid_change",
        transformed_source
        == sp.kronecker_product(sheet_sign, fermion_parity)
        and transformed_source != anchored_source,
        "if an independently physical sheet-localized source is supplied, the Phase-17 basis change moves it and is no longer an allowed passive relabeling",
    )

    a, b, c, d = sp.symbols("a b c d")
    generic_q = sp.Matrix([[a, b], [c, d]])
    q_x = root_swap
    eta_values = {
        "+1": sp.Integer(1),
        "-1": sp.Integer(-1),
        "+i": sp.I,
        "-i": -sp.I,
    }
    intertwiner_records: dict[str, dict[str, object]] = {}
    expected_nullities = {"+1": 2, "-1": 2, "+i": 0, "-i": 0}
    expected_candidate_nullities = {"+1": 2, "-1": 0, "+i": 0, "-i": 0}
    candidate_a, candidate_b = sp.symbols("candidate_a candidate_b")
    candidate_q = candidate_a * identity + candidate_b * root_swap
    for name, eta in eta_values.items():
        obstruction = sp.simplify(eta * root_swap * generic_q - generic_q * root_swap)
        coefficient_map = obstruction.reshape(4, 1).jacobian([a, b, c, d])
        nullity = 4 - coefficient_map.rank()
        candidate_obstruction = sp.simplify(
            eta * root_swap * candidate_q - candidate_q * root_swap
        )
        candidate_map = candidate_obstruction.reshape(4, 1).jacobian(
            [candidate_a, candidate_b]
        )
        candidate_nullity = 2 - candidate_map.rank()
        q_x_obstruction = sp.simplify(
            eta * root_swap * q_x - q_x * root_swap
        )
        intertwiner_records[name] = {
            "eta": str(eta),
            "declared_QX_compatible": exact_zero(q_x_obstruction),
            "declared_candidate_subspace_dimension": candidate_nullity,
            "unrestricted_sheet_intertwiner_dimension": nullity,
            "coefficient_map_rank": coefficient_map.rank(),
        }

    audit.exact(
        "P37.intertwiner.specific_QX_classification",
        [
            intertwiner_records[name]["declared_QX_compatible"]
            for name in ("+1", "-1", "+i", "-i")
        ]
        == [True, False, False, False],
        "for the declared toy H_B=P, H_F=eta P, the specific Q_X=P sheet map intertwines only eta=+1",
    )
    audit.exact(
        "P37.intertwiner.full_and_candidate_nullities",
        all(
            record["unrestricted_sheet_intertwiner_dimension"]
            == expected_nullities[name]
            and record["declared_candidate_subspace_dimension"]
            == expected_candidate_nullities[name]
            for name, record in intertwiner_records.items()
        ),
        "the exact toy nullities separate the declared span{I,P} from all 2x2 sheet intertwiners; neither count is a physical supercharge count",
    )

    anticommuting_z = sheet_sign
    anticommuting_j = half_form_ccw
    audit.exact(
        "P37.intertwiner.specific_failure_is_not_total_no_go",
        exact_zero(-root_swap * anticommuting_z - anticommuting_z * root_swap)
        and exact_zero(
            -root_swap * anticommuting_j - anticommuting_j * root_swap
        ),
        "at eta=-1 the declared Q_X=P fails while two other sheet intertwiners survive, so a specific-Q obstruction is not a total no-go",
    )

    pfaffian_parameter = sp.Symbol("p", nonzero=True)
    antisymmetric_plus = sp.Matrix(
        [[0, pfaffian_parameter], [-pfaffian_parameter, 0]]
    )
    antisymmetric_minus = -antisymmetric_plus
    audit.exact(
        "P37.guard.pfaffian_sign_not_recovered_from_determinant",
        antisymmetric_plus.det() == antisymmetric_minus.det()
        and antisymmetric_plus[0, 1] == -antisymmetric_minus[0, 1],
        "two antisymmetric matrices can have the same determinant and opposite Pfaffians, so the reduced bosonic determinant does not compute a fermion Pfaffian sign",
    )

    reduced_block = sp.Matrix([[1]])
    full_operator_with_gauge_zero = sp.diag(1, 0)
    audit.exact(
        "P37.guard.reduced_block_does_not_fix_full_BFV_operator",
        reduced_block.det() == 1
        and full_operator_with_gauge_zero.det() == 0,
        "a nonzero reduced block can coexist with a zero mode of the full operator and therefore cannot establish BFV nondegeneracy or a quantum master equation",
    )

    physical_claim_guards = {
        "physical_contour_selected": False,
        "absolute_maslov_orientation_fixed": False,
        "pfaffian_phase_computed": False,
        "full_BFV_superdeterminant_computed": False,
        "upper_or_lower_lateral_physically_selected": False,
        "conserved_spinorial_supercharge_constructed": False,
        "physical_state_constructed": False,
    }
    audit.exact(
        "P37.scope.semantic_claim_guards",
        not any(physical_claim_guards.values()),
        "the executable keeps every uncomputed physical selection, Pfaffian/BFV, supercharge, and state claim false",
    )

    return {
        "typed_spaces": {
            "root_sheet": "two local BVP stationary-root sheets",
            "airy_solution": "the exact (Ai,Bi) solution space",
            "relative_cycle": "the separately declared Phase-36 contour-chain space",
            "soft_half_form": "the conditional reduced d^(-1/2) lift",
            "boson_fermion_sheet_fibers": "finite conditional intertwiner witness only",
        },
        "typed_matrices": {
            "root_sheet_monodromy_P": exact_matrix_payload(root_swap),
            "Airy_solution_monodromy": exact_matrix_payload(
                airy_solution_monodromy
            ),
            "Phase36_Gauss_Manin_cycle_map": exact_matrix_payload(
                gauss_manin
            ),
            "Phase36_Stokes_down": exact_matrix_payload(stokes_down),
            "conditional_canonical_soft_half_form_CCW": exact_matrix_payload(
                half_form_ccw
            ),
            "conditional_canonical_soft_half_form_CW": exact_matrix_payload(
                half_form_cw
            ),
        },
        "conjugacy_invariants": {
            "root_sheet_P": exact_invariants(root_swap),
            "Gauss_Manin_G": exact_invariants(gauss_manin),
            "Stokes_down": exact_invariants(stokes_down),
            "conditional_canonical_soft_half_form_CCW": exact_invariants(
                half_form_ccw
            ),
        },
        "conditional_intertwiner_table": intertwiner_records,
        "physical_claim_guards": physical_claim_guards,
    }


def determinant_indices(point_count: int) -> np.ndarray:
    return np.unique(
        np.rint(
            np.linspace(0, point_count - 1, DETERMINANT_SAMPLE_COUNT)
        ).astype(int)
    )


def continue_closed_loop(
    start_center: np.ndarray,
    loop_center: complex,
    radius: float,
    point_count: int,
    boundary: np.ndarray,
    fold_center: np.ndarray,
    right_null: np.ndarray,
    turn_count: int = 1,
    secant_predictor: bool = False,
) -> tuple[list[dict[str, object]], float]:
    angles = np.linspace(
        np.pi, np.pi + 2.0 * np.pi * turn_count, point_count
    )
    first_time = loop_center - radius
    center = np.asarray(start_center, dtype=np.complex128)
    records = [
        p36.light_record(
            first_time, center, boundary, fold_center, right_null
        )
    ]
    max_root_residual = 0.0
    previous_center: np.ndarray | None = None
    for angle in angles[1:]:
        proper_length = loop_center + radius * np.exp(1.0j * angle)
        guess = center
        if secant_predictor and previous_center is not None:
            guess = center + (center - previous_center)
        solved_center, residual = p36.solve_prescribed_center(
            proper_length, boundary, guess
        )
        previous_center = center
        center = solved_center
        max_root_residual = max(max_root_residual, residual)
        records.append(
            p36.light_record(
                proper_length, center, boundary, fold_center, right_null
            )
        )

    for index in determinant_indices(point_count):
        records[index] = p36.add_determinant_data(records[index], boundary)
    return records, max_root_residual


def path_metrics(
    records: list[dict[str, object]],
    root_residual: float,
) -> dict[str, object]:
    selected = determinant_indices(len(records))
    determinant_values = np.array(
        [complex(records[index]["determinant"]) for index in selected]
    )
    determinant_phases, determinant_increments = p36.unwrap_phase(
        determinant_values
    )
    soft_values = np.array(
        [complex(records[index]["soft"]) for index in selected]
    )
    soft_phases, soft_increments = p36.unwrap_phase(soft_values)
    hard_values = determinant_values / soft_values
    hard_phases, hard_increments = p36.unwrap_phase(hard_values)
    centers = np.array(
        [np.asarray(record["center"], dtype=np.complex128) for record in records]
    )
    steps = np.linalg.norm(np.diff(centers, axis=0), axis=1)
    return {
        "start_center": [pair(complex(value)) for value in centers[0]],
        "end_center": [pair(complex(value)) for value in centers[-1]],
        "start_soft": pair(soft_values[0]),
        "end_soft": pair(soft_values[-1]),
        "start_determinant": pair(determinant_values[0]),
        "end_determinant": pair(determinant_values[-1]),
        "determinant_phase_rotation": float(
            determinant_phases[-1] - determinant_phases[0]
        ),
        "soft_phase_rotation": float(soft_phases[-1] - soft_phases[0]),
        "sampled_hard_quotient_phase_rotation": float(
            hard_phases[-1] - hard_phases[0]
        ),
        "max_sampled_determinant_phase_increment": float(
            max(abs(determinant_increments))
        ),
        "max_sampled_soft_phase_increment": float(max(abs(soft_increments))),
        "max_sampled_hard_phase_increment": float(max(abs(hard_increments))),
        "min_sampled_sigma_Bv": float(
            min(float(records[index]["sigma_min"]) for index in selected)
        ),
        "min_sampled_abs_hard_quotient": float(min(abs(hard_values))),
        "max_full_endpoint_residual": float(
            max(
                float(records[index]["full_endpoint_residual"])
                for index in selected
            )
        ),
        "max_root_residual": float(root_residual),
        "max_center_step": float(max(steps)),
        "determinant_sample_count": int(len(selected)),
    }


def principal_inverse_sqrt(value: complex) -> complex:
    phase = float(np.angle(value))
    return complex(np.exp(-0.5 * (np.log(abs(value)) + 1.0j * phase)))


def transport_coefficient(
    path: dict[str, object], destination_start_determinant: complex
) -> complex:
    end_determinant = complex(*path["end_determinant"])
    end_phase = float(np.angle(complex(*path["start_determinant"]))) + float(
        path["determinant_phase_rotation"]
    )
    transported = np.exp(
        -0.5 * (np.log(abs(end_determinant)) + 1.0j * end_phase)
    )
    reference = principal_inverse_sqrt(destination_start_determinant)
    return complex(transported / reference)


def loop_pair_summary(
    paths: list[list[dict[str, object]]],
    root_residuals: list[float],
) -> dict[str, object]:
    metrics = [
        path_metrics(records, residual)
        for records, residual in zip(paths, root_residuals, strict=True)
    ]
    start_centers = [
        np.asarray(records[0]["center"], dtype=np.complex128)
        for records in paths
    ]
    end_centers = [
        np.asarray(records[-1]["center"], dtype=np.complex128)
        for records in paths
    ]
    endpoint_swap_errors = [
        float(np.linalg.norm(end_centers[index] - start_centers[1 - index]))
        for index in (0, 1)
    ]
    separations = [
        float(
            np.linalg.norm(
                np.asarray(paths[0][index]["center"])
                - np.asarray(paths[1][index]["center"])
            )
        )
        for index in range(len(paths[0]))
    ]
    start_determinants = [
        complex(*metric["start_determinant"]) for metric in metrics
    ]
    lift = np.zeros((2, 2), dtype=np.complex128)
    for source in (0, 1):
        destination = 1 - source
        lift[destination, source] = transport_coefficient(
            metrics[source], start_determinants[destination]
        )

    combined_det_rotation = sum(
        float(metric["determinant_phase_rotation"]) for metric in metrics
    )
    combined_soft_rotation = sum(
        float(metric["soft_phase_rotation"]) for metric in metrics
    )
    combined_hard_rotation = sum(
        float(metric["sampled_hard_quotient_phase_rotation"])
        for metric in metrics
    )
    return {
        "paths": metrics,
        "root_sheet_monodromy": [[0, 1], [1, 0]],
        "endpoint_swap_errors": endpoint_swap_errors,
        "min_root_separation": float(min(separations)),
        "max_step_over_min_root_separation": float(
            max(float(metric["max_center_step"]) for metric in metrics)
            / min(separations)
        ),
        "reduced_half_form_lift": matrix_pairs(lift),
        "lift_trace": pair(complex(np.trace(lift))),
        "lift_determinant": pair(complex(np.linalg.det(lift))),
        "lift_square_plus_identity_norm": float(
            np.linalg.norm(lift @ lift + np.eye(2))
        ),
        "lift_fourth_minus_identity_norm": float(
            np.linalg.norm(np.linalg.matrix_power(lift, 4) - np.eye(2))
        ),
        "combined_two_turn_determinant_phase_rotation": combined_det_rotation,
        "combined_two_turn_soft_phase_rotation": combined_soft_rotation,
        "combined_two_turn_sampled_hard_phase_rotation": combined_hard_rotation,
        "combined_two_turn_inverse_sqrt_phase": pair(
            complex(np.exp(-0.5j * combined_det_rotation))
        ),
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, _velocity, _action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    right_null = p34.deterministic_right_null(
        np.asarray(fold["right_null_vector"], dtype=float)
    )

    radius_records: list[dict[str, object]] = []
    raw_paths: list[list[list[dict[str, object]]]] = []
    for radius, point_count in RADIUS_CONFIGS:
        real_branches = p33.solve_two_branches(boundary, fold, radius)
        centers = [
            np.asarray(branch["center"], dtype=np.complex128)
            for branch in real_branches
        ]
        paths: list[list[dict[str, object]]] = []
        residuals: list[float] = []
        for center in centers:
            records, residual = continue_closed_loop(
                center,
                complex(fold_time),
                radius,
                point_count,
                boundary,
                fold_center,
                right_null,
            )
            paths.append(records)
            residuals.append(residual)
        summary = loop_pair_summary(paths, residuals)
        summary.update(
            {
                "radius": radius,
                "point_count_per_path": point_count,
                "incoming_root_order": ["soft_minus", "soft_plus"],
            }
        )
        radius_records.append(summary)
        raw_paths.append(paths)

    audit.numerical(
        "P37.BVP.closed_loop_root_swap_three_radii",
        max(
            max(record["endpoint_swap_errors"]) for record in radius_records
        )
        < 3e-8,
        "both BVP roots exchange at one fixed basepoint after one enclosing loop on each of three finite radii",
    )

    audit.numerical(
        "P37.BVP.residual_and_continuity_gates",
        max(
            path["max_root_residual"]
            for record in radius_records
            for path in record["paths"]
        )
        < 3e-10
        and max(
            path["max_full_endpoint_residual"]
            for record in radius_records
            for path in record["paths"]
        )
        < 9e-8
        and max(
            record["max_step_over_min_root_separation"]
            for record in radius_records
        )
        < 0.09,
        "all six enclosing paths pass the half-BVP, independently reintegrated sampled endpoint, and continuous-nearest-root step gates",
    )

    audit.numerical(
        "P37.detline.sampled_nonzero_phase_lifts",
        min(
            path["min_sampled_sigma_Bv"]
            for record in radius_records
            for path in record["paths"]
        )
        > 0.04
        and min(
            path["min_sampled_abs_hard_quotient"]
            for record in radius_records
            for path in record["paths"]
        )
        > 1.0
        and max(
            path["max_sampled_determinant_phase_increment"]
            for record in radius_records
            for path in record["paths"]
        )
        < 0.4,
        "the thirteen sampled endpoint blocks per path are nonzero and support a minimal-jump sampled determinant phase lift, conditional on no unresolved intersample winding or zero",
    )

    audit.numerical(
        "P37.detline.closed_lift_conjugacy_class",
        max(record["lift_square_plus_identity_norm"] for record in radius_records)
        < 2e-6
        and max(
            record["lift_fourth_minus_identity_norm"]
            for record in radius_records
        )
        < 4e-6
        and max(
            abs(complex(*record["lift_trace"])) for record in radius_records
        )
        < 2e-6
        and max(
            abs(complex(*record["lift_determinant"]) - 1.0)
            for record in radius_records
        )
        < 2e-6,
        "conditional on the minimal-jump sampled phase with no unresolved intersample winding, the reduced half-form has tr L=0, det L=1, L^2=-I, and L^4=I on all three loops",
    )

    two_pi = 2.0 * np.pi
    audit.numerical(
        "P37.detline.two_turn_soft_origin_of_central_sign",
        max(
            abs(
                abs(record["combined_two_turn_determinant_phase_rotation"])
                - two_pi
            )
            for record in radius_records
        )
        < 2e-6
        and max(
            abs(
                abs(record["combined_two_turn_soft_phase_rotation"])
                - two_pi
            )
            for record in radius_records
        )
        < 2e-6
        and max(
            abs(record["combined_two_turn_sampled_hard_phase_rotation"])
            for record in radius_records
        )
        < 2e-6
        and max(
            abs(
                complex(
                    *record["combined_two_turn_inverse_sqrt_phase"]
                )
                + 1.0
            )
            for record in radius_records
        )
        < 2e-6,
        "on the minimal-jump sampled lift over the two-sheet return path, the determinant and soft coordinate wind once, d/soft has zero net phase, and the inverse square root acquires -1",
    )

    # Coarse/fine control at the smallest enclosing radius.  The fine path is
    # already present as the positive-soft path in radius_records[0].
    smallest_radius = RADIUS_CONFIGS[0][0]
    smallest_branches = p33.solve_two_branches(
        boundary, fold, smallest_radius
    )
    coarse_records, coarse_residual = continue_closed_loop(
        np.asarray(smallest_branches[1]["center"], dtype=np.complex128),
        complex(fold_time),
        smallest_radius,
        REFINEMENT_POINT_COUNT,
        boundary,
        fold_center,
        right_null,
    )
    coarse_metrics = path_metrics(coarse_records, coarse_residual)
    fine_metrics = radius_records[0]["paths"][1]
    coarse_end = np.array(
        [complex(*value) for value in coarse_metrics["end_center"]]
    )
    fine_end = np.array(
        [complex(*value) for value in fine_metrics["end_center"]]
    )
    audit.numerical(
        "P37.mesh.coarse_fine_closed_path_stability",
        np.linalg.norm(coarse_end - fine_end) < 3e-9
        and abs(
            coarse_metrics["determinant_phase_rotation"]
            - fine_metrics["determinant_phase_rotation"]
        )
        < 2e-8
        and coarse_metrics["max_root_residual"] < 3e-10,
        "a 25-point and 49-point BVP continuation of the same enclosing root path agree at the endpoint and on their shared thirteen-angle determinant table; this is not determinant-sampling refinement",
    )

    # Direct 4pi control: unlike the stitched two-root summary above, this
    # path never resets the solver or determinant lift at the intermediate
    # return to the basepoint.
    direct_two_turn_records, direct_two_turn_residual = continue_closed_loop(
        np.asarray(smallest_branches[1]["center"], dtype=np.complex128),
        complex(fold_time),
        smallest_radius,
        DIRECT_TWO_TURN_POINT_COUNT,
        boundary,
        fold_center,
        right_null,
        turn_count=2,
        secant_predictor=True,
    )
    direct_two_turn_metrics = path_metrics(
        direct_two_turn_records, direct_two_turn_residual
    )
    direct_start = np.array(
        [
            complex(*value)
            for value in direct_two_turn_metrics["start_center"]
        ]
    )
    direct_end = np.array(
        [complex(*value) for value in direct_two_turn_metrics["end_center"]]
    )
    direct_two_turn_transport = transport_coefficient(
        direct_two_turn_metrics,
        complex(*direct_two_turn_metrics["start_determinant"]),
    )
    stitched_small = radius_records[0]
    audit.numerical(
        "P37.detline.direct_two_turn_matches_stitched_return",
        np.linalg.norm(direct_end - direct_start) < 3e-9
        and abs(
            direct_two_turn_metrics["determinant_phase_rotation"]
            - stitched_small[
                "combined_two_turn_determinant_phase_rotation"
            ]
        )
        < 2e-8
        and abs(
            direct_two_turn_metrics["soft_phase_rotation"]
            - stitched_small["combined_two_turn_soft_phase_rotation"]
        )
        < 2e-8
        and abs(
            direct_two_turn_metrics[
                "sampled_hard_quotient_phase_rotation"
            ]
            - stitched_small[
                "combined_two_turn_sampled_hard_phase_rotation"
            ]
        )
        < 2e-8
        and abs(direct_two_turn_transport + 1.0) < 2e-8
        and direct_two_turn_metrics[
            "max_sampled_determinant_phase_increment"
        ]
        < 0.7
        and direct_two_turn_metrics["max_root_residual"] < 3e-10,
        "one uninterrupted 4pi continuation returns the same root with inverse-square-root phase -1 and agrees with the independently stitched two-sheet return",
    )

    # Winding-zero numerical control: center a smaller circle strictly on
    # the real pre-fold side.  Its leftmost basepoint is T_c-5r.
    nonenclosing_radius = smallest_radius
    nonenclosing_offset = 5.0 * nonenclosing_radius
    nonenclosing_branches = p33.solve_two_branches(
        boundary, fold, nonenclosing_offset
    )
    nonenclosing_center = complex(
        fold_time - 4.0 * nonenclosing_radius
    )
    nonenclosing_records, nonenclosing_residual = continue_closed_loop(
        np.asarray(
            nonenclosing_branches[1]["center"], dtype=np.complex128
        ),
        nonenclosing_center,
        nonenclosing_radius,
        NONENCLOSING_POINT_COUNT,
        boundary,
        fold_center,
        right_null,
    )
    nonenclosing_metrics = path_metrics(
        nonenclosing_records, nonenclosing_residual
    )
    non_start = np.array(
        [complex(*value) for value in nonenclosing_metrics["start_center"]]
    )
    non_end = np.array(
        [complex(*value) for value in nonenclosing_metrics["end_center"]]
    )
    nonenclosing_transport = transport_coefficient(
        nonenclosing_metrics,
        complex(*nonenclosing_metrics["start_determinant"]),
    )
    audit.numerical(
        "P37.control.nonenclosing_BVP_loop_returns_identity",
        np.linalg.norm(non_end - non_start) < 3e-9
        and abs(nonenclosing_metrics["determinant_phase_rotation"]) < 2e-8
        and abs(nonenclosing_transport - 1.0) < 2e-8
        and nonenclosing_metrics["max_root_residual"] < 3e-10,
        "a nearby loop that does not enclose the fold returns the same BVP root and reduced inverse-square-root lift",
    )

    return {
        "boundary": boundary.tolist(),
        "fold": {
            "T_c": fold_time,
            "center": fold_center.tolist(),
            "right_null_oriented": right_null.tolist(),
        },
        "orientation": "T-loop counterclockwise from T_c-r; z=T_c-T also winds counterclockwise",
        "basepoint_half_form_reference": "principal Arg in (-pi,pi] is fixed once on each basepoint root; paths use unwrapped minimal-jump sample phases, and constant changes of the two fixed references act by conjugation",
        "radius_records": radius_records,
        "mesh_refinement": {
            "radius": smallest_radius,
            "coarse_point_count": REFINEMENT_POINT_COUNT,
            "fine_point_count": RADIUS_CONFIGS[0][1],
            "coarse_positive_soft_path": coarse_metrics,
            "fine_positive_soft_path": fine_metrics,
        },
        "direct_two_turn_control": {
            "radius": smallest_radius,
            "point_count": DIRECT_TWO_TURN_POINT_COUNT,
            "path": direct_two_turn_metrics,
            "inverse_sqrt_transport": pair(direct_two_turn_transport),
            "comparison": "uninterrupted 4pi path versus two independently solved 2pi sheet paths stitched at their matching basepoint roots",
        },
        "nonenclosing_control": {
            "loop_center": pair(nonenclosing_center),
            "radius": nonenclosing_radius,
            "point_count": NONENCLOSING_POINT_COUNT,
            "path": nonenclosing_metrics,
            "inverse_sqrt_transport": pair(nonenclosing_transport),
        },
        "sampling_warning": (
            "minimal-jump phase lifts from sampled nonzero endpoint blocks "
            "and d/soft quotients do not exclude zeros or alias winding "
            "between samples, on other sheets, or in omitted modes"
        ),
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P37",
        "calculation": (
            "typed exact monodromy/intertwiner audit plus same-basepoint "
            "closed BVP-root and sampled reduced-half-form transport"
        ),
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "exact_controls": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_local_BVP_root_cover_has_nontrivial_Z2_monodromy": "SUPPORTED_ON_THREE_SAMPLED_FINITE_LOOPS",
            "the_sampled_reduced_determinant_half_form_has_order_four_closed_loop_transport": "SUPPORTED_CONDITIONALLY_ON_THE_MINIMAL_JUMP_SAMPLED_NONZERO_LIFT_WITH_NO_UNRESOLVED_INTERSAMPLE_WINDING",
            "the_closed_loop_result_is_removed_by_constant_root_relabeling": "CONTRADICTED_FOR_THE_RECORDED_CONJUGACY_INVARIANTS",
            "root_monodromy_alone_breaks_the_Phase17_local_exchange_basis_equivalence": "CONTRADICTED_IN_THE_EXACT_FINITE_FIBER_CONTROL",
            "a_physical_sheet_anchor_is_present_in_the_current_model": "OPEN_NOT_SUPPLIED",
            "the_original_gravitational_relative_cycle_is_selected": "OPEN_NOT_COMPUTED",
            "the_reduced_bosonic_half_form_is_a_spacetime_Pin_or_fermion_Pfaffian_holonomy": "OPEN_NOT_COMPUTED_AND_NOT_IDENTIFIED",
            "a_global_conserved_spinorial_supercharge_or_SUGRA_constraint_is_constructed": "OPEN_NOT_COMPUTED",
            "the_full_BFV_superdeterminant_or_physical_state_is_constructed": "OPEN_NOT_COMPUTED",
        },
        "scope_guard": {
            "computed": [
                "exact typed distinctions among root, Airy-solution, cycle, Stokes, and soft-half-form matrices",
                "exact conjugacy invariants of declared canonical representatives and mutation controls for one local simple-fold model",
                "conditional finite sheet-holonomy intertwiner dimensions for four declared eta values",
                "six same-basepoint closed BVP-root paths on three finite enclosing radii",
                "sampled endpoint-determinant, soft-coordinate, and d/soft phase lifts",
                "one coarse/fine comparison, one uninterrupted two-turn return, and one nonenclosing-loop control",
            ],
            "not_computed": [
                "a proof excluding determinant/hard-quotient zeros or alias winding between samples, on other sheets, or in omitted modes",
                "the original lapse-field relative cycle, all good ends, or a global Picard-Lefschetz intersection coefficient",
                "the regular hard determinant and complete Airy/Airy-prime uniform kernel coefficients",
                "a spacetime Pin lift, fermion Pfaffian line, eta phase, or anomaly cancellation",
                "a full joint field-lapse BFV/SUGRA operator, cohomology, quantum master equation, or WDW state",
                "a conserved fermion-odd Lorentz-spinor supercharge, SUSY breaking order parameter, pole splitting, or SUSY scale",
            ],
        },
        "next_calculation": (
            "transport one regulated original lapse-field relative cycle from "
            "the origin prescription through the fold, compute its signed "
            "global intersections and hard CFU coefficients, then lift the "
            "selected saddle to the full BFV/SUGRA Pfaffian line"
        ),
    }
    print("PHASE37_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
