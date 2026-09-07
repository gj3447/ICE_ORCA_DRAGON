"""Audit conditional BFV carrier, constrained dual and positive quotient Lean proofs.

One output: kernel-checked algebraic implications with explicit analytic hypotheses.
No PDE existence proof, selected physical inner product, full CPT sewing or G1 claim.
Run committed sources only: ./ice run starobinsky_bfv_dual_structure_lean.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / "formal/cpt_sewing"
INDEX = PROJECT / "bfv-dual-structure-proof-index.json"
RESULT = HERE / "STAROBINSKY_BFV_DUAL_STRUCTURE_LEAN_RESULT.json"
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
    files = [Path(__file__), INDEX, *(PROJECT / m["source"] for m in index["modules"]),
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
            "inputs":records, "python":platform.python_version(),
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
    with tempfile.TemporaryDirectory(prefix="ice-bfv-dual-structure-") as temp:
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


def main() -> int:
    started = time.monotonic()
    result = {
        "schema":"ice-bfv-dual-structure-lean/v1", "status":"FAILED",
        "started_at_utc":datetime.now(timezone.utc).isoformat(),
        "question":"Which carrier, constrained-dual and positive-quotient consequences follow in Lean from explicit algebraic and analytic hypotheses?",
        "scope":"SUPPORTING_METHOD: abstract algebraic formalization of the existing fixed-Neumann analysis",
        "non_claim":"No Lean PDE existence/Green integral proof, physical inner-product selection, full BFV/CPT lift or original cycle.",
        "reproduction_command":"./ice run starobinsky_bfv_dual_structure_lean",
        "allowed_axioms":sorted(ALLOWED_AXIOMS),
        "analytic_inputs_not_formalized":[
            "Actual Weyl differential realization and commutation on the smooth carrier",
            "Cauchy existence, uniqueness, propagation, seed injectivity and interior nonzero witness",
            "Green cancellation for the selected bulk state and actual boundary tests",
            "Full-R_phi KG current conservation/degeneracy and N-collar primary injectivity",
            "Actual conjugation covariance and seed separator witnesses",
        ],
        "modules":[],
    }
    try:
        index = json.loads(INDEX.read_text())
        result["provenance"] = provenance(index)
        for module in index["modules"]:
            if time.monotonic()-started > 65:
                raise TimeoutError("insufficient bounded time for another Lean module")
            result["modules"].append(audit_module(module))
        if not all(m["accepted"] for m in result["modules"]):
            raise ValueError("Lean elaboration or axiom control failed; see every module diagnostic")
        result["theorem_count"] = sum(m["theorem_count"] for m in result["modules"])
        result["status"] = "SCOPED_LEAN_BFV_DUAL_STRUCTURE_WITH_EXPLICIT_ANALYTIC_HYPOTHESES"
    except Exception as error:
        result["failure"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.monotonic()-started
    payload = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
    if len(payload.encode()) > 200_000:
        raise RuntimeError("unexpectedly large proof audit")
    RESULT.write_text(payload)
    print(result["status"])
    for module in result["modules"]:
        print(f"{module['source']}: accepted={module['accepted']}; expected theorems={module['expected_theorem_count']}")
    if result["status"] == "FAILED":
        print(result["failure"])
        return 1
    print(f"Lean theorems: {result['theorem_count']}; analytic hypotheses remain explicit inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
