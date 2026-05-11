# KG: Koide Q = 2/3 from Z₃, Cabibbo angle = √(1/20), ICE Observable and Likelihood Descent
# LONGINUS: sourceId=derive_dimensionless_ICE, sourcePath=derive_dimensionless_ICE.py
"""
Dimensionless ICE Observables — Scale-free Predictions
========================================================
ICE는 scale-free → dimensionless observable에만 예측 능력.

전략:
1. ICE 구조의 "자연" dimensionless numbers 열거
2. 실험값(Koide, θ_W, Cabibbo, θ_13/23, CP phase 등)과 비교
3. Numerology Taliban 자동 적용 (우연 match 여과)
4. 생존 예측 식별

실행: python3 derive_dimensionless_ICE.py
"""
import numpy as np
import json
from itertools import combinations

np.set_printoptions(precision=6, suppress=True)


# ============================================================
# ICE structural numbers (Z₂⁴-graded sedenion)
# ============================================================
ICE_NUMBERS = {
    # OEIS A167654
    "ZD_n4": 42, "ZD_n5": 294, "ZD_n6": 1518, "ZD_n7": 6942, "ZD_n8": 29886,
    # G₂ Lie algebra
    "G2_fundamental_dim": 7,
    "G2_adjoint_dim": 14,
    "G2_num_roots": 12,
    "G2_long_roots": 6,
    "G2_short_roots": 6,
    "G2_Weyl_order": 12,
    "root_length_ratio_sq": 3,  # long²/short² = 3
    # Orbit structure
    "orbits": 7,
    "orbit_size": 6,
    "total_ZD_pairs": 42,
    # XOR structure
    "XOR_sectors": 7,
    "XOR_min_offset": 8,  # XOR = 8 + excluded
    # Combinatorial
    "generations": 3,
    "SU3_dim": 8,
    "SU2_dim": 3,
    "U1_dim": 1,
    "SM_gauge_total": 12,
}

# ============================================================
# Experimental dimensionless observables
# ============================================================
EXPERIMENTAL_OBSERVABLES = {
    "Koide_Q": {"value": 2/3, "exact": True, "measured": 0.666661, "tol": 1e-4,
                "description": "Charged lepton mass ratio"},
    "sin2_theta_W_GUT": {"value": 3/8, "exact": True, "measured": 0.375, "tol": 0.01,
                          "description": "Weinberg angle at GUT scale"},
    "sin2_Cabibbo": {"value": 1/20, "exact": False, "measured": 0.0506, "tol": 0.005,
                      "description": "Cabibbo angle sin² ≈ 0.0506"},
    "g3_g2_ratio": {"value": 1, "exact": False, "measured": 1.0, "tol": 0.1,
                     "description": "g_strong/g_weak coupling ratio"},
    "g2sq_g1sq": {"value": 5/3, "exact": True, "measured": 1.667, "tol": 0.05,
                   "description": "GUT coupling ratio g_2²/g_1²"},
    "theta_13_neutrino_sq": {"value": 0.02241, "exact": False, "tol": 0.005,
                               "description": "neutrino θ_13 mixing"},
    "CP_phase_rad": {"value": 1.36, "exact": False, "tol": 0.2,
                      "description": "CP violation phase δ"},
    "Jarlskog": {"value": 3.18e-5, "exact": False, "tol": 5e-6,
                  "description": "CP asymmetry invariant"},
}


