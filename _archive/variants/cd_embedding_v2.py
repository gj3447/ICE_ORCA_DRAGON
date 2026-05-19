# LONGINUS: sourceId=cd_embedding_v2, sourcePath=cd_embedding_v2.py
"""
CD Embedding Map v2: Refined orthogonal decomposition of 32D null spaces
relative to the 16D sedenion subspace.

Key insight from v1: The union of all 16D null spaces (embedded in 32D)
spans a 14-dimensional subspace. Every 32D null space has mixed overlap
because CD doubling entangles the two halves with equal weight (singular
values all = 1/sqrt(2)).

This version performs proper orthogonal decomposition.
"""
import numpy as np
from collections import Counter
np.set_printoptions(precision=6, suppress=True, linewidth=140)

# ============================================================
# Cayley-Dickson machinery
# ============================================================
def cd_conj(x):
    c = -x.copy(); c[0] = x[0]; return c

def cd_multiply(a, b, n):
    dim = 2**n
    if n == 0: return a * b
    half = dim // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    p1 = cd_multiply(a1, b1, n-1) - cd_multiply(cd_conj(b2), a2, n-1)
    p2 = cd_multiply(b2, a1, n-1) + cd_multiply(a2, cd_conj(b1), n-1)
    return np.concatenate([p1, p2])

def build_mult_table(n):
    dim = 2**n
    M = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            ei = np.zeros(dim); ei[i] = 1.0
            ej = np.zeros(dim); ej[j] = 1.0
            M[i, j, :] = cd_multiply(ei, ej, n)
    return M

def left_mult_matrix(a, MULT):
    dim = len(a)
    L = np.zeros((dim, dim))
    for j in range(dim):
        for k in range(dim):
            if a[k] != 0: L[:, j] += a[k] * MULT[k, j]
    return L

def null_space(M, tol=1e-10):
    U, S, Vh = np.linalg.svd(M)
    null_dim = np.sum(S < tol)
    if null_dim == 0: return np.zeros((0, M.shape[1]))
    return Vh[-null_dim:]  # rows = basis vectors

print("Building multiplication tables...")
MULT16 = build_mult_table(4)
MULT32 = build_mult_table(5)

# ============================================================
# Compute all ZD pairs for 16D and 32D
# ============================================================
def find_zd_pairs(MULT, dim):
    pairs = []
    for i in range(1, dim):
        for j in range(i+1, dim):
            a = np.zeros(dim); a[i] = 1.0; a[j] = 1.0
            La = left_mult_matrix(a, MULT)
            ns = null_space(La)
            if ns.shape[0] > 0:
                pairs.append((i, j, ns))
    return pairs

print("Finding 16D ZD pairs...")
zd16 = find_zd_pairs(MULT16, 16)
print("Finding 32D ZD pairs...")
zd32 = find_zd_pairs(MULT32, 32)

print(f"\n{'='*80}")
print(f"RAW COUNTS")
print(f"{'='*80}")
print(f"16D: {len(zd16)} ZD pairs, all null_dim = {zd16[0][2].shape[0]}")

ndim32 = Counter(ns.shape[0] for (i,j,ns) in zd32)
print(f"32D: {len(zd32)} ZD pairs")
print(f"  null_dim distribution: {dict(sorted(ndim32.items()))}")

# ============================================================
# Build the 14D "inherited subspace" from all 16D null spaces
# ============================================================
# Embed each 16D null vector as (v, 0) in 32D
all_16d_vecs_in_32 = []
for (i, j, ns16) in zd16:
    for row in ns16:
        v32 = np.zeros(32)
        v32[:16] = row
        all_16d_vecs_in_32.append(v32)

V = np.array(all_16d_vecs_in_32).T  # 32 x N
U, S, _ = np.linalg.svd(V, full_matrices=False)
inherited_dim = np.sum(S > 1e-8)
P_inh_basis = U[:, :inherited_dim]  # Orthonormal basis for inherited subspace
P_inh = P_inh_basis @ P_inh_basis.T  # Projector

print(f"\nUnion of all 16D null spaces (in 32D): spans {inherited_dim} dimensions")
print(f"  (16D has 15 imaginary units; null spaces span {inherited_dim} of 16 lower dims)")

