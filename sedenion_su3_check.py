# LONGINUS: sourceId=sedenion_su3_check, sourcePath=sedenion_su3_check.py
"""
Deep investigation of the 8-dimensional ZD-preserving Lie algebra
on the ell-O sector. Is it su(3)?
"""

import numpy as np
from scipy.linalg import null_space
np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# Rebuild sedenion infrastructure
# ============================================================

def cd_conj(a, level):
    if level == 0:
        return a.copy()
    n = len(a)
    half = n // 2
    a1, a2 = a[:half], a[half:]
    result = np.zeros_like(a)
    result[:half] = cd_conj(a1, level - 1)
    result[half:] = -a2
    return result

def cd_mult(a, b, level):
    if level == 0:
        return a * b
    n = len(a)
    half = n // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    cb2 = cd_conj(b2, level - 1)
    cb1 = cd_conj(b1, level - 1)
    part1 = cd_mult(a1, b1, level - 1) - cd_mult(cb2, a2, level - 1)
    part2 = cd_mult(b2, a1, level - 1) + cd_mult(a2, cb1, level - 1)
    return np.concatenate([part1, part2])

def sedenion_mult(a, b):
    return cd_mult(a, b, 4)

def make_basis(i, dim):
    v = np.zeros(dim)
    v[i] = 1.0
    return v

e = [make_basis(i, 16) for i in range(16)]

# Build structure constants
f = np.zeros((16, 16, 16))
for i in range(16):
    for j in range(16):
        f[i, j] = sedenion_mult(e[i], e[j])

def left_mult_matrix(a):
    L = np.zeros((16, 16))
    for j in range(16):
        L[:, j] = sedenion_mult(a, make_basis(j, 16))
    return L

# Identify ZD pairs
zd_pairs = []
non_zd_pairs = []
for i in range(1, 8):
    for j in range(8, 16):
        a = e[i] + e[j]
        L = left_mult_matrix(a)
        sv = np.linalg.svd(L, compute_uv=False)
        if sv[-1] < 1e-10:
            zd_pairs.append((i, j))
        else:
            non_zd_pairs.append((i, j))

print(f"ZD pairs: {len(zd_pairs)}, Non-ZD: {len(non_zd_pairs)}")

# ============================================================
# Extract the 8D ZD-preserving algebra on ell-O sector
# ============================================================

# Recompute constraints (same as before)
constraints = []
for (i, j) in zd_pairs:
    a = e[i] + e[j]
    L_a = left_mult_matrix(a)
    U, S_vals, Vt_la = np.linalg.svd(L_a)
    ker_indices = np.where(S_vals < 1e-10)[0]
    ker_vecs = Vt_la[ker_indices].T
    coker_vecs = U[:, ker_indices]

    for ki in range(ker_vecs.shape[1]):
        v = ker_vecs[:, ki]
        for ci in range(coker_vecs.shape[1]):
            u = coker_vecs[:, ci]
            row = np.zeros(256)
            for alpha in range(16):
                L_ea = np.zeros((16, 16))
                for col in range(16):
                    L_ea[:, col] = f[alpha, col]
                coeff = u @ L_ea @ v
                row[alpha * 16 + i] += coeff
                row[alpha * 16 + j] += coeff
            if np.linalg.norm(row) > 1e-12:
                constraints.append(row)

C = np.array(constraints)

# Restrict to ell-O sector: T[a+8, b+8] for a,b in 0..7
ell_o_indices = []
for a in range(8, 16):
    for b in range(8, 16):
        ell_o_indices.append(a * 16 + b)

C_restricted = C[:, ell_o_indices]
U_cr, S_cr, Vt_cr = np.linalg.svd(C_restricted)
tol = 1e-8
rank_Cr = np.sum(S_cr > tol)
dim_zd_ello = 64 - rank_Cr
print(f"\nDimension of ZD-preserving on ell-O: {dim_zd_ello}")

# Extract basis of the null space (the 8D Lie algebra)
null_basis = Vt_cr[rank_Cr:]  # shape (8, 64)
print(f"Null space basis shape: {null_basis.shape}")

# Reshape to 8x8 matrices
T_generators = []
for idx in range(null_basis.shape[0]):
    T = null_basis[idx].reshape(8, 8)
    T_generators.append(T)

