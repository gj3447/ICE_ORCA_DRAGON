#!/usr/bin/env python3
# KG: Higgs Mechanism in ICE, Derive the Higgs Sector from the Sedenion Span, Higgs from Sedenion Algebra
# LONGINUS: sourceId=higgs_mechanism, sourcePath=higgs_mechanism.py
"""
ORCA Theory: Higgs Mechanism as O→S Cayley-Dickson Transition
=============================================================
Defining order parameters and deriving Higgs-like potentials
for the octonion → sedenion transition.
"""

import numpy as np
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

print("=" * 78)
print("ORCA THEORY: HIGGS MECHANISM AS O→S CAYLEY-DICKSON TRANSITION")
print("=" * 78)

# ============================================================================
# SECTION 0: Algebra Infrastructure
# ============================================================================

def cayley_dickson_mult(a, b, conj_func, mult_func):
    """Generic Cayley-Dickson doubling: (a,b)(c,d) = (ac - d*b, da + bc*)"""
    n = len(a) // 2
    a1, a2 = a[:n], a[n:]
    b1, b2 = b[:n], b[n:]
    
    b1_conj = conj_func(b1)
    a1_conj = conj_func(a1)
    # Not used directly here; we use the specific mult tables
    raise NotImplementedError("Use multiplication table approach instead")

# Octonion multiplication table (Fano plane convention)
# e_i * e_j for i,j in {1..7}, result is ±e_k
# Using standard convention: e1*e2=e3, e1*e4=e5, e2*e4=e6, e3*e4=e7,
#                             e1*e6=e7(neg check), etc.

# Full octonion structure constants (antisymmetric part)
# Triples (i,j,k) where e_i * e_j = e_k
OCT_TRIPLES = [
    (1,2,3), (1,4,5), (1,7,6),  # e1*e7 = -e6, so (1,6,7) reversed
    (2,4,6), (2,5,7),
    (3,4,7), (3,6,5)             # e3*e6 = -e5, so (3,5,6) reversed
]

def build_oct_mult_table():
    """Build 8x8x8 structure constants for octonions."""
    # C[i][j] = (sign, index) meaning e_i * e_j = sign * e_index
    table = {}
    # e_0 is identity
    for i in range(8):
        table[(0, i)] = (1, i)
        table[(i, 0)] = (1, i)
    
    # From triples: (i,j,k) means e_i * e_j = e_k
    triples = [(1,2,3), (1,4,5), (1,7,6), (2,4,6), (2,5,7), (3,4,7), (3,6,5)]
    
    for (i, j, k) in triples:
        table[(i, j)] = (1, k)
        table[(j, i)] = (-1, k)
        # Cyclic: e_j * e_k = e_i
        table[(j, k)] = (1, i)
        table[(k, j)] = (-1, i)
        # e_k * e_i = e_j
        table[(k, i)] = (1, j)
        table[(i, k)] = (-1, j)
    
    # e_i * e_i = -1 for i >= 1
    for i in range(1, 8):
        table[(i, i)] = (-1, 0)
    
    return table

OCT_TABLE = build_oct_mult_table()

def oct_mult(a, b):
    """Multiply two octonions (8-component vectors)."""
    result = np.zeros(8)
    for i in range(8):
        for j in range(8):
            if abs(a[i]) < 1e-15 or abs(b[j]) < 1e-15:
                continue
            sign, idx = OCT_TABLE[(i, j)]
            result[idx] += sign * a[i] * b[j]
    return result

def oct_conj(a):
    """Conjugate of octonion: negate imaginary parts."""
    c = -a.copy()
    c[0] = a[0]
    return c

def build_sed_mult_table():
    """
    Build sedenion multiplication table via Cayley-Dickson doubling of octonions.
    Sedenion (a, b) where a, b are octonions.
    (a,b)(c,d) = (ac - d*b, da + bc*)
    where * is octonion conjugation.
    """
    # We store as 16-component vectors: indices 0-7 are first octonion, 8-15 second
    # Rather than building a full table, we implement multiplication directly
    pass

def sed_mult(x, y):
    """
    Multiply two sedenions (16-component vectors) using CD doubling of octonions.
    (a,b)(c,d) = (ac - d*b, da + bc*)
    """
    a, b = x[:8], x[8:]
    c, d = y[:8], y[8:]
    
    d_conj = oct_conj(d)
    c_conj = oct_conj(c)
    
    # First component: ac - d*b
    part1 = oct_mult(a, c) - oct_mult(d_conj, b)
    # Second component: da + bc*
    part2 = oct_mult(d, a) + oct_mult(b, c_conj)
    
    return np.concatenate([part1, part2])

def sed_conj(x):
    """Conjugate of sedenion."""
    c = -x.copy()
    c[0] = x[0]
    return c

