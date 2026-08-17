#!/usr/bin/env python3
# LONGINUS: sourceId=zd64_analysis, sourcePath=zd64_analysis.py
"""
64D Cayley-Dickson Algebra: Zero Divisor Structure Analysis for ORCA Theory

Computes ZD pairs, null space dimensions, doublet counts, and mass formula extrapolation.
"""

import numpy as np
from itertools import combinations
import time

# ============================================================
# 1. Cayley-Dickson multiplication table for 2^n dimensions
# ============================================================

def cayley_dickson_mult_table(n):
    """
    Build multiplication table for 2^n-dimensional Cayley-Dickson algebra.
    Returns (sign, index) arrays such that e_i * e_j = sign[i,j] * e_{index[i,j]}
    """
    dim = 2**n
    # Start with reals: e0*e0 = e0
    sign = np.ones((1, 1), dtype=np.int8)
    idx = np.zeros((1, 1), dtype=np.int32)
    
    for _ in range(n):
        d = sign.shape[0]
        new_sign = np.zeros((2*d, 2*d), dtype=np.int8)
        new_idx = np.zeros((2*d, 2*d), dtype=np.int32)
        
        # Cayley-Dickson doubling formula:
        # (a, b)(c, d) = (ac - d*b, da + bc*)
        # where c* is conjugate of c: if c = e_0, c*=e_0; if c = e_i (i>0), c* = -e_i
        
        for i in range(2*d):
            for j in range(2*d):
                if i < d and j < d:
                    # (a,0)*(c,0) = (ac, 0)
                    new_sign[i, j] = sign[i, j]
                    new_idx[i, j] = idx[i, j]
                elif i < d and j >= d:
                    # (a,0)*(0,d) = (0, da)
                    # Actually: (a,0)*(c,d) with c=0,d=e_{j-d}
                    # = (0*a - d_conj * 0, d*a + 0*a_conj) -- no
                    # Let me use the standard formula more carefully.
                    # (a,b)(c,d) = (ac - d*b, da + bc*)
                    # Here a=e_i, b=0, c=0, d=e_{j-d}
                    # = (0 - conj(e_{j-d})*0, e_{j-d}*e_i + 0) = (0, e_{j-d}*e_i)
                    jj = j - d
                    new_sign[i, j] = sign[jj, i]  # d*a
                    new_idx[i, j] = idx[jj, i] + d
                elif i >= d and j < d:
                    # (0,b)*(c,0) = (0, 0 + b*conj(c))
                    # a=0, b=e_{i-d}, c=e_j, d=0
                    # = (0 - 0, 0 + e_{i-d}*conj(e_j))
                    ii = i - d
                    if j == 0:
                        # conj(e_0) = e_0
                        new_sign[i, j] = sign[ii, j]
                        new_idx[i, j] = idx[ii, j] + d
                    else:
                        # conj(e_j) = -e_j
                        new_sign[i, j] = -sign[ii, j]
                        new_idx[i, j] = idx[ii, j] + d
                else:
                    # (0,b)*(0,d) = (-conj(d)*b, 0)
                    # a=0, b=e_{i-d}, c=0, d=e_{j-d}
                    # = (-conj(e_{j-d})*e_{i-d}, 0)
                    ii = i - d
                    jj = j - d
                    if jj == 0:
                        # conj(e_0) = e_0
                        new_sign[i, j] = -sign[jj, ii]
                        new_idx[i, j] = idx[jj, ii]
                    else:
                        new_sign[i, j] = sign[jj, ii]
                        new_idx[i, j] = idx[jj, ii]
        
        sign = new_sign
        idx = new_idx
    
    return sign, idx

def build_left_mult_matrix(sign, idx, dim, a_vec):
    """
    Build the 64x64 matrix L_a such that L_a @ x = a * x
    in the Cayley-Dickson algebra.
    """
    L = np.zeros((dim, dim), dtype=np.float64)
    for j in range(dim):
        for i in range(dim):
            if a_vec[i] != 0:
                target = idx[i, j]
                L[target, j] += sign[i, j] * a_vec[i]
    return L

