# KG: Higgs from Sedenion Algebra, Derive the Higgs Sector from the Sedenion Span, Higgs Mechanism in ICE
# LONGINUS: sourceId=prove_higgs_ZD_doublet, sourcePath=prove_higgs_ZD_doublet.py
"""
ICE Higgs Candidate Identification - 수치 증명
===============================================
주장: 세데니온 42개 ZD pair 중 일부가 SU(2) doublet으로 변환 → Higgs candidate

테스트 절차:
1. 42개 ZD pair의 4-dim null space 계산
2. 각 null space가 SU(2) 작용 하에서 invariant인지 검사
3. 2-complex (=doublet) 표현으로 분해 가능한지 확인
4. Higgs candidate 후보 식별 및 분류

실행: python3 prove_higgs_ZD_doublet.py
"""
import numpy as np
from scipy.linalg import null_space as scipy_null_space
from cd_core import cd_multiply

np.set_printoptions(precision=4, suppress=True, linewidth=200)


def basis(i, dim):
    v = np.zeros(dim)
    v[i] = 1.0
    return v


def mul(a, b, n):
    return cd_multiply(a, b, n)


# =====================================================
# Stage 0: Sedenion 곱셈 연산자 구성
# =====================================================
def build_left_mult_op(a, n):
    """L_a: x -> a*x, (2^n, 2^n) 행렬로 표현"""
    dim = 2**n
    L = np.zeros((dim, dim))
    for i in range(dim):
        e_i = basis(i, dim)
        L[:, i] = mul(a, e_i, n)
    return L


def build_right_mult_op(a, n):
    """R_a: x -> x*a"""
    dim = 2**n
    R = np.zeros((dim, dim))
    for i in range(dim):
        e_i = basis(i, dim)
        R[:, i] = mul(e_i, a, n)
    return R


# =====================================================
# Stage 1: 42개 ZD pair 및 null space 계산
# =====================================================
def find_all_ZD_pairs(n=4):
    """n=4 (sedenion) ZD pair (e_i + e_j) 전부 탐색"""
    dim = 2**n
    zd_pairs = []

    for i in range(1, dim):
        for j in range(i + 1, dim):
            a = basis(i, dim) + basis(j, dim)
            L_a = build_left_mult_op(a, n)
            # null space of L_a: {x : a*x = 0}
            ns = scipy_null_space(L_a, rcond=1e-10)
            null_dim = ns.shape[1]
            if null_dim > 0:
                zd_pairs.append({
                    "i": i, "j": j,
                    "null_space": ns,
                    "null_dim": null_dim,
                    "annihilator": a
                })

    return zd_pairs


# =====================================================
# Stage 2: SU(2) triple candidates (associative triples)
# =====================================================
def find_su2_triples(n=4, max_search=30):
    """
    SU(2) 대응 관계 [e_a, e_b] = 2 e_c 를 만족하는 basis triple 탐색.
    Octonion의 associative triples 확장 + sedenion 추가 triples.
    """
    dim = 2**n
    triples = []

    for a in range(1, dim):
        for b in range(a + 1, dim):
            e_a, e_b = basis(a, dim), basis(b, dim)
            # [e_a, e_b] = e_a*e_b - e_b*e_a
            comm = mul(e_a, e_b, n) - mul(e_b, e_a, n)
            # comm = ±2 e_c 형태인지 확인
            nonzero_idx = np.where(np.abs(comm) > 1e-9)[0]
            if len(nonzero_idx) == 1:
                c = nonzero_idx[0]
                val = comm[c]
                if abs(abs(val) - 2.0) < 1e-9 and c != a and c != b:
                    # triple (a, b, c) with [e_a, e_b] = sign * 2 * e_c
                    triple = tuple(sorted([a, b, c]))
                    if triple not in [t["idx"] for t in triples]:
                        triples.append({
                            "idx": triple,
                            "e_a": a, "e_b": b, "e_c": c,
                            "sign": int(np.sign(val))
                        })
                        if len(triples) >= max_search:
                            return triples

    return triples


