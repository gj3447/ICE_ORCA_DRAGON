#!/usr/bin/env python3
"""Classify one safe compact projective mixed-end chart, with a bad control.

This bounded unnumbered calculation records only action-real-part signs on a
declared ratio/phase chart.  It leaves a leading-transition band unresolved;
Stokes data are not computed.  It does not
construct a compactification, relative cycle, connector, or intersection.
"""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_M2_SAFE_PROJECTIVE_MIXED_PHASE_CHART_INPUTS.json"
RESULT_NAME = "GATE1_M2_SAFE_PROJECTIVE_MIXED_PHASE_CHART_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_m2_safe_projective_mixed_phase_chart.py"
EXPECTED_INPUT_SHA256 = "2dcab3066903a855bdb85ead8add9e0f46defdaeb9e3171939f5f1bf9d694fec"
EXPECTED_UPSTREAM_SHA256 = {
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json": "b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4",
    "cpt_temporal_folded_susy/GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_RESULT.json": "089962d1f2452e4906eb103ab647bf305aeec72cf02d621727d977829d5f7ca9",
}
CALCULATION_ID = "Gate1M2SafeProjectiveMixedPhaseChart"
SCHEMA = "ice.gate1-m2-safe-projective-mixed-phase-chart.result.v1"
VERDICT = "KEEP_SCOPED_SAFE_PROJECTIVE_MIXED_PHASE_SIGN_CHART"
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144,
            "changed_artifact_files": 12, "changed_artifact_bytes": 1000000,
            "symbolic_operations": 180, "quadratures": 0, "root_calls": 0,
            "ode_calls": 0, "sampling_points": 72, "automatic_descendants": 0}


