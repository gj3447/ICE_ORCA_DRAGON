"""Check exact identities supporting a Neumann simultaneous dual-state construction.

PDE existence uses an analytic source theorem, not a computed PDE solution array.
No selected physical product, RAQ, full CPT sewing or original cycle.
Run only clean committed sources with ./ice run starobinsky_dual_cauchy.
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
RESULT = HERE / "STAROBINSKY_DUAL_CAUCHY_RESULT.json"
DERIVATION = HERE / "STAROBINSKY_DUAL_CAUCHY_DERIVATION.md"
PINS = {
    "cpt_boundary_sewing_lean.py": "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb",
    "STAROBINSKY_WARD_DOMAIN_DERIVATION.md": "a7a62e4084554eba5f1dd5b9100903f1ea689c448c9952062d69686daa2f098f",
    "STAROBINSKY_WARD_DOMAIN_RESULT.json": "929bc9d5acdf583e7335efa57255a2cca48665dced009b3fe4f6e35c9305c5e9",
    "STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md": "6f38da66b0fc511c21c8f26919a41417200ff36e00346997b095f3f261c72da6",
}
for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise RuntimeError(f"changed convention or audit dependency: {name}")

from cpt_boundary_sewing_lean import audit_axioms, checked, elaborate


def provenance() -> dict:
    paths = [
        Path(__file__), DERIVATION, *(HERE / name for name in PINS),
        PROJECT / "CptSewing/DualState.lean", PROJECT / "dual-state-proof-index.json",
        PROJECT / "lean-toolchain", PROJECT / "lakefile.toml",
        PROJECT / "lake-manifest.json", ROOT / "uv.lock",
    ]
    records = {}
    for path in paths:
        rel = str(path.relative_to(ROOT))
        data = path.read_bytes()
        committed = subprocess.run(
            ["git", "show", f"HEAD:{rel}"], cwd=ROOT,
            capture_output=True, check=True, timeout=10,
        ).stdout
        if data != committed:
            raise ValueError(f"uncommitted input: {rel}")
        records[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    prior = json.loads((HERE / "STAROBINSKY_WARD_DOMAIN_RESULT.json").read_text())
    if prior["status"] != "SCOPED_LOCAL_WARD_CANCELLATION_DOES_NOT_DEFINE_INVARIANT_BFV_TEST_SPACE":
        raise ValueError("unexpected domain-obstruction predecessor")
    return {"source_commit": checked(["git", "rev-parse", "HEAD"], cwd=ROOT),
            "inputs": records, "python": platform.python_version(), "sympy": s.__version__}


def lean_audit() -> dict:
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
        dependencies.append({"name": package["name"], "rev": revision})
    if not any(p["name"] == "mathlib" and p["rev"] ==
               "db584cd6d46c92f209a44c0f1c829460d327499d" for p in dependencies):
        raise ValueError("wrong mathlib revision")
    index = json.loads((PROJECT / "dual-state-proof-index.json").read_text())
    source = (PROJECT / index["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != index["theorems"]:
        raise ValueError("incomplete Lean theorem index")
    expected = [index["namespace"] + "." + name for name in names]
    payload = source + "\n" + "\n".join(f"#check {n}\n#print axioms {n}" for n in expected) + "\n"
    with tempfile.TemporaryDirectory(prefix="ice-dual-cauchy-") as temp:
        run = elaborate(payload, Path(temp), "DualStateAudit")
    result = {"version": version, "dependencies": dependencies, "elaboration": run,
              "scope": "finite rank-one coefficient algebra only; no PDE existence, dual injectivity or physical product theorem"}
    if run["exit_code"] != 0 or run["stderr"].strip() or any(
        m.get("severity") in {"warning", "error"} for m in run["messages"]
    ):
        result["accepted"] = False
        return result
    records = audit_axioms(run["messages"], expected)
    result.update(theorems=records, theorem_count=len(expected),
                  accepted=all(r["accepted"] for r in records.values()))
    return result


def derive() -> dict:
    a = s.symbols("a", positive=True)
    x, phi, n = s.symbols("x phi N", real=True)
    beta = s.sqrt(s.Rational(2, 3))
    f = -1/(24*s.pi**2*a)
    b = 1/(4*s.pi**2*a**3)
    potential = -6*s.pi**2*a+s.Rational(3, 2)*s.pi**2*a**3*(1-s.exp(-beta*phi))**2
    w = potential-s.diff(f, a, 2)/4
    v = -s.Rational(1, 2)-144*s.pi**4*s.exp(4*x)+36*s.pi**4*s.exp(6*x)*(1-s.exp(-beta*phi))**2
    checks = []

    def equal(name, actual, expected=0, group="actual_Weyl_Cauchy_transform"):
        residual = s.simplify(s.expand(actual-expected))
        checks.append({"id":name, "group":group, "passed":residual == 0, "residual":str(residual)})

    def h(z):
        return -s.diff(f*s.diff(z, a), a)-b*s.diff(z, phi, 2)+w*z

    chi = s.Function("chi")(x, phi)
    actual = (24*s.pi**2*a**2*h(a*chi.subs(x, s.log(a)))).subs(a, s.exp(x)).doit()
    target = s.diff(chi, x, 2)-6*s.diff(chi, phi, 2)+v*chi
    equal("actual_Weyl_log_rescale_PDE", actual, target)
    equal("Weyl_correction_scaled_before_rescale", 24*s.pi**2*a**3*(w-potential), s.Rational(1, 2))
    q, qx, g, r = s.symbols("q q_x g r", real=True)
    equal("terminal_s_trace_is_g", (2*q).subs(q, g/2), g)
    equal("terminal_Neumann_derivative_zero", (q+qx).subs({q:g/2, qx:-g/2}))
    equal("general_Robin_transformed_trace", q+(2*r-1)*q-r*(2*q))

    u = s.Function("u")(a, phi, n)
    state = s.Function("state")(a, phi)
    divergence = s.diff(f*(state*s.diff(u,a)-s.diff(state,a)*u), a)+b*s.diff(
        state*s.diff(u,phi)-s.diff(state,phi)*u, phi)
    equal("actual_H_bilinear_Green_divergence", h(state)*u-state*h(u), divergence, "Green_primary_current")
    equal("N_independent_state_primary_zero", -s.I*s.diff(state,n), group="Green_primary_current")
    z1, z2, d1, d2 = s.symbols("z1 z2 d1 d2", complex=True)
    equal("Neumann_upper_Green_face_zero", (f*(z1*d2-d1*z2)).subs({d1:0,d2:0}), group="Green_primary_current")
    # p stands for conjugate(chi_1); real coefficients imply Pp=0 too.
    p = s.Function("p")(x, phi)
    qfun = s.Function("q")(x, phi)
    current = p*s.diff(qfun,x)-s.diff(p,x)*qfun
    evolution = s.diff(current,x).subs({s.diff(qfun,x,2):6*s.diff(qfun,phi,2)-v*qfun,
                                         s.diff(p,x,2):6*s.diff(p,phi,2)-v*p})
    equal("on_shell_full_phi_current_divergence", evolution,
          6*s.diff(p*s.diff(qfun,phi)-s.diff(p,phi)*qfun,phi), "Green_primary_current")
    equal("common_real_Robin_KG_terminal_zero", z1*((2*r-1)*z2)-((2*r-1)*z1)*z2,
          group="Green_primary_current")
    p_a, q_a = a*p.subs(x,s.log(a)), a*qfun.subs(x,s.log(a))
    equal("original_a_Green_current_rescaling", (f*(p_a*s.diff(q_a,a)-s.diff(p_a,a)*q_a)).subs(a,s.exp(x)).doit(),
          -current/(24*s.pi**2), "Green_primary_current")

    zr, zi, wr, wi = s.symbols("z_re z_im w_re w_im", real=True)
    z, zw = zr+s.I*zi, wr+s.I*wi
    form = s.conjugate(z)*zw
    equal("rank_one_Hermitian", s.conjugate(form), s.conjugate(zw)*z, "rank_one_form_scope")
    equal("rank_one_diagonal_sum_of_squares", s.conjugate(z)*z, zr**2+zi**2, "rank_one_form_scope")
    equal("rank_one_K_covariance", z*s.conjugate(zw), s.conjugate(form), "rank_one_form_scope")
    equal("rank_one_left_constraint_kernel", form.subs({zr:0,zi:0}), group="rank_one_form_scope")
    equal("rank_one_right_constraint_kernel", form.subs({wr:0,wi:0}), group="rank_one_form_scope")
    return {
        "checks":checks,
        "operator":{"f":str(f), "b":str(b), "W":str(w), "P_potential":str(v),
                    "ordering_density":"actual Weyl; hbar=1; flat auxiliary density"},
        "domain":{"box":"[1/2,2] x [-1,2] x [1/4,2]",
                  "test_space":"smooth collar-zero except a=2; partial_a H^k p_N^m u|_2=0 for all k,m>=0",
                  "PDE_extension":"open R_x x R_phi, metric -dx^2+dphi^2/6; then restrict"},
        "analytic_construction":{
            "proof_kind":"source-theorem application and analytic Green/injectivity proof; NOT executed PDE or Lean existence proof",
            "source":"https://arxiv.org/pdf/0806.1036v1",
            "locator":"Theorems 3.2.11-12, printed pp.85-87",
            "Cauchy_data":"chi(log 2,phi)=g/2, chi_x(log 2,phi)=-g/2, g in C_c^infty((-1,2))",
            "dual":"T_g[u]=integral_B a chi_g(log a,phi) u; injective in g; T_g H=T_g p_N=0",
            "KG":"i integral over all R_phi (bar chi_1 chi_2,x-bar chi_1,x chi_2)=0 for all pairs in this family",
            "current_scope":"conservation over whole R_phi, not a truncated box",
            "positive_form":"real nonzero seed; F_T(u,v)=bar T[u] T[v]; Phi/ker T is a positive one-dimensional quotient",
            "noncanonical":"independent real seeds give different kernels; arbitrary positive rescaling",
            "K_scope":"conjugation antiunitary involution on chosen quotient, not full CPT",
        },
        "analytic_proof":str(DERIVATION.relative_to(ROOT)),
        "remaining":"observable-* compatible physical product/RAQ, full BFV ghosts, mQME/sewing kernel and original cycle",
    }


def main() -> int:
    start = time.monotonic()
    result = {
        "schema":"ice-starobinsky-dual-cauchy/v1", "status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Does the repaired Neumann test-space dual contain nonzero simultaneous actual H and p_N solutions, and what do KG and chosen rank-one forms show?",
        "scope":"SUPPORTING_METHOD: fixed Weyl ordering, finite a slab, explicit Neumann choice",
        "non_claim":"No selected physical Hilbert/RAQ product, full BFV/CPT sewing, original cycle or new physics.",
        "reproduction_command":"./ice run starobinsky_dual_cauchy",
    }
    try:
        result["provenance"] = provenance()
        result["symbolic"] = derive()
        result["lean"] = lean_audit()
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not result["lean"]["accepted"]:
            raise ValueError("symbolic or Lean control failed; see raw diagnostics")
        result["status"] = "SCOPED_NEUMANN_CAUCHY_DUAL_FAMILY_WITH_DEGENERATE_KG_FORM"
    except Exception as error:
        result["failure"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.monotonic()-start
    payload = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
    if len(payload.encode()) > 120_000:
        raise RuntimeError("unexpectedly large result")
    RESULT.write_text(payload)
    print(result["status"])
    if result["status"] == "FAILED":
        print(result["failure"])
        return 1
    print(f"exact controls: {len(result['symbolic']['checks'])}; Lean theorems: {result['lean']['theorem_count']}")
    print("Analytic source-theorem construction: injective simultaneous dual family; full-R_phi KG form zero")
    print("Chosen positive rank-one quotient exists; physical product and full CPT sewing remain unresolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