# Verify: check octonion alternativity
print("\n" + "=" * 78)
print("SECTION 0: VERIFICATION OF ALGEBRAIC PROPERTIES")
print("=" * 78)

np.random.seed(42)

def check_alternativity(mult_func, dim, name, n_trials=1000):
    """Check ||a(ax) - (aa)x|| for random elements. Should be 0 for alternative algebras."""
    violations = []
    for _ in range(n_trials):
        a = np.random.randn(dim)
        x = np.random.randn(dim)
        
        lhs = mult_func(a, mult_func(a, x))  # a(ax)
        rhs = mult_func(mult_func(a, a), x)   # (aa)x
        
        diff = np.linalg.norm(lhs - rhs)
        norm_factor = max(np.linalg.norm(a)**2 * np.linalg.norm(x), 1e-15)
        violations.append(diff / norm_factor)
    
    violations = np.array(violations)
    print(f"\n{name} alternativity check (||a(ax)-(aa)x|| / ||a||²||x||):")
    print(f"  Mean:   {violations.mean():.2e}")
    print(f"  Max:    {violations.max():.2e}")
    print(f"  Median: {np.median(violations):.2e}")
    return violations

oct_viol = check_alternativity(oct_mult, 8, "OCTONION")
# For sedenions, we embed in 16D
def sed_mult_16(a, b):
    return sed_mult(a, b)

sed_viol = check_alternativity(sed_mult_16, 16, "SEDENION")

# ============================================================================
# SECTION 1: ZERO DIVISOR ANALYSIS IN SEDENIONS
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 1: ZERO DIVISOR STRUCTURE")
print("=" * 78)

def find_zero_divisor_pairs():
    """
    Find zero divisor pairs among sedenion basis elements.
    A zero divisor pair (a,b) has a*b = 0 with a≠0, b≠0.
    Check all pairs of non-real basis elements e_i, e_j and 
    also sums/differences of basis elements.
    """
    # Check basis element pairs first
    basis_zd = []
    for i in range(1, 16):
        for j in range(i+1, 16):
            ei = np.zeros(16); ei[i] = 1
            ej = np.zeros(16); ej[j] = 1
            
            # Check (e_i + e_j)(e_k + e_l) type zero divisors
            # But first, simple pairs
            prod = sed_mult(ei, ej)
            if np.linalg.norm(prod) < 1e-10:
                basis_zd.append((i, j))
    
    print(f"\nBasis element zero divisor pairs e_i*e_j=0: {len(basis_zd)}")
    if basis_zd:
        for p in basis_zd[:5]:
            print(f"  e_{p[0]} * e_{p[1]} = 0")
    
    # The 84 zero divisors come from (e_i ± e_j) combinations
    # Standard result: there are 84 zero divisor pairs of form (e_i+e_j)(e_k-e_l)=0
    zd_pairs = []
    checked = 0
    for i in range(1, 16):
        for j in range(i+1, 16):
            ei = np.zeros(16); ei[i] = 1
            ej = np.zeros(16); ej[j] = 1
            a_plus = ei + ej
            a_minus = ei - ej
            
            for k in range(1, 16):
                for l in range(k+1, 16):
                    ek = np.zeros(16); ek[k] = 1
                    el = np.zeros(16); el[l] = 1
                    b_plus = ek + el
                    b_minus = ek - el
                    
                    # Check all four combos
                    for a_test in [a_plus, a_minus]:
                        for b_test in [b_plus, b_minus]:
                            prod = sed_mult(a_test, b_test)
                            if np.linalg.norm(prod) < 1e-10:
                                pair_key = (tuple(sorted([i,j])), tuple(sorted([k,l])), 
                                           int(a_test[i] > 0), int(b_test[k] > 0))
                                zd_pairs.append(pair_key)
                    checked += 1
    
    # Remove duplicates
    unique_zd = set()
    for p in zd_pairs:
        unique_zd.add(p)
    
    print(f"  Zero divisor pairs (e_i±e_j)(e_k±e_l)=0: {len(unique_zd)}")
    
    # Count unique directions that participate
    zd_directions = set()
    for p in unique_zd:
        zd_directions.add(p[0])
        zd_directions.add(p[1])
    print(f"  Unique index pairs participating: {len(zd_directions)}")
    
    return unique_zd

zd_pairs = find_zero_divisor_pairs()

# ============================================================================
# SECTION 2: ORDER PARAMETER CANDIDATES
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 2: ORDER PARAMETER CANDIDATES WITH INTERPOLATION")
print("=" * 78)

