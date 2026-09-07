"""Classify first-order local strong observables and discriminate the selected seam.

One output: exact observable nonselection plus complementary bosonic pairing.
Analytic classification/PDE/Green proofs are separate from finite symbolic/Lean checks.
No PDE existence proof, selected physical inner product, full CPT sewing or G1 claim.
Run committed sources only: ./ice run starobinsky_observable_selection.
"""
from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import tempfile
import time

import sympy as s
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / "formal/cpt_sewing"
INDEX = PROJECT / "observable-selection-proof-index.json"
RESULT = HERE / "STAROBINSKY_OBSERVABLE_SELECTION_RESULT.json"
PINS = {
    "cpt_boundary_sewing_lean.py": "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb",
    "STAROBINSKY_DUAL_CAUCHY_DERIVATION.md": "4c5ff22a482d2bbcebad04e7de2f30a612777cb38136386a330189487550249c",
    "STAROBINSKY_DUAL_CAUCHY_RESULT.json": "9cc9d9533d105de6bd2be58e93a789581846d0d67d4efc80166825936af84f2d",
    "STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md": "6f38da66b0fc511c21c8f26919a41417200ff36e00346997b095f3f261c72da6",
}
for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise ValueError(f"changed analytic/audit input: {name}")

from cpt_boundary_sewing_lean import ALLOWED_AXIOMS, audit_axioms, checked, elaborate


