#!/usr/bin/env python3
"""Exact fixed-metric scalar-matter DH falsifier on a zonal unit-S3 packet.

The calculation separates a missing metric-strain contribution from a hard
field-mode projection remainder.  It is not a full ADM/HDA or anomaly test.
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

import closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger as zonal


INPUT_NAME = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_DH_FIXED_METRIC_FALSIFIER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_DH_FIXED_METRIC_FALSIFIER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_v0_scalar_matter_dh_fixed_metric_falsifier.py"
EXPECTED_INPUT_SHA256 = "837b06609fabc4926ebd9dd8b1c3f7177f261c619ef2c188337c1e9482ad6a13"
CALCULATION_ID = "ClosedS3ZonalV0ScalarMatterDHFixedMetricFalsifier"
RESULT_SCHEMA = "ice.closed-s3-zonal-v0-scalar-matter-dh-fixed-metric-falsifier.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_DH_FIXED_METRIC_FALSIFIER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, residual: sp.Expr | bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        passed = bool(residual) if isinstance(residual, bool) else sp.simplify(residual) == 0
        self.exact.append({"id": check_id, "passed": passed, "statement": statement})


def expected_caps() -> dict[str, int]:
    return {
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


def read_input() -> tuple[dict[str, Any], str, dict[str, str]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    payload = json.loads(raw)
    if (
        payload["schema_version"]
        != "ice.closed-s3-zonal-v0-scalar-matter-dh-fixed-metric-falsifier.input.v1"
        or payload["calculation_id"] != CALCULATION_ID
        or payload["numbered_phase"] is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap drift")
    if payload["primary_failure_class"] != "model_omission":
        raise AssertionError("primary failure classification drift")

    root = Path(__file__).resolve().parent.parent
    dependency = payload["reused_local_implementation"]
    dependency_raw = (root / dependency["path"]).read_bytes()
    dependency_sha = sha256_bytes(dependency_raw)
    if dependency_sha != dependency["sha256"]:
        raise AssertionError(f"reused helper hash mismatch: {dependency['path']}")
    reused = {"path": dependency["path"], "sha256": dependency_sha}
    return payload, observed, reused


def scalar_coefficients(raw: dict[str, str]) -> dict[int, sp.Expr]:
    return {int(index): sp.sympify(value) for index, value in raw.items()}


def diffeomorphism(
    shift_degree: int,
    cutoff: int,
    theta: list[sp.Symbol],
    xi: list[sp.Symbol],
    a: sp.Symbol,
    normalizer: sp.Expr,
) -> sp.Expr:
    return sp.expand(
        sum(
            xi[i]
            * theta[j]
            * zonal.gradient_triple(i, shift_degree, j, normalizer)
            / a**2
            for i in range(cutoff + 1)
            for j in range(cutoff + 1)
        )
    )


def lie_lapse_hamiltonian(
    shift_degree: int,
    lapse_degree: int,
    field_cutoff: int,
    theta: list[sp.Symbol],
    xi: list[sp.Symbol],
    a: sp.Symbol,
    normalizer: sp.Expr,
) -> sp.Expr:
    """H[L_v N], with v^a=a^-2 D^a Q_shift and N=Q_lapse."""
    return sp.expand(
        sum(
            zonal.gradient_triple(
                smear_degree, shift_degree, lapse_degree, normalizer
            )
            * zonal.hamiltonian(
                smear_degree, field_cutoff, theta, xi, a, normalizer
            )
            / a**2
            for smear_degree in range(shift_degree + lapse_degree + 1)
        )
    )


def printable(expression: sp.Expr) -> str:
    return str(sp.factor(sp.simplify(expression)))


def run(payload: dict[str, Any], input_sha: str, reused: dict[str, str]) -> dict[str, Any]:
    ledger = Ledger()
    a = sp.symbols("a", positive=True, real=True)
    chi = sp.symbols("chi", real=True)
    normalizer = 1 / sp.sqrt(2 * sp.pi**2)

    packet = payload["packet"]
    shift_degree = int(packet["shift_degree"])
    lapse_degree = int(packet["lapse_degree"])
    cutoffs = [int(value) for value in packet["cutoffs"]]
    theta_coefficients = scalar_coefficients(packet["theta_coefficients"])
    xi_coefficients = scalar_coefficients(packet["xi_coefficients"])
    if cutoffs != [2, 3]:
        raise AssertionError("declared cutoff packet drift")
    if any(index < 0 or index > min(cutoffs) for index in theta_coefficients | xi_coefficients):
        raise AssertionError("packet coefficients exceed the smallest cutoff")

    max_ambient = max(cutoffs) + max(shift_degree, lapse_degree)
    theta = list(sp.symbols(f"theta0:{max_ambient + 1}", real=True))
    xi = list(sp.symbols(f"xi0:{max_ambient + 1}", real=True))

    q_shift = zonal.direct_q(shift_degree, chi, normalizer)
    q_lapse = zonal.direct_q(lapse_degree, chi, normalizer)
    theta_direct = sum(
        coefficient * zonal.direct_q(index, chi, normalizer)
        for index, coefficient in theta_coefficients.items()
    )
    xi_direct = sum(
        coefficient * zonal.direct_q(index, chi, normalizer)
        for index, coefficient in xi_coefficients.items()
    )
    v_chi = sp.diff(q_shift, chi) / a**2
    divergence_v = -zonal.eigenvalue(shift_degree) * q_shift / a**2
    strain_chichi = sp.diff(q_shift, chi, 2) / a**2
    lie_lapse_direct = sp.expand(v_chi * sp.diff(q_lapse, chi))
    energy_direct = sp.expand(
        xi_direct**2 / (2 * a**3)
        + a * sp.diff(theta_direct, chi) ** 2 / 2
    )
    target_direct = zonal.direct_integral(
        lie_lapse_direct * energy_direct, chi
    )
    residual_direct_kinetic = zonal.direct_integral(
        -q_lapse * xi_direct**2 * divergence_v / (2 * a**3),
        chi,
    )
    residual_direct_gradient = zonal.direct_integral(
        q_lapse
        * (
            a * sp.diff(theta_direct, chi) ** 2 * divergence_v
            - 2 * a * strain_chichi * sp.diff(theta_direct, chi) ** 2
        )
        / 2,
        chi,
    )
    residual_direct = sp.simplify(
        residual_direct_kinetic + residual_direct_gradient
    )

    ledger.check(
        "CS3V0DH.geometry.Q1_hessian",
        sp.diff(q_shift, chi, 2) + q_shift,
        "The zonal Q1 radial Hessian component obeys D_chi D_chi Q1=-Q1.",
    )
    ledger.check(
        "CS3V0DH.geometry.Q1_divergence",
        divergence_v + 3 * q_shift / a**2,
        "For v=a^-2 DQ1, the unit-S3 divergence is -3Q1/a^2.",
    )

    rows: list[dict[str, Any]] = []
    for cutoff in cutoffs:
        ambient = cutoff + max(shift_degree, lapse_degree)
        substitutions = {
            theta[index]: theta_coefficients.get(index, sp.S.Zero)
            for index in range(ambient + 1)
        }
        substitutions.update(
            {
                xi[index]: xi_coefficients.get(index, sp.S.Zero)
                for index in range(ambient + 1)
            }
        )

        d_ambient = diffeomorphism(
            shift_degree, ambient, theta, xi, a, normalizer
        )
        h_ambient = zonal.hamiltonian(
            lapse_degree, ambient, theta, xi, a, normalizer
        )
        channel_terms = [
            sp.expand(
                sp.diff(d_ambient, theta[index])
                * sp.diff(h_ambient, xi[index])
                - sp.diff(d_ambient, xi[index])
                * sp.diff(h_ambient, theta[index])
            )
            for index in range(ambient + 1)
        ]
        ambient_bracket = sp.simplify(sum(channel_terms).subs(substitutions))

        d_projected = diffeomorphism(
            shift_degree, cutoff, theta, xi, a, normalizer
        )
        h_projected = zonal.hamiltonian(
            lapse_degree, cutoff, theta, xi, a, normalizer
        )
        projected_bracket = sp.simplify(
            zonal.poisson(
                d_projected, h_projected, theta, xi, cutoff
            ).subs(substitutions)
        )
        reverse_bracket = sp.simplify(
            zonal.poisson(
                h_projected, d_projected, theta, xi, cutoff
            ).subs(substitutions)
        )
        lapse_transport = sp.simplify(
            lie_lapse_hamiltonian(
                shift_degree,
                lapse_degree,
                cutoff,
                theta,
                xi,
                a,
                normalizer,
            ).subs(substitutions)
        )
        fixed_metric_residual = sp.simplify(ambient_bracket - lapse_transport)
        projection_remainder = sp.simplify(ambient_bracket - projected_bracket)
        omitted_channels = [
            index
            for index in range(cutoff + 1, ambient + 1)
            if sp.simplify(channel_terms[index].subs(substitutions)) != 0
        ]
        omitted_sum = sp.simplify(
            sum(channel_terms[index].subs(substitutions) for index in omitted_channels)
        )

        prefix = f"CS3V0DH.L{cutoff}"
        ledger.check(
            f"{prefix}.lapse_transport_direct",
            lapse_transport - target_direct,
            "The spectral H[L_v N] coefficient agrees with direct chi integration.",
        )
        ledger.check(
            f"{prefix}.fixed_metric_residual_direct",
            fixed_metric_residual - residual_direct,
            "The canonical bracket residual agrees with the independent divergence/Hessian strain integral.",
        )
        ledger.check(
            f"{prefix}.decomposition",
            ambient_bracket - lapse_transport - residual_direct,
            "The ambient matter-only bracket is lapse transport plus the fixed-metric strain residual.",
        )
        ledger.check(
            f"{prefix}.target_nonzero",
            lapse_transport != 0,
            "The mixed-parity packet makes the lapse-transport target nonzero.",
        )
        ledger.check(
            f"{prefix}.strain_nonzero",
            fixed_metric_residual != 0,
            "The selected non-Killing shift exposes a strain residual that is not identically zero as a function of a.",
        )
        ledger.check(
            f"{prefix}.strain_components_nonzero",
            residual_direct_kinetic != 0 and residual_direct_gradient != 0,
            "Kinetic and gradient strain contributions are separately nonzero, so an isolated cancellation cannot establish a functional identity.",
        )
        ledger.check(
            f"{prefix}.strain_scaled_polynomial",
            sp.pi**2 * a**5 * fixed_metric_residual - (3 - a**4),
            "The residual is (3-a^4)/(pi^2 a^5), exposing its isolated positive-scale cancellation at a^4=3.",
        )
        ledger.check(
            f"{prefix}.projection_decomposition",
            projection_remainder - omitted_sum,
            "The ambient-minus-L-only difference equals the omitted canonical-channel sum.",
        )
        ledger.check(
            f"{prefix}.reverse_sign",
            projected_bracket + reverse_bracket,
            "Reversing the projected Poisson-bracket order flips its sign exactly.",
        )

        rows.append(
            {
                "cutoff_L": cutoff,
                "ambient_cutoff": ambient,
                "matter_only_ambient_bracket_exact": printable(ambient_bracket),
                "lapse_transport_exact": printable(lapse_transport),
                "fixed_metric_strain_residual_exact": printable(fixed_metric_residual),
                "fixed_metric_strain_kinetic_exact": printable(
                    residual_direct_kinetic
                ),
                "fixed_metric_strain_gradient_exact": printable(
                    residual_direct_gradient
                ),
                "fixed_metric_strain_isolated_zero_condition": "a^4=3",
                "required_metric_variation_contribution_exact": printable(
                    -fixed_metric_residual
                ),
                "L_only_bracket_exact": printable(projected_bracket),
                "projection_remainder_exact": printable(projection_remainder),
                "omitted_canonical_channels": omitted_channels,
                "omitted_channel_sum_exact": printable(omitted_sum),
            }
        )

    passed = all(check["passed"] for check in ledger.exact)
    verdict = (
        "KILL_FIXED_METRIC_MATTER_ONLY_DH_CLOSURE_RETAIN_EXACT_STRAIN_DECOMPOSITION_NOT_FULL_ADM_HDA"
        if passed
        else "KILL_DECLARED_FIXED_METRIC_DH_FALSIFIER_PACKET"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "question": payload["question"],
        "one_output": payload["one_output"],
        "primary_failure_class": payload["primary_failure_class"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "reused_local_implementation": reused,
        "primary_sources": payload["primary_sources"],
        "declared_conventions": payload["declared_conventions"],
        "packet": packet,
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(check["passed"] for check in ledger.exact),
            "exact_total": len(ledger.exact),
            "all_executable_checks_passed": passed,
        },
        "decomposition_rows": rows,
        "evidence_layers": {
            "calculated_fact": "The selected fixed-metric matter-only DH bracket differs from H[L_v N] by a strain residual that is not identically zero; its two nonzero components cancel only at a^4=3 for this packet.",
            "error_diagnosis": "The residual is reproduced by an independent fixed-metric divergence/Hessian integral; finite projection error is reported separately by cutoff.",
            "model_boundary": "The gravitational metric part of the diffeomorphism generator is absent, so no full ADM/HDA conclusion follows.",
            "physics_claim": None,
        },
        "non_claims": payload["non_claims"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    payload, input_sha, reused = read_input()
    result = run(payload, input_sha, reused)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "result": RESULT_NAME,
                "result_sha256": sha256_bytes(encoded),
                "result_bytes": len(encoded),
                "automatic_next": None,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
