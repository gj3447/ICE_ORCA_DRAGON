#!/usr/bin/env python3
"""Audit the declared Starobinsky LB scalar fiber's positive-D hypothesis.

Exact symbolic identities and two analytic negative-form witnesses, not a
finite-matrix spectrum. Execute only through ./ice run.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction

import sympy as s
from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "STAROBINSKY_MORSE_FIBER_POSITIVITY_RESULT.json"
BOUNDARY_A = "3.5668031935672753"


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def exact_ball(text):
    q = Fraction(text)
    return arb(fmpq(q.numerator,q.denominator))


def record(value):
    def dyadic(x):
        m,e = x.man_exp()
        return str(Fraction(int(m))*Fraction(2)**int(e))
    if not value.is_finite():
        raise ArithmeticError("nonfinite interval")
    return {"lower_exact":dyadic(value.lower()),"upper_exact":dyadic(value.upper()),
            "display_only":value.str(18)}


def audit():
    a,phi,z,x,lam,hbar = s.symbols("a phi z x lambda hbar",positive=True)
    n = s.symbols("n",integer=True,nonnegative=True)
    beta = s.sqrt(s.Rational(2,3))
    psi = s.Function("psi")(a,phi)
    density = s.sqrt(6)*a**2
    LB = (s.diff(density*(-1/(6*a))*s.diff(psi,a),a)
          +s.diff(density/a**3*s.diff(psi,phi),phi))/density
    V = s.Rational(3,4)*(1-s.exp(-beta*phi))**2
    rawH = -hbar**2*LB/(4*s.pi**2)+(-6*s.pi**2*a+2*s.pi**2*a**3*V)*psi
    target = (hbar**2*(a*a*s.diff(psi,a,2)+a*s.diff(psi,a))-6*hbar**2*s.diff(psi,phi,2)
              +(36*s.pi**4*a**6*(1-s.exp(-beta*phi))**2-144*s.pi**4*a**4)*psi)
    B,C = 36*s.pi**4*a**6,144*s.pi**4*a**4
    lvalue = 3*s.pi**2*a**3
    spectral_energy = lam**2-(lam-n-s.Rational(1,2))**2
    exponent = lam-n-s.Rational(1,2)
    w = z**exponent*s.exp(-z/2)
    f = s.Function("f")(z)
    K = lambda y: -(z*z*s.diff(y,z,2)+z*s.diff(y,z))+(lam**2-lam*z+z*z/4)*y
    reduced = s.simplify((K(w*f)-spectral_energy*w*f)/w)
    laguerre_residual = -z*(z*s.diff(f,z,2)+(2*exponent+1-z)*s.diff(f,z)+n*f)
    W = lam-s.Rational(1,2)-lam*s.exp(-x)
    E0 = 12*s.pi**2*a**3-1-C
    gap,L = s.symbols("gap L",positive=True)
    u = s.symbols("u",real=True)
    packet = s.sqrt(2/L)*s.sin(s.pi*u/L)
    symbolic = {
        "laplace_beltrami_density":s.simplify(density**2-6*a**4),
        "raw_LB_to_alpha_fiber_equation":s.simplify(24*s.pi**2*a**3*rawH-target),
        "morse_kinetic_coefficient":s.simplify(6*beta**2-4),
        "morse_potential_coefficient":s.simplify(4*lvalue**2-B),
        "laguerre_differential_equation_reduction":s.simplify(reduced-laguerre_residual),
        "ground_eigenfunction":s.simplify((K(w.subs(n,0))-spectral_energy.subs(n,0)*w.subs(n,0))/w.subs(n,0)),
        "ground_factorization":s.simplify(W**2-s.diff(W,x)+lam-s.Rational(1,4)-lam**2*(1-s.exp(-x))**2),
        "essential_threshold_factorization":s.factor(B-C-36*s.pi**4*a**4*(a*a-4)),
        "ground_energy_map":s.simplify(4*spectral_energy.subs({lam:lvalue,n:0})-C-E0),
        "large_a_negative_energy_factorization":s.simplify(E0-(12*s.pi**2*a**3*(1-12*s.pi**2*a)-1)),
        "compact_packet_norm":s.simplify(s.integrate(packet**2,(u,0,L))-1),
        "compact_packet_kinetic":s.simplify(6*s.integrate(s.diff(packet,u)**2,(u,0,L))-6*s.pi**2/L**2),
        "compact_packet_negative_bound":s.simplify((6*s.pi**2/L**2-gap).subs(L,s.sqrt(12*s.pi**2/gap))+gap/2),
        "ground_normalization_gamma":s.simplify((beta/s.gamma(2*lam-1))/beta*s.gamma(2*lam-1)-1),
    }
    checks = {k:v==0 for k,v in symbolic.items()}
    # Inequality guards for the analytic a>=2 branch. The 0<a<2 branch
    # uses a positive symbolic gap and the exact Rayleigh identity above.
    with ctx.workprec(192):
        pi = arb.pi()
        guards = {
            "pi_greater_than_3":bool(pi.lower()>3),
            "ground_exists_for_all_a_ge_2":bool((24*pi**2-arb(1)/2).lower()>0),
            "one_minus_12_pi2_a_negative_for_all_a_ge_2":bool((1-24*pi**2).upper()<0),
        }
        ab = exact_ball(BOUNDARY_A)
        lb = 3*pi*pi*ab**3
        cb = 144*pi**4*ab**4
        threshold = 4*lb*lb-cb
        ground = 4*lb-1-cb
        last_bound_exclusive = lb-arb(1)/2
        last_negative_exclusive = last_bound_exclusive-(lb*lb-cb/4).sqrt()

        def count_strict_nonnegative_integers(bound):
            count = math.ceil(float(bound.mid()))
            passed = bool(bound.lower()>count-1 and bound.upper()<count)
            if not passed:
                raise ArithmeticError("integer spectral count not separated from threshold")
            return {"count":count,"exclusive_upper_index":record(bound),
                    "strict_separation_from_adjacent_integers":True}

        diagnostic = {"a_exact_decimal":BOUNDARY_A,"lambda":record(lb),
                      "essential_threshold":record(threshold),"ground_energy":record(ground),
                      "bound_state_count":count_strict_nonnegative_integers(last_bound_exclusive),
                      "negative_bound_state_count":count_strict_nonnegative_integers(last_negative_exclusive),
                      "scope":"A scalar-fiber diagnostic at the old boundary scale; not a WDW solution or the full constraint spectrum."}
        guards["diagnostic_a_above_2"] = bool(ab.lower()>2)
        guards["diagnostic_ground_strictly_negative"] = bool(ground.upper()<0)
        guards["diagnostic_essential_threshold_positive"] = bool(threshold.lower()>0)
    return {
        "verdict":("EXACT_SCOPED_NEGATIVE_SPECTRUM_IN_EVERY_POSITIVE_SCALE_FIBER"
                   if all(checks.values()) and all(guards.values()) else "INCONCLUSIVE_FIBER_POSITIVITY"),
        "symbolic_checks":checks,"symbolic_residuals":{k:str(v) for k,v in symbolic.items()},
        "analytic_guards":guards,
        "operator":{"ordering":"Laplace-Beltrami on G=diag(-6a,a^3)","hbar":"1",
                    "fiber_space":"L2(R,dphi), fixed a>0; unique semibounded closure of C_c^infinity",
                    "D_a":"-6 d_phi^2 + 36*pi^4*a^6*(1-exp(-sqrt(2/3)*phi))^2 - 144*pi^4*a^4",
                    "x":"sqrt(2/3)*phi","lambda":"3*pi^2*a^3",
                    "equation_boundary":"Multiplying the raw WDW equation by 24*pi^2*a^3 is not a RAQ/domain equivalence theorem."},
        "spectrum":{"essential":"[36*pi^4*a^4*(a^2-4), infinity)",
                    "discrete":"E_n=4*(lambda^2-(lambda-n-1/2)^2)-144*pi^4*a^4",
                    "index_domain":"n integer >=0, n < lambda-1/2, strictly",
                    "ground_wavefunction":"sqrt(beta/Gamma(2*lambda-1))*z^(lambda-1/2)*exp(-z/2), z=2*lambda*exp(-beta*phi), lambda>1/2"},
        "all_scale_proof":[
            {"domain":"0<a<2","gap":"144*pi^4*a^4-36*pi^4*a^6 > 0",
             "witness":"sqrt(2/L)*sin(pi*(phi-1)/L) on [1,1+L], zero elsewhere; H1 form-domain state",
             "L":"sqrt(12*pi^2/gap)","rayleigh_upper_bound":"-gap/2 < 0",
             "reason":"On phi>=1, (1-exp(-beta*phi))^2 <= 1. This form witness needs no bound-state formula or finite spectral cutoff."},
            {"domain":"a>=2","witness":"normalizable exact Morse ground state",
             "energy":"12*pi^2*a^3*(1-12*pi^2*a)-1 < 0",
             "reason":"lambda>=24*pi^2>1/2 and 1-12*pi^2*a<0."}],
        "boundary_cases":{"a_zero":"excluded singular geometry, not an endpoint limit theorem",
                          "a_two":"essential threshold 0; ground energy strictly negative",
                          "n_equals_lambda_minus_half":"non-normalizable continuum threshold, excluded from bound-state count"},
        "diagnostic":diagnostic,
        "logical_output":"No a>0 makes this full scalar fiber nonnegative; no positive self-adjoint square root with square D_a on that full fiber.",
        "remaining_choices":"Other clock/order/domain/spectral restrictions and Mostafazadeh's positive replacement operator remain possible; no state preparation or source cycle has been selected.",
    }


def main():
    started = time.monotonic()
    result = {"schema_version":1,"created_at_utc":datetime.now(timezone.utc).isoformat(),
              "question":"Does the declared same-Starobinsky LB scalar fiber admit the positive-D reference-scale premise anywhere at a>0?",
              "scope":"SCOPED_QUANTUM_OPERATOR_DISCRIMINATOR; SUPPORTING, no original G1 source class",
              "non_claim":"No full WDW spectrum/self-adjoint extension, physical instability, universal Hilbert-space no-go, BFV measure/cycle, choice invariance, TOE or empirical discovery.",
              "dominant_failure_class":"spectrum",
              "controls":"Exact LB/Morse algebra; independent compact negative-form witness; ground normalizability and spectral thresholds.",
              "provenance":{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=HERE,text=True).strip(),
                            "runner_sha256":sha(__file__),"uv_lock_sha256":sha(HERE.parent/"uv.lock"),
                            "classical_source_path":"cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md",
                            "classical_source_sha256":sha(HERE/"STAROBINSKY_POLYNOMIAL_BFV_CHART.md"),
                            "entry_command":"./ice run starobinsky_morse_fiber_positivity",
                            "python":sys.version,"platform":platform.platform(),
                            "packages":{p:importlib.metadata.version(p) for p in ("sympy","python-flint")}},
              "primary_sources":["https://doi.org/10.1103/PhysRev.34.57",
                                 "https://arxiv.org/html/2102.05102","https://arxiv.org/abs/gr-qc/0306003"]}
    try:
        result.update(audit())
    except Exception as error:
        result["verdict"] = "INCONCLUSIVE_FIBER_POSITIVITY"
        result["execution_error"] = {"type":type(error).__name__,"message":str(error)[:2000]}
    result["elapsed_seconds"] = time.monotonic()-started
    serialized = json.dumps(result,indent=2)+"\n"
    if len(serialized.encode())>250000:
        raise RuntimeError("artifact budget exceeded")
    OUTPUT.write_text(serialized)
    print(json.dumps({"verdict":result["verdict"],"symbolic_checks":result.get("symbolic_checks"),
                      "analytic_guards":result.get("analytic_guards"),"execution_error":result.get("execution_error"),
                      "elapsed_seconds":result["elapsed_seconds"]}))
    return int(result["verdict"].startswith("INCONCLUSIVE"))


if __name__ == "__main__":
    raise SystemExit(main())
