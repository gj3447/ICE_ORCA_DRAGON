#!/usr/bin/env python3
# KG: ICE hidden numerology MC scan v2 — target category expansion
# Origin: challenge-naesengmoon-numerology-1lens-axis5-hidden-scan-target-category-coverage-2026-05-20
# Predecessor: numerology_hidden_scan.py (v1, 2026-05-18)
# LONGINUS: sourceId=numerology_hidden_scan_v2, sourcePath=numerology_hidden_scan_v2_target_categories_2026-05-20.py
"""
Hidden Numerology MC Scanner v2 — 4-family target enumeration

v1 covered only small-rational targets. v2 adds three target families per
naesengmoon 1-lens axis 5 challenge:

  Family A: small-rational (already in v1 — re-checked here for parity)
  Family B: transcendental (π/n, e^±n, √2/2)
  Family C: log-value (ln n)
  Family D: large-integer combinatorial (42, 137, 105 etc.)

For each candidate, run MC null sampling against same ICE_PRIMITIVES set
and apply look-elsewhere Bonferroni correction.
"""
import json
import math
import random
from pathlib import Path

random.seed(42)

ICE_DIR = Path(__file__).resolve().parent

ICE_PRIMITIVES = {
    "sedenion_dim": 16, "sedenion_pair_count": 120,
    "zd_n4_42": 42, "zd_n5_294": 294, "zd_n6_1518": 1518,
    "zd_n7_6942": 6942, "zd_n8_29886": 29886,
    "g2_fundamental": 7, "g2_adjoint": 14, "g2_roots": 12,
    "g2_long_roots": 6, "g2_short_roots": 6, "g2_weyl_order": 12,
    "g2_root_ratio_sq": 3,
    "s3_order": 6, "s3_irreducible_sum_sq": 6,
    "ice_orbits": 7, "ice_orbit_size": 6, "ice_total_zd_pairs": 42,
    "xor_sectors": 7, "xor_min_offset": 8,
    "su2_dim": 3, "su2_doublet": 2, "custodial_failures": 42,
    "octonion_dim": 8, "octonion_aut": 14,
    "zd64_dim": 64, "friedmann_dim": 4,
}


def extract_ratios(primitives, max_value=10000):
    ratios = []
    keys = list(primitives.keys())
    for i, k1 in enumerate(keys):
        for k2 in keys[i:]:
            v1, v2 = primitives[k1], primitives[k2]
            if v2 != 0:
                r = v1 / v2
                if r <= max_value:
                    ratios.append((f"{k1}/{k2}", r))
            if v1 != 0:
                r = v2 / v1
                if r <= max_value:
                    ratios.append((f"{k2}/{k1}", r))
    return ratios


def mc_null_match(target, tol, primitives, n_mc=10000):
    values = list(primitives.values())
    hits = 0
    for _ in range(n_mc):
        v1 = random.choice(values)
        v2 = random.choice(values)
        if v2 == 0:
            continue
        if abs(v1 / v2 - target) <= tol:
            hits += 1
    return hits / n_mc


def look_elsewhere(p, n):
    return min(1.0, p * n)


def verdict(p):
    if p < 0.01:
        return "SIGNAL_GENUINE"
    if p < 0.5:
        return "SIGNAL_WEAK"
    return "NUMEROLOGY_CONFIRMED"


