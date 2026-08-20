#!/usr/bin/env python3
"""Phase 38 -- Gate-1 joint-cycle identifiability and bounded end ledger.

The ordered five-gate programme begins with a complete original joint
lapse--field relative cycle and its signed Picard--Lefschetz intersections.
Phases 28--37 do not yet contain that object.  They contain a projected
lapse-base crossing, bounded stationary-root continuations, a local Airy
cycle-basis map, root-cover monodromy, and a reduced bosonic half-form.

This executable makes the resulting information boundary testable.  Its
exact layer exhibits a noninjective declared finite surrogate (not the
physical relative-homology projection), uses the Phase-36 Gauss--Manin map
(not the root permutation) to transport cycle coefficients, and rejects a
global integer whenever an end or cycle orientation is missing.  Its
numerical layer stitches the known reduced real dual ledger and extends the
conjugate stationary-family arms from Re T=13 to Re T=16 with two
continuation step-size controls.

The result is a Gate-1 preflight and obstruction witness.  It does not solve
the full joint field--lapse gradient flow, classify every good end, orient a
BFV/Pfaffian line, select a physical original contour, or output a global
intersection coefficient.  The script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase32_below_origin_lapse_intersection as p32
    from . import phase34_directed_fold_dual_continuation as p34
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase32_below_origin_lapse_intersection as p32
    import phase34_directed_fold_dual_continuation as p34


EXTENSION_START_REAL_T = 13.0
EXTENSION_MAX_REAL_T = 16.0
COARSE_REAL_T_STEP = 0.25
FINE_REAL_T_STEP = 0.125
EXTENSION_RECORD_TIMES = (14.0, 15.0, 16.0)


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


def exact_matrix_payload(matrix: sp.MatrixBase) -> list[list[str]]:
    return [
        [str(sp.simplify(value)) for value in row]
        for row in matrix.tolist()
    ]


def global_integer_or_none(
    *,
    original_joint_cycle_complete: bool,
    all_upward_ends_classified: bool,
    orientation_line_fixed: bool,
    signed_local_points: tuple[int, ...],
) -> int | None:
    """Return a signed sum only after the three Gate-1 completeness guards."""

    if not (
        original_joint_cycle_complete
        and all_upward_ends_classified
        and orientation_line_fixed
    ):
        return None
    return sum(signed_local_points)


def exact_controls(audit: Audit) -> dict[str, object]:
    # A deliberately finite typed information-loss witness.  The coordinates
    # are (lapse projection, upper field-cycle component, lower field-cycle
    # component).  It is not asserted to be the complete relative homology.
    lapse_projection = sp.Matrix([[1, 0, 0]])
    projection_kernel = lapse_projection.nullspace()
    audit.exact(
        "P38.identifiability.surrogate_projection_has_kernel",
        lapse_projection.rank() == 1
        and len(projection_kernel) == 2
        and lapse_projection.shape == (1, 3),
        "the declared finite surrogate has a two-dimensional label kernel invisible to its lapse coordinate; this is not a theorem about physical relative homology",
    )

    surrogate_upper_label = sp.Matrix([1, 1, 0])
    surrogate_lower_label = sp.Matrix([1, 0, 1])
    audit.exact(
        "P38.identifiability.same_projection_distinct_surrogate_labels",
        lapse_projection * surrogate_upper_label == sp.Matrix([1])
        and lapse_projection * surrogate_lower_label == sp.Matrix([1])
        and surrogate_upper_label != surrogate_lower_label,
        "distinct labels in the declared surrogate share one lapse coordinate, showing why inverse reconstruction needs an independent injectivity theorem or physical completions",
    )

    projected_sign, omitted_cycle_orientation = sp.symbols(
        "epsilon_T epsilon_omitted_cycle", real=True
    )
    joint_sign = projected_sign * omitted_cycle_orientation
    possible_joint_signs = {
        sp.simplify(
            joint_sign.subs(
                {
                    projected_sign: 1,
                    omitted_cycle_orientation: omitted_sign,
                }
            )
        )
        for omitted_sign in (-1, 1)
    }
    audit.exact(
        "P38.orientation.projected_sign_does_not_fix_joint_sign",
        possible_joint_signs == {-1, 1},
        "even with projected lapse sign +1, an unresolved omitted-cycle orientation allows either full-joint local sign; no fermion/Pfaffian factor is folded into this PL integer",
    )

    gamma_u = sp.Matrix([1, 0])
    gamma_l = sp.Matrix([0, 1])
    gamma_0 = -gamma_u - gamma_l
    gauss_manin = sp.Matrix([[-1, -1], [0, 1]])
    root_swap = sp.Matrix([[0, 1], [1, 0]])
    audit.exact(
        "P38.cycles.local_three_ray_relation_and_basis_map",
        gamma_0 + gamma_l + gamma_u == sp.zeros(2, 1)
        and gauss_manin**2 == sp.eye(2),
        "the frozen local Airy cycles obey Gamma_0+Gamma_L+Gamma_U=0 and the Phase-36 ordered-basis map is involutive",
    )

    c_0, c_l = sp.symbols("c_0 c_L")
    c_in = sp.Matrix([c_0, c_l])
    c_out = gauss_manin.T * c_in
    audit.exact(
        "P38.cycles.coefficients_transform_by_transpose",
        c_out == sp.Matrix([-c_0, -c_0 + c_l]),
        "when Gamma_in=G Gamma_out, coefficients of the same chain transform as c_out=G^T c_in",
    )

    dual_map = gauss_manin.inv().T
    audit.exact(
        "P38.cycles.dual_inverse_transpose_preserves_pairing",
        dual_map == sp.Matrix([[-1, 0], [-1, 1]])
        and exact_zero(gauss_manin * dual_map.T - sp.eye(2)),
        "the upward dual basis uses G^(-T), and G (G^(-T))^T=I preserves the declared row-basis pairing",
    )

    conditional_gamma_0 = sp.Matrix([1, 0])
    true_conditional_output = gauss_manin.T * conditional_gamma_0
    root_mutant_output = root_swap * conditional_gamma_0
    audit.exact(
        "P38.mutation.root_swap_is_not_cycle_transport",
        true_conditional_output == sp.Matrix([-1, -1])
        and root_mutant_output == sp.Matrix([0, 1])
        and true_conditional_output != root_mutant_output,
        "for the conditional Gamma_0 input, G^T gives two arms (-1,-1), whereas the forbidden root-swap mutant fabricates a single arm",
    )

    audit.exact(
        "P38.cycles.orientation_reversal_flips_coefficients",
        gauss_manin.T * (-conditional_gamma_0)
        == -true_conditional_output,
        "reversing the original cycle orientation reverses every transported cycle coefficient",
    )

    audit.exact(
        "P38.intersection.pair_birth_preserves_signed_sum",
        sum((1, -1)) == 0 and sum((1, 1, -1)) == 1,
        "a transverse +1/-1 crossing-pair birth leaves the signed intersection sum unchanged",
    )

    arm_from_airy = sp.Matrix([[-1, -sp.I], [-1, sp.I]]) / 2
    c_u, c_lower = sp.symbols("c_U c_lower")
    arm_coefficients = sp.Matrix([c_u, c_lower])
    airy_bi_coefficients = arm_from_airy.T * arm_coefficients
    audit.exact(
        "P38.cycles.arm_to_Ai_Bi_coefficients",
        exact_zero(
            airy_bi_coefficients
            - sp.Matrix(
                [-(c_u + c_lower) / 2, sp.I * (c_lower - c_u) / 2]
            )
        ),
        "the Gate-1 arm vector fixes only its exact Ai/Bi combination, not the hard CFU Ai-prime coefficient",
    )

    # The first two coordinates are the Gate-1 arm data; A and B denote the
    # independent hard even/odd CFU functions required by Gate 2.
    gate1_to_arm_data = sp.Matrix(
        [[1, 0, 0, 0], [0, 1, 0, 0]]
    )
    audit.exact(
        "P38.gates.Gate1_record_schema_omits_hard_CFU_data",
        gate1_to_arm_data.rank() == 2
        and len(gate1_to_arm_data.nullspace()) == 2,
        "the declared Gate-1 output schema records arm data but omits the two hard CFU slots; this is bookkeeping, not a proof of physical independence",
    )

    incomplete_global = global_integer_or_none(
        original_joint_cycle_complete=False,
        all_upward_ends_classified=False,
        orientation_line_fixed=False,
        signed_local_points=(1,),
    )
    complete_toy_global = global_integer_or_none(
        original_joint_cycle_complete=True,
        all_upward_ends_classified=True,
        orientation_line_fixed=True,
        signed_local_points=(1, 1, -1),
    )
    audit.exact(
        "P38.guard.missing_completion_forces_null_global_integer",
        incomplete_global is None and complete_toy_global == 1,
        "the result API refuses a global integer until the joint cycle, every upward end, and the orientation line are complete",
    )

    positive_half_line_intersection: int | None = None
    audit.exact(
        "P38.guard.endpoint_contact_is_not_half_intersection",
        positive_half_line_intersection is None,
        "the positive lapse half-line endpoint contact remains unassigned rather than being counted as 0, 1/2, or +1",
    )

    cutoffs = (5, 9, 10, 11, 20, 40)
    bosonic_gauge_signs = tuple((-1) ** (cutoff - 1) for cutoff in cutoffs)
    audit.exact(
        "P38.guard.finite_BFV_bosonic_parity_is_not_absolute_orientation",
        bosonic_gauge_signs == (1, 1, -1, 1, -1, -1)
        and set(bosonic_gauge_signs) == {-1, 1},
        "the inherited nonzero-mode BFV bosonic sign alternates with cutoff parity and cannot supply an absolute continuum orientation line",
    )

    physical_claims = {
        "physical_projection_noninjective": False,
        "admissible_distinct_joint_completions_constructed": False,
        "original_joint_cycle_complete": False,
        "all_upward_ends_classified": False,
        "full_joint_local_sign_computed": False,
        "global_intersection_integer_computed": False,
        "hard_CFU_coefficients_computed": False,
        "full_BFV_Pfaffian_Pin_line_computed": False,
    }
    audit.exact(
        "P38.scope.semantic_claim_guards",
        not any(physical_claims.values()),
        "the executable keeps every uncomputed joint-cycle, global-intersection, hard-CFU, and BFV/Pfaffian claim false",
    )

    return {
        "typed_information_loss_witness": {
            "coordinate_order": [
                "lapse_projection",
                "upper_field_cycle",
                "lower_field_cycle",
            ],
            "projection_matrix": exact_matrix_payload(lapse_projection),
            "rank": int(lapse_projection.rank()),
            "nullity": len(projection_kernel),
            "scope": (
                "finite surrogate/schema witness only; not a computation of "
                "the physical projection map or relative-homology rank"
            ),
        },
        "local_cycle_transport": {
            "basis_equation": "Gamma_in=G Gamma_out",
            "G": exact_matrix_payload(gauss_manin),
            "coefficient_equation": "c_out=G^T c_in",
            "dual_equation": "K_in=G^(-T) K_out",
            "root_swap_P": exact_matrix_payload(root_swap),
            "conditional_Gamma0_input": ["1", "0"],
            "conditional_cycle_output": ["-1", "-1"],
            "forbidden_root_mutant_output": ["0", "1"],
            "conditional_warning": (
                "Phase 38 does not establish that the physical original "
                "cycle has input coefficients (1,0)"
            ),
        },
        "arm_to_Ai_Bi": {
            "Ai_coefficient": "-(c_U+c_L)/2",
            "Bi_coefficient": "I*(c_L-c_U)/2",
            "hard_CFU_A_and_B": None,
        },
        "global_integer_policy": {
            "requires": [
                "complete original joint cycle",
                "all upward ends and intersections classified",
                "fixed bosonic/gauge-reduced cycle orientation",
            ],
            "current_value": incomplete_global,
        },
        "finite_BFV_bosonic_cutoff_signs": {
            str(cutoff): sign
            for cutoff, sign in zip(cutoffs, bosonic_gauge_signs, strict=True)
        },
    }


def real_stationary_dual_ledger(
    boundary: np.ndarray, fold_time: float
) -> dict[str, object]:
    short_scan = p32.real_dual_scan()
    short_records = sorted(short_scan["records"], key=lambda item: item["r"])

    center = np.array([np.sqrt(3.0 / p25.potential(1.0)), 1.0])
    center, _endpoint = p25.solve_symmetric_center(0.1, boundary, center)
    bridge_records: list[dict[str, float]] = []
    for proper_time in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        center, endpoint = p25.solve_symmetric_center(
            proper_time, boundary, center
        )
        solution = p25.solve_fixed_time(
            proper_time, boundary, -endpoint[[1, 3]]
        )
        singular_values = np.linalg.svd(
            solution.velocity_monodromy, compute_uv=False
        )
        bridge_records.append(
            {
                "T": proper_time,
                "W_T": float(-solution.energy),
                "endpoint_residual": float(solution.endpoint_residual),
                "sigma_min_Bv": float(singular_values[-1]),
            }
        )

    post_saddle_records = p34.incoming_real_segment_control(
        boundary, fold_time
    )
    return {
        "short_origin_records": [
            {
                "T": float(record["r"]),
                "W_T": float(record["W_T"]),
                "endpoint_residual": float(record["endpoint_residual"]),
                "sigma_min_over_T": float(record["sigma_min_over_r"]),
            }
            for record in short_records
        ],
        "bridge_records": bridge_records,
        "post_saddle_records": post_saddle_records,
    }


def extend_stationary_arm(
    boundary: np.ndarray,
    fold: dict[str, object],
    right_null: np.ndarray,
    base_unknown: np.ndarray,
    *,
    step: float,
    collect_records: bool,
) -> dict[str, object]:
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    unknown = base_unknown.copy()
    current = EXTENSION_START_REAL_T
    max_root_residual = 0.0
    records: list[dict[str, object]] = []

    while EXTENSION_MAX_REAL_T - current > 1e-13:
        target = min(EXTENSION_MAX_REAL_T, current + step)
        unknown, residual = p34.solve_symmetric_constant_phase(
            target, boundary, unknown
        )
        max_root_residual = max(max_root_residual, residual)
        current = target
        if collect_records and any(
            abs(current - record_time) < 1e-12
            for record_time in EXTENSION_RECORD_TIMES
        ):
            records.append(
                p34.point_record(
                    current - fold_time,
                    fold_time,
                    fold_center,
                    right_null,
                    boundary,
                    unknown,
                    residual,
                )
            )

    return {
        "step": step,
        "max_root_residual": max_root_residual,
        "end_unknown": unknown,
        "records": records,
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, velocity, benchmark_action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    right_null = p34.deterministic_right_null(
        np.asarray(fold["right_null_vector"], dtype=float)
    )

    real_ledger = real_stationary_dual_ledger(boundary, fold_time)
    short_records = real_ledger["short_origin_records"]
    bridge_records = real_ledger["bridge_records"]
    post_saddle_records = real_ledger["post_saddle_records"]
    saddle_record = bridge_records[-1]

    audit.numerical(
        "P38.dual.real_stationary_ledger_stitches_at_saddle",
        all(record["W_T"] > 0.0 for record in short_records)
        and all(record["W_T"] > 0.0 for record in bridge_records[:-1])
        and abs(saddle_record["W_T"]) < 1e-10
        and all(record["W_T"] < 0.0 for record in post_saddle_records)
        and max(
            record["endpoint_residual"]
            for record in short_records + bridge_records + post_saddle_records
        )
        < 2e-8,
        "the sampled reduced real stationary ledger joins the origin-side branch to the T=.7 saddle and the post-saddle branch toward the fold",
    )

    audit.numerical(
        "P38.intersection.inherited_projected_crossing_is_stable_but_typed",
        len(short_records) == len(p32.RADII)
        and all(record["W_T"] > 0.0 for record in short_records)
        and all(record["sigma_min_over_T"] > 0.99 for record in short_records),
        "seven regulated lower-bypass locations retain the inherited positive transverse lapse-base crossing, explicitly typed as projected rather than joint",
    )

    seed = p34.p33_seed_data(boundary, fold, right_null)
    phase34_records = p34.continue_upper_arm(
        boundary, fold, right_null, seed
    )
    base_unknown = p34.unknown_from_record(phase34_records[-1])
    coarse = extend_stationary_arm(
        boundary,
        fold,
        right_null,
        base_unknown,
        step=COARSE_REAL_T_STEP,
        collect_records=True,
    )
    fine = extend_stationary_arm(
        boundary,
        fold,
        right_null,
        base_unknown,
        step=FINE_REAL_T_STEP,
        collect_records=False,
    )
    extension_records = coarse["records"]
    endpoint_difference = float(
        np.linalg.norm(coarse["end_unknown"] - fine["end_unknown"])
    )

    audit.numerical(
        "P38.continuation.coarse_fine_stationary_arm_extension",
        endpoint_difference < 1e-10
        and coarse["max_root_residual"] < 5e-8
        and fine["max_root_residual"] < 5e-8
        and len(extension_records) == len(EXTENSION_RECORD_TIMES),
        "two continuation step sizes converge to the same tracked upper stationary-family root/basin at Re T=16; this is not an integration-mesh convergence theorem",
    )

    audit.numerical(
        "P38.continuation.extended_BVP_and_Jacobi_controls",
        max(record["root_residual"] for record in extension_records) < 5e-8
        and max(
            record["full_endpoint_residual"]
            for record in extension_records
        )
        < 1e-6
        and min(record["sigma_min_Bv"] for record in extension_records) > 8.0
        and max(record["conjugation_residual"] for record in extension_records)
        < 2e-9,
        "three new upper checkpoints and their real-coefficient conjugation controls pass the symmetric root, independently reintegrated full-endpoint, and sampled Jacobi gates through Re T=16",
    )

    all_arm_records = phase34_records + extension_records
    audit.numerical(
        "P38.intersection.bounded_arms_disjoint_from_original_lapse_base",
        min(record["T"][0] for record in all_arm_records) > fold_time
        and max(record["T"][0] for record in all_arm_records)
        <= EXTENSION_MAX_REAL_T + 1e-12
        and min(abs(complex(*record["T"])) for record in all_arm_records)
        > 9.0,
        "the sampled tracked conjugate outgoing lapse projections remain disjoint from the declared Phase-32 full-line imaginary-T base and origin caps through Re T=16",
    )

    # The box boundary is a numerical stopping surface, not a relative good
    # end.  This is intentionally what keeps the global integer null.
    end_ledger = {
        "origin_side": {
            "classification": "SINGULAR_ENDPOINT_UNRESOLVED",
            "reason": "the regulated crossing approaches N=T=0",
        },
        "upper_outgoing_at_ReT_16": {
            "classification": "BOX_EXIT_UNRESOLVED",
            "T": extension_records[-1]["T"],
        },
        "lower_outgoing_at_ReT_16": {
            "classification": "BOX_EXIT_UNRESOLVED",
            "T": extension_records[-1]["lower_T"],
        },
    }
    unclassified_end_count = sum(
        entry["classification"].endswith("UNRESOLVED")
        for entry in end_ledger.values()
    )
    audit.numerical(
        "P38.guard.box_exits_are_not_good_ends",
        unclassified_end_count == 3
        and global_integer_or_none(
            original_joint_cycle_complete=False,
            all_upward_ends_classified=False,
            orientation_line_fixed=False,
            signed_local_points=(1,),
        )
        is None,
        "the origin limit and both Re T=16 box exits remain unresolved ends, so the bounded census cannot emit a global coefficient",
    )

    return {
        "frozen_benchmark": {
            "boundary": boundary.tolist(),
            "velocity": velocity.tolist(),
            "W_star": benchmark_action,
            "T_star": 0.7,
            "T_c": fold_time,
        },
        "real_stationary_dual_ledger": real_ledger,
        "phase34_last_record": phase34_records[-1],
        "extension": {
            "start_ReT": EXTENSION_START_REAL_T,
            "max_ReT": EXTENSION_MAX_REAL_T,
            "coarse_step": COARSE_REAL_T_STEP,
            "fine_step": FINE_REAL_T_STEP,
            "coarse_max_root_residual": coarse["max_root_residual"],
            "fine_max_root_residual": fine["max_root_residual"],
            "coarse_fine_endpoint_unknown_difference": endpoint_difference,
            "records": extension_records,
            "scope": "bounded reduced stationary-family continuation only",
        },
        "end_ledger": end_ledger,
        "recorded_intersections": {
            "lower_full_line_projected_lapse_crossing_count": 1,
            "projected_coordinate_sign": 1,
            "full_joint_local_sign": None,
            "complete_global_signed_vector": None,
            "global_n_sigma": None,
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P38",
        "gate": "Gate 1 -- original joint cycle and signed global intersections",
        "calculation": (
            "exact joint-cycle identifiability audit plus bounded reduced-dual "
            "and unresolved-end ledger"
        ),
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "exact_controls": exact,
        "numerical_controls": numerical,
        "gate_status": {
            "Gate_1": "OPEN_PARTIAL_PROGRESS",
            "Gate_2": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_1_TYPED_OUTPUT",
            "Gate_3": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_2_TYPED_OUTPUT",
            "Gate_4": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_3_TYPED_OUTPUT",
            "Gate_5": "PHYSICAL_PROMOTION_DEPENDS_ON_GATE_4_TYPED_OUTPUT",
        },
        "claim_status": {
            "the_original_joint_cycle_is_identifiable_from_the_recorded_projected_and_local_data_without_an_injectivity_theorem_or_physical_completions": "NOT_ESTABLISHED_NONINJECTIVE_ONLY_IN_THE_DECLARED_FINITE_SURROGATE",
            "the_root_swap_matrix_can_replace_the_Gauss_Manin_cycle_map": "CONTRADICTED_BY_THE_EXACT_MUTATION",
            "the_known_reduced_conjugate_stationary_arms_add_a_projected_crossing_with_the_declared_Phase32_imaginary_T_base_at_the_sampled_points_through_ReT_16": "NOT_SEEN_ON_THE_BOUNDED_TRACKED_TABLE",
            "the_original_joint_lapse_field_momentum_gauge_relative_cycle_is_complete": "OPEN_NOT_COMPUTED",
            "the_full_joint_local_intersection_sign_is_fixed": "OPEN_FULL_CYCLE_TANGENT_AND_ORIENTATION_DATA_MISSING",
            "all_upward_components_sheets_and_good_ends_are_classified": "OPEN_BOX_AND_SINGULAR_ENDS_UNRESOLVED",
            "the_global_signed_intersection_vector_or_n_sigma_is_fixed": "OPEN_AND_EXPLICITLY_NULL_IN_THE_RESULT_API",
            "the_conditional_Gamma0_input_would_continue_as_two_cycle_arms": "SUPPORTED_EXACTLY_BUT_THE_PHYSICAL_Gamma0_INPUT_IS_NOT_SELECTED",
            "hard_CFU_Airy_and_Airy_prime_coefficients_are_computed": "OPEN_GATE_2_NOT_COMPUTED",
            "a_full_BFV_Pfaffian_Pin_line_or_spinorial_charge_is_computed": "OPEN_GATES_3_AND_4_NOT_COMPUTED",
        },
        "scope_guard": {
            "computed": [
                "a finite exact surrogate showing that the recorded lapse coordinate does not by itself license inverse reconstruction of joint-cycle data",
                "the exact Phase-36 cycle coefficient and inverse-transpose dual transformations",
                "a mutation that distinguishes root permutation from cycle transport",
                "the exact conditional arm-to-Ai/Bi coefficient map",
                "the sampled real stationary-dual ledger from the origin regulator through the T=.7 saddle toward the fold",
                "two-step-size bounded continuation of the tracked conjugate stationary-family arms from ReT=13 to ReT=16",
                "an explicit unresolved-end ledger that prevents a global integer output",
            ],
            "not_computed": [
                "a fully specified original lapse-field-momentum-gauge relative cycle",
                "the exact discrete joint saddle, full joint gradient flow, or its transported tangent frame",
                "a signed full-joint local intersection determinant",
                "all complex sheets, upward components, Stokes jumps, singular divisors, or asymptotic good ends",
                "a regulator/cutoff-stable global Picard-Lefschetz integer",
                "hard CFU Ai/Ai-prime coefficients",
                "the full boson-fermion-ghost BFV/Pfaffian/Pin line, physical charge, order parameter, or pole splitting",
            ],
        },
        "next_calculation": (
            "construct one explicit finite-cutoff holomorphic joint action, "
            "re-solve its discrete saddle and fiber fold, embed the separately "
            "specified lower and upper original cycles, and transport full "
            "joint tangent frames to certified local intersections"
        ),
    }
    print("PHASE38_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
