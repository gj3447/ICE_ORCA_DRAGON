"""Apply MC numerology judge verdicts to 3 HOLD JSONs.

Promotes NUMEROLOGY_HOLD -> NUMEROLOGY_CONFIRMED (or stays HOLD with MC evidence)
based on numerology_mc_results.json.

# KG: ICE_ORCA_DRAGON L2 numerology gate operationalization
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-17"

mc = json.loads((ROOT / "numerology_mc_results.json").read_text())

UPDATES = {
    "derive_dimensionless_results.json": {
        "verdict": "NUMEROLOGY_CONFIRMED",
        "mc_evidence_ref": "numerology_mc_results.json :: claim_K_koide_2_3",
        "mc_p_e_given_not_h": mc["claim_K_koide_2_3"]["p_any_target_hit"],
        "mc_null_model": "499 random ratios from ICE-like atomic integer set",
        "mc_verdict_reasoning": (
            "P(any-target hit | null) = 1.000 over 8 small-rational targets x 499 candidates. "
            "Look-elsewhere effect renders the observed exact matches inevitable. "
            "ICE 'derivation' of Koide_Q = 2/3 (and 7 other observables) carries no information "
            "beyond combinatorial arithmetic; promotion from HOLD."
        ),
    },
    "verify_mp_mW_results.json": {
        "verdict": "NUMEROLOGY_CONFIRMED",
        "mc_evidence_ref": "numerology_mc_results.json :: claim_M1_mp_mW_literal + claim_M2_mp_mW_layer3",
        "mc_p_e_given_not_h_layer3": mc["claim_M2_mp_mW_layer3"]["p_random_R_fits_within_0.1pct"],
        "mc_layer1_rel_diff_literal_pct": mc["claim_M1_mp_mW_literal"]["rel_diff_literal_pct"],
        "mc_layer1_rel_diff_reciprocal_pct": mc["claim_M1_mp_mW_literal"]["rel_diff_reciprocal_pct"],
        "mc_null_model_layer3": "random R log-uniform, search a in [1,500000] x n in {14..19}",
        "mc_verdict_reasoning": (
            "layer1 literal 3*256 vs observed mp/mW off by O(10) even with reciprocal interpretation "
            "(88.8% rel_diff). layer3 a*2^n search space ~3M candidates per ratio: under null, "
            "81.2% of random R fit within 0.1%. This is rational approximation, not physics. "
            "Promotion from HOLD."
        ),
    },
    "derive_epsilon_results.json": {
        "verdict": "NUMEROLOGY_HOLD",
        "mc_evidence_ref": "numerology_mc_results.json :: claim_E_epsilon_adelberger",
        "mc_p_e_given_not_h": mc["claim_E_epsilon_adelberger"]["adelberger_pass_rate_under_null"],
        "mc_null_model": "random power-law eps0/r0/alpha log-uniform; Adelberger gate check",
        "mc_verdict_reasoning": (
            "Adelberger pass rate under wide-prior null = 23.8% (not trivially permissive). "
            "Gate has discriminatory power, but ICE did not pre-predict a specific epsilon form -- "
            "the script enumerates 7 forms and reports 5 pass. Post-hoc enumeration without "
            "pre-prediction remains NUMEROLOGY_HOLD even though the constraint itself has teeth. "
            "Upgrade to CONFIRMED or SIGNAL requires ICE-derived unique form prediction first."
        ),
    },
}


def patch(path: pathlib.Path, upd: dict) -> None:
    d = json.loads(path.read_text())
    d["verdict"] = upd["verdict"]
    # preserve original verdict_reasoning, add mc_verdict_reasoning
    d.setdefault("verdict_reasoning_prior", d.get("verdict_reasoning", ""))
    d["verdict_reasoning"] = upd["mc_verdict_reasoning"]
    d["verdict_source"] = "numerology_mc_judge.py 2026-05-17 (supersedes 2026-05-14 ledger)"
    d["verdict_date"] = DATE
    for k, v in upd.items():
        if k.startswith("mc_"):
            d[k] = v
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print(f"  patched: {path.name} -> {upd['verdict']}")


def main() -> None:
    for name, upd in UPDATES.items():
        p = ROOT / name
        if not p.exists():
            print(f"  MISSING: {name}")
            continue
        patch(p, upd)


if __name__ == "__main__":
    main()