def build_right_mult_matrix(sign, idx, dim, b_vec):
    """
    Build the 64x64 matrix R_b such that R_b @ x = x * b
    """
    R = np.zeros((dim, dim), dtype=np.float64)
    for i in range(dim):
        for j in range(dim):
            if b_vec[j] != 0:
                target = idx[i, j]
                R[target, i] += sign[i, j] * b_vec[j]
    return R

# ============================================================
# 2. Verify multiplication table
# ============================================================

print("="*70)
print("64D CAYLEY-DICKSON ALGEBRA: ZERO DIVISOR ANALYSIS")
print("="*70)

t0 = time.time()

print("\nBuilding 64D multiplication table...")
sign64, idx64 = cayley_dickson_mult_table(6)  # 2^6 = 64
DIM = 64

# Quick verification: e_i * e_i should = -e_0 for i>0
print("Verification: e_i * e_i for i=1..5:")
for i in range(1, 6):
    t_idx = idx64[i, i]
    t_sign = sign64[i, i]
    print(f"  e_{i} * e_{i} = {'+' if t_sign>0 else '-'}e_{t_idx}")
assert all(idx64[i,i] == 0 and sign64[i,i] == -1 for i in range(1, DIM)), "Failed: e_i^2 != -1"
print("  ✓ All e_i^2 = -e_0 for i>0")

# ============================================================
# 3. Compute ALL cross-sector ZD pairs (i in 1..31, j in 32..63)
# ============================================================

print("\n" + "="*70)
print("COMPUTING CROSS-SECTOR ZERO DIVISOR PAIRS")
print("Sector A: basis elements e_1 .. e_31")
print("Sector B: basis elements e_32 .. e_63")
print("="*70)

sector_A = list(range(1, 32))   # e_1 to e_31
sector_B = list(range(32, 64))  # e_32 to e_63

# For unit imaginary basis elements e_i, the product e_i * e_j
# The ZD condition: find pairs where L_{e_i} has nontrivial kernel
# But for basis elements, e_i * e_j = ± e_k (single basis element), never zero.
# ZDs arise from LINEAR COMBINATIONS.

# Standard approach: for each pair of basis indices (i,j) with i in A, j in B,
# compute the left multiplication matrix for (e_i + e_j) and find its kernel.
# If ker is nontrivial, we have zero divisors.

# Actually, a ZD pair (a, b) means a*b = 0 with a,b ≠ 0.
# For Cayley-Dickson, canonical ZD pairs come from:
#   a = e_i + e_j,  and we look for b in ker(L_a).

print("\nComputing null spaces for all (e_i + e_j) pairs, i∈A, j∈B...")

null_dims = {}
zd_pairs = []
null_dim_counts = {}

total_pairs = len(sector_A) * len(sector_B)
count = 0
t1 = time.time()

for i in sector_A:
    a_vec = np.zeros(DIM)
    a_vec[i] = 1.0
    
    for j in sector_B:
        a_full = a_vec.copy()
        a_full[j] = 1.0
        
        # Build left multiplication matrix
        L = build_left_mult_matrix(sign64, idx64, DIM, a_full)
        
        # SVD to find null space dimension
        s = np.linalg.svd(L, compute_uv=False)
        # Count near-zero singular values
        tol = 1e-10 * s[0] if s[0] > 0 else 1e-10
        nd = int(np.sum(s < tol))
        
        if nd > 0:
            zd_pairs.append((i, j, nd))
            null_dim_counts[nd] = null_dim_counts.get(nd, 0) + 1
        
        count += 1

t2 = time.time()
print(f"Computed {count} pairs in {t2-t1:.2f}s")

print(f"\nTotal ZD pairs found: {len(zd_pairs)}")
print(f"\nNull dimension distribution:")
for nd in sorted(null_dim_counts.keys()):
    print(f"  null_dim = {nd:3d}: {null_dim_counts[nd]:5d} pairs")

# ============================================================
# 4. Also check within-sector pairs for completeness
# ============================================================

print("\n" + "="*70)
print("WITHIN-SECTOR ZD PAIRS (for completeness)")
print("="*70)