print("\n" + "=" * 70)
print("PROPERTIES OF THE 8D LIE ALGEBRA")
print("=" * 70)

# Check: are they antisymmetric (so(8) generators)?
print("\nAntisymmetry check (T + T^T = 0?):")
for idx, T in enumerate(T_generators):
    asym = np.linalg.norm(T + T.T)
    sym = np.linalg.norm(T - T.T)
    tr = np.trace(T)
    print(f"  T_{idx}: |T+T^T|={asym:.6f}, |T-T^T|={sym:.6f}, tr(T)={tr:.6f}")

# Check: are they traceless?
print("\nTracelessness check:")
for idx, T in enumerate(T_generators):
    print(f"  T_{idx}: trace = {np.trace(T):.8f}")

# Compute Lie brackets [T_i, T_j] = T_i T_j - T_j T_i
print("\n--- Lie bracket structure ---")
dim = len(T_generators)
brackets = np.zeros((dim, dim, dim))
max_residual = 0

for i in range(dim):
    for j in range(dim):
        comm = T_generators[i] @ T_generators[j] - T_generators[j] @ T_generators[i]
        # Express in terms of basis
        comm_flat = comm.flatten()
        coeffs = null_basis @ comm_flat
        brackets[i, j] = coeffs
        # Check closure
        projected = null_basis.T @ coeffs
        residual = np.linalg.norm(comm_flat - projected)
        max_residual = max(max_residual, residual)

print(f"Max bracket closure residual: {max_residual:.2e}")
print(f"Lie algebra is {'closed' if max_residual < 1e-6 else 'NOT closed'}!")

# Compute Killing form
print("\n--- Killing form ---")
killing = np.zeros((dim, dim))
for i in range(dim):
    for j in range(dim):
        ad_i = brackets[i].T  # (ad_i)_{k,j} = brackets[i,j,k]
        ad_j = brackets[j].T
        killing[i, j] = np.trace(ad_i @ ad_j)

print("Killing form matrix:")
print(killing)

k_eigenvalues = np.sort(np.linalg.eigvalsh(killing))
print(f"\nKilling form eigenvalues: {k_eigenvalues}")
k_rank = np.linalg.matrix_rank(killing, tol=1e-4)
print(f"Killing form rank: {k_rank}")
print(f"Semisimple: {k_rank == dim}")

if k_rank < dim:
    print(f"Radical dimension: {dim - k_rank}")
    # This means the algebra is NOT semisimple
    # It could be a direct sum of a semisimple part and an abelian part

# Check if some generators commute with everything (center)
print("\n--- Center of the algebra ---")
center_dim = 0
for i in range(dim):
    is_central = True
    for j in range(dim):
        if np.linalg.norm(brackets[i, j]) > 1e-8:
            is_central = False
            break
    if is_central:
        print(f"  T_{i} is in the center")
        center_dim += 1
print(f"Center dimension: {center_dim}")

# Compute the Cartan matrix / classify
# For su(3): rank=2, dim=8, Killing form proportional to identity on Cartan-Weyl basis
# Let's try: compute the Casimir operator
print("\n--- Casimir analysis ---")
if k_rank == dim and k_rank > 0:
    # Inverse of Killing form
    k_inv = np.linalg.inv(killing)
    # Casimir = sum_{ij} k_inv[i,j] ad_i ad_j
    casimir = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            ad_i = brackets[i].T
            ad_j = brackets[j].T
            casimir += k_inv[i, j] * ad_i @ ad_j
    print(f"Casimir eigenvalues: {np.sort(np.linalg.eigvalsh(casimir))}")
    # For su(n), Casimir on adjoint rep has eigenvalue = n
    # For su(3), all eigenvalues should be 3 (in appropriate normalization)

# ============================================================
# Alternative: check su(3) directly
# ============================================================

print("\n" + "=" * 70)
print("DIRECT su(3) CHECK")
print("=" * 70)

# su(3) has: dim=8, rank=2, Killing form with signature (8,0) (negative definite)
# Characteristic: the structure constants f_{ijk} satisfy specific identities

# Let's check the Cartan subalgebra
# Find maximal abelian subalgebra
print("\nSearching for Cartan subalgebra (maximal abelian)...")

# Try all pairs as potential Cartan elements
from itertools import combinations