# ============================================================
# PROPER ORTHOGONAL DECOMPOSITION of each 32D null space
# ============================================================
print(f"\n{'='*80}")
print(f"ORTHOGONAL DECOMPOSITION: 32D null space = inherited + new")
print(f"{'='*80}")

results = []
for (i, j, ns32) in zd32:
    ndim = ns32.shape[0]

    # Project each null space basis vector onto inherited subspace
    # ns32 has shape (ndim, 32), rows are basis vectors
    # Projected: P_inh @ ns32.T gives inherited components

    ns32_vecs = ns32.T  # 32 x ndim
    inh_component = P_inh @ ns32_vecs  # 32 x ndim
    new_component = ns32_vecs - inh_component  # 32 x ndim

    # The inherited and new components span subspaces
    # Use SVD to find their ranks
    _, S_inh, _ = np.linalg.svd(inh_component, full_matrices=False)
    _, S_new, _ = np.linalg.svd(new_component, full_matrices=False)

    rank_inh = np.sum(S_inh > 1e-8)
    rank_new = np.sum(S_new > 1e-8)

    # Category based on index positions
    if i < 16 and j < 16:
        idx_cat = "SS"  # sedenion-sedenion
    elif i < 16 or j < 16:
        idx_cat = "SN"  # sedenion-new
    else:
        idx_cat = "NN"  # new-new

    results.append({
        'pair': (i,j), 'ndim': ndim,
        'rank_inh': rank_inh, 'rank_new': rank_new,
        'idx_cat': idx_cat
    })

# ============================================================
# Print results organized by null_dim and index category
# ============================================================
for ndim_val in sorted(set(r['ndim'] for r in results)):
    subset = [r for r in results if r['ndim'] == ndim_val]
    print(f"\n--- null_dim = {ndim_val} ({len(subset)} pairs) ---")

    by_cat = {}
    for r in subset:
        cat = r['idx_cat']
        if cat not in by_cat: by_cat[cat] = []
        by_cat[cat].append(r)

    for cat in sorted(by_cat.keys()):
        group = by_cat[cat]
        inh_vals = [r['rank_inh'] for r in group]
        new_vals = [r['rank_new'] for r in group]
        print(f"\n  Index category '{cat}': {len(group)} pairs")
        print(f"    inherited rank: min={min(inh_vals)}, max={max(inh_vals)}, "
              f"mean={np.mean(inh_vals):.2f}")
        print(f"    new rank:       min={min(new_vals)}, max={max(new_vals)}, "
              f"mean={np.mean(new_vals):.2f}")
        # Show a few examples
        for r in group[:3]:
            p = r['pair']
            print(f"    ({p[0]:2d},{p[1]:2d}): inherited={r['rank_inh']}, new={r['rank_new']}")

# ============================================================
# TOTAL DOUBLET COUNTING
# ============================================================
print(f"\n{'='*80}")
print(f"DOUBLET BUDGET (1 doublet = 4 real null dims)")
print(f"{'='*80}")

for ndim_val in sorted(set(r['ndim'] for r in results)):
    subset = [r for r in results if r['ndim'] == ndim_val]
    n_pairs = len(subset)
    doublets_per_pair = ndim_val // 4

    total_inh = sum(r['rank_inh'] for r in subset)
    total_new = sum(r['rank_new'] for r in subset)
    total_dims = n_pairs * ndim_val

    print(f"\nnull_dim={ndim_val}: {n_pairs} pairs x {doublets_per_pair} doublets = "
          f"{n_pairs * doublets_per_pair} doublets ({total_dims} null dims)")
    print(f"  Total inherited dims: {total_inh} -> ~{total_inh/4:.0f} inherited doublets")
    print(f"  Total new dims:       {total_new} -> ~{total_new/4:.0f} new doublets")
    print(f"  inherited fraction: {total_inh/total_dims:.4f}")
    print(f"  new fraction:       {total_new/total_dims:.4f}")
    print(f"  SUM CHECK: {total_inh} + {total_new} vs {total_dims} total")
    # Note: these don't add up exactly because projection doesn't preserve orthogonality

# ============================================================
# More precise: compute overlap dimension via Gram matrix
# ============================================================
print(f"\n{'='*80}")
print(f"PRECISE DECOMPOSITION via intersection dimensions")
print(f"{'='*80}")