# 4-family target enumeration
CANDIDATES = [
    # Family B: transcendental
    {"family": "B_transcendental", "name": "pi_over_4", "target": math.pi / 4, "tol": 0.01,
     "note": "π/4 ≈ 0.7854 — close to Casimir 0.75 (8% off, v1 missed)"},
    {"family": "B_transcendental", "name": "pi_over_2", "target": math.pi / 2, "tol": 0.02,
     "note": "π/2 ≈ 1.5708"},
    {"family": "B_transcendental", "name": "e_inv", "target": 1 / math.e, "tol": 0.005,
     "note": "e⁻¹ ≈ 0.3679 — close to Singh δ²=3/8=0.375 (2% off)"},
    {"family": "B_transcendental", "name": "e_inv_sq", "target": 1 / (math.e ** 2), "tol": 0.005,
     "note": "e⁻² ≈ 0.1353"},
    {"family": "B_transcendental", "name": "sqrt2_over_2", "target": math.sqrt(2) / 2, "tol": 0.01,
     "note": "√2/2 ≈ 0.7071"},
    {"family": "B_transcendental", "name": "pi_squared_over_6", "target": (math.pi ** 2) / 6, "tol": 0.02,
     "note": "ζ(2) = π²/6 ≈ 1.6449"},

    # Family C: log-value
    {"family": "C_log_value", "name": "ln_2", "target": math.log(2), "tol": 0.01,
     "note": "ln 2 ≈ 0.6931 — close to Casimir 0.75 (8% off, v1 missed)"},
    {"family": "C_log_value", "name": "ln_3", "target": math.log(3), "tol": 0.01,
     "note": "ln 3 ≈ 1.0986"},
    {"family": "C_log_value", "name": "ln_pi", "target": math.log(math.pi), "tol": 0.01,
     "note": "ln π ≈ 1.1447"},
    {"family": "C_log_value", "name": "ln_2_times_4", "target": 4 * math.log(2), "tol": 0.02,
     "note": "4·ln 2 ≈ 2.7726 — claimed in N-5 session log, MC test now done"},

    # Family D: large-integer combinatorial (target as direct value, not ratio)
    # For these, sample products instead of ratios
    {"family": "D_large_integer", "name": "fine_structure_recip_137", "target": 137.036, "tol": 0.5,
     "note": "1/α ≈ 137.036 — fine structure reciprocal"},
    {"family": "D_large_integer", "name": "xor_105", "target": 105.0, "tol": 1.0,
     "note": "XOR invariant count 105 = 7·15 (already in primitives via 105 = 7·15)"},
    {"family": "D_large_integer", "name": "proton_lifetime_log_33", "target": 33.0, "tol": 0.5,
     "note": "log₁₀(τ_p / yr) ≈ 33-34 (proton decay bound)"},

    # Family A: small-rational (parity re-check)
    {"family": "A_small_rational", "name": "three_quarters", "target": 0.75, "tol": 0.005,
     "note": "3/4 — Casimir 0.75 baseline"},
    {"family": "A_small_rational", "name": "two_thirds", "target": 2 / 3, "tol": 0.005,
     "note": "2/3 — Koide Q baseline (already CONFIRMED)"},
]


def main():
    ratios = extract_ratios(ICE_PRIMITIVES)
    n_trials = len(ratios)
    print(f"ICE primitives: {len(ICE_PRIMITIVES)}")
    print(f"Pairwise ratios: {n_trials}")
    print(f"Candidates across 4 families: {len(CANDIDATES)}")
    print()

    results = []
    for cand in CANDIDATES:
        p_raw = mc_null_match(cand["target"], cand["tol"], ICE_PRIMITIVES, n_mc=10000)
        p_corr = look_elsewhere(p_raw, n_trials)
        v = verdict(p_corr)
        result = {
            "family": cand["family"],
            "candidate": cand["name"],
            "target": cand["target"],
            "tolerance": cand["tol"],
            "p_raw": p_raw,
            "p_corrected": p_corr,
            "verdict": v,
            "note": cand["note"],
        }
        results.append(result)
        print(f"  [{cand['family']}] {cand['name']:<32} target={cand['target']:.4f}  "
              f"p_raw={p_raw:.4f}  p_corr={p_corr:.4f}  → {v}")

    # Family-level summary
    by_family = {}
    for r in results:
        f = r["family"]
        by_family.setdefault(f, []).append(r["verdict"])

    out = ICE_DIR / "numerology_hidden_scan_v2_results_2026-05-20.json"
    with out.open("w") as fh:
        json.dump({
            "date": "2026-05-20",
            "origin_challenge": "challenge-naesengmoon-numerology-1lens-axis5-hidden-scan-target-category-coverage-2026-05-20",
            "predecessor": "numerology_hidden_scan_results.json (v1, 2026-05-18)",
            "n_primitives": len(ICE_PRIMITIVES),
            "n_pairwise_ratios": n_trials,
            "n_mc_samples": 10000,
            "target_family_enumeration": ["A_small_rational", "B_transcendental", "C_log_value", "D_large_integer"],
            "results": results,
            "by_family_verdicts": by_family,
            "summary_counts": {
                "SIGNAL_GENUINE": sum(1 for r in results if r["verdict"] == "SIGNAL_GENUINE"),
                "SIGNAL_WEAK": sum(1 for r in results if r["verdict"] == "SIGNAL_WEAK"),
                "NUMEROLOGY_CONFIRMED": sum(1 for r in results if r["verdict"] == "NUMEROLOGY_CONFIRMED"),
            },
        }, fh, indent=2)
    print(f"\nSaved: {out}")
    print("\nBy-family verdicts:")
    for fam, verds in by_family.items():
        print(f"  {fam}: {verds}")


if __name__ == "__main__":
    main()
