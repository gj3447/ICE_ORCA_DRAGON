"""4-condition custodial diagnostic — empirical test of PROM 16 hypothesis.

PROM 16 (cycle prom16-ice-residual-2026-05-17) hypothesis from f_A2_S4:
  Existing queue_02 tests ONLY condition (iii) = cross-commutator [T_L^a, T_R^b] = 0.
  Three other conditions usually fail FIRST in non-alternative algebras:
    c1: SU(2)_L closure   [T_L^a, T_L^b] = +/- 2 T_L^c
    c2: SU(2)_R closure   [T_R^a, T_R^b] = +/- 2 T_R^c
    c3: cross-commutator  [T_L^a, T_R^b] = 0           (existing test)
    c4: Y consistency     [Y, T_L^a] = 0               (deferred — Y identification non-trivial)
  Prediction: ~70% of triples fail c1 or c2 in projected rep -> 1.93 c3 is symptom not root.

Test: for each of 42 ZD pairs, record c1, c2, c3 residuals + failure pattern.

Verdict criteria (per pair):
  PASS_FULL   = c1, c2, c3 all < 1e-6
  PASS_CLOSED = c1, c2 < 1e-6 but c3 >= 1e-6   (SU(2)'s closed but not custodial-commuting)
  FAIL_CLOSURE = c1 or c2 >= 1e-6              (SU(2) closure already broken)

If FAIL_CLOSURE > 50% of pairs: PROM 16 A2-S4 hypothesis CONFIRMED.

# KG: R1 of prom16-ice-residual ActionPlan, empirical discrimination of paper-bureaucracy risk
"""

from __future__ import annotations

import json
import pathlib
import statistics

import numpy as np
from cd_core import cd_multiply
from scipy.linalg import null_space

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-17"
TOL = 1e-6


def basis(i, dim):
    v = np.zeros(dim); v[i] = 1.0; return v


def mul(a, b, n):
    return cd_multiply(a, b, n)


def build_L(a, n):
    dim = 2**n
    L = np.zeros((dim, dim))
    for k in range(dim):
        L[:, k] = mul(a, basis(k, dim), n)
    return L


def find_ZD_and_null(n=4):
    dim = 2**n
    pairs = []
    for i in range(1, dim):
        for j in range(i + 1, dim):
            a = basis(i, dim) + basis(j, dim)
            L = build_L(a, n)
            ns = null_space(L, rcond=1e-10)
            if ns.shape[1] > 0:
                pairs.append({"i": i, "j": j, "a": a, "ns": ns})
    return pairs


def find_su2_triples(n=4, max_n=40):
    dim = 2**n
    triples = []
    for a in range(1, dim):
        for b in range(a + 1, dim):
            ea, eb = basis(a, dim), basis(b, dim)
            comm = mul(ea, eb, n) - mul(eb, ea, n)
            nz = np.where(np.abs(comm) > 1e-9)[0]
            if len(nz) == 1:
                c = nz[0]
                val = comm[c]
                if abs(abs(val) - 2.0) < 1e-9 and c != a and c != b:
                    t = tuple(sorted([a, b, c]))
                    if t not in [x["idx"] for x in triples]:
                        triples.append({"idx": t, "a": a, "b": b, "c": c})
                        if len(triples) >= max_n:
                            return triples
    return triples


def project_generator_to_null(gen_a, ns, n):
    dim = 2**n
    L = build_L(basis(gen_a, dim), n)
    return ns.T @ L @ ns


def find_invariant_triples(pair, triples, n):
    invariant = []
    for t in triples:
        ok = True
        for gen in [t["a"], t["b"], t["c"]]:
            L = build_L(basis(gen, 2**n), n)
            proj = pair["ns"].T @ L @ pair["ns"]
            reconstructed = pair["ns"] @ proj
            full = L @ pair["ns"]
            if np.max(np.abs(full - reconstructed)) > 1e-7:
                ok = False
                break
        if ok:
            invariant.append(t)
    return invariant


def closure_residual(triple, ns, n):
    """Test if projected (Ma, Mb, Mc) form an SU(2) Lie algebra.

    Ambient: [e_a, e_b] = +/- 2 e_c (and cyclic). Projected should preserve this.
    Returns max residual across the 3 cyclic relations.
    """
    a, b, c = triple["a"], triple["b"], triple["c"]
    dim = 2**n
    Ma = ns.T @ build_L(basis(a, dim), n) @ ns
    Mb = ns.T @ build_L(basis(b, dim), n) @ ns
    Mc = ns.T @ build_L(basis(c, dim), n) @ ns

    def cyclic_check(Mp, Mq, Mr, p, q, r):
        # Ambient [e_p, e_q] = comm_pq; find coefficient on e_r
        comm_pq = mul(basis(p, dim), basis(q, dim), n) - mul(basis(q, dim), basis(p, dim), n)
        coef = comm_pq[r]  # +/-2 or 0
        if abs(coef) < 0.5:
            return None  # ambient relation doesn't close on this triple member
        proj_comm = Mp @ Mq - Mq @ Mp
        expected = coef * Mr
        return float(np.max(np.abs(proj_comm - expected)))

    r1 = cyclic_check(Ma, Mb, Mc, a, b, c)
    r2 = cyclic_check(Mb, Mc, Ma, b, c, a)
    r3 = cyclic_check(Mc, Ma, Mb, c, a, b)
    residuals = [r for r in (r1, r2, r3) if r is not None]
    if not residuals:
        return float("inf")  # ambient relations don't close at all
    return max(residuals)


