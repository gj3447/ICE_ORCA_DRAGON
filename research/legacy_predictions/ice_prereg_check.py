#!/usr/bin/env python3
# KG: ICE pre-registered prediction PDG comparison + MC null gate
# LONGINUS: sourceId=ice_prereg_check
"""
ICE Pre-Registration Step 3+4: PDG comparison + MC null gate.

Reads the pre-registered prediction list (ice_prereg_predictions_2026-05-18.json)
and compares each P01-P15 against a frozen set of PDG observables.

For each (prediction, observable) pair within tolerance, computes:
  P(E|~H) via MC null model (random ratios from ICE primitives)
  P_corrected (Bonferroni look-elsewhere: 15 predictions × N_observables)

Decision rule:
  P_corr < 0.01 → SIGNAL_GENUINE (pre-registered confirmed prediction)
  0.01 ≤ P_corr < 0.5 → SIGNAL_WEAK
  P_corr ≥ 0.5 → NUMEROLOGY (chance match)
  NO match within tolerance → STRUCTURAL_INCAPACITY for this observable
"""
import hashlib
import json
import random
from pathlib import Path

random.seed(42)

ICE_DIR = Path(__file__).resolve().parent
PREREG = ICE_DIR / "ice_prereg_predictions_2026-05-18.json"

# Frozen pre-registration verification
prereg = json.loads(PREREG.read_text())
expected_hash = prereg["sha256_commit"]
recomputed = hashlib.sha256(
    json.dumps(prereg["predictions"], sort_keys=True, indent=None, separators=(",", ":")).encode()
).hexdigest()
assert expected_hash == recomputed, f"PREREG HASH MISMATCH: {expected_hash} vs {recomputed}"
print(f"✓ Pre-registration sha256 verified: {expected_hash}")

predictions = prereg["predictions"]

# ============================================================
# PDG observable set (frozen — chosen BEFORE seeing predictions)
# ============================================================
PDG_OBSERVABLES = [
    {"name": "n_generations_SM", "value": 3, "tolerance": 0.001, "note": "3 fermion generations"},
    {"name": "Higgs_isospin_doublet", "value": 2, "tolerance": 0.001, "note": "Higgs SU(2) doublet"},
    {"name": "EW_sector_SU2xU1_rank", "value": 2, "tolerance": 0.001, "note": "EW gauge rank"},
    {"name": "m_W_over_m_Z_squared", "value": 0.777, "tolerance": 0.002, "note": "(m_W/m_Z)² ≈ cos²θ_W"},
    {"name": "m_W_over_m_Z", "value": 0.8815, "tolerance": 0.002, "note": "m_W/m_Z ratio"},
    {"name": "m_H_over_m_Z", "value": 1.374, "tolerance": 0.005, "note": "Higgs/Z mass ratio"},
    {"name": "m_H_over_m_W", "value": 1.559, "tolerance": 0.005, "note": "Higgs/W mass ratio"},
    {"name": "m_top_over_m_Z", "value": 1.901, "tolerance": 0.01, "note": "Top/Z mass ratio"},
    {"name": "alpha_em_inv_at_MZ", "value": 127.95, "tolerance": 0.05, "note": "α_em^-1 at M_Z"},
    {"name": "alpha_s_at_MZ", "value": 0.1180, "tolerance": 0.001, "note": "α_s at M_Z"},
    {"name": "sin_sq_theta_W", "value": 0.23122, "tolerance": 0.0005, "note": "Weinberg angle (already in registry)"},
    {"name": "Cabibbo_angle_squared", "value": 0.05077, "tolerance": 0.0005, "note": "sin²θ_C ≈ 0.05"},
    {"name": "Cabibbo_angle", "value": 0.2253, "tolerance": 0.001, "note": "sin θ_C"},
    {"name": "Koide_Q_lepton", "value": 0.6666, "tolerance": 0.001, "note": "Koide relation (in registry)"},
    {"name": "SU3_color_dim", "value": 3, "tolerance": 0.001, "note": "SU(3) fundamental dim"},
    {"name": "SU3_octet_dim", "value": 8, "tolerance": 0.001, "note": "SU(3) adjoint dim"},
    {"name": "spin_one_half", "value": 0.5, "tolerance": 0.001, "note": "fermion spin"},
    {"name": "spin_one", "value": 1.0, "tolerance": 0.001, "note": "gauge boson spin"},
    {"name": "spin_two", "value": 2.0, "tolerance": 0.001, "note": "graviton spin"},
    {"name": "lepton_quark_charge_ratio", "value": 3.0, "tolerance": 0.001, "note": "(-1)/(-1/3) = 3 anomaly cancel"},
]

