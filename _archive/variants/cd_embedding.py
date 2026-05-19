# LONGINUS: sourceId=cd_embedding, sourcePath=cd_embedding.py
"""
CD Embedding Map: How 32D (trigintaduonion) doublets embed into 16D (sedenion) doublets.

Cayley-Dickson multiplication: (a1,a2)(b1,b2) = (a1*b1 - conj(b2)*a2, b2*a1 + a2*conj(b1))
conj: negate all imaginary components (all except index 0).
"""
import numpy as np
from itertools import combinations
np.set_printoptions(precision=6, suppress=True, linewidth=140)

# ============================================================
# 1. Cayley-Dickson multiplication (recursive)
# ============================================================
def cd_conj(x):
    """Conjugate: negate all components except index 0."""
    c = -x.copy()
    c[0] = x[0]
    return c

def cd_multiply(a, b, n):
    """Multiply two elements in the 2^n-dimensional CD algebra."""
    dim = 2**n
    assert len(a) == dim and len(b) == dim
    if n == 0:
        return a * b
    half = dim // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    part1 = cd_multiply(a1, b1, n-1) - cd_multiply(cd_conj(b2), a2, n-1)
    part2 = cd_multiply(b2, a1, n-1) + cd_multiply(a2, cd_conj(b1), n-1)
    return np.concatenate([part1, part2])

def build_mult_table(n):
    """Build full multiplication table for 2^n-dim CD algebra."""
    dim = 2**n
    MULT = np.zeros((dim, dim, dim), dtype=float)
    for i in range(dim):
        for j in range(dim):
            ei = np.zeros(dim); ei[i] = 1.0
            ej = np.zeros(dim); ej[j] = 1.0
            MULT[i, j, :] = cd_multiply(ei, ej, n)
    return MULT

def left_mult_matrix(a, MULT):
    """Matrix L_a such that L_a @ x = a * x."""
    dim = len(a)
    L = np.zeros((dim, dim))
    for j in range(dim):
        for k in range(dim):
            if a[k] != 0:
                L[:, j] += a[k] * MULT[k, j]
    return L

def right_mult_matrix(b, MULT):
    """Matrix R_b such that R_b @ x = x * b."""
    dim = len(b)
    R = np.zeros((dim, dim))
    for j in range(dim):
        for k in range(dim):
            if b[k] != 0:
                R[:, j] += b[k] * MULT[j, k]
    return R

def null_space(M, tol=1e-10):
    """Compute null space of matrix M."""
    U, S, Vh = np.linalg.svd(M)
    null_dim = np.sum(S < tol)
    if null_dim == 0:
        return np.zeros((0, M.shape[1]))
    return Vh[-null_dim:]

# ============================================================
# 2. Build multiplication tables for 16D and 32D
# ============================================================
print("Building 16D (sedenion) multiplication table...")
MULT16 = build_mult_table(4)  # 2^4 = 16
print("Building 32D (trigintaduonion) multiplication table...")
MULT32 = build_mult_table(5)  # 2^5 = 32

# ============================================================
# 3. Find all ZD pairs and null spaces for 16D
# ============================================================
print("\n" + "="*80)
print("SEDENION (16D) ZERO DIVISOR ANALYSIS")
print("="*80)

zd_pairs_16 = []
for i in range(1, 16):
    for j in range(i+1, 16):
        a = np.zeros(16); a[i] = 1.0; a[j] = 1.0
        La = left_mult_matrix(a, MULT16)
        ns = null_space(La)
        if ns.shape[0] > 0:
            zd_pairs_16.append((i, j, ns))

print(f"Total ZD pairs (e_i + e_j): {len(zd_pairs_16)}")

# Group by null space dimension
from collections import Counter
ndim_counts_16 = Counter(ns.shape[0] for (i, j, ns) in zd_pairs_16)
print(f"Null space dimensions: {dict(ndim_counts_16)}")

# ============================================================
# 4. For each 16D ZD pair, find the SU(2) doublet in null space
# ============================================================
# A doublet is a 2D subspace in the null space that transforms as j=1/2 under SU(2)
# For a 4D null space, we use right-multiplication R_{e_k} restricted to null space
# to find which 2D subspaces are irreducible.