# Sector A internal
within_A_counts = {}
within_A_zd = []
for i, j in combinations(sector_A, 2):
    a_vec = np.zeros(DIM)
    a_vec[i] = 1.0
    a_vec[j] = 1.0
    L = build_left_mult_matrix(sign64, idx64, DIM, a_vec)
    s = np.linalg.svd(L, compute_uv=False)
    tol = 1e-10 * s[0] if s[0] > 0 else 1e-10
    nd = int(np.sum(s < tol))
    if nd > 0:
        within_A_zd.append((i, j, nd))
        within_A_counts[nd] = within_A_counts.get(nd, 0) + 1

print(f"\nWithin Sector A (e_1..e_31): {len(within_A_zd)} ZD pairs")
for nd in sorted(within_A_counts.keys()):
    print(f"  null_dim = {nd:3d}: {within_A_counts[nd]:5d} pairs")

# Sector B internal
within_B_counts = {}
within_B_zd = []
for i, j in combinations(sector_B, 2):
    a_vec = np.zeros(DIM)
    a_vec[i] = 1.0
    a_vec[j] = 1.0
    L = build_left_mult_matrix(sign64, idx64, DIM, a_vec)
    s = np.linalg.svd(L, compute_uv=False)
    tol = 1e-10 * s[0] if s[0] > 0 else 1e-10
    nd = int(np.sum(s < tol))
    if nd > 0:
        within_B_zd.append((i, j, nd))
        within_B_counts[nd] = within_B_counts.get(nd, 0) + 1

print(f"\nWithin Sector B (e_32..e_63): {len(within_B_zd)} ZD pairs")
for nd in sorted(within_B_counts.keys()):
    print(f"  null_dim = {nd:3d}: {within_B_counts[nd]:5d} pairs")

# ============================================================
# 5. Full ZD count: all pairs across all 63 imaginary units
# ============================================================

print("\n" + "="*70)
print("ALL PAIRS (e_i + e_j), 1 ≤ i < j ≤ 63")
print("="*70)

all_zd = []
all_counts = {}
# Combine all
for zp_list in [zd_pairs, within_A_zd, within_B_zd]:
    for (i, j, nd) in zp_list:
        all_zd.append((i, j, nd))
        # already counted above, let's recount
        
# Also need cross pairs where both in A or mixed differently
# Actually we covered: within_A (1..31 x 1..31), cross (1..31 x 32..63), within_B (32..63 x 32..63)
# That's all C(63,2) pairs.

all_counts = {}
for (i, j, nd) in all_zd:
    all_counts[nd] = all_counts.get(nd, 0) + 1

total_zd = len(all_zd)
total_possible = 63 * 62 // 2

print(f"\nTotal ZD pairs: {total_zd} out of {total_possible} possible")
print(f"\nNull dimension distribution (ALL pairs):")
for nd in sorted(all_counts.keys()):
    print(f"  null_dim = {nd:3d}: {all_counts[nd]:5d} pairs")

# ============================================================
# 6. Doublet analysis
# ============================================================

print("\n" + "="*70)
print("DOUBLET ANALYSIS")
print("="*70)
print("Doublets per ZD pair = null_dim / 2 (from Casimir = -3/4 SU(2) pattern)")

total_doublets = 0
print(f"\n{'null_dim':>10} {'#pairs':>10} {'doub/pair':>10} {'total_doub':>12}")
print("-" * 45)
for nd in sorted(all_counts.keys()):
    n_pairs = all_counts[nd]
    doub_per = nd // 2
    td = n_pairs * doub_per
    total_doublets += td
    print(f"{nd:10d} {n_pairs:10d} {doub_per:10d} {td:12d}")
print("-" * 45)
print(f"{'TOTAL':>10} {total_zd:10d} {'':>10} {total_doublets:12d}")

# ============================================================
# 7. Comparison across dimensions
# ============================================================

print("\n" + "="*70)
print("CROSS-DIMENSIONAL COMPARISON")
print("="*70)