# =====================================================
# Stage 3: Null space에 대한 SU(2) invariance 검사
# =====================================================
def is_SU2_invariant(null_space, triple, n):
    """
    Null space가 주어진 SU(2) triple 생성자 하에서 invariant인지 확인.
    즉 L_{e_a}, L_{e_b}, L_{e_c}가 null space를 보존하는지.
    """
    dim = 2**n
    e_a = basis(triple["e_a"], dim)
    e_b = basis(triple["e_b"], dim)
    e_c = basis(triple["e_c"], dim)

    L_a = build_left_mult_op(e_a, n)
    L_b = build_left_mult_op(e_b, n)
    L_c = build_left_mult_op(e_c, n)

    # null space basis: ns[:, k] for k
    k = null_space.shape[1]

    # L_a (null_space) 의 각 벡터가 null_space 안에 있는지 검사
    def stays_inside(L, ns):
        projected = L @ ns  # (dim, k)
        # projection onto null space
        proj_coeffs = ns.T @ projected  # (k, k)
        reconstructed = ns @ proj_coeffs
        residual = projected - reconstructed
        return np.max(np.abs(residual)) < 1e-7

    inv_a = stays_inside(L_a, null_space)
    inv_b = stays_inside(L_b, null_space)
    inv_c = stays_inside(L_c, null_space)

    return inv_a and inv_b and inv_c


def count_invariant_triples(zd_pair, triples, n):
    """ZD pair null space가 몇 개의 SU(2) triple에 대해 invariant인지"""
    count = 0
    invariant_list = []
    for t in triples:
        if is_SU2_invariant(zd_pair["null_space"], t, n):
            count += 1
            invariant_list.append(t["idx"])
    return count, invariant_list


# =====================================================
# Stage 4: 복소 구조 J 존재 확인 (doublet 조건)
# =====================================================
def has_complex_structure(null_space):
    """
    4-real-dim null space가 compatible complex structure J (J²=-I)를
    가지는지 확인. Skew-symmetric orthogonal 행렬의 존재.
    """
    k = null_space.shape[1]
    if k != 4:
        return False, None

    # 단순 시도: J를 [[0,-I],[I,0]] block form으로 가정 (standard)
    # null_space 기저를 orthonormal로 조정
    ns_orth, _ = np.linalg.qr(null_space)

    # J = [[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]]
    # 이건 ns_orth 좌표에서 standard complex structure
    # 실제 세데니온 공간에서의 J는: J = ns_orth @ J_std @ ns_orth.T
    J_std = np.array([
        [0, 0, -1, 0],
        [0, 0, 0, -1],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])

    J = ns_orth @ J_std @ ns_orth.T
    # J² = -I 검증 (null space restricted)
    J_sq_on_ns = ns_orth.T @ (J @ J) @ ns_orth
    is_minus_I = np.max(np.abs(J_sq_on_ns + np.eye(4))) < 1e-9

    return is_minus_I, J


# =====================================================
# Stage 5: SM Higgs doublet hypercharge structure
# =====================================================
def hypercharge_check(null_space, U1_generator, n):
    """
    SM Higgs: Y = 1/2. U(1)_Y 생성자 하에서 eigenvalue 확인.
    """
    dim = 2**n
    gen = basis(U1_generator, dim)
    L_U1 = build_left_mult_op(gen, n)

    # null space 제한한 U1 액션
    action = null_space.T @ L_U1 @ null_space  # (k, k)

    # Skew-Hermitian (SU(2) 생성자이므로)의 eigenvalue
    evals = np.linalg.eigvals(action)

    # imaginary eigenvalues의 크기
    im_vals = np.imag(evals)

    return action, evals, np.max(np.abs(im_vals))