# ============================================================
# Enumerate ICE ratios
# ============================================================
def enumerate_ice_ratios():
    """ICE 구조에서 나올 수 있는 dimensionless ratios 생성"""
    nums = ICE_NUMBERS.copy()
    ratios = {}

    # Single values
    for k, v in nums.items():
        ratios[f"{k}"] = float(v)

    # Pairwise ratios
    keys = list(nums.keys())
    for k1, k2 in combinations(keys, 2):
        v1, v2 = nums[k1], nums[k2]
        if v2 != 0:
            ratios[f"{k1}/{k2}"] = v1 / v2
        if v1 != 0:
            ratios[f"{k2}/{k1}"] = v2 / v1

    # Fractions of orbits and related
    ratios["C(7,2)/7"] = 21 / 7  # = 3
    ratios["C(7,2)/42"] = 21 / 42  # = 0.5
    ratios["2/3"] = 2/3
    ratios["3/8"] = 3/8
    ratios["1/20"] = 1/20
    ratios["5/3"] = 5/3
    ratios["1/42"] = 1/42
    ratios["6/14"] = 6/14  # G2 short/adjoint

    # sqrt-based (from root length)
    ratios["sqrt(3)"] = np.sqrt(3)
    ratios["1/sqrt(3)"] = 1/np.sqrt(3)

    # arctan specific
    ratios["arctan(7/3)"] = np.arctan(7/3)
    ratios["arctan(sqrt(3))"] = np.arctan(np.sqrt(3))  # = π/3

    # Koide-specific
    ratios["Koide_predicted"] = 2/3  # C(7,2)/7 = 3, then Koide?

    # Jarlskog-like products
    ratios["sin_theta13_sq"] = 1/(ICE_NUMBERS["total_ZD_pairs"] + 3)  # ≈ 1/45 ≈ 0.022
    ratios["1/(C(6,3)*C(6,2)*2)"] = 1/(20 * 15 * 2)  # = 1/600

    return ratios


# ============================================================
# Match to experimental observables
# ============================================================
def match_observables(ratios, observables):
    """각 관측량에 대해 ICE ratio 매칭 찾기"""
    matches = {}
    for obs_name, obs_data in observables.items():
        obs_val = obs_data["value"]
        tol = obs_data["tol"]
        candidates = []
        for ratio_name, ratio_val in ratios.items():
            if ratio_val == 0 or obs_val == 0:
                continue
            diff = abs(ratio_val - obs_val)
            rel_diff = diff / abs(obs_val) if abs(obs_val) > 1e-10 else 1e10
            if diff < tol:
                candidates.append({
                    "formula": ratio_name,
                    "value": ratio_val,
                    "experimental": obs_val,
                    "abs_diff": diff,
                    "rel_diff_pct": rel_diff * 100
                })
        candidates.sort(key=lambda x: x["abs_diff"])
        matches[obs_name] = {
            "observable": obs_data["description"],
            "experimental_value": obs_val,
            "ICE_candidates": candidates[:3]
        }
    return matches


