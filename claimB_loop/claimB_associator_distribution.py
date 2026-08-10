#!/usr/bin/env python3
"""
Claim B Sealed Loop — Stage S_c2: Associator Distribution Measurement
Protocol: LOOP_PROTOCOL.md
Prereg: prereg_claimB_loop_20260724.json

Measures: random unit-vector triple associator ratio
  r(x,y,z) = ||[x,y,z]|| / (||x|| ||y|| ||z||)
  where [x,y,z] = (xy)z - x(yz)

Levels: 4,5,6,7  (dim 16,32,64,128)
Sample size: M=10000 per level, seed=42

Verdict rules (pre-registered):
  PROGRESSIVE: mean_r >= 0.01 AND |mean_r(n+1)-mean_r(n)|/mean_r(n) < 0.05
                for all consecutive n, AND KS(n,n+1) < 0.05 for all consecutive
  KILL-A_growth: mean_r(n+1) > mean_r(n)*1.20 for 2+ consecutive levels
  KILL-B_collapse: mean_r(n+1) < mean_r(n)*0.50 for 2+ consecutive levels
                   OR mean_r(n) < 1e-6 for any n >= 6
  KILL-C_reconfiguration: mean_r stable (all <5% change) BUT KS(n,n+1) > 0.05
                          for 2+ consecutive levels

Anti-numerology guard: thresholds fixed BEFORE computation (S_setup).
3-layer disclosure: L1 algebra only; no physics prediction claims.
Avenue3 caveat: even PROGRESSIVE does NOT imply gravitational observable.
"""

import numpy as np
import json
import hashlib
import os
import sys
from datetime import datetime, timezone
from scipy import stats

# =============================================================================
# 1. Cayley-Dickson multiplication (vectorized, recursive)
# =============================================================================

def cd_conj_vec(X):
    """Conjugate: negate all components except index 0. X shape (M, dim)."""
    c = -X.copy()
    c[:, 0] = X[:, 0]
    return c

def cd_multiply_batch(A, B, n):
    """
    Batch CD multiplication.
    A, B: arrays of shape (M, 2**n)
    Returns: array of shape (M, 2**n)
    """
    dim = 2 ** n
    assert A.shape[1] == dim and B.shape[1] == dim
    if n == 0:
        return A * B
    half = dim // 2
    A1, A2 = A[:, :half], A[:, half:]
    B1, B2 = B[:, :half], B[:, half:]
    B2_conj = cd_conj_vec(B2)
    B1_conj = cd_conj_vec(B1)
    part1 = cd_multiply_batch(A1, B1, n - 1) - cd_multiply_batch(B2_conj, A2, n - 1)
    part2 = cd_multiply_batch(B2, A1, n - 1) + cd_multiply_batch(A2, B1_conj, n - 1)
    return np.concatenate([part1, part2], axis=1)

def cd_norm(X):
    """Euclidean norm along last axis."""
    return np.linalg.norm(X, axis=1)

# =============================================================================
# 2. Associator and defect computations
# =============================================================================

def compute_associator(X, Y, Z, n):
    """
    Compute [X,Y,Z] = (XY)Z - X(YZ) for batches of shape (M, dim).
    """
    XY = cd_multiply_batch(X, Y, n)
    YZ = cd_multiply_batch(Y, Z, n)
    XYZ1 = cd_multiply_batch(XY, Z, n)
    XYZ2 = cd_multiply_batch(X, YZ, n)
    return XYZ1 - XYZ2

def compute_flexibility_defect(X, Y, n):
    """||(XY)X - X(YX)||"""
    XY = cd_multiply_batch(X, Y, n)
    YX = cd_multiply_batch(Y, X, n)
    XY_X = cd_multiply_batch(XY, X, n)
    X_YX = cd_multiply_batch(X, YX, n)
    return cd_norm(XY_X - X_YX)

def compute_power_assoc_defect(X, n):
    """||(XX)X - X(XX)||"""
    XX = cd_multiply_batch(X, X, n)
    XX_X = cd_multiply_batch(XX, X, n)
    X_XX = cd_multiply_batch(X, XX, n)
    return cd_norm(XX_X - X_XX)

# =============================================================================
# 3. Main measurement routine
# =============================================================================

