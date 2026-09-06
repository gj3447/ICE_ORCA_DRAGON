#!/usr/bin/env python3
"""Construct a bounded local constrained principal-action interface, or fail closed.

Run through ./ice run with ICE_CAPD_PRINCIPAL_BINARY. This is a supporting
classical construction, not a quantum source, original cycle or discovery.
"""
from __future__ import annotations

import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as Q

import numpy as np
from flint import arb, ctx

import starobinsky_continuum_endpoint_certificate as base

HERE = Path(__file__).resolve().parent
INPUT = HERE / "STAROBINSKY_PRINCIPAL_BRANCH_INPUTS.json"
OUTPUT = HERE / "STAROBINSKY_PRINCIPAL_BRANCH_RESULT.json"
HELPER = HERE / "starobinsky_principal_branch_flow.cpp"
SEED = HERE / "STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_RESULT.json"
ball, bounds, decode, rec, records = base.ball, base.bounds, base.decode, base.record, base.array_records
R = base.RationalInterval


def vec(raw):
    return list(map(decode, raw))


def mat(raw):
    return [vec(row) for row in raw]


def exact_box(c, r):
    return bounds(ball(c-r), ball(c+r))


def midpoint(x):
    return Q(float(x.mid()))


def inside(x, container, strict=False):
    lo, hi = base.dyadic(x.lower()), base.dyadic(x.upper())
    a, b = base.dyadic(container.lower()), base.dyadic(container.upper())
    return a < lo and hi < b if strict else a <= lo and hi <= b


def overlap(x, y):
    return base.zero_in(x-y)


def outward_hex(x):
    lo, hi = base.dyadic(x.lower()), base.dyadic(x.upper())
    a, b = float(lo), float(hi)
    if Q(a) > lo:
        a = math.nextafter(a, -math.inf)
    if Q(b) < hi:
        b = math.nextafter(b, math.inf)
    if not (Q(a) <= lo <= hi <= Q(b)):
        raise ArithmeticError("failed outward binary64 conversion")
    return [a.hex(), b.hex()]


def determinant(A):
    if len(A) == 2:
        return A[0][0]*A[1][1]-A[0][1]*A[1][0]
    return sum(((-1)**j*A[0][j]*determinant([
        [A[i][k] for k in range(3) if k != j] for i in (1, 2)])
                for j in range(3)), arb(0))


def inverse3(A):
    d = determinant(A)
    if base.zero_in(d):
        raise ArithmeticError("interval determinant does not exclude zero")
    return [[(-1)**(i+j)*determinant([
        [A[k][l] for l in range(3) if l != i]
        for k in range(3) if k != j])/d for j in range(3)] for i in range(3)]