# ============================================================
# Numerology Taliban per candidate
# ============================================================
def numerology_audit(candidate, context):
    """각 candidate에 대해 6-signature check"""
    formula = candidate["formula"]
    issues = []

    # (1) Truncation-dependence — 이 경우는 순수 formula라 해당 없음 (대부분)

    # (4) Post-hoc fitting: 너무 convenient한 matches?
    # 예: Koide Q=2/3. 2/3가 ICE 구조에 자연 나오나?
    # C(7,2)/7 = 21/7 = 3, not 2/3. Hmm wrong.
    # 2/3는 specifically picked to match Koide
    if "/" in formula:
        parts = formula.split("/")
        if len(parts) == 2:
            # Check if numbers are "natural" in ICE
            num_str, denom_str = parts
            try:
                num = int(num_str)
                denom = int(denom_str)
                # 자연수지만 ICE 구조에 name-aligned 하지 않으면 fitting 의심
                is_named = num_str in ICE_NUMBERS or denom_str in ICE_NUMBERS
                if not is_named and num < 100 and denom < 100:
                    issues.append(f"Small number ratio {num}/{denom} — fitting risk")
            except ValueError:
                pass  # named ratio

    # (5) Physical derivation weakness
    if "G2" not in formula and "ZD" not in formula and "orbit" not in formula and \
       "sqrt" not in formula and "arctan" not in formula:
        # Simple number ratio without ICE structure
        issues.append("No explicit ICE structural component")

    return issues


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DIMENSIONLESS ICE OBSERVABLES — Scale-free predictions")
    print("=" * 70 + "\n")

    print("ICE 구조의 모든 dimensionless quantity 열거 중...")
    ratios = enumerate_ice_ratios()
    print(f"  총 {len(ratios)} 개 candidates generated")
    print()

    matches = match_observables(ratios, EXPERIMENTAL_OBSERVABLES)

    print("=" * 70)
    print("실험값 매칭 결과")
    print("=" * 70)
    print()

    for obs_name, match_data in matches.items():
        exp_val = match_data["experimental_value"]
        print(f"[{obs_name}] ({match_data['observable']})")
        print(f"  실험값: {exp_val:.6f}")
        if match_data["ICE_candidates"]:
            print(f"  ICE 후보:")
            for c in match_data["ICE_candidates"]:
                marker = "🎯" if c["rel_diff_pct"] < 1 else ("✓" if c["rel_diff_pct"] < 5 else "~")
                print(f"    {marker} {c['formula']:<40} = {c['value']:.6f}, "
                      f"diff = {c['rel_diff_pct']:.3f}%")

                # Numerology audit
                issues = numerology_audit(c, obs_name)
                for iss in issues:
                    print(f"        ⚠️ {iss}")
        else:
            print(f"  ICE 후보: 없음")
        print()

    # Summary
    print("=" * 70)
    print("수비학 탈레반 종합 판정")
    print("=" * 70)
    print()

    genuinely_structural = 0
    fitting_suspected = 0
    no_match = 0

    for obs_name, match_data in matches.items():
        if not match_data["ICE_candidates"]:
            no_match += 1
            continue
        best = match_data["ICE_candidates"][0]
        issues = numerology_audit(best, obs_name)
        if len(issues) == 0:
            genuinely_structural += 1
            print(f"  ✅ {obs_name}: genuinely ICE-structural match")
        else:
            fitting_suspected += 1
            print(f"  ⚠️ {obs_name}: structural match but flagged")

    print()
    print(f"Total observables: {len(EXPERIMENTAL_OBSERVABLES)}")
    print(f"  🎯 Genuinely structural: {genuinely_structural}")
    print(f"  ⚠️ Fitting suspected:     {fitting_suspected}")
    print(f"  ❌ No match:              {no_match}")
    print()

    # ============================================================
    # HONEST OVERALL ASSESSMENT
    # ============================================================
    print("=" * 70)
    print("HONEST ASSESSMENT")
    print("=" * 70)
    print()
    print("Finding: ICE 구조에서 '자연스럽게' 나오는 dimensionless numbers가")
    print("         실험값과 일부 매치됨. 그러나:")
    print()
    print("(1) Koide Q=2/3: ICE 구조에서 직접 나온다는 증명 없음 (postdiction)")
    print("(2) sin²θ_W=3/8: G₂ 구조가 아닌 SU(5) GUT fact (rediscovery)")
    print("(3) Cabibbo 1/20: specific C(6,3)·C(6,2)·2 = 600 조합 → fitting 의심")
    print("(4) θ_13 = 1/45: fitting risk")
    print()
    print("이 모든 match는 **postdiction/fitting/rediscovery 조합**.")
    print("진짜 ICE-predicted observable 없음.")
    print()
    print("탈레반 최종 verdict: **NOT NOBEL-WORTHY**")
    print()
    print("남은 희망:")
    print("  • ICE가 새로운 dimensionless quantity를 predict:")
    print("    — 미측정된 neutrino mass ordering ratio?")
    print("    — 미발견 입자의 charge quantum number?")
    print("    — 새로운 CP-invariant?")
    print("  • 기존 관측값 중 SM이 설명 못하는 것을 ICE가 설명:")
    print("    — Koide relation이 정확히 2/3인 이유?")
    print("    — CP 위상값의 구조?")
    print()
    print("이 방향 중 하나 pursuit 하면 genuine prediction 가능.")
    print("하지만 structural derivation 필수 (fitting 금지).")

    results = {
        "total_ICE_ratios": len(ratios),
        "matches": matches,
        "genuinely_structural": genuinely_structural,
        "fitting_suspected": fitting_suspected,
        "no_match": no_match,
        "verdict": "Postdictions/fitting, no genuine prediction yet"
    }
    with open("/Users/lagyeongjun/CD/AGENT/derive_dimensionless_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults → derive_dimensionless_results.json")
