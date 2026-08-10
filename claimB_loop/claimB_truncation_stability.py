#!/usr/bin/env python3
"""
Claim B — C3 Truncation Stability (S_c3)
Protocol: LOOP_PROTOCOL.md
Prereg:   prereg_claimB_loop_20260724.json

Computes prediction-family P_n = {mean_r_n, mode_nullity_n, zd_density_n}
from prior C1/C2 outputs and applies the pre-registered Cauchy-convergence
criteria (absolute 0.10, relative 0.20, component-wise decreasing).

Absolute rules:
- No post-hoc fitting.
- 3-layer disclosure enforced in JSON.
- Avenue3 caveat mandatory.
"""

import json
import hashlib
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = Path(__file__).parent.resolve()
C2_PATH = HERE / "results_c2_associator_distribution.json"
C1_PATH = HERE / "results_c1_zd_nullity_spectrum.json"
OUT_PATH = HERE / "results_c3_truncation_stability.json"
PREREG_PATH = HERE / "prereg_claimB_loop_20260724.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_mode_nullity(metrics_per_level: dict, level: int) -> int:
    """Most frequent nullity value for a given level."""
    dist = metrics_per_level[str(level)]["nullity_distribution"]
    # nullity_distribution keys are strings like "0", "4", ...
    return int(max(dist, key=dist.get))


def compute_zd_density(metrics_per_level: dict, level: int) -> float:
    """ZD density = count of pairs with nullity > 0 / total_pairs."""
    m = metrics_per_level[str(level)]
    total = m["total_pairs"]
    nullity_counts = m["nullity_counts"]
    zd_count = sum(c for k, c in nullity_counts.items() if int(k) > 0)
    return zd_count / total


def compute_mean_r(metrics_per_level: dict, level: int) -> float:
    return metrics_per_level[str(level)]["mean_r"]


def apply_verdict(p5, p6, p7, abs_tol=0.10, rel_tol=0.20):
    """
    Returns (verdict, verdict_reason, details)
    p5, p6, p7 are dicts with the three components.
    """
    components = ["mean_r", "mode_nullity", "zd_density"]
    diffs_56 = {k: p6[k] - p5[k] for k in components}
    diffs_67 = {k: p7[k] - p6[k] for k in components}

    # Cauchy decreasing: |P7-P6| < |P6-P5| for ALL components
    cauchy_ok = all(abs(diffs_67[k]) < abs(diffs_56[k]) for k in components)

    # Absolute tolerance
    abs_ok = all(abs(diffs_67[k]) < abs_tol for k in components)

    # Relative tolerance (guard against division by zero)
    rel_ok = True
    rel_details = {}
    for k in components:
        denom = abs(p6[k])
        if denom < 1e-12:
            rel_ok = False
            rel_details[k] = {"relative_change": None, "guard_triggered": True}
        else:
            rc = abs(diffs_67[k]) / denom
            rel_details[k] = {"relative_change": rc, "guard_triggered": False}
            if rc >= rel_tol:
                rel_ok = False

    # INSUFFICIENT check (already verified files exist, but keep for protocol)
    has_nan = any(
        (v != v) or (v is None)
        for k in components
        for v in (p5[k], p6[k], p7[k])
    )
    if has_nan:
        return (
            "INSUFFICIENT_LEVELS",
            "NaN or undefined component detected.",
            {"cauchy_ok": False, "abs_ok": False, "rel_ok": False, "has_nan": True},
        )

    if cauchy_ok and abs_ok and rel_ok:
        verdict = "CONVERGED"
        reason = "Cauchy-decreasing AND absolute<0.10 AND relative<0.20 for all components."
    elif (not cauchy_ok) or (not abs_ok) or (not rel_ok):
        verdict = "DRIFTING"
        parts = []
        if not cauchy_ok:
            parts.append("NOT cauchy-decreasing")
        if not abs_ok:
            parts.append("absolute>=0.10")
        if not rel_ok:
            parts.append("relative>=0.20")
        reason = "DRIFTING: " + "; ".join(parts) + "."
    else:
        # Defensive fallback (should not reach here)
        verdict = "DRIFTING"
        reason = "Fallback: structural condition failure."

    details = {
        "cauchy_ok": cauchy_ok,
        "abs_ok": abs_ok,
        "rel_ok": rel_ok,
        "diffs_5_to_6": diffs_56,
        "diffs_6_to_7": diffs_67,
        "abs_6_to_7": {k: abs(diffs_67[k]) for k in components},
        "rel_details": rel_details,
    }
    return verdict, reason, details


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # --- Load prior results ---
    if not C2_PATH.exists():
        print(f"ERROR: C2 result missing: {C2_PATH}", file=sys.stderr)
        sys.exit(1)
    if not C1_PATH.exists():
        print(f"ERROR: C1 result missing: {C1_PATH}", file=sys.stderr)
        sys.exit(1)

    c2 = load_json(C2_PATH)
    c1 = load_json(C1_PATH)

    # --- Build P_n ---
    levels = [5, 6, 7]
    P = {}
    for n in levels:
        P[n] = {
            "mean_r": compute_mean_r(c2["metrics_per_level"], n),
            "mode_nullity": compute_mode_nullity(c1["metrics_per_level"], n),
            "zd_density": compute_zd_density(c1["metrics_per_level"], n),
        }

    # --- Apply pre-registered thresholds ---
    verdict, reason, details = apply_verdict(P[5], P[6], P[7])

    # --- Self-sha256 ---
    script_sha256 = sha256_file(Path(__file__))

    # --- Assemble output ---
    output = {
        "findingId": "C3_truncation_stability_2026-07-24",
        "stage": "S_c3",
        "timestamp": None,  # filled at write time
        "script_sha256": script_sha256,
        "script_path": str(Path(__file__).resolve()),
        "protocol": "LOOP_PROTOCOL.md",
        "prereg": "prereg_claimB_loop_20260724.json",
        "levels": levels,
        "prediction_family": {
            "components": ["mean_r", "mode_nullity", "zd_density"],
            "P_5": P[5],
            "P_6": P[6],
            "P_7": P[7],
        },
        "thresholds_applied": {
            "cauchy_decreasing": "|P_7 - P_6| < |P_6 - P_5| for all components",
            "absolute_tolerance": 0.10,
            "relative_tolerance": 0.20,
        },
        "verdict": verdict,
        "verdict_reason": reason,
        "verdict_details": details,
        "layer_disclosure": {
            "L1_algebra": "Cayley-Dickson prediction-family P_n = {mean_r, mode_nullity, zd_density}",
            "L2_L3_physics": "NO physics prediction claimed. Avenue3 barrier intact.",
            "mythology": "USER_PRIMARY ICE_ORCA_DRAGON canon #2",
        },
        "avenue3_caveat": (
            "Even if PROGRESSIVE: CD doubling forces discrete integers {2,3,7,14} only. "
            "No continuous observable emergence mechanism connects any algebraic invariant to gravitational observables. "
            "This caveat is MANDATORY per ICE_WORKBENCH_REFRAME_2026-05-18 §3."
        ),
    }

    # --- Write ---
    from datetime import datetime, timezone
    output["timestamp"] = datetime.now(timezone.utc).isoformat()

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"S_c3 complete. Verdict: {verdict}")
    print(f"Output written to: {OUT_PATH}")


if __name__ == "__main__":
    main()