def measure_level(n, M, seed, verbose=True):
    """
    Measure associator distribution at level n (dim = 2^n).
    Returns dict of metrics.
    """
    dim = 2 ** n
    rng = np.random.default_rng(seed)

    # Generate M random unit vectors (normalized Gaussian)
    X = rng.standard_normal((M, dim))
    X = X / cd_norm(X)[:, None]
    Y = rng.standard_normal((M, dim))
    Y = Y / cd_norm(Y)[:, None]
    Z = rng.standard_normal((M, dim))
    Z = Z / cd_norm(Z)[:, None]

    # Compute associator
    assoc = compute_associator(X, Y, Z, n)
    assoc_norm = cd_norm(assoc)

    # Ratio r = ||[x,y,z]|| / (||x|| ||y|| ||z||)
    # Since x,y,z are unit vectors, denominators are 1
    r = assoc_norm

    # Defects (Schafer 1954: should be ~0)
    flex_defect = compute_flexibility_defect(X, Y, n)
    power_defect = compute_power_assoc_defect(X, n)

    result = {
        "level": n,
        "dim": dim,
        "M": M,
        "seed": seed,
        "mean_r": float(np.mean(r)),
        "median_r": float(np.median(r)),
        "std_r": float(np.std(r)),
        "max_r": float(np.max(r)),
        "min_r": float(np.min(r)),
        "q05_r": float(np.quantile(r, 0.05)),
        "q95_r": float(np.quantile(r, 0.95)),
        "flexibility_defect_max": float(np.max(flex_defect)),
        "power_assoc_defect_max": float(np.max(power_defect)),
        "flexibility_defect_mean": float(np.mean(flex_defect)),
        "power_assoc_defect_mean": float(np.mean(power_defect)),
        "r_samples": r.tolist(),  # full sample for KS and exact reproducibility
    }

    if verbose:
        print(f"  Level {n} (dim={dim}): mean_r={result['mean_r']:.6f}, "
              f"median_r={result['median_r']:.6f}, max_r={result['max_r']:.6f}, "
              f"flex_max={result['flexibility_defect_max']:.2e}, "
              f"power_max={result['power_assoc_defect_max']:.2e}")

    return result

# =============================================================================
# 4. Verdict engine (pre-registered thresholds)
# =============================================================================

def apply_verdict(results_by_level):
    """
    Apply pre-registered verdict rules.
    results_by_level: dict {n: result_dict}
    """
    levels = sorted(results_by_level.keys())

    mean_rs = [results_by_level[n]["mean_r"] for n in levels]

    # Check Schafer oracle: defects must be < 1e-12
    for n in levels:
        flex_max = results_by_level[n]["flexibility_defect_max"]
        power_max = results_by_level[n]["power_assoc_defect_max"]
        if flex_max >= 1e-12 or power_max >= 1e-12:
            return {
                "verdict": "IMPLEMENTATION_BUG",
                "reason": f"Schafer oracle violated at level {n}: "
                          f"flex_max={flex_max:.2e}, power_max={power_max:.2e}",
                "level": n
            }

    # Check PROGRESSIVE: saturation + distributional convergence
    all_sat = True
    all_ks = True
    for i in range(len(levels) - 1):
        n1, n2 = levels[i], levels[i + 1]
        rel_change = abs(mean_rs[i + 1] - mean_rs[i]) / mean_rs[i] if mean_rs[i] != 0 else float('inf')
        if rel_change >= 0.05:
            all_sat = False
        # KS test between consecutive levels
        r1 = np.array(results_by_level[n1]["r_samples"])
        r2 = np.array(results_by_level[n2]["r_samples"])
        ks_stat, _ = stats.ks_2samp(r1, r2)
        if ks_stat >= 0.05:
            all_ks = False

    min_r_ok = all(mr >= 0.01 for mr in mean_rs)

    if min_r_ok and all_sat and all_ks:
        return {"verdict": "PROGRESSIVE", "reason": "mean_r >= 0.01, all consecutive relative changes < 5%, all KS < 0.05"}

    # Check KILL-A: growth
    growth_count = 0
    for i in range(len(levels) - 1):
        if mean_rs[i + 1] > mean_rs[i] * 1.20:
            growth_count += 1
        else:
            growth_count = 0
        if growth_count >= 2:
            return {"verdict": "KILL-A_growth", "reason": f"mean_r growth > 20% for 2+ consecutive levels at {levels[i]}-{levels[i+1]}"}

    # Check KILL-B: collapse
    collapse_count = 0
    for i in range(len(levels) - 1):
        if mean_rs[i + 1] < mean_rs[i] * 0.50:
            collapse_count += 1
        else:
            collapse_count = 0
        if collapse_count >= 2:
            return {"verdict": "KILL-B_collapse", "reason": f"mean_r collapse > 50% for 2+ consecutive levels at {levels[i]}-{levels[i+1]}"}

    for n in levels:
        if n >= 6 and mean_rs[levels.index(n)] < 1e-6:
            return {"verdict": "KILL-B_collapse", "reason": f"mean_r < 1e-6 at level {n}"}

    # Check KILL-C: reconfiguration (stable mean but distributional shift)
    if min_r_ok and all_sat:
        ks_fail_count = 0
        for i in range(len(levels) - 1):
            n1, n2 = levels[i], levels[i + 1]
            r1 = np.array(results_by_level[n1]["r_samples"])
            r2 = np.array(results_by_level[n2]["r_samples"])
            ks_stat, _ = stats.ks_2samp(r1, r2)
            if ks_stat >= 0.05:
                ks_fail_count += 1
            else:
                ks_fail_count = 0
            if ks_fail_count >= 2:
                return {"verdict": "KILL-C_reconfiguration", "reason": f"KS > 0.05 for 2+ consecutive levels at {levels[i]}-{levels[i+1]}"}

    # Fallback: MIXED / UNDECIDED
    return {"verdict": "MIXED", "reason": "Does not satisfy any pre-registered decisive verdict rule"}