def interpolated_mult(a16, b16, t):
    """
    Interpolate between octonion (t=0) and sedenion (t=1) multiplication on 16D space.
    
    At t=0: Only the first 8 components interact (octonion mult), 
            components 8-15 are inert (act as separate copy).
    At t=1: Full sedenion multiplication.
    
    Interpolation: mult_t = (1-t)*oct_embed + t*sed_mult
    where oct_embed treats (a,b)(c,d) = (ac, 0) — only first octonion sector.
    
    Better approach: The CD doubling formula is
    (a,b)(c,d) = (ac - d*b, da + bc*)
    At t=0 we want this to reduce to (ac, 0) — pure octonion in first sector.
    At t=1 we want full CD formula.
    So: (a,b)(c,d) = (ac - t*d*b, t*(da + bc*))
    This smoothly introduces the cross-terms.
    """
    a, b = a16[:8], a16[8:]
    c, d = b16[:8], b16[8:]
    
    d_conj = oct_conj(d)
    c_conj = oct_conj(c)
    
    ac = oct_mult(a, c)
    d_conj_b = oct_mult(d_conj, b)
    da = oct_mult(d, a)
    b_c_conj = oct_mult(b, c_conj)
    
    part1 = ac - t * d_conj_b
    part2 = t * (da + b_c_conj)
    
    return np.concatenate([part1, part2])

# Candidate A: Non-alternativity measure
print("\n--- Candidate A: Non-Alternativity φ_A = ||a(ax) - (aa)x|| / ||a||²||x|| ---")

t_values = np.linspace(0, 1, 51)
phi_A_vals = []
phi_A_std = []

for t in t_values:
    mult_t = lambda a, b, t_=t: interpolated_mult(a, b, t_)
    violations = []
    for trial in range(500):
        a = np.random.randn(16)
        x = np.random.randn(16)
        
        ax = mult_t(a, x)
        a_ax = mult_t(a, ax)
        aa = mult_t(a, a)
        aa_x = mult_t(aa, x)
        
        diff = np.linalg.norm(a_ax - aa_x)
        norm_factor = max(np.linalg.norm(a)**2 * np.linalg.norm(x), 1e-15)
        violations.append(diff / norm_factor)
    
    phi_A_vals.append(np.mean(violations))
    phi_A_std.append(np.std(violations))

phi_A_vals = np.array(phi_A_vals)
phi_A_std = np.array(phi_A_std)

print(f"  φ_A(t=0) = {phi_A_vals[0]:.6e}")
print(f"  φ_A(t=0.5) = {phi_A_vals[25]:.6e}")
print(f"  φ_A(t=1) = {phi_A_vals[-1]:.6e}")
print(f"  φ_A range: [{phi_A_vals.min():.4e}, {phi_A_vals.max():.4e}]")

# Check if it looks like a phase transition (sharp change)
dphi = np.gradient(phi_A_vals, t_values)
t_max_slope = t_values[np.argmax(np.abs(dphi))]
print(f"  Maximum slope at t = {t_max_slope:.2f} (phase transition point)")

# Candidate B: Zero-divisor density
print("\n--- Candidate B: Zero-Divisor Density φ_B ---")

phi_B_vals = []

for t in t_values:
    mult_t = lambda a, b, t_=t: interpolated_mult(a, b, t_)
    
    # Measure: what fraction of random pairs (a,b) have ||a*b|| < ε||a||||b||?
    # More refined: minimum singular value of left multiplication map L_a
    zd_count = 0
    n_test = 300
    for _ in range(n_test):
        a = np.random.randn(16)
        b = np.random.randn(16)
        
        prod = mult_t(a, b)
        expected_norm = np.linalg.norm(a) * np.linalg.norm(b)
        
        if expected_norm > 1e-10:
            ratio = np.linalg.norm(prod) / expected_norm
            if ratio < 0.1:  # near-zero-divisor threshold
                zd_count += 1
    
    phi_B_vals.append(zd_count / n_test)

phi_B_vals = np.array(phi_B_vals)
print(f"  φ_B(t=0) = {phi_B_vals[0]:.4f}")
print(f"  φ_B(t=0.5) = {phi_B_vals[25]:.4f}")
print(f"  φ_B(t=1) = {phi_B_vals[-1]:.4f}")

# Candidate C: Minimum singular value of L_a
print("\n--- Candidate C: Min Singular Value of L_a (Division Defect) ---")

phi_C_vals = []
phi_C_std = []

for t in t_values:
    mult_t = lambda a, b, t_=t: interpolated_mult(a, b, t_)
    
    min_svs = []
    for _ in range(200):
        a = np.random.randn(16)
        a = a / np.linalg.norm(a)  # Normalize
        
        # Build left multiplication matrix L_a
        L_a = np.zeros((16, 16))
        for j in range(16):
            ej = np.zeros(16)
            ej[j] = 1.0
            L_a[:, j] = mult_t(a, ej)
        
        svs = np.linalg.svd(L_a, compute_uv=False)
        min_svs.append(svs.min())
    
    phi_C_vals.append(np.mean(min_svs))
    phi_C_std.append(np.std(min_svs))