def cross_commutator(T_L, T_R, ns, n):
    """Existing c3 test."""
    max_norm = 0.0
    dim = 2**n
    for gL in [T_L["a"], T_L["b"], T_L["c"]]:
        for gR in [T_R["a"], T_R["b"], T_R["c"]]:
            ML = ns.T @ build_L(basis(gL, dim), n) @ ns
            MR = ns.T @ build_L(basis(gR, dim), n) @ ns
            comm = ML @ MR - MR @ ML
            max_norm = max(max_norm, float(np.max(np.abs(comm))))
    return max_norm


def main():
    print("\n" + "=" * 60)
    print("R1: queue_02 4-CONDITION DIAGNOSTIC (PROM 16 empirical)")
    print("=" * 60 + "\n")

    n = 4
    pairs = find_ZD_and_null(n)
    triples = find_su2_triples(n)
    print(f"  ZD pairs: {len(pairs)}, SU(2) triples: {len(triples)}")
    print()

    records = []
    for p in pairs:
        inv = find_invariant_triples(p, triples, n)
        if len(inv) < 2:
            continue

        T_L, T_R = inv[0], inv[1]
        c1 = closure_residual(T_L, p["ns"], n)
        c2 = closure_residual(T_R, p["ns"], n)
        c3 = cross_commutator(T_L, T_R, p["ns"], n)

        if c1 < TOL and c2 < TOL and c3 < TOL:
            verdict = "PASS_FULL"
        elif c1 < TOL and c2 < TOL:
            verdict = "PASS_CLOSED_FAIL_CUSTODIAL"
        elif c1 >= TOL and c2 >= TOL:
            verdict = "FAIL_BOTH_CLOSURE"
        elif c1 >= TOL:
            verdict = "FAIL_C1_LEFT_CLOSURE"
        else:
            verdict = "FAIL_C2_RIGHT_CLOSURE"

        records.append({
            "pair": [p["i"], p["j"]],
            "T_L": list(T_L["idx"]),
            "T_R": list(T_R["idx"]),
            "c1_left_closure": c1,
            "c2_right_closure": c2,
            "c3_cross_commutator": c3,
            "verdict": verdict,
        })

    # Aggregate
    verdict_counts = {}
    for r in records:
        verdict_counts[r["verdict"]] = verdict_counts.get(r["verdict"], 0) + 1

    c1_vals = [r["c1_left_closure"] for r in records]
    c2_vals = [r["c2_right_closure"] for r in records]
    c3_vals = [r["c3_cross_commutator"] for r in records]

    def stat_summary(vals):
        return {
            "min": min(vals),
            "median": statistics.median(vals),
            "max": max(vals),
            "mean": statistics.mean(vals),
            "pct_pass": 100 * sum(1 for v in vals if v < TOL) / len(vals),
        }

    summary = {
        "n_pairs_tested": len(records),
        "tolerance": TOL,
        "verdict_distribution": verdict_counts,
        "c1_left_closure_stats": stat_summary(c1_vals),
        "c2_right_closure_stats": stat_summary(c2_vals),
        "c3_cross_commutator_stats": stat_summary(c3_vals),
    }

    # PROM 16 hypothesis test
    pct_closure_fail = 100 * sum(1 for r in records
                                 if r["c1_left_closure"] >= TOL or r["c2_right_closure"] >= TOL) / len(records)
    hypothesis_threshold = 50.0
    if pct_closure_fail >= hypothesis_threshold:
        hypothesis_verdict = "CONFIRMED"
        hypothesis_msg = (
            f"PROM 16 A2-S4 hypothesis CONFIRMED: {pct_closure_fail:.1f}% of pairs "
            f"fail SU(2) closure (c1 or c2 >= {TOL}). The 1.93 cross-commutator is "
            f"a SYMPTOM; root cause is broken closure in projected rep, due to "
            f"sedenion non-alternativity. queue_02 c3-only test was diagnostically incomplete."
        )
    else:
        hypothesis_verdict = "REFUTED"
        hypothesis_msg = (
            f"PROM 16 A2-S4 hypothesis REFUTED: only {pct_closure_fail:.1f}% pairs "
            f"fail closure. Cross-commutator c3 IS the primary failure mode, "
            f"and the PROM 16 prediction of '~70% closure failure' was paper-bureaucracy."
        )

    print(f"  Verdict distribution: {verdict_counts}")
    print(f"  c1 stats: {summary['c1_left_closure_stats']}")
    print(f"  c2 stats: {summary['c2_right_closure_stats']}")
    print(f"  c3 stats: {summary['c3_cross_commutator_stats']}")
    print()
    print(f"  Closure-fail %: {pct_closure_fail:.1f}%")
    print(f"  PROM 16 hypothesis: {hypothesis_verdict}")
    print(f"  Message: {hypothesis_msg}")

    out = {
        "verdict": hypothesis_verdict,
        "verdict_reasoning": hypothesis_msg,
        "verdict_source": "queue_02_4condition_diagnostic.py 2026-05-17 (R1 of prom16-ice-residual)",
        "verdict_date": DATE,
        "prom16_hypothesis_threshold_pct": hypothesis_threshold,
        "empirical_closure_fail_pct": pct_closure_fail,
        "summary": summary,
        "per_pair_records": records,
        "c4_y_consistency": "DEFERRED — Y generator identification in sedenion ambient is non-trivial; defer to follow-up",
        "cycle_ref": "prom16-ice-residual-2026-05-17",
        "actionplan_item": "R1",
    }
    out_path = ROOT / "queue_02_4condition_diagnostic_results.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=lambda o: int(o) if hasattr(o, "item") else str(o)) + "\n")
    print(f"\nResults -> {out_path.name}")
    return out


if __name__ == "__main__":
    main()