# =============================================================================
# 5. Script self-hash (for reproducibility audit)
# =============================================================================

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# =============================================================================
# 6. Main execution
# =============================================================================

if __name__ == "__main__":
    SCRIPT_PATH = __file__
    script_sha256 = sha256_of_file(SCRIPT_PATH)
    timestamp = datetime.now(timezone.utc).isoformat()

    LEVELS = [4, 5, 6, 7]
    M = 10000
    SEED = 42

    print("=" * 70)
    print("Claim B S_c2: Associator Distribution Measurement")
    print(f"Timestamp: {timestamp}")
    print(f"Script SHA256: {script_sha256}")
    print(f"Levels: {LEVELS}, M={M}, seed={SEED}")
    print("=" * 70)

    # Run 1
    print("\n--- Run 1 ---")
    results_run1 = {}
    for n in LEVELS:
        results_run1[n] = measure_level(n, M, SEED, verbose=True)

    # Verdict for run 1
    verdict1 = apply_verdict(results_run1)
    print(f"\nVerdict (run 1): {verdict1['verdict']}")
    print(f"Reason: {verdict1['reason']}")

    # Run 2 (reproducibility check)
    print("\n--- Run 2 (reproducibility check) ---")
    results_run2 = {}
    for n in LEVELS:
        results_run2[n] = measure_level(n, M, SEED, verbose=True)

    verdict2 = apply_verdict(results_run2)
    print(f"\nVerdict (run 2): {verdict2['verdict']}")

    # Byte-identical check on key metrics
    identical = True
    mismatches = []
    for n in LEVELS:
        for key in ["mean_r", "median_r", "max_r", "std_r"]:
            v1 = results_run1[n][key]
            v2 = results_run2[n][key]
            if v1 != v2:
                identical = False
                mismatches.append((n, key, v1, v2))

    print(f"\nByte-identical reproducibility: {'PASS' if identical else 'FAIL'}")
    if not identical:
        print("Mismatches:")
        for m in mismatches:
            print(f"  Level {m[0]}, {m[1]}: run1={m[2]}, run2={m[3]}")

    # Compute KS statistics for reporting
    ks_stats = {}
    for i in range(len(LEVELS) - 1):
        n1, n2 = LEVELS[i], LEVELS[i + 1]
        r1 = np.array(results_run1[n1]["r_samples"])
        r2 = np.array(results_run1[n2]["r_samples"])
        ks_stat, ks_pval = stats.ks_2samp(r1, r2)
        ks_stats[f"{n1}_to_{n2}"] = {
            "ks_statistic": float(ks_stat),
            "p_value": float(ks_pval),
            "n1": n1, "n2": n2
        }

    # Relative changes in mean_r
    rel_changes = {}
    for i in range(len(LEVELS) - 1):
        n1, n2 = LEVELS[i], LEVELS[i + 1]
        mr1 = results_run1[n1]["mean_r"]
        mr2 = results_run1[n2]["mean_r"]
        rel_changes[f"{n1}_to_{n2}"] = float(abs(mr2 - mr1) / mr1) if mr1 != 0 else None

    # Build output JSON
    output = {
        "findingId": "C2_associator_distribution_2026-07-24",
        "stage": "S_c2",
        "timestamp": timestamp,
        "script_sha256": script_sha256,
        "script_path": SCRIPT_PATH,
        "protocol": "LOOP_PROTOCOL.md",
        "prereg": "prereg_claimB_loop_20260724.json",
        "levels": LEVELS,
        "M": M,
        "seed": SEED,
        "verdict": verdict1["verdict"],
        "verdict_reason": verdict1["reason"],
        "reproducibility": {
            "run2_verdict": verdict2["verdict"],
            "byte_identical": identical,
            "mismatches": mismatches if not identical else []
        },
        "layer_disclosure": {
            "L1_algebra": "Cayley-Dickson associator norm ratio r(x,y,z)",
            "L2_L3_physics": "NO physics prediction claimed. Avenue3 barrier intact.",
            "mythology": "USER_PRIMARY ICE_ORCA_DRAGON canon #2"
        },
        "avenue3_caveat": (
            "Even if PROGRESSIVE: CD doubling forces discrete integers {2,3,7,14} only. "
            "No continuous observable emergence mechanism connects any algebraic invariant "
            "to gravitational observables. This caveat is MANDATORY per ICE_WORKBENCH_REFRAME_2026-05-18 §3."
        ),
        "metrics_per_level": {
            str(n): {
                k: v for k, v in results_run1[n].items() if k != "r_samples"
            } for n in LEVELS
        },
        "ks_statistics": ks_stats,
        "mean_r_relative_changes": rel_changes,
        "thresholds_applied": {
            "saturation_relative_change": 0.05,
            "saturation_min_r": 0.01,
            "growth_relative_increase": 0.20,
            "collapse_relative_decrease": 0.50,
            "collapse_absolute_r": 1e-06,
            "ks_reconfiguration": 0.05
        }
    }

    OUT_PATH = "results_c2_associator_distribution.json"
    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults written to: {OUT_PATH}")
    print(f"Final verdict: {verdict1['verdict']}")
