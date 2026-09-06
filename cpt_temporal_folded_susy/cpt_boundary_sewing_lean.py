"""Re-elaborate the pinned Lean boundary proofs and audit every theorem's axioms."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "formal/cpt_sewing"
RESULT = Path(__file__).with_name("CPT_BOUNDARY_SEWING_LEAN_RESULT.json")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
TOOLCHAIN = "leanprover/lean4:v4.33.0"
MATHLIB_REV = "db584cd6d46c92f209a44c0f1c829460d327499d"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture(args: list[str], *, cwd: Path = PROJECT, timeout: int = 20) -> dict:
    completed = subprocess.run(
        args, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False
    )
    return {
        "command": args,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def checked(args: list[str], *, cwd: Path = PROJECT) -> str:
    run = capture(args, cwd=cwd)
    if run["exit_code"] != 0:
        raise RuntimeError(f"command failed: {args}: {run['stderr']}")
    return run["stdout"].strip()


def lean_messages(run: dict) -> list[dict]:
    return [json.loads(line) for line in run["stdout"].splitlines() if line.strip()]


def audit_axioms(messages: list[dict], expected: list[str]) -> dict:
    records: dict[str, dict] = {}
    for message in messages:
        data = message.get("data", "")
        match = re.fullmatch(
            r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
            data.strip(),
        )
        if not match:
            continue
        name = match[1]
        if name in records:
            raise ValueError(f"duplicate axiom report for {name}")
        axioms = [a.strip() for a in (match[2] or "").split(",") if a.strip()]
        records[name] = {
            "axioms": axioms,
            "accepted": set(axioms) <= ALLOWED_AXIOMS,
        }
    if set(records) != set(expected):
        raise ValueError(f"axiom report mismatch: expected {expected}, got {list(records)}")
    return records


def elaborate(payload: str, directory: Path, name: str) -> dict:
    path = directory / f"{name}.lean"
    path.write_text(payload, encoding="utf-8")
    run = capture(
        ["lake", "env", "lean", "--json", "-DwarningAsError=true", str(path)],
        timeout=45,
    )
    # Keep the rerunnable command shape without relying on the temporary pathname.
    run["command"][-1] = f"<temporary>/{name}.lean"
    run["payload_sha256"] = digest(payload.encode())
    run["messages"] = lean_messages(run)
    del run["stdout"]
    return run


def main() -> int:
    started = time.monotonic()
    result: dict = {
        "schema": "ice-lean-boundary-sewing-result/v1",
        "question": "Does the declared real bosonic reflection cancel the sum boundary primitive?",
        "status": "FAILED",
        "scope": "real coordinate boundary algebra; fixed Starobinsky Hamiltonian convention",
        "non_claim": "No full BFV/CPT lift, boundary state, original relative cycle or physical discovery.",
        "reproduction_command": "./ice run cpt_boundary_sewing_lean",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
    }
    try:
        files = [
            Path(__file__).resolve(),
            PROJECT / "lean-toolchain",
            PROJECT / "lakefile.toml",
            PROJECT / "lake-manifest.json",
            PROJECT / "CptSewing.lean",
            PROJECT / "CptSewing/Boundary.lean",
            PROJECT / "proof-index.json",
        ]
        result["source_commit"] = checked(["git", "rev-parse", "HEAD"], cwd=ROOT)
        provenance = {}
        for path in files:
            relpath = str(path.relative_to(ROOT))
            current = path.read_bytes()
            committed = subprocess.run(
                ["git", "show", f"HEAD:{relpath}"], cwd=ROOT,
                capture_output=True, timeout=10, check=True,
            ).stdout
            if current != committed:
                raise ValueError(f"proof input differs from its committed source: {relpath}")
            provenance[relpath] = {"sha256": digest(current), "bytes": len(current)}
        result["inputs"] = provenance
        if (PROJECT / "lean-toolchain").read_text().strip() != TOOLCHAIN:
            raise ValueError("unexpected Lean toolchain")
        version = checked(["lake", "env", "lean", "--version"])
        if not version.startswith("Lean (version 4.33.0,"):
            raise ValueError(f"wrong Lean compiler: {version}")
        result["lean_version"] = version
        manifest = json.loads((PROJECT / "lake-manifest.json").read_text())
        dependencies = []
        for package in manifest["packages"]:
            location = PROJECT / manifest["packagesDir"] / package["name"]
            revision = checked(["git", "rev-parse", "HEAD"], cwd=location)
            if revision != package["rev"]:
                raise ValueError(f"dependency revision mismatch: {package['name']}")
            if checked(["git", "status", "--porcelain", "--untracked-files=no"], cwd=location):
                raise ValueError(f"modified dependency: {package['name']}")
            dependencies.append({"name": package["name"], "url": package["url"], "rev": revision})
        if not any(p["name"] == "mathlib" and p["rev"] == MATHLIB_REV for p in dependencies):
            raise ValueError("pinned mathlib missing")
        result["dependencies"] = dependencies

        index = json.loads((PROJECT / "proof-index.json").read_text())
        source = (PROJECT / index["source"]).read_text()
        # This deliberately simple project uses one namespace and ordinary theorem declarations.
        declared = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, flags=re.MULTILINE)
        if declared != index["theorems"]:
            raise ValueError("the proof index must list every theorem, in source order")
        expected = [f"{index['namespace']}.{name}" for name in declared]
        audit = "\n".join(f"#check {name}\n#print axioms {name}" for name in expected)
        payload = source + "\n" + audit + "\n"
        with tempfile.TemporaryDirectory(prefix="ice-cpt-lean-") as directory:
            scratch = Path(directory)
            run = elaborate(payload, scratch, "BoundaryAudit")
            result["elaboration"] = run
            records = audit_axioms(run["messages"], expected)
            result["theorems"] = records
            compilation_ok = (
                run["exit_code"] == 0
                and not run["stderr"].strip()
                and not any(m.get("severity") in {"warning", "error"} for m in run["messages"])
                and all(record["accepted"] for record in records.values())
            )
            if not compilation_ok:
                raise ValueError("Lean compilation or transitive axiom audit failed")

            # Independent acceptance controls: compilation alone accepts a custom axiom;
            # an admitted proof must fail under warningAsError. Neither is a project theorem.
            custom_payload = (
                "axiom controlAssumption : False\n"
                "theorem controlTheorem : False := controlAssumption\n"
                "#print axioms controlTheorem\n"
            )
            custom = elaborate(custom_payload, scratch, "CustomAxiomControl")
            custom_records = audit_axioms(custom["messages"], ["controlTheorem"])
            admitted = elaborate(
                "theorem controlAdmitted : False := by sorry\n"
                "#print axioms controlAdmitted\n", scratch, "AdmissionControl"
            )
            controls = {
                "custom_axiom_rejected": custom["exit_code"] == 0
                and not custom_records["controlTheorem"]["accepted"],
                "admitted_proof_rejected": admitted["exit_code"] != 0
                and any(m.get("severity") == "error" for m in admitted["messages"]),
            }
            result["acceptance_controls"] = controls
            result["control_diagnostics"] = {"custom_axiom": custom, "admission": admitted}
            if not all(controls.values()):
                raise ValueError("negative acceptance control failed")
        result["status"] = "LEAN_KERNEL_ACCEPTED_SCOPED_REAL_BOUNDARY_SEWING"
        result["theorem_count"] = len(expected)
    except Exception as error:
        result["failure"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.monotonic() - started
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(result["status"])
    if result["status"] == "FAILED":
        print(result["failure"])
        return 1
    print(f"kernel-checked theorems: {result['theorem_count']}")
    print("transitive axiom audit: standard axioms only")
    print("acceptance controls: custom axiom and admitted proof rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