print(f"\n{'Dim':>5} {'ZD pairs':>10} {'Doublets':>10} {'Null dims observed':>30}")
print("-" * 60)
print(f"{'16D':>5} {'42':>10} {'42':>10} {'  {4}':>30}")
# 32D from context
print(f"{'32D':>5} {'294':>10} {'630':>10} {'  {4, 8, 12}':>30}")

nd_set = sorted(all_counts.keys())
print(f"{'64D':>5} {total_zd:>10} {total_doublets:>10} {'  ' + str(set(nd_set)):>30}")

# ============================================================
# 8. Quark mass formula analysis
# ============================================================

print("\n" + "="*70)
print("QUARK MASS FORMULA ANALYSIS")
print("="*70)

# Previous result from context: m ~ null_dim^5.75
# with 32D: null_dims {4, 12, 28} → {u, c, t}
# m_t/m_c = (28/12)^5.75 ≈ 130 vs experimental 136 (4% off)

# Now with 64D data, we have null_dims = nd_set
# The pattern 4*{1,3,5,7} = {4,12,20,28}

print("\n--- Previous 32D result ---")
print("Null dims used: {4, 12, 28}")
print("Power law: m ~ null_dim^alpha, alpha = 5.75")

alpha_prev = 5.75
ratio_tc_32 = (28/12)**alpha_prev
ratio_cu_32 = (12/4)**alpha_prev
print(f"m_t/m_c = (28/12)^{alpha_prev} = {ratio_tc_32:.1f}  (exp: 136)")
print(f"m_c/m_u = (12/4)^{alpha_prev} = {ratio_cu_32:.1f}  (exp: ~553)")

# Experimental quark masses (PDG central values, MS-bar at 2 GeV for u,d; pole for t)
m_u = 2.16e-3  # GeV
m_c = 1.27     # GeV
m_t = 172.69   # GeV
ratio_tc_exp = m_t / m_c
ratio_cu_exp = m_c / m_u

print(f"\nExperimental ratios:")
print(f"  m_t/m_c = {ratio_tc_exp:.1f}")
print(f"  m_c/m_u = {ratio_cu_exp:.1f}")

print("\n--- 64D analysis ---")
print(f"Null dims available: {nd_set}")

# Try mapping: which triplet of null_dims best fits {u, c, t}?
# We need n1 < n2 < n3 and fit m ~ n^alpha
# Best fit: find alpha that minimizes error on both ratios

from itertools import combinations as comb3

print("\nSearching for best (n_u, n_c, n_t) triplet and alpha...")
print(f"\n{'n_u':>5} {'n_c':>5} {'n_t':>5} {'alpha':>8} {'m_t/m_c':>10} {'m_c/m_u':>10} {'err_tc%':>10} {'err_cu%':>10} {'tot_err%':>10}")
print("-" * 80)

best_results = []

for combo in comb3(nd_set, 3):
    n_u, n_c, n_t = combo
    if n_u == 0 or n_c == 0 or n_t == 0:
        continue
    
    # Fit alpha from t/c ratio: (n_t/n_c)^alpha = 136
    # and from c/u ratio: (n_c/n_u)^alpha = 588
    # Use geometric mean of the two alphas
    
    r_tc = n_t / n_c
    r_cu = n_c / n_u
    
    if r_tc <= 1 or r_cu <= 1:
        continue
    
    alpha_tc = np.log(ratio_tc_exp) / np.log(r_tc)
    alpha_cu = np.log(ratio_cu_exp) / np.log(r_cu)
    
    # Use average alpha
    alpha_avg = (alpha_tc + alpha_cu) / 2
    
    pred_tc = r_tc ** alpha_avg
    pred_cu = r_cu ** alpha_avg
    
    err_tc = abs(pred_tc - ratio_tc_exp) / ratio_tc_exp * 100
    err_cu = abs(pred_cu - ratio_cu_exp) / ratio_cu_exp * 100
    tot_err = (err_tc + err_cu) / 2
    
    best_results.append((tot_err, n_u, n_c, n_t, alpha_avg, pred_tc, pred_cu, err_tc, err_cu))

best_results.sort()

