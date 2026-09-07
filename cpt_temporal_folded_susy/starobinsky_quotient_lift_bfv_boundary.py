"""Audit actual finite quotient lifts and the declared canonical BFV endpoint.

One output: adjoint-domain obstruction plus free/ghost-fixed boundary contrast.
Actual PDE/Gram construction is analytic; Lean checks abstract implications and
normalized real closure. No physical observable, selected metric or CPT sewing.
Run committed sources only: ./ice run starobinsky_quotient_lift_bfv_boundary.
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
INDEX = PROJECT / "quotient-lift-bfv-boundary-proof-index.json"
RESULT = HERE / "STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_RESULT.json"
PINS = {
    "STAROBINSKY_OBSERVABLE_SEWING_SOURCE_REVIEW.md": "2699facacfd7ef54c469084338745d0d187ebc3426ec616cea2bd2f9dfacd434",
    "STAROBINSKY_POLYNOMIAL_BFV_CHART.md": "c40c63bd2e3f6a3495133c4668ebdd421f90a85edca3cfeda901d56b32bd745d",
    "gate1_v0_improved_static_bfv_source.py": "62f52d079c62b9b84ccea6562e44b952067cd6c8e10f7d1a9673cc124b949ccf",
    "cpt_boundary_sewing_lean.py": "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb",
    "STAROBINSKY_DUAL_CAUCHY_DERIVATION.md": "4c5ff22a482d2bbcebad04e7de2f30a612777cb38136386a330189487550249c",
    "STAROBINSKY_DUAL_CAUCHY_RESULT.json": "9cc9d9533d105de6bd2be58e93a789581846d0d67d4efc80166825936af84f2d",
    "STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md": "6f38da66b0fc511c21c8f26919a41417200ff36e00346997b095f3f261c72da6",
}
for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise ValueError(f"changed analytic/audit input: {name}")

from cpt_boundary_sewing_lean import ALLOWED_AXIOMS, audit_axioms, checked, elaborate
# Utility import only: no historical inputs or main routine are executed.
from gate1_v0_improved_static_bfv_source import Exterior as E, graded_poisson


def provenance(index: dict) -> dict:
    files = [Path(__file__), HERE / "STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_DERIVATION.md", INDEX, *(PROJECT / m["source"] for m in index["modules"]),
             *(HERE / name for name in PINS), PROJECT / "lean-toolchain",
             PROJECT / "lakefile.toml", PROJECT / "lake-manifest.json", ROOT / "uv.lock",
             ROOT / "docs/research/ICE_BFV_CPT_SEAM_WARD_SOURCE_PROPOSAL_2026-09-07.md"]
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
    with tempfile.TemporaryDirectory(prefix="ice-quotient-boundary-") as temp:
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
    a = s.Symbol("a", positive=True)
    phi, n, pa, pp, Pi = s.symbols("phi N p_a p_phi Pi", real=True)
    beta = s.sqrt(s.Rational(2, 3))
    zphi = s.exp(-beta*phi)
    F = (1-zphi)**2
    H = -pa**2/(24*s.pi**2*a)+pp**2/(4*s.pi**2*a**3)-6*s.pi**2*a+s.Rational(3,2)*s.pi**2*a**3*F
    Ha = s.diff(H,a)
    c, br, rho, bc = (E.generator(k) for k in ("c_g","bar_rho","rho","bar_c"))
    even = ((a,pa),(phi,pp),(n,Pi))
    odd = (("c_g","bar_rho"),("rho","bar_c"))
    omega = c*H+rho*Pi
    checks = []

    def pb(x, y):
        return graded_poisson(E.coerce(x), E.coerce(y), even, odd)

    def eq(name, actual, expected=0, group="canonical_sign_and_free_ghost"):
        residual = E.coerce(actual)-E.coerce(expected)
        checks.append({"id":name,"group":group,"passed":residual.is_zero(),"residual":residual.record()})

    def restrict(value, even_values=None, zero_ghosts=()):
        return E({mon:coef.subs(even_values or {}, simultaneous=True)
                  for mon,coef in E.coerce(value).terms.items()
                  if not any(g in mon for g in zero_ghosts)})

    eq("even_q_p_sign",pb(a,pa),1)
    eq("even_p_q_sign",pb(pa,a),-1)
    eq("odd_c_bar_rho_sign",pb(c,br),1)
    eq("odd_bar_rho_c_sign",pb(br,c),1)
    eq("odd_rho_bar_c_sign",pb(rho,bc),1)
    eq("odd_bar_c_rho_sign",pb(bc,rho),1)
    coordinates={"a":a,"phi":phi,"N":n,"p_a":pa,"p_phi":pp,"Pi":Pi,
                 "c":c,"rho":rho,"bar_rho":br,"bar_c":bc}
    qtable={key:pb(omega,value) for key,value in coordinates.items()}
    expected={"a":c*pa/(12*s.pi**2*a),"phi":-c*pp/(2*s.pi**2*a**3),"N":-rho,
              "p_a":c*(pa**2/(24*s.pi**2*a**2)-3*pp**2/(4*s.pi**2*a**4)-6*s.pi**2+s.Rational(9,2)*s.pi**2*a**2*F),
              "p_phi":c*(3*s.pi**2*a**3*beta*zphi*(1-zphi)),"Pi":0,"c":0,"rho":0,"bar_rho":H,"bar_c":Pi}
    for key in coordinates:
        eq("actual_Q_"+key,qtable[key],expected[key])
    eq("canonical_master_bracket",pb(omega,omega))
    pp2=24*s.pi**4*a**4-6*s.pi**4*a**6*F
    eq("constraint_elimination_H",H.subs(pa,0).subs(pp**2,pp2))
    eq("constraint_elimination_Ha",Ha.subs(pa,0).subs(pp**2,pp2),3*s.pi**2*(3*a**2*F-8))
    witness={a:2,phi:0,pa:0,pp:8*s.sqrt(6)*s.pi**2,Pi:0}
    eq("actual_constraint_body_witness",H.subs(witness))
    eq("actual_fixed_a_tangency_witness",restrict(qtable["a"],witness))
    eq("actual_free_ghost_defect_coefficient",restrict(qtable["p_a"],witness),-24*s.pi**2*c)
    checks.append({"id":"actual_free_ghost_defect_nonzero","group":"canonical_sign_and_free_ghost",
                   "passed":not restrict(qtable["p_a"],witness).is_zero(),
                   "defect":restrict(qtable["p_a"],witness).record()})
    next_coefficient=restrict(pb(H,Ha),{pa:0})
    eq("exceptional_root_next_tangency_coefficient",next_coefficient,-s.Rational(9,2)*pp*s.diff(F,phi)/a)
    p,z=s.symbols("p z",real=True)
    normalization={a:2,pa:0,pp:s.pi**2*p}
    eq("normalized_actual_H",(H.subs(normalization)/s.pi**2).subs(zphi,z),p**2/32-12+12*(1-z)**2)
    eq("normalized_actual_Ha",(Ha.subs(normalization)/s.pi**2).subs(zphi,z),-3*p**2/64-6+18*(1-z)**2)
    eq("normalized_next_tangency",restrict(next_coefficient,normalization).coefficient(()).subs(zphi,z),
       -s.Rational(9,2)*s.pi**2*beta*p*z*(1-z))

    # Ghost restriction is a boundary pullback, not deletion of the bulk sector.
    a0=s.Symbol("a_0",positive=True)
    phi0,n0=s.symbols("phi_0 N_0",real=True)
    endpoint={a:a0,phi:phi0,n:n0}
    zero_ghosts=("c_g","rho")
    eq("ghost_fixed_endpoint_charge",restrict(omega,endpoint,zero_ghosts),group="ghost_fixed_endpoint")
    endpoint_table={key:restrict(qtable[key],endpoint,zero_ghosts) for key in ("a","phi","N","c","rho")}
    for key,value in endpoint_table.items():
        eq("ghost_fixed_endpoint_Q_"+key,value,group="ghost_fixed_endpoint")
    # Free barred momenta may move; they are not additional fixed constraints.
    eq("ghost_fixed_free_bar_rho_direction",restrict(qtable["bar_rho"],endpoint,zero_ghosts),H.subs(endpoint),"ghost_fixed_endpoint")
    eq("ghost_fixed_free_bar_c_direction",restrict(qtable["bar_c"],endpoint,zero_ghosts),Pi,"ghost_fixed_endpoint")
    return {"checks":checks,"actual_classical_H":str(H),"Q_convention":"QF={Omega,F}; {q,p}=+1; symmetric odd brackets +1",
        "actual_Q_table":{key:value.record() for key,value in qtable.items()},
        "analytic_proof":"cpt_temporal_folded_susy/STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_DERIVATION.md",
        "actual_finite_lift":"R_i=T_{s_i}, J from compact-bump Gram inverse, O_A=J A R exists on the original test carrier; PDE/bump existence is analytic, not numerically evaluated",
        "adjoint_obstruction":"Nonzero right-killing O p_N=0 cannot have a same-carrier adjoint when p_N is symmetric and injective; split lifts fail this necessary observable condition",
        "general_lift_boundary":"O=J A R+B, RB=0; nonzero compatible O requires B p_N !=0. No general lift or all-observable no-go is claimed",
        "fixed_a_free_ghost":"Exact a=2, undeformed classical charge, real H=0 body, independent free c: no fully tangent locus, including the exceptional root",
        "ghost_fixed_endpoint":"a,phi,N fixed and c=rho=0 gives a finite canonical Q-tangent Lagrangian with zero primitive/charge pullback; dimension/primitive proof analytic",
        "remaining":"Full self-adjoint H+p_N realization, kernel-active star observable, selected positive metric, bulk-induced BFV/quantum state map, CPT/sewing and original joint cycle"}


def main() -> int:
    started = time.monotonic()
    result = {"schema":"ice-starobinsky-quotient-lift-bfv-boundary/v1","status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Can a quotient-only lift on the actual compact-N carrier be a star observable, and does the declared canonical BFV charge preserve a fixed-a endpoint?",
        "scope":"SUPPORTING_METHOD: actual finite quotient lifts and finite canonical boundary classification; G1 unchanged",
        "non_claim":"No full physical observable algebra, selected positive metric, BFV/CPT sewing or G1 original cycle.",
        "reproduction_command":"./ice run starobinsky_quotient_lift_bfv_boundary",
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
        result["status"]="SCOPED_QUOTIENT_LIFT_ADJOINT_OBSTRUCTION_AND_CANONICAL_ENDPOINT"
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
    print("Nonzero quotient-only lifts fail same-carrier adjoint compatibility; kernel action is required")
    print("Free-ghost fixed-a branch fails; ghost-fixed finite canonical endpoint exists; full BFV/CPT remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