def find_doublets_in_null_space(ns_basis, MULT, dim):
    """
    Given a null space basis (rows = basis vectors), find SU(2) doublet decomposition.
    We look for right-multiplication operators R_{e_k} that preserve the null space
    and act as Pauli-like matrices on 2D subspaces.
    """
    n_null = ns_basis.shape[0]
    if n_null < 2:
        return []

    # Project R_{e_k} onto the null space
    projected_R = {}
    for k in range(1, dim):
        ek = np.zeros(dim); ek[k] = 1.0
        Rk = right_mult_matrix(ek, MULT)
        # Project: P @ Rk @ P^T where P = ns_basis (rows are basis vectors)
        Rk_proj = ns_basis @ Rk @ ns_basis.T
        projected_R[k] = Rk_proj

    # Find triplets (k1,k2,k3) where projected R's form su(2) algebra
    # {J_a, J_b} = -2 delta_{ab} (for imaginary quaternion units)
    # Look for pairs that anticommute and square to -I

    su2_generators = []
    for k in range(1, dim):
        Rk = projected_R[k]
        # Check if Rk^2 ~ -I on null space
        Rk2 = Rk @ Rk
        if np.allclose(Rk2, -np.eye(n_null), atol=1e-8):
            su2_generators.append(k)

    # Now find anticommuting triples among these
    doublets = []
    if len(su2_generators) >= 3:
        for a_idx in range(len(su2_generators)):
            for b_idx in range(a_idx+1, len(su2_generators)):
                for c_idx in range(b_idx+1, len(su2_generators)):
                    ka, kb, kc = su2_generators[a_idx], su2_generators[b_idx], su2_generators[c_idx]
                    Ja, Jb, Jc = projected_R[ka], projected_R[kb], projected_R[kc]
                    # Check anticommutation
                    ab = Ja @ Jb + Jb @ Ja
                    ac = Ja @ Jc + Jc @ Ja
                    bc = Jb @ Jc + Jc @ Jb
                    if (np.linalg.norm(ab) < 1e-8 and
                        np.linalg.norm(ac) < 1e-8 and
                        np.linalg.norm(bc) < 1e-8):
                        # Found su(2)! Now decompose null space into doublets
                        # Eigenvalues of iJa are ±1, each eigenspace is a doublet
                        # Number of doublets = n_null / 2
                        n_doublets = n_null // 2

                        # Diagonalize Ja to find the doublets explicitly
                        evals, evecs = np.linalg.eigh(1j * Ja)
                        # Group into +1 and -1 eigenspaces
                        plus_idx = np.where(np.abs(evals - 1.0) < 1e-8)[0]
                        minus_idx = np.where(np.abs(evals + 1.0) < 1e-8)[0]

                        doublet_list = []
                        for p in range(min(len(plus_idx), len(minus_idx))):
                            v_up = evecs[:, plus_idx[p]]  # in null-space coordinates
                            v_down = evecs[:, minus_idx[p]]
                            # Convert to full space coordinates
                            v_up_full = (ns_basis.T @ v_up).real
                            v_down_full = (ns_basis.T @ v_down).real
                            # Also get the imaginary parts
                            v_up_full_i = (ns_basis.T @ v_up).imag
                            v_down_full_i = (ns_basis.T @ v_down).imag
                            doublet_list.append({
                                'up_real': v_up_full,
                                'up_imag': v_up_full_i,
                                'down_real': v_down_full,
                                'down_imag': v_down_full_i,
                                'su2_triple': (ka, kb, kc)
                            })

                        return (ka, kb, kc), n_doublets, doublet_list

    return None

# Simpler approach: just find the null space basis vectors as doublet content
# For a 4D null space, there is 1 doublet (2 complex = 4 real dimensions)
# For a 12D null space, there are 6 doublets

print(f"\n16D ZD pairs with null spaces:")
sed_zd_data = {}
for (i, j, ns) in zd_pairs_16:
    ndim = ns.shape[0]
    n_doublets = ndim // 2  # Each doublet = 2 real dimensions in simplest count
    # Actually: j=1/2 doublet = 2 complex dims = 4 real dims
    # So 4D null -> 1 doublet, but let's verify
    sed_zd_data[(i,j)] = {'null_basis': ns, 'null_dim': ndim}

print(f"  All {len(zd_pairs_16)} pairs have null_dim = {zd_pairs_16[0][2].shape[0]}")