def mm(A, B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))), arb(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def initial(q, y):
    return [q[0], y[0], q[1], y[1], y[2]]


def constraint(q, y):
    a, phi = q
    u, v, _ = y
    V, Vp, _ = base.potential(phi)
    C = u*u-1-a*a*(v*v/2-V)/3
    Cy = [2*u, -a*a*v/3, arb(0)]
    Cq = [-2*a*(v*v/2-V)/3, a*a*Vp/3]
    return C, Cy, Cq


def momenta(z):
    a, u, _, v = z[:4]
    return [-12*arb.pi()**2*a*u, 2*arb.pi()**2*a**3*v]


def lagrangian(z):
    a, u, phi, v = z[:4]
    V, _, _ = base.potential(phi)
    return 2*arb.pi()**2*(-3*a*u*u+a**3*v*v/2-3*a+a**3*V)


class Work:
    def __init__(self, inputs, result, binary):
        self.inputs, self.result, self.binary = inputs, result, binary
        self.controls = result["controls"]
        self.flows = result["flows"]

    def flow(self, name, state, free=False):
        argv = [str(self.binary)] + [s for x in state for s in outward_hex(x)]
        argv += [str(self.inputs["taylor_order"]), str(self.inputs["max_steps"])]
        if free:
            argv.append("--free-control")
        raw, execution = base.bounded_child(argv, 8, 32768)
        self.flows[name] = {"argv": argv, "execution": execution, "raw": raw}
        if raw["status"] != "FLOW_ENCLOSURES_COMPUTED":
            raise ArithmeticError(f"{name}: {raw}")
        init = vec(raw["initial"])
        f = raw["flow"]
        check = all(inside(x, got) for x, got in zip(state, init))
        check &= inside(arb(1), decode(f["step_end_times"][-1]))
        check &= bool(decode(f["whole_time_tube"][0]).lower() > 0 and init[4].lower() > 0)
        self.controls[name+"_inputs_domain_completed"] = bool(check)
        if not check:
            raise ArithmeticError(f"{name}: invalid input/domain/completion")
        return f

    def branch(self, name, qL, qR, centres, radii):
        Y = [exact_box(c, r) for c, r in zip(centres, radii)]
        c = list(map(ball, centres))
        centre_flow = self.flow(name+"_centre", initial(qL, c))
        box_flow = self.flow(name+"_box", initial(qL, Y))
        M = mat(box_flow["derivative"])
        e = vec(centre_flow["endpoint"])
        F = [e[0]-qR[0], e[2]-qR[1], constraint(qL, c)[0]]
        J = [[M[i][j] for j in (1, 3, 4)] for i in (0, 2)]
        J.append(constraint(qL, Y)[1])
        B_float = np.linalg.inv(np.array([[float(x.mid()) for x in row] for row in J]))
        Bq = [[Q(float(x)) for x in row] for row in B_float]
        rj = [[R.from_ball(x) for x in row] for row in J]
        rf = list(map(R.from_ball, F))
        rb = [[R(x) for x in row] for row in Bq]
        D = [[R(int(i == j))-sum((rb[i][k]*rj[k][j] for k in range(3)), R(0))
              for j in range(3)] for i in range(3)]
        K = [R(centres[i])-sum((rb[i][k]*rf[k] for k in range(3)), R(0))
             + sum((D[i][j]*R(-radii[j], radii[j]) for j in range(3)), R(0))
             for i in range(3)]
        margins = [min(K[i].lo-(centres[i]-radii[i]),
                       centres[i]+radii[i]-K[i].hi) for i in range(3)]
        norm = max(sum(D[i][j].magnitude()*radii[j]/radii[i] for j in range(3)) for i in range(3))
        passed = all(m > 0 for m in margins) and norm < 1
        self.controls[name+"_uniform_parametric_krawczyk"] = passed
        summary = {
            "endpoint_order": ["aL", "phiL", "aR", "phiR"],
            "endpoint_box": records(qL+qR), "shooting_order": ["uL", "vL", "T"],
            "shooting_box_exact": [R(c-r,c+r).record() for c,r in zip(centres,radii)],
            "F_centre_uniform_in_endpoints": records(F), "DF_shooting": records(J),
            "preconditioner_exact_hex": [[float(x).hex() for x in row] for row in B_float],
            "K_exact_rational": [x.record() for x in K],
            "inclusion_margins_exact": list(map(str, margins)),
            "weighted_defect_norm_exact": str(norm), "weighted_defect_norm_display": float(norm),
            "uniform_pass": passed,
            "fixed_T_endpoint_block_determinant": rec(determinant([row[:2] for row in J[:2]])),
            "action_enclosure": rec(decode(box_flow["endpoint"][5])),
        }
        self.result["branches"][name] = summary
        if not passed:
            raise ArithmeticError(name+": parametric inclusion failed")
        # Smooth analytic RHS plus uniform nonsingular shooting derivative gives
        # a unique smooth branch over the whole declared endpoint product box.
        inverse = inverse3(J)
        Cq = constraint(qL, Y)[2]
        E = [[M[0][0], M[0][2], arb(-1), arb(0)],
             [M[2][0], M[2][2], arb(0), arb(-1)],
             [Cq[0], Cq[1], arb(0), arb(0)]]
        Dy = [[-x for x in row] for row in mm(inverse, E)]
        summary["shooting_endpoint_derivative"] = records(Dy)
        summary["DF_determinant"] = rec(determinant(J))
        Kb = [bounds(ball(k.lo), ball(k.hi)) for k in K]
        pL = momenta(initial(qL, Y))
        pR = momenta(vec(box_flow["endpoint"]))
        summary["action_endpoint_gradient"] = records([-x for x in pL]+pR)
        return {"qL": qL, "qR": qR, "Y": Y, "K": Kb, "Dy": Dy,
                "flow": box_flow, "gradient": [-x for x in pL]+pR}


def midpoint_element(q0, q1, h):
    a, phi = [(x+y)/2 for x,y in zip(q0,q1)]
    da, dp = [y-x for x,y in zip(q0,q1)]
    V, Vp, _ = base.potential(phi)
    U, Ua, Up = -3*a+a**3*V, -3+3*a*a*V, a**3*Vp
    P = 2*arb.pi()**2
    S = P*(-3*a*da*da/h+a**3*dp*dp/(2*h)+h*U)
    dm = [-3*da*da/h+3*a*a*dp*dp/(2*h)+h*Ua, h*Up]
    dd = [-6*a*da/h, a**3*dp/h]
    L = [P*(dm[i]/2-dd[i]) for i in range(2)]
    Rg = [P*(dm[i]/2+dd[i]) for i in range(2)]
    dh = P*(3*a*da*da/(h*h)-a**3*dp*dp/(2*h*h)+U)
    return S, L, Rg, dh


def construct(work):
    inputs = work.inputs
    seed = json.loads(SEED.read_text())
    qb = [Q(inputs["boundary"][k]) for k in ("a", "phi")]
    er = Q(2)**inputs["endpoint_radius_binary_exponent"]
    q = [exact_box(c, er) for c in qb]
    centres = [Q(float(seed["inputs"]["centre_decimal"][k])) for k in ("u", "v", "T")]
    radii = [Q(2)**e for e in inputs["full_shooting_radius_binary_exponents"]]

    free_state = list(map(ball, [Q(2), Q(1,4), Q(1), Q(-1,8), Q(1,2)]))
    free = work.flow("free", free_state, True)
    ef = list(map(ball, [Q(17,8), Q(1,4), Q(15,16), Q(-1,8), Q(1,2), Q(5,256)]))
    mf = [[arb(int(i == j)) for j in range(6)] for i in range(6)]
    mf[0][1], mf[0][4], mf[2][3], mf[2][4] = arb(1)/2, arb(1)/4, arb(1)/2, -arb(1)/8
    mf[5][1], mf[5][3], mf[5][4] = arb(1)/8, -arb(1)/16, arb(5)/128
    work.controls["free_action_and_C1_exact_42_entries"] = all(
        inside(x, decode(y)) for x,y in zip(ef,free["endpoint"])) and all(
        inside(mf[i][j], decode(free["derivative"][i][j])) for i in range(6) for j in range(6))

    full = work.branch("full", q, q, centres, radii)
    y = full["K"]
    tight = work.flow("full_restricted", initial(q, y))
    third = work.flow("first_third", initial(q, [y[0],y[1],y[2]/3]))
    half = work.flow("first_half", initial(q, [y[0],y[1],y[2]/2]))
    third_e, half_e, tight_e = vec(third["endpoint"]), vec(half["endpoint"]), vec(tight["endpoint"])
    qm_centres = [midpoint(third_e[i]) for i in (0,2)]
    qm = [exact_box(c,Q(2)**inputs["vertex_radius_binary_exponent"]) for c in qm_centres]
    work.controls["third_vertex_inside_independent_product_box"] = all(
        inside(third_e[i],qm[j],True) for j,i in enumerate((0,2)))
    cell_radii = [Q(2)**e for e in inputs["cell_shooting_radius_binary_exponents"]]
    left_c = [midpoint(y[0]),midpoint(y[1]),midpoint(y[2]/3)]
    right_c = [midpoint(third_e[1]),midpoint(third_e[3]),midpoint(y[2]*2/3)]
    left = work.branch("left",q,qm,left_c,cell_radii)
    right = work.branch("right",qm,q,right_c,cell_radii)
    left_restriction = [y[0],y[1],y[2]/3]
    right_restriction = [third_e[1],third_e[3],y[2]*2/3]
    work.controls["full_restrictions_inside_both_cell_shooting_boxes"] = all(
        inside(x,box,True) for xs,bs in ((left_restriction,left["Y"]),(right_restriction,right["Y"]))
        for x,box in zip(xs,bs))
    work.controls["nonzero_characteristic_at_matched_vertex"] = (
        not base.zero_in(third_e[1]) or not base.zero_in(third_e[3]))

    # Exact Noether subtraction is proved in the report. This interval checks
    # its nonzero vector on the independent product of the two edge branches.
    left_end = vec(left["flow"]["endpoint"])
    pminus = momenta([qm[0],left_end[1],qm[1],left_end[3]])
    pplus = momenta(initial(qm,right["Y"]))
    Rg = [-(pminus[0]+pplus[0])/(24*arb.pi()**2*qm[0]),
          (pminus[1]+pplus[1])/(4*arb.pi()**2*qm[0]**3)]
    work.controls["nonzero_characteristic_on_cell_product_box"] = any(not base.zero_in(x) for x in Rg)

    # Exact semigroup/action additivity uses the already identified full branch.
    # A separate enclosure is a consistency check, not independent existence.
    suffix = work.flow("restricted_suffix",initial([third_e[0],third_e[2]],right_restriction))
    suffix_e = vec(suffix["endpoint"])
    composition_gap = tight_e[5]-third_e[5]-suffix_e[5]
    work.controls["action_additivity_enclosure_consistency"] = base.zero_in(composition_gap)

    # A real C1 pullback comparator, explicitly using the continuum-selected T.
    # It is not a fixed-T identity or a lapse-extremized midpoint action.
    qh = [half_e[0],half_e[2]]
    h = y[2]/2
    s1,l1,r1,t1 = midpoint_element(q,qh,h)
    s2,l2,r2,t2 = midpoint_element(qh,q,h)
    Dy = full["Dy"]
    Zp = [[arb(1),arb(0),arb(0),arb(0)],Dy[0],
          [arb(0),arb(1),arb(0),arb(0)],Dy[1],[x/2 for x in Dy[2]], [arb(0)]*4]
    Mhalf = mat(half["derivative"])
    Dhalf = mm(Mhalf,Zp)
    Dcomp = [sum(((r1[j]+l2[j])*Dhalf[i][k] for j,i in enumerate((0,2))),arb(0))
             +(t1+t2)*Dy[2][k]/2
             +(l1[k] if k<2 else r2[k-2]) for k in range(4)]
    p0 = momenta(initial(q,y))
    pT = momenta(tight_e)
    grad = [-x for x in p0]+pT
    value_defect = tight_e[5]-s1-s2
    gradient_defect = [a-b for a,b in zip(grad,Dcomp)]
    # Independent first variation check against the integrated action's C1 row.
    Zfull = [Zp[i] for i in range(4)]+[Dy[2],[arb(0)]*4]
    action_chain = mm(mat(tight["derivative"]),Zfull)[5]
    work.controls["action_first_variation_C1_consistency"] = all(overlap(a,b) for a,b in zip(action_chain,grad))
    end = vec(full["flow"]["endpoint"])
    work.controls["autonomous_T_action_column_consistency"] = overlap(
        decode(full["flow"]["derivative"][5][4]),lagrangian(end))
    work.result["interface"] = {
        "action_enclosure_on_endpoint_box": rec(tight_e[5]),
        "endpoint_gradient_enclosure": records(grad),
        "endpoint_derivative_from_integrated_action": records(action_chain),
        "third_vertex_state": records(third_e[:4]),
        "characteristic_on_independent_cell_product": records(Rg),
        "composition_gap_consistency_only": rec(composition_gap),
        "composition_scope": "Restriction of each full branch to its one-third split; any nearby matched pair whose concatenated shooting data remain in the full box has that same action. No global critical-point exhaustion.",
        "projection": "P(qL,qR)=(qL,q(T(qL,qR)/2),qR,T(qL,qR)); two equal-duration midpoint cells",
        "midpoint_pullback_value": rec(s1+s2),
        "midpoint_pullback_gradient": records(Dcomp),
        "C1_pullback_value_defect": rec(value_defect),
        "C1_pullback_gradient_defect": records(gradient_defect),
        "comparator_scope": "Continuum-selected lapse pullback only; neither fixed-T nor stationary-midpoint source equivalence, no transfer of gauge identities to the midpoint action.",
    }


def main():
    started = time.monotonic()
    try:
        inputs = json.loads(INPUT.read_text())
    except Exception as error:
        failure = {"verdict":"INCONCLUSIVE_PRINCIPAL_INTERFACE",
                   "execution_error":{"type":type(error).__name__,"message":str(error)[:2000]}}
        OUTPUT.write_text(json.dumps(failure,indent=2)+"\n")
        print(json.dumps(failure))
        return 1
    result = {"schema_version":1,"created_at_utc":datetime.now(timezone.utc).isoformat(),
              "question":"Can one explicit real endpoint box support a constrained principal-action branch, a two-cell characteristic/composition interface, and a C1 midpoint pullback enclosure?",
              "scope":"SUPPORTING_METHOD; local real classical constrained branches",
              "non_claim":"No full BFV source, original relative cycle, quantum measure, fixed-T midpoint equality, global intersection or new physics/discovery.",
              "dominant_failure_class":"solver","inputs":inputs,"controls":{},"flows":{},"branches":{},
              "provenance":{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=HERE,text=True).strip(),
                            "runner_sha256":base.sha(__file__),"helper_source_sha256":base.sha(HELPER),
                            "inputs_sha256":base.sha(INPUT),"seed_result_sha256":base.sha(SEED),
                            "arithmetic_helper_sha256":base.sha(base.__file__),"uv_lock_sha256":base.sha(HERE.parent/"uv.lock"),
                            "python":sys.version,"platform":platform.platform(),
                            "packages":{n:importlib.metadata.version(n) for n in ("numpy","python-flint")},
                            "entry_command":"ICE_CAPD_PRINCIPAL_BINARY=<pinned binary> ./ice run starobinsky_principal_branch"}}
    try:
        binary = Path(os.environ["ICE_CAPD_PRINCIPAL_BINARY"]).resolve(strict=True)
        for path,want in ((HELPER,inputs["helper_source_sha256"]),(binary,inputs["helper_binary_sha256"]),
                          (SEED,inputs["seed_result_sha256"]),(Path(base.__file__),inputs["arithmetic_helper_sha256"])):
            if base.sha(path)!=want:
                raise ValueError(f"hash mismatch: {path.name}")
        result["provenance"]["binary_sha256"] = base.sha(binary)
        with ctx.workprec(192):
            construct(Work(inputs,result,binary))
        result["verdict"] = ("CERTIFIED_LOCAL_CONSTRAINED_PRINCIPAL_COMPOSITION_INTERFACE"
                             if all(result["controls"].values()) else "INCONCLUSIVE_PRINCIPAL_INTERFACE")
    except Exception as error:
        result["verdict"] = "INCONCLUSIVE_PRINCIPAL_INTERFACE"
        result["execution_error"] = {"type":type(error).__name__,"message":str(error)[:2000]}
    result["elapsed_seconds"] = time.monotonic()-started
    data = json.dumps(result,indent=2)+"\n"
    if len(data.encode())>900000:
        raise RuntimeError("result exceeds artifact budget")
    OUTPUT.write_text(data)
    print(json.dumps({"verdict":result["verdict"],"controls":result["controls"],
                      "execution_error":result.get("execution_error"),"elapsed_seconds":result["elapsed_seconds"]}))
    return int(result["verdict"].startswith("INCONCLUSIVE"))


if __name__ == "__main__":
    raise SystemExit(main())