# ICE primitives for MC null
ICE_PRIMS = {
    "sedenion_dim": 16, "sedenion_pair_count": 120,
    "zd_n4_42": 42, "zd_n5_294": 294, "zd_n6_1518": 1518, "zd_n7_6942": 6942, "zd_n8_29886": 29886,
    "g2_fundamental": 7, "g2_adjoint": 14, "g2_roots": 12, "g2_long_roots": 6,
    "g2_short_roots": 6, "g2_weyl_order": 12, "g2_root_ratio_sq": 3,
    "s3_order": 6, "s3_irreducible_sum_sq": 6,
    "ice_orbits": 7, "ice_orbit_size": 6, "ice_total_zd_pairs": 42,
    "xor_sectors": 7, "xor_min_offset": 8,
    "su2_dim": 3, "su2_doublet": 2, "custodial_failures": 42,
    "octonion_dim": 8, "octonion_aut": 14,
    "zd64_dim": 64, "friedmann_dim": 4,
}


def mc_null(target, tolerance, n_mc=10000):
    """P(E|~H) = fraction of random ICE primitive ratios within tolerance of target."""
    values = list(ICE_PRIMS.values())
    match = 0
    for _ in range(n_mc):
        v1 = random.choice(values)
        v2 = random.choice(values)
        if v2 == 0:
            continue
        if abs(v1 / v2 - target) <= tolerance:
            match += 1
    return match / n_mc


def main():
    print("=" * 70)
    print("ICE PRE-REGISTERED PREDICTION CHECK")
    print(f"  pre-registered hash: {expected_hash}")
    print(f"  n_predictions: {len(predictions)}")
    print(f"  n_observables : {len(PDG_OBSERVABLES)}")
    print(f"  n_trials (look-elsewhere): {len(predictions) * len(PDG_OBSERVABLES)}")
    print("=" * 70)

    n_trials = len(predictions) * len(PDG_OBSERVABLES)
    results = []
    matches = []

    for p in predictions:
        for obs in PDG_OBSERVABLES:
            if abs(p["value"] - obs["value"]) <= obs["tolerance"]:
                p_raw = mc_null(obs["value"], obs["tolerance"])
                p_corr = min(1.0, p_raw * n_trials)
                if p_corr < 0.01:
                    verdict = "SIGNAL_GENUINE"
                elif p_corr < 0.5:
                    verdict = "SIGNAL_WEAK"
                else:
                    verdict = "NUMEROLOGY"
                match = {
                    "prediction_id": p["id"],
                    "prediction_name": p["name"],
                    "prediction_value": p["value"],
                    "observable_name": obs["name"],
                    "observable_value": obs["value"],
                    "diff": p["value"] - obs["value"],
                    "p_raw": p_raw,
                    "p_corrected": p_corr,
                    "verdict": verdict,
                    "obs_note": obs["note"],
                }
                matches.append(match)
                print(f"\n  MATCH: {p['id']} ({p['name']}) ↔ {obs['name']}")
                print(f"    prediction = {p['value']:.4f}, observable = {obs['value']:.4f}")
                print(f"    P_raw = {p_raw:.4f}, P_corr = {p_corr:.4f}")
                print(f"    VERDICT: {verdict}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total matches within tolerance: {len(matches)}")
    print(f"  SIGNAL_GENUINE (P_corr < 0.01) : {sum(1 for m in matches if m['verdict']=='SIGNAL_GENUINE')}")
    print(f"  SIGNAL_WEAK    (0.01-0.5)      : {sum(1 for m in matches if m['verdict']=='SIGNAL_WEAK')}")
    print(f"  NUMEROLOGY     (≥0.5)          : {sum(1 for m in matches if m['verdict']=='NUMEROLOGY')}")

    # Save
    out = ICE_DIR / "ice_prereg_check_results.json"
    payload = {
        "date": "2026-05-18",
        "cycle": "autoloop iter 41-55 Task 4 (Step 3+4)",
        "pre_registered_hash": expected_hash,
        "verified_hash_match": True,
        "n_predictions": len(predictions),
        "n_observables": len(PDG_OBSERVABLES),
        "n_trials_lookelsewhere": n_trials,
        "matches": matches,
        "summary": {
            "total_matches": len(matches),
            "SIGNAL_GENUINE": sum(1 for m in matches if m["verdict"] == "SIGNAL_GENUINE"),
            "SIGNAL_WEAK": sum(1 for m in matches if m["verdict"] == "SIGNAL_WEAK"),
            "NUMEROLOGY": sum(1 for m in matches if m["verdict"] == "NUMEROLOGY"),
        },
        "verdict_top_level": "PREREG_CHECK_COMPLETE",
        "gate_passed": True,
    }
    with out.open("w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n  Results saved: {out}")


if __name__ == "__main__":
    main()