# ============================================================
# 5. Find all ZD pairs and null spaces for 32D
# ============================================================
print("\n" + "="*80)
print("TRIGINTADUONION (32D) ZERO DIVISOR ANALYSIS")
print("="*80)

zd_pairs_32 = []
for i in range(1, 32):
    for j in range(i+1, 32):
        a = np.zeros(32); a[i] = 1.0; a[j] = 1.0
        La = left_mult_matrix(a, MULT32)
        ns = null_space(La)
        if ns.shape[0] > 0:
            zd_pairs_32.append((i, j, ns))

print(f"Total ZD pairs (e_i + e_j): {len(zd_pairs_32)}")

ndim_counts_32 = Counter(ns.shape[0] for (i, j, ns) in zd_pairs_32)
print(f"Null space dimensions: {dict(ndim_counts_32)}")

# Classify 32D ZD pairs
zd32_by_ndim = {}
for (i, j, ns) in zd_pairs_32:
    ndim = ns.shape[0]
    if ndim not in zd32_by_ndim:
        zd32_by_ndim[ndim] = []
    zd32_by_ndim[ndim].append((i, j, ns))

for ndim in sorted(zd32_by_ndim.keys()):
    pairs = zd32_by_ndim[ndim]
    n_doublets = ndim // 4  # 4 real dims per j=1/2 doublet
    print(f"  null_dim={ndim}: {len(pairs)} pairs, {n_doublets} doublet(s) each")

# ============================================================
# 6. EMBEDDING ANALYSIS: 32D → 16D projection
# ============================================================
print("\n" + "="*80)
print("EMBEDDING ANALYSIS: 32D null spaces → 16D projection")
print("="*80)

# The 16D sedenion embeds in the 32D trigintaduonion as the first 16 components.
# (a, 0) in 32D corresponds to a in 16D (CD doubling: 32D = 16D x 16D)

# For each 32D ZD pair, project its null space vectors onto first 16 components
# and check overlap with 16D null spaces.

def project_to_16(ns_basis_32):
    """Project 32D null space basis to first 16 components."""
    return ns_basis_32[:, :16]

def project_to_upper_16(ns_basis_32):
    """Project 32D null space basis to last 16 components."""
    return ns_basis_32[:, 16:]

# Classify 32D ZD pairs by whether indices are both <16, mixed, or both >=16
both_lower = []  # both i,j < 16 (inherited from 16D)
mixed = []       # one < 16, one >= 16
both_upper = []  # both i,j >= 16

for (i, j, ns) in zd_pairs_32:
    if i < 16 and j < 16:
        both_lower.append((i, j, ns))
    elif i >= 16 and j >= 16:
        both_upper.append((i, j, ns))
    else:
        mixed.append((i, j, ns))

print(f"\n32D ZD pairs by index location:")
print(f"  Both indices < 16 (sedenion-inherited): {len(both_lower)}")
print(f"  Mixed (one < 16, one >= 16):            {len(mixed)}")
print(f"  Both indices >= 16 (upper half):         {len(both_upper)}")

# ============================================================
# 6a. For "both_lower" pairs: these should correspond to 16D ZD pairs
# ============================================================
print("\n" + "-"*80)
print("CATEGORY 1: Both indices < 16 (sedenion-inherited pairs)")
print("-"*80)

inherited_count = 0
for (i, j, ns32) in both_lower:
    ndim32 = ns32.shape[0]
    # Check if (i,j) is a 16D ZD pair
    key16 = (i, j) if i < j else (j, i)
    is_16d_zd = key16 in sed_zd_data

    # Project null space to lower 16
    proj_lower = project_to_16(ns32)
    proj_upper = project_to_upper_16(ns32)

    # Rank of projection tells us how many dimensions land in lower 16
    rank_lower = np.linalg.matrix_rank(proj_lower, tol=1e-8)
    rank_upper = np.linalg.matrix_rank(proj_upper, tol=1e-8)

    if inherited_count < 5:  # Print first few examples
        print(f"\n  Pair ({i},{j}): null_dim_32={ndim32}, is_16D_ZD={is_16d_zd}")
        print(f"    Lower-16 projection rank: {rank_lower}")
        print(f"    Upper-16 projection rank: {rank_upper}")

        if is_16d_zd:
            ns16 = sed_zd_data[key16]['null_basis']
            # Check overlap: do the 32D null vectors' lower-16 projections
            # land in the 16D null space?
            # Project each 32D null vector's lower-16 part onto 16D null space
            P16 = ns16.T @ ns16  # projector onto 16D null space
            proj_in_null = P16 @ proj_lower.T  # project lower-16 components
            proj_in_null_rank = np.linalg.matrix_rank(proj_in_null, tol=1e-8)

            # Also check complement
            proj_perp = proj_lower.T - proj_in_null
            proj_perp_rank = np.linalg.matrix_rank(proj_perp, tol=1e-8)

            print(f"    16D null_dim: {ns16.shape[0]}")
            print(f"    32D lower-proj landing in 16D null space: rank={proj_in_null_rank}")
            print(f"    32D lower-proj orthogonal to 16D null space: rank={proj_perp_rank}")

    inherited_count += 1

