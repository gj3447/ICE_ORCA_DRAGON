"""Audit the Gaussian Ward weak-pairing limit on the a=2 cutoff face.

Output: one Green face functional with an analytic sqrt(tau) convergence bound.
No physical state, self-adjoint realization, bulk BFV source or original cycle.
Run only clean committed sources with ./ice run starobinsky_ward_face_limit.
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
RESULT = HERE / "STAROBINSKY_WARD_FACE_LIMIT_RESULT.json"
DERIVATION = HERE / "STAROBINSKY_WARD_FACE_LIMIT_DERIVATION.md"
PINS = {
    "cpt_boundary_sewing_lean.py": "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb",
    "starobinsky_bfv_seam_ward.py": "cd98cc9c2cad0f3aead59a769fdbf6f475702f250f80636e3b73ce3743c36671",
    "STAROBINSKY_BFV_SEAM_WARD_RESULT.json": "778964e519ec85e5602cbbd7960f2b6a8a302fd655cfb3fe24ee49155dd62bef",
}
for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise RuntimeError(f"changed convention or audit dependency: {name}")

from cpt_boundary_sewing_lean import audit_axioms, checked, elaborate
from starobinsky_bfv_seam_ward import add, scale, wedge


def provenance() -> dict:
    files = [
        Path(__file__), DERIVATION, *(HERE / name for name in PINS),
        PROJECT / "CptSewing/WardFace.lean", PROJECT / "ward-face-proof-index.json",
        PROJECT / "lean-toolchain", PROJECT / "lakefile.toml",
        PROJECT / "lake-manifest.json", ROOT / "uv.lock",
    ]
    records = {}
    for path in files:
        rel = str(path.relative_to(ROOT))
        data = path.read_bytes()
        committed = subprocess.run(
            ["git", "show", f"HEAD:{rel}"], cwd=ROOT,
            capture_output=True, check=True, timeout=10,
        ).stdout
        if data != committed:
            raise ValueError(f"uncommitted input: {rel}")
        records[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    prior = json.loads((HERE / "STAROBINSKY_BFV_SEAM_WARD_RESULT.json").read_text())
    if prior["status"] != "SCOPED_GAUSSIAN_SEAM_HAS_NONZERO_BFV_WARD_DEFECT":
        raise ValueError("unexpected finite-width predecessor")
    return {
        "source_commit": checked(["git", "rev-parse", "HEAD"], cwd=ROOT),
        "inputs": records, "python": platform.python_version(), "sympy": s.__version__,
        "predecessor_status": prior["status"],
    }


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
    index = json.loads((PROJECT / "ward-face-proof-index.json").read_text())
    source = (PROJECT / index["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != index["theorems"]:
        raise ValueError("incomplete Lean theorem index")
    expected = [index["namespace"] + "." + name for name in names]
    payload = source + "\n" + "\n".join(f"#check {n}\n#print axioms {n}" for n in expected) + "\n"
    with tempfile.TemporaryDirectory(prefix="ice-ward-face-") as temp:
        run = elaborate(payload, Path(temp), "WardFaceAudit")
    result = {"version": version, "dependencies": dependencies, "elaboration": run,
              "scope": "finite real boundary-jet algebra, not the distributional limit"}
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
    phi, n = s.symbols("phi N", real=True)
    tau, z = s.symbols("tau z", positive=True)
    f = -1 / (24 * s.pi**2 * a)
    b = 1 / (4 * s.pi**2 * a**3)
    potential = -6*s.pi**2*a + s.Rational(3, 2)*s.pi**2*a**3 * (
        1-s.exp(-s.sqrt(s.Rational(2, 3))*phi))**2
    checks = []

    def equal(name, actual, expected=0, group="boundary_algebra"):
        residual = s.simplify(s.expand(actual-expected))
        checks.append({"id": name, "group": group, "passed": residual == 0,
                       "residual": str(residual)})

    def h(w):
        return (-f*s.diff(w, a, 2)-s.diff(f, a)*s.diff(w, a)
                -s.diff(f, a, 2)*w/4-b*s.diff(w, phi, 2)+potential*w)

    u, v = s.Function("u")(a, phi, n), s.Function("v")(a, phi, n)
    ja = f*(u*s.diff(v, a)-v*s.diff(u, a))
    jp = b*(u*s.diff(v, phi)-v*s.diff(u, phi))
    equal("Green_current_from_actual_Weyl_operator", h(u)*v-u*h(v),
          s.diff(ja, a)+s.diff(jp, phi), "transpose_and_ghost")

    # A dual of the full four-generator exterior algebra reads an actual Ward component.
    c1, c2, r1, r2 = ({1: 1}, {2: 1}, {4: 1}, {8: 1})
    ghost = wedge(add(c2, c1), add(r2, scale(-1, r1)))
    constraint_dual = wedge(r1, wedge(c1, ghost))
    primary_dual = wedge(r1, wedge(r1, ghost))
    checks.append({"id": "Berezin_dual_reads_constraint_and_kills_primary",
                   "group": "transpose_and_ghost",
                   "passed": constraint_dual == {15: 1} and not primary_dual,
                   "constraint": {str(k): str(v) for k, v in constraint_dual.items()},
                   "primary": {str(k): str(v) for k, v in primary_dual.items()}})
    n1, n2 = s.symbols("N1 N2", real=True)
    dn = s.exp(-(n1-n2)**2/(2*tau))
    equal("primary_diagonal_N_derivative", s.diff(dn, n1)+s.diff(dn, n2),
          group="transpose_and_ghost")

    eta = s.Function("eta")(a)
    psi = s.Function("psi")(phi, n)
    wu, wv = eta*psi, (a-1)*eta*psi
    equal("witness_current_profile", wu*s.diff(wv, a)-wv*s.diff(wu, a), eta**2*psi**2)
    equal("witness_diagonal_bulk_is_face_primitive", h(wu)*wv-wu*h(wv),
          s.diff(f*eta**2, a)*psi**2)
    coefficient = s.simplify(f.subs(a, 2))
    equal("upper_a2_kinetic_coefficient", coefficient, -1/(48*s.pi**2))
    checks.append({"id": "normalized_face_witness_is_strictly_negative",
                   "group": "boundary_algebra", "passed": coefficient.is_negative is True,
                   "value": str(coefficient)})
    uu, du, vv, dv, k, r = s.symbols("u du v dv k r", real=True)
    flux = k*(uu*dv-du*vv)
    equal("orientation_swap_reverses_flux", flux,
          -flux.xreplace({uu: vv, vv: uu, du: dv, dv: du}))
    equal("common_Dirichlet_cancellation", flux.subs({uu: 0, vv: 0}))
    equal("common_real_Robin_cancellation", flux.subs({du: r*uu, dv: r*vv}))
    ru = s.exp(r*(a-2))*eta*psi
    rv = (1+(a-2)**2)*ru
    robin_current = s.simplify(ru*s.diff(rv, a)-rv*s.diff(ru, a))
    equal("distinct_Robin_test_pair_current", robin_current, 2*(a-2)*ru**2)
    equal("distinct_Robin_test_pair_face_zero", robin_current.subs(a, 2))

    moment = s.integrate(2*z*s.exp(-z**2/(2*tau))/s.sqrt(2*s.pi*tau), (z, 0, s.oo))
    equal("Gaussian_absolute_first_moment", moment, s.sqrt(2*tau/s.pi), "limit_bound")
    lengths = [s.Rational(3, 2), s.Integer(3), s.Rational(7, 4)]
    volume = s.prod(lengths)
    face_area_sum = sum(s.prod(lengths[j] for j in range(3) if j != i) for i in range(3))
    equal("box_volume", volume, s.Rational(63, 8), "limit_bound")
    equal("box_overlap_area_sum", face_area_sum, s.Rational(99, 8), "limit_bound")
    l1, l2, l3, d1, d2, d3 = s.symbols("l1 l2 l3 d1 d2 d3", nonnegative=True)
    overlap_loss = l1*l2*l3-(l1-d1)*(l2-d2)*(l3-d3)
    telescoped = d1*l2*l3+(l1-d1)*d2*l3+(l1-d1)*(l2-d2)*d3
    equal("overlap_loss_telescopes", overlap_loss, telescoped, "limit_bound")
    lip, maximum = s.symbols("L M0", nonnegative=True)
    error = (3*volume*lip+face_area_sum*maximum)*moment
    equal("declared_pairing_error_bound_coefficients", error,
          (s.Rational(189, 8)*lip+s.Rational(99, 8)*maximum)*s.sqrt(2*tau/s.pi),
          "limit_bound")
    equal("pairing_error_bound_tends_to_zero", s.limit(error, tau, 0, dir="+"),
          group="limit_bound")
    return {
        "checks": checks,
        "operator": {"f": str(f), "b": str(b), "U": str(potential),
                     "ordering": "Weyl; hbar=1; flat real bilinear distribution pairing"},
        "pairing": {
            "box": {"a": ["1/2", "2"], "phi": ["-1", "2"], "N": ["1/4", "2"]},
            "test_space": "real C_c^infty((0,infinity)xR^2), zero near every box face except a=2",
            "definition": "<(H1-H2)(chi1 chi2 D_tau), u(q1)v(q2)> over the ambient open chart",
            "exact_transpose_form": "integral_BxB D_tau * [(Hu)(q1)v(q2)-u(q1)(Hv)(q2)]",
            "ghost_dual": "left rho1 wedge, then coefficient c1*c2*rho1*rho2 = +1",
            "primary_component": "zero: diagonal N derivative cancels and tests vanish at both N faces",
        },
        "analytic_limit": {
            "proof": str(DERIVATION.relative_to(ROOT)),
            "proof_kind": "analytic derivation with symbolic subidentity and independent reading audits; not Lean distribution formalization",
            "limit": "f(2) integral_(phi,N) [u*d_a(v)-v*d_a(u)]_(a=2)",
            "error_bound": str(error),
            "L": "max over BxB and i of abs(partial_y_i A(x,y))",
            "M0": "max over B of abs(A(q,q))",
            "conditions": "one fixed smooth test pair; coefficients smooth near the compact box; fixed box; tau>0",
            "overlap_inequality": "0<=d_i=min(abs(Z_i),l_i)<=l_i; telescoping loss<=sum_i abs(Z_i) product_(j!=i)l_j",
            "boundary_half_factor": "none in full pairing limit; separate face terms were not independently limited",
            "operator_norm_convergence": "NOT_CLAIMED",
        },
        "witness": {
            "u": "eta(a)*psi(phi,N)", "v": "(a-1)*eta(a)*psi(phi,N)",
            "eta": "S(4a-6)*S(10-4a); S(t)=E(t)/(E(t)+E(1-t)); E(t)=exp(-1/t) for t>0, else 0",
            "psi": "L2-normalized E(1-4phi^2)*E(1-16(N-1)^2)",
            "a2_jets_after_factoring_psi": ["1", "0", "1", "1"],
            "integral_psi_squared": "1", "limit_value": str(coefficient),
            "normalization_scope": "diagnostic test normalization, not a physical Hilbert product",
        },
        "boundary_controls": {
            "Dirichlet": "u_D=(a-2)eta psi, v_D=(a-2)^2 eta psi; both face values zero",
            "Robin": "u_R=exp(r(a-2))eta psi, v_R=(1+(a-2)^2)u_R; same real r, distinct functions",
            "limits": {"interior_test_pair": "0", "common_Dirichlet": "0", "common_real_Robin": "0"},
            "physical_equivalence_of_boundary_choices": "NOT_ASSUMED",
        },
    }


def main() -> int:
    start = time.monotonic()
    result = {
        "schema": "ice-starobinsky-ward-face-limit/v1", "status": "FAILED",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "question": "Does the full Gaussian Ward pairing on declared a=2 tests converge to the Green face functional?",
        "scope": "Supporting fixed-box smooth-test boundary functional",
        "non_claim": "No physical BFV state, self-adjoint realization, full source or original relative cycle.",
        "reproduction_command": "./ice run starobinsky_ward_face_limit",
    }
    try:
        result["provenance"] = provenance()
        result["symbolic"] = derive()
        result["lean"] = lean_audit()
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not result["lean"]["accepted"]:
            raise ValueError("symbolic or Lean control failed; see raw diagnostics")
        result["status"] = "SCOPED_A2_WARD_LIMIT_EQUALS_GREEN_FACE_FUNCTIONAL"
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
    print("a=2 normalized test witness: -1/(48*pi**2); common Dirichlet/real Robin limit: 0")
    print("analytic paired error <= (189*L/8+99*M0/8)*sqrt(2*tau/pi); no physical source or cycle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