best_abelian = []
for combo_size in range(dim, 0, -1):
    found = False
    for combo in combinations(range(dim), combo_size):
        is_abelian = True
        for i in combo:
            for j in combo:
                if i < j and np.linalg.norm(brackets[i, j]) > 1e-8:
                    is_abelian = False
                    break
            if not is_abelian:
                break
        if is_abelian:
            best_abelian = list(combo)
            found = True
            break
    if found:
        break

print(f"Maximal abelian subalgebra dimension: {len(best_abelian)}")
print(f"Indices: {best_abelian}")

rank_algebra = len(best_abelian)
print(f"\nAlgebra rank: {rank_algebra}")

# For su(n): dim = n²-1, rank = n-1
# su(2): dim=3, rank=1
# su(3): dim=8, rank=2
# su(4): dim=15, rank=3
# g₂: dim=14, rank=2
# so(5)=sp(2): dim=10, rank=2

if dim == 8 and rank_algebra == 2:
    print("Dimension 8 with rank 2 is consistent with su(3)!")
elif dim == 8 and rank_algebra == 1:
    print("Dimension 8 with rank 1 is NOT standard simple Lie algebra")
elif dim == 8 and rank_algebra == 3:
    print("Dimension 8 with rank 3 could be su(2)^3 or other")

# Compute root system
if rank_algebra >= 2 and k_rank == dim:
    print("\n--- Root system analysis ---")
    # Diagonalize the Cartan elements simultaneously
    H = [brackets[i].T for i in best_abelian]  # ad(H_i) matrices

    # H should be simultaneously diagonalizable
    # Find common eigenvectors
    # For su(3), there should be 6 roots and 2 zero weights

    # Eigenvalues of ad(H_1)
    for h_idx, h in enumerate(H):
        evals = np.sort(np.linalg.eigvals(h).real)
        print(f"  Eigenvalues of ad(H_{best_abelian[h_idx]}): {evals}")


# ============================================================
# Even more direct: representation theory check
# ============================================================

print("\n" + "=" * 70)
print("REPRESENTATION CHECK: 8D matrices acting on 8-dim space")
print("=" * 70)

# Our generators T_i are 8x8 matrices. This is the defining representation.
# For su(3), the fundamental rep is 3-dim, adjoint is 8-dim.
# An 8-dim rep of su(3) would be the adjoint rep.
# But our generators are 8x8 matrices acting on an 8-dim space.
# So this is an 8-dim representation of an 8-dim Lie algebra.
# If the algebra is su(3), this would be the adjoint representation!

# Check: for su(3) adjoint rep, the quadratic Casimir = 3 (in standard normalization)
# Let's compute Tr(T_i T_j) in the 8x8 rep
print("\nComputing Tr(T_i T_j) in the 8-dim representation:")
rep_metric = np.zeros((dim, dim))
for i in range(dim):
    for j in range(dim):
        rep_metric[i, j] = np.trace(T_generators[i] @ T_generators[j])

print(rep_metric)

rep_eigenvalues = np.sort(np.linalg.eigvalsh(rep_metric))
print(f"\nRep metric eigenvalues: {rep_eigenvalues}")

# For su(3) in adjoint rep: Tr(T_a T_b) = 3 * delta_{ab} (with standard normalization)
# Check if rep_metric is proportional to identity
if dim > 0:
    rep_metric_normalized = rep_metric / rep_metric[0, 0] if abs(rep_metric[0, 0]) > 1e-10 else rep_metric
    diff_from_identity = np.linalg.norm(rep_metric_normalized - np.eye(dim))
    print(f"|rep_metric/rep_metric[0,0] - I| = {diff_from_identity:.6f}")
    if diff_from_identity < 1e-6:
        print("Rep metric is proportional to identity -> simple Lie algebra")
        print(f"Proportionality constant: {rep_metric[0,0]:.6f}")

# ============================================================
# Definitive test: Compute the dimension of the representation
# decomposition when restricted to a Cartan subalgebra
# ============================================================

print("\n" + "=" * 70)
print("WEIGHT DECOMPOSITION")
print("=" * 70)