print(f"\n  ... total {len(both_lower)} such pairs")

# ============================================================
# 6b. Systematic overlap computation
# ============================================================
print("\n" + "-"*80)
print("SYSTEMATIC OVERLAP: 32D null space projections → 16D null spaces")
print("-"*80)

# For ALL 32D ZD pairs, compute the overlap of their null space (projected to lower 16)
# with ALL 16D null spaces

# First, collect all 16D null space projectors
sed_projectors = {}
for (i, j, ns) in zd_pairs_16:
    P = ns.T @ ns  # Projector onto null space
    sed_projectors[(i,j)] = P

# Now for each 32D pair, compute overlap
print("\nFor each 32D null_dim category, analyze projection structure:")

for ndim in sorted(zd32_by_ndim.keys()):
    pairs = zd32_by_ndim[ndim]
    n_doublets_32 = ndim // 4

    print(f"\n  null_dim={ndim} ({len(pairs)} pairs, {n_doublets_32} doublet(s) each):")

    # Statistics
    overlap_stats = []

    for (i, j, ns32) in pairs[:20]:  # Sample first 20
        proj_lower = project_to_16(ns32)
        rank_lower = np.linalg.matrix_rank(proj_lower, tol=1e-8)

        proj_upper = project_to_upper_16(ns32)
        rank_upper = np.linalg.matrix_rank(proj_upper, tol=1e-8)

        # Find which 16D ZD null spaces have overlap
        max_overlap = 0
        best_16d_pair = None
        total_overlap_dim = 0
        overlapping_16d_pairs = []

        for (si, sj), P16 in sed_projectors.items():
            # Project the lower-16 components through the 16D null space projector
            overlap = P16 @ proj_lower.T
            overlap_rank = np.linalg.matrix_rank(overlap, tol=1e-8)
            if overlap_rank > 0:
                overlapping_16d_pairs.append(((si, sj), overlap_rank))
                if overlap_rank > max_overlap:
                    max_overlap = overlap_rank
                    best_16d_pair = (si, sj)

        overlap_stats.append({
            'pair': (i,j), 'ndim': ndim,
            'rank_lower': rank_lower, 'rank_upper': rank_upper,
            'n_overlapping_16d': len(overlapping_16d_pairs),
            'max_overlap': max_overlap,
            'best_16d': best_16d_pair
        })

    # Print summary
    cat_label = "both<16" if all(i<16 and j<16 for (i,j,_) in pairs[:5]) else \
                "mixed" if any(i<16 and j>=16 or i>=16 and j<16 for (i,j,_) in pairs[:5]) else \
                "both>=16"

    for stat in overlap_stats[:5]:
        p = stat['pair']
        cat = "both<16" if p[0]<16 and p[1]<16 else "mixed" if (p[0]<16)!=(p[1]<16) else "both>=16"
        print(f"    ({p[0]:2d},{p[1]:2d}) [{cat:>8s}]: lower_rank={stat['rank_lower']}, "
              f"upper_rank={stat['rank_upper']}, "
              f"#overlapping_16D_pairs={stat['n_overlapping_16d']}, "
              f"max_overlap_dim={stat['max_overlap']}")

    if len(overlap_stats) > 5:
        # Aggregate
        avg_n_overlap = np.mean([s['n_overlapping_16d'] for s in overlap_stats])
        avg_max = np.mean([s['max_overlap'] for s in overlap_stats])
        print(f"    ... (avg over {len(overlap_stats)} samples: "
              f"mean_#overlapping={avg_n_overlap:.1f}, mean_max_overlap={avg_max:.1f})")

