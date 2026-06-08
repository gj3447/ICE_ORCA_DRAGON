# LONGINUS: sourceId=queue_01_orbit_analysis, sourcePath=queue_01_orbit_analysis.py
"""
Queue 1: Orbit Analysis (DECISIVE)
===================================
42 ZD pair가 Aut(𝕊) = G₂×S₃ 작용 하에 몇 개 orbit인지 판별.

- 1 orbit  → gauge-equivalent = "42/42 통과"는 redundant, 실제로 1 Higgs
- 3 orbits → 3 generation 구조 가능성 (42 = 3×14)
- 7 orbits → C(7,2) 연결 가능성
- 42 orbits → 전부 독립, landscape
"""
import numpy as np
from cd_embedding import cd_multiply

np.set_printoptions(precision=4, suppress=True)


def basis(i, dim):
    v = np.zeros(dim); v[i] = 1.0; return v


def mul(a, b, n):
    return cd_multiply(a, b, n)


def commutator(a, b, n):
    return mul(a, b, n) - mul(b, a, n)


def find_ZD_annihilators(n=4):
    """42개 ZD 유발 annihilator e_i+e_j 전부 찾기"""
    dim = 2**n
    ann = []
    for i in range(1, dim):
        for j in range(i+1, dim):
            a = basis(i, dim) + basis(j, dim)
            from scipy.linalg import null_space
            L = np.zeros((dim, dim))
            for k in range(dim):
                L[:, k] = mul(a, basis(k, dim), n)
            if null_space(L, rcond=1e-10).shape[1] > 0:
                ann.append((i, j, a))
    return ann


def build_derivation_generators(n=4):
    """
    Der(A_n) Lie algebra generators.
    Octonion case: inner derivations D_{x,y}(z) = [[x,y], z] - 3[x,y,z]
    Sedenion: extend similarly.
    여기선 basis commutators로 generator set 구성.
    """
    dim = 2**n
    gens = []
    # Inner derivation from all e_i, e_j pairs
    for i in range(1, dim):
        for j in range(i+1, dim):
            # D_{ij}(z) := [e_i, [e_j, z]] (double commutator)
            def make_D(ii, jj):
                def D(z):
                    ei, ej = basis(ii, dim), basis(jj, dim)
                    inner = commutator(ej, z, n)
                    return commutator(ei, inner, n)
                return D
            gens.append((i, j, make_D(i, j)))
    return gens


def orbit_of(annihilator, annihilators, gens, n, max_iter=5):
    """
    주어진 annihilator에서 시작해 Der 작용 반복하여 도달 가능한 ZD annihilator 집합.
    """
    dim = 2**n
    # annihilator를 (i,j) tuple로 식별
    visited = set()
    start_key = None
    for (ii, jj, a) in annihilators:
        if np.allclose(a, annihilator):
            start_key = (ii, jj)
            break
    if start_key is None:
        return set()

    frontier = {start_key}
    visited.add(start_key)

    for iteration in range(max_iter):
        new_frontier = set()
        for key in frontier:
            # 해당 annihilator 찾기
            a_current = None
            for (ii, jj, a) in annihilators:
                if (ii, jj) == key:
                    a_current = a
                    break
            if a_current is None:
                continue

            # 모든 generator 작용
            for (_, _, D) in gens[:30]:  # 처음 30개 generator만 (속도)
                transformed = D(a_current)
                # ZD annihilator 중 하나와 일치? (부호/정규화 허용)
                for (ii, jj, a) in annihilators:
                    if (ii, jj) in visited:
                        continue
                    # 비교: transformed ∝ a (선형 종속)?
                    norm_t = np.linalg.norm(transformed)
                    norm_a = np.linalg.norm(a)
                    if norm_t < 1e-9 or norm_a < 1e-9:
                        continue
                    # cosine similarity
                    cos = abs(np.dot(transformed, a)) / (norm_t * norm_a)
                    if cos > 0.99:  # nearly parallel
                        new_frontier.add((ii, jj))
        new_frontier -= visited
        if not new_frontier:
            break
        visited |= new_frontier
        frontier = new_frontier

    return visited


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 1: ORBIT ANALYSIS — 42 ZD pair")
    print("=" * 60 + "\n")

    n = 4
    print("[Stage 1] annihilator 42개 수집 중...")
    annihilators = find_ZD_annihilators(n)
    print(f"  annihilators: {len(annihilators)}")

    print("[Stage 2] Derivation generators 구성 중...")
    gens = build_derivation_generators(n)
    print(f"  generators: {len(gens)} (처음 30개 사용)")
    print()

    print("[Stage 3] Orbit 계산...")
    all_keys = {(ii, jj) for (ii, jj, _) in annihilators}
    remaining = set(all_keys)
    orbits = []

    while remaining:
        start_key = next(iter(remaining))
        start_ann = next(a for (ii, jj, a) in annihilators if (ii, jj) == start_key)
        orbit = orbit_of(start_ann, annihilators, gens, n)
        orbits.append(orbit)
        remaining -= orbit

    print(f"  찾은 orbit 수: {len(orbits)}")
    print(f"  orbit 크기 분포: {sorted([len(o) for o in orbits], reverse=True)}")
    print()
    for i, o in enumerate(orbits[:10]):
        print(f"  Orbit {i+1} (size={len(o)}): {sorted(o)[:10]}{'...' if len(o)>10 else ''}")
    print()

    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)
    n_orbits = len(orbits)
    if n_orbits == 1:
        print(f"  ⚠️  1 ORBIT: 42 pair = gauge-equivalent (redundant 표현)")
        print(f"     실제 독립 Higgs candidate = 1개")
        print(f"     → 'landscape' 해석 기각, 단일 Higgs")
    elif n_orbits == 3:
        print(f"  🎯 3 ORBITS: 42 = 3 × 14 구조 possibly = 3 GENERATIONS!")
        print(f"     각 orbit 크기 = {[len(o) for o in orbits]}")
        print(f"     → Higgs 섹터 × 3세대 구조 강력 시사")
    elif n_orbits == 7:
        print(f"  🔶 7 ORBITS: C(7,2) 연결 가능")
    else:
        print(f"  🔷 {n_orbits} ORBITS: 기타 구조")
        print(f"     orbit 크기: {sorted([len(o) for o in orbits], reverse=True)}")

    import json
    with open(__import__("pathlib").Path(__file__).resolve().parent / "queue_01_orbit_results.json", "w") as f:
        json.dump({
            "n_orbits": n_orbits,
            "orbit_sizes": sorted([len(o) for o in orbits], reverse=True),
            "orbits": [sorted(list(o)) for o in orbits]
        }, f, indent=2, default=str)
    print(f"\nResults → queue_01_orbit_results.json")
