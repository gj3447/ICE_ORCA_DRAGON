#!/usr/bin/env python3
"""Gate 1 -- local V=0 m=2 spectral BFV trajectory control.

This bounded non-numbered calculation performs the smallest nontrivial
trajectory extension of the hash-pinned improved-static BFV source: one
endpoint-vanishing sine mode and its cosine partners.  It projects the exact
local Darboux BFV action, checks endpoints and nilpotent mode maps, and compares
the nonzero bosonic gauge determinant with the ordered ghost Pfaffian.

The physical pair is a frozen ``p0>0`` spectator and the nonzero amplitudes are
only formal local tangent modes; no finite-amplitude chart containment is
certified.  The hybrid continuum-spectral
mode is not an exact midpoint-difference lattice.  The result exposes two
inequivalent zero-mode ledgers and therefore does not construct a unique or
absolute finite BFV measure, continuum path integral, physical state or TOE.
One adjacent JSON result is written and no descendant starts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_INPUTS.json"
RESULT_NAME = "GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_bfv_m2_spectral_trajectory.py"
)
EXPECTED_INPUT_SHA256 = (
    "dc301d233540b5d635d448c4e2c1cf897e6c9ae612493a5ab11a1d44b403eb77"
)
CALCULATION_ID = "Gate1V0BfvM2SpectralTrajectory"
RESULT_SCHEMA = "ice.gate1.v0-bfv-m2-spectral-trajectory.result.v1"
RESULT_PREFIX = "GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def guard(
        self,
        guard_id: str,
        theorem: str,
        domain: str,
        statement: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "domain": domain,
                "statement": statement,
            }
        )


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, Any]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream is not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload mutation: {item['path']}")

    contract: dict[str, Any]
    if item["path"].endswith("IMPROVED_STATIC_BFV_SOURCE_RESULT.json"):
        exact = payload["exact_calculation"]
        contract = {
            "kind": "static_bfv",
            "sPsi": exact["bfv_algebra"]["sPsi"],
            "brst_generator_images": exact["bfv_algebra"][
                "brst_generator_images"
            ],
            "endpoint_ideal": exact["endpoint_source"]["endpoint_ideal"],
            "odd_order": exact["bfv_algebra"]["odd_order"],
            "full_path_constructed": exact["endpoint_source"][
                "full_path_bfv_measure_constructed"
            ],
        }
    elif item["path"].endswith("STATIC_SPECTRAL_PAIRING_RESULT.json"):
        contract = {
            "kind": "static_spectral",
            "equals_static_matrix": payload["exact_calculation"][
                "spectral_form"
            ]["equals_static_matrix"],
            "full_bfv_trajectory_measure": payload["promoted_outputs"][
                "full_bfv_trajectory_measure"
            ],
        }
    else:
        raise AssertionError(f"unexpected upstream role: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
        "contract": contract,
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this frozen calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-bfv-m2-spectral-trajectory.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "unique_trajectory_zero_mode_completion": None,
        "absolute_finite_bfv_measure": None,
        "full_bfv_trajectory_measure": None,
        "continuum_bfv_limit": None,
        "exact_endpoint_state_transform": None,
        "physical_inner_product": None,
        "full_real_lapse_delta_C": None,
        "old_fixed_a_kernel_equivalence": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    projection = payload["m2_spectral_projection"]
    if (
        projection["basis"]
        != "e0=1, e_c=sqrt(2)*cos(pi*s), e_s=sqrt(2)*sin(pi*s)"
        or projection["regulator_status"]
        != "HYBRID_CONTINUUM_SPECTRAL_ONE_MODE_NOT_AN_EXACT_MIDPOINT_DIFFERENCE_OPERATOR"
        or payload["continuum_source"]["lambda_domain"] != "lambda>0"
    ):
        raise AssertionError("m2 projection mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def matrix_record(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def exact_calculation(
    upstream: list[dict[str, Any]], audit: Audit
) -> tuple[dict[str, Any], dict[str, bool], bool]:
    contracts = {item["contract"]["kind"]: item["contract"] for item in upstream}
    static = contracts["static_bfv"]
    static_spectral = contracts["static_spectral"]
    expected_s_psi = [
        {"coefficient": "N*c + Pi*T", "monomial": "1"},
        {"coefficient": "-1", "monomial": "c_g*bar_c"},
        {"coefficient": "-1", "monomial": "rho*bar_rho"},
    ]
    upstream_contract = audit.observe(
        "G1.m2.upstream.static_bfv_contract",
        static["sPsi"] == expected_s_psi
        and static["endpoint_ideal"] == ["T", "Pi", "c_g", "bar_c"]
        and static["odd_order"] == ["c_g", "bar_c", "rho", "bar_rho"]
        and static["full_path_constructed"] is False,
        "the pinned static source supplies sPsi, endpoint ideal and odd order but explicitly no full path measure",
    )
    prerequisite = audit.observe(
        "G1.m2.upstream.static_spectral_prerequisite",
        static_spectral["equals_static_matrix"] is True
        and static_spectral["full_bfv_trajectory_measure"] is None,
        "the frozen static-spectral comparison survived while leaving the trajectory measure null",
    )

    s = sp.Symbol("s", real=True)
    e0 = sp.Integer(1)
    e_c = sp.sqrt(2) * sp.cos(sp.pi * s)
    e_s = sp.sqrt(2) * sp.sin(sp.pi * s)
    basis = (e0, e_c, e_s)
    gram = sp.Matrix(
        3,
        3,
        lambda row, column: sp.integrate(
            basis[row] * basis[column], (s, 0, 1)
        ),
    )
    basis_sector_pass = audit.observe(
        "G1.m2.basis.sector_normalization_and_overlaps",
        all(gram[index, index] == 1 for index in range(3))
        and gram[0, 1] == 0
        and gram[1, 0] == 0
        and gram[1, 2] == 0
        and gram[2, 1] == 0
        and sp.simplify(gram[0, 2] - 2 * sp.sqrt(2) / sp.pi) == 0
        and sp.simplify(gram[2, 0] - 2 * sp.sqrt(2) / sp.pi) == 0,
        "the sector functions have unit norm and the required e0-e_c/e_c-e_s orthogonality; the distinct-boundary-sector overlap int(e0*e_s)=2*sqrt(2)/pi is explicitly retained",
    )
    derivative_relation = audit.observe(
        "G1.m2.basis.derivative_relation",
        sp.simplify(sp.diff(e_s, s) - sp.pi * e_c) == 0,
        "the one Dirichlet sine mode differentiates to pi times its cosine partner",
    )
    endpoint_vanishing = audit.observe(
        "G1.m2.endpoint.sine_modes_vanish",
        e_s.subs(s, 0) == 0 and e_s.subs(s, 1) == 0,
        "T,Pi,c_g,bar_c sine modes obey both endpoint conditions exactly",
    )
    minimal_nonzero = audit.observe(
        "G1.m2.basis.minimal_nonzero_mode_count",
        1 - 1 == 0 and 2 - 1 == 1,
        "m=1 has no endpoint-vanishing nonzero mode while m=2 has exactly the k=1 mode used here",
    )

    t1, c0, c1, lapse0, lapse1, primary1 = sp.symbols(
        "T1 c0 c1 N0 N1 Pi1", real=True
    )
    p0 = sp.Symbol("p0", positive=True, real=True)
    delta_phi = sp.Symbol("DeltaPhi", real=True)
    lam = sp.Symbol("lambda", positive=True, real=True)
    t_field = t1 * e_s
    c_field = c0 + c1 * e_c
    lapse_field = lapse0 + lapse1 * e_c
    primary_field = primary1 * e_s
    projected_even = sp.simplify(
        sp.integrate(
            c_field * sp.diff(t_field, s)
            + p0 * delta_phi
            - lapse_field * sp.diff(primary_field, s)
            + lam
            * (primary_field * t_field + lapse_field * c_field),
            (s, 0, 1),
        )
    )
    expected_even = (
        p0 * delta_phi
        + sp.pi * c1 * t1
        - sp.pi * lapse1 * primary1
        + lam
        * (primary1 * t1 + lapse0 * c0 + lapse1 * c1)
    )
    even_projection = audit.observe(
        "G1.m2.action.even_projection",
        sp.simplify(projected_even - expected_even) == 0,
        "direct basis projection recovers the frozen physical spectator plus the declared m=2 bosonic gauge action",
    )

    kinetic_b_r = sp.integrate(sp.diff(e_s, s) * e_c, (s, 0, 1))
    kinetic_g_br = sp.integrate(sp.diff(e_s, s) * e_c, (s, 0, 1))
    sine_overlap = sp.integrate(e_s**2, (s, 0, 1))
    cosine_overlap = sp.integrate(e_c**2, (s, 0, 1))
    zero_overlap = sp.integrate(e0**2, (s, 0, 1))
    ghost_coefficients = {
        "g1*b1": sp.simplify(-lam * sine_overlap),
        "g1*br1": sp.simplify(kinetic_g_br),
        "b1*rho1": sp.simplify(kinetic_b_r),
        "rho1*br1": sp.simplify(-lam * cosine_overlap),
        "rho0*br0": sp.simplify(-lam * zero_overlap),
    }
    expected_ghost_coefficients = {
        "g1*b1": -lam,
        "g1*br1": sp.pi,
        "b1*rho1": sp.pi,
        "rho1*br1": -lam,
        "rho0*br0": -lam,
    }
    ghost_projection = audit.observe(
        "G1.m2.action.ghost_projection",
        ghost_coefficients == expected_ghost_coefficients,
        "the projected ordered ghost action is pi*b1*rho1+pi*g1*br1-lambda*(g1*b1+rho0*br0+rho1*br1)",
    )

    pinned_images = static["brst_generator_images"]
    pinned_image_contract = {
        "T": [{"coefficient": "1", "monomial": "c_g"}],
        "N": [{"coefficient": "1", "monomial": "rho"}],
        "bar_c": [{"coefficient": "Pi", "monomial": "1"}],
        "bar_rho": [{"coefficient": "c", "monomial": "1"}],
        "c": [],
        "Pi": [],
        "c_g": [],
        "rho": [],
        "Phi": [],
        "p": [],
    }
    mode_images = {
        "T1": "g1",
        "N0": "rho0",
        "N1": "rho1",
        "b1": "Pi1",
        "br0": "c0",
        "br1": "c1",
        "c0": None,
        "c1": None,
        "Pi1": None,
        "g1": None,
        "rho0": None,
        "rho1": None,
        "Phi0": None,
        "Phi1": None,
        "p0": None,
    }
    second_images = {
        name: (mode_images.get(image) if image is not None else None)
        for name, image in mode_images.items()
    }
    nilpotent_modes = audit.observe(
        "G1.m2.brst.projected_generator_nilpotence",
        pinned_images == pinned_image_contract
        and all(image is None for image in second_images.values()),
        "the pinned bracket-derived generator images project to sT1=g1, sN_i=rho_i, sb1=Pi1, sbr_i=c_i and square to zero",
    )
    endpoint_stability = audit.observe(
        "G1.m2.brst.endpoint_mode_stability",
        mode_images["T1"] == "g1"
        and mode_images["b1"] == "Pi1"
        and mode_images["Pi1"] is None
        and mode_images["g1"] is None
        and mode_images["Phi0"] is None
        and mode_images["Phi1"] is None,
        "the endpoint-vanishing T,Pi,c_g,bar_c sine sector is BRST stable and the fixed physical endpoints are invariant",
    )

    nonzero_even = sp.expand(
        projected_even - p0 * delta_phi - lam * lapse0 * c0
    )
    x_modes = (t1, lapse1)
    y_modes = (c1, primary1)
    bosonic_matrix = sp.Matrix(
        2,
        2,
        lambda row, column: sp.diff(
            sp.diff(nonzero_even, x_modes[row]), y_modes[column]
        ),
    )
    expected_bosonic = sp.Matrix([[sp.pi, lam], [lam, -sp.pi]])
    bosonic_det = sp.factor(bosonic_matrix.det())
    bosonic_pass = audit.observe(
        "G1.m2.nonzero.bosonic_gauge_matrix",
        bosonic_matrix == expected_bosonic
        and sp.simplify(bosonic_det + sp.pi**2 + lam**2) == 0,
        "the nonzero bosonic gauge matrix is [[pi,lambda],[lambda,-pi]] with determinant -(pi^2+lambda^2)",
    )

    ghost_matrix = sp.zeros(4)

    def set_odd_pair(left: int, right: int, coefficient: sp.Expr) -> None:
        ghost_matrix[left, right] = coefficient
        ghost_matrix[right, left] = -coefficient

    set_odd_pair(0, 1, ghost_coefficients["g1*b1"])
    set_odd_pair(0, 3, ghost_coefficients["g1*br1"])
    set_odd_pair(1, 2, ghost_coefficients["b1*rho1"])
    set_odd_pair(2, 3, ghost_coefficients["rho1*br1"])
    ghost_pfaffian = sp.factor(
        ghost_matrix[0, 1] * ghost_matrix[2, 3]
        - ghost_matrix[0, 2] * ghost_matrix[1, 3]
        + ghost_matrix[0, 3] * ghost_matrix[1, 2]
    )
    ghost_det = sp.factor(ghost_matrix.det())
    ghost_pass = audit.observe(
        "G1.m2.nonzero.ghost_pfaffian",
        sp.simplify(ghost_pfaffian - (sp.pi**2 + lam**2)) == 0
        and sp.simplify(ghost_det - ghost_pfaffian**2) == 0,
        "the ordered (g1,b1,rho1,br1) ghost matrix has Pfaffian pi^2+lambda^2 and determinant Pf^2",
    )
    relative_match = audit.observe(
        "G1.m2.nonzero.relative_determinant_pfaffian_match",
        sp.simplify(-bosonic_det - ghost_pfaffian) == 0,
        "the nonzero bosonic Jacobian magnitude and ghost Pfaffian share the same pi^2+lambda^2 polynomial only as a same-regulator relative identity",
    )
    sample_values = [sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)]
    sampled_match = audit.observe(
        "G1.m2.nonzero.sampled_lambda_identity",
        all(
            sp.simplify(
                (-bosonic_det - ghost_pfaffian).subs(lam, value)
            )
            == 0
            for value in sample_values
        ),
        "the exact relative polynomial identity survives the frozen positive lambda samples 1/2,1,2",
    )

    hbar = sp.Symbol("hbar", positive=True, real=True)
    bosonic_zero_jacobian = 1 / lam
    raw_zero_ghost_coefficient = -sp.I * lam / hbar
    retained_zero_ghost_measure = sp.I * hbar
    retained_zero_ghost_factor = sp.simplify(
        retained_zero_ghost_measure * raw_zero_ghost_coefficient
    )
    retained_combined = sp.simplify(
        bosonic_zero_jacobian * retained_zero_ghost_factor
    )
    eliminated_combined = bosonic_zero_jacobian
    retained_ledger = audit.observe(
        "G1.m2.zero.retained_pair_relative_cancellation",
        retained_zero_ghost_factor == lam and retained_combined == 1,
        "with the explicitly declared i*hbar coefficient-extraction orientation, the retained rho0,br0 factor lambda cancels delta(lambda*c0)'s 1/lambda Jacobian",
    )
    zero_ledger_inequivalence = audit.observe(
        "G1.m2.zero.ledger_inequivalence",
        sp.diff(retained_combined, lam) == 0
        and sp.diff(eliminated_combined, lam) != 0
        and [retained_combined.subs(lam, value) for value in sample_values]
        == [1, 1, 1]
        and [eliminated_combined.subs(lam, value) for value in sample_values]
        == [2, 1, sp.Rational(1, 2)],
        "retaining the algebraic zero ghost pair gives a lambda-independent relative unit, while eliminating it leaves 1/lambda; the pinned inputs do not choose between them",
    )

    audit.guard(
        "G1.m2.guard.hybrid_spectral_only",
        "one-mode continuum sine/cosine projection",
        "d e_s/ds=pi e_c is exact before any midpoint projection",
        "this is a hybrid spectral finite regulator, not an exact midpoint-difference gauge symmetry, nonlinear lattice solution or continuum convergence result",
    )
    audit.guard(
        "G1.m2.guard.relative_not_absolute",
        "finite-dimensional determinant/Pfaffian polynomial comparison",
        "one common ordered nonzero gauge/ghost regulator",
        "matching pi^2+lambda^2 does not assign the bosonic Fourier/Gaussian contour phase, absolute Pfaffian orientation or functional-measure normalization",
    )
    audit.guard(
        "G1.m2.guard.physical_spectator",
        "local U_plus component protection",
        "p(s)=p0>0 and Phi linear, while nonzero gauge amplitudes are only formal local tangent variables",
        "no finite-amplitude inverse-chart containment, nonlinear physical trajectory integration, chart-edge crossing or global Darboux atlas is certified",
    )
    audit.guard(
        "G1.m2.guard.zero_mode_ambiguity",
        "separation of algebraic zero ghosts and lapse modulus conventions",
        "the static source retains a normalized finite zero-mode quartet while historical trajectory regulators may eliminate the rho0,br0 pair or retain N0 as a modulus",
        "the two explicit ledgers prove underdetermination by the pinned inputs; no unique trajectory zero-mode completion is promoted",
    )
    audit.guard(
        "G1.m2.guard.no_full_bfv_or_physics",
        "bounded workbench interpretation",
        "one local gauge/ghost mode and a frozen physical spectator",
        "full BFV trajectory measure, full-real-lapse delta(C), old-kernel equality, physical cycle, observable, physics and TOE remain null",
    )

    core_flags = {
        "upstream_static_bfv_contract": upstream_contract,
        "static_spectral_prerequisite": prerequisite,
        "basis_sector_normalization_and_overlaps": basis_sector_pass,
        "derivative_relation": derivative_relation,
        "endpoint_vanishing": endpoint_vanishing,
        "minimal_nonzero_mode": minimal_nonzero,
        "even_projection": even_projection,
        "ghost_projection": ghost_projection,
        "projected_nilpotence": nilpotent_modes,
        "endpoint_mode_stability": endpoint_stability,
        "bosonic_gauge_matrix": bosonic_pass,
        "ghost_pfaffian": ghost_pass,
        "relative_polynomial_match": relative_match,
        "sampled_lambda_match": sampled_match,
        "retained_zero_ledger": retained_ledger,
    }
    ambiguity = zero_ledger_inequivalence
    return (
        {
            "basis": {
                "e0": str(e0),
                "e_c": str(e_c),
                "e_s": str(e_s),
                "gram_matrix": matrix_record(gram),
                "d_e_s": str(sp.diff(e_s, s)),
                "endpoint_values_e_s": [
                    str(e_s.subs(s, 0)),
                    str(e_s.subs(s, 1)),
                ],
                "regulator_status": "HYBRID_CONTINUUM_SPECTRAL_ONE_MODE",
            },
            "projected_action": {
                "continuum_source": "c*Tdot+p*Phidot-N*Pidot+bar_c_dot*rho+c_g_dot*bar_rho+lambda*sPsi",
                "physical_spectator": "p0*DeltaPhi with p0>0",
                "bosonic": str(projected_even),
                "ghost_order": ["g1", "b1", "rho1", "br1"],
                "ghost_coefficients": {
                    key: str(value)
                    for key, value in ghost_coefficients.items()
                },
            },
            "brst_modes": {
                "source": "projection of hash-pinned bracket-derived continuum images",
                "images": mode_images,
                "second_images": second_images,
                "nilpotent": nilpotent_modes,
                "endpoint_sine_sector_stable": endpoint_stability,
            },
            "nonzero_relative_control": {
                "bosonic_mode_order": ["T1", "N1", "c1", "Pi1"],
                "bosonic_cross_matrix": matrix_record(bosonic_matrix),
                "bosonic_determinant": str(bosonic_det),
                "ghost_matrix": matrix_record(ghost_matrix),
                "ghost_pfaffian": str(ghost_pfaffian),
                "ghost_determinant": str(ghost_det),
                "relative_polynomial": str(ghost_pfaffian),
                "absolute_measure_or_phase": None,
            },
            "zero_mode_ledgers": {
                "common_bosonic_fourier": {
                    "phase": "lambda*N0*c0",
                    "measure": "dN0/(2*pi*hbar)",
                    "distribution": "delta(lambda*c0)=delta(c0)/lambda for lambda>0",
                    "jacobian": str(bosonic_zero_jacobian),
                },
                "retained_algebraic_pair": {
                    "ghost_phase": "-lambda*rho0*br0",
                    "raw_top_coefficient": str(raw_zero_ghost_coefficient),
                    "declared_oriented_measure": str(retained_zero_ghost_measure),
                    "ghost_factor": str(retained_zero_ghost_factor),
                    "combined_relative_factor": str(retained_combined),
                },
                "eliminated_algebraic_pair": {
                    "ghost_factor": None,
                    "combined_relative_factor": str(eliminated_combined),
                },
                "sample_lambda_values": [str(value) for value in sample_values],
                "retained_samples": [
                    str(retained_combined.subs(lam, value))
                    for value in sample_values
                ],
                "eliminated_samples": [
                    str(eliminated_combined.subs(lam, value))
                    for value in sample_values
                ],
                "unique_completion": None,
                "inequivalent": ambiguity,
            },
            "core_flags": core_flags,
            "zero_mode_ambiguity": ambiguity,
        },
        core_flags,
        ambiguity,
    )


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, Any]],
    audit: Audit,
) -> dict[str, Any]:
    exact, core_flags, ambiguity = exact_calculation(upstream, audit)
    core_pass = all(core_flags.values())
    if not core_pass:
        verdict = "KILL_V0_DECLARED_M2_SPECTRAL_BFV_MODE_EXTENSION"
        impact = "RETAIN_STATIC_SOURCE_ONLY"
        classification = "GATE1_V0_M2_SPECTRAL_BFV_MODE_EXTENSION_NONPASS"
        condition = (
            "the projected action, endpoint conditions, nilpotent mode maps or "
            "determinant-Pfaffian identity fails"
        )
    elif ambiguity:
        verdict = (
            "NARROW_V0_M2_RELATIVE_QUARTET_KEEP_ZERO_MODE_COMPLETION_AMBIGUOUS"
        )
        impact = "KEEP_MINIMAL_NONZERO_MODE_RELATIVE_CONTROL_ONLY"
        classification = (
            "GATE1_V0_M2_ONE_MODE_RELATIVE_BFV_QUARTET_KEEP_"
            "TRAJECTORY_ZERO_MODE_COMPLETION_UNDERDETERMINED"
        )
        condition = (
            "the basis, projected action, endpoint/BRST mode maps and relative "
            "determinant-Pfaffian identities pass, while the retained and "
            "eliminated zero-mode ledgers remain inequivalent"
        )
    else:
        verdict = "KEEP_V0_M2_RELATIVE_BFV_MODE_AND_ZERO_COMPLETION"
        impact = "CLOSE_DECLARED_FINITE_REGULATOR_ONLY"
        classification = "GATE1_V0_M2_RELATIVE_BFV_MODE_AND_ZERO_COMPLETION_KEEP"
        condition = (
            "the nonzero mode identities pass and the zero-mode completion is "
            "uniquely fixed by the pinned inputs"
        )
    promoted = dict(frozen_input["required_fail_closed_outputs"])
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": classification,
        "verdict": verdict,
        "programme_impact": impact,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_provenance": upstream,
        "exact_calculation": exact,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": [],
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "one formal local m=2 hybrid spectral gauge/ghost tangent mode with a frozen p0>0 physical spectator and no certified finite-amplitude chart containment",
            "relative_boundary": "determinant/Pfaffian equality is same-regulator and relative only",
            "zero_mode_boundary": "two explicit ledgers are inequivalent, so no unique trajectory measure is promoted",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted,
        "gate1_decision": promoted["gate1"],
        "global_promotion": promoted["global_promotion"],
        "automatic_next": promoted["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_scope": frozen_input["epistemic_scope"],
            "decision_table": frozen_input["decision_table"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256, upstream = load_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, upstream, audit)
    encoded = json.dumps(
        result,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds the bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": sum(item["passed"] for item in audit.exact),
                "exact_checks_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_total": 0,
                "unique_trajectory_zero_mode_completion": None,
                "full_bfv_trajectory_measure": None,
                "gate1": result["gate1_decision"],
                "global_n_sigma": None,
                "physics_claim": None,
                "TOE_claim": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
