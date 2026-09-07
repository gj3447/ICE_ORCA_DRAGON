"""Discriminate local Ward cancellation from an invariant BFV test-space ansatz.

Output: complex Robin, primary-lapse and Hamiltonian boundary-jet obstructions.
No self-adjoint-extension no-go, anomaly, physical CPT lift or original cycle.
Run only clean committed sources with ./ice run starobinsky_ward_domain.
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
RESULT = HERE / "STAROBINSKY_WARD_DOMAIN_RESULT.json"
DERIVATION = HERE / "STAROBINSKY_WARD_DOMAIN_DERIVATION.md"
PINS = {
    "cpt_boundary_sewing_lean.py": "7013ffe5f6c334ea24731aa364d6ae51f3be9960639f78c655abae7e5e4f3fdb",
    "STAROBINSKY_WARD_FACE_LIMIT_RESULT.json": "e4d922b054ee5d8ad448fef856f82dc0239d3ca405ee3430f4eb8f47e0976a92",
    "STAROBINSKY_WARD_FACE_LIMIT_DERIVATION.md": "5c09c5bfb9677cf02cec53a1657b3dda998097c88b733b4f4b30920ba211cd64",
}
for name, expected in PINS.items():
    if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
        raise RuntimeError(f"changed convention or audit dependency: {name}")

from cpt_boundary_sewing_lean import audit_axioms, checked, elaborate


def provenance() -> dict:
    paths = [
        Path(__file__), DERIVATION, *(HERE / name for name in PINS),
        PROJECT / "CptSewing/WardDomain.lean", PROJECT / "ward-domain-proof-index.json",
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
    prior = json.loads((HERE / "STAROBINSKY_WARD_FACE_LIMIT_RESULT.json").read_text())
    if prior["status"] != "SCOPED_A2_WARD_LIMIT_EQUALS_GREEN_FACE_FUNCTIONAL":
        raise ValueError("unexpected weak-limit predecessor")
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
    index = json.loads((PROJECT / "ward-domain-proof-index.json").read_text())
    source = (PROJECT / index["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != index["theorems"]:
        raise ValueError("incomplete Lean theorem index")
    expected = [index["namespace"] + "." + name for name in names]
    payload = source + "\n" + "\n".join(f"#check {n}\n#print axioms {n}" for n in expected) + "\n"
    with tempfile.TemporaryDirectory(prefix="ice-ward-domain-") as temp:
        run = elaborate(payload, Path(temp), "WardDomainAudit")
    result = {"version": version, "dependencies": dependencies, "elaboration": run,
              "scope": "finite complex Green and real normal-jet algebra; not an operator-domain theorem"}
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
    f = -1/(24*s.pi**2*a)
    b = 1/(4*s.pi**2*a**3)
    potential = -6*s.pi**2*a + s.Rational(3, 2)*s.pi**2*a**3 * (
        1-s.exp(-s.sqrt(s.Rational(2, 3))*phi))**2
    w = potential-s.diff(f, a, 2)/4
    r = s.Function("r")(phi, n)
    u = s.Function("u")(a, phi, n)
    psi = s.Function("psi")(phi, n)
    checks = []

    def equal(name, actual, expected=0, group="normal_jet_obstruction"):
        residual = s.simplify(s.expand(actual-expected))
        checks.append({"id": name, "group": group, "passed": residual == 0,
                       "residual": str(residual)})

    def h(v):
        return -s.diff(f*s.diff(v, a), a)-b*s.diff(v, phi, 2)+w*v

    def pn(v):
        return -s.I*s.diff(v, n)

    def boundary(v):
        return s.diff(v, a)-r*v

    z, v, rc = s.symbols("z v r_complex", complex=True)
    rr, ri, k = s.symbols("r_real r_imag k", real=True)
    flux = k*(s.conjugate(z)*rc*v-s.conjugate(rc*z)*v)
    expected = k*(rc-s.conjugate(rc))*s.conjugate(z)*v
    equal("complex_Robin_flux_formula", flux, expected, "complex_and_primary")
    equal("imaginary_Robin_flux_coefficient", flux.subs(rc, rr+s.I*ri),
          2*s.I*k*ri*s.conjugate(z)*v, "complex_and_primary")
    equal("real_Robin_sesquilinear_cancellation", flux.subs(rc, rr),
          group="complex_and_primary")
    equal("imaginary_Robin_unit_trace_counterexample", flux.subs({rc: s.I, z: 1, v: 1}),
          2*s.I*k, "complex_and_primary")
    equal("conjugation_maps_Robin_to_conjugate_Robin", s.conjugate(rc*z),
          s.conjugate(rc)*s.conjugate(z), "complex_and_primary")
    equal("primary_boundary_product_rule", boundary(pn(u))-pn(boundary(u)),
          -s.I*s.diff(r, n)*u, "complex_and_primary")
    equal("formal_H_primary_commutator", h(pn(u))-pn(h(u)), group="complex_and_primary")
    # These germs are extended by eta=1 near a=2 and compact transverse psi.
    lapse_witness = s.exp(n*(a-2))*psi
    equal("lapse_dependent_real_Robin_input", (s.diff(lapse_witness, a)-n*lapse_witness).subs(a, 2),
          group="complex_and_primary")
    equal("lapse_dependent_real_Robin_primary_failure",
          (s.diff(pn(lapse_witness), a)-n*pn(lapse_witness)).subs(a, 2),
          -s.I*psi, "complex_and_primary")

    # This is substitution of boundary identities only, not a bulk PDE assumption.
    robin_subs = {
        s.diff(u, a): r*u,
        s.diff(u, a, phi, 2): s.diff(r, phi, 2)*u+2*s.diff(r, phi)*s.diff(u, phi)+r*s.diff(u, phi, 2),
    }
    actual = s.expand(boundary(h(u))).xreplace(robin_subs)
    expected_jet = (-f*s.diff(u, a, 3)+(r*f-2*s.diff(f, a))*s.diff(u, a, 2)
                    -s.diff(b, a)*s.diff(u, phi, 2)-2*b*s.diff(r, phi)*s.diff(u, phi)
                    +(s.diff(w, a)-r*s.diff(f, a, 2)+r**2*s.diff(f, a)
                      -b*s.diff(r, phi, 2))*u)
    equal("full_actual_Weyl_Robin_jet_formula", actual, expected_jet)
    cubic = (a-2)**3*psi
    quadratic = (a-2)**2*psi
    equal("cubic_witness_satisfies_every_Robin_condition", boundary(cubic).subs(a, 2))
    equal("cubic_H_value_zero", h(cubic).subs(a, 2))
    cubic_residual = s.simplify(boundary(h(cubic)).subs(a, 2))
    equal("cubic_H_Robin_obstruction", cubic_residual, psi/(8*s.pi**2))
    equal("quadratic_witness_satisfies_Dirichlet", quadratic.subs(a, 2))
    equal("quadratic_H_Dirichlet_obstruction", h(quadratic).subs(a, 2), psi/(24*s.pi**2))
    equal("cubic_face_coeff_from_independent_jet_formula", -6*f.subs(a, 2), 1/(8*s.pi**2))
    coefficient = s.simplify(cubic_residual/psi)
    checks.append({"id": "cubic_obstruction_coefficient_positive", "group": "normal_jet_obstruction",
                   "passed": coefficient.is_positive is True, "value": str(coefficient)})
    return {
        "checks": checks,
        "operator": {"f": str(f), "b": str(b), "W": str(w), "p_N": "-i partial_N",
                     "ordering_density": "Weyl, hbar=1, flat complex auxiliary pairing"},
        "ansatz": "D_r^sm tensor exterior(c,rho), same first-order boundary test space in every ghost coefficient",
        "boundary": "B_r u=(partial_a-r(phi,N))u at a=2; compact support away from every other box face",
        "classification": {
            "all_trace_sesquilinear_zero": "iff r=conjugate(r)",
            "kinematic_conjugation_invariant": "real r; does not select its value or give full CPT",
            "all_trace_primary_preserved": "iff partial_N r=0",
            "same_space_H_preserved": False,
            "same_space_Dirichlet_H_preserved": False,
        },
        "formulas": {
            "primary_residual": "-i (partial_N r) u|_2",
            "full_Robin_H_jet": str(expected_jet),
            "cubic_Robin_residual": str(cubic_residual),
            "quadratic_Dirichlet_residual": str(s.simplify(h(quadratic).subs(a, 2))),
        },
        "analytic_proof": str(DERIVATION.relative_to(ROOT)),
        "proof_boundaries": "local germs have smooth compact extensions; functional interpretation is analytic, not Lean",
        "repair_scope": "all B_r H^k p_N^m traces zero is algebraically invariant and contains interior tests; no selected graph core or physical states established",
    }


def main() -> int:
    start = time.monotonic()
    result = {
        "schema": "ice-starobinsky-ward-domain/v1", "status": "FAILED",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "question": "Does local a=2 Ward cancellation define the same invariant smooth test space in every BFV ghost coefficient?",
        "scope": "Supporting complex local boundary test-space ansatz with fixed Weyl operator",
        "non_claim": "No self-adjoint-extension no-go, physical BRST anomaly, CPT lift, selected physical state or original cycle.",
        "reproduction_command": "./ice run starobinsky_ward_domain",
    }
    try:
        result["provenance"] = provenance()
        result["symbolic"] = derive()
        result["lean"] = lean_audit()
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not result["lean"]["accepted"]:
            raise ValueError("symbolic or Lean control failed; see raw diagnostics")
        result["status"] = "SCOPED_LOCAL_WARD_CANCELLATION_DOES_NOT_DEFINE_INVARIANT_BFV_TEST_SPACE"
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
    print("Robin flux: real r; primary preservation: partial_N r=0")
    print("cubic H boundary residual: psi/(8*pi**2); Dirichlet H trace: psi/(24*pi**2)")
    print("same-space BFV ansatz fails; no self-adjointness no-go or physical CPT conclusion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
