#!/usr/bin/env python3
"""Exact polynomial BFV chart for the declared Lorentzian Starobinsky model.

Question: does the full extended canonical change, including lapse and ghosts,
produce a polynomial nilpotent charge with the adopted Phase-28 gauge fermion?
Output: one exact identity audit and a wrong-shift counterexample.
Non-claim: no original relative cycle, quantum measure, or physical discovery.

Use ./ice run starobinsky_polynomial_bfv_chart after committing this file.
Only the pinned four-generator exterior-algebra utilities are imported from
the older V=0 runner. None of its model inputs, results or main routine is used.
The Phase-28 gauge-fermion convention is adopted, not evidence for an original
Lorentzian physical source. Conventions are in the adjacent completion report.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
HELPER = HERE / "gate1_v0_improved_static_bfv_source.py"
HELPER_SHA = "62f52d079c62b9b84ccea6562e44b952067cd6c8e10f7d1a9673cc124b949ccf"
if hashlib.sha256(HELPER.read_bytes()).hexdigest() != HELPER_SHA:
    raise RuntimeError("exterior-algebra helper hash changed")

from gate1_v0_improved_static_bfv_source import Exterior as E, graded_poisson


def main() -> int:
    u, v = s.symbols("u v", positive=True)
    Pu, Pv, n, pn = s.symbols("P_u P_v n pi_n", real=True)
    beta = s.sqrt(s.Rational(2, 3))
    f = 24 * s.pi**2 * u**s.Rational(3, 2)
    C = E.generator("c_g")
    B = E.generator("bar_rho")
    R = E.generator("rho")
    D = E.generator("bar_c")
    even = ((u, Pu), (v, Pv), (n, pn))
    odd = (("c_g", "bar_rho"), ("rho", "bar_c"))

    def pb(x, y):
        return graded_poisson(E.coerce(x), E.coerce(y), even, odd)

    def h(k):
        k = E.coerce(k)
        return -4*k*k - 8*v*k*Pv - 144*s.pi**4*u**2 + 36*s.pi**4*u*(u-v)**2

    checks = []

    def equal(name, actual, expected=0):
        residual = E.coerce(actual) - E.coerce(expected)
        checks.append({"name": name, "passed": residual.is_zero(), "residual": residual.record()})

    G = B*C + D*R
    J = E.scalar(n*pn) + G
    k = E.scalar(u*Pu) - s.Rational(3, 2)*J
    Hpoly = h(k)
    omega = C*Hpoly + R*pn
    psi = -n*B
    # Inverse map, including the momentum contribution from the odd one-form.
    pu_old = E.scalar(Pu) - s.Rational(3, 2)*J/u
    pa_old = 2*s.sqrt(u)*(pu_old + v*Pv/u)
    pphi_old = -beta*v*Pv
    N_old, Pi_old = f*n, pn/f
    c_old, br_old, rho_old, bc_old = f*C, B/f, f*R, D/f
    H_old = (-pa_old*pa_old/(24*s.pi**2*s.sqrt(u))
             + E.scalar(pphi_old**2/(4*s.pi**2*u**s.Rational(3, 2))
                        - 6*s.pi**2*s.sqrt(u)
                        + s.Rational(3, 2)*s.pi**2*u**s.Rational(3, 2)*(1-v/u)**2))

    # Control 1: exact one-form and same-model/sign identities.
    equal("liouville_du", pa_old/(2*s.sqrt(u)) + pphi_old/(beta*u)
          + Pi_old*s.diff(f, u)*n + br_old*s.diff(f, u)*C
          + bc_old*s.diff(f, u)*R, Pu)
    equal("liouville_dv", -pphi_old/(beta*v), Pv)
    equal("liouville_dn", Pi_old*f, pn)
    equal("liouville_dC", br_old*f, B)
    equal("liouville_dR", bc_old*f, D)
    equal("densitized_hamiltonian", f*H_old, Hpoly)
    equal("charge_is_original_pullback", c_old*H_old + rho_old*Pi_old, omega)
    equal("gauge_fermion_is_original_pullback", -N_old*br_old, psi)
    ap, ps = s.symbols("a_p p_scalar", real=True)
    kinetic = -(2*u*ap+2*v*ps)**2 + 6*(-beta*v*ps)**2
    equal("starobinsky_slope_cancels_pv_squared", kinetic, -4*u**2*ap**2-8*u*v*ap*ps)
    # p_L=i p_E reverses H_L into -H_E; both potential signs are explicit.
    a, p_a, p_phi, V = s.symbols("a p_a p_phi V", nonzero=True)
    kinetic_E = -p_a**2/(24*s.pi**2*a)+p_phi**2/(4*s.pi**2*a**3)
    potential_L = -6*s.pi**2*a+2*s.pi**2*a**3*V
    equal("wick_HL_i_pE_equals_minus_HE", -kinetic_E+potential_L, -(kinetic_E-potential_L))

    # Control 2: independent graded bracket checks on the canonical image.
    equal("old_pa_a_bracket", pb(s.sqrt(u), pa_old), 1)
    equal("old_pa_c_cross_bracket", pb(pa_old, c_old))
    equal("old_pa_rho_cross_bracket", pb(pa_old, rho_old))
    equal("old_N_Pi_bracket", pb(N_old, Pi_old), 1)
    equal("old_c_barrho_bracket", pb(c_old, br_old), 1)
    equal("old_rho_barc_bracket", pb(rho_old, bc_old), 1)
    equal("strong_BFV_nilpotency", pb(omega, omega))
    equal("gauge_fixed_action_density", -pb(omega, psi), n*Hpoly+B*R)
    equal("gauge_fixed_density_BRST_closed", pb(omega, n*Hpoly+B*R))
    polynomial_degrees = []
    for obj in (omega, psi, n*Hpoly+B*R):
        polynomial_degrees.append(max(s.Poly(c, u, v, Pu, Pv, n, pn).total_degree()
                                      for c in obj.terms.values()))

    # Control 3: removing only the ghost momentum shift must fail off shell.
    A = u*Pu-s.Rational(3, 2)*n*pn
    bad = C*h(A) + R*pn
    bad_square = pb(bad, bad)
    expected_bad = 24*C*R*pn*(A+v*Pv)
    equal("wrong_shift_has_predicted_defect", bad_square, expected_bad)
    checks.append({"name": "wrong_shift_is_not_nilpotent", "passed": not bad_square.is_zero(),
                   "defect": bad_square.record()})
    # Short hand-derived form is independent of exterior square completion.
    short_charge = C*h(A)+R*pn-12*C*R*D*(A+v*Pv)
    equal("charge_matches_hand_expansion", omega, short_charge)

    result = {
        "question": "Exact same-Starobinsky polynomial extended BFV coordinate pushforward?",
        "classification": "FINITE_CANONICAL_POLYNOMIAL_BFV_CHART" if all(x["passed"] for x in checks) else "FAILED_IDENTITY_AUDIT",
        "scope": "Classical interior chart u>0,v>0; a fixed square-root/log lift is required after complexification.",
        "non_claim": "No original relative cycle, boundary completion, quantum path measure or physical discovery.",
        "convention": {"even_pairs": [[str(a),str(b)] for a,b in even],
                       "odd_pairs": [list(pair) for pair in odd],
                       "odd_bracket": "symmetric +1; right derivative on left argument, left derivative on right",
                       "ghost_names": {"C":"c_g", "B":"bar_rho", "R":"rho", "D":"bar_c"},
                       "old_gauge_fermion": "-N*bar_rho", "gauge_fixed_hamiltonian": "-{Omega,Psi}"},
        "map": {"u":"a**2", "v":"a**2*exp(-sqrt(2/3)*phi)", "f":str(f),
                "N":"f*n", "Pi":"pi_n/f", "c":"f*C", "bar_rho":"B/f", "rho":"f*R", "bar_c":"D/f",
                "p_a":pa_old.record(), "p_phi":str(pphi_old), "k":k.record()},
        "polynomials": {"Omega":omega.record(), "Psi":psi.record(),
                        "gauge_fixed_hamiltonian":(n*Hpoly+B*R).record(),
                        "maximum_even_degrees":polynomial_degrees},
        "controls": checks,
        "provenance": {"command":"./ice run starobinsky_polynomial_bfv_chart",
                       "runner_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                       "algebra_helper_sha256":HELPER_SHA,
                       "algebra_helper_scope":"Pure exterior multiplication and graded differentiation only; no V=0 physical input.",
                       "python":platform.python_version(), "sympy":s.__version__},
    }
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+"\n"
    if len(payload.encode()) > 100_000:
        raise RuntimeError("unexpectedly large exact result")
    (HERE / "STAROBINSKY_POLYNOMIAL_BFV_CHART_RESULT.json").write_text(payload)
    passed = sum(x["passed"] for x in checks)
    print(result["classification"])
    print(f"exact controls: {passed}/{len(checks)}")
    print(f"polynomial even degrees: {polynomial_degrees}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
