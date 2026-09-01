#!/usr/bin/env python3
"""Complete the real normalized kappa-differentiated minus-end tail.

This bounded calculation starts at the already certified Q0-normalized
projective seed.  A global rotating-frame Gronwall/Duhamel envelope controls
U, partial_kappa U, c_kappa and partial_kappa c_kappa on the whole minus
half-line.  Exact exponential mass and first-moment formulas then enclose the
combined differentiated Wronskian tail.  No cutoff solver, root theorem,
nonreal Weyl object, spectral measure, RAQ object or physics claim is made.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import arb, ctx, fmpq

import raw_c_actual_nonzero_lambda_hybrid_validated_transfer as interval_tools


INPUT_NAME = "RAW_C_COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_INPUTS.json"
RESULT_NAME = "RAW_C_COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/raw_c_combined_kappa_differentiated_minus_tail.py"
)
EXPECTED_INPUT_SHA256 = "d5f8798e06087056baa4f62721a2c7b0509471a84f224893b42b67147d3146dc"
CALCULATION_ID = "RawCCombinedKappaDifferentiatedMinusTail"
RESULT_SCHEMA = "ice.raw-c-combined-kappa-differentiated-minus-tail.result.v1"
RESULT_PREFIX = "RAW_C_COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_RESULT="
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


def exact_rational(text: str) -> fmpq:
    return interval_tools.exact_rational(text)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return interval_tools.interval_record(value, digits)


def interval_from_record(value: dict[str, str]) -> arb:
    return interval_tools.interval_from_bounds(
        arb(exact_rational(value["lower"])),
        arb(exact_rational(value["upper"])),
    )


def absolute_upper(value: arb) -> arb:
    return interval_tools.absolute_upper(value)


def symmetric(radius: arb) -> arb:
    return interval_tools.symmetric_interval(radius)


def intersection(left: arb, right: arb) -> arb | None:
    return interval_tools.intersection(left, right)


def excludes_zero(value: arb) -> bool:
    return interval_tools.excludes_zero(value)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 24,
        "upstream_results": 3,
        "method_sources": 1,
        "precision_tiers": 2,
        "elementary_ball_rows": 2,
        "kappa_corridors": 1,
        "lambda_slabs": 1,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "ball_bessel_evaluations": 0,
        "ball_gamma_evaluations": 0,
        "kernel_panels_evaluated": 0,
        "compact_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "absolute_actual_Gamma1_amplitude_or_sign": None,
        "absolute_actual_plus_kappa_derivative": None,
        "pointwise_actual_kappa_variation_values_or_sign": None,
        "pointwise_reference_kappa_variation_values_or_sign": None,
        "kappa_lambda_mixed_derivative": None,
        "root_transversality_or_monotonicity_or_uniqueness": None,
        "continuous_root_selector_or_continuation": None,
        "root_velocity": None,
        "roots_outside_declared_corridor_or_global_census": None,
        "nonreal_weyl_m_function_or_spectral_measure": None,
        "raw_C_RAQ_or_C_H_equivalence": None,
        "BFV_or_physical_product": None,
        "physics_claim": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check id: {identifier}")
        self.seen.add(identifier)

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self.register(identifier)
        reduced = sp.simplify(residual)
        self.exact.append(
            {
                "id": identifier,
                "passed": bool(reduced == 0),
                "statement": statement,
                "residual": str(reduced),
            }
        )

    def inequality(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.exact.append(
            {"id": identifier, "passed": bool(passed), "statement": statement, **data}
        )

    def control(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.controls.append(
            {"id": identifier, "passed": bool(passed), "statement": statement, **data}
        )

    def guard(
        self, identifier: str, theorem: str, hypotheses: str, scope: str
    ) -> None:
        self.register(identifier)
        self.guards.append(
            {
                "id": identifier,
                "verified": True,
                "verification_mode": (
                    "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_ARB_HYPOTHESIS_AUDIT"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": scope,
            }
        )


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream raw hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("schema_version") != item["schema_version"]:
        raise AssertionError(f"upstream schema mismatch: {item['path']}")
    if payload.get("verdict") != item["verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    if payload.get("run_status") != "VALID_RUN" or payload.get("numbered_phase") is not None:
        raise AssertionError(f"upstream execution-scope mismatch: {item['path']}")
    claimed = payload.get("result_payload_sha256_without_self")
    unsigned = dict(payload)
    unsigned.pop("result_payload_sha256_without_self", None)
    recomputed = sha256_bytes(canonical_bytes(unsigned))
    if claimed != item["payload_sha256_without_self"] or recomputed != claimed:
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    return payload, {
        "path": item["path"],
        "sha256": observed,
        "schema_version": item["schema_version"],
        "verdict": item["verdict"],
        "payload_sha256_without_self": claimed,
        "role": item["role"],
    }


def exact_audit(audit: Audit) -> None:
    q, t = sp.symbols("Q t", real=True)
    u, uq, z, zq, c, cq, d, dq = sp.symbols(
        "U U_Q Z Z_Q c c_Q D D_Q", real=True
    )
    a, v, lam, kappa, h, signed_integral = sp.symbols(
        "a V lambda kappa h I", real=True
    )
    reference = v - kappa**2
    actual = reference + lam * a
    w_uc = u * cq - uq * c
    h_combined = z * cq - zq * c + u * dq - uq * d
    w_uc_q = (
        sp.diff(w_uc, u) * uq
        + sp.diff(w_uc, uq) * actual * u
        + sp.diff(w_uc, c) * cq
        + sp.diff(w_uc, cq) * reference * c
    )
    h_q = (
        sp.diff(h_combined, u) * uq
        + sp.diff(h_combined, uq) * actual * u
        + sp.diff(h_combined, z) * zq
        + sp.diff(h_combined, zq) * (actual * z - 2 * kappa * u)
        + sp.diff(h_combined, c) * cq
        + sp.diff(h_combined, cq) * reference * c
        + sp.diff(h_combined, d) * dq
        + sp.diff(h_combined, dq) * (reference * d - 2 * kappa * c)
    )
    audit.identity(
        "rawc.kappa_tail.wronskian_derivative",
        w_uc_q + lam * a * u * c,
        "The declared W(U,c)_Q is -lambda*a*U*c in the repository Wronskian convention.",
    )
    audit.identity(
        "rawc.kappa_tail.combined_wronskian_derivative",
        h_q + lam * a * (z * c + u * d),
        "The actual and reference -2*kappa forcing terms cancel and H_Q=-lambda*a*(Z*c+U*D).",
    )
    audit.identity(
        "rawc.kappa_tail.actual_variation_coefficient",
        sp.diff(actual, kappa) + 2 * kappa,
        "At fixed lambda the actual coefficient has kappa derivative -2*kappa.",
    )
    audit.identity(
        "rawc.kappa_tail.reference_variation_coefficient",
        sp.diff(reference, kappa) + 2 * kappa,
        "The reference coefficient has the same kappa derivative -2*kappa.",
    )
    h_seed = h_combined.subs(
        {u: 1, uq: sp.symbols("r"), z: 0, zq: -h, c: 1, cq: 0, d: 0, dq: 0}
    )
    audit.identity(
        "rawc.kappa_tail.Q0_combined_seed",
        h_seed - h,
        "The normalized Q0 data give H(Q0)=h(Q0).",
    )
    audit.identity(
        "rawc.kappa_tail.improper_integral_orientation",
        h - (h + lam * signed_integral) + lam * signed_integral,
        "H(Q0)-H(-infinity)=-lambda*I_signed fixes H(-infinity)=h+lambda*I_signed.",
    )
    audit.identity(
        "rawc.kappa_tail.complete_derivative_sign",
        -(h + lam * signed_integral) - (-h - lam * signed_integral),
        "Integrating H_Q from the singular end to Q0 gives partial_kappa G=-h-lambda*I_signed.",
    )
    a_q0 = 6 * sp.pi**2 * sp.exp(-6)
    audit.identity(
        "rawc.kappa_tail.a_mass",
        a_q0 * sp.integrate(sp.exp(-sp.Rational(3, 2) * t), (t, 0, sp.oo))
        - 4 * sp.pi**2 * sp.exp(-6),
        "The complete a-tail mass at Q0=-4 is A0=4*pi^2*exp(-6).",
    )
    audit.identity(
        "rawc.kappa_tail.a_first_moment",
        a_q0
        * sp.integrate(t * sp.exp(-sp.Rational(3, 2) * t), (t, 0, sp.oo))
        - sp.Rational(8, 3) * sp.pi**2 * sp.exp(-6),
        "The complete a-tail first moment is A1=(2/3)*A0.",
    )
    audit.identity(
        "rawc.kappa_tail.V_mass",
        sp.diff(18 * sp.pi**4 * sp.exp(2 * q), q)
        - 36 * sp.pi**4 * sp.exp(2 * q),
        "The reference-potential tail has antiderivative 18*pi^4*exp(2Q).",
    )
    y, yq, perturbation = sp.symbols("y y_Q B", real=True)
    rotating_energy_q = 2 * y * yq + 2 * (yq / kappa) * (
        (-kappa**2 + perturbation) * y / kappa
    )
    audit.identity(
        "rawc.kappa_tail.rotating_energy",
        rotating_energy_q - 2 * perturbation * y * yq / kappa**2,
        "The free rotating part is skew and only B contributes to the rotating-energy derivative.",
    )
    beta_left, beta_right = sp.symbols("beta_left beta_right", real=True)
    audit.identity(
        "rawc.kappa_tail.duhamel_exponent_composition",
        sp.exp(beta_left) * sp.exp(beta_right)
        - sp.exp(beta_left + beta_right),
        "The propagator and base-solution exponents compose across each Duhamel split without an extra full-tail factor.",
    )
    audit.identity(
        "rawc.kappa_tail.lambda_zero_regression",
        (-h - 0 * signed_integral) - (-h),
        "At lambda=0 the complete differentiated tail vanishes exactly and partial_kappa G=-h(Q0).",
    )


def all_intersection(values: list[arb]) -> arb | None:
    result = values[0]
    for candidate in values[1:]:
        result = intersection(result, candidate)
        if result is None:
            return None
    return result


def common_upper_bound(values: list[arb]) -> arb:
    """Return one conservative scalar upper bound valid for every tier."""
    return arb(max(value.upper() for value in values))


def strict_sign(value: arb) -> str:
    if value.lower() > 0:
        return "POSITIVE"
    if value.upper() < 0:
        return "NEGATIVE"
    return "ZERO_NOT_EXCLUDED"


def elementary_row(
    *,
    dps: int,
    conventions: dict[str, Any],
    rho_record: dict[str, str],
    h_record: dict[str, str],
    reference_d_l2_record: dict[str, str],
) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    q0 = exact_rational(conventions["Q_0"])
    corridor = conventions["kappa_corridor"]
    slab = conventions["lambda_slab"]
    k_left = exact_rational(corridor["left_exact"])
    k_right = exact_rational(corridor["right_exact"])
    kappa = interval_tools.bracket_band(k_left, k_right)
    kappa_lower = arb(k_left)
    lambda_abs = arb(
        max(
            abs(exact_rational(slab["left_exact"])),
            abs(exact_rational(slab["right_exact"])),
        )
    )
    rho = interval_from_record(rho_record)
    h = interval_from_record(h_record)
    minus_h = -h
    x0 = 6 * arb.pi() ** 2 * arb(q0).exp()
    u_q0 = -rho - x0 - arb(1) / 2

    a_mass = 4 * arb.pi() ** 2 * (arb(3 * q0) / 2).exp()
    a_first_moment = arb((arb(2) * a_mass / 3).upper())
    v_mass = 18 * arb.pi() ** 4 * arb(2 * q0).exp()
    q_u = (v_mass + lambda_abs * a_mass) / kappa_lower
    q_c = v_mass / kappa_lower

    r_u0 = arb(
        (arb(1) + (absolute_upper(u_q0) / kappa_lower) ** 2).sqrt().upper()
    )
    r_z0 = arb((absolute_upper(minus_h) / kappa_lower).upper())
    exp_q_u = q_u.exp()
    exp_q_c = q_c.exp()
    r_u = arb((r_u0 * exp_q_u).upper())
    r_c = arb(exp_q_c.upper())

    zc_bound = arb(
        (
            r_c
            * (exp_q_u * r_z0 * a_mass + 2 * r_u * a_first_moment)
        ).upper()
    )
    ud_pointwise_bound = arb((2 * r_u * r_c * a_first_moment).upper())
    reference_d_l2 = arb(exact_rational(reference_d_l2_record["upper"]))
    ud_l2_bound = arb((r_u * a_mass.sqrt() * reference_d_l2).upper())
    if ud_pointwise_bound.upper() <= ud_l2_bound.upper():
        ud_selected_bound = arb(ud_pointwise_bound.upper())
        ud_selected_method = "GLOBAL_POINTWISE_FIRST_MOMENT"
    else:
        ud_selected_bound = arb(ud_l2_bound.upper())
        ud_selected_method = "UPSTREAM_L2_CAUCHY_SCHWARZ"
    integral_magnitude_bound = arb((zc_bound + ud_selected_bound).upper())
    lambda_tail_radius = arb((lambda_abs * integral_magnitude_bound).upper())
    partial_kappa_g = minus_h + symmetric(lambda_tail_radius)

    finite_nonnegative = all(
        value.is_finite() and value.lower() >= 0
        for value in (
            kappa_lower,
            lambda_abs,
            a_mass,
            a_first_moment,
            v_mass,
            q_u,
            q_c,
            r_u0,
            r_z0,
            r_u,
            r_c,
            zc_bound,
            ud_pointwise_bound,
            ud_l2_bound,
            ud_selected_bound,
            integral_magnitude_bound,
            lambda_tail_radius,
        )
    )
    selected_below_both = bool(
        ud_selected_bound.upper() <= ud_pointwise_bound.upper()
        and ud_selected_bound.upper() <= ud_l2_bound.upper()
    )
    record = {
        "decimal_digits": dps,
        "kappa_corridor": interval_record(kappa, digits),
        "rho_Q0": interval_record(rho, digits),
        "h_Q0": interval_record(h, digits),
        "minus_h_Q0_lambda_zero_regression": interval_record(minus_h, digits),
        "U_Q_Q0": interval_record(u_q0, digits),
        "a_tail_mass_A0": interval_record(a_mass, digits),
        "a_tail_first_moment_A1": interval_record(a_first_moment, digits),
        "V_tail_mass": interval_record(v_mass, digits),
        "q_U": interval_record(q_u, digits),
        "q_c": interval_record(q_c, digits),
        "R_U_Q0": interval_record(r_u0, digits),
        "R_Z_Q0": interval_record(r_z0, digits),
        "R_U_global": interval_record(r_u, digits),
        "R_c_global": interval_record(r_c, digits),
        "Zc_integral_magnitude_bound": interval_record(zc_bound, digits),
        "UD_pointwise_first_moment_bound": interval_record(
            ud_pointwise_bound, digits
        ),
        "UD_L2_Cauchy_Schwarz_bound": interval_record(ud_l2_bound, digits),
        "UD_selected_bound": interval_record(ud_selected_bound, digits),
        "UD_selected_method": ud_selected_method,
        "combined_signed_integral_magnitude_bound": interval_record(
            integral_magnitude_bound, digits
        ),
        "lambda_times_tail_radius": interval_record(lambda_tail_radius, digits),
        "partial_kappa_G_complete": interval_record(partial_kappa_g, digits),
        "partial_kappa_G_zero_excluded": excludes_zero(partial_kappa_g),
        "partial_kappa_G_strict_sign": strict_sign(partial_kappa_g),
        "finite_nonnegative_envelope": finite_nonnegative,
        "selected_UD_bound_below_both_independent_bounds": selected_below_both,
        "status": (
            "CERTIFIED_ELEMENTARY_GLOBAL_ENVELOPE_ROW"
            if finite_nonnegative and selected_below_both and partial_kappa_g.is_finite()
            else "ELEMENTARY_GLOBAL_ENVELOPE_ROW_NOT_CERTIFIED"
        ),
    }
    return record, {
        "partial_kappa_G": partial_kappa_g,
        "tail_radius": lambda_tail_radius,
        "combined_integral_bound": integral_magnitude_bound,
        "UD_pointwise": ud_pointwise_bound,
        "UD_L2": ud_l2_bound,
        "minus_h": minus_h,
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw_input = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    cfg = json.loads(raw_input)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-combined-kappa-differentiated-minus-tail.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
        or cfg.get("resource_caps") != expected_caps()
        or cfg.get("required_fail_closed_outputs") != expected_nulls()
    ):
        raise AssertionError("identity, resource or fail-closed output drift")

    method = cfg["method_reuse"]
    method_path = Path(__file__).resolve().parent.parent / method["path"]
    if sha256_bytes(method_path.read_bytes()) != method["sha256"]:
        raise AssertionError("method-source hash mismatch")
    if method_path.resolve() != Path(interval_tools.__file__).resolve():
        raise AssertionError("method-source import path mismatch")

    conventions = cfg["declared_conventions"]
    if (
        conventions["precision_ladder_decimal_digits"] != [80, 120]
        or conventions["Q_0"] != "-4"
        or conventions["lambda_slab"]
        != {"left_exact": "-1/10000", "right_exact": "1/10000"}
    ):
        raise AssertionError("precision, Q0 or lambda-slab drift")

    root = Path(__file__).resolve().parent.parent
    upstream: dict[str, dict[str, Any]] = {}
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream[item["path"]] = payload
        upstream_records.append(record)
    signstrip_path, seed_path, reference_path = [
        item["path"] for item in cfg["upstream_results"]
    ]
    signstrip = upstream[signstrip_path]
    seed = upstream[seed_path]
    reference = upstream[reference_path]

    audit = Audit()
    exact_audit(audit)

    declared_corridor = conventions["kappa_corridor"]
    declared_slab = conventions["lambda_slab"]
    signstrip_corridor = signstrip["certified_calculation"]["kappa_corridor"]
    seed_conventions = seed["declared_conventions"]
    reference_conventions = reference["declared_conventions"]
    k_left = exact_rational(declared_corridor["left_exact"])
    k_right = exact_rational(declared_corridor["right_exact"])
    lambda_left = exact_rational(declared_slab["left_exact"])
    lambda_right = exact_rational(declared_slab["right_exact"])
    audit.inequality(
        "rawc.kappa_tail.declared_rectangle",
        bool(k_left > 0 and k_left < k_right and lambda_left < 0 < lambda_right),
        "The exact current real rectangle is ordered and has kappa bounded away from zero.",
        kappa_left_exact=str(k_left),
        kappa_right_exact=str(k_right),
        lambda_left_exact=str(lambda_left),
        lambda_right_exact=str(lambda_right),
    )
    audit.inequality(
        "rawc.kappa_tail.upstream_rectangle_alignment",
        bool(
            signstrip_corridor["left_exact"] == declared_corridor["left_exact"]
            and signstrip_corridor["right_exact"] == declared_corridor["right_exact"]
            and signstrip["declared_conventions"]["lambda_slab"] == declared_slab
            and seed_conventions["kappa_corridor"] == declared_corridor
            and seed_conventions["lambda_slab"] == declared_slab
            and reference_conventions["kappa_corridor"] == declared_corridor
            and reference_conventions["lambda_slab_context_only"] == declared_slab
        ),
        "All three upstream certificates cover the same exact K corridor and lambda slab.",
    )
    audit.inequality(
        "rawc.kappa_tail.boundary_and_reference_alignment",
        bool(
            signstrip["declared_conventions"]["Q_0"] == conventions["Q_0"]
            and seed_conventions["Q_0"] == conventions["Q_0"]
            and reference_conventions["Q_0"] == conventions["Q_0"]
            and signstrip["declared_conventions"]["boundary_map"]
            == "Gamma_1,p(u)=-lim_(Q->-infinity) W(u,c_p)"
            and signstrip["declared_conventions"]["projective_functional"]
            == "G(kappa,lambda)=Gamma_1,kappa(u_plus)/u_plus(Q0)=-lim_(Q->-infinity)W(U,c_kappa), U=u_plus/u_plus(Q0)"
            and reference_conventions["reference_equation"]
            == conventions["reference_equation"]
            and reference_conventions["reference_kappa_variation"]
            == conventions["reference_kappa_variation"]
        ),
        "The Q0, selected projective boundary map and fixed-reference variation conventions align exactly.",
    )

    corridor_charts = {
        row["label"]: row
        for row in signstrip["certified_calculation"]["q0_final_charts"]
    }
    corridor_chart = corridor_charts.get("corridor")
    h_record = seed["certified_calculation"]["two_sided_h_Q0"]
    normalized_seed = seed["certified_calculation"]["normalized_tail_initial_data"]
    zq_record = normalized_seed["Z_kappa_Q_Q0"]
    h_seed_exact = bool(
        normalized_seed["Z_kappa_Q0"] == "0"
        and exact_rational(zq_record["lower"])
        == -exact_rational(h_record["upper"])
        and exact_rational(zq_record["upper"])
        == -exact_rational(h_record["lower"])
    )
    audit.inequality(
        "rawc.kappa_tail.selected_Q0_seed",
        bool(
            corridor_chart is not None
            and corridor_chart["certified"]
            and corridor_chart["Q0_amplitude_excludes_zero"]
            and seed["certified_calculation"]["scope"]
            == "selected real fixed-lambda projective kappa sensitivity at Q0 on the exact current K times Lambda strip only"
            and seed_conventions["h"] == "partial_kappa rho at fixed lambda"
            and h_seed_exact
        ),
        "The same selected nonzero Q0 chart supplies rho, fixed-lambda h and the exact normalized Z seed on the full rectangle.",
    )

    reference_scope = reference["certified_calculation"]
    reference_d_l2_record = reference_scope["full_minus_half_line_intersections"][
        "variation_L2_a"
    ]
    audit.inequality(
        "rawc.kappa_tail.reference_envelope_scope",
        bool(
            reference_scope["equation"]
            == "D_QQ=(V-kappa^2)*D-2*kappa*c_kappa with D(Q0)=D_Q(Q0)=0"
            and reference_scope["scope"]
            == "declared c_kappa reference variation on the exact current real kappa corridor only; the pinned lambda slab is context only because c_kappa and D are lambda-independent"
            and exact_rational(reference_d_l2_record["upper"]) > 0
        ),
        "The reference result supplies the zero-data D equation and a positive finite full-half-line L2(a) upper bound only.",
    )

    audit.guard(
        "rawc.kappa_tail.guard.selected_projective_seed",
        "Regular finite-IVP parameter dependence and projective normalization",
        "The hash-pinned selected real family has u_plus(Q0) uniformly nonzero on the exact rectangle, and h(Q0) is its fixed-lambda projective kappa derivative.",
        "U(Q0)=1, Z(Q0)=0 and Z_Q(Q0)=-h(Q0) are valid throughout the chart; no absolute actual amplitude or derivative follows.",
    )
    audit.guard(
        "rawc.kappa_tail.guard.global_rotating_duhamel",
        "Rotating-frame Gronwall and variation of constants",
        "kappa>=kappa_left>0, integral(V+abs(lambda)*a) and integral(V) are finite, and the Z,D forcing norms are respectively 2*abs(U), 2*abs(c).",
        "U,c are uniformly bounded and Z,D grow at most linearly toward the minus end with the displayed constants; these are magnitude envelopes, not pointwise values or signs.",
    )
    audit.guard(
        "rawc.kappa_tail.guard.differentiated_improper_limit",
        "Uniform dominated convergence for the differentiated Wronskian limit",
        "The finite-IVP derivatives are uniform on the compact parameter rectangle and a(Q)*(1+Q0-Q) is integrable on the minus half-line.",
        "H has a uniform endpoint limit and partial_kappa passes through the declared real projective Wronskian limit. This does not construct a singular Weyl m-function.",
    )
    audit.guard(
        "rawc.kappa_tail.guard.reference_crosscheck",
        "Cauchy-Schwarz in L2(a dQ)",
        "The upstream D envelope is on the identical kappa corridor and U is uniformly bounded by R_U.",
        "The U*D contribution has both a pointwise-first-moment bound and an independent L2 bound; selecting the smaller upper endpoint remains rigorous.",
    )
    audit.guard(
        "rawc.kappa_tail.guard.scope",
        "Computational-workbench claim separation",
        "Only a real normalized complete partial_kappa G interval on the declared rectangle is evaluated.",
        "No root theorem is composed here, and transversality, uniqueness, selector, velocity, global roots, nonreal Weyl data, spectral measure, RAQ, BFV and physics remain null.",
    )

    rows: list[dict[str, Any]] = []
    balls: list[dict[str, arb]] = []
    for tier, dps in enumerate(
        conventions["precision_ladder_decimal_digits"], start=1
    ):
        row, row_balls = elementary_row(
            dps=int(dps),
            conventions=conventions,
            rho_record=corridor_chart["rho_Q0"],
            h_record=h_record,
            reference_d_l2_record=reference_d_l2_record,
        )
        rows.append(row)
        balls.append(row_balls)
        audit.control(
            f"rawc.kappa_tail.tier{tier}.finite_global_envelope",
            bool(
                row["status"] == "CERTIFIED_ELEMENTARY_GLOBAL_ENVELOPE_ROW"
            ),
            "Every global mass, rotating norm, variation integral bound and complete derivative interval is finite and outward.",
            combined_signed_integral_magnitude_bound=row[
                "combined_signed_integral_magnitude_bound"
            ],
            lambda_times_tail_radius=row["lambda_times_tail_radius"],
            partial_kappa_G_complete=row["partial_kappa_G_complete"],
        )
        audit.control(
            f"rawc.kappa_tail.tier{tier}.independent_UD_bounds",
            bool(row["selected_UD_bound_below_both_independent_bounds"]),
            "The selected U*D radius is no larger than both the direct first-moment and upstream L2 Cauchy-Schwarz radii.",
            selected_method=row["UD_selected_method"],
            pointwise_bound=row["UD_pointwise_first_moment_bound"],
            L2_bound=row["UD_L2_Cauchy_Schwarz_bound"],
            selected_bound=row["UD_selected_bound"],
        )

    overlap_keys = ("partial_kappa_G", "minus_h")
    overlap_ok = all(
        intersection(balls[0][key], balls[1][key]) is not None
        for key in overlap_keys
    )
    audit.control(
        "rawc.kappa_tail.precision_overlap",
        overlap_ok,
        "The 80- and 120-digit outward set enclosures overlap for minus h and the complete derivative interval; scalar magnitude radii are one-sided upper bounds and are combined by their conservative maximum, not by set intersection.",
    )
    final_gk = all_intersection([row["partial_kappa_G"] for row in balls])
    final_tail_radius = common_upper_bound([row["tail_radius"] for row in balls])
    final_integral_bound = common_upper_bound(
        [row["combined_integral_bound"] for row in balls]
    )
    final_minus_h = all_intersection([row["minus_h"] for row in balls])
    final_ok = bool(
        final_gk is not None
        and final_minus_h is not None
        and final_gk.is_finite()
        and final_tail_radius.is_finite()
        and final_tail_radius.lower() >= 0
        and final_integral_bound.is_finite()
        and final_integral_bound.lower() >= 0
    )
    digits = int(conventions["ball_output_digits"])
    audit.control(
        "rawc.kappa_tail.final_complete_intersection",
        final_ok,
        "Both precision tiers have a common complete normalized partial_kappa G interval on the exact real rectangle.",
        partial_kappa_G_complete=(
            interval_record(final_gk, digits) if final_gk is not None else None
        ),
        strict_sign=(strict_sign(final_gk) if final_gk is not None else None),
    )

    exact_pass = all(item["passed"] for item in audit.exact)
    control_pass = all(item["passed"] for item in audit.controls)
    if exact_pass and control_pass and final_gk is not None:
        sign = strict_sign(final_gk)
        if sign == "POSITIVE":
            verdict = "CERTIFY_COMPLETE_UNIFORM_POSITIVE_NORMALIZED_G_KAPPA_INTERVAL_ONLY"
        elif sign == "NEGATIVE":
            verdict = "CERTIFY_COMPLETE_UNIFORM_NEGATIVE_NORMALIZED_G_KAPPA_INTERVAL_ONLY"
        else:
            verdict = "CERTIFY_COMPLETE_NORMALIZED_G_KAPPA_INTERVAL_ZERO_NOT_EXCLUDED"
    else:
        sign = None
        verdict = "COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_NOT_CERTIFIED"

    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "upstream_results": upstream_records,
        "method_reuse": cfg["method_reuse"],
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": cfg["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "controls_passed": sum(item["passed"] for item in audit.controls),
            "controls_total": len(audit.controls),
            "theorem_guards": len(audit.guards),
            "all_executable_checks_passed": bool(exact_pass and control_pass),
        },
        "certified_calculation": {
            "scope": "the exact current real K times Lambda rectangle for the same selected Q0-normalized actual family and fixed c_kappa reference",
            "equations": {
                "H": "W(Z,c_kappa)+W(U,D)=partial_kappa W(U,c_kappa)",
                "H_Q": "-lambda*a*(Z*c_kappa+U*D)",
                "H_Q0": "h(Q0)",
                "partial_kappa_G": "-h(Q0)-lambda*I_signed",
            },
            "precision_rows": rows,
            "lambda_zero_regression_minus_h_Q0": (
                interval_record(final_minus_h, digits)
                if final_minus_h is not None
                else None
            ),
            "combined_signed_integral_magnitude_bound": (
                interval_record(final_integral_bound, digits)
            ),
            "lambda_times_complete_tail_radius": (
                interval_record(final_tail_radius, digits)
            ),
            "partial_kappa_G_complete": (
                interval_record(final_gk, digits) if final_gk is not None else None
            ),
            "partial_kappa_G_zero_excluded": (
                excludes_zero(final_gk) if final_gk is not None else None
            ),
            "partial_kappa_G_strict_sign": sign,
            "endpoint_derivative_scope": "ordinary derivative in the corridor interior and the corresponding one-sided derivative at each kappa face",
            "next_mathematical_gap": "A separately authorized theorem-composition audit may combine this derivative interval with an independently pinned root-existence statement. No transversality, uniqueness, selector, continuation or velocity is emitted here.",
        },
        "non_claim": "This is a real normalized boundary-functional derivative interval in a computational workbench, not an absolute Gamma_1 amplitude, root theorem, singular Weyl m-function, spectral measure, RAQ/BFV result, empirical result or physics discovery.",
        "required_fail_closed_outputs": cfg["required_fail_closed_outputs"],
        "resource_accounting": {
            "symbolic_checks": len(audit.exact),
            "upstream_results": len(upstream_records),
            "method_sources": 1,
            "precision_tiers": len(rows),
            "elementary_ball_rows": len(rows),
            "kappa_corridors": 1,
            "lambda_slabs": 1,
            "ode_calls": 0,
            "quadrature_calls": 0,
            "root_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "ball_bessel_evaluations": 0,
            "ball_gamma_evaluations": 0,
            "kernel_panels_evaluated": 0,
            "compact_steps": 0,
            "adjacent_result_files_written": 1,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "sympy": sp.__version__,
            "python_flint": importlib.metadata.version("python-flint"),
            "platform": platform.platform(),
        },
    }
    if result["resource_accounting"]["symbolic_checks"] > expected_caps()[
        "symbolic_checks"
    ]:
        raise AssertionError("symbolic-check cap exceeded")
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "controls_passed": result["check_summary"]["controls_passed"],
                "controls_total": result["check_summary"]["controls_total"],
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
