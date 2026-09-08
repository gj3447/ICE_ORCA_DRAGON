"""Check two selected classical relative primary BFV boundary reductions.

Actual graded source brackets and endpoint pullbacks are checked symbolically;
Lean verifies the separate finite linear-generator model. No quantum pushforward,
physical state/product, original integration cycle, or G1 resolution is computed.
Run committed sources: ./ice run starobinsky_relative_primary_boundary.
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

# Pure utility imports only; neither historical main routine is invoked.
from cpt_boundary_sewing_lean import ALLOWED_AXIOMS, audit_axioms, checked, elaborate
from gate1_v0_improved_static_bfv_source import Exterior as E, graded_poisson

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / "formal/cpt_sewing"
INDEX = PROJECT / "relative-primary-boundary-proof-index.json"
DERIVATION = HERE / "STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY_DERIVATION.md"
RESULT = HERE / "STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY_RESULT.json"


def provenance(index: dict) -> dict:
    paths = [Path(__file__), DERIVATION, INDEX,
             *(PROJECT / m["source"] for m in index["modules"]),
             ROOT / "docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md",
             HERE / "STAROBINSKY_POLYNOMIAL_BFV_CHART.md",
             HERE / "STAROBINSKY_PRIMARY_REDUCTION_GRADED_SEWING_RESULT.json",
             HERE / "gate1_v0_improved_static_bfv_source.py",
             HERE / "cpt_boundary_sewing_lean.py", ROOT / "uv.lock",
             PROJECT / "lean-toolchain", PROJECT / "lakefile.toml",
             PROJECT / "lake-manifest.json"]
    records = {}
    for path in paths:
        rel = str(path.relative_to(ROOT))
        data = path.read_bytes()
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT,
                                   capture_output=True, check=True, timeout=10).stdout
        if data != committed:
            raise ValueError(f"uncommitted input: {rel}")
        records[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
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
        raise ValueError("unexpected mathlib revision")
    return {"source_commit": checked(["git", "rev-parse", "HEAD"], cwd=ROOT),
            "inputs": records, "python": platform.python_version(), "sympy": s.__version__,
            "lean_version": version, "dependencies": dependencies}


def restrict(poly, *, even=None, kill=()) -> E:
    """Pull back to a coordinate slice; keep surviving odd generators formal."""
    return E({monomial: coefficient.subs(even or {}, simultaneous=True)
              for monomial, coefficient in E.coerce(poly).terms.items()
              if not any(g in monomial for g in kill)})


def derive() -> dict:
    a = s.Symbol("a", positive=True)
    phi, n, n0, pa, pp, pi, dn = s.symbols("phi N N0 p_a p_phi Pi delta_N", real=True)
    hl = (-pa**2/(24*s.pi**2*a) + pp**2/(4*s.pi**2*a**3) - 6*s.pi**2*a
          + s.Rational(3, 2)*s.pi**2*a**3*(1-s.exp(-s.sqrt(s.Rational(2, 3))*phi))**2)
    c, rho, br, bc = (E.generator(k) for k in ("c_g", "rho", "bar_rho", "bar_c"))
    ep = ((a, pa), (phi, pp), (n, pi))
    op = (("c_g", "bar_rho"), ("rho", "bar_c"))
    omega = c*hl + rho*pi
    reduced = c*hl
    def q(poly): return graded_poisson(omega, E.coerce(poly), ep, op)
    def qr(poly): return graded_poisson(reduced, E.coerce(poly), ep[:2], op[:1])
    def rm(poly): return restrict(poly, even={pi: 0}, kill=("bar_c",))
    def rq(poly): return restrict(poly, even={n: n0}, kill=("rho",))
    checks = []
    def eq(name, actual, expected=0, group="graded_Q_and_projection"):
        residual = E.coerce(actual)-E.coerce(expected)
        checks.append({"id": name, "group": group, "passed": residual.is_zero(),
                       "residual": residual.record()})
    def nonzero(name, actual):
        actual = E.coerce(actual)
        checks.append({"id": name, "group": "isolated_condition_falsifiers",
                       "passed": not actual.is_zero(), "nonzero_expression": actual.record()})
    eq("source_master_equation", q(omega))
    for name, variable, expected in [("N", n, -rho), ("bar_c", bc, pi),
                                      ("Pi", pi, 0), ("rho", rho, 0)]:
        eq(f"source_Q_{name}", q(variable), expected)
    eq("M_Q_Pi_tangent", rm(q(pi)))
    eq("M_Q_bar_c_tangent", rm(q(bc)))
    eq("P_Q_shifted_N_tangent", rq(q(n-n0)))
    eq("P_Q_rho_tangent", rq(q(rho)))
    for name, variable in [("a", a), ("phi", phi), ("p_a", pa),
                           ("p_phi", pp), ("c", c), ("bar_rho", br)]:
        eq(f"projection_Q_{name}_independent_of_primary", q(variable), qr(variable))
    q_reduced = {name: qr(variable).record() for name, variable in
                 [("a", a), ("phi", phi), ("p_a", pa), ("p_phi", pp),
                  ("c", c), ("bar_rho", br)]}
    group = "relative_pullbacks_and_characteristic_quotient"
    eq("M_charge_pullback", rm(omega), reduced, group)
    eq("P_charge_pullback", rq(omega), reduced, group)
    # Coefficients of the primary one-form Pi deltaN + barc delta-rho.
    eq("M_alpha_deltaN_coefficient", rm(pi), group=group)
    eq("M_alpha_delta_rho_coefficient", rm(bc), group=group)
    # On P, both deltaN and delta-rho are zero tangent vectors; no parity
    # identification of delta-rho with an ordinary commuting scalar is made.
    eq("P_alpha_on_allowed_tangents", E.scalar(pi)*0+bc*0, group=group)
    action_residue = bc*rho
    primitive_residue = -bc*dn
    eq("M_source_action_residue", rm(action_residue), group=group)
    eq("M_source_primitive_residue", rm(primitive_residue), group=group)
    eq("P_source_action_residue", rq(action_residue), group=group)
    eq("P_source_primitive_on_allowed_tangents",
       restrict(rq(primitive_residue), even={dn: 0}), group=group)
    for name, constraints in [("M", (E.scalar(pi), bc)), ("P", (E.scalar(n-n0), rho))]:
        for i, left in enumerate(constraints):
            for j, right in enumerate(constraints):
                eq(f"{name}_constraint_bracket_{i}_{j}",
                   graded_poisson(left, right, ep, op), group=group)
    # Block coefficient matrix of delta alpha_primary in (N, Pi | rho, barc).
    # Even skew / odd symmetric blocks are tested separately by this exact
    # coordinate calculation; the graded dimension argument is in the derivation.
    w = s.diag(s.Matrix([[0, -1], [1, 0]]), s.Matrix([[0, 1], [1, 0]]))
    matrix_records = {}
    for name, columns in [("M", (0, 2)), ("P", (1, 3))]:
        tangent = s.eye(4)[:, list(columns)]
        restricted = tangent.T*w*tangent
        annihilator = tangent.T*w
        checks.append({"id": f"{name}_primary_Lagrangian_block", "group": group,
                       "passed": restricted == s.zeros(2) and tangent.rank() == 2
                       and annihilator.rank() == 2 and w.det() != 0,
                       "restricted_matrix": [str(t) for t in restricted],
                       "tangent_rank": tangent.rank(), "annihilator_rank": annihilator.rank()})
        matrix_records[name] = {"coordinate_order": ["N", "Pi", "rho", "bar_c"],
                                "characteristic_primary_coordinates":
                                    ["N", "rho"] if name == "M" else ["Pi", "bar_c"],
                                "full_slice_dimension_even_odd": [5, 3],
                                "reduced_dimension_even_odd": [4, 2],
                                "relation_ambient_dimension_even_odd": [10, 6]}
    nonzero("bar_c_only_is_not_Q_tangent", restrict(q(bc), kill=("bar_c",)))
    eq("bar_c_only_tangency_failure_even_witness",
       restrict(q(bc), even={pi: 1}, kill=("bar_c",)), 1,
       "isolated_condition_falsifiers")
    nonzero("N_fixed_only_is_not_Q_tangent", restrict(q(n-n0), even={n: n0}))
    eq("rho_only_kills_action", restrict(action_residue, kill=("rho",)),
       group="isolated_condition_falsifiers")
    nonzero("rho_only_retains_primitive", restrict(primitive_residue, even={dn: 1}, kill=("rho",)))
    eq("reduction_does_not_impose_matter_constraint", hl.subs({a: 1, phi: 0, pa: 0, pp: 0}),
       -6*s.pi**2, "isolated_condition_falsifiers")
    return {"primary_failure_class": "inference",
            "control_groups": ["graded_Q_and_projection", group, "isolated_condition_falsifiers"],
            "H_L": str(hl), "Q_convention": "QF={Omega,F}; even {q,p}=+1; odd conjugates symmetric +1",
            "reduced_Q_generators": q_reduced, "checks": checks,
            "slices": {"M": "Pi=bar_c=0", "P": "N=N0,rho=0; deltaN=delta-rho=0"},
            "source_relative_terms": {"action": "+[bar_c*rho]", "cotangent_primitive": "-[bar_c*deltaN]",
                                      "identification": "bar_c=-sigma_plus=-e2_plus"},
            "characteristic_quotients": matrix_records,
            "analytic_extension": "Generator identities extend by the derivation property to smooth coefficient superfunctions in the declared local chart; geometric reduction argument is in the derivation.",
            "scope": "Two selected classical coisotropic reductions to the same reduced boundary target. The primary factors, and the graphs in B_ext^- x B_red, are graded Lagrangian; the full slices are not Lagrangian.",
            "noncomputed": "No classification of all polarizations, interval BV gauge-fixing, residual measure, quantum chain map, physical cohomology/product, CPT amplitude or original integration cycle."}


def audit_module(module: dict) -> dict:
    source = (PROJECT / module["source"]).read_text()
    names = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
    if names != module["theorems"] or not names:
        raise ValueError("incomplete theorem index")
    if re.search(r"\b(sorry|admit)\b|^\s*axiom\s", source, re.MULTILINE):
        raise ValueError("proof placeholder or local axiom")
    expected = [module["namespace"]+"."+name for name in names]
    payload = source+"\n"+"\n".join(f"#check {n}\n#print axioms {n}" for n in expected)+"\n"
    with tempfile.TemporaryDirectory(prefix="ice-relative-primary-") as temp:
        run = elaborate(payload, Path(temp), "RelativePrimaryBoundaryAudit")
    record = {"source": module["source"], "scope": module["scope"],
              "expected_theorem_count": len(expected), "elaboration": run, "accepted": False}
    if run["exit_code"] != 0 or run["stderr"].strip() or any(
        m.get("severity") in {"warning", "error"} for m in run["messages"]
    ):
        return record
    records = audit_axioms(run["messages"], expected)
    record.update(theorems=records, theorem_count=len(records),
                  accepted=all(r["accepted"] for r in records.values()))
    return record


def main() -> int:
    started = time.monotonic()
    result = {"schema": "ice-starobinsky-relative-primary-boundary/v1", "status": "FAILED",
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "question": "Do two selected primary slices preserve the actual classical BFV data and both retained source endpoint terms under characteristic reduction?",
              "scope": "SUPPORTING_METHOD: classical relative boundary reduction in the fixed homogeneous source chart",
              "non_claim": "No quantum BV pushforward, positive physical state/product, CPT amplitude or G1 cycle resolution.",
              "reproduction_command": "./ice run starobinsky_relative_primary_boundary",
              "allowed_axioms": sorted(ALLOWED_AXIOMS), "modules": []}
    try:
        index = json.loads(INDEX.read_text())
        result["provenance"] = provenance(index)
        result["symbolic"] = derive()
        for module in index["modules"]:
            if time.monotonic()-started > 65:
                raise TimeoutError("insufficient time for Lean module")
            result["modules"].append(audit_module(module))
        if not all(c["passed"] for c in result["symbolic"]["checks"]) or not all(
            m["accepted"] for m in result["modules"]
        ):
            raise ValueError("symbolic or Lean audit failed; see raw diagnostics")
        result["theorem_count"] = sum(m["theorem_count"] for m in result["modules"])
        result["status"] = "SCOPED_TWO_CLASSICAL_RELATIVE_PRIMARY_REDUCTIONS"
    except Exception as error:
        result["failure"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.monotonic()-started
    payload = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
    if len(payload.encode()) > 200_000:
        raise RuntimeError("unexpectedly large output")
    RESULT.write_text(payload)
    print(result["status"])
    if "symbolic" in result:
        print(f"exact controls: {sum(c['passed'] for c in result['symbolic']['checks'])}/{len(result['symbolic']['checks'])}")
    for module in result["modules"]:
        print(f"{module['source']}: accepted={module['accepted']}; expected={module['expected_theorem_count']}")
    if result["status"] == "FAILED":
        print(result["failure"])
        return 1
    print(f"Lean theorems: {result['theorem_count']}")
    print("Classical selected boundary reductions only; quantum pushforward and original cycle remain open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
