#!/usr/bin/env python3
# Claim B Sealed Loop — Stage S_c1: ZD Nullity Spectrum
# LONGINUS: sourceId=claimB_zd_nullity_spectrum, sourcePath=claimB_zd_nullity_spectrum.py
#
# Protocol: LOOP_PROTOCOL.md
# Prereg: prereg_claimB_loop_20260724.json
#
# Computes simple-ZD pair (e_i + e_j) nullity distribution across CD levels 5,6,7
# and tests for convergence via TV-distance and mode-shape stability.

import numpy as np
import json
import hashlib
import time
from itertools import combinations
from pathlib import Path

def cayley_dickson_mult_table(n):
    """Build multiplication table for 2^n-dimensional Cayley-Dickson algebra.
    Returns (sign, index) arrays such that e_i * e_j = sign[i,j] * e_{index[i,j]}"""
    dim = 2**n
    sign = np.ones((1, 1), dtype=np.int8)
    idx = np.zeros((1, 1), dtype=np.int32)
    for _ in range(n):
        d = sign.shape[0]
        new_sign = np.zeros((2*d, 2*d), dtype=np.int8)
        new_idx = np.zeros((2*d, 2*d), dtype=np.int32)
        for i in range(2*d):
            for j in range(2*d):
                if i < d and j < d:
                    new_sign[i, j] = sign[i, j]
                    new_idx[i, j] = idx[i, j]
                elif i < d and j >= d:
                    jj = j - d
                    new_sign[i, j] = sign[jj, i]
                    new_idx[i, j] = idx[jj, i] + d
                elif i >= d and j < d:
                    ii = i - d
                    if j == 0:
                        new_sign[i, j] = sign[ii, j]
                        new_idx[i, j] = idx[ii, j] + d
                    else:
                        new_sign[i, j] = -sign[ii, j]
                        new_idx[i, j] = idx[ii, j] + d
                else:
                    ii = i - d
                    jj = j - d
                    if jj == 0:
                        new_sign[i, j] = -sign[jj, ii]
                        new_idx[i, j] = idx[jj, ii]
                    else:
                        new_sign[i, j] = sign[jj, ii]
                        new_idx[i, j] = idx[jj, ii]
        sign = new_sign
        idx = new_idx
    return sign, idx

def build_left_mult_matrix(sign, idx, dim, a_vec):
    """Build matrix L_a such that L_a @ x = a * x."""
    L = np.zeros((dim, dim), dtype=np.float64)
    for j in range(dim):
        for i in range(dim):
            if a_vec[i] != 0:
                target = idx[i, j]
                L[target, j] += sign[i, j] * a_vec[i]
    return L

def compute_nullity_distribution(n):
    """Compute nullity distribution for all simple-ZD pairs at level n."""
    dim = 2**n
    sign, idx = cayley_dickson_mult_table(n)
    total_pairs = (dim - 1) * (dim - 2) // 2
    nullity_counts = {}
    nullities = []
    t0 = time.time()
    for i, j in combinations(range(1, dim), 2):
        a_vec = np.zeros(dim, dtype=np.float64)
        a_vec[i] = 1.0
        a_vec[j] = 1.0
        L = build_left_mult_matrix(sign, idx, dim, a_vec)
        s = np.linalg.svd(L, compute_uv=False)
        tol = 1e-10 * s[0] if s[0] > 0 else 1e-10
        nd = int(np.sum(s < tol))
        nullities.append(nd)
        nullity_counts[nd] = nullity_counts.get(nd, 0) + 1
    elapsed = time.time() - t0
    return {
        "n": n,
        "dim": dim,
        "total_pairs": total_pairs,
        "nullity_counts": nullity_counts,
        "nullities_list": nullities,
        "elapsed_sec": elapsed
    }

def normalize_distribution(nullity_counts, total_pairs):
    """p(k) = count(k) / total_pairs"""
    return {k: v / total_pairs for k, v in nullity_counts.items()}

def tv_distance(p, q):
    """Total variation distance with zero-padding to common support."""
    all_keys = set(p.keys()) | set(q.keys())
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in all_keys)