print("\nFor each 32D null space V, compute:")
print("  dim(V ∩ inherited_subspace) = inherited doublet content")
print("  dim(V) - dim(V ∩ inherited) = genuinely new doublet content")

precise_results = []
for (i, j, ns32) in zd32:
    ndim = ns32.shape[0]

    # Compute dim(null_space ∩ inherited_subspace)
    # This is the dimension of vectors in null space that also lie in inherited subspace
    # Method: project null space basis onto inherited subspace, find rank

    # The null space basis: ns32 (ndim x 32)
    # Inherited subspace basis: P_inh_basis (32 x inherited_dim)

    # Overlap = null space vectors projected onto inherited subspace
    # Then find how many independent vectors in the null space
    # have their entire content within the inherited subspace

    # Better: compute the Gram matrix of ns32 vectors with inherited basis
    # and find the dimension of the intersection

    # Stack bases: [ns32^T | P_inh_basis] (32 x (ndim + inherited_dim))
    combined = np.hstack([ns32.T, P_inh_basis])
    rank_combined = np.linalg.matrix_rank(combined, tol=1e-8)
    rank_ns = ndim
    rank_inh = inherited_dim

    # dim(V ∩ W) = dim(V) + dim(W) - dim(V + W)
    intersection_dim = rank_ns + rank_inh - rank_combined

    if i < 16 and j < 16:
        idx_cat = "SS"
    elif i < 16 or j < 16:
        idx_cat = "SN"
    else:
        idx_cat = "NN"

    precise_results.append({
        'pair': (i,j), 'ndim': ndim,
        'intersection': intersection_dim,
        'new': ndim - intersection_dim,
        'idx_cat': idx_cat
    })

# Print results
for ndim_val in sorted(set(r['ndim'] for r in precise_results)):
    subset = [r for r in precise_results if r['ndim'] == ndim_val]
    print(f"\n--- null_dim = {ndim_val} ({len(subset)} pairs) ---")

    by_cat = {}
    for r in subset:
        cat = r['idx_cat']
        if cat not in by_cat: by_cat[cat] = []
        by_cat[cat].append(r)

    for cat in sorted(by_cat.keys()):
        group = by_cat[cat]
        inh_vals = [r['intersection'] for r in group]
        new_vals = [r['new'] for r in group]
        inh_set = set(inh_vals)
        new_set = set(new_vals)

        print(f"\n  Index category '{cat}': {len(group)} pairs")
        print(f"    dim(V ∩ inherited): values = {sorted(inh_set)}")
        print(f"    dim(genuinely new): values = {sorted(new_set)}")
        print(f"    -> inherited doublets: {sorted(set(v//4 for v in inh_vals))}")
        print(f"    -> new doublets:       {sorted(set(v//4 for v in new_vals))}")

        for r in group[:3]:
            p = r['pair']
            print(f"    ({p[0]:2d},{p[1]:2d}): intersection={r['intersection']}, "
                  f"new={r['new']}")

# ============================================================
# GRAND TOTAL
# ============================================================
print(f"\n{'='*80}")
print(f"GRAND TOTAL: DOUBLET DEPTH CLASSIFICATION")
print(f"{'='*80}")

total_inherited = sum(r['intersection'] for r in precise_results)
total_new = sum(r['new'] for r in precise_results)
total_null = sum(r['ndim'] for r in precise_results)

print(f"\nAcross all {len(precise_results)} 32D ZD pairs:")
print(f"  Total null space dims:        {total_null}")
print(f"  Inherited dims (depth 1):     {total_inherited}")
print(f"  New dims (depth 2):           {total_new}")
print(f"  Sum check: {total_inherited} + {total_new} = {total_inherited + total_new} "
      f"(should equal {total_null})")

print(f"\nIn doublet units (÷4):")
print(f"  Total doublets:    {total_null // 4}")
print(f"  Depth-1 doublets:  {total_inherited // 4}")
print(f"  Depth-2 doublets:  {total_new // 4}")