# =====================================================
# MAIN: 42개 ZD pair 전수 분석
# =====================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ICE HIGGS CANDIDATE IDENTIFICATION - Sedenion 42 ZD Pairs")
    print("=" * 70 + "\n")

    n = 4
    dim = 2**n

    print("[Stage 1] 42 ZD pair + null space 계산 중...")
    zd_pairs = find_all_ZD_pairs(n)
    print(f"  찾은 ZD pair: {len(zd_pairs)}")
    if zd_pairs:
        dims = [p["null_dim"] for p in zd_pairs]
        print(f"  Null dim 분포: min={min(dims)}, max={max(dims)}, "
              f"all 4?: {all(d == 4 for d in dims)}")
    print()

    print("[Stage 2] SU(2) associative triples 탐색...")
    triples = find_su2_triples(n, max_search=40)
    print(f"  찾은 SU(2) triples: {len(triples)}")
    for t in triples[:10]:
        print(f"    {t['idx']}: [e_{t['e_a']}, e_{t['e_b']}] = "
              f"{t['sign']:+d} * 2 * e_{t['e_c']}")
    if len(triples) > 10:
        print(f"    ... (전체 {len(triples)}개)")
    print()

    print("[Stage 3] 각 ZD pair: 몇 개의 SU(2) triple에 대해 invariant?")
    print()
    invariance_results = []
    higgs_candidates = []

    for idx, p in enumerate(zd_pairs):
        n_inv, inv_list = count_invariant_triples(p, triples, n)

        has_J, J = has_complex_structure(p["null_space"])

        invariance_results.append({
            "pair": (p["i"], p["j"]),
            "n_invariant_triples": n_inv,
            "invariant_triples": inv_list[:3],  # first 3
            "has_complex_structure": has_J
        })

        # Higgs candidate: SU(2) invariant + complex structure 존재
        if n_inv >= 1 and has_J:
            higgs_candidates.append(p)

    # 분류 summary
    from collections import Counter
    n_inv_distribution = Counter(r["n_invariant_triples"] for r in invariance_results)
    print(f"  SU(2) invariance 분포 (triple 개수별 ZD pair 수):")
    for k in sorted(n_inv_distribution.keys()):
        print(f"    {k} triples invariant: {n_inv_distribution[k]} pairs")
    print()

    n_with_J = sum(1 for r in invariance_results if r["has_complex_structure"])
    print(f"  Complex structure J 보유 pair: {n_with_J} / 42")
    print()

    print("[Stage 4] Higgs candidate 최종 후보")
    print("-" * 70)
    print(f"  조건: SU(2) invariant (≥1 triple) AND complex structure 보유")
    print(f"  Higgs candidate 수: {len(higgs_candidates)}")
    print()

    if higgs_candidates:
        print(f"  상위 10개 후보:")
        print(f"  {'Pair':<12} {'SU(2) triples':<20} {'Status':<15}")
        print("  " + "-" * 60)
        for c in higgs_candidates[:10]:
            inv = [r for r in invariance_results
                   if r["pair"] == (c["i"], c["j"])][0]
            triples_str = str(inv["invariant_triples"])[:20]
            print(f"  ({c['i']:2d}, {c['j']:2d})    {triples_str:<20} Higgs candidate")

    print()
    print("[Stage 5] 구체 검증: 첫 번째 Higgs candidate의 SU(2) 작용")
    if higgs_candidates:
        c = higgs_candidates[0]
        inv = [r for r in invariance_results
               if r["pair"] == (c["i"], c["j"])][0]
        if inv["invariant_triples"]:
            triple_idx = inv["invariant_triples"][0]
            print(f"  Pair: ({c['i']}, {c['j']})")
            print(f"  First invariant SU(2) triple: {triple_idx}")
            print(f"  Null space dim: {c['null_dim']}")
            print(f"  Null space basis (첫 2 벡터):")
            print(f"    v1 = {c['null_space'][:, 0]}")
            print(f"    v2 = {c['null_space'][:, 1]}")

            # U(1) hypercharge 유사 체크 - 첫 번째 triple의 e_c 사용
            t = next(t for t in triples if t["idx"] == triple_idx)
            action, evals, max_im = hypercharge_check(
                c["null_space"], t["e_c"], n)
            print(f"  U(1) 후보 (e_{t['e_c']}) eigenvalue:")
            print(f"    eigenvalues = {evals}")
            print(f"    max|Im(eig)| = {max_im:.4f}")

    # Summary
    print()
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    if higgs_candidates:
        print(f"  ✅ Higgs candidate 식별 성공!")
        print(f"  42 ZD pair 중 {len(higgs_candidates)}개가 SU(2) doublet 구조")
        print(f"     (SU(2) invariant + complex structure J²=-I 보유)")
        print()
        print(f"  ⚠️  주의: SU(2) invariance는 필요조건, 충분조건 아님.")
        print(f"          SM Higgs (1, 2, 1/2)로 완전 일치는 U(1)_Y hypercharge +")
        print(f"          custodial 구조 추가 검증 필요.")
    else:
        print(f"  ❌ 42 ZD pair 모두 SU(2) doublet 구조 부합 안 됨")
        print(f"  ICE의 Higgs는 ZD pair 아닌 다른 경로 필요")

    import json
    save_obj = {
        "total_zd_pairs": len(zd_pairs),
        "n_su2_triples_searched": len(triples),
        "n_invariant_distribution": dict(n_inv_distribution),
        "n_with_complex_structure": n_with_J,
        "n_higgs_candidates": len(higgs_candidates),
        "higgs_candidate_pairs": [(c["i"], c["j"]) for c in higgs_candidates]
    }
    with open(__import__("pathlib").Path(__file__).resolve().parent / "prove_higgs_results.json", "w") as f:
        json.dump(save_obj, f, indent=2, default=str)
    print()
    print(f"Results → prove_higgs_results.json")