def main():
    script_path = Path(__file__)
    script_bytes = script_path.read_bytes()
    script_sha256 = hashlib.sha256(script_bytes).hexdigest()

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())

    levels = [5, 6, 7]
    results = {}
    distributions = {}

    for n in levels:
        print(f"\n[Level n={n}, dim={2**n}]")
        res = compute_nullity_distribution(n)
        results[n] = res
        distributions[n] = normalize_distribution(res["nullity_counts"], res["total_pairs"])
        print(f"  total_pairs={res['total_pairs']}, elapsed={res['elapsed_sec']:.2f}s")
        print(f"  nullity_counts={res['nullity_counts']}")
        print(f"  distribution={dict(sorted(distributions[n].items()))}")

    # TV distances
    tv_5_6 = tv_distance(distributions[5], distributions[6])
    tv_6_7 = tv_distance(distributions[6], distributions[7])

    # Mode nullity and normalized mode
    mode_5 = max(results[5]["nullity_counts"], key=results[5]["nullity_counts"].get)
    mode_6 = max(results[6]["nullity_counts"], key=results[6]["nullity_counts"].get)
    mode_7 = max(results[7]["nullity_counts"], key=results[7]["nullity_counts"].get)

    norm_mode_5 = mode_5 / (2**5)
    norm_mode_6 = mode_6 / (2**6)
    norm_mode_7 = mode_7 / (2**7)

    rel_change_5_6 = abs(norm_mode_6 - norm_mode_5) / norm_mode_5 if norm_mode_5 > 0 else float('inf')
    rel_change_6_7 = abs(norm_mode_7 - norm_mode_6) / norm_mode_6 if norm_mode_6 > 0 else float('inf')

    print(f"\n[TV distances]")
    print(f"  TV(p_5, p_6) = {tv_5_6:.6f}")
    print(f"  TV(p_6, p_7) = {tv_6_7:.6f}")

    print(f"\n[Mode nullity / dim]")
    print(f"  n=5: mode={mode_5}, norm={norm_mode_5:.6f}")
    print(f"  n=6: mode={mode_6}, norm={norm_mode_6:.6f}")
    print(f"  n=7: mode={mode_7}, norm={norm_mode_7:.6f}")
    print(f"  rel_change(5→6) = {rel_change_5_6:.6f}")
    print(f"  rel_change(6→7) = {rel_change_6_7:.6f}")

    # Verdict per prereg thresholds
    thresholds = {
        "convergence_tv_max": 0.05,
        "progressive_tv_monotone": True,  # TV(p_7,p_6) < TV(p_6,p_5)
        "progressive_mode_rel_change_max": 0.10,
        "kill_tv_increase": True,  # TV(p_7,p_6) >= TV(p_6,p_5)
        "kill_tv_max": 0.05,
        "kill_mode_rel_change_max": 0.20
    }

    # Apply thresholds strictly
    progressive_conditions = [
        tv_5_6 < thresholds["convergence_tv_max"],
        tv_6_7 < tv_5_6,
        max(rel_change_5_6, rel_change_6_7) < thresholds["progressive_mode_rel_change_max"]
    ]
    kill_conditions = [
        tv_6_7 >= tv_5_6,
        tv_6_7 > thresholds["kill_tv_max"],
        max(rel_change_5_6, rel_change_6_7) > thresholds["kill_mode_rel_change_max"]
    ]

    progressive_met = all(progressive_conditions)
    kill_met = any(kill_conditions)

    if progressive_met and not kill_met:
        verdict = "PROGRESSIVE_converging_distribution"
        verdict_reason = "TV below threshold and monotone decreasing; mode shape stable."
    elif kill_met:
        verdict = "KILL_diverging_or_unstable_distribution"
        verdict_reason = (
            f"Kill conditions: TV_6_7 >= TV_5_6={kill_conditions[0]}, "
            f"TV_6_7 > 0.05={kill_conditions[1]}, "
            f"mode_rel_change > 0.20={kill_conditions[2]}. "
            f"At least one kill condition satisfied."
        )
    else:
        # Boundary / ambiguous — per prereg, threshold governs; if not PROGRESSIVE, it's not PROGRESSIVE
        verdict = "KILL_boundary_not_progressive"
        verdict_reason = (
            f"Did not meet all PROGRESSIVE conditions: tv_5_6<0.05={progressive_conditions[0]}, "
            f"tv_6_7<tv_5_6={progressive_conditions[1]}, "
            f"mode_rel_change<0.10={progressive_conditions[2]}. "
            f"Kill conditions: {kill_conditions}."
        )

    print(f"\n[Verdict] {verdict}")
    print(f"[Reason] {verdict_reason}")

    # Reproducibility: run 2 (same process, same code)
    print("\n[Reproducibility check: Run 2]")
    results_r2 = {}
    distributions_r2 = {}
    for n in levels:
        res = compute_nullity_distribution(n)
        results_r2[n] = res
        distributions_r2[n] = normalize_distribution(res["nullity_counts"], res["total_pairs"])

    tv_5_6_r2 = tv_distance(distributions_r2[5], distributions_r2[6])
    tv_6_7_r2 = tv_distance(distributions_r2[6], distributions_r2[7])

    # Check byte-identical metrics (up to float tolerance for SVD numerical noise)
    def metrics_equal(v1, v2, tol=1e-12):
        return abs(v1 - v2) < tol

    byte_identical = (
        metrics_equal(tv_5_6, tv_5_6_r2) and
        metrics_equal(tv_6_7, tv_6_7_r2) and
        results[5]["nullity_counts"] == results_r2[5]["nullity_counts"] and
        results[6]["nullity_counts"] == results_r2[6]["nullity_counts"] and
        results[7]["nullity_counts"] == results_r2[7]["nullity_counts"]
    )

    run2_verdict_conditions = [
        tv_5_6_r2 < thresholds["convergence_tv_max"],
        tv_6_7_r2 < tv_5_6_r2,
    ]
    mode_5_r2 = max(results_r2[5]["nullity_counts"], key=results_r2[5]["nullity_counts"].get)
    mode_6_r2 = max(results_r2[6]["nullity_counts"], key=results_r2[6]["nullity_counts"].get)
    mode_7_r2 = max(results_r2[7]["nullity_counts"], key=results_r2[7]["nullity_counts"].get)
    norm_mode_5_r2 = mode_5_r2 / 32.0
    norm_mode_6_r2 = mode_6_r2 / 64.0
    norm_mode_7_r2 = mode_7_r2 / 128.0
    rel_change_5_6_r2 = abs(norm_mode_6_r2 - norm_mode_5_r2) / norm_mode_5_r2 if norm_mode_5_r2 > 0 else float('inf')
    rel_change_6_7_r2 = abs(norm_mode_7_r2 - norm_mode_6_r2) / norm_mode_6_r2 if norm_mode_6_r2 > 0 else float('inf')
    run2_verdict_conditions.append(max(rel_change_5_6_r2, rel_change_6_7_r2) < thresholds["progressive_mode_rel_change_max"])
    run2_progressive_met = all(run2_verdict_conditions)
    run2_kill_met = any([
        tv_6_7_r2 >= tv_5_6_r2,
        tv_6_7_r2 > thresholds["kill_tv_max"],
        max(rel_change_5_6_r2, rel_change_6_7_r2) > thresholds["kill_mode_rel_change_max"]
    ])

    if run2_progressive_met and not run2_kill_met:
        run2_verdict = "PROGRESSIVE_converging_distribution"
    elif run2_kill_met:
        run2_verdict = "KILL_diverging_or_unstable_distribution"
    else:
        run2_verdict = "KILL_boundary_not_progressive"

    print(f"  Run2 TV(5,6)={tv_5_6_r2:.6f}, TV(6,7)={tv_6_7_r2:.6f}")
    print(f"  Run2 verdict={run2_verdict}")
    print(f"  Byte-identical (counts+TV): {byte_identical}")

    mismatches = []
    if not byte_identical:
        for n in levels:
            if results[n]["nullity_counts"] != results_r2[n]["nullity_counts"]:
                mismatches.append(f"level_{n}_nullity_counts")
        if not metrics_equal(tv_5_6, tv_5_6_r2):
            mismatches.append("tv_5_6")
        if not metrics_equal(tv_6_7, tv_6_7_r2):
            mismatches.append("tv_6_7")

    # Build verdict JSON
    output = {
        "findingId": "C1_zd_nullity_spectrum_2026-07-24",
        "stage": "S_c1",
        "timestamp": timestamp,
        "script_sha256": script_sha256,
        "script_path": str(script_path),
        "protocol": "LOOP_PROTOCOL.md",
        "prereg": "prereg_claimB_loop_20260724.json",
        "levels": levels,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "reproducibility": {
            "run2_verdict": run2_verdict,
            "byte_identical": byte_identical,
            "mismatches": mismatches
        },
        "layer_disclosure": {
            "L1_algebra": "Cayley-Dickson simple-ZD pair nullity distribution",
            "L2_L3_physics": "NO physics prediction claimed. Avenue3 barrier intact.",
            "mythology": "USER_PRIMARY ICE_ORCA_DRAGON canon #2"
        },
        "avenue3_caveat": (
            "Even if PROGRESSIVE: CD doubling forces discrete integers {2,3,7,14} only. "
            "No continuous observable emergence mechanism connects any algebraic invariant "
            "to gravitational observables. This caveat is MANDATORY per ICE_WORKBENCH_REFRAME_2026-05-18 §3."
        ),
        "metrics_per_level": {},
        "tv_distances": {
            "5_to_6": {"tv": tv_5_6},
            "6_to_7": {"tv": tv_6_7}
        },
        "mode_analysis": {
            "mode_nullity": {"5": mode_5, "6": mode_6, "7": mode_7},
            "norm_mode_by_dim": {"5": norm_mode_5, "6": norm_mode_6, "7": norm_mode_7},
            "rel_change_5_to_6": rel_change_5_6,
            "rel_change_6_to_7": rel_change_6_7
        },
        "thresholds_applied": thresholds
    }

    for n in levels:
        output["metrics_per_level"][str(n)] = {
            "n": n,
            "dim": 2**n,
            "total_pairs": results[n]["total_pairs"],
            "nullity_counts": results[n]["nullity_counts"],
            "nullity_distribution": dict(sorted(distributions[n].items())),
            "elapsed_sec": results[n]["elapsed_sec"]
        }

    output_path = script_path.parent / "results_c1_zd_nullity_spectrum.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[Saved] {output_path}")

if __name__ == "__main__":
    main()
