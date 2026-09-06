#!/usr/bin/env python3
"""Certify one fixed-box constrained continuum endpoint root, or report INCONCLUSIVE.

Run only through ./ice run, with ICE_CAPD_BVP_BINARY pointing to the pinned
external executable. This is a local real-branch supporting result, not a
source cycle, gauge-preserving discrete action, or global intersection result.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import selectors
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as Q

import numpy as np
from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
INPUT = HERE / "STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_INPUTS.json"
OUTPUT = HERE / "STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_RESULT.json"
HELPER = HERE / "starobinsky_continuum_endpoint_certificate.cpp"


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def ball(q):
    q = Q(q)
    return arb(fmpq(q.numerator, q.denominator))


def bounds(lo, hi):
    if hi < lo:
        raise ValueError("reversed bounds")
    value = arb((lo + hi) / 2, (hi - lo) / 2)
    if not (value.lower() <= lo and value.upper() >= hi):
        raise ArithmeticError("interval import lost an endpoint")
    return value


def decode(record):
    lo = Q(float.fromhex(record["lower_hex"]))
    hi = Q(float.fromhex(record["upper_hex"]))
    return bounds(ball(lo), ball(hi))


def dyadic(value):
    mantissa, exponent = value.man_exp()
    return Q(int(mantissa)) * Q(2) ** int(exponent)


def record(value):
    if not value.is_finite():
        raise ArithmeticError("nonfinite certificate interval")
    return {
        "lower_exact": str(dyadic(value.lower())),
        "upper_exact": str(dyadic(value.upper())),
        "display_only": value.str(18),
    }


def array_records(values):
    return [array_records(x) if isinstance(x, list) else record(x) for x in values]


class RationalInterval:
    """Independent exact rational arithmetic for the final inclusion test."""

    def __init__(self, lo, hi=None):
        self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("reversed rational interval")

    @classmethod
    def from_ball(cls, x):
        return cls(dyadic(x.lower()), dyadic(x.upper()))

    def __add__(self, other):
        return RationalInterval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self):
        return RationalInterval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        p = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return RationalInterval(min(p), max(p))

    def magnitude(self):
        return max(abs(self.lo), abs(self.hi))

    def record(self):
        return {"lower_exact": str(self.lo), "upper_exact": str(self.hi)}


def bounded_child(command, timeout, limit):
    started = time.monotonic()
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          start_new_session=True) as child:
        streams = {"stdout": bytearray(), "stderr": bytearray()}
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ, "stdout")
                selector.register(child.stderr, selectors.EVENT_READ, "stderr")
                while selector.get_map():
                    if time.monotonic() - started > timeout:
                        raise TimeoutError("declared CAPD child timeout")
                    for key, _ in selector.select(timeout=0.1):
                        chunk = os.read(key.fileobj.fileno(), 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        streams[key.data].extend(chunk)
                        if len(streams[key.data]) > limit:
                            raise RuntimeError("declared CAPD stream limit")
            child.wait(timeout=max(0.01, timeout - (time.monotonic() - started)))
        except BaseException:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
            raise
    stdout, stderr = (bytes(streams[k]) for k in ("stdout", "stderr"))
    if child.returncode:
        raise RuntimeError(f"CAPD exited {child.returncode}: {stderr[:2000]!r}")
    return json.loads(stdout), {
        "returncode": child.returncode, "elapsed_seconds": time.monotonic() - started,
        "stdout_bytes": len(stdout), "stderr_bytes": len(stderr),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr": stderr.decode("utf-8", errors="replace"),
    }


def potential(phi):
    b = (arb(2) / 3).sqrt()
    e = (-b * phi).exp()
    return 3 * (1 - e) ** 2 / 4, 3 * b * e * (1 - e) / 2, 2 * e**2 - e


def physical_rhs(z):
    a, u, phi, v = z[:4]
    V, Vp, _ = potential(phi)
    return [u, (1-u*u)/(2*a) - a*v*v/4 - a*V/2, v, Vp-3*u*v/a]


def analytic_augmented_jacobian(z):
    a, u, phi, v, T = z
    V, Vp, Vpp = potential(phi)
    D = [[arb(0), arb(1), arb(0), arb(0)],
         [-(1-u*u)/(2*a*a)-v*v/4-V/2, -u/a, -a*Vp/2, -a*v/2],
         [arb(0), arb(0), arb(0), arb(1)],
         [3*u*v/(a*a), -3*v/a, Vpp, -3*u/a]]
    f = physical_rhs(z)
    return [[T*D[i][j] for j in range(4)] + [f[i]] for i in range(4)] + [[arb(0)]*5]


def zero_in(x):
    return bool(x.lower() <= 0 <= x.upper())


def certify(raw, inputs):
    centre_q = [Q(float(inputs["centre_decimal"][k])) for k in ("u", "v", "T")]
    radius_q = [Q(2)**e for e in inputs["radius_binary_exponents"]]
    centre, radius = list(map(ball, centre_q)), list(map(ball, radius_q))
    Y = [bounds(c-r, c+r) for c, r in zip(centre, radius)]
    a, phi = [ball(Q(inputs["boundary"][k])) for k in ("a", "phi")]
    point = [a, centre[0], phi, centre[1], centre[2]]
    point_end = list(map(decode, raw["point_flow"]["endpoint"]))
    M = [[decode(x) for x in row] for row in raw["box_flow"]["derivative"]]
    V, _, _ = potential(phi)
    constraint = centre[0]**2 - 1 - a*a*(centre[1]**2/2-V)/3
    F = [point_end[0]-a, point_end[2]-phi, constraint]
    J = [[M[i][j] for j in (1, 3, 4)] for i in (0, 2)]
    J.append([2*Y[0], -a*a*Y[1]/3, arb(0)])

    # The floating inverse only chooses a fixed real dyadic preconditioner.
    # Every conclusion below uses enclosing ball or exact rational arithmetic.
    B_float = np.linalg.inv(np.array([[float(x.mid()) for x in row] for row in J]))
    B_q = [[Q(float(x)) for x in row] for row in B_float]
    B = [[ball(x) for x in row] for row in B_q]
    defect = [[arb(int(i == j))-sum((B[i][k]*J[k][j] for k in range(3)), arb(0))
               for j in range(3)] for i in range(3)]
    K = [centre[i]-sum((B[i][k]*F[k] for k in range(3)), arb(0))
         + sum((defect[i][j]*bounds(-radius[j], radius[j]) for j in range(3)), arb(0))
         for i in range(3)]
    strict_ball = [bool(K[i].lower() > centre[i]-radius[i] and
                        K[i].upper() < centre[i]+radius[i]) for i in range(3)]

    R = RationalInterval
    rf, rj = list(map(R.from_ball, F)), [[R.from_ball(x) for x in row] for row in J]
    rb = [[R(x) for x in row] for row in B_q]
    rq = [[R(int(i == j))-sum((rb[i][k]*rj[k][j] for k in range(3)), R(0))
           for j in range(3)] for i in range(3)]
    rk = [R(centre_q[i])-sum((rb[i][k]*rf[k] for k in range(3)), R(0))
          + sum((rq[i][j]*R(-radius_q[j], radius_q[j]) for j in range(3)), R(0))
          for i in range(3)]
    margins = [min(rk[i].lo-(centre_q[i]-radius_q[i]),
                   centre_q[i]+radius_q[i]-rk[i].hi) for i in range(3)]
    weighted_norm = max(sum(rq[i][j].magnitude()*radius_q[j]/radius_q[i]
                            for j in range(3)) for i in range(3))

    input_checks = []
    for i in range(3):
        # Exact endpoint checks prevent an accidentally different backend box.
        for field, expected in (("centre", R(centre_q[i])), ("radii", R(radius_q[i])),
                                ("box", R(centre_q[i]-radius_q[i], centre_q[i]+radius_q[i]))):
            entry = raw[field][i]
            input_checks.append(Q(float.fromhex(entry["lower_hex"])) == expected.lo and
                                Q(float.fromhex(entry["upper_hex"])) == expected.hi)
    for i, key in enumerate(("a", "phi")):
        entry = raw["boundary_enclosures"][i]
        input_checks.append(Q(float.fromhex(entry["lower_hex"])) <= Q(inputs["boundary"][key])
                            <= Q(float.fromhex(entry["upper_hex"])))

    analytic = analytic_augmented_jacobian(point)
    emitted = [[decode(x) for x in row] for row in raw["initial_augmented_jacobian"]]
    jacobian_checks = [zero_in(analytic[i][j]-emitted[i][j]) for i in range(5) for j in range(5)]
    time_differences = {}
    for name in ("point_flow", "box_flow"):
        endpoint = list(map(decode, raw[name]["endpoint"]))
        rhs = physical_rhs(endpoint)
        time_differences[name] = [decode(raw[name]["derivative"][i][4])-rhs[i] for i in range(4)]
    time_checks = [zero_in(x) for row in time_differences.values() for x in row]

    free = raw["free_flow_control"]
    free_endpoint = list(map(ball, [Q(17,8), Q(1,4), Q(15,16), Q(-1,8), Q(1,2)]))
    free_matrix = [[arb(int(i == j)) for j in range(5)] for i in range(5)]
    free_matrix[0][1], free_matrix[0][4] = arb(1)/2, arb(1)/4
    free_matrix[2][3], free_matrix[2][4] = arb(1)/2, -arb(1)/8
    free_checks = [bool(exact in decode(got)) for exact, got in zip(free_endpoint, free["endpoint"])]
    free_checks += [bool(free_matrix[i][j] in decode(free["derivative"][i][j]))
                    for i in range(5) for j in range(5)]
    tubes = {name: decode(raw[name]["whole_time_tube"][0]) for name in ("point_flow", "box_flow")}
    domain_valid = all(x.lower() > 0 for x in tubes.values()) and Y[2].lower() > 0
    completed = all(Q(float.fromhex(raw[name]["step_end_times"][-1]["lower_hex"])) == 1 and
                    Q(float.fromhex(raw[name]["step_end_times"][-1]["upper_hex"])) == 1
                    for name in ("point_flow", "box_flow", "free_flow_control"))
    controls = {
        "declared_input_enclosures_match": all(input_checks),
        "all_flows_reach_s_one": completed,
        "positive_a_whole_time_and_positive_T": bool(domain_valid),
        "analytic_initial_Dg_overlap_25_entries": all(jacobian_checks),
        "autonomous_T_sensitivity_overlap_8_entries": all(time_checks),
        "exact_free_flow_endpoint_and_C1_30_entries": all(free_checks),
    }
    certified = (all(controls.values()) and all(strict_ball) and
                 all(m > 0 for m in margins) and weighted_norm < 1)
    return {
        "verdict": ("CERTIFIED_UNIQUE_REGULAR_REAL_CONSTRAINED_ENDPOINT_ROOT_IN_DECLARED_BOX"
                    if certified else "INCONCLUSIVE_CONTINUUM_ENDPOINT_CERTIFICATE"),
        "controls": controls,
        "certificate": {
            "shooting_order": ["u_minus", "v_minus", "T"],
            "residual_order": ["a_endpoint-a_boundary", "phi_endpoint-phi_boundary", "C_initial"],
            "Y": array_records(Y), "F_at_centre": array_records(F), "DF_over_Y": array_records(J),
            "B_exact_binary64_hex": [[float(x).hex() for x in row] for row in B_float],
            "K_arb": array_records(K), "strict_inclusion_arb": strict_ball,
            "K_independent_exact_rational": [x.record() for x in rk],
            "strict_margin_exact_rational": [str(x) for x in margins],
            "strict_margin_over_radius_display": [float(x/r) for x, r in zip(margins, radius_q)],
            "weighted_defect_norm_upper_exact_rational": str(weighted_norm),
            "weighted_defect_norm_upper_display": float(weighted_norm),
            "regularity_criterion": "||D^-1(I-B[DF])D||_infinity < 1; D=diag(radii)",
            "positive_a_whole_time": {k: record(v) for k, v in tubes.items()},
        },
        "diagnostics": {
            "time_sensitivity_difference": {k: array_records(v) for k, v in time_differences.items()},
            "jacobian_overlap_is_consistency_only": True,
            "rational_check_reuses_CAPD_flow_enclosures": True,
        },
    }


def main():
    started = time.monotonic()
    inputs = json.loads(INPUT.read_text())
    result = {
        "schema_version": 1, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "question": "Does one declared box contain a unique regular zero of the constrained continuum endpoint map?",
        "scope": "SUPPORTING_METHOD; fixed exact real boundary data and one local shooting box",
        "non_claim": "No original integration cycle, global saddle census/intersection, gauge/FP/BFV source, continuum quantum measure or physical/empirical claim.",
        "dominant_failure_class": "solver",
        "inputs": inputs,
        "provenance": {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=HERE, text=True).strip(),
            "runner_sha256": sha(__file__), "helper_source_sha256": sha(HELPER),
            "inputs_sha256": sha(INPUT), "uv_lock_sha256": sha(HERE.parent / "uv.lock"),
            "python": sys.version, "platform": platform.platform(),
            "packages": {name: importlib.metadata.version(name) for name in ("numpy", "python-flint")},
            "entry_command": "ICE_CAPD_BVP_BINARY=<pinned external binary> ./ice run starobinsky_continuum_endpoint_certificate",
        },
    }
    try:
        binary = Path(os.environ["ICE_CAPD_BVP_BINARY"]).resolve(strict=True)
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise ValueError("backend is not an executable regular file")
        if sha(binary) != inputs["backend"]["binary_sha256"]:
            raise ValueError("backend executable hash mismatch")
        if sha(HELPER) != inputs["backend"]["source_sha256"]:
            raise ValueError("backend source hash mismatch")
        args = [inputs["boundary"][k] for k in ("a", "phi")]
        args += [inputs["centre_decimal"][k] for k in ("u", "v", "T")]
        args += list(map(str, inputs["radius_binary_exponents"]))
        args += [str(inputs["taylor_order"]), str(inputs["max_steps"])]
        command = [str(binary), *args]
        result["provenance"]["actual_backend_argv"] = command
        result["provenance"]["binary_sha256"] = sha(binary)
        raw, execution = bounded_child(command, inputs["child_timeout_seconds"], inputs["child_stream_limit_bytes"])
        result["backend_execution"], result["validated_flow"] = execution, raw
        if raw["status"] != "FLOW_ENCLOSURES_COMPUTED":
            result["verdict"] = "INCONCLUSIVE_CONTINUUM_ENDPOINT_CERTIFICATE"
        else:
            with ctx.workprec(inputs["arb_precision_bits"]):
                result.update(certify(raw, inputs))
    except Exception as error:
        result["verdict"] = "INCONCLUSIVE_CONTINUUM_ENDPOINT_CERTIFICATE"
        result["execution_error"] = {"type": type(error).__name__, "message": str(error)[:2000]}
    result["elapsed_seconds"] = time.monotonic() - started
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if len(serialized.encode()) > 900_000:
        raise RuntimeError("result exceeds declared artifact budget")
    OUTPUT.write_text(serialized)
    print(json.dumps({"verdict": result["verdict"], "controls": result.get("controls"),
                      "execution_error": result.get("execution_error"),
                      "elapsed_seconds": result["elapsed_seconds"], "result": OUTPUT.name}))
    return int("execution_error" in result or not all(result.get("controls", {}).values()))


if __name__ == "__main__":
    raise SystemExit(main())
