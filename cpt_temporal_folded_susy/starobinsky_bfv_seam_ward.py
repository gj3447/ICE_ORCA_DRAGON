"""Derive the regulated Starobinsky quantum boundary-sewing Ward defect.

One output: a same-model polarized boundary kernel and its bulk/window defect.
Not a time-sliced trajectory source, self-adjoint extension, or original cycle.
Run only a clean committed source with ./ice run starobinsky_bfv_seam_ward.
"""
from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / "formal/cpt_sewing"
RESULT = HERE / "STAROBINSKY_BFV_SEAM_WARD_RESULT.json"
AUDITOR = HERE / "cpt_boundary_sewing_lean.py"
AUDITOR_SHA = "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb"
if hashlib.sha256(AUDITOR.read_bytes()).hexdigest() != AUDITOR_SHA:
    raise RuntimeError("pinned Lean audit helper changed")
from cpt_boundary_sewing_lean import audit_axioms, checked, elaborate


def provenance() -> dict:
    files = [Path(__file__), AUDITOR, PROJECT / "CptSewing/SeamWard.lean",
             PROJECT / "seam-ward-proof-index.json", PROJECT / "lean-toolchain",
             PROJECT / "lakefile.toml", PROJECT / "lake-manifest.json"]
    records = {}
    for path in files:
        rel = str(path.relative_to(ROOT))
        data = path.read_bytes()
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT,
                                   capture_output=True, check=True, timeout=10).stdout
        if data != committed:
            raise ValueError(f"uncommitted proof input: {rel}")
        records[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    return {"source_commit": checked(["git", "rev-parse", "HEAD"], cwd=ROOT),
            "inputs": records, "python": platform.python_version(), "sympy": s.__version__}


def lean_audit() -> dict:
    if (PROJECT / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.33.0":
        raise ValueError("wrong toolchain")
    version = checked(["lake", "env", "lean", "--version"])
    if not version.startswith("Lean (version 4.33.0,"):
        raise ValueError(version)
    manifest = json.loads((PROJECT / "lake-manifest.json").read_text())
    deps = []
    for p in manifest["packages"]:
        location = PROJECT / manifest["packagesDir"] / p["name"]
        revision = checked(["git", "rev-parse", "HEAD"], cwd=location)
        if revision != p["rev"] or checked(["git", "status", "--porcelain", "--untracked-files=no"], cwd=location):
            raise ValueError(f"modified dependency {p['name']}")
        deps.append({"name": p["name"], "rev": revision})
    if not any(p["name"] == "mathlib" and p["rev"] == "db584cd6d46c92f209a44c0f1c829460d327499d" for p in deps):
        raise ValueError("wrong mathlib pin")
    index = json.loads((PROJECT / "seam-ward-proof-index.json").read_text())
    source = (PROJECT / index["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != index["theorems"]:
        raise ValueError("incomplete Lean theorem index")
    expected = [index["namespace"] + "." + n for n in names]
    payload = source + "\n" + "\n".join(f"#check {n}\n#print axioms {n}" for n in expected) + "\n"
    with tempfile.TemporaryDirectory(prefix="ice-seam-ward-") as temp:
        run = elaborate(payload, Path(temp), "SeamWardAudit")
    # Preserve diagnostics even on a compiler failure.
    result = {"version": version, "dependencies": deps, "elaboration": run}
    if run["exit_code"] != 0 or run["stderr"].strip() or any(m.get("severity") in {"error", "warning"} for m in run["messages"]):
        result["accepted"] = False
        return result
    records = audit_axioms(run["messages"], expected)
    result.update(theorems=records, theorem_count=len(expected),
                  accepted=all(r["accepted"] for r in records.values()))
    return result


# Independent generic bit-mask exterior multiplication, not the Lean coefficient tables.
def wedge(left: dict, right: dict) -> dict:
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if a & b:
                continue
            inversions = sum(1 for i in range(4) for j in range(4) if a & (1 << i) and b & (1 << j) and i > j)
            mask = a | b
            out[mask] = out.get(mask, 0) + (-1)**inversions * ca * cb
    return {k: s.expand(v) for k, v in out.items() if s.expand(v) != 0}


def add(*objects: dict) -> dict:
    out = {}
    for obj in objects:
        for k, v in obj.items():
            out[k] = out.get(k, 0) + v
    return {k: s.expand(v) for k, v in out.items() if s.expand(v) != 0}


def scale(t, obj: dict) -> dict:
    return {k: s.expand(t*v) for k, v in obj.items() if s.expand(t*v) != 0}


def integrate_copy2(obj: dict) -> dict:
    # Right fiber extraction: integral d rho2 d c2 of A(c1,rho1) c2 rho2 is A.
    out = {}
    for mask, coeff in obj.items():
        if mask & 10 != 10:  # indices 1,3 = c2,rho2
            continue
        remaining = mask ^ 10
        inversions = sum(1 for i in (0, 2) for j in (1, 3) if remaining & (1 << i) and i > j)
        out[remaining] = out.get(remaining, 0) + (-1)**inversions * coeff
    return {k: s.expand(v) for k, v in out.items() if s.expand(v) != 0}


def derive() -> dict:
    a1, a2, t = s.symbols("a1 a2 tau", positive=True)
    p1, p2, n1, n2 = s.symbols("phi1 phi2 N1 N2", real=True)
    beta = s.sqrt(s.Rational(2, 3))
    f = lambda a: -1/(24*s.pi**2*a)
    b = lambda a: 1/(4*s.pi**2*a**3)
    u = lambda a, p: -6*s.pi**2*a + s.Rational(3, 2)*s.pi**2*a**3*(1-s.exp(-beta*p))**2
    d, e, ell = a1-a2, p1-p2, n1-n2
    kernel = s.exp(-(d*d+e*e+ell*ell)/(2*t))/(2*s.pi*t)**s.Rational(3, 2)
    checks = []

    def equal(name, actual, expected=0):
        residual = s.simplify(s.expand(actual-expected))
        checks.append({"id": name, "passed": residual == 0, "residual": str(residual)})

    def hw(z, a, p):
        return -f(a)*s.diff(z, a, 2)-s.diff(f(a), a)*s.diff(z, a)-s.diff(f(a), a, 2)*z/4-b(a)*s.diff(z, p, 2)+u(a, p)*z

    difference = (-(f(a1)-f(a2))*(d*d/t**2-1/t)
                  +(s.diff(f(a1), a1)+s.diff(f(a2), a2))*d/t
                  -(s.diff(f(a1), a1, 2)-s.diff(f(a2), a2, 2))/4
                  -(b(a1)-b(a2))*(e*e/t**2-1/t)+u(a1, p1)-u(a2, p2))
    equal("gaussian_H_difference_from_direct_derivatives", (hw(kernel,a1,p1)-hw(kernel,a2,p2))/kernel, difference)
    equal("primary_lapse_interior_cancellation", (s.diff(kernel,n1)+s.diff(kernel,n2))/kernel)
    equal("gaussian_normalized_difference_symmetry", kernel.xreplace({a1:a2,a2:a1,p1:p2,p2:p1,n1:n2,n2:n1}), kernel)
    phi_witness = s.log(2)/beta
    equal("positive_y_chart_witness", s.exp(-beta*phi_witness), s.Rational(1,2))
    witness = s.simplify(difference.subs({a1:1,a2:1,p1:0,p2:phi_witness}))
    equal("Starobinsky_nonzero_Ward_witness", witness, -3*s.pi**2/8)
    checks.append({"id":"witness_nonzero_for_every_positive_width", "passed": bool(witness.is_negative),
                   "coefficient":str(witness), "kernel_at_witness":str(s.simplify(kernel.subs({a1:1,a2:1,p1:0,p2:phi_witness,n1:1,n2:1})))})

    # Formal transpose/Green identity for Weyl ordering on the compact interior core.
    z=s.Function("z")(a1,p1); w=s.Function("w")(a1,p1)
    current_a=f(a1)*(z*s.diff(w,a1)-w*s.diff(z,a1))
    current_phi=b(a1)*(z*s.diff(w,p1)-w*s.diff(z,p1))
    equal("formal_transpose_boundary_current", w*hw(z,a1,p1)-z*hw(w,a1,p1), s.diff(current_a,a1)+s.diff(current_phi,p1))

    # Derive collar terms for arbitrary smooth windows, then record hard-window distributions.
    chi=s.Function("chi")(a1,p1,n1)
    collar=(-f(a1)*s.diff(chi,a1,2)*kernel
            -(2*f(a1)*s.diff(kernel,a1)+s.diff(f(a1),a1)*kernel)*s.diff(chi,a1)
            -b(a1)*s.diff(chi,p1,2)*kernel-2*b(a1)*s.diff(kernel,p1)*s.diff(chi,p1))
    equal("window_commutator_exact", hw(chi*kernel,a1,p1)-chi*hw(kernel,a1,p1), collar)
    chi2=s.Function("chi2")(a2,p2,n2)
    equal("primary_window_flux_exact", s.diff(chi*chi2*kernel,n1)+s.diff(chi*chi2*kernel,n2),
          kernel*(chi2*s.diff(chi,n1)+chi*s.diff(chi2,n2)))
    x, lower, upper=s.symbols("x lower upper", real=True)
    interval=s.Heaviside(x-lower)-s.Heaviside(x-upper)
    equal("hard_face_first_derivative", s.diff(interval,x), s.DiracDelta(x-lower)-s.DiracDelta(x-upper))
    equal("hard_face_second_derivative", s.diff(interval,x,2), s.DiracDelta(x-lower,1)-s.DiracDelta(x-upper,1))

    c1,c2,r1,r2=({1:1},{2:1},{4:1},{8:1})
    ghost=wedge(add(c2,c1),add(r2,scale(-1,r1)))
    def ghost_equal(name, actual, expected):
        defect=add(actual,scale(-1,expected))
        checks.append({"id":name,"passed":not defect,"residual":{str(k):str(v) for k,v in defect.items()}})
    ghost_equal("graded_constraint_pair_cancellation",wedge(add(c1,c2),ghost),{})
    ghost_equal("graded_primary_pair_equality",wedge(r1,ghost),wedge(r2,ghost))
    h1,h2=s.symbols("h1 h2")
    ghost_equal("graded_Ward_factorization",wedge(add(scale(h1,c1),scale(h2,c2)),ghost),scale(h1-h2,wedge(c1,ghost)))
    for name,test,expected in [("one",{0:1},{0:1}),("c2",c2,scale(-1,c1)),("rho2",r2,r1),("c2rho2",wedge(c2,r2),scale(-1,wedge(c1,r1)))]:
        ghost_equal("Berezin_pullback_"+name,integrate_copy2(wedge(ghost,test)),expected)
    checks.append({"id":"constraint_ghost_factor_nonzero","passed":bool(wedge(c1,ghost)),
                   "coefficients":{str(k):str(v) for k,v in wedge(c1,ghost).items()}})
    # Negative orientation control: an incorrect difference of constraint ghosts survives.
    bad=wedge(add(c1,scale(-1,c2)),ghost)
    ghost_equal("wrong_ghost_sign_predicted_defect",bad,scale(2,wedge(c1,ghost)))
    checks.append({"id":"wrong_ghost_sign_nonzero","passed":bool(bad)})

    # Matched constant-coefficient/no-potential model cancels: a control, not ICE evidence.
    A,B=s.symbols("A B")
    constant=lambda a,p: -A*s.diff(kernel,a,2)-B*s.diff(kernel,p,2)
    equal("constant_coefficient_control",(constant(a1,p1)-constant(a2,p2))/kernel)
    return {
        "checks": checks,
        "kernel": {"bosonic":str(kernel),"ghost_order":["c1","c2","rho1","rho2"],
                   "ghost_coefficients":{str(k):str(v) for k,v in ghost.items()},
                   "fiber_Berezin_convention":"integral d rho2 d c2 [A(c1,rho1) c2 rho2] = A(c1,rho1)",
                   "body_domain_per_copy":{"a":["1/2","2"],"phi":["-1","2"],"N":["1/4","2"]},
                   "boundary_extension":"product of hard interval indicators; distribution derivatives retained",
                   "polarization":"(a,phi,N;c,rho); conjugate momenta act by derivatives, not additional delta constraints",
                   "width":"tau>0 in declared reduced coordinate units; Gaussian normalized on R^3, not renormalized at box faces"},
        "operator":{"ordering":"Weyl, hbar=1, flat bosonic density; formal C_c^infty interior core only",
                    "H_W":"-f d_a^2-f_prime d_a-f_second/4-b d_phi^2+U", "f":str(f(a1)),"b":str(b(a1)),"U":str(u(a1,p1)),
                    "Omega_i":"c_i H_W_i - i rho_i d_N_i; all odd factors multiply from the left in one graded tensor algebra"},
        "defect":{"interior_H_difference_divided_by_Gaussian":str(difference),
                  "full_graded_form":"c1*g*(H1-H2)(chi1 chi2 D_tau) - i*rho1*g*(d_N1+d_N2)(chi1 chi2 D_tau)",
                  "window_commutator_copy1":str(collar),"copy2_rule":"swap copy indices; subtract for H1-H2",
                  "hard_window_derivatives":["chi'=delta(x-lower)-delta(x-upper)","chi''=delta'(x-lower)-delta'(x-upper)"],
                  "primary_flux":"D_tau*(chi2*d_N1 chi1 + chi1*d_N2 chi2)",
                  "lapse_lower_face":"N=1/4, positive delta coefficient in derivative of zero extension; not N=0 contact",
                  "lapse_upper_face":"N=2, negative delta coefficient in derivative of zero extension; not infinity",
                  "zero_lapse_contact":"UNRESOLVED: no trajectory kernel or nu->0 identity limit constructed",
                  "witness":{"a1":"1","a2":"1","phi1":"0","phi2":str(phi_witness),"N1":"1","N2":"1","coefficient":str(witness)}},
        "limits":{"formal_delta_seam":"distributional identity on smooth compact interior test functions by formal transpose, not a self-adjoint/domain theorem",
                  "finite_width":"nonzero pointwise Ward defect for every tau>0; this does not refute a controlled distributional tau->0 limit",
                  "trajectory_source":"NOT_CONSTRUCTED", "physical_CPT":"NOT_CONSTRUCTED", "original_relative_cycle":"NOT_CONSTRUCTED"}
    }


def main() -> int:
    start=time.monotonic()
    result={"schema":"ice-starobinsky-bfv-seam-ward/v1", "started_at_utc":datetime.now(timezone.utc).isoformat(),
            "status":"FAILED", "question":"Is the declared Gaussian-regulated Starobinsky boundary sewing exactly BFV closed at finite width?",
            "scope":"Supporting quantum boundary-pairing discriminator only, not a finite bulk path integral",
            "non_claim":"No full trajectory source, original relative class, self-adjoint completion, physical CPT or discovery.",
            "reproduction_command":"./ice run starobinsky_bfv_seam_ward"}
    try:
        result["provenance"]=provenance()
        result["symbolic"]=derive()
        result["lean"]=lean_audit()
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not result["lean"]["accepted"]:
            raise ValueError("symbolic or Lean audit failed; see raw diagnostics")
        result["status"]="SCOPED_GAUSSIAN_SEAM_HAS_NONZERO_BFV_WARD_DEFECT"
    except Exception as error:
        result["failure"]=f"{type(error).__name__}: {error}"
    result["elapsed_seconds"]=time.monotonic()-start
    payload=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if len(payload.encode())>150_000:
        raise RuntimeError("unexpectedly large seam result")
    RESULT.write_text(payload)
    print(result["status"])
    if result["status"]=="FAILED":
        print(result["failure"])
        return 1
    print(f"exact controls: {len(result['symbolic']['checks'])}; Lean theorems: {result['lean']['theorem_count']}")
    print("finite-width witness: (H1-H2)D_tau / D_tau = -3*pi**2/8")
    print("cutoff faces retained; full trajectory and original relative cycle remain open")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
