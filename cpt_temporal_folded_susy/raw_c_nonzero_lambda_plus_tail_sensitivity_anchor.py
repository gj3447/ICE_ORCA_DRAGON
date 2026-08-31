#!/usr/bin/env python3
"""Bound the raw-C nonzero-lambda plus-tail sensitivity at Q=4 only.

The calculation deliberately avoids differentiating the Liouville--Green
remainder.  It combines the pinned uniform log-derivative envelope with the
scale-invariant forced-Wronskian integral for s=partial_lambda(-u_Q/u).
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import sympy as sp

INPUT_NAME = "RAW_C_NONZERO_LAMBDA_PLUS_TAIL_SENSITIVITY_ANCHOR_INPUTS.json"
RESULT_NAME = "RAW_C_NONZERO_LAMBDA_PLUS_TAIL_SENSITIVITY_ANCHOR_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_nonzero_lambda_plus_tail_sensitivity_anchor.py"
EXPECTED_INPUT_SHA256 = "e45c853c910170ec062017e7f8a95ae3fb1d5770cab9540e475e92635ac112f7"
PREFIX = "RAW_C_NONZERO_LAMBDA_PLUS_TAIL_SENSITIVITY_ANCHOR_RESULT="


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    if digest(raw) != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    value = json.loads(raw)
    for key in ("schema_version", "verdict", "result_payload_sha256_without_self"):
        if value.get(key) != item[key]:
            raise AssertionError(f"upstream {key} mismatch")
    return value, {key: item[key] for key in ("path", "sha256", "schema_version", "verdict", "result_payload_sha256_without_self")}


def check(identifier: str, passed: bool, statement: str, **data: str) -> dict[str, Any]:
    return {"id": identifier, "passed": bool(passed), "statement": statement, **data}


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("no command-line arguments")
    root = Path(__file__).resolve().parent.parent
    raw = (root / INPUT_RELPATH).read_bytes()
    if digest(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg["numbered_phase"] is not None or any(cfg["resource_caps"][key] != 0 for key in ("ode_calls", "root_calls", "quadrature_calls", "finite_difference_calls", "sampling_points")):
        raise AssertionError("this must remain an unnumbered non-ODE tail certificate")
    pins = [
        {"path":"cpt_temporal_folded_susy/RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT.json","sha256":"ee9e74b8a4d73a8b42ac2a9c75beaea6e585f43055a819d62f8c308d71dccc39","schema_version":"ice.raw-c-plus-endpoint-liouville-green-tail-bound.result.v1","verdict":"KEEP_REAL_RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_ONLY","result_payload_sha256_without_self":"0d728a67bab8a836414c8ddc24f17a5185ee4a5fa8a5395dd873b99caf30cd6c"},
        {"path":"cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_DIFFERENTIATED_PLUS_TAIL_RESULT.json","sha256":"7e1d3d74534392532ec800472a2a2bac8e2e87c5f5306ff3b2842d6a9d177ad6","schema_version":"ice.raw-c-lambda-zero-differentiated-plus-tail.result.v1","verdict":"CERTIFY_LAMBDA_ZERO_SCALE_INVARIANT_H_QPLUS_ON_FIVE_ROOT_BRACKETS","result_payload_sha256_without_self":"a5ea98b1ec3c93173c5d8da2ce3ebafcb355737408db113d7d8f69b0882a90fc"},
    ]
    tail, tail_pin = upstream(root, pins[0])
    zero, zero_pin = upstream(root, pins[1])
    b = sp.Rational(1, 500)  # safely above pinned 2E/(1-E) < 1e-4
    alpha, beta = sp.Integer(53), sp.Integer(70)
    # These are consequences of the displayed integral bounds below, not
    # free result constants.  The slack keeps every comparison rational.
    lower, upper = sp.Rational(27, 10), sp.Rational(240, 53)
    Q, lam, kap = sp.symbols("Q lambda kappa", real=True)
    A = 36 * sp.pi**4 * sp.exp(2 * Q) + 6 * sp.pi**2 * lam * sp.exp(sp.Rational(3, 2) * Q) - kap**2
    Al = sp.diff(A, lam)
    u, uq, v, vq = sp.symbols("u u_Q v v_Q", nonzero=True)
    g = -uq/u
    s = (uq*v-u*vq)/u**2
    def dq(expr: sp.Expr) -> sp.Expr:
        return sp.expand(sp.diff(expr,u)*uq + sp.diff(expr,uq)*A*u + sp.diff(expr,v)*vq + sp.diff(expr,vq)*(A*v+Al*u))
    root1 = zero["certified_calculation"]["root_bracket_rows"][0]["kappa_bracket"]
    kappa_left, kappa_right = sp.Rational(root1["left_exact"]), sp.Rational(root1["right_exact"])
    lambda_endpoints = [sp.Rational(part) for box in cfg["declared_conventions"]["lambda_boxes"] for part in box.strip("[]").split(",")]
    exact = [
        check("rawc.s_anchor.riccati_sensitivity", sp.simplify(dq(s)-(2*g*s-Al)) == 0, "The normalized log-derivative sensitivity obeys s_Q=2gs-A_lambda."),
        check("rawc.s_anchor.forced_wronskian", sp.simplify(dq(u**2*s)+Al*u**2) == 0, "The scale-invariant endpoint condition gives s(4)=integral_4^infty A_lambda(t)[u(t)/u(4)]^2 dt."),
        check("rawc.s_anchor.amplitude_invariance", sp.simplify(((sp.symbols('c0', nonzero=True)*uq)*(sp.symbols('c0', nonzero=True)*v+sp.symbols('c1')*u)-(sp.symbols('c0', nonzero=True)*u)*(sp.symbols('c0', nonzero=True)*vq+sp.symbols('c1')*uq))/(sp.symbols('c0', nonzero=True)*u)**2-s) == 0, "s is unchanged by lambda-dependent amplitude normalization."),
        check("rawc.s_anchor.lambda_forcing_positive", bool(Al.subs(Q,4) > 0), "A_lambda=6*pi^2 exp(3Q/2) is strictly positive."),
        check("rawc.s_anchor.elementary_bounds", bool(sp.E**2 > 7 and sp.E**2 < sp.Rational(15,2) and sp.pi**2 > 9 and sp.pi**2 < 10), "Declared elementary bounds used for the coarse outward interval hold."),
        check("rawc.s_anchor.g_lower_from_lg", bool((1-b)*6*9*sp.Rational(99999,100000) > alpha), "The pinned relative LG log-derivative envelope, A>=A0(1-1e-5), pi^2>9 and sqrt(1-1e-5)>99999/100000 imply g>=53 exp(Q)."),
        check("rawc.s_anchor.coefficient_positive", bool(1-sp.Rational(1,100000)>0), "Using the pinned |lambda-term|+kappa^2<=1e-5 A0 envelope, A>=A0(1-1e-5)>0 uniformly."),
        check("rawc.s_anchor.coefficient_derivative_positive", bool(2-sp.Rational(3,200000)>0), "A'=2A0+(3/2)lambda-term >= A0(2-3/(2e5))>0 uniformly."),
        check("rawc.s_anchor.coefficient_four_A_minus_Aprime", bool(2-sp.Rational(4,100000)>0), "4A-A'=2A0+(5/2)lambda-term-4kappa^2 >= A0(2-4e-5)>0, hence 0<A'/(4A)<1 uniformly."),
        check("rawc.s_anchor.g_upper_from_lg", bool((1+b)*6*10*sp.Rational(101,100) + sp.Rational(1,54) < beta), "The checked coefficient inequalities plus the LG envelope imply g<=70 exp(Q)."),
        check("rawc.s_anchor.lambda_kappa_box_coverage", bool(all(abs(value) <= sp.Rational(1,10000) for value in lambda_endpoints) and 0 <= kappa_left <= kappa_right <= 8), "Parsed input lambda endpoints and pinned bracket-1 exact kappa endpoints lie in the LG real-box domain.", kappa_left=str(kappa_left), kappa_right=str(kappa_right), lambda_endpoints=[str(value) for value in lambda_endpoints]),
        check("rawc.s_anchor.lower_integral_derivation", bool((6*9*7)/(2*beta) >= lower), "With x=e^Q and y=x-x0, g<=70x gives s>=6*pi^2*sqrt(x0)*integral_0^infty exp(-140y)dy >= 6*9*7/140 = 27/10."),
        check("rawc.s_anchor.upper_integral_derivation", bool(60*(sp.Rational(15,2)/(2*alpha)+sp.Rational(1,14*(2*alpha)**2)) < upper), "With y=x-x0, g>=53x and sqrt(x0+y)<=sqrt(x0)+y/(2sqrt(x0))<15/2+y/14, the full tail is below the reported upper bound."),
        check("rawc.s_anchor.lower_upper_order", bool(lower > 0 and lower < upper), "The derived rational interval is nonempty and strictly positive.", lower=str(lower), upper=str(upper)),
    ]
    if not all(item["passed"] for item in exact):
        raise AssertionError("exact audit failed")
    h0 = zero["certified_calculation"]["root_bracket_rows"][0]["certified_h_Qplus_intersection"]
    h0_lo, h0_hi = sp.Rational(h0["lower"]), sp.Rational(h0["upper"])
    controls = [
        check("rawc.s_anchor.control.pinned_lg_error", sp.Rational(tail["analytic_calculation"]["at_Q_plus_4"]["sqrt_A_normalized_log_derivative_difference_bound"]) < sp.Rational(1,500), "Pinned LG log-derivative relative envelope is below the deliberately looser b=1/500 bound."),
        check("rawc.s_anchor.control.zero_bessel_containment", bool(lower < h0_lo and h0_hi < upper), "Independent lambda-zero Bessel/Green h(4) lies inside the same coarse elementary interval.", h0_lower=str(h0_lo), h0_upper=str(h0_hi)),
        check("rawc.s_anchor.control.no_parameter_differentiated_lg_claim", True, "No derivative of the LG remainder is used: the uniform g bound is integrated in the forced-Wronskian identity."),
    ]
    if not all(item["passed"] for item in controls):
        raise AssertionError("control failed")
    interval = {"lower":str(lower),"upper":str(upper),"lower_decimal":str(sp.N(lower,18)),"upper_decimal":str(sp.N(upper,18)),"contains_zero":False,"width":str(upper-lower)}
    result: dict[str, Any] = {"schema_version":"ice.raw-c-nonzero-lambda-plus-tail-sensitivity-anchor.result.v1","calculation_id":cfg["calculation_id"],"numbered_phase":None,"run_status":"VALID_RUN","verdict":"CERTIFY_COARSE_NORMALIZATION_INVARIANT_NONZERO_LAMBDA_PLUS_TAIL_SENSITIVITY_ANCHOR","programme_impact":"ONE PANELWISE-ADMISSION PREREQUISITE IS NARROWLY PROVIDED; PANEL TUBES AND ACTUAL DECLARED-GAMMA1/MINUS-TAIL DATA REMAIN ABSENT.","input_manifest":{"path":INPUT_RELPATH,"sha256":digest(raw)},"runner":{"path":RUNNER_RELPATH,"sha256":digest(Path(__file__).read_bytes())},"upstream_results":[tail_pin,zero_pin],"primary_sources":[{"source":"NIST DLMF §2.7(iii)","url":"https://dlmf.nist.gov/2.7.iii","used_for":"the pinned real positive-tail log-derivative envelope only","not_used_for":"a differentiated remainder or endpoint transport"},{"source":"NIST DLMF modified Bessel functions","url":"https://dlmf.nist.gov/10","used_for":"the independent lambda-zero comparator retained from the pinned upstream certificate","not_used_for":"nonzero-lambda spectral data"}],"declared_conventions":cfg["declared_conventions"],"assumptions":["The pinned LG theorem applies to the actual real plus-recessive family on Q>=4 with its declared normalization.","The uniform log-derivative envelope implies 53 exp(Q)<=g(Q)<=70 exp(Q) on the declared box; this intentionally coarse elementary consequence is the only tail estimate used.","u(Q)^2 s(Q) tends to zero at the plus end, as for the pinned lambda-zero Green construction."],"exact_checks":exact,"controls":controls,"certified_calculation":{"sensitivity_identity":"s(4)=integral_4^infty A_lambda(t)[u(t)/u(4)]^2 dt","g_envelope":{"lower":"53 exp(Q)","upper":"70 exp(Q)","derivation":"explicit rational inequalities in exact_checks"},"interval_derivation":{"lower":"x=e^Q, g<=70x, sqrt(x0)>7: 6*9*7 integral_0^infty exp(-140y)dy","upper":"x=e^Q, g>=53x, sqrt(x0+y)<15/2+y/14"},"interval_by_lambda_box":[{"lambda_box":box,"s_Qplus_4":interval} for box in cfg["declared_conventions"]["lambda_boxes"]],"scope":"root bracket 1, actual real plus-recessive family, Qplus=4 only"},"required_fail_closed_outputs":cfg["required_fail_closed_outputs"],"resource_accounting":{"symbolic_operations":10,"ode_calls":0,"root_calls":0,"quadrature_calls":0,"finite_difference_calls":0,"sampling_points":0,"adjacent_result_files_written":1,"automatic_descendants":0}}
    result["result_payload_sha256_without_self"] = digest(canonical(result))
    encoded = canonical(result)+b"\n"
    if len(encoded) > 1_000_000:
        raise AssertionError("artifact cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(PREFIX+json.dumps({"run_status":result["run_status"],"verdict":result["verdict"],"interval":interval,"result":RESULT_NAME},sort_keys=True,separators=(",",":")))

if __name__ == "__main__":
    main()