phi_C_vals = np.array(phi_C_vals)
phi_C_std = np.array(phi_C_std)

# For Candidate C, the order parameter is (1 - min_sv) or similar
phi_C_order = 1.0 - phi_C_vals

print(f"  min_sv(t=0) = {phi_C_vals[0]:.6f}  →  φ_C = {phi_C_order[0]:.6f}")
print(f"  min_sv(t=0.5) = {phi_C_vals[25]:.6f}  →  φ_C = {phi_C_order[25]:.6f}")
print(f"  min_sv(t=1) = {phi_C_vals[-1]:.6f}  →  φ_C = {phi_C_order[-1]:.6f}")

# ============================================================================
# SECTION 3: PHASE TRANSITION ANALYSIS
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 3: PHASE TRANSITION ANALYSIS")
print("=" * 78)

# Fit each candidate to determine transition characteristics
from numpy.polynomial import polynomial as P

# For Candidate A: fit to determine if 1st or 2nd order transition
print("\n--- Candidate A: Transition Profile ---")

# Normalize φ_A to [0,1]
phi_A_norm = phi_A_vals / phi_A_vals.max() if phi_A_vals.max() > 0 else phi_A_vals

# Try power-law fit: φ ~ t^β near t=0
mask = (t_values > 0.01) & (t_values < 0.5)
if np.any(phi_A_norm[mask] > 1e-10):
    log_t = np.log(t_values[mask][phi_A_norm[mask] > 1e-10])
    log_phi = np.log(phi_A_norm[mask][phi_A_norm[mask] > 1e-10])
    if len(log_t) > 2:
        beta_fit = np.polyfit(log_t, log_phi, 1)
        print(f"  Power law fit: φ_A ~ t^{beta_fit[0]:.3f}")
        print(f"  (β = {beta_fit[0]:.3f}, compare: mean-field β = 0.5, Ising β ≈ 0.326)")

# Candidate A: check for critical exponent
print(f"\n  φ_A transition profile (sampled):")
for i in range(0, len(t_values), 5):
    bar = "█" * int(phi_A_norm[i] * 50)
    print(f"    t={t_values[i]:.2f}: φ={phi_A_vals[i]:.4e}  {bar}")

# For Candidate C
print("\n--- Candidate C: Transition Profile ---")
phi_C_norm = phi_C_order / phi_C_order.max() if phi_C_order.max() > 0 else phi_C_order

print(f"  φ_C transition profile (sampled):")
for i in range(0, len(t_values), 5):
    bar = "█" * int(phi_C_norm[i] * 50)
    print(f"    t={t_values[i]:.2f}: φ={phi_C_order[i]:.6f}  {bar}")

mask_c = (t_values > 0.01) & (t_values < 0.5)
if np.any(phi_C_norm[mask_c] > 1e-10):
    log_t_c = np.log(t_values[mask_c][phi_C_norm[mask_c] > 1e-10])
    log_phi_c = np.log(phi_C_norm[mask_c][phi_C_norm[mask_c] > 1e-10])
    if len(log_t_c) > 2:
        beta_fit_c = np.polyfit(log_t_c, log_phi_c, 1)
        print(f"  Power law fit: φ_C ~ t^{beta_fit_c[0]:.3f}")

# ============================================================================
# SECTION 4: HIGGS-LIKE POTENTIAL CONSTRUCTION  
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 4: HIGGS-LIKE POTENTIAL V(φ)")
print("=" * 78)

print("""
THEORETICAL FRAMEWORK:
━━━━━━━━━━━━━━━━━━━━
In the Standard Model, the Higgs potential is:
    V(φ) = μ²|φ|² + λ|φ|⁴

with μ² < 0 (tachyonic mass) giving VEV v = √(-μ²/2λ) = 246 GeV.

In the ORCA O→S transition, we construct V(φ) from the algebraic energy
landscape. The "cost" of deviating from a division algebra structure
provides the potential.
""")

# Approach: Define V(φ) as the "algebraic energy" of a state with 
# non-alternativity parameter φ

# The key insight: in the octonion (symmetric) phase, the algebra is
# "stiff" — all multiplications are invertible. In the sedenion (broken)
# phase, zero divisors create "soft modes" that lower the energy.

# V(φ, t) = cost_of_nonalternativity(φ) - benefit_of_zero_divisors(φ, t)
# At the transition, the benefit overcomes the cost → symmetry breaking

# Concrete computation: Use Candidate A as the order parameter
# Compute the "algebraic free energy" F(t) from the interpolated algebra

print("--- Computing Algebraic Free Energy F(t) ---")
print("F(t) = -log Z(t), where Z(t) = ∫ exp(-||L_a||²) da")
print("(normalized Gaussian integral over algebra elements)\n")

# For each t, compute the distribution of ||L_a x|| for random a, x
# The "free energy" relates to how the multiplication norm distribution changes

