#!/usr/bin/env python3
"""Node-safe four-state transfer of the Bessel-preconditioned switch data.

This runner deliberately ends at Q0=-4.  It transports the projective
direction rho=-v_Q/v-x-1/2 and its parameter derivative s=partial_lambda rho
through nodes by evolving (v,v_Q,w,w_Q), where w=partial_lambda v in the
gauge v(Q_switch)=1.  It does not evaluate Gamma_1 or a minus-tail.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq

# Reuse the already-audited interval primitives and, critically, the
# coefficient and whole-step-majorant convention.  This is an import, not a
# copy: any semantic change to that convention is visible to this runner.
import raw_c_actual_nonzero_lambda_hybrid_validated_transfer as hybrid


INPUT_NAME = "RAW_C_BESSEL_PRECONDITIONED_NODE_SAFE_SWITCH_TO_Q0_SENSITIVITY_TRANSFER_INPUTS.json"
RESULT_NAME = "RAW_C_BESSEL_PRECONDITIONED_NODE_SAFE_SWITCH_TO_Q0_SENSITIVITY_TRANSFER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_bessel_preconditioned_node_safe_switch_to_q0_sensitivity_transfer.py"
)
EXPECTED_INPUT_SHA256 = "b1668b5eb06eda2552ed519022932a70dbb3e54faadbe9bac9a5c4086d4d3762"
CALCULATION_ID = "RawCBesselPreconditionedNodeSafeSwitchToQ0SensitivityTransfer"
RESULT_SCHEMA = "ice.raw-c-bessel-preconditioned-node-safe-switch-to-q0-sensitivity-transfer.result.v1"
RESULT_PREFIX = "RAW_C_BESSEL_PRECONDITIONED_NODE_SAFE_SWITCH_TO_Q0_SENSITIVITY_TRANSFER_RESULT="
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
    return hybrid.exact_rational(text)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return hybrid.interval_record(value, digits)


def interval_from_record(value: dict[str, str]) -> arb:
    return hybrid.interval_from_bounds(
        arb(exact_rational(value["lower"])),
        arb(exact_rational(value["upper"])),
    )


def contains_zero(value: arb) -> bool:
    return hybrid.contains_zero(value)


def excludes_zero(value: arb) -> bool:
    return hybrid.excludes_zero(value)


def interval_width(value: arb) -> arb:
    return hybrid.interval_width(value)


def intersection(left: arb, right: arb) -> arb | None:
    return hybrid.intersection(left, right)


def expected_caps() -> dict[str, Any]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 512,
        "compact_q_segment_ladder": [16, 32],
        "compact_taylor_order": 12,
        "precision_tiers": 2,
        "ball_bessel_evaluations": 12,
        "root_brackets": 1,
        "nonzero_lambda_boxes": 2,
        "ode_calls": 0,
        "root_calls": 0,
        "quadrature_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "panel_specific_absolute_rho_picard_tubes": None,
        "actual_nonzero_lambda_declared_Gamma1": None,
        "complete_minus_tail_remainder": None,
        "actual_declared_Gamma1_sign_separation": None,
        "nonzero_lambda_root_continuation": None,
        "root_velocity": None,
        "nonreal_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_RAQ_completion": None,
        "physical_or_empirical_claim": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)
    bessel_evaluations: int = 0

    def _register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check id: {identifier}")
        self.seen.add(identifier)

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self._register(identifier)
        reduced = sp.simplify(residual)
        passed = (
            all(sp.simplify(entry) == 0 for entry in reduced)
            if isinstance(reduced, sp.MatrixBase)
            else bool(reduced == 0)
        )
        self.exact.append({"id": identifier, "passed": passed, "statement": statement, "residual": str(reduced)})

    def inequality(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self._register(identifier)
        self.exact.append({"id": identifier, "passed": bool(passed), "statement": statement, **data})

    def control(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self._register(identifier)
        self.controls.append({"id": identifier, "passed": bool(passed), "statement": statement, **data})

    def guard(self, identifier: str, theorem: str, hypotheses: str, scope: str) -> None:
        self._register(identifier)
        self.guards.append({"id": identifier, "verified": True, "theorem": theorem, "hypotheses": hypotheses, "scope": scope})

    def bessel_k(self, z: acb, order: acb) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("Bessel evaluation cap exceeded")
        return z.bessel_k(order)


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload self-hash mismatch: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    return payload, {"path": item["path"], "sha256": observed, "payload_sha256_without_self": item["payload_sha256_without_self"], "role": item["role"]}


def exact_audit(audit: Audit) -> None:
    q_switch, q0 = sp.Rational(-29, 10), sp.Rational(-4)
    audit.identity("rawc.switch_q0.exact_partition_16", 16 * sp.Rational(-11, 160) - (q0 - q_switch), "Sixteen exact rational subintervals join Q_switch to Q0.")
    audit.identity("rawc.switch_q0.exact_partition_32", 32 * sp.Rational(-11, 320) - (q0 - q_switch), "Thirty-two exact rational subintervals join Q_switch to Q0.")
    v, vq, w, wq, a, b = sp.symbols("v vq w wq a b")
    rho = -vq / v - sp.symbols("x") - sp.Rational(1, 2)
    sensitivity = sp.diff(rho, v) * w + sp.diff(rho, vq) * wq
    audit.identity("rawc.switch_q0.projective_sensitivity_identity", sensitivity - (vq * w - v * wq) / v**2, "The four-state quotient gives s=partial_lambda rho without differentiating through a node chart.")
    matrix = sp.Matrix([[0, 1, 0, 0], [a, 0, 0, 0], [0, 0, 0, 1], [b, 0, a, 0]])
    state = sp.Matrix([v, vq, w, wq])
    audit.identity("rawc.switch_q0.four_state_system", matrix * state - sp.Matrix([vq, a * v, wq, b * v + a * w]), "Y=(v,v_Q,w,w_Q) is the differentiated two-state system.")
    scale, scale_lambda = sp.symbols("scale scale_lambda", nonzero=True)
    scaled_sensitivity = (
        (scale * vq) * (scale_lambda * v + scale * w)
        - (scale * v) * (scale_lambda * vq + scale * wq)
    ) / (scale * v) ** 2
    audit.identity(
        "rawc.switch_q0.lambda_dependent_scale_invariance",
        scaled_sensitivity - (vq * w - v * wq) / v**2,
        "The projective sensitivity is invariant under lambda-dependent nonzero amplitude rescaling.",
    )


def matrix_derivative(q_base: fmpq, kappa_band: arb, lambda_band: arb, derivative: int, order: int) -> list[list[arb]]:
    _, A_values = hybrid.coefficient_derivatives(q_base, kappa_band, lambda_band, order)
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    forcing = x_value * x_value.sqrt() / c_value.sqrt()
    b_value = (arb(3) / 2) ** derivative * forcing
    A_value = A_values[derivative]
    return [[arb(0), arb(0), arb(0), arb(0)], [A_value, arb(0), arb(0), arb(0)], [arb(0), arb(0), arb(0), arb(0)], [b_value, arb(0), A_value, arb(0)]] if derivative else [[arb(0), arb(1), arb(0), arb(0)], [A_value, arb(0), arb(0), arb(0)], [arb(0), arb(0), arb(0), arb(1)], [b_value, arb(0), A_value, arb(0)]]


def matrix_apply(matrix: list[list[arb]], state: list[arb]) -> list[arb]:
    return [sum((matrix[row][column] * state[column] for column in range(4)), arb(0)) for row in range(4)]


def matrix_majorants(q_base: fmpq, kappa_band: arb, lambda_band: arb, order: int) -> list[arb]:
    # `hybrid.whole_step_majorants` supplies the inherited a(q) convention.
    a_majorants = hybrid.whole_step_majorants(q_base, kappa_band, lambda_band, order)
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    forcing = x_value * x_value.sqrt() / c_value.sqrt()
    values = []
    for derivative in range(order + 1):
        b_majorant = (arb(3) / 2) ** derivative * forcing
        # Induced infinity norm of M^(n), with identity off-diagonal only for n=0.
        values.append(arb((a_majorants[derivative] + b_majorant + (arb(1) if derivative == 0 else arb(0))).upper()))
    return values


def propagate_box(audit: Audit, *, label: str, tier: int, dps: int, segments: int, kappa_band: arb, lambda_band: arb, rho_switch: arb, s_switch: arb, conventions: dict[str, Any]) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    q_switch = exact_rational(conventions["Q_switch"])
    q0 = exact_rational(conventions["Q_0"])
    step = (q0 - q_switch) / segments
    x_switch = 6 * arb.pi() ** 2 * arb(q_switch).exp()
    # Gauge v(Qswitch)=1.  Then rho=-vQ-v terms and s=-wQ exactly.
    state = [arb(1), -(x_switch + arb(1) / 2 + rho_switch), arb(0), -s_switch]
    audit.control(f"rawc.switch_q0.{label}.tier{tier}.segments{segments}.switch_state", bool(x_switch.lower() > 3 and state[1].is_finite() and state[3].is_finite()), "The hash-pinned actual switch rho and s boxes initialize a projective four-state chart inside x>3.", rho_Qswitch=interval_record(rho_switch, digits), s_Qswitch=interval_record(s_switch, digits), v_Qswitch=interval_record(state[1], digits), w_Qswitch=interval_record(state[3], digits))
    step_records: list[dict[str, Any]] = []
    if step >= 0:
        raise AssertionError("Q_switch-to-Q0 transfer must be backward in Q")
    abs_step = arb(-step)
    for index in range(segments):
        q_base = q_switch + index * step
        derivatives: list[list[arb]] = [state]
        matrices = [matrix_derivative(q_base, kappa_band, lambda_band, derivative, order) for derivative in range(order + 1)]
        for n in range(order):
            next_derivative = [arb(0) for _ in range(4)]
            for derivative in range(n + 1):
                applied = matrix_apply(matrices[derivative], derivatives[n - derivative])
                for component in range(4):
                    next_derivative[component] += math.comb(n, derivative) * applied[component]
            derivatives.append(next_derivative)
        polynomial = [arb(0) for _ in range(4)]
        for n, jet in enumerate(derivatives):
            factor = arb(step) ** n / math.factorial(n)
            for component in range(4):
                polynomial[component] += factor * jet[component]
        majorants = matrix_majorants(q_base, kappa_band, lambda_band, order)
        state_norm = max(
            (hybrid.absolute_upper(value) for value in state),
            key=lambda value: value.upper(),
        )
        tube_norm = arb((state_norm * (majorants[0] * abs_step).exp()).upper())
        derivative_bounds = [tube_norm]
        for n in range(order + 1):
            derivative_bounds.append(arb(sum((math.comb(n, derivative) * majorants[derivative] * derivative_bounds[n - derivative] for derivative in range(n + 1)), arb(0)).upper()))
        remainder = arb((derivative_bounds[order + 1] * abs_step ** (order + 1) / math.factorial(order + 1)).upper())
        remainder_box = hybrid.symmetric_interval(remainder)
        state = [value + remainder_box for value in polynomial]
        step_ok = bool(remainder.is_finite() and remainder.lower() >= 0 and all(value.is_finite() for value in state))
        audit.control(f"rawc.switch_q0.{label}.tier{tier}.segments{segments}.step{index + 1}.whole_step_taylor", step_ok, "The four-state order-12 Taylor polynomial is enlarged by a full-step D13 bound using the inherited coefficient-majorant semantics.", q_base=str(q_base), q_next=str(q_base + step), remainder_radius=interval_record(remainder, digits))
        step_records.append({"index": index + 1, "q_base": str(q_base), "q_next": str(q_base + step), "remainder_radius_upper": remainder.upper().str(digits, radius=False)})
    v, vq, w, wq = state
    denominator_ok = excludes_zero(v)
    rho_q0: arb | None = None
    s_q0: arb | None = None
    if denominator_ok:
        x0 = 6 * arb.pi() ** 2 * arb(q0).exp()
        rho_q0 = -vq / v - x0 - arb(1) / 2
        s_q0 = (vq * w - v * wq) / (v * v)
    endpoint_ok = bool(denominator_ok and rho_q0 is not None and s_q0 is not None and rho_q0.is_finite() and s_q0.is_finite())
    audit.control(f"rawc.switch_q0.{label}.tier{tier}.segments{segments}.projective_endpoint", endpoint_ok, "The node-safe state has nonzero v(Q0), so rho(Q0) and s(Q0) are finite projective outputs.", v_Q0=interval_record(v, digits), rho_Q0=interval_record(rho_q0, digits) if rho_q0 else None, s_Q0=interval_record(s_q0, digits) if s_q0 else None)
    return {"label": label, "decimal_digits": dps, "segments": segments, "compact_steps": step_records, "v_Q0": interval_record(v, digits), "v_Q_Q0": interval_record(vq, digits), "w_Q0": interval_record(w, digits), "w_Q_Q0": interval_record(wq, digits), "v_Q0_excludes_zero": denominator_ok, "rho_Q0": interval_record(rho_q0, digits) if rho_q0 else None, "s_Q0": interval_record(s_q0, digits) if s_q0 else None, "status": "CERTIFIED_FINITE_PROJECTIVE_ENDPOINT" if endpoint_ok else "ENDPOINT_NOT_CERTIFIED"}, {"v": v, "rho": rho_q0 if rho_q0 else arb(0), "s": s_q0 if s_q0 else arb(0)}


def bessel_rho_q0(audit: Audit, kappa_band: arb, digits: int) -> arb:
    x0 = acb(6 * arb.pi() ** 2 * arb(-4).exp())
    order = acb(0, kappa_band)
    k0 = audit.bessel_k(x0, order)
    km = audit.bessel_k(x0, order - 1)
    kp = audit.bessel_k(x0, order + 1)
    ratio = (-x0 * (km + kp) / 2) / k0
    if not (ratio.imag.lower() <= 0 <= ratio.imag.upper() and k0.abs_lower() > 0):
        raise AssertionError("lambda-zero Bessel endpoint is not a real nonzero chart")
    return -ratio.real - x0.real - arb(1) / 2


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input_sha = sha256_bytes(raw)
    if observed_input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input_sha}")
    config = json.loads(raw)
    if (
        config.get("schema_version")
        != "ice.raw-c-bessel-preconditioned-node-safe-switch-to-q0-sensitivity-transfer.input.v1"
        or config.get("calculation_id") != CALCULATION_ID
        or config.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if config.get("resource_caps") != expected_caps() or config.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("resource or null-output drift")
    conventions = config["declared_conventions"]
    if conventions["precision_ladder_decimal_digits"] != [80, 120] or conventions["compact_q_segment_ladder"] != [16, 32] or conventions["compact_taylor_order"] != 12:
        raise AssertionError("precision, segment ladder or Taylor order drift")
    root = Path(__file__).resolve().parent.parent
    method_reuse = config["method_reuse"]
    method_path = root / method_reuse["path"]
    method_sha = sha256_bytes(method_path.read_bytes())
    if method_sha != method_reuse["sha256"]:
        raise AssertionError("imported interval-Taylor helper hash mismatch")
    if method_path.resolve() != Path(hybrid.__file__).resolve():
        raise AssertionError("imported interval-Taylor helper path mismatch")
    upstream_payloads: dict[str, dict[str, Any]] = {}
    upstream_records: list[dict[str, str]] = []
    expected_upstream_paths = [
        conventions["switch_result_path"],
        conventions["green_result_path"],
    ]
    if [item["path"] for item in config["upstream_results"]] != expected_upstream_paths:
        raise AssertionError("upstream result topology drift")
    for item in config["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream_payloads[item["path"]] = payload
        upstream_records.append(record)
    audit = Audit()
    exact_audit(audit)
    audit.guard("rawc.switch_q0.guard.node_safe_four_state", "Differentiated linear two-state system", "w=partial_lambda v is evolved with v rather than differentiating rho through a possible node.", "Only finite projective endpoint data are returned after an executable v(Q0) nonzero check.")
    audit.guard("rawc.switch_q0.guard.whole_step_taylor", "Taylor theorem with complete parameter-box derivative majorants", "The imported hybrid coefficient/majorant functions are used on every exact rational subinterval and each D13 remainder is outward.", "This is not a black-box ODE solve or sampled trajectory.")
    audit.guard("rawc.switch_q0.guard.scope", "Computational-workbench claim separation", "One root bracket and two punctured real lambda boxes are inherited from a hash-pinned switch certificate.", "Gamma1, its tail, roots, spectra, RAQ and physical interpretation remain null.")
    switch_path = conventions["switch_result_path"]
    switch_result = upstream_payloads[switch_path]
    green_result = upstream_payloads[conventions["green_result_path"]]
    final_rows = switch_result["certified_calculation"]["final_intersections"]
    by_label = {row["label"]: row for row in final_rows}
    if set(by_label) != {"negative", "positive"} or not all(row["certified"] for row in final_rows):
        raise AssertionError("switch certificate topology drift")
    bracket = conventions["root_bracket"]
    kappa_band = hybrid.bracket_band(exact_rational(bracket["left_exact"]), exact_rational(bracket["right_exact"]))
    digits = int(conventions["ball_output_digits"])
    green_root = green_result["certified_calculation"]["root_bracket_rows"][0]
    if (
        green_root["kappa_bracket"]["left_exact"] != bracket["left_exact"]
        or green_root["kappa_bracket"]["right_exact"] != bracket["right_exact"]
    ):
        raise AssertionError("lambda-zero Green root bracket drift")
    green_h_q0 = interval_from_record(green_root["certified_h_Q0_intersection"])
    tier_balls: dict[str, list[dict[str, arb]]] = {"negative": [], "positive": [], "lambda_zero": []}
    tier_records: dict[str, list[dict[str, Any]]] = {"negative": [], "positive": [], "lambda_zero": []}
    for tier, dps in enumerate(conventions["precision_ladder_decimal_digits"], start=1):
        for label in ("negative", "positive"):
            row = by_label[label]
            rho_switch = interval_from_record(row["rho_actual_Qswitch_intersection"])
            s_switch = interval_from_record(row["actual_s_Qswitch_intersection"])
            lambda_box = row["lambda_box"]
            lambda_band = hybrid.bracket_band(exact_rational(lambda_box["left_exact"]), exact_rational(lambda_box["right_exact"]))
            for segments in conventions["compact_q_segment_ladder"]:
                record, balls = propagate_box(audit, label=label, tier=tier, dps=int(dps), segments=int(segments), kappa_band=kappa_band, lambda_band=lambda_band, rho_switch=rho_switch, s_switch=s_switch, conventions=conventions)
                tier_records[label].append(record)
                tier_balls[label].append(balls)
        # The closed-segment switch theorem includes lambda=0, where the
        # projective sensitivity is nonzero.  Reuse that uniform s box and
        # the exact Bessel switch direction.
        zero_rho = interval_from_record(by_label["negative"]["rho0_Qswitch_intersection"])
        zero_s = interval_from_record(by_label["negative"]["actual_s_Qswitch_intersection"])
        for segments in conventions["compact_q_segment_ladder"]:
            record, balls = propagate_box(audit, label="lambda_zero", tier=tier, dps=int(dps), segments=int(segments), kappa_band=kappa_band, lambda_band=arb(0), rho_switch=zero_rho, s_switch=zero_s, conventions=conventions)
            exact_rho = bessel_rho_q0(audit, kappa_band, digits)
            regression_ok = bool(
                balls["v"].is_finite()
                and balls["rho"].lower() <= exact_rho.lower()
                and balls["rho"].upper() >= exact_rho.upper()
                and balls["s"].lower() <= green_h_q0.lower()
                and balls["s"].upper() >= green_h_q0.upper()
            )
            audit.control(f"rawc.switch_q0.lambda_zero.tier{tier}.segments{segments}.bessel_green_regression", regression_ok, "The lambda-zero node-safe transfer contains both the Bessel endpoint rho and the independently certified Green sensitivity h(Q0).", exact_Bessel_rho_Q0=interval_record(exact_rho, digits), transported_rho_Q0=interval_record(balls["rho"], digits), Green_h_Q0=interval_record(green_h_q0, digits), transported_s_Q0=interval_record(balls["s"], digits))
            tier_records["lambda_zero"].append(record)
            tier_balls["lambda_zero"].append(balls)
    for label in ("negative", "positive", "lambda_zero"):
        for tier_index in range(2):
            coarse = tier_balls[label][2 * tier_index]
            refined = tier_balls[label][2 * tier_index + 1]
            nested = all(intersection(coarse[key], refined[key]) is not None for key in ("v", "rho", "s"))
            audit.control(f"rawc.switch_q0.{label}.tier{tier_index + 1}.segment_refinement_overlap", nested, "The 16- and 32-segment enclosures overlap componentwise; this is a discretization refinement control, not independent evidence.")
        for segment_index in range(2):
            low = tier_balls[label][segment_index]
            high = tier_balls[label][segment_index + 2]
            overlap = all(intersection(low[key], high[key]) is not None for key in ("v", "rho", "s"))
            audit.control(f"rawc.switch_q0.{label}.segments{conventions['compact_q_segment_ladder'][segment_index]}.precision_overlap", overlap, "The 80/120-digit same-backend enclosures overlap componentwise.")
    final_intersections: list[dict[str, Any]] = []
    width_target = arb(
        exact_rational(conventions["projective_sensitivity_width_target"])
    )
    for label in ("negative", "positive", "lambda_zero"):
        combined: dict[str, arb | None] = {}
        for key in ("v", "rho", "s"):
            current: arb | None = tier_balls[label][0][key]
            for row in tier_balls[label][1:]:
                current = intersection(current, row[key]) if current is not None else None
            combined[key] = current
        v_final = combined["v"]
        rho_final = combined["rho"]
        s_final = combined["s"]
        final_ok = bool(
            v_final is not None
            and rho_final is not None
            and s_final is not None
            and excludes_zero(v_final)
            and rho_final.is_finite()
            and s_final.is_finite()
            and interval_width(s_final).upper() < width_target.lower()
        )
        audit.control(
            f"rawc.switch_q0.{label}.final_projective_sensitivity",
            final_ok,
            "The four valid tier/subdivision enclosures have a common finite Q0 projective endpoint, nonzero amplitude and sensitivity width below the declared target.",
            v_Q0=interval_record(v_final, digits) if v_final is not None else None,
            rho_Q0=interval_record(rho_final, digits) if rho_final is not None else None,
            s_Q0=interval_record(s_final, digits) if s_final is not None else None,
            s_Q0_excludes_zero=(excludes_zero(s_final) if s_final is not None else None),
            sensitivity_width_target=conventions[
                "projective_sensitivity_width_target"
            ],
        )
        final_intersections.append(
            {
                "label": label,
                "certified": final_ok,
                "v_Q0": interval_record(v_final, digits) if v_final is not None else None,
                "rho_Q0": interval_record(rho_final, digits) if rho_final is not None else None,
                "s_Q0": interval_record(s_final, digits) if s_final is not None else None,
                "s_Q0_excludes_zero": (
                    excludes_zero(s_final) if s_final is not None else None
                ),
                "projective_sensitivity_width_target": conventions[
                    "projective_sensitivity_width_target"
                ],
                "status": (
                    "CERTIFIED_FINITE_PROJECTIVE_Q0_SENSITIVITY"
                    if final_ok
                    else "PROJECTIVE_Q0_SENSITIVITY_NOT_CERTIFIED"
                ),
            }
        )
    audit.inequality("rawc.switch_q0.bessel_call_count", audit.bessel_evaluations == expected_caps()["ball_bessel_evaluations"], "The lambda-zero regression makes exactly three Bessel calls for each precision/segment row.", observed=audit.bessel_evaluations, expected=expected_caps()["ball_bessel_evaluations"])
    exact_pass = all(item["passed"] for item in audit.exact)
    control_pass = all(item["passed"] for item in audit.controls)
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": config["calculation_id"], "numbered_phase": None, "run_status": "VALID_RUN", "verdict": "CERTIFY_FINITE_BESSEL_PRECONDITIONED_NODE_SAFE_SWITCH_TO_Q0_PROJECTIVE_SENSITIVITY_TRANSFER" if exact_pass and control_pass else "NODE_SAFE_SWITCH_TO_Q0_TRANSFER_NOT_CERTIFIED", "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input_sha}, "method_reuse": {"path": method_reuse["path"], "sha256": method_sha, "role": method_reuse["role"]}, "upstream_results": upstream_records, "primary_sources": config["primary_sources"], "declared_conventions": conventions, "assumptions": config["assumptions"], "exact_checks": audit.exact, "controls": audit.controls, "theorem_guards": audit.guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "theorem_guards": len(audit.guards), "all_executable_checks_passed": bool(exact_pass and control_pass)}, "certified_calculation": {"scope": "root bracket 1, two punctured real lambda boxes, Q_switch to Q0", "outputs": "finite projective v(Q0), rho(Q0), s(Q0) only", "final_intersections": final_intersections, "tier_records": tier_records, "next_mathematical_gap": "construct a separate differentiated rotating-frame minus-tail functional for the declared Gamma_1 before any sign or root claim"}, "non_claim": "No Gamma_1 value or tail, sign/zero separation, root continuation, Weyl/spectral/RAQ or physical claim.", "required_fail_closed_outputs": config["required_fail_closed_outputs"], "resource_accounting": {"compact_segment_rows": 12, "compact_steps_evaluated": 288, "compact_taylor_order": 12, "precision_tiers": 2, "ball_bessel_evaluations": audit.bessel_evaluations, "ode_calls": 0, "root_calls": 0, "quadrature_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "adjacent_result_files_written": 1}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "sympy": sp.__version__, "python_flint": importlib.metadata.version("python-flint"), "platform": platform.platform()}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded)}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
