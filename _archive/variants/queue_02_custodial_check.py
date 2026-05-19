# LONGINUS: sourceId=queue_02_custodial_check, sourcePath=queue_02_custodial_check.py
"""
Queue 2: Custodial SU(2)_R Check
=================================
42 pair 각각이 2 invariant SU(2) triple 보유 →
첫 번째 = SU(2)_L, 두 번째 = SU(2)_R?
[T_L^a, T_R^b] = 0 (독립성) 수치 검증.

성공 시: ρ parameter = 1 자동 보존 → 실험(1.00038) 부합
"""
import numpy as np
from cd_embedding import cd_multiply
from scipy.linalg import null_space

np.set_printoptions(precision=3, suppress=True)


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
        for j in range(i+1, dim):
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
        for b in range(a+1, dim):
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
    """generator e_a의 null space 상 행렬 표현 (k, k)"""
    dim = 2**n
    L = build_L(basis(gen_a, dim), n)
    return ns.T @ L @ ns


def find_invariant_triples(pair, triples, n):
    """해당 pair가 invariant인 SU(2) triples"""
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


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 2: CUSTODIAL SU(2)_R CHECK")
    print("=" * 60 + "\n")

    n = 4
    pairs = find_ZD_and_null(n)
    triples = find_su2_triples(n)
    print(f"  ZD pairs: {len(pairs)}, SU(2) triples: {len(triples)}")
    print()

    custodial_success = 0
    custodial_fail = 0
    commutator_stats = []

    for p in pairs:
        inv = find_invariant_triples(p, triples, n)
        if len(inv) < 2:
            continue

        # 첫 두 triple = L, R candidate
        T_L, T_R = inv[0], inv[1]

        # [T_L^a, T_R^a'] 모든 조합 체크
        max_commutator_norm = 0.0
        for gL in [T_L["a"], T_L["b"], T_L["c"]]:
            for gR in [T_R["a"], T_R["b"], T_R["c"]]:
                ML = project_generator_to_null(gL, p["ns"], n)
                MR = project_generator_to_null(gR, p["ns"], n)
                comm = ML @ MR - MR @ ML
                norm = np.max(np.abs(comm))
                if norm > max_commutator_norm:
                    max_commutator_norm = norm

        commutator_stats.append({
            "pair": (p["i"], p["j"]),
            "T_L": T_L["idx"], "T_R": T_R["idx"],
            "max_commutator": float(max_commutator_norm),
            "custodial": max_commutator_norm < 1e-6
        })

        if max_commutator_norm < 1e-6:
            custodial_success += 1
        else:
            custodial_fail += 1

    print(f"[결과]")
    print(f"  Custodial 성공 (commutator = 0): {custodial_success}/42")
    print(f"  Custodial 실패 (commutator ≠ 0): {custodial_fail}/42")
    print()
    print(f"  Max commutator norm 분포:")
    vals = [s["max_commutator"] for s in commutator_stats]
    print(f"    min:  {min(vals):.2e}")
    print(f"    max:  {max(vals):.2e}")
    print(f"    mean: {np.mean(vals):.2e}")
    print()
    print(f"  상위 5개 샘플:")
    for s in commutator_stats[:5]:
        mark = "✅" if s["custodial"] else "❌"
        print(f"    {mark} pair {s['pair']}: T_L={s['T_L']} T_R={s['T_R']} "
              f"max|comm|={s['max_commutator']:.2e}")

    print()
    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)
    if custodial_success == 42:
        print(f"  🎯 Custodial SU(2)_L × SU(2)_R 완전 확인!")
        print(f"     [T_L, T_R] = 0 for all 42 pairs")
        print(f"     ρ parameter = 1 자동 보존 → 실험 1.00038 부합")
    elif custodial_success > 0:
        print(f"  🔶 부분 custodial: {custodial_success}/42")
        print(f"     custodial 되는 pair vs 안 되는 pair 구조 차이 존재")
    else:
        print(f"  ❌ Custodial 없음")
        print(f"     두 triple이 독립 SU(2)_L, SU(2)_R 아님")

    import json
    with open("/Users/lagyeongjun/CD/AGENT/queue_02_custodial_results.json", "w") as f:
        json.dump({
            "n_success": custodial_success,
            "n_fail": custodial_fail,
            "stats": commutator_stats
        }, f, indent=2, default=str)
    print(f"\nResults → queue_02_custodial_results.json")