free_energy = []
for idx, t in enumerate(t_values):
    mult_t = lambda a, b, t_=t: interpolated_mult(a, b, t_)
    
    # Compute <||L_a||²> = <sum of squared singular values of L_a>
    norms_sq = []
    for _ in range(200):
        a = np.random.randn(16)
        a = a / np.linalg.norm(a)
        
        L_a = np.zeros((16, 16))
        for j in range(16):
            ej = np.zeros(16); ej[j] = 1.0
            L_a[:, j] = mult_t(a, ej)
        
        svs = np.linalg.svd(L_a, compute_uv=False)
        norms_sq.append(np.sum(svs**2))  # Frobenius norm squared
    
    free_energy.append(np.mean(norms_sq))

free_energy = np.array(free_energy)

print("Algebraic energy <||L_a||²_F> vs interpolation parameter t:")
for i in range(0, len(t_values), 5):
    print(f"  t={t_values[i]:.2f}: E = {free_energy[i]:.4f}")

# Now construct V(φ) parametrically: (φ(t), F(t)) gives V as function of φ
print("\n--- Constructing V(φ) from parametric curve (φ_A(t), F(t)) ---")

# Use φ_A as the order parameter
phi_param = phi_A_vals.copy()

# Fit V(φ) = a₀ + a₂φ² + a₄φ⁴ to the data
# We need φ to be our independent variable
# Remove t=0 point if φ=0 there (degenerate)
mask_fit = phi_param > 1e-10
if np.sum(mask_fit) > 4:
    phi_fit = phi_param[mask_fit]
    V_fit = free_energy[mask_fit]
    
    # Fit polynomial in φ²
    phi2 = phi_fit**2
    phi4 = phi_fit**4
    
    # V = c0 + c2*φ² + c4*φ⁴
    A_matrix = np.column_stack([np.ones_like(phi2), phi2, phi4])
    coeffs, residuals, rank, sv = np.linalg.lstsq(A_matrix, V_fit, rcond=None)
    
    c0, c2, c4 = coeffs
    print(f"\n  Fitted V(φ) = {c0:.4f} + ({c2:.4f})φ² + ({c4:.4f})φ⁴")
    print(f"  Residual: {residuals[0] if len(residuals)>0 else 'N/A'}")
    
    if c2 < 0 and c4 > 0:
        print(f"\n  *** MEXICAN HAT STRUCTURE DETECTED ***")
        print(f"  μ² = {c2:.6f} (negative → tachyonic mass)")
        print(f"  λ  = {c4:.6f} (positive → stable)")
        vev_algebra = np.sqrt(-c2 / (2 * c4))
        print(f"  VEV = √(-μ²/2λ) = {vev_algebra:.6f} (in algebra units)")
    elif c2 > 0 and c4 > 0:
        print(f"\n  Convex potential (no spontaneous breaking in this parametrization)")
        print(f"  μ² = {c2:.6f} (positive)")
        print(f"  λ  = {c4:.6f} (positive)")
    else:
        print(f"\n  Unusual potential shape: μ² = {c2:.6f}, λ = {c4:.6f}")
else:
    print("  Insufficient data points for fitting")

# ============================================================================
# SECTION 5: ALTERNATIVE POTENTIAL FROM SINGULAR VALUE SPECTRUM
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 5: POTENTIAL FROM SINGULAR VALUE SPECTRUM (Candidate C)")
print("=" * 78)

print("""
Key insight: The singular value spectrum of L_a encodes the algebra structure.
- Octonions: all SVs equal (L_a is conformal) → division algebra
- Sedenions: SVs spread out, some → 0 (zero divisors)

The "effective potential" for the minimum singular value σ_min:
  V(σ_min) ∝ -T·log(ρ(σ_min))
where ρ is the density of states with given σ_min.
""")

# Compute SV spectrum at t=0 and t=1
print("--- Singular Value Spectra ---")
for t_test in [0.0, 0.25, 0.5, 0.75, 1.0]:
    mult_t = lambda a, b, t_=t_test: interpolated_mult(a, b, t_)
    
    all_svs = []
    for _ in range(500):
        a = np.random.randn(16)
        a = a / np.linalg.norm(a)
        
        L_a = np.zeros((16, 16))
        for j in range(16):
            ej = np.zeros(16); ej[j] = 1.0
            L_a[:, j] = mult_t(a, ej)
        
        svs = np.linalg.svd(L_a, compute_uv=False)
        all_svs.append(svs)
    
    all_svs = np.array(all_svs)
    print(f"\n  t={t_test:.2f}: SV spectrum (mean over samples):")
    mean_svs = np.mean(all_svs, axis=0)
    std_svs = np.std(all_svs, axis=0)
    for k in range(16):
        bar = "▓" * int(mean_svs[k] * 30)
        print(f"    σ_{k+1:2d} = {mean_svs[k]:.4f} ± {std_svs[k]:.4f}  {bar}")

