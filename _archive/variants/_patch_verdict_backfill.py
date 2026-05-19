"""Backfill `verdict` field on existing 15 result JSONs.

Verdict taxonomy: CONFIRMED | CONFIRMATION_LOCAL | REFUTED | NUMEROLOGY_HOLD
                  | INCONCLUSIVE | DISCOVERY

Preserves all existing fields. Adds top-level keys:
  - verdict
  - verdict_reasoning
  - verdict_source ("STATUS.md ledger 2026-05-14" or "result-inspection-2026-05-17")
  - verdict_date

# KG: ICE_ORCA_DRAGON L3 self-verdict generalization, Roadmap #4
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-17"

VERDICTS = {
    "derive_epsilon_results.json": {
        "verdict": "NUMEROLOGY_HOLD",
        "verdict_reasoning": (
            "Dimensional analysis category locally degenerating (STATUS.md). "
            "epsilon power-law sweeps span 18 orders of magnitude with adelberger_pass=true "
            "but observable_scales mostly absent; no pre-registered prediction. Post-fit."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14 + result inspection 2026-05-17",
    },
    "prove_higgs_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "42 ZD pairs (n_higgs_candidates=42) match external Lygeros 2006 '42 Assessors'. "
            "All 42 pairs show n_invariant=2 with complex structure. "
            "Pre-prediction via Lygeros literature; external peer reference exists."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14",
    },
    "prove_s3_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "All 4 sub-cases pass: S3.1 Jacobi=6*associator identity (diff=0.0), "
            "S3.2 2-form B absorbs Jacobi (residual=0.0), "
            "S3.3 L_infty Stasheff with l_3=associator, "
            "S3.4 FDA structure constants nontrivial (28/35 triads, 42 ZD pairs confirmed at n=4). "
            "Algebraic identity; ground-truth comparable."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14 + per-sub-case verdict fields",
    },
    "prove_s5_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "BV bracket S5.1 all_zero=true + all_bounded=true across test cases. "
            "Consistency check passes; algebraic ground truth."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14",
    },
    "queue_01_orbit_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "n_orbits=7, all orbit_sizes=6, so 7x6=42 matches sedenion ZD count. "
            "Consistent with S3 orbit decomposition on 42 ZD pairs."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14",
    },
    "queue_02_custodial_results.json": {
        "verdict": "REFUTED",
        "verdict_reasoning": (
            "n_success=0, n_fail=42; all 42 pairs fail custodial with "
            "max_commutator ~1.91-1.96 (not near 0). "
            "Naive custodial SU(2)xSU(2) embedding refuted. "
            "Pivot recommended: alternative embedding or threshold sensitivity scan."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14",
    },
    "queue_03_rep_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "All 42 pairs share uniform Casimir pattern (0.75, 0.75, 0.75, 0.75). "
            "Strong rep-decomposition regularity; pattern_counts shows single bucket."
        ),
        "verdict_source": "README headline + result inspection 2026-05-17",
    },
    "queue_04_hosotani_results.json": {
        "verdict": "CONFIRMATION_LOCAL",
        "verdict_reasoning": (
            "All 3 cases produce Hosotani vacuum signature: case1 V(pi)<V(0) (symmetric flip), "
            "case2 SSB confirmed (V0>0, Vpi<0), "
            "case3 theta converges to pi for all 7 angles (spread ~1e-7). "
            "Toy model only; no external peer reference."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_05_cw_results.json": {
        "verdict": "CONFIRMATION_LOCAL",
        "verdict_reasoning": (
            "4/4 scenarios show SSB=True with bounded V_min "
            "(SM-like / ICE orbit-like / G2 fundamental / Reverse). "
            "Coleman-Weinberg potential bounded across regimes. "
            "Toy; no external peer review."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_06_coop_results.json": {
        "verdict": "INCONCLUSIVE",
        "verdict_reasoning": (
            "gamma_critical=null (no critical coupling found in search range). "
            "final_scenario shows active_orbits=[1] only (1 of 7). "
            "Cooperative vacuum mechanism not demonstrated; "
            "broader gamma sweep or alternative initialization required."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_08_g2_results.json": {
        "verdict": "CONFIRMATION_LOCAL",
        "verdict_reasoning": (
            "independent_generators=16 (g2 expected 14 — 2-generator discrepancy noted), "
            "commutant_dim=1, 7 orbit_reps. "
            "Casimir eigenvalues range -3.95 to -0.20 (non-degenerate). "
            "Local confirmation with caveat: 16 vs 14 generator gap deserves follow-up."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_09_s3_results.json": {
        "verdict": "INCONCLUSIVE",
        "verdict_reasoning": (
            "group_order=1 (only 1 sample permutation generated, group did not close). "
            "12 distinct indices but no orbit structure emerged. "
            "S3 action not demonstrated; algorithm reseed or generator-completion needed."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_10_group6_results.json": {
        "verdict": "CONFIRMATION_LOCAL",
        "verdict_reasoning": (
            "exclusion_pattern shows each of 7 orbits excludes exactly one first-index and one second-index "
            "(Z6 substructure on 6-element orbits). "
            "Orbit 1 i^j (XOR) uniform =10; Z6 test gives 3 distinct sums, 2 distinct diffs. "
            "excluded_set_confirms_pattern field present."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "queue_11_xor_results.json": {
        "verdict": "CONFIRMED",
        "verdict_reasoning": (
            "sedenion_mult_xor_match_rate=105/105 (100%). "
            "All 42 ZD pairs produce XOR in {9,10,11,12,13,14,15} (7 unique values, 1 per orbit). "
            "Strong invariant: sedenion multiplication XOR pattern reproduces full orbit structure."
        ),
        "verdict_source": "result-inspection-2026-05-17",
    },
    "verify_mp_mW_results.json": {
        "verdict": "NUMEROLOGY_HOLD",
        "verdict_reasoning": (
            "layer1 rel_diff=39.1% (n_sigma=26.2) — mp/mW=3*256 hypothesis far off observed ratio. "
            "layer3 best_a values arbitrary (e.g., a=462143 for mW/mZ). "
            "Existing taliban_verdict='WARN — partial signatures, needs more work'. "
            "Fitting Detection: post-fit, no pre-registered prediction. "
            "STATUS.md marks as candidate; Fitting Detection now resolves to HOLD."
        ),
        "verdict_source": "STATUS.md ledger 2026-05-14 + result inspection 2026-05-17",
    },
}


def patch(path: pathlib.Path, entry: dict) -> None:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} root is not dict, cannot patch in-place")
    if "verdict" in data:
        print(f"  skip (already has verdict): {path.name}")
        return
    new_data = {
        "verdict": entry["verdict"],
        "verdict_reasoning": entry["verdict_reasoning"],
        "verdict_source": entry["verdict_source"],
        "verdict_date": DATE,
        **data,
    }
    path.write_text(json.dumps(new_data, indent=2, ensure_ascii=False) + "\n")
    print(f"  patched: {path.name} -> {entry['verdict']}")


def main() -> None:
    patched = 0
    for name, entry in VERDICTS.items():
        p = ROOT / name
        if not p.exists():
            print(f"  MISSING: {name}")
            continue
        patch(p, entry)
        patched += 1
    print(f"\ntotal patched: {patched}/{len(VERDICTS)}")


if __name__ == "__main__":
    main()