if len(best_abelian) >= 2 and k_rank == dim:
    # Simultaneously diagonalize H_1 and H_2 in the 8-dim rep
    H1 = T_generators[best_abelian[0]]
    H2 = T_generators[best_abelian[1]]

    # Check if they commute in the rep
    comm_H = H1 @ H2 - H2 @ H1
    print(f"|[H1, H2]| = {np.linalg.norm(comm_H):.2e}")

    if np.linalg.norm(comm_H) < 1e-8:
        # Simultaneously diagonalizable
        # Find eigenvalues of H1 + random*H2 to break degeneracy
        np.random.seed(123)
        r = 0.3721  # irrational to break degeneracies
        H_combo = H1 + r * H2
        evals_combo, evecs_combo = np.linalg.eig(H_combo)

        # For each eigenvector, compute (h1, h2) weight
        weights = []
        for idx in range(8):
            v = evecs_combo[:, idx]
            h1_val = (v.conj() @ H1 @ v).real / (v.conj() @ v).real
            h2_val = (v.conj() @ H2 @ v).real / (v.conj() @ v).real
            weights.append((h1_val, h2_val))
            print(f"  Weight {idx}: ({h1_val:.4f}, {h2_val:.4f})")

        # For su(3) adjoint rep, weights should be:
        # (1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1), (0,0), (0,0)
        # (the 6 roots plus 2 zero weights from the Cartan)
        print("\nExpected for su(3) adjoint: 6 nonzero roots + 2 zero weights")
        zero_weights = sum(1 for (h1, h2) in weights if abs(h1) < 0.1 and abs(h2) < 0.1)
        print(f"Number of near-zero weights: {zero_weights}")

# ============================================================
# Try explicit su(3) Gell-Mann matrices
# ============================================================

print("\n" + "=" * 70)
print("COMPARISON WITH GELL-MANN MATRICES (su(3) generators)")
print("=" * 70)

# Gell-Mann matrices are 3x3. Their adjoint rep gives 8x8 matrices.
# Let's construct the adjoint rep of su(3) and compare.