# ============================================================
# 7. DETAILED DOUBLET EMBEDDING for null_dim=12 pairs
# ============================================================
print("\n" + "="*80)
print("DETAILED DOUBLET EMBEDDING: 32D null_dim=12 → 16D")
print("="*80)

if 12 in zd32_by_ndim:
    # Take a representative pair with null_dim=12
    rep_pairs = zd32_by_ndim[12][:3]

    for idx, (i, j, ns32) in enumerate(rep_pairs):
        print(f"\n--- Representative pair ({i},{j}), null_dim=12 ---")

        # The 12D null space should contain 3 doublets (12/4=3)
        # or 6 doublets if counting as 2-real-dim

        # Project to lower and upper 16
        proj_lower = ns32[:, :16]
        proj_upper = ns32[:, 16:]

        rank_lower = np.linalg.matrix_rank(proj_lower, tol=1e-8)
        rank_upper = np.linalg.matrix_rank(proj_upper, tol=1e-8)

        print(f"  Null space projection ranks: lower-16={rank_lower}, upper-16={rank_upper}")

        # SVD of the lower-16 projection to see which dimensions contribute
        U, S, Vh = np.linalg.svd(proj_lower, full_matrices=False)
        sig_vals = S[S > 1e-8]
        print(f"  Significant singular values of lower-16 projection: {sig_vals}")
        print(f"  Number of significant: {len(sig_vals)} (out of {len(S)})")

        # Find the subspace of the 32D null space that projects purely into lower 16
        # (i.e., upper-16 components are zero)
        # This is the "inherited" part
        U_up, S_up, Vh_up = np.linalg.svd(proj_upper, full_matrices=False)
        zero_sv = np.where(S_up < 1e-8)[0]
        if len(zero_sv) > 0:
            # Null space of the upper projection = vectors purely in lower 16
            inherited_vecs = U[:, zero_sv]  # in null-space coordinates
            inherited_32d = ns32.T @ inherited_vecs  # in 32D coordinates
            inherited_16d = inherited_32d[:16, :]  # lower 16 components
            print(f"  Purely lower-16 subspace dim: {len(zero_sv)}")
            print(f"  These are 'inherited' doublet dimensions")
        else:
            print(f"  No purely lower-16 subspace (all null vectors have upper components)")

        # Find the subspace that projects purely into upper 16
        U_lo, S_lo, Vh_lo = np.linalg.svd(proj_lower, full_matrices=False)
        zero_sv_lo = np.where(S_lo < 1e-8)[0]
        if len(zero_sv_lo) > 0:
            new_vecs = U[:, zero_sv_lo]
            print(f"  Purely upper-16 subspace dim: {len(zero_sv_lo)}")
            print(f"  These are 'genuinely new' doublet dimensions")
        else:
            print(f"  No purely upper-16 subspace")

        # The mixed part
        mixed_dim = 12 - len(zero_sv) - len(zero_sv_lo) if len(zero_sv) > 0 else 12 - len(zero_sv_lo)
        if 'zero_sv' not in dir():
            mixed_dim = 12
        print(f"  Mixed (both halves nonzero) subspace dim: ~{12 - (len(zero_sv) if len(zero_sv)>0 else 0) - (len(zero_sv_lo) if len(zero_sv_lo)>0 else 0)}")

        # Check overlap with each 16D ZD pair's null space
        print(f"\n  Overlaps with 16D ZD null spaces:")
        overlaps = []
        for (si, sj, ns16) in zd_pairs_16:
            P16 = ns16.T @ ns16
            # Project 32D null vectors' lower-16 parts through 16D null projector
            overlap_vecs = P16 @ proj_lower.T
            overlap_rank = np.linalg.matrix_rank(overlap_vecs, tol=1e-8)
            if overlap_rank > 0:
                overlaps.append(((si, sj), overlap_rank))

        print(f"  Number of 16D pairs with nonzero overlap: {len(overlaps)}")
        for (pair16, rank) in sorted(overlaps, key=lambda x: -x[1])[:10]:
            print(f"    16D pair ({pair16[0]:2d},{pair16[1]:2d}): overlap dim = {rank}")

# ============================================================
# 8. BUILD THE EMBEDDING MATRIX
# ============================================================
print("\n" + "="*80)
print("EMBEDDING MATRIX: 32D doublets → 16D doublets")
print("="*80)

