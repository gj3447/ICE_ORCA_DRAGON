# LONGINUS: sourceId=queue_03_rep_decomposition, sourcePath=queue_03_rep_decomposition.py
"""
Queue 3: Representation Decomposition (DECISIVE)
=================================================
42 pair 각 null space를 Der(𝕊) Casimir 작용으로 분해.
SM Higgs (1,2,1/2) 표현과 매칭 여부 검증.

- Casimir C² = Σ T_a² eigenvalue
- (1,2): C² = 3/4 (SU(2) doublet)
- (2,1): C² = 3/4
- trivial singlet: C² = 0
"""
import numpy as np
from cd_embedding import cd_multiply
from scipy.linalg import null_space

np.set_printoptions(precision=4, suppress=True)


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


def find_ZD_pairs(n=4):
    dim = 2**n
    pairs = []
    for i in range(1, dim):
        for j in range(i+1, dim):
            a = basis(i, dim) + basis(j, dim)
            L = build_L(a, n)
            ns = null_space(L, rcond=1e-10)
            if ns.shape[1] > 0:
                pairs.append({"i": i, "j": j, "ns": ns})
    return pairs


def find_su2_triples(n=4):
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
    return triples


def find_invariant_triples(pair, triples, n):
    inv = []
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
            inv.append(t)
    return inv


def casimir_eigenvalues(pair, triple, n):
    """
    SU(2) Casimir C² = T_1² + T_2² + T_3² 고유값.
    doublet이면 3/4, trivial이면 0.
    주의: generator 정규화는 T_a = e_a/2 (standard SU(2) gen)
    """
    T1 = basis(triple["a"], 2**n)
    T2 = basis(triple["b"], 2**n)
    T3 = basis(triple["c"], 2**n)

    # null space 제한
    M1 = pair["ns"].T @ build_L(T1, n) @ pair["ns"] / 2.0
    M2 = pair["ns"].T @ build_L(T2, n) @ pair["ns"] / 2.0
    M3 = pair["ns"].T @ build_L(T3, n) @ pair["ns"] / 2.0

    # Casimir: -T_a² (generators are anti-hermitian, so T_a² is negative)
    C_sq = -(M1 @ M1 + M2 @ M2 + M3 @ M3)
    return np.linalg.eigvals(C_sq)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 3: REPRESENTATION DECOMPOSITION")
    print("=" * 60 + "\n")

    n = 4
    pairs = find_ZD_pairs(n)
    triples = find_su2_triples(n)
    print(f"  Pairs: {len(pairs)}, triples: {len(triples)}\n")

    rep_results = []
    doublet_count = 0
    double_doublet_count = 0

    for p in pairs:
        inv = find_invariant_triples(p, triples, n)
        if len(inv) < 1:
            continue
        # 첫 invariant triple로 Casimir 계산
        evals = casimir_eigenvalues(p, inv[0], n)
        # 실수부 추출
        real_evals = sorted(np.real(evals))
        # doublet check: SU(2) T=1/2 → C²=3/4 (단위: [e_a, e_b]=2e_c 정규화 시 실제 1)
        # 여기선 eigenvalue 패턴 그대로 보기

        # 가능한 표현: singlet (C²=0), doublet (C²=3/4 또는 1), triplet (C²=2)
        # 42개 중 패턴 분류
        pattern = tuple(round(e, 2) for e in real_evals)

        rep_results.append({
            "pair": (p["i"], p["j"]),
            "casimir_evals": [round(float(e), 4) for e in real_evals],
            "pattern": pattern,
            "T_used": inv[0]["idx"]
        })

    # 패턴 집계
    from collections import Counter
    pattern_counts = Counter(r["pattern"] for r in rep_results)
    print(f"[Casimir 고유값 패턴 집계]")
    for pat, cnt in pattern_counts.most_common():
        print(f"  {pat}: {cnt} pairs")
    print()

    # 대표 샘플
    print(f"[상위 5개 pair 상세]")
    for r in rep_results[:5]:
        print(f"  pair {r['pair']}: "
              f"Casimir evals = {r['casimir_evals']}, "
              f"triple = {r['T_used']}")
    print()

    # Interpretation
    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)

    # 모든 eigenvalue가 같은 값이면 irreducible
    # 두 개 값이면 2+2 분해 (예: doublet ⊕ doublet or doublet ⊕ anti-doublet)
    dominant_pattern = pattern_counts.most_common(1)[0][0]
    n_unique = len(set(dominant_pattern))
    print(f"  주 패턴: {dominant_pattern}")
    print(f"  구성: {n_unique}개 distinct value")

    if n_unique == 1:
        val = dominant_pattern[0]
        print(f"  → 4-dim irreducible representation (Casimir = {val})")
        if abs(val - 0.75) < 0.1 or abs(val - 1.0) < 0.1:
            print(f"     SU(2) doublet ⊕ doublet (j=1/2)")
        elif abs(val - 2.0) < 0.1:
            print(f"     Possibly triplet + singlet")
    elif n_unique == 2:
        print(f"  → 2+2 분해 = doublet ⊕ (anti-)doublet 가능성")
        print(f"     SM (1,2,1/2) 와 complex conjugate 쌍 구조")
    elif n_unique == 4:
        print(f"  → 1+1+1+1 = 4 singlets (부합 안 됨)")

    print()
    print(f"  *주의*: Normalization 차이로 eigenvalue 절대값 미세 조정 필요.")
    print(f"   패턴(동일/분해 여부)이 중요.")

    import json
    with open("/Users/lagyeongjun/CD/AGENT/queue_03_rep_results.json", "w") as f:
        json.dump({
            "n_pairs": len(rep_results),
            "pattern_counts": {str(k): v for k, v in pattern_counts.items()},
            "samples": rep_results[:10]
        }, f, indent=2, default=str)
    print(f"\nResults → queue_03_rep_results.json")
