"""Construct the compact-primary contraction and correctly graded seam evaluation.

Actual integral/PDE constructions remain analytic; exact controls and Lean
verify the chain homotopy, cohomology detector and source sign boundaries.
No physical product, quantum interval amplitude or original-cycle claim.
Run committed sources only: ./ice run starobinsky_primary_reduction_graded_sewing.
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
INDEX = PROJECT / "primary-reduction-graded-sewing-proof-index.json"
RESULT = HERE / "STAROBINSKY_PRIMARY_REDUCTION_GRADED_SEWING_RESULT.json"
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
PINS.update({'STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_RESULT.json': 'ba863b486d6503193776e35cc29e317b8036f7583d2efa6264d8e0a73e304496', 'STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_DERIVATION.md': '8611a354760296d16a211dddb91b2127dd68e9e2da1a73bcb15bc7200a375366'})

for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise ValueError(f"changed analytic/audit input: {name}")

from cpt_boundary_sewing_lean import ALLOWED_AXIOMS, audit_axioms, checked, elaborate
# Utility import only: no historical inputs or main routine are executed.
from gate1_v0_improved_static_bfv_source import Exterior as E, graded_poisson


def provenance(index: dict) -> dict:
    files = [Path(__file__), HERE / "STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md", HERE / "STAROBINSKY_GRADED_DUAL_SEWING_DERIVATION.md", ROOT / "docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md", ROOT / "docs/research/ICE_STAROBINSKY_GRADED_SEAM_ADVERSARIAL_REVIEW_2026-09-07.md", INDEX, *(PROJECT / m["source"] for m in index["modules"]),
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
    with tempfile.TemporaryDirectory(prefix="ice-primary-graded-sewing-") as temp:
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
    phi,n,nlo,nhi=s.symbols("phi N N_lo N_hi",real=True)
    f=-1/(24*s.pi**2*a); b=1/(4*s.pi**2*a**3)
    beta=s.sqrt(s.Rational(2,3))
    U=-6*s.pi**2*a+s.Rational(3,2)*s.pi**2*a**3*(1-s.exp(-beta*phi))**2
    W=U-s.diff(f,a,2)/4
    def H(z): return -s.diff(f*s.diff(z,a),a)-b*s.diff(z,phi,2)+W*z
    def p(z): return -s.I*s.diff(z,n)
    checks=[]
    def eq(name,actual,expected=0,group="actual_primary_and_support"):
        residual=E.coerce(actual)-E.coerce(expected)
        checks.append({"id":name,"group":group,"passed":residual.is_zero(),"residual":residual.record()})
    u=s.Function("u")(a,phi,n); v=s.Function("v")(a,phi)
    chi=s.Function("chi")(n); r=s.Function("R_u")(a,phi)
    Ku=s.I*s.Integral(u-chi*r,(n,nlo,n))
    eq("actual_pK_is_identity_minus_section",p(Ku),u-chi*r)
    eq("actual_H_commutes_primary",H(p(u)),p(H(u)))
    eq("actual_H_commutes_section",H(chi*v),chi*H(v))
    eq("actual_H_commutes_corrected_primitive_integrand",H(u-chi*r),H(u)-chi*H(r))
    trace=s.Function("uN")(n)
    integral_p=-s.I*s.integrate(s.diff(trace,n),(n,nlo,nhi))
    eq("R_p_is_endpoint_traces",integral_p,-s.I*(trace.subs(n,nhi)-trace.subs(n,nlo)))
    eq("R_p_vanishes_on_two_collars",integral_p.subs({trace.subs(n,nhi):0,trace.subs(n,nlo):0}))
    eq("K_p_recovers_u_on_lower_collar",s.I*(-s.I)*(trace-trace.subs(n,nlo)).subs(trace.subs(n,nlo),0),trace)
    ru,ic=s.symbols("R_u integral_chi")
    eq("corrected_total_integral_zero",(ru-ic*ru).subs(ic,1))
    checks.append({"id":"bare_primitive_upper_trace_generically_nonzero","group":"actual_primary_and_support","passed":s.I*ru!=0,"expression":str(s.I*ru),"scope":"formal trace diagnostic; actual compact support justified in derivation"})
    c,rho,br,bc=(E.generator(k) for k in ("c_g","rho","bar_rho","bar_c"))
    u0,x,y,z,l2,lc,lr,l0=s.symbols("u0 x y z lambda2 lambda_c lambda_rho lambda0")
    primal=E.scalar(u0)+c*x+rho*y+c*rho*z
    dual=E.scalar(l2)+c*lr-rho*lc+c*rho*l0
    paired=(dual*primal).terms.get(("c_g","rho"),s.Integer(0))
    eq("ordered_Berezin_dual_left_evaluation",paired,l2*z+lc*x+lr*y+l0*u0,"graded_dual_and_Ward")
    wrong=(primal*dual).terms.get(("c_g","rho"),s.Integer(0))
    eq("swapping_Berezin_factors_changes_middle_signs",wrong-paired,-2*(lc*x+lr*y),"graded_dual_and_Ward")
    hx,hy,px,py=s.symbols("H_x H_y p_x p_y")
    eq("actual_ghost_q1_orientation",c*(c*hx+rho*hy)+rho*(c*px+rho*py),c*rho*(hy-px),"graded_dual_and_Ward")
    # Finite exact matrix audit ONLY for the two-ghost algebra, not the PDE.
    hval,pval=s.symbols("H_formal p_formal")
    q0=s.Matrix([hval,pval]); q1=s.Matrix([[-pval,hval]])
    d0=q1.T; d1=-q0.T
    eq("graded_transpose_square",(d1*d0)[0,0],group="graded_dual_and_Ward")
    eq("Ward_degree_zero_matrix",(d1*s.Matrix([lc,lr]))[0]+(s.Matrix([[lc,lr]])*q0)[0],group="graded_dual_and_Ward")
    xy=s.Matrix([x,y])
    eq("Ward_degree_one_matrix",l2*(q1*xy)[0]-(d0*l2).dot(xy),group="graded_dual_and_Ward")
    theta=s.diag(1,1,-1,-1)
    Q=s.Matrix([[0,0,0,0],[hval,0,0,0],[pval,0,0,0],[0,-pval,hval,0]])
    theta_defect=theta*Q.subs(pval,-pval)-Q*theta
    checks.append({"id":"antilinear_coordinate_ghost_flip_covariance","group":"graded_dual_and_Ward","passed":theta_defect == s.zeros(4),"residual_matrix":[str(t) for t in theta_defect]})
    pa,pp,Pi=s.symbols("p_a p_phi Pi",real=True)
    HL=f*pa**2+b*pp**2+U
    omega=c*HL+rho*Pi; psi=-n*br
    ep=((a,pa),(phi,pp),(n,Pi)); op=(("c_g","bar_rho"),("rho","bar_c"))
    eq("source_charge_master",graded_poisson(omega,omega,ep,op),group="source_and_orientation")
    gauge=-graded_poisson(omega,psi,ep,op)
    eq("source_gauge_hamiltonian_sign",gauge,n*HL+br*rho,"source_and_orientation")
    eq("source_primary_BRST_sign",graded_poisson(omega,E.scalar(n),ep,op),-rho,"source_and_orientation")
    ad,pd=s.symbols("a_dot phi_dot",real=True)
    pa_sol=-12*s.pi**2*a*ad/n; pp_sol=2*s.pi**2*a**3*pd/n
    lag=pa*ad+pp*pd-n*HL
    e1,e2,nd=s.symbols("e1 e2 N_dot",real=True)
    extended=pa*ad+pp*pd+Pi*nd-e1*HL-e2*Pi
    eq("CMW_full_primary_component_bridge",extended.subs({e1:n,e2:nd}),lag,"source_and_orientation")
    eq("CMW_zero_second_multiplier_leaves_primary_kinetic",extended.subs({e1:n,e2:0})-lag,Pi*nd,"source_and_orientation")
    bp_in,bp_out=s.symbols("alpha_in alpha_out")
    eq("CMW_boundary_master_cancellation",(bp_out-bp_in)+(bp_in-bp_out),group="source_and_orientation")
    sigma=s.Symbol("sigma")
    eq("CMW_primary_bulk_split",Pi*nd-(sigma+nd)*Pi,-Pi*sigma,"source_and_orientation")
    # Here br=sigma_plus, bc=d_s sigma_plus, c=d_s rho; all are odd.
    total_odd_derivative=bc*rho+br*c
    eq("CMW_odd_boundary_split_sign",-br*c,-rho*bc-total_odd_derivative,"source_and_orientation")
    st=s.Symbol("s",real=True)
    sp=s.Function("sigma_plus")(st); dn=s.Function("delta_N")(st)
    eq("CMW_cotangent_boundary_primitive",sp*s.diff(dn,st),s.diff(sp*dn,st)-s.diff(sp,st)*dn,"source_and_orientation")
    eq("source_momentum_elimination",lag.subs({pa:pa_sol,pp:pp_sol}),-6*s.pi**2*a*ad**2/n+s.pi**2*a**3*pd**2/n-n*U,"source_and_orientation")
    def transform(poly, signs):
        return E({m: coefficient.subs({pa:-pa,pp:-pp,Pi:-Pi}, simultaneous=True)*s.prod(signs.get(g,1) for g in m) for m,coefficient in poly.terms.items()})
    eq("classical_seam_charge_flips",transform(omega,{"c_g":-1,"bar_c":-1}),-omega,"source_and_orientation")
    eq("coordinate_antilinear_charge_preserved",transform(omega,{"rho":-1,"bar_rho":-1}),omega,"source_and_orientation")
    return {"checks":checks,
        "primary_failure_class":"inference",
        "control_groups":["actual_primary_and_support","graded_dual_and_Ward","source_and_orientation"],
        "analytic_derivation":"cpt_temporal_folded_susy/STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md",
        "actual_contraction":"R_N=integral_N, J_chi=chi*, K_chi=i integral_lower^N(1-J_chi R_N); FI=1 and Id-IF=qh+hq",
        "cohomology":"H0=H1=0; H2 is isomorphic to Psi/H Psi and infinite-dimensional by actual Cauchy/Gram detectors; no physical degree reassignment",
        "graded_pairing":"T_g[z]=t_g[R_N z], closed dual degree -2; explicit Ward and dual-left Berezin signs; selected actual detectors continuous",
        "choice_scope":"normalized real compact N bump changes representatives by exact terms; no gauge/contour/physics promotion",
        "source_scope":"CMW component action splits into a minimal bulk source and formal doublet sectors with action boundary -[sigma_plus*rho] and cotangent boundary [sigma_plus*deltaN]; endpoint and global cycle equivalence remain separate",
        "continuous_coefficient_dual":"For the stated ambient C-infinity continuous dual, V=T composed with K is continuous and p-transpose V=T; hence its coefficient-only top cohomology is zero, unlike correctly graded top detectors",
        "noncomputed":"No numerical PDE data, full continuous-dual cohomology, nonperturbative BV integral, quantum CPT kernel, positive norm or G1 cycle"}


def main() -> int:
    started=time.monotonic()
    result={"schema":"ice-starobinsky-primary-reduction-graded-sewing/v1","status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Can the actual compact-primary complex be reduced by a cohomology-preserving homotopy and paired with its correctly graded dual?",
        "scope":"SUPPORTING_METHOD: actual test-space contraction and graded evaluation; original source/cycle/physical product remain open",
        "non_claim":"No source-selected physical state, full quantum BFV/CPT amplitude or G1 original cycle.",
        "reproduction_command":"./ice run starobinsky_primary_reduction_graded_sewing",
        "allowed_axioms":sorted(ALLOWED_AXIOMS),"modules":[]}
    try:
        index=json.loads(INDEX.read_text()); result["provenance"]=provenance(index)
        result["symbolic"]=derive()
        for module in index["modules"]:
            if time.monotonic()-started>65: raise TimeoutError("insufficient time for another Lean module")
            result["modules"].append(audit_module(module))
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not all(m["accepted"] for m in result["modules"]):
            raise ValueError("symbolic or Lean audit failed; see raw diagnostics")
        result["theorem_count"]=sum(m["theorem_count"] for m in result["modules"])
        result["status"]="SCOPED_PRIMARY_CHAIN_EQUIVALENCE_AND_NONZERO_GRADED_PAIRING"
    except Exception as error:
        result["failure"]=f"{type(error).__name__}: {error}"
    result["elapsed_seconds"]=time.monotonic()-started
    payload=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if len(payload.encode())>200_000: raise RuntimeError("unexpectedly large output")
    RESULT.write_text(payload); print(result["status"])
    if "symbolic" in result: print(f"exact controls: {sum(c['passed'] for c in result['symbolic']['checks'])}/{len(result['symbolic']['checks'])}")
    for module in result["modules"]: print(f"{module['source']}: accepted={module['accepted']}; expected={module['expected_theorem_count']}")
    if result["status"]=="FAILED": print(result["failure"]); return 1
    print(f"Lean theorems: {result['theorem_count']}")
    print("Primary contraction preserves top classes and dual evaluation; positive product and quantum source remain open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