# Strategy: For each 32D ZD pair, decompose null space into:
#   - Component in span of all 16D null spaces (inherited)
#   - Component orthogonal to all 16D null spaces (new)

# Build the union of all 16D null spaces (embedded in 32D as lower-16)
all_16d_null_vecs = []
for (i, j, ns16) in zd_pairs_16:
    for row in ns16:
        v32 = np.zeros(32)
        v32[:16] = row
        all_16d_null_vecs.append(v32)

all_16d_null_vecs = np.array(all_16d_null_vecs)
# Orthogonalize to get the subspace
U16, S16, Vh16 = np.linalg.svd(all_16d_null_vecs.T, full_matrices=False)
sig_16 = np.sum(S16 > 1e-8)
print(f"\nUnion of all 16D null spaces (embedded in 32D): dimension = {sig_16}")
P_inherited = U16[:, :sig_16] @ U16[:, :sig_16].T  # Projector

# Now classify each 32D ZD pair
print(f"\nClassification of 32D ZD pairs:")
print(f"{'Pair':>10s} {'null_dim':>8s} {'inherited':>10s} {'new':>6s} {'category':>10s}")
print("-" * 50)

classification = {'purely_inherited': 0, 'purely_new': 0, 'mixed': 0}
detailed_results = []

for (i, j, ns32) in zd_pairs_32:
    ndim = ns32.shape[0]

    # Project each null space vector through P_inherited
    inherited_components = P_inherited @ ns32.T  # 32 x ndim
    new_components = ns32.T - inherited_components  # 32 x ndim

    rank_inherited = np.linalg.matrix_rank(inherited_components, tol=1e-8)
    rank_new = np.linalg.matrix_rank(new_components, tol=1e-8)

    if rank_new == 0:
        cat = 'inherited'
        classification['purely_inherited'] += 1
    elif rank_inherited == 0:
        cat = 'new'
        classification['purely_new'] += 1
    else:
        cat = 'mixed'
        classification['mixed'] += 1

    detailed_results.append((i, j, ndim, rank_inherited, rank_new, cat))

# Print summary by null_dim
for ndim in sorted(zd32_by_ndim.keys()):
    results_this_ndim = [(i,j,n,ri,rn,c) for (i,j,n,ri,rn,c) in detailed_results if n == ndim]
    print(f"\n  null_dim={ndim}: {len(results_this_ndim)} pairs")

    cat_counts = Counter(c for (_,_,_,_,_,c) in results_this_ndim)
    for cat in ['inherited', 'mixed', 'new']:
        if cat in cat_counts:
            print(f"    {cat}: {cat_counts[cat]}")

    # Print a few examples
    for (i, j, n, ri, rn, c) in results_this_ndim[:5]:
        print(f"    ({i:2d},{j:2d}): inherited_dim={ri}, new_dim={rn} [{c}]")
    if len(results_this_ndim) > 5:
        print(f"    ...")

# Distribution of inherited vs new dimensions
print(f"\n{'='*80}")
print(f"SUMMARY: INHERITED vs NEW DOUBLETS")
print(f"{'='*80}")
print(f"\nTotal 32D ZD pairs: {len(zd_pairs_32)}")
print(f"  Purely inherited (all null dims from 16D): {classification['purely_inherited']}")
print(f"  Mixed (some inherited, some new):          {classification['mixed']}")
print(f"  Purely new (no 16D null space overlap):    {classification['purely_new']}")

# Count total doublet dimensions
total_inherited_dims = sum(ri for (_,_,_,ri,_,_) in detailed_results)
total_new_dims = sum(rn for (_,_,_,_,rn,_) in detailed_results)
total_null_dims = sum(n for (_,_,n,_,_,_) in detailed_results)

print(f"\nTotal null space dimensions across all 32D pairs: {total_null_dims}")
print(f"  Inherited dimensions (depth 1): {total_inherited_dims}")
print(f"  New dimensions (depth 2):       {total_new_dims}")
print(f"  Ratio inherited/total: {total_inherited_dims/total_null_dims:.4f}")
print(f"  Ratio new/total:       {total_new_dims/total_null_dims:.4f}")

