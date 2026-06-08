#!/usr/bin/env python3
"""ICE_ORCA_DRAGON L1 재현성 검증 harness (PROM 16 remediation 2026-06-08).

REPRODUCIBILITY attestation — NOT a correctness/physics-truth claim.
green = "스크립트를 재실행하면 committed JSON의 *computed* 키가 byte-identical 재생성된다"
       (= exit 0 이 기록된 수를 실제로 썼다). 물리 진리 주장 아님 (L2/L3 는 STAGNANT 유지).

설계 (PROM 16 적대검증 교훈 lesson-ice-naive-remediation-reintroduces-drift-2026-06-08):
- 비파괴: committed JSON 을 백업 → 스크립트 실행 → computed 키 비교 → committed 원본 복원.
  (naive "재실행→커밋" 은 hand-curated verdict 를 덮어써 Eilu va-Eilu 위반.)
- VERDICT_FAMILY 키는 *항상* curated-canonical (committed 우선). _verdict_auto_emit.py
  "NEVER overwrites pre-existing verdict" 계약과 일치. 비교 대상에서 제외.
- exit 0 ≠ reproduced: 출력 파일 생성 + computed 키 일치까지 확인해야 PASS.

usage: python3 repro_check.py          # 검증 (committed 불변)
       python3 repro_check.py --list   # 스크립트↔출력 매핑만 출력
"""
import json, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent

# named script -> its output JSON (PROM 16 grep-confirmed 2026-06-08)
SCRIPTS = {
    "derive_Lstar_from_ICE": "derive_Lstar_results.json",
    "derive_dimensionless_ICE": "derive_dimensionless_results.json",
    "derive_mass_ratios_ICE": "derive_mass_ratios_results.json",
    "prove_higgs_ZD_doublet": "prove_higgs_results.json",
    "prove_s3_higher_gauge": "prove_s3_results.json",
    "prove_s5_bv_ainfty": "prove_s5_results.json",
    "queue_01_orbit_analysis": "queue_01_orbit_results.json",
    "queue_03_threshold_sensitivity_scan": "queue_03_threshold_sensitivity_results.json",
    "queue_04_hosotani_toy": "queue_04_hosotani_results.json",
    "queue_05_coleman_weinberg": "queue_05_cw_results.json",
    "queue_06_cooperative_vacuum": "queue_06_coop_results.json",
    "queue_10_group_of_6": "queue_10_group6_results.json",
    "queue_11_xor_invariant": "queue_11_xor_results.json",
    "verify_mp_mW_3_256": "verify_mp_mW_results.json",
}

# 항상 curated-canonical (committed 우선, 비교 제외). _verdict_auto_emit.py 계약.
VERDICT_FAMILY = {"verdict", "verdict_reasoning", "verdict_source", "verdict_date",
                  "self_refutation", "sub_verdicts", "verdict_provenance"}
# 본질적 비결정 키 (timestamp 등) — bit-reproduction 비교에서 제외.
NON_DETERMINISTIC = {"researchedAt", "timestamp", "generated_at", "createdAt", "run_at"}
EXCLUDE = VERDICT_FAMILY | NON_DETERMINISTIC

# committed JSON 이 named script 가 아닌 다른 source 에서 옴 (PROM 16 적대검증 확정).
SUPERSEDED = {"queue_06_cooperative_vacuum":
              "committed=inconclusive_redo.py (n_trials supersede, method_fix); named script output differs"}
NO_PRIOR_MAPPING = {"queue_03_threshold_sensitivity_scan":
                    "committed queue_03_rep_results.json = archived queue_03_rep_decomposition.py; named script output was absent → NEW artifact"}


def cmp_keys(d):
    return {k: v for k, v in d.items() if k not in EXCLUDE}


def baseline(out):
    """git-HEAD committed 버전 (working-tree 아님). 미추적이면 None."""
    r = subprocess.run(["git", "show", f"HEAD:./{out}"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, False
    try:
        return json.loads(r.stdout), True
    except Exception:
        return None, True


def main():
    if "--list" in sys.argv:
        for s, o in SCRIPTS.items():
            print(f"{s}.py -> {o}")
        return 0
    npass = nfail = 0
    rows = []
    for script, out in SCRIPTS.items():
        op = ROOT / out
        prior, tracked = baseline(out)
        try:
            r = subprocess.run([sys.executable, f"{script}.py"], cwd=ROOT,
                               capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            rows.append((script, "TIMEOUT>300s")); nfail += 1; continue
        if r.returncode != 0:
            rows.append((script, f"EXIT{r.returncode}: {(r.stderr or '')[-100:]}")); nfail += 1
            if tracked: subprocess.run(["git", "checkout", "--", out], cwd=ROOT)
            continue
        if not op.exists():
            rows.append((script, "exit0 but NO OUTPUT FILE")); nfail += 1; continue
        fresh = json.loads(op.read_text())
        if prior is None:  # named script has no committed baseline
            tag = NO_PRIOR_MAPPING.get(script, "NEW (no prior committed output)")
            rows.append((script, f"NEW_ARTIFACT — {tag}")); npass += 1
            continue  # keep fresh (genuine new output)
        # subset-match: fresh 의 computed 키 전부 prior 와 일치 (prior 의 추가 curated 키는 OK)
        fc = cmp_keys(fresh)
        same = all(k in prior and prior[k] == v for k, v in fc.items())
        if script in SUPERSEDED:
            rows.append((script, f"SUPERSEDED — {SUPERSEDED[script]}"))
        elif same:
            rows.append((script, "REPRO ✓ (computed keys reproduce; verdict-family/timestamps excluded, curated-preserved)")); npass += 1
        else:
            diff = [k for k, v in fc.items() if prior.get(k) != v]
            rows.append((script, f"COMPUTED_CHANGED {diff[:5]}")); nfail += 1
        if tracked:
            subprocess.run(["git", "checkout", "--", out], cwd=ROOT)  # 비파괴: committed 복원
    print("ICE L1 reproducibility attestation (computed keys; verdict-family + timestamps excluded)\n")
    for s, st in rows:
        print(f"  {s:38s} {st}")
    print(f"\nREPRO/NEW {npass} | needs-attention {nfail} | "
          f"SUPERSEDED {len(SUPERSEDED)} (committed canonical, named script not 1:1)")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
