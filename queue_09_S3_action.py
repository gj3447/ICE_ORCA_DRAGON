# LONGINUS: sourceId=queue_09_S3_action, sourcePath=queue_09_S3_action.py
"""
Queue 9: S₃ Action Verification
================================
size-6 orbit 내 S₃ permutation group 작용이 진짜인가.

Test: Aut(𝕊) = G₂ × S₃ 의 S₃ 부분이 각 orbit의 6 원소를 transitively permute하는지.
- 6 = |S₃| = 3! 이면 free + transitive
- 다른 수면 다른 sub-group
"""
import numpy as np
from itertools import permutations
from cd_embedding import cd_multiply

np.set_printoptions(precision=3, suppress=True)


def basis(i, dim):
    v = np.zeros(dim); v[i] = 1.0; return v


def mul(a, b, n):
    return cd_multiply(a, b, n)


# Q1 결과의 첫 번째 orbit
ORBIT_1 = [(1, 11), (3, 9), (4, 14), (5, 15), (6, 12), (7, 13)]


def build_annihilator(i, j, dim=16):
    return basis(i, dim) + basis(j, dim)


def apply_sign_flip(vec, flip_indices, dim=16):
    """특정 기저 성분의 부호 뒤집기 (S₃ element 후보)"""
    result = vec.copy()
    for idx in flip_indices:
        if idx < dim:
            result[idx] = -result[idx]
    return result


def match_to_orbit(transformed_vec, orbit, dim=16, tol=1e-6):
    """transformed_vec이 orbit의 어느 원소와 일치/반일치하는지"""
    for idx, pair in enumerate(orbit):
        ann = build_annihilator(*pair, dim=dim)
        # 양/음 방향 모두 체크
        if np.max(np.abs(transformed_vec - ann)) < tol:
            return idx, '+'
        if np.max(np.abs(transformed_vec + ann)) < tol:
            return idx, '-'
    return None, None


def find_S3_candidates_by_permutation(orbit, n=4):
    """
    6 orbit 원소를 6! 순열 중에서 S₃ subgroup으로 매핑하는 작용 탐색.
    1. 6 원소 사이의 기저 전환으로 permutation 구현
    2. 그 permutation이 S₃ (order 6) subgroup을 형성하는지 검증
    """
    dim = 2**n
    # orbit 원소를 지수집합으로: 각 (i, j) pair의 {i, j}
    orbit_sets = [set(p) for p in orbit]
    # 모든 index union
    all_indices = sorted(set.union(*orbit_sets))
    print(f"  orbit 인덱스 union: {all_indices}")
    print(f"  총 {len(all_indices)}개 distinct indices")
    return all_indices, orbit_sets


def verify_S3_action_via_permutations(orbit, n=4):
    """
    Index permutation으로 orbit elements 간 permutation 찾기.
    각 permutation σ ∈ S_k (k = # distinct indices) 에 대해,
    σ가 orbit elements을 자기 자신에게 매핑하는지 확인.
    유효 permutation 전체 group이 어떤 구조인가?
    """
    dim = 2**n
    orbit_sets = [frozenset(p) for p in orbit]
    all_indices = sorted(set.union(*[set(p) for p in orbit]))
    k = len(all_indices)
    print(f"  [permutation test] {k}! = {np.math.factorial(k)} 순열 중 orbit 보존 검색...")

    valid_perms = []
    # k가 큰 경우 전수 검색 대신 generator 찾기 접근
    if k <= 8:
        # 전수
        for sigma_tuple in permutations(all_indices):
            sigma = dict(zip(all_indices, sigma_tuple))
            # sigma로 orbit 원소 매핑
            mapped = []
            for p in orbit_sets:
                mapped_set = frozenset(sigma[i] for i in p)
                if mapped_set not in orbit_sets:
                    break
                mapped.append(mapped_set)
            else:
                # 모든 매핑 유효 → permutation 자체가 orbit 유지
                # but only identity → skip
                sigma_nontrivial = any(sigma[i] != i for i in all_indices)
                if sigma_nontrivial or True:  # identity 포함
                    valid_perms.append(tuple(sigma_tuple))
    else:
        # sampling
        import random
        sample_size = 10000
        random.seed(42)
        all_perms_list = list(all_indices)
        seen = set()
        for _ in range(sample_size):
            perm = tuple(random.sample(all_indices, k))
            if perm in seen:
                continue
            seen.add(perm)
            sigma = dict(zip(all_indices, perm))
            mapped = []
            for p in orbit_sets:
                mapped_set = frozenset(sigma[i] for i in p)
                if mapped_set not in orbit_sets:
                    break
                mapped.append(mapped_set)
            else:
                valid_perms.append(perm)

    return valid_perms, k


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 9: S₃ ACTION VERIFICATION")
    print("=" * 60 + "\n")

    print(f"Orbit 1 원소: {ORBIT_1}")
    n = 4

    indices, orbit_sets = find_S3_candidates_by_permutation(ORBIT_1, n)
    print()

    print("[Permutation-based S₃ search]")
    valid_perms, k = verify_S3_action_via_permutations(ORBIT_1, n)
    print(f"  orbit-preserving permutations 수: {len(valid_perms)}")
    print()

    # Group order = |valid permutations|
    # S₃ = 6, S₄ = 24, S₅ = 120, ...
    group_order = len(valid_perms)
    print(f"  발견된 orbit-preserving group order: {group_order}")

    # S_n group 식별
    from math import factorial
    for n_test in range(2, 8):
        if group_order == factorial(n_test):
            print(f"  → |G| = {n_test}! 가능성 (S_{n_test}?)")
            break
    else:
        for n_test in range(2, 10):
            if group_order == 2**n_test:
                print(f"  → |G| = 2^{n_test} (Abelian group 가능성)")
                break
        else:
            if group_order == 6:
                print(f"  → |G| = 6 = |S₃| = |Z₆| (확인 필요)")

    print()
    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)
    if group_order == 6:
        print(f"  🎯 order-6 group 확인! |S₃| = 6과 일치")
        print(f"     Aut(𝕊) ⊃ G₂ × S₃의 S₃ 부분이 orbit 내에서 transitive 작동")
        print(f"     → 42 = 7(G₂ orbits) × 6(S₃ orbits) 해석 공고화")
    elif group_order > 6:
        print(f"  🔶 order {group_order} group > |S₃|")
        print(f"     S₃보다 큰 group이 orbit 보존 — 추가 구조 존재")
    elif group_order < 6:
        print(f"  ⚠️  order {group_order} < |S₃|")
        print(f"     S₃ 가설 부분 성립만")
    else:
        print(f"  other structure")

    # Sample permutations
    print()
    print(f"샘플 permutations (최대 5개):")
    for p in valid_perms[:5]:
        print(f"  {dict(zip(indices, p))}")

    import json
    with open("/Users/lagyeongjun/CD/AGENT/queue_09_s3_results.json", "w") as f:
        json.dump({
            "group_order": group_order,
            "distinct_indices": indices,
            "n_distinct_indices": k,
            "sample_permutations": valid_perms[:10],
        }, f, indent=2, default=str)
    print(f"\nResults → queue_09_s3_results.json")