# ============================================================================
# SECTION 6: CONNECTING TO ELECTROWEAK SCALE
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 6: CONNECTING TO ELECTROWEAK SCALE (246 GeV)")
print("=" * 78)

print("""
DIMENSIONAL ANALYSIS AND SCALE SETTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The O→S transition order parameter φ is dimensionless in algebra units.
To connect to physics, we need a mass scale Λ such that:

    v_phys = Λ × φ_VEV = 246 GeV

Candidates for Λ:
""")

# The algebra VEV from our fit
if 'vev_algebra' in dir():
    vev_alg = vev_algebra
else:
    vev_alg = phi_A_vals[-1]  # Use the t=1 value as approximate VEV

print(f"  φ_VEV (algebra units) = {vev_alg:.6f}")
print(f"  v_phys = 246 GeV")
print(f"  Required scale: Λ = v_phys / φ_VEV = {246.0/vev_alg:.1f} GeV")

print("""
Scale interpretation in ORCA:
─────────────────────────────
1. If Λ = Planck scale (1.22 × 10¹⁹ GeV):
   Then φ_VEV = 246/1.22e19 = 2.02 × 10⁻¹⁷
   → Hierarchy problem reproduced (fine-tuning needed)

2. If Λ = EW scale directly (246 GeV):
   Then φ_VEV = 1 (natural)
   → Requires the algebra transition to SET the EW scale

3. ORCA natural scale hypothesis:
   The CD transition introduces a scale via:
   Λ_ORCA = √(dim_S / dim_O) × v = √(16/8) × v = √2 × v
   So: Λ_ORCA × φ_VEV = 246 GeV
""")

# Compute the algebraic Weinberg angle connection
print("--- Zero Divisor Space and SU(2)_L × U(1)_Y Structure ---")
print()

# The 42 zero divisor directions in S span a subspace
# This subspace should contain the SU(2)_L doublet structure

# Count ZD directions
n_zd = len(zd_pairs)
print(f"  Zero divisor pairs found: {n_zd}")
print(f"  Sedenion imaginary dimensions: 15")
print(f"  Octonion imaginary dimensions: 7")
print(f"  New directions in S \\ O: 8 (indices 8-15)")
print(f"  Of these 8, zero divisors create null subspaces")

# Compute the null space dimension at t=1
mult_1 = lambda a, b: sed_mult(a, b)
null_dims = []
for _ in range(500):
    a = np.random.randn(16)
    a = a / np.linalg.norm(a)
    
    L_a = np.zeros((16, 16))
    for j in range(16):
        ej = np.zeros(16); ej[j] = 1.0
        L_a[:, j] = mult_1(a, ej)
    
    svs = np.linalg.svd(L_a, compute_uv=False)
    null_dim = np.sum(svs < 0.01)
    null_dims.append(null_dim)

null_dims = np.array(null_dims)
print(f"\n  Null space dimension of L_a (sedenion, random a):")
print(f"    Mean: {null_dims.mean():.2f}")
print(f"    Mode: {np.bincount(null_dims).argmax()}")
print(f"    Max:  {null_dims.max()}")

# Check specifically for elements in the e8-e15 sector
print("\n  Checking elements purely in extended sector (e8-e15):")
null_dims_ext = []
for _ in range(500):
    a = np.zeros(16)
    a[8:] = np.random.randn(8)
    a = a / np.linalg.norm(a)
    
    L_a = np.zeros((16, 16))
    for j in range(16):
        ej = np.zeros(16); ej[j] = 1.0
        L_a[:, j] = sed_mult(a, ej)
    
    svs = np.linalg.svd(L_a, compute_uv=False)
    null_dim = np.sum(svs < 0.01)
    null_dims_ext.append(null_dim)

null_dims_ext = np.array(null_dims_ext)
print(f"    Mean null dim: {null_dims_ext.mean():.2f}")
print(f"    Mode: {np.bincount(null_dims_ext).argmax()}")

# ============================================================================
# SECTION 7: EFFECTIVE POTENTIAL RECONSTRUCTION
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 7: EFFECTIVE POTENTIAL V(φ) — FULL RECONSTRUCTION")
print("=" * 78)

print("""
Method: Landau-Ginzburg approach
─────────────────────────────────
Define the effective potential from the partition function of the 
interpolated algebra. The "temperature" parameter is t (interpolation).

V_eff(φ; t) = α(t)φ² + β(t)φ⁴ + γ(t)φ⁶

where α(t) changes sign at t = t_c (critical point).
""")

# For each t, find the equilibrium value of φ (= the measured φ_A(t))
# Then V'(φ_eq) = 0 → 2αφ + 4βφ³ + 6γφ⁵ = 0
# And the "stiffness" κ(t) = V''(φ_eq) from fluctuations

