# LONGINUS: sourceId=queue_08_G2_adjoint, sourcePath=queue_08_G2_adjoint.py
"""
Queue 8: G₂ Representation Identification
==========================================
7 orbits가 G₂ fundamental (7-dim) 표현인가?

Test: orbit 대표 7개 원소에 Der(𝕆) = G₂ (14-dim Lie algebra) 작용 행렬 구성.
- Irreducible?
- Casimir eigenvalue → 7-dim rep label
- G₂ fundamental rep Casimir = 2 (정규화 선택에 따라 다름)
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


# 7 orbits 대표 (Q1 결과)
ORBIT_REPS = [
    (1, 11),  # Orbit 1
    (2, 11),  # Orbit 2
    (1, 12),  # Orbit 3
    (1, 10),  # Orbit 4
    (1, 15),  # Orbit 5
    (1, 14),  # Orbit 6
    (1, 13),  # Orbit 7
]


def build_annihilator_vector(pair, dim=16):
    """(i,j) → e_i + e_j"""
    i, j = pair
    return basis(i, dim) + basis(j, dim)


def derivation_action(e_a, e_b, z, n):
    """
    Inner derivation D_{a,b}(z) := [[e_a, e_b], z] - 3*[e_a, e_b, z]
    octonion inner derivation 정규식 (Der(O) = G₂).
    """
    comm_ab = commutator(basis(e_a, 2**n), basis(e_b, 2**n), n)
    part1 = commutator(comm_ab, z, n)
    # Associator [e_a, e_b, z] = (e_a*e_b)*z - e_a*(e_b*z)
    ea, eb = basis(e_a, 2**n), basis(e_b, 2**n)
    ab_z = mul(mul(ea, eb, n), z, n)
    a_bz = mul(ea, mul(eb, z, n), n)
    assoc = ab_z - a_bz
    return part1 - 3 * assoc


def project_to_orbit_reps(vec, orbit_reps, n, threshold=1e-7):
    """
    vec를 7 orbit 대표 annihilator들의 선형 결합으로 분해 + 직교 보정.
    각 orbit rep의 "방향" 성분 계수 추출.
    """
    dim = 2**n
    # orbit rep 벡터들
    basis_vecs = np.array([build_annihilator_vector(p, dim) for p in orbit_reps])
    # 정규화
    basis_norm = basis_vecs / np.linalg.norm(basis_vecs, axis=1, keepdims=True)
    # vec 정사영 계수
    coeffs = basis_norm @ vec
    return coeffs


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 8: G₂ REPRESENTATION IDENTIFICATION")
    print("=" * 60 + "\n")

    n = 4
    dim = 2**n

    # 7 orbit 대표 annihilator
    orbit_vecs = np.array([
        build_annihilator_vector(p, dim) for p in ORBIT_REPS
    ])
    print(f"7 orbit 대표: {ORBIT_REPS}")
    print()

    # G₂ generator: all (a,b) pairs in Im(O) = {e_1, ..., e_7}
    # Der(O) = span{D_{ab} : a<b in Im(O)} with dim 14
    print("[Stage 1] G₂ generators 구성 (Der(O) = 14-dim)...")
    g2_gens = []
    for a in range(1, 8):
        for b in range(a+1, 8):
            g2_gens.append((a, b))
    print(f"  후보 (a,b) 쌍: {len(g2_gens)} → G₂ dim = 14 예상")
    print()

    # 각 generator 작용을 7x7 rep matrix로 표현
    print("[Stage 2] 각 generator의 7x7 rep matrix 구성...")
    rep_matrices = []
    for (a, b) in g2_gens:
        M = np.zeros((7, 7))
        for i, pair in enumerate(ORBIT_REPS):
            v = build_annihilator_vector(pair, dim)
            # D_{ab}(v) 계산
            Dv = derivation_action(a, b, v, n)
            # 7 orbit 대표 방향으로 사영
            coeffs = project_to_orbit_reps(Dv, ORBIT_REPS, n)
            M[:, i] = coeffs
        rep_matrices.append(M)

    # 독립적 generator만 추출 (행렬을 벡터화하여 랭크 계산)
    M_flat = np.array([M.flatten() for M in rep_matrices])
    rank = np.linalg.matrix_rank(M_flat, tol=1e-8)
    print(f"  independent generator 개수 (rank): {rank}")
    print(f"  예상 G₂ dim: 14")
    print()

    # Casimir computation: C² = Σ M_i² (적절 정규화 후)
    print("[Stage 3] Casimir 연산자 계산...")
    # 반대칭 generator 선택: M의 반대칭 부분
    M_antisymmetric = [0.5 * (M - M.T) for M in rep_matrices]
    # Gram-Schmidt 유사: trace inner product로 정규화
    norms = [np.sqrt(np.trace(M @ M.T) + 1e-12) for M in M_antisymmetric]
    M_normalized = [M / nr if nr > 1e-9 else M
                    for M, nr in zip(M_antisymmetric, norms)]

    Casimir = np.zeros((7, 7))
    for M in M_normalized[:14]:  # G₂ generator 14개만 사용
        Casimir += M @ M

    evals = np.linalg.eigvals(Casimir)
    real_evals = sorted(np.real(evals))
    print(f"  Casimir eigenvalues: {[round(e, 4) for e in real_evals]}")
    print()

    # Irreducibility check: commutant dimension
    print("[Stage 4] Irreducibility check...")
    # 모든 generator와 commute하는 matrix space의 dim
    # Schur: irreducible → commutant = scalar multiples of I (dim 1)
    comm_dim = 7 * 7  # 시작
    from numpy.linalg import lstsq
    # 각 generator M에 대해 [X, M] = 0 → vec(X)에 대한 linear constraint
    # 여기선 단순화: 몇 개 generator의 commutant 차원
    identity = np.eye(7)
    # Commutant of the whole G₂: vectorized (generators, 7^2)
    constraint_rows = []
    for M in M_antisymmetric[:14]:
        # [X, M]_ij = 0 constraint for all i,j
        # X_{ik}M_{kj} - M_{ik}X_{kj} = 0
        # kronecker product form: (I ⊗ M^T - M ⊗ I) vec(X) = 0
        kron = np.kron(np.eye(7), M.T) - np.kron(M, np.eye(7))
        constraint_rows.append(kron)
    A = np.vstack(constraint_rows)
    # null space of A
    from scipy.linalg import null_space
    ns = null_space(A, rcond=1e-7)
    commutant_dim = ns.shape[1]
    print(f"  commutant dimension: {commutant_dim}")
    print(f"  (1 = irreducible, >1 = reducible)")
    print()

    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)
    if commutant_dim == 1:
        print(f"  🎯 7-dim IRREDUCIBLE G₂ representation 확인!")
        print(f"     = G₂ fundamental rep (유일한 7-dim irrep)")
        print(f"     → 7 orbits 은 G₂ fundamental weights 에 대응")
    else:
        print(f"  🔶 Commutant dim = {commutant_dim} (irreducible 아님)")
        print(f"     → 더 작은 irrep 분해 가능")

    if abs(real_evals[0] - real_evals[-1]) < 0.1:
        print(f"  Casimir uniform → Single irrep candidate")

    import json
    with open("/Users/lagyeongjun/CD/AGENT/queue_08_g2_results.json", "w") as f:
        json.dump({
            "independent_generators": rank,
            "casimir_evals": [round(float(e), 4) for e in real_evals],
            "commutant_dim": int(commutant_dim),
            "orbit_reps": ORBIT_REPS
        }, f, indent=2, default=str)
    print(f"\nResults → queue_08_g2_results.json")