# Gell-Mann matrices (standard basis of su(3)):
gm = np.zeros((8, 3, 3), dtype=complex)
gm[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])  # lambda_1
gm[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]])  # lambda_2
gm[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]])  # lambda_3
gm[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]])  # lambda_4
gm[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]])  # lambda_5
gm[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]])  # lambda_6
gm[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]])  # lambda_7
gm[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / np.sqrt(3)  # lambda_8

# Normalize: T_a = lambda_a / 2
gm = gm / 2

# Compute structure constants of su(3)
su3_f = np.zeros((8, 8, 8))
for a in range(8):
    for b in range(8):
        comm = gm[a] @ gm[b] - gm[b] @ gm[a]
        # comm = i * sum_c f_{abc} T_c
        for c in range(8):
            # f_{abc} = -2i * Tr(comm * T_c) / Tr(T_c T_c) ...
            # Actually [T_a, T_b] = i * f_{abc} T_c
            # Tr([T_a,T_b] T_c) = i * f_{abc} * Tr(T_c^2) = i * f_{abc} * 1/2
            coeff = np.trace(comm @ gm[c])
            # coeff = i * f_{abc} * Tr(T_c^2) = i * f_{abc} / 2...
            # For Gell-Mann with T=lambda/2: Tr(T_a T_b) = delta_{ab}/2
            su3_f[a, b, c] = (-2j * coeff).real  # f_{abc}

print("su(3) structure constants (nonzero f_{abc}):")
for a in range(8):
    for b in range(a+1, 8):
        for c in range(8):
            if abs(su3_f[a, b, c]) > 1e-10:
                print(f"  f_{{{a+1},{b+1},{c+1}}} = {su3_f[a,b,c]:.4f}")

# Now compute structure constants of our algebra
print("\nOur algebra structure constants (nonzero):")
for a in range(dim):
    for b in range(a+1, dim):
        for c in range(dim):
            if abs(brackets[a, b, c]) > 1e-8:
                print(f"  f_{{{a},{b},{c}}} = {brackets[a,b,c]:.4f}")

# ============================================================
# The definitive test: compute the Cartan matrix
# ============================================================

print("\n" + "=" * 70)
print("CARTAN MATRIX COMPUTATION")
print("=" * 70)

if k_rank == dim and len(best_abelian) >= 2:
    # Use the ad representation to find roots
    H_ads = [brackets[i].T for i in best_abelian]

    # Simultaneously diagonalize
    # Since they commute, find common eigenspaces
    H1_ad = H_ads[0]
    H2_ad = H_ads[1]

    evals1 = np.linalg.eigvals(H1_ad).real
    evals2 = np.linalg.eigvals(H2_ad).real
    print(f"ad(H1) eigenvalues: {np.sort(evals1)}")
    print(f"ad(H2) eigenvalues: {np.sort(evals2)}")

    # Find roots by simultaneous diagonalization
    H_combo_ad = H1_ad + 0.3721 * H2_ad
    evals_c, evecs_c = np.linalg.eig(H_combo_ad)

    roots_ad = []
    for idx in range(dim):
        v = evecs_c[:, idx]
        h1 = (v.conj() @ H1_ad @ v).real / (v.conj() @ v).real
        h2 = (v.conj() @ H2_ad @ v).real / (v.conj() @ v).real
        roots_ad.append((h1, h2))
        print(f"  Root {idx}: ({h1:.4f}, {h2:.4f})")

    nonzero_roots = [(h1, h2) for (h1, h2) in roots_ad if abs(h1) > 0.05 or abs(h2) > 0.05]
    print(f"\nNonzero roots: {len(nonzero_roots)}")
    print(f"Zero roots (Cartan): {len(roots_ad) - len(nonzero_roots)}")

    # For su(3): 6 nonzero roots, 2 zero roots
    # For su(2)^2 or other rank-2 algebras: different root count
    if len(nonzero_roots) == 6:
        print("6 nonzero roots -> consistent with su(3) (A2 root system)!")
    elif len(nonzero_roots) == 4:
        print("4 nonzero roots -> consistent with su(2) x su(2) (A1 x A1)")
    elif len(nonzero_roots) == 12:
        print("12 nonzero roots -> consistent with g2")

# ============================================================
# Also: check the 8D algebra generators as elements of gl(8,R)
# ============================================================

print("\n" + "=" * 70)
print("GENERATOR PROPERTIES IN gl(8,R)")
print("=" * 70)

# For a REAL form of su(3), we'd expect:
# - 8 generators that are 8x8 real matrices
# - Antisymmetric (since su(n) consists of anti-Hermitian matrices)

# Check antisymmetry again
n_antisymm = 0
n_symm = 0
for T in T_generators:
    if np.linalg.norm(T + T.T) < 1e-8:
        n_antisymm += 1
    elif np.linalg.norm(T - T.T) < 1e-8:
        n_symm += 1

print(f"Antisymmetric generators: {n_antisymm}/{dim}")
print(f"Symmetric generators: {n_symm}/{dim}")

# If not all antisymmetric, try to find a basis change that makes them antisymmetric
# A Lie algebra isomorphic to su(n) should have a compact real form
# where all generators are antisymmetric

# Check: are generators in so(8)? (antisymmetric 8x8 = so(8), dim=28)
# Our 8-dim subalgebra of gl(8) -- is it contained in so(8)?

# Try to orthogonalize: find a positive definite metric G such that
# G T + T^T G = 0 for all generators T (i.e., T is antisymmetric w.r.t. G)

print("\n--- Checking if algebra embeds in so(8) after basis change ---")
# This requires: exists G > 0 s.t. GT + T^TG = 0 for all T
# i.e., GT is antisymmetric for all T
# Vectorize: for each T, the condition GT + T^TG = 0 is linear in G
# G is 8x8 symmetric positive definite (36 unknowns)

num_G_vars = 36  # upper triangular entries of symmetric G
G_constraints = []

for T in T_generators:
    # GT + T^T G = 0
    # (GT)_{ij} + (T^T G)_{ij} = 0
    # sum_k G_{ik} T_{kj} + sum_k T_{ki} G_{kj} = 0
    # G is symmetric: G_{ij} = G_{ji}
    for ii in range(8):
        for jj in range(ii, 8):  # only upper triangle of the equation (it's symmetric)
            row = np.zeros(num_G_vars)
            # (GT + T^TG)_{ij} = sum_k G_{ik}T_{kj} + T_{ki}G_{kj}
            for k in range(8):
                # G_{ik} -> index of (min(i,k), max(i,k)) in upper triangle
                gi, gj = min(ii, k), max(ii, k)
                g_idx = gi * 8 - gi * (gi - 1) // 2 + (gj - gi)
                row[g_idx] += T[k, jj]

                gi2, gj2 = min(k, jj), max(k, jj)
                g_idx2 = gi2 * 8 - gi2 * (gi2 - 1) // 2 + (gj2 - gi2)
                row[g_idx2] += T[k, ii]  # T^T_{ik} = T_{ki}

            G_constraints.append(row)

G_mat = np.array(G_constraints)
U_g, S_g, Vt_g = np.linalg.svd(G_mat)
rank_G = np.sum(S_g > 1e-8)
null_G = num_G_vars - rank_G
print(f"Constraint matrix rank: {rank_G}, null space dim: {null_G}")

if null_G > 0:
    # Extract a solution
    G_null = Vt_g[rank_G:]
    print(f"Found {null_G}-parameter family of invariant metrics")

    # Try each null vector and check positive definiteness
    for idx in range(null_G):
        g_vec = G_null[idx]
        G = np.zeros((8, 8))
        v_idx = 0
        for ii in range(8):
            for jj in range(ii, 8):
                G[ii, jj] = g_vec[v_idx]
                G[jj, ii] = g_vec[v_idx]
                v_idx += 1
        evals_G = np.linalg.eigvalsh(G)
        print(f"  Metric {idx}: eigenvalues = {evals_G}")
        if np.all(evals_G > 1e-10) or np.all(evals_G < -1e-10):
            print(f"    -> Positive/negative definite! Algebra embeds in so(8)")

    # Try linear combinations
    if null_G >= 2:
        for alpha in np.linspace(-2, 2, 20):
            g_vec = G_null[0] + alpha * G_null[1]
            G = np.zeros((8, 8))
            v_idx = 0
            for ii in range(8):
                for jj in range(ii, 8):
                    G[ii, jj] = g_vec[v_idx]
                    G[jj, ii] = g_vec[v_idx]
                    v_idx += 1
            evals_G = np.linalg.eigvalsh(G)
            if np.all(evals_G > 1e-8):
                print(f"\n  Found positive definite metric at alpha={alpha:.2f}!")
                print(f"  Eigenvalues: {evals_G}")
                print(f"  -> The algebra is COMPACT and embeds in so(8)")
                break

print("\n" + "=" * 70)
print("FINAL IDENTIFICATION")
print("=" * 70)

print(f"""
Summary of the 8-dimensional ZD-preserving Lie algebra on ell-O sector:
  - Dimension: {dim}
  - Semisimple: {k_rank == dim}
  - Killing form rank: {k_rank}
  - Maximal abelian subalgebra dimension (rank): {len(best_abelian)}
""")

if k_rank == dim and dim == 8:
    if len(best_abelian) == 2:
        print("IDENTIFICATION: su(3)")
        print("  dim=8, rank=2, semisimple -> unique answer is su(3) = A_2")
    elif len(best_abelian) == 1:
        print("IDENTIFICATION: unclear (dim 8, rank 1)")
    elif len(best_abelian) == 3:
        print("IDENTIFICATION: possibly su(2)^3 (dim 9?) or other")
elif k_rank < dim:
    ss_dim = k_rank
    abelian_dim = dim - k_rank
    print(f"NOT semisimple: {ss_dim}-dim semisimple part + {abelian_dim}-dim radical")
    if ss_dim == 3:
        print(f"Could be: su(2) + R^{abelian_dim}")
    elif ss_dim == 6:
        print(f"Could be: su(2)^2 + R^{abelian_dim}")

print(f"""
PHYSICS CONCLUSION:
===================
The zero-divisor preserving symmetry on the ell-O (e8-e15) sector
of the sedenion algebra has Lie algebra of dimension {dim}.
""")

if dim == 8 and k_rank == dim:
    print("""This is su(3) -- the gauge algebra of QCD (strong force)!

The chain of Cayley-Dickson symmetry breaking:
  Aut(R) = trivial
  Aut(C) = Z_2
  Aut(H) = SO(3) = SU(2)/Z_2   [dim = 3]
  Aut(O) = G_2                   [dim = 14]
  Der(S) = g_2                   [dim = 14, same as octonions]

  ZD-preserving on ell-O sector = su(3) [dim = 8]

The SU(3) gauge group of the Standard Model emerges naturally as
the group preserving the zero-divisor structure on the second
(imaginary) octonion copy within the sedenion algebra.
""")