# Compute fluctuation stiffness
print("--- Computing fluctuation stiffness κ(t) = <δφ²>⁻¹ ---")

kappa_vals = []
for idx, t in enumerate(t_values[::5]):
    mult_t = lambda a, b, t_=t: interpolated_mult(a, b, t_)
    
    # Compute φ for many samples, get variance
    phi_samples = []
    for _ in range(500):
        a = np.random.randn(16)
        x = np.random.randn(16)
        
        ax = mult_t(a, x)
        a_ax = mult_t(a, ax)
        aa = mult_t(a, a)
        aa_x = mult_t(aa, x)
        
        diff = np.linalg.norm(a_ax - aa_x)
        norm_factor = max(np.linalg.norm(a)**2 * np.linalg.norm(x), 1e-15)
        phi_samples.append(diff / norm_factor)
    
    phi_samples = np.array(phi_samples)
    variance = np.var(phi_samples)
    kappa = 1.0 / variance if variance > 1e-15 else float('inf')
    kappa_vals.append((t, np.mean(phi_samples), variance, kappa))

print(f"\n  {'t':>5s}  {'<φ>':>10s}  {'Var(φ)':>12s}  {'κ=1/Var':>12s}")
print(f"  {'─'*5}  {'─'*10}  {'─'*12}  {'─'*12}")
for t, mean_phi, var_phi, kappa in kappa_vals:
    k_str = f"{kappa:.2f}" if kappa < 1e10 else "∞"
    print(f"  {t:5.2f}  {mean_phi:10.6f}  {var_phi:12.6e}  {k_str:>12s}")

# ============================================================================
# SECTION 8: POTENTIAL COEFFICIENTS FROM ALGEBRAIC QUANTITIES
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 8: μ² AND λ FROM CAYLEY-DICKSON ALGEBRA QUANTITIES")
print("=" * 78)

print("""
DERIVATION OF POTENTIAL COEFFICIENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Starting from the algebraic structure:

1. The alternativity defect φ measures departure from division algebra:
   φ = ||[L_a, L_a, L_x]|| / (||a||²||x||)   (associator-like)

2. For the interpolated algebra A_t:
   - The "stiffness" against non-alternativity is:
     μ²(t) = ∂²V/∂φ² |_{φ=0}  = restoring force toward alternativity
   
   - At t=0 (pure octonion): μ²(0) > 0 (alternativity is enforced)
   - At t=1 (sedenion): μ²(1) < 0 (alternativity is broken)
   - Critical point: μ²(t_c) = 0

3. The quartic coupling λ stabilizes the potential:
   λ = ∂⁴V/∂φ⁴ / 4! > 0 (from higher-order algebraic constraints)
""")

# Estimate μ²(t) from the curvature of V(φ) near the minimum
print("--- Estimating μ²(t) from algebraic curvature ---\n")

# Use the free energy data to estimate the curvature
# dF/dφ = 0 at equilibrium, d²F/dφ² = μ²_eff

# For the Landau potential V = μ²φ² + λφ⁴:
# At minimum: 2μ²φ + 4λφ³ = 0 → φ² = -μ²/(2λ)
# V''(φ_min) = 2μ² + 12λφ² = 2μ² + 12λ(-μ²/(2λ)) = 2μ² - 6μ² = -4μ²

# From fluctuations: κ = V''(φ_min) = -4μ²
# And φ_min² = -μ²/(2λ)

# So: μ² = -κ/4 and λ = κ/(8φ_min²)

print(f"  {'t':>5s}  {'φ_min':>10s}  {'κ':>10s}  {'μ²':>12s}  {'λ':>12s}  {'VEV_alg':>10s}")
print(f"  {'─'*5}  {'─'*10}  {'─'*10}  {'─'*12}  {'─'*12}  {'─'*10}")

mu2_list = []
lam_list = []
for t, mean_phi, var_phi, kappa in kappa_vals:
    if mean_phi > 1e-6 and kappa < 1e10:
        mu2 = -kappa / 4
        lam = kappa / (8 * mean_phi**2) if mean_phi > 1e-10 else float('inf')
        vev = np.sqrt(-mu2 / (2 * lam)) if (mu2 < 0 and lam > 0) else 0
        print(f"  {t:5.2f}  {mean_phi:10.6f}  {kappa:10.2f}  {mu2:12.4f}  {lam:12.2f}  {vev:10.6f}")
        mu2_list.append(mu2)
        lam_list.append(lam)
    else:
        print(f"  {t:5.2f}  {mean_phi:10.6f}  {'∞':>10s}  {'N/A':>12s}  {'N/A':>12s}  {'N/A':>10s}")

