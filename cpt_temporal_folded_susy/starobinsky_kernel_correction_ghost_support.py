"""Audit finite-rank kernel corrections and the support of top-ghost classes.

Actual compact-carrier constructions remain analytic; exact controls and Lean
separate a kernel-active star correction from an observable, and test-complex
classes from a coefficient-algebraic-dual endpoint. No physical metric/CPT claim.
Run committed sources only: ./ice run starobinsky_kernel_correction_ghost_support.
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
INDEX = PROJECT / "kernel-correction-ghost-support-proof-index.json"
RESULT = HERE / "STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_RESULT.json"
PINS = {
    "STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_RESULT.json": "4e57d2535694d1c1bfb174ca04ae4819b085ca8a5d9ea2023bf7f4f80e7aaeb7",
    "STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_DERIVATION.md": "b3674f79572814940239297982fd44fc391c15439b32c1fb063c40a22a5e3355",
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
from gate1_v0_improved_static_bfv_source import Exterior as E


def provenance(index: dict) -> dict:
    files = [Path(__file__), HERE / "STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_DERIVATION.md", INDEX, *(PROJECT / m["source"] for m in index["modules"]),
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
    with tempfile.TemporaryDirectory(prefix="ice-kernel-ghost-support-") as temp:
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
    phi,n,n0=s.symbols("phi N N_0",real=True)
    f=-1/(24*s.pi**2*a)
    b=1/(4*s.pi**2*a**3)
    beta=s.sqrt(s.Rational(2,3))
    U=-6*s.pi**2*a+s.Rational(3,2)*s.pi**2*a**3*(1-s.exp(-beta*phi))**2
    W=U-s.diff(f,a,2)/4
    def H(z): return -s.diff(f*s.diff(z,a),a)-b*s.diff(z,phi,2)+W*z
    def p(z): return -s.I*s.diff(z,n)
    checks=[]
    def eq(name,actual,expected=0,group="actual_carrier_and_transpose"):
        residual=E.coerce(actual)-E.coerce(expected)
        checks.append({"id":name,"group":group,"passed":residual.is_zero(),"residual":residual.record()})

    F=s.Function("F")(a,phi)
    chi=s.Function("chi")(n)
    w=F*s.diff(chi,n)
    eq("actual_rank_one_primary_w",p(w),-s.I*F*s.diff(chi,n,2))
    eq("actual_rank_one_primary_squared_w",p(p(w)),-F*s.diff(chi,n,3))
    eq("real_rank_one_moment_is_collar_boundary",w*p(w),-s.I*s.diff(w*w,n)/2)
    z,u=(s.Function(k)(a,phi,n) for k in ("z","u"))
    eq("actual_Weyl_bilinear_Green_divergence",z*H(u)-H(z)*u,
       s.diff(f*(u*s.diff(z,a)-z*s.diff(u,a)),a)+b*s.diff(u*s.diff(z,phi)-z*s.diff(u,phi),phi))
    eq("actual_primary_bilinear_transpose_sign",z*p(u)+p(z)*u,-s.I*s.diff(z*u,n))
    eq("actual_H_primary_for_coordinate_complex",H(p(u))-p(H(u)))
    zu,uu,za,ua=s.symbols("z_upper u_upper za_upper ua_upper")
    flux=f.subs(a,2)*(uu*za-zu*ua)
    eq("shared_Neumann_Green_face_vanishes",flux.subs({za:0,ua:0}))

    # The helper's other two odd generators are not introduced in this selected
    # coordinate polarization; no nonminimal/negative-degree result is inferred.
    c,rho=E.generator("c_g"),E.generator("rho")
    Hx,Hy,px,py,Hz,pz=s.symbols("H_x H_y p_x p_y H_z p_z")
    eq("coordinate_ghost_order",rho*c,-c*rho,"ghost_degree_and_chain_sign")
    q1=c*(c*Hx+rho*Hy)+rho*(c*px+rho*py)
    eq("actual_two_ghost_q1_sign",q1,c*rho*(Hy-px),"ghost_degree_and_chain_sign")
    eq("top_ghost_is_closed",c*c*rho*Hz+rho*c*rho*pz,group="ghost_degree_and_chain_sign")
    eq("ghost_delta_c_annihilation",c*c*rho,group="ghost_degree_and_chain_sign")
    eq("ghost_delta_rho_annihilation",rho*c*rho,group="ghost_degree_and_chain_sign")
    eq("coefficient_dual_chain_degree_zero",c*Hz+rho*(-pz),c*Hz-rho*pz,"ghost_degree_and_chain_sign")
    dual_q1=c*(-rho*Hy)+rho*(c*(-px))
    eq("coefficient_dual_chain_degree_one",dual_q1,-c*rho*(Hy-px),"ghost_degree_and_chain_sign")
    defect=(c*Hz-rho*pz)-(c*Hz+rho*pz)
    eq("unflipped_ghost_embedding_defect",defect,-2*rho*pz,"ghost_degree_and_chain_sign")
    checks.append({"id":"unflipped_ghost_embedding_defect_nonzero","group":"ghost_degree_and_chain_sign",
                   "passed":not defect.is_zero(),"defect":defect.record(),"scope":"formal coefficient identity; actual p is nonzero on the carrier"})

    # Endpoint traces on the closed-box test carrier, not an interior Dirac at a=2.
    trace=s.Function("u_trace")(n)
    ptS=-s.I*s.integrate(s.diff(trace,n),(n,n0,2))
    d0=trace.subs(n,n0)
    eq("endpoint_transpose_primitive_with_upper_trace",ptS,-s.I*(trace.subs(n,2)-d0),"endpoint_support")
    ptS_collar=ptS.subs(trace.subs(n,2),0)
    eq("endpoint_transpose_primitive_collar",ptS_collar,s.I*d0,"endpoint_support")
    ptV=-s.I*ptS_collar
    eq("endpoint_V_transpose_maps_to_delta",ptV,d0,"endpoint_support")
    hv=s.Symbol("Htranspose_V")
    eq("endpoint_top_candidate_is_exact",c*(-c*hv)+rho*(-c*ptV),c*rho*d0,"endpoint_support")
    ghostfree_primary=-s.I*s.diff(trace,n).subs(n,n0)
    checks.append({"id":"ghost_free_endpoint_primary_is_not_identically_zero","group":"endpoint_support",
                   "passed":ghostfree_primary!=0,"expression":str(ghostfree_primary),
                   "scope":"nonzero trace-derivative functional; actual repaired-carrier witnesses supplied analytically"})
    eq("ket_versus_transpose_Heaviside_sign",p(s.I*s.Heaviside(n-n0)),s.DiracDelta(n-n0),"endpoint_support")
    eq("bra_density_Heaviside_primitive",s.I*s.diff(-s.I*s.Heaviside(n-n0),n),s.DiracDelta(n-n0),"endpoint_support")
    return {"checks":checks,
      "analytic_proof":"cpt_temporal_folded_susy/STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_DERIVATION.md",
      "actual_kernel_correction":"w=d_N(F*chi) real interior bump; K_w u=<w,u>w is bounded, self-adjoint, carrier-preserving, R K_w=0 and K_w p_N!=0, but [p_N,K_w]w!=0",
      "finite_rank_result":"Bounded finite-rank K and K-adjoint preserving Phi, with R K=A R, force A=0; lambda I+K induces only lambda I on that finite quotient",
      "compact_test_top_cohomology":"Actual constrained-dual Gram sections yield n independent H^2(Phi tensor Lambda(c,rho)) classes for every finite n; H^0 remains zero; no physical degree reassignment",
      "coefficient_algebraic_dual":"Phi_alg* tensor Lambda(c,rho), with H^t T=T H and p^t T=T p, has top cohomology zero because p is injective and its algebraic transpose is surjective",
      "embedding":"Bilinear inclusion plus c->c,rho->-rho is a chain injection, not a quasi-isomorphism; it is not the full graded dual or a selected quantum BFV equivalence",
      "endpoint":"D[u]=u(2,phi0,N0); S[u]=integral_N0^2 u(2,phi0,N)dN; p^t(-iS)=D; c rho D=Qhat(-c*(-iS)); explicit C-infinity-continuous primitive, not an L2-bounded or compact-N primitive",
      "remaining":"Infinite-rank/unbounded or other justified observable realization; physical ghost degree, support/topology and half-density module; positive metric; bulk BFV/quantum state/CPT sewing and original cycle"}


def main() -> int:
    started = time.monotonic()
    result = {"schema":"ice-starobinsky-kernel-correction-ghost-support/v1","status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Do finite-rank star-preserving kernel corrections and the direct coefficient-dual endpoint candidate provide a nontrivial selector, and which top-ghost classes survive the stated carriers?",
        "scope":"SUPPORTING_METHOD: actual kernel correction, finite-rank nonselection and carrier-dependent top-ghost classes; G1 unchanged",
        "non_claim":"No full physical observable algebra, selected positive metric, BFV/CPT sewing or G1 original cycle.",
        "reproduction_command":"./ice run starobinsky_kernel_correction_ghost_support",
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
        result["status"]="SCOPED_KERNEL_CORRECTION_NONSELECTION_AND_TOP_GHOST_SUPPORT_CONTRAST"
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
    print("Actual kernel-active star correction exists; finite-rank correction cannot change finite quotient labels")
    print("Compact test top classes are nontrivial; coefficient-dual top classes and direct endpoint are exact; physical BFV/CPT remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