def provenance(index: dict) -> dict:
    files = [Path(__file__), HERE / "STAROBINSKY_OBSERVABLE_SELECTION_DERIVATION.md", INDEX, *(PROJECT / m["source"] for m in index["modules"]),
             *(HERE / name for name in PINS), PROJECT / "lean-toolchain",
             PROJECT / "lakefile.toml", PROJECT / "lake-manifest.json", ROOT / "uv.lock"]
    records = {}
    for path in files:
        rel = str(path.relative_to(ROOT))
        data = path.read_bytes()
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT,
                                   capture_output=True, check=True, timeout=10).stdout
        if data != committed:
            raise ValueError(f"uncommitted input: {rel}")
        records[rel] = {"sha256":hashlib.sha256(data).hexdigest(), "bytes":len(data)}
    if (PROJECT / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.33.0":
        raise ValueError("unexpected Lean toolchain")
    version = checked(["lake", "env", "lean", "--version"])
    if not version.startswith("Lean (version 4.33.0,"):
        raise ValueError(version)
    manifest = json.loads((PROJECT / "lake-manifest.json").read_text())
    dependencies = []
    for package in manifest["packages"]:
        location = PROJECT / manifest["packagesDir"] / package["name"]
        revision = checked(["git", "rev-parse", "HEAD"], cwd=location)
        if revision != package["rev"] or checked(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=location
        ):
            raise ValueError(f"modified dependency: {package['name']}")
        dependencies.append({"name":package["name"], "rev":revision})
    if not any(p["name"] == "mathlib" and p["rev"] ==
               "db584cd6d46c92f209a44c0f1c829460d327499d" for p in dependencies):
        raise ValueError("unexpected mathlib revision")
    return {"source_commit":checked(["git", "rev-parse", "HEAD"], cwd=ROOT),
            "inputs":records, "python":platform.python_version(), "sympy":s.__version__,
            "lean_version":version, "dependencies":dependencies}


def audit_module(module: dict) -> dict:
    source = (PROJECT / module["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != module["theorems"] or not names:
        raise ValueError(f"incomplete theorem index: {module['source']}")
    if re.search(r"\b(sorry|admit)\b|^\s*axiom\s", source, re.MULTILINE):
        raise ValueError(f"proof placeholder or local axiom: {module['source']}")
    expected = [module["namespace"]+"."+name for name in names]
    payload = source+"\n"+"\n".join(f"#check {n}\n#print axioms {n}" for n in expected)+"\n"
    with tempfile.TemporaryDirectory(prefix="ice-observable-selection-") as temp:
        run = elaborate(payload, Path(temp), Path(module["source"]).stem+"Audit")
    record = {"source":module["source"], "scope":module["scope"],
              "expected_theorem_count":len(expected), "elaboration":run, "accepted":False}
    if run["exit_code"] != 0 or run["stderr"].strip() or any(
        message.get("severity") in {"warning", "error"} for message in run["messages"]
    ):
        return record
    records = audit_axioms(run["messages"], expected)
    record.update(theorems=records, theorem_count=len(records),
                  accepted=all(r["accepted"] for r in records.values()))
    return record


def derive() -> dict:
    a, r, t = s.symbols("a r t", positive=True)
    phi, theta, n = s.symbols("phi theta N", real=True)
    k = 4*s.pi*s.sqrt(6)/3
    q = s.sqrt(s.Rational(3, 8))
    beta = s.sqrt(s.Rational(2, 3))
    ra = k*a**s.Rational(3, 2)
    f = -1/(24*s.pi**2*a)
    b = 1/(4*s.pi**2*a**3)
    U = -6*s.pi**2*a+s.Rational(3, 2)*s.pi**2*a**3*(1-s.exp(-beta*phi))**2
    W = U-s.diff(f,a,2)/4
    checks = []

    def eq(name, actual, expected=0, group="actual_strong_commutant"):
        residual = s.simplify(s.expand(actual-expected))
        checks.append({"id":name, "group":group, "passed":residual == 0, "residual":str(residual)})

    def H(z):
        return -s.diff(f*s.diff(z,a),a)-b*s.diff(z,phi,2)+W*z

    def lap(z):
        return s.diff(z,r,2)+s.diff(z,r)/r-s.diff(z,theta,2)/r**2

    psi = s.Function("psi")(r,theta,n)
    eq("actual_radial_second_order_coefficient", -f*s.diff(ra,a)**2, 1)
    eq("actual_radial_first_order_coefficient", -f*s.diff(ra,a,2)-s.diff(f,a)*s.diff(ra,a), -1/(3*ra))
    eq("actual_angular_second_order_coefficient", -b*q**2, -1/ra**2)
    eq("similarity_not_constraint_rescaling", r**s.Rational(2,3)*lap(r**(-s.Rational(2,3))*psi),
       s.diff(psi,r,2)-s.diff(psi,r)/(3*r)-s.diff(psi,theta,2)/r**2+4*psi/(9*r**2))
    eq("actual_Weyl_residual_potential", W-4/(9*ra**2), U-1/(48*s.pi**2*a**3))
    eq("actual_angular_exponent", beta/q, s.Rational(4,3))
    eq("actual_potential_r_squared_coefficient", 3*s.pi**2/(2*k**2), s.Rational(9,64))
    eq("actual_Weyl_barrier_coefficient", k**2/(48*s.pi**2), s.Rational(2,9))

    xr, xt = s.Function("Xr")(r,theta), s.Function("Xt")(r,theta)
    def X(z): return xr*s.diff(z,r)+xt*s.diff(z,theta)
    comm = s.expand(lap(X(psi))-X(lap(psi)))
    eq("principal_rr_Killing_equation", comm.coeff(s.diff(psi,r,2)), 2*s.diff(xr,r))
    eq("principal_rtheta_Killing_equation", comm.coeff(s.diff(psi,r,theta)), 2*s.diff(xt,r)-2*s.diff(xr,theta)/r**2)
    eq("principal_thetatheta_Killing_equation", comm.coeff(s.diff(psi,theta,2)), -2*s.diff(xt,theta)/r**2-2*xr/r**3)
    def trans1(z): return s.cosh(theta)*s.diff(z,r)-s.sinh(theta)*s.diff(z,theta)/r
    def trans2(z): return s.sinh(theta)*s.diff(z,r)-s.cosh(theta)*s.diff(z,theta)/r
    eq("translation_one_wave_commutator", lap(trans1(psi))-trans1(lap(psi)))
    eq("translation_two_wave_commutator", lap(trans2(psi))-trans2(lap(psi)))
    eq("boost_wave_commutator", lap(s.diff(psi,theta))-s.diff(lap(psi),theta))
    gamma, dn = s.Function("gamma")(r,theta), s.Function("D")(r,theta)
    eq("multiplication_first_order_remainder", lap(gamma*psi)-gamma*lap(psi),
       2*s.diff(gamma,r)*s.diff(psi,r)-2*s.diff(gamma,theta)*s.diff(psi,theta)/r**2+lap(gamma)*psi)
    eq("primary_mixed_derivative_remainder", lap(dn*s.diff(psi,n))-dn*s.diff(lap(psi),n),
       2*s.diff(dn,r)*s.diff(psi,r,n)-2*s.diff(dn,theta)*s.diff(psi,theta,n)/r**2+lap(dn)*s.diff(psi,n))

    AA, BB, CC = s.symbols("A B C", positive=True)
    alpha, zeta, delta = s.symbols("alpha zeta delta")
    FF = (1-s.exp(-s.Rational(4,3)*theta))**2
    GG = alpha*s.cosh(theta)+zeta*s.sinh(theta)
    Q = -AA*r**s.Rational(2,3)+BB*r**2*FF-CC/r**2
    XQ = GG*s.diff(Q,r)+(-s.diff(GG,theta)/r+delta)*s.diff(Q,theta)
    expected = 2*CC*GG/r**3-s.Rational(2,3)*AA*GG/r**s.Rational(1,3)+BB*r*(2*FF*GG-s.diff(FF,theta)*s.diff(GG,theta))+delta*BB*r**2*s.diff(FF,theta)
    eq("actual_potential_Killing_derivative", XQ, expected)
    polynomial = s.Poly(s.expand((r**3*XQ).subs(r,t**3)),t)
    for power, coeff in [(0,2*CC*GG),(8,-s.Rational(2,3)*AA*GG),
                         (12,BB*(2*FF*GG-s.diff(FF,theta)*s.diff(GG,theta))),
                         (15,delta*BB*s.diff(FF,theta))]:
        eq(f"finite_open_interval_polynomial_coefficient_{power}", polynomial.nth(power), coeff)
    checks.append({"id":"radial_polynomial_has_only_declared_powers","group":"actual_strong_commutant",
                   "passed":set(m[0] for m in polynomial.monoms())=={0,8,12,15},
                   "powers":[m[0] for m in polynomial.monoms()]})
    eq("translation_basis_Wronskian", s.cosh(theta)**2-s.sinh(theta)**2,1)
    eq("boost_potential_nonzero_witness", s.diff(FF,theta).subs(theta,3*s.log(2)/4),s.Rational(2,3))
    u = s.Function("u")(a,phi,n)
    eq("naive_phi_is_not_a_strong_observable", H(phi*u)-phi*H(u),-2*b*s.diff(u,phi))
    eq("naive_scalar_momentum_is_not_a_strong_observable", H(-s.I*s.diff(u,phi))+s.I*s.diff(H(u),phi),s.I*s.diff(W,phi)*u)
    eq("actual_primary_commutes_H", H(-s.I*s.diff(u,n))+s.I*s.diff(H(u),n))

    # R scalar coefficients describe T after both constraints are annihilated.
    c, d, z = s.symbols("c d z", complex=True)
    eq("declared_scalar_star_compatibility", s.conjugate(c*z),s.conjugate(c)*s.conjugate(z),"rank_one_and_bosonic_seam")
    g, hh = s.symbols("g h",complex=True)
    eq("actual_Neumann_Dirichlet_Green_coefficient",f.subs(a,2)*(g*hh-0),-g*hh/(48*s.pi**2),"rank_one_and_bosonic_seam")
    vfun = s.Function("v")(r,theta,n)
    jr = r*(psi*s.diff(vfun,r)-s.diff(psi,r)*vfun)
    evolution = s.diff(jr,r).subs({s.diff(psi,r,2):-s.diff(psi,r)/r+s.diff(psi,theta,2)/r**2-Q*psi,
                                  s.diff(vfun,r,2):-s.diff(vfun,r)/r+s.diff(vfun,theta,2)/r**2-Q*vfun})
    eq("full_line_bilinear_current_divergence",evolution,
       s.diff(psi*s.diff(vfun,theta)-s.diff(psi,theta)*vfun,theta)/r,"rank_one_and_bosonic_seam")
    return {"checks":checks,
            "analytic_proof":"cpt_temporal_folded_susy/STAROBINSKY_OBSERVABLE_SELECTION_DERIVATION.md",
            "operator_convention":"unscaled Starobinsky Weyl H; flat density; hbar=1; fixed finite box",
            "classification":"All smooth first-order local O with [H,O]=[p_N,O]=0 are c I+d p_N",
            "scope":"Analytic completeness in the stated local strong class; not all physical observables",
            "selected_dual_action":"T_g P(H,p_N)=P(0,0) T_g: kernel and star compatibility pass, seed/normalization remain unselected",
            "seed_QP_boundary":"Cauchy seed-label Q,P are not established test-space/BFV observables; a lift would fail the fixed bump rank-one kernel",
            "bosonic_seam":"Actual complementary Neumann/Dirichlet families: W_ND= -integral_R(g h)/(48*pi^2); nondegenerate bilinear pairing; W_NN=W_DD=0",
            "remaining":"Higher-order/weak/nonlocal observable realization; oriented ghost/CPT exchange; actual BFV kernel, residual BV/mQME/pushforward and original joint cycle"}


def main() -> int:
    started = time.monotonic()
    result = {"schema":"ice-starobinsky-observable-selection/v1","status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Does the actual first-order strong observable algebra select the current dual quotient, and what bosonic seam survives a polarization test?",
        "scope":"SUPPORTING_METHOD: local first-order strong commutant and complementary bosonic Cauchy pairing",
        "non_claim":"No full physical observable algebra, selected positive metric, BFV/CPT sewing or G1 original cycle.",
        "reproduction_command":"./ice run starobinsky_observable_selection",
        "allowed_axioms":sorted(ALLOWED_AXIOMS),"modules":[]}
    try:
        index=json.loads(INDEX.read_text())
        result["provenance"]=provenance(index)
        result["symbolic"]=derive()
        for module in index["modules"]:
            if time.monotonic()-started>65:
                raise TimeoutError("insufficient time for another Lean module")
            result["modules"].append(audit_module(module))
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not all(m["accepted"] for m in result["modules"]):
            raise ValueError("symbolic or Lean audit failed; see raw diagnostics")
        result["theorem_count"]=sum(m["theorem_count"] for m in result["modules"])
        result["status"]="SCOPED_FIRST_ORDER_OBSERVABLE_NONSELECTION_AND_COMPLEMENTARY_BOSONIC_PAIRING"
    except Exception as error:
        result["failure"]=f"{type(error).__name__}: {error}"
    result["elapsed_seconds"]=time.monotonic()-started
    payload=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if len(payload.encode())>200_000:
        raise RuntimeError("unexpectedly large output")
    RESULT.write_text(payload)
    print(result["status"])
    if "symbolic" in result:
        print(f"exact controls: {sum(c['passed'] for c in result['symbolic']['checks'])}/{len(result['symbolic']['checks'])}")
    for module in result["modules"]:
        print(f"{module['source']}: accepted={module['accepted']}; expected={module['expected_theorem_count']}")
    if result["status"]=="FAILED":
        print(result["failure"])
        return 1
    print(f"Lean theorems: {result['theorem_count']}")
    print("Strong first-order observables act as scalars on constrained duals; no seed selection")
    print("Complementary bosonic pairing is nondegenerate; full BFV/CPT sewing remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