print(f"\nBy null_dim category:")
for ndim_val in sorted(set(r['ndim'] for r in precise_results)):
    subset = [r for r in precise_results if r['ndim'] == ndim_val]
    n_pairs = len(subset)
    inh = sum(r['intersection'] for r in subset)
    new = sum(r['new'] for r in subset)
    tot = sum(r['ndim'] for r in subset)
    print(f"  null_dim={ndim_val:2d}: {n_pairs:3d} pairs | "
          f"inherited={inh:5d} ({inh/tot:.2%}) | "
          f"new={new:5d} ({new/tot:.2%}) | "
          f"inherited_doublets={inh//4:4d} | new_doublets={new//4:4d}")

print(f"\nBy index category:")
for cat in sorted(set(r['idx_cat'] for r in precise_results)):
    subset = [r for r in precise_results if r['idx_cat'] == cat]
    n_pairs = len(subset)
    inh = sum(r['intersection'] for r in subset)
    new = sum(r['new'] for r in subset)
    tot = sum(r['ndim'] for r in subset)
    cat_label = {'SS': 'both<16 (sedenion-sedenion)',
                 'SN': 'mixed (sedenion-new)',
                 'NN': 'both>=16 (new-new)'}[cat]
    print(f"  {cat_label:35s}: {n_pairs:3d} pairs | "
          f"inherited={inh:5d} | new={new:5d} | "
          f"inh_doublets={inh//4:4d} | new_doublets={new//4:4d}")

# ============================================================
# Key structural observation
# ============================================================
print(f"\n{'='*80}")
print(f"KEY STRUCTURAL OBSERVATIONS")
print(f"{'='*80}")

print(f"""
1. CD DOUBLING STRUCTURE:
   The 16D sedenion embeds in 32D as indices 0-15.
   CD doubling means 32D = 16D ⊕ 16D as vector spaces,
   but multiplication mixes the two halves.

2. INHERITED SUBSPACE:
   The union of all 42 sedenion null spaces (each 4D) spans
   {inherited_dim} dimensions when embedded as (v,0) in 32D.
   This is the "depth-1 reservoir" that 32D null spaces can draw from.

3. NULL SPACE STRUCTURE AT 32D:
   - null_dim=4 pairs: 84 pairs, each null space barely touches inherited
   - null_dim=8 pairs: 84 pairs (includes the 42 sedenion-sedenion pairs)
   - null_dim=12 pairs: 126 pairs, largest null spaces

4. DEPTH CLASSIFICATION:
   Depth 1 = doublets whose null-space directions lie entirely in the
             span of 16D null spaces embedded as (v,0).
   Depth 2 = doublets requiring the upper-16 half (genuinely new at 32D).

5. PHYSICAL IMPLICATION FOR MASS MODEL:
   Inherited doublets suppress via shorter path integrals (depth 1),
   New doublets need longer paths (depth 2) → heavier masses.
""")

# ============================================================
# Specific doublet-level inheritance map
# ============================================================
print(f"{'='*80}")
print(f"WHICH 16D ZD PAIRS PARENT EACH 32D PAIR?")
print(f"{'='*80}")

# For a 32D pair, find which 16D pairs' null spaces have nonzero
# intersection with the 32D pair's null space

for ndim_val in sorted(set(r['ndim'] for r in precise_results)):
    subset_32 = [(i,j,ns) for (i,j,ns) in zd32 if ns.shape[0] == ndim_val]
    print(f"\n--- 32D null_dim={ndim_val} ---")

    for (i32, j32, ns32) in subset_32[:3]:
        parents = []
        for (i16, j16, ns16) in zd16:
            # Embed 16D null in 32D
            ns16_32 = np.zeros((ns16.shape[0], 32))
            ns16_32[:, :16] = ns16

            # Intersection dimension
            combined = np.hstack([ns32.T, ns16_32.T])
            rank_comb = np.linalg.matrix_rank(combined, tol=1e-8)
            inter = ns32.shape[0] + ns16.shape[0] - rank_comb
            if inter > 0:
                parents.append(((i16, j16), inter))

        parents.sort(key=lambda x: -x[1])
        n_with_overlap = len(parents)
        total_inter = sum(d for _, d in parents)
        print(f"\n  32D ({i32:2d},{j32:2d}): {n_with_overlap} 16D parents, "
              f"total intersection dims = {total_inter}")
        for (pp, d) in parents[:6]:
            print(f"    <- 16D ({pp[0]:2d},{pp[1]:2d}): intersection dim = {d}")
        if len(parents) > 6:
            print(f"    ... and {len(parents)-6} more")