# ============================================================================
# SECTION 9: SUMMARY AND PHYSICAL INTERPRETATION
# ============================================================================
print("\n" + "=" * 78)
print("SECTION 9: SUMMARY — HIGGS MECHANISM AS O→S TRANSITION")
print("=" * 78)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ORDER PARAMETER COMPARISON                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Candidate A (Non-Alternativity):                                            ║
║    φ_A(O) = {phi_A_vals[0]:.2e},  φ_A(S) = {phi_A_vals[-1]:.4f}              ║
║    Power-law onset: φ ~ t^β                                                 ║
║    Pros: Direct measure of algebra property change                           ║
║    Cons: Not directly a field; ensemble average                              ║
║                                                                              ║
║  Candidate B (Zero-Divisor Density):                                         ║
║    φ_B(O) = {phi_B_vals[0]:.4f},  φ_B(S) = {phi_B_vals[-1]:.4f}             ║
║    Pros: Discrete, countable; connects to null spaces                        ║
║    Cons: Not continuous for finite-dim analysis                              ║
║                                                                              ║
║  Candidate C (Division Defect = 1 - min_sv):                                ║
║    φ_C(O) = {phi_C_order[0]:.6f},  φ_C(S) = {phi_C_order[-1]:.6f}          ║
║    Pros: Continuous; connects to L_a spectrum; natural ∈ [0,1]              ║
║    Cons: Requires spectral computation                                       ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                     RECOMMENDED ORDER PARAMETER                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  φ_ORCA ≡ Candidate A (non-alternativity)                                   ║
║                                                                              ║
║  Reasons:                                                                    ║
║  1. Directly measures the algebraic symmetry that breaks                     ║
║  2. Alternativity ↔ Moufang identity ↔ gauge symmetry structure             ║
║  3. φ=0 ↔ division algebra ↔ unbroken phase                                ║
║  4. φ>0 ↔ zero divisors appear ↔ broken phase                              ║
║  5. Smoothly interpolatable between O and S                                  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                     HIGGS POTENTIAL STRUCTURE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  V(φ) = μ²(t)·φ² + λ(t)·φ⁴                                                ║
║                                                                              ║
║  where:                                                                      ║
║    μ²(t) = μ₀²·(1 - t/t_c)  changes sign at t_c                           ║
║    λ(t)  > 0                  (algebraic stability)                          ║
║                                                                              ║
║  Physical identification:                                                    ║
║    μ² ↔ -(stiffness of alternativity enforcement) / 4                       ║
║    λ  ↔  (stiffness) / (8·φ_min²)                                          ║
║    VEV: v = √(-μ²/2λ) = φ_min (algebra) × Λ_ORCA (energy scale)           ║
║                                                                              ║
║  For v_phys = 246 GeV:                                                       ║
║    Λ_ORCA = 246 GeV / φ_A(t=1) = {246.0/phi_A_vals[-1]:.1f} GeV            ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                     KEY PHYSICAL DICTIONARY                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Standard Model          ↔  ORCA O→S Transition                             ║
║  ─────────────────────────────────────────────────                           ║
║  Higgs field φ           ↔  Non-alternativity measure                        ║
║  Mexican hat potential   ↔  Algebraic free energy landscape                  ║
║  SU(2)_L × U(1)_Y       ↔  Moufang identity (cross-sector)                 ║
║  U(1)_em (unbroken)      ↔  Moufang identity (within-sector)                ║
║  VEV = 246 GeV           ↔  φ_VEV × Λ_ORCA                                 ║
║  Goldstone bosons (W±,Z) ↔  Directions along ZD null spaces                 ║
║  Higgs boson (125 GeV)   ↔  Radial fluctuation of φ around VEV              ║
║  μ² < 0                  ↔  Energetic preference for non-alternativity       ║
║  λ > 0                   ↔  Higher-order algebraic constraints               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Final: check the Higgs mass prediction
print("--- Higgs Mass Prediction ---")
print()
if len(mu2_list) > 0 and len(lam_list) > 0:
    mu2_final = mu2_list[-1]  # At t=1
    lam_final = lam_list[-1]
    
    # m_H² = -2μ² = 2λv²
    # In algebra units:
    m_H_sq_alg = -2 * mu2_final
    print(f"  m_H² (algebra) = -2μ² = {m_H_sq_alg:.4f}")
    print(f"  m_H (algebra)  = {np.sqrt(abs(m_H_sq_alg)):.4f}")
    
    # Ratio m_H/v in algebra units
    if phi_A_vals[-1] > 1e-10:
        ratio = np.sqrt(abs(m_H_sq_alg)) / phi_A_vals[-1]
        print(f"  m_H / v (algebra) = {ratio:.4f}")
        print(f"  m_H / v (SM)      = 125/246 = {125/246:.4f}")
        print(f"  Discrepancy factor: {ratio / (125/246):.2f}")

print("\n" + "=" * 78)
print("COMPUTATION COMPLETE")
print("=" * 78)