for tot_err, n_u, n_c, n_t, alpha, pred_tc, pred_cu, err_tc, err_cu in best_results[:15]:
    print(f"{n_u:5d} {n_c:5d} {n_t:5d} {alpha:8.3f} {pred_tc:10.1f} {pred_cu:10.1f} {err_tc:10.1f} {err_cu:10.1f} {tot_err:10.1f}")

print("\n--- Best fit analysis ---")
tot_err, n_u, n_c, n_t, alpha, pred_tc, pred_cu, err_tc, err_cu = best_results[0]
print(f"Best triplet: n_u={n_u}, n_c={n_c}, n_t={n_t}")
print(f"Best alpha: {alpha:.4f}")
print(f"Predicted m_t/m_c = {pred_tc:.1f}  (exp: {ratio_tc_exp:.1f}, err: {err_tc:.1f}%)")
print(f"Predicted m_c/m_u = {pred_cu:.1f}  (exp: {ratio_cu_exp:.1f}, err: {err_cu:.1f}%)")
print(f"Average error: {tot_err:.1f}%")

# Compare with 32D-only result
print(f"\n--- Comparison: 32D vs 64D ---")
print(f"32D: (4,12,28) → alpha=5.75, m_t/m_c err ≈ 4%")
print(f"64D: ({n_u},{n_c},{n_t}) → alpha={alpha:.3f}, avg err = {tot_err:.1f}%")

# ============================================================
# 9. Fourth generation prediction
# ============================================================

print("\n" + "="*70)
print("FOURTH GENERATION PREDICTION")
print("="*70)

# If the pattern extends, what null_dim would a 4th generation use?
# And what mass would it predict?

print(f"\nNull dims in 64D: {nd_set}")
print(f"Pattern check: are these 4×{{1,3,5,7,...}}?")

nd_arr = np.array(nd_set)
if len(nd_arr) > 0 and nd_arr[0] != 0:
    ratios = nd_arr / 4.0
    print(f"  null_dim / 4 = {list(ratios)}")

# Using best-fit triplet, predict 4th gen with next null_dim
print(f"\nUsing best triplet ({n_u},{n_c},{n_t}) with alpha={alpha:.3f}:")

# Find null_dims larger than n_t
higher_nds = [nd for nd in nd_set if nd > n_t]
print(f"Available null_dims > {n_t}: {higher_nds}")

if higher_nds:
    for n4 in higher_nds:
        m4_over_mt = (n4 / n_t) ** alpha
        m4 = m4_over_mt * m_t
        print(f"  n_4 = {n4}: m_4/m_t = {m4_over_mt:.2f}, m_4 = {m4:.1f} GeV")

# Also extrapolate the series: if nd = 4*(2k-1), next after 28 is 4*9=36, etc.
print(f"\nExtrapolating null_dim series 4×{{1,3,5,7,...}}:")
print(f"  Next: 4×9=36, 4×11=44, 4×13=52, 4×15=60")
for n4 in [36, 44, 52, 60]:
    if n4 > n_t:
        m4_over_mt = (n4 / n_t) ** alpha
        m4 = m4_over_mt * m_t
        print(f"  n_4 = {n4}: m_4 = {m4:.1f} GeV")

# ============================================================
# 10. Refined alpha fit: use all three ratios simultaneously
# ============================================================

print("\n" + "="*70)
print("REFINED POWER LAW FIT (least squares)")
print("="*70)

# Fit: log(m) = alpha * log(n) + beta
# Using (m_u, m_c, m_t) and best (n_u, n_c, n_t)
from numpy.linalg import lstsq

masses = np.array([m_u, m_c, m_t])
nds_best = np.array([n_u, n_c, n_t])

A_mat = np.column_stack([np.log(nds_best), np.ones(3)])
b_vec = np.log(masses)
result = lstsq(A_mat, b_vec, rcond=None)
alpha_fit, beta_fit = result[0]
residuals = b_vec - A_mat @ result[0]

print(f"Fit: log(m) = {alpha_fit:.4f} * log(n) + {beta_fit:.4f}")
print(f"  → m = {np.exp(beta_fit):.6e} × n^{alpha_fit:.4f}")
print(f"Residuals (log space): {residuals}")
print(f"RMS residual: {np.sqrt(np.mean(residuals**2)):.4f}")