# ============================================================
# 9. Detailed: Which 16D pairs does each 32D pair inherit from?
# ============================================================
print(f"\n{'='*80}")
print(f"INHERITANCE MAP: Which 16D ZD pairs feed each 32D category")
print(f"{'='*80}")

# For each 32D pair category, find which 16D pairs contribute
for ndim in sorted(zd32_by_ndim.keys()):
    pairs = zd32_by_ndim[ndim]
    print(f"\n  32D null_dim={ndim}:")

    for (i, j, ns32) in pairs[:3]:
        # Find overlapping 16D pairs
        parent_pairs = []
        for (si, sj, ns16) in zd_pairs_16:
            # Embed 16D null space in 32D
            ns16_in_32 = np.zeros((ns16.shape[0], 32))
            ns16_in_32[:, :16] = ns16

            # Check overlap with 32D null space
            # Compute: ns32 @ ns16_in_32.T -> overlap matrix
            overlap = ns32 @ ns16_in_32.T
            overlap_rank = np.linalg.matrix_rank(overlap, tol=1e-8)
            if overlap_rank > 0:
                parent_pairs.append(((si, sj), overlap_rank))

        print(f"    32D pair ({i:2d},{j:2d}): inherits from {len(parent_pairs)} 16D pairs")
        for (pp, rank) in sorted(parent_pairs, key=lambda x: -x[1])[:5]:
            print(f"      ← 16D ({pp[0]:2d},{pp[1]:2d}), overlap dim={rank}")

# ============================================================
# 10. The key physics question: depth classification
# ============================================================
print(f"\n{'='*80}")
print(f"DEPTH CLASSIFICATION FOR PATH INTEGRAL MASS MODEL")
print(f"{'='*80}")

# Depth 1: doublets that are projections of 16D doublets
# Depth 2: genuinely new doublets appearing only at 32D

# Per-pair analysis
depth1_doublets_total = 0
depth2_doublets_total = 0

for (i, j, ndim, ri, rn, cat) in detailed_results:
    d1 = ri // 4 if ri >= 4 else (1 if ri >= 2 else 0)  # rough count
    d2 = rn // 4 if rn >= 4 else (1 if rn >= 2 else 0)
    depth1_doublets_total += ri  # count dimensions, not doublets
    depth2_doublets_total += rn

# Actually let's count by the context given: 4D null → 1 doublet, 12D null → multiple
# The question says "4D null space containing 1 SU(2) j=1/2 doublet"
# So 1 doublet per 4 null dims

print(f"\nBy 'doublet count' (1 doublet per 4 null dims):")
for ndim in sorted(zd32_by_ndim.keys()):
    results_this = [(i,j,n,ri,rn,c) for (i,j,n,ri,rn,c) in detailed_results if n == ndim]
    n_pairs = len(results_this)
    doublets_per_pair = ndim // 4
    total_doublets = n_pairs * doublets_per_pair

    # Average inherited/new
    avg_inherited = np.mean([ri for (_,_,_,ri,_,_) in results_this])
    avg_new = np.mean([rn for (_,_,_,_,rn,_) in results_this])

    print(f"\n  null_dim={ndim}: {n_pairs} pairs × {doublets_per_pair} doublet(s) = {total_doublets} total doublets")
    print(f"    Avg inherited dims per pair: {avg_inherited:.1f}")
    print(f"    Avg new dims per pair:       {avg_new:.1f}")
    print(f"    Inherited doublets ~ {avg_inherited/4:.1f} per pair")
    print(f"    New doublets ~       {avg_new/4:.1f} per pair")

print(f"\n{'='*80}")
print(f"FINAL EMBEDDING SUMMARY")
print(f"{'='*80}")
print(f"""
The Cayley-Dickson embedding 16D → 32D creates the following doublet structure:

16D (sedenion):
  - {len(zd_pairs_16)} ZD pairs, each with 4D null space → 1 doublet each
  - Total: {len(zd_pairs_16)} doublets

32D (trigintaduonion):
  - {len(zd_pairs_32)} ZD pairs total
  - Null dim distribution: {dict(ndim_counts_32)}

Classification:
  - Purely inherited: {classification['purely_inherited']} pairs
  - Mixed:            {classification['mixed']} pairs
  - Purely new:       {classification['purely_new']} pairs

Inherited null dims (depth 1): {total_inherited_dims}
New null dims (depth 2):       {total_new_dims}
""")