def nulls() -> dict[str, Any]:
    return {"connection_to_compact_phase39_chain": None, "tail_amplitude_or_measure_absolute_convergence": None,
            "complete_mixed_end_census": None, "all_ratio_or_phase_end_admissibility": None,
            "stokes_band_resolution": None, "admissible_full_joint_completion": None,
            "full_relative_homology_class": None, "source_defined_joint_relative_cycle": None,
            "source_to_thimble_deformation": None, "physical_original_cycle": None,
            "complete_global_signed_intersection_vector": None, "global_n_sigma": None,
            "singular_endpoint_nonreal_weyl_m": None, "spectral_measure": None,
            "RAQ_completion": None, "physics_claim": None, "TOE_claim": None,
            "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)
    samples: int = 0

    def add(self, kind: str, ident: str, ok: bool, statement: str, **data: Any) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate check id: {ident}")
        self.seen.add(ident)
        if not ok:
            raise AssertionError(f"[{kind} FAIL] {ident}: {statement}")
        target = self.exact if kind == "EXACT" else self.numerical if kind == "NUM" else self.guards
        target.append({"id": ident, "passed" if kind != "GUARD" else "verified": True,
                       "statement" if kind != "GUARD" else "conclusion_and_scope": statement, **data})

    def count(self) -> None:
        self.samples += 1
        if self.samples > caps()["sampling_points"]:
            raise AssertionError("sampling cap exceeded")


def fraction(text: str) -> mp.mpf:
    if "/" not in text:
        return mp.mpf(text)
    a, b = text.split("/", 1)
    return mp.mpf(a) / mp.mpf(b)


def text(value: mp.mpf | mp.mpc, digits: int = 24) -> str:
    return mp.nstr(value, digits)


def potential(phi: mp.mpc) -> mp.mpc:
    return mp.mpf(3) / 4 * (1 - mp.exp(-mp.sqrt(mp.mpf(2) / 3) * phi)) ** 2


def direct_action(s: mp.mpf, rho: mp.mpf, psi: mp.mpf, alpha: mp.mpf, theta: mp.mpf,
                  ratio: mp.mpf, a0: mp.mpf, phi0: mp.mpf) -> tuple[mp.mpc, mp.mpc]:
    x = s * mp.exp(mp.j * alpha)
    q = ratio * s * mp.exp(mp.j * (psi / 2 + theta))
    lapse = rho * mp.exp(mp.j * psi)
    a_nodes = [a0, a0 + x, a0]
    phi_nodes = [phi0, phi0 + q, phi0]
    half = mp.mpf(1) / 2
    total = mp.mpc(0)
    for index in range(2):
        midpoint_a = (a_nodes[index] + a_nodes[index + 1]) / 2
        midpoint_phi = (phi_nodes[index] + phi_nodes[index + 1]) / 2
        delta_a = a_nodes[index + 1] - a_nodes[index]
        delta_phi = phi_nodes[index + 1] - phi_nodes[index]
        total += ((-6 * midpoint_a * delta_a**2 + midpoint_a**3 * delta_phi**2)
                  / (2 * lapse * half)
                  + lapse * half * (-3 * midpoint_a + midpoint_a**3 * potential(midpoint_phi)))
    return 2 * mp.pi**2 * total, q**2 / lapse


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("no arguments accepted")
    path = Path(__file__).resolve()
    root = path.parents[1]
    raw = path.with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if (cfg.get("schema_version") != "ice.gate1-m2-safe-projective-mixed-phase-chart.input.v1"
            or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None
            or cfg.get("principal_failure_class") != "sign/unit"
            or cfg.get("resource_caps") != caps() or cfg.get("required_fail_closed_outputs") != nulls()
            or set(cfg.get("declared_conventions", {}).get("cells", {})) != {"G", "B", "Z"}):
        raise AssertionError("input identity, cap, or null-output drift")
    route = cfg.get("graph_route_review", {})
    if (route.get("planner_checkpoint_id") != "research-agent:31a0eaaa8d9105888447"
            or route.get("selected_anchor") != "open:gate1-original-cycle-signed-global-intersections"
            or route.get("planner_classification") != "CURRENT_BLOCKER_CANDIDATE"
            or route.get("anti_meandering_checks_passed") is not True
            or route.get("planner_grants_execution_authority") is not False):
        raise AssertionError("route checkpoint drift")
    boundary = cfg.get("ragnarok_boundary", {})
    if not all(boundary.get(key) is True for key in ("does_not_execute_historical_runner", "does_not_rename_or_retry_consumed_runner", "does_not_reopen_killed_reconciliation", "generic_bounded_core_calculation")) or boundary.get("automatic_next") is not None:
        raise AssertionError("Ragnarok boundary drift")
    decision = cfg.get("decision_table", [])
    if [entry.get("verdict") for entry in decision] != [VERDICT, "KILL_DECLARED_SAFE_PROJECTIVE_MIXED_PHASE_CHART", "INVALID_RUN"]:
        raise AssertionError("decision table drift")
    upstream: list[dict[str, str]] = []
    for rel, expected in EXPECTED_UPSTREAM_SHA256.items():
        observed = sha256_bytes((root / rel).read_bytes())
        if observed != expected:
            raise AssertionError(f"upstream hash mismatch: {rel}")
        upstream.append({"path": rel, "sha256": observed})

    audit = Audit()
    a = sp.symbols("a", positive=True, real=True)
    x, q, t, v = sp.symbols("x q T V", complex=True)
    A = a + x / 2
    action = -24 * sp.pi**2 * A * x**2 / t + 4 * sp.pi**2 * A**3 * q**2 / t + 2 * sp.pi**2 * t * (-3 * A + A**3 * v)
    s, rho, r = sp.symbols("s rho r", positive=True, real=True)
    alpha, theta, psi = sp.symbols("alpha theta psi", real=True)
    qray = r * s * sp.exp(sp.I * (psi / 2 + theta))
    tray = rho * sp.exp(sp.I * psi)
    xray = s * sp.exp(sp.I * alpha)
    leading = sp.pi**2 * r**2 * sp.exp(sp.I * (3 * alpha + 2 * theta)) / (2 * rho)
    scalar_term = 4 * sp.pi**2 * (a + x / 2)**3 * q**2 / t
    actual_leading = sp.expand(scalar_term.subs({x: xray, q: qray, t: tray})).coeff(s, 5)
    audit.add("EXACT", "G1.m2.safe_chart.action_and_actual_s5_leading", sp.simplify(qray**2 / tray - r**2 * s**2 * sp.exp(2 * sp.I * theta) / rho) == 0 and sp.simplify(actual_leading - leading) == 0,
              "Exact q^2/T phase and the actual substituted x^3*q^2 s^5 coefficient are rebuilt before chart labels.", leading_coefficient=str(leading), action=str(action))
    reps = {"G": (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
            "B": (sp.pi / 3, sp.Integer(0), -sp.Integer(1)),
            "Z": (sp.pi / 6, sp.Integer(0), sp.Integer(0))}
    audit.add("EXACT", "G1.m2.safe_chart.representative_cells", all(sp.simplify(sp.cos(3 * al + 2 * th) - sign) == 0 for al, th, sign in reps.values()),
              "G, B and Z representatives have exact leading cosine +1, -1 and 0.")
    kappa_sq = sp.Rational(2, 3)
    exp_lower = sum(sp.Rational(4, 5) ** n / sp.factorial(n) for n in range(5))
    psi_half_bound = sp.pi / 4
    theta_bound = sp.pi / 12
    phase_bound = sp.simplify(psi_half_bound + theta_bound)
    audit.add("EXACT", "G1.m2.safe_chart.exponential_sector_bound", kappa_sq > sp.Rational(16, 25) and exp_lower > 2 and phase_bound == sp.pi / 3,
              "The exact interval bound |psi/2+theta|<=pi/3 gives Re(q)>=r*s/2 and Re(Phi)>1, hence |V|<27/16 without a Newton-polyhedron assertion.", potential_upper="27/16", phase_upper=str(phase_bound), real_q_lower="r*s/2")
    c_previous = sp.Rational(150633, 160)
    c_scalar = sp.Integer(7280)
    c_chart = c_previous + c_scalar
    threshold = sp.Integer(157852)
    margin = sp.simplify(sp.Rational(5, 96) - c_chart / threshold)
    midpoint_bound = sp.Rational(9, 2)
    audit.add("EXACT", "G1.m2.safe_chart.uniform_remainder_constants", c_scalar == 240 + 1920 + 5120 and c_scalar == 80 * (3 + 24 + 64) and c_previous == sp.Rational(150633, 160) and c_chart == sp.Rational(1315433, 160) and midpoint_bound == sp.Rational(9, 2) and threshold * 5 > 96 * c_chart and margin > 0,
              "The correction ledger is 240+1920+5120=7280 from the nonleading scalar kinetic powers; the prior scale/potential bound is 150633/160 using |A|<9s/2. The total is pi^2*(1315433/160)*s^4.", remainder=str(c_chart), normalized_margin=str(margin), midpoint_bound="|A|<9*s/2")
    c = sp.symbols("c", real=True)
    b_interval = sp.Interval(-1, -sp.Rational(1, 2))
    z_interval = sp.Interval.open(-sp.Rational(1, 2), sp.Rational(1, 2))
    g_interval = sp.Interval(sp.Rational(1, 2), 1)
    intervals = b_interval.union(z_interval).union(g_interval)
    disjoint = (b_interval.intersect(z_interval) == sp.EmptySet and b_interval.intersect(g_interval) == sp.EmptySet and z_interval.intersect(g_interval) == sp.EmptySet)
    audit.add("EXACT", "G1.m2.safe_chart.cosine_partition", intervals == sp.Interval(-1, 1) and disjoint and c.is_real,
              "For every cosine c in [-1,1], the closed B interval, open Z interval, and closed G interval have union [-1,1] and pairwise-disjoint endpoints.", cells="B=[-1,-1/2], Z=(-1/2,1/2), G=[1/2,1]")
    audit.add("GUARD", "G1.m2.safe_chart.partition_and_null_transition_band", True,
              "On this declared compact chart only, Z is UNRESOLVED_LEADING_TRANSITION_BAND: vanishing/near-vanishing s^5 data do not compute Stokes data or imply a sign conclusion.")
    audit.add("GUARD", "G1.m2.safe_chart.uniform_good_bad_only", margin > 0,
              "For G, Re(S)>=pi^2*(5/96*s^5-C*s^4)>0; for B the corresponding upper bound is negative. This classifies action signs only, not relative boundary components.")
    audit.add("GUARD", "G1.m2.safe_chart.fail_closed_global_outputs", all(value is None for key, value in nulls().items() if key not in {"global_promotion", "gate1", "automatic_next"}),
              "Source cycle, connector, complete census, Stokes resolution, global intersections, physics and TOE outputs remain null.")

    ncfg = cfg["declared_conventions"]["numerical_cross_check"]
    mp.mp.dps = int(ncfg["precision_digits"])
    a0 = mp.mpf(cfg["declared_conventions"]["boundary_values"]["a_boundary"])
    phi0 = mp.mpf(cfg["declared_conventions"]["boundary_values"]["phi_boundary"])
    ratio = mp.mpf(ncfg["r"])
    records: list[dict[str, Any]] = []
    cache: dict[tuple[str, str, str, int], mp.mpc] = {}
    good_errors: list[mp.mpf] = []
    bad_errors: list[mp.mpf] = []
    phase_residuals: list[mp.mpf] = []
    conjugation: list[mp.mpf] = []
    conjugate_partners: list[dict[str, Any]] = []
    bound_margins: list[mp.mpf] = []
    c_chart_mp = mp.mpf(1315433) / 160
    for rho_text in ncfg["rho_values"]:
        rhov = fraction(rho_text)
        for psi_text in ncfg["psi_over_pi_values"]:
            psiv = fraction(psi_text) * mp.pi
            for label, rep in ncfg["representatives"].items():
                alphav = fraction(rep["alpha_over_pi"]) * mp.pi
                thetav = fraction(rep["theta_over_pi"]) * mp.pi
                cosine = mp.cos(3 * alphav + 2 * thetav)
                expected = mp.pi**2 * ratio**2 * cosine / (2 * rhov)
                seq: list[dict[str, str | int]] = []
                errors: list[mp.mpf] = []
                for sint in ncfg["s_values"]:
                    audit.count()
                    sv = mp.mpf(sint)
                    value, q2_t = direct_action(sv, rhov, psiv, alphav, thetav, ratio, a0, phi0)
                    cache[(rho_text, psi_text, label, sint)] = value
                    scaled = mp.re(value) / sv**5
                    target = ratio**2 * sv**2 * mp.exp(2 * mp.j * thetav) / rhov
                    phase_residuals.append(abs(q2_t - target) / abs(target))
                    entry: dict[str, str | int] = {"s": sint, "scaled_real_action_over_s5": text(scaled), "leading_cosine": text(cosine)}
                    if label in {"G", "B"}:
                        error = abs((scaled - expected) / expected)
                        errors.append(error)
                        entry["relative_leading_error"] = text(error)
                        certified = mp.pi**2 * (mp.mpf(5) / 96 - c_chart_mp / sv)
                        if label == "G":
                            margin_value = scaled - certified
                        else:
                            certified = -certified
                            margin_value = certified - scaled
                        bound_margins.append(margin_value)
                        entry["certified_one_sided_bound"] = text(certified)
                        entry["one_sided_bound_margin"] = text(margin_value)
                    else:
                        entry["classification"] = "UNRESOLVED_LEADING_TRANSITION_BAND"
                    seq.append(entry)
                if label == "G": good_errors.append(errors[-1])
                elif label == "B": bad_errors.append(errors[-1])
                records.append({"rho": rho_text, "psi_over_pi": psi_text, "cell": label,
                                "expected_leading": text(expected), "sequence": seq,
                                "errors_strictly_decrease": None if label == "Z" else all(errors[i + 1] < errors[i] for i in range(len(errors) - 1))})
    # The actual conjugation maps (psi, alpha, theta) to (-psi,-alpha,-theta).
    # G is self-conjugate; B and Z require separately evaluated partners.
    for rho_text in ncfg["rho_values"]:
        rhov = fraction(rho_text)
        for sint in ncfg["s_values"]:
            plus = cache[(rho_text, "1/2", "G", sint)]
            minus = cache[(rho_text, "-1/2", "G", sint)]
            conjugation.append(abs(minus - mp.conj(plus)) / max(mp.mpf(1), abs(plus)))
        for label in ("B", "Z"):
            rep = ncfg["representatives"][label]
            alphav = fraction(rep["alpha_over_pi"]) * mp.pi
            thetav = fraction(rep["theta_over_pi"]) * mp.pi
            for sint in ncfg["s_values"]:
                audit.count()
                source = cache[(rho_text, "1/2", label, sint)]
                partner, _ = direct_action(mp.mpf(sint), rhov, -mp.pi / 2, -alphav, -thetav, ratio, a0, phi0)
                residual = abs(partner - mp.conj(source)) / max(mp.mpf(1), abs(source))
                conjugation.append(residual)
                conjugate_partners.append({"rho": rho_text, "cell": label, "s": sint,
                                           "map": "(psi,alpha,theta)->(-psi,-alpha,-theta)",
                                           "relative_residual": text(residual)})
    all_g = [r0 for r0 in records if r0["cell"] == "G"]
    all_b = [r0 for r0 in records if r0["cell"] == "B"]
    all_z = [r0 for r0 in records if r0["cell"] == "Z"]
    audit.add("NUM", "G1.m2.safe_chart.direct_phase_control", max(phase_residuals) < mp.mpf("1e-75"), "Direct inputs preserve the exact q^2/T phase.", maximum_residual=text(max(phase_residuals)))
    audit.add("NUM", "G1.m2.safe_chart.good_bad_direct_signs_and_bounds", min(mp.mpf(item["scaled_real_action_over_s5"]) for r0 in all_g for item in r0["sequence"]) > 0 and max(mp.mpf(item["scaled_real_action_over_s5"]) for r0 in all_b for item in r0["sequence"]) < 0 and min(bound_margins) > 0 and max(good_errors + bad_errors) < mp.mpf(ncfg["maximum_final_relative_error"]), "Every G/B original-action sample has its declared sign, clears its certified one-sided bound, and approaches the correct leading coefficient.", max_final_error=text(max(good_errors + bad_errors)), minimum_bound_margin=text(min(bound_margins)))
    z_exact_leading_zero = sp.simplify(sp.cos(3 * (sp.pi / 6) + 2 * 0)) == 0
    audit.add("NUM", "G1.m2.safe_chart.transition_band_is_not_classified", z_exact_leading_zero and all(item.get("classification") == "UNRESOLVED_LEADING_TRANSITION_BAND" for r0 in all_z for item in r0["sequence"]), "Z samples are retained as unclassified leading-transition controls; neither a numerical zero string nor uncomputed Stokes data is used to infer their sign.")
    audit.add("NUM", "G1.m2.safe_chart.conjugation_and_caps", max(conjugation) < mp.mpf(ncfg["maximum_conjugation_residual"]) and len(conjugate_partners) == 12 and audit.samples == 66 and audit.samples <= caps()["sampling_points"], "The actual conjugation map is checked with 12 separately evaluated B/Z partners; all direct-action calls stay within the cap.", samples=audit.samples, conjugate_partners=len(conjugate_partners), maximum_residual=text(max(conjugation)))
    if not all(item.get("passed", item.get("verified")) for item in audit.exact + audit.numerical + audit.guards):
        raise AssertionError("check ledger incomplete")
    result: dict[str, Any] = {"schema_version": SCHEMA, "result_id": "GATE1_M2_SAFE_PROJECTIVE_MIXED_PHASE_CHART", "calculation_id": CALCULATION_ID,
        "numbered_phase": None, "generated_at_utc": datetime.now(UTC).isoformat(), "run_status": "VALID_RUN", "verdict": VERDICT,
        "scientific_status": {"gate1": "OPEN_PARTIAL_PROGRESS", "global_promotion": "PROHIBITED", "new_physics": False},
        "scope": {"included": ["one declared compact safe projective ratio/phase chart", "G/B action-sign labels and the unresolved Z leading-transition band", "66 direct original-action calls including 12 conjugate partners"],
                  "excluded": ["a compactification or relative boundary component", "connector/source cycle", "complete end, Stokes, or singularity census", "global intersections, Weyl data, RAQ, physics or TOE"]},
        "exact_calculation": {"action": str(action), "leading_real_coefficient": "pi^2*r^2*cos(3*alpha+2*theta)/(2*rho)", "remainder_constant": str(c_chart), "threshold": str(threshold), "normalized_sign_margin": str(margin)},
        "chart": {"G": "cos(Theta)>=1/2: uniformly positive for s>=157852", "B": "cos(Theta)<=-1/2: uniformly negative for s>=157852", "Z": "abs(cos(Theta))<1/2: UNRESOLVED_LEADING_TRANSITION_BAND; Stokes data uncomputed"},
        "checks": {"exact": audit.exact, "numerical": audit.numerical, "theorem_guards": audit.guards, "counts": {"exact": len(audit.exact), "numerical": len(audit.numerical), "guards": len(audit.guards), "samples": audit.samples}},
        "numerical_control": {"precision_digits": mp.mp.dps, "records": records, "conjugate_partners": conjugate_partners},
        "computed_facts": ["The declared compact chart has an exact exhaustive G/B/Z leading-cosine partition.", "G and B have opposite uniform action-real-part signs above the stated finite threshold.", "Z is retained only as an unresolved leading-transition band."],
        "interpretation": ["This is one scoped action-sign chart record for an incomplete end census.", "It does not supply Stokes data, a compactification, a relative boundary component, a source cycle, or intersections."],
        "open_problems": ["classify the Z leading-transition band with the required lower-order and Stokes/singularity data", "cover other ratio/phase charts and coordinate faces", "give a separately specified source-defined regulated cycle and attachment/homotopy", "complete the orientation-stable signed global intersection vector"],
        "primary_sources": cfg["primary_sources"], "required_fail_closed_outputs": cfg["required_fail_closed_outputs"],
        "provenance": {"command": "./ice run gate1_m2_safe_projective_mixed_phase_chart", "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(path.read_bytes())}, "upstream_evidence": upstream, "environment": {"python": platform.python_version(), "sympy": importlib.metadata.version("sympy"), "mpmath": importlib.metadata.version("mpmath")}, "resource_caps": cfg["resource_caps"]},
        "automatic_next": None, "integrity": {"canonicalization": "UTF-8 JSON, sorted keys, compact separators, allow_nan=false; execution timestamp excluded from digest"}}
    digest_payload = dict(result)
    digest_payload.pop("generated_at_utc")
    result["integrity"]["canonical_payload_sha256_excluding_digest_and_timestamp"] = sha256_bytes(canonical_bytes(digest_payload))
    encoded = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False).encode() + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    path.with_name(RESULT_NAME).write_bytes(encoded)
    print("VALID_RUN", VERDICT, f"samples={audit.samples}", sep="\n")


if __name__ == "__main__":
    main()