# Predictions with this fit
print(f"\nPredicted masses:")
for nd_val, m_exp, name in zip(nds_best, masses, ['u', 'c', 't']):
    m_pred = np.exp(beta_fit) * nd_val**alpha_fit
    err = abs(m_pred - m_exp)/m_exp * 100
    print(f"  {name}: n={nd_val}, m_pred={m_pred:.4f} GeV, m_exp={m_exp:.4f} GeV, err={err:.1f}%")

# 4th gen prediction with refined fit
print(f"\n4th generation predictions (refined fit):")
for n4 in higher_nds + [36, 44, 52, 60]:
    if n4 > n_t:
        m4 = np.exp(beta_fit) * n4**alpha_fit
        print(f"  n_4 = {n4}: m_4 = {m4:.1f} GeV")

# ============================================================
# 11. Detailed null space structure for select pairs
# ============================================================

print("\n" + "="*70)
print("NULL SPACE STRUCTURE: SAMPLE ANALYSIS")
print("="*70)

# For a few representative pairs, show the actual null space basis
for nd_target in sorted(all_counts.keys()):
    # Find first pair with this null_dim
    sample = None
    for (i, j, nd) in all_zd:
        if nd == nd_target:
            sample = (i, j)
            break
    if sample is None:
        continue
    
    i, j = sample
    a_vec = np.zeros(DIM)
    a_vec[i] = 1.0
    a_vec[j] = 1.0
    L = build_left_mult_matrix(sign64, idx64, DIM, a_vec)
    U, S, Vt = np.linalg.svd(L)
    tol = 1e-10 * S[0]
    null_mask = S < tol
    null_basis = Vt[null_mask]
    
    print(f"\nnull_dim={nd_target}: sample pair (e_{i}, e_{j})")
    print(f"  Null space dimension: {null_basis.shape[0]}")
    print(f"  Null basis vectors (nonzero components):")
    for k, v in enumerate(null_basis[:min(3, len(null_basis))]):
        nz = np.where(np.abs(v) > 1e-10)[0]
        components = [(int(idx), f"{v[idx]:+.4f}") for idx in nz]
        print(f"    v_{k}: {components[:8]}{'...' if len(components)>8 else ''}")

# ============================================================
# Summary
# ============================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
64D Cayley-Dickson Algebra Zero Divisor Analysis:

1. TOTAL ZD PAIRS: {total_zd} / {total_possible} possible basis-pair combinations
   - Cross-sector (A×B): {len(zd_pairs)}
   - Within sector A: {len(within_A_zd)}  
   - Within sector B: {len(within_B_zd)}

2. NULL DIMENSION DISTRIBUTION:""")
for nd in sorted(all_counts.keys()):
    print(f"   null_dim={nd}: {all_counts[nd]} pairs")

print(f"""
3. DOUBLET COUNT: {total_doublets} total doublets

4. DIMENSIONAL PROGRESSION:
   16D: 42 ZD pairs, 42 doublets, null_dims = {{4}}
   32D: 294 ZD pairs, 630 doublets, null_dims = {{4, 8, 12}}
   64D: {total_zd} ZD pairs, {total_doublets} doublets, null_dims = {set(nd_set)}

5. MASS FORMULA:
   Best fit: ({n_u},{n_c},{n_t}) → (u,c,t)
   Power law: m ~ n^{alpha_fit:.4f}
   Average ratio error: {tot_err:.1f}%
   {'IMPROVEMENT' if tot_err < 4 else 'COMPARABLE' if tot_err < 6 else 'WORSE'} vs 32D (4%)

6. 4TH GENERATION:""")
if higher_nds:
    n4 = higher_nds[0]
    m4 = np.exp(beta_fit) * n4**alpha_fit
    print(f"   Lowest available n_4 = {n4}: m_4 ≈ {m4:.0f} GeV")

elapsed = time.time() - t0
print(f"\nTotal computation time: {elapsed:.1f}s")

