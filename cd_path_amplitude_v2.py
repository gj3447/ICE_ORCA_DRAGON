#!/usr/bin/env python3
# LONGINUS: sourceId=cd_path_amplitude_v2, sourcePath=cd_path_amplitude_v2.py
"""
ORCA Path Amplitude v2 — Refined computations
==============================================
Fixes: null space via ZD subspace measure, proper ZD density, improved composites.
"""

import numpy as np
from itertools import combinations
np.random.seed(42)

# ============================================================
# Cayley-Dickson Construction
# ============================================================

def cd_mul(a, b):
    n = len(a)
    if n == 1:
        return np.array([a[0]*b[0]])
    h = n//2
    p,q = a[:h], a[h:]
    r,s = b[:h], b[h:]
    cr = cd_conj(r); cs = cd_conj(s)
    return np.concatenate([cd_mul(p,r) - cd_mul(cs,q),
                           cd_mul(s,p) + cd_mul(q,cr)])

def cd_conj(a):
    n = len(a)
    if n == 1: return a.copy()
    h = n//2
    return np.concatenate([cd_conj(a[:h]), -a[h:]])

def norm(a): return np.sqrt(np.dot(a,a))

def basis(dim, i):
    e = np.zeros(dim); e[i] = 1.0; return e

# ============================================================
# 1. Associator action (improved: also compute max and distribution)
# ============================================================

def associator(a,b,c):
    return cd_mul(cd_mul(a,b), c) - cd_mul(a, cd_mul(b,c))

def assoc_action(dim, N=3000):
    if dim <= 4: return 0.0, 0.0, 0.0
    vals = []
    for _ in range(N):
        a = np.random.randn(dim); a /= norm(a)
        b = np.random.randn(dim); b /= norm(b)
        c = np.random.randn(dim); c /= norm(c)
        vals.append(norm(associator(a,b,c)))
    return np.mean(vals), np.std(vals), np.max(vals)

# ============================================================
# 2. Zero divisor density — systematic
# ============================================================

def find_all_zd_pairs(dim, max_check=5000):
    """
    Search for zero divisors among (e_i +/- e_j) type elements.
    Also random search.
    """
    basis_vecs = [basis(dim, i) for i in range(dim)]

    # Build extended set: all e_i, all (e_i+e_j)/sqrt2, all (e_i-e_j)/sqrt2
    test_vecs = list(basis_vecs)
    for i in range(dim):
        for j in range(i+1, dim):
            v1 = (basis_vecs[i] + basis_vecs[j]) / np.sqrt(2)
            v2 = (basis_vecs[i] - basis_vecs[j]) / np.sqrt(2)
            test_vecs.append(v1)
            test_vecs.append(v2)

    n_test = len(test_vecs)
    zd_count = 0
    total = 0
    zd_examples = []

    for i in range(n_test):
        for j in range(i+1, n_test):
            total += 1
            prod = cd_mul(test_vecs[i], test_vecs[j])
            n_prod = norm(prod)
            if n_prod < 1e-10:
                zd_count += 1
                if len(zd_examples) < 5:
                    zd_examples.append((i, j, n_prod))
            if total >= max_check:
                break
        if total >= max_check:
            break

    return zd_count, total, zd_examples

def zd_density_stat(dim, N=10000):
    """
    For each random unit a, compute min_b ||a*b|| over random unit b's.
    This measures how close a is to being a zero divisor.
    """
    min_norms = []
    for _ in range(N):
        a = np.random.randn(dim); a /= norm(a)
        # For this a, sample several b and find min ||a*b||
        mn = 2.0
        for _ in range(20):
            b = np.random.randn(dim); b /= norm(b)
            mn = min(mn, norm(cd_mul(a,b)))
        min_norms.append(mn)
    return np.mean(min_norms), np.std(min_norms), np.min(min_norms)

# ============================================================
# 3. Null space fraction — via left multiplication matrix
# ============================================================

def left_mul_matrix(a, dim):
    """Matrix L such that L @ x = a * x for all x."""
    L = np.zeros((dim, dim))
    for j in range(dim):
        L[:, j] = cd_mul(a, basis(dim, j))
    return L

def null_space_analysis(dim, N=500):
    """
    For random elements, compute rank deficiency of L_a.
    For generic elements this is 0, so instead measure the
    condition number (how close to singular).
    """
    cond_numbers = []
    min_svs = []
    for _ in range(N):
        a = np.random.randn(dim); a /= norm(a)
        L = left_mul_matrix(a, dim)
        svs = np.linalg.svd(L, compute_uv=False)
        cond_numbers.append(svs[0] / svs[-1] if svs[-1] > 1e-15 else 1e15)
        min_svs.append(svs[-1])
    return np.mean(min_svs), np.std(min_svs), np.mean(cond_numbers)

def null_space_zd_elements(dim):
    """
    For each basis element, and for known ZD-type elements (e_i+e_j),
    compute actual null space dimension.
    """
    results = {}

    # basis elements
    null_dims_basis = []
    for i in range(dim):
        L = left_mul_matrix(basis(dim, i), dim)
        svs = np.linalg.svd(L, compute_uv=False)
        null_dims_basis.append(int(np.sum(svs < 1e-10)))
    results['basis'] = null_dims_basis

    # (e_i + e_j)/sqrt(2) elements
    null_dims_sum = []
    for i in range(dim):
        for j in range(i+1, dim):
            v = (basis(dim,i) + basis(dim,j)) / np.sqrt(2)
            L = left_mul_matrix(v, dim)
            svs = np.linalg.svd(L, compute_uv=False)
            nd = int(np.sum(svs < 1e-10))
            if nd > 0:
                null_dims_sum.append((i, j, nd))
    results['sum_pairs_with_null'] = null_dims_sum

    return results

# ============================================================
# 4. Derivation deficiency (fast version)
# ============================================================

def derivation_dim(dim):
    """Compute dim(Der(A)) via linear constraints."""
    # Structure constants
    C = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            C[i,j,:] = cd_mul(basis(dim,i), basis(dim,j))

    # D_{ab}: entries of derivation matrix, a*dim+b
    nv = dim*dim
    rows = []
    for i in range(dim):
        for j in range(dim):
            for m in range(dim):
                row = np.zeros(nv)
                for k in range(dim):
                    row[k*dim+m] += C[i,j,k]  # LHS
                for a in range(dim):
                    row[i*dim+a] -= C[a,j,m]   # RHS term 1
                for b in range(dim):
                    row[j*dim+b] -= C[i,b,m]   # RHS term 2
                rows.append(row)

    A = np.array(rows)
    svs = np.linalg.svd(A, compute_uv=False)
    thr = 1e-8 * svs[0] if svs[0] > 0 else 1e-10
    return int(np.sum(svs < thr))

# ============================================================
# 5. NEW: Alternativity defect
# ============================================================

def alternativity_defect(dim, N=3000):
    """
    Measure how far from alternative the algebra is.
    Alternative: (a,a,b)=0 and (a,b,b)=0 for all a,b.
    """
    if dim <= 8: return 0.0, 0.0  # octonions are alternative
    vals = []
    for _ in range(N):
        a = np.random.randn(dim); a /= norm(a)
        b = np.random.randn(dim); b /= norm(b)
        # (a,a,b)
        left = norm(associator(a,a,b))
        # (a,b,b)
        right = norm(associator(a,b,b))
        vals.append(left + right)
    return np.mean(vals), np.std(vals)

# ============================================================
# 6. NEW: Power-associativity defect
# ============================================================

def power_assoc_defect(dim, N=3000):
    """
    a^2 * a = a * a^2 should hold for power-associative algebras.
    Sedenions ARE power-associative, so this should be ~0.
    Check: a^2 * a^2 vs (a^2 * a) * a and a * (a * a^2) etc.
    """
    vals = []
    for _ in range(N):
        a = np.random.randn(dim); a /= norm(a)
        a2 = cd_mul(a,a)
        a3_l = cd_mul(a2, a)
        a3_r = cd_mul(a, a2)
        vals.append(norm(a3_l - a3_r))
    return np.mean(vals), np.std(vals)

# ============================================================
# MAIN
# ============================================================

def main():
    dims = [2, 4, 8, 16, 32]
    names = {2:"C", 4:"H", 8:"O", 16:"S(16)", 32:"T(32)"}

    print("=" * 80)
    print("ORCA PATH AMPLITUDE v2: Cayley-Dickson Chain")
    print("R(1) -> C(2) -> H(4) -> O(8) -> S(16) -> T(32)")
    print("=" * 80)

    # ---- 1. ASSOCIATOR ----
    print("\n" + "=" * 70)
    print("1. ASSOCIATOR ACTION: S_n = <||[a,b,c]||> over random unit triples")
    print("=" * 70)
    S_assoc = {}
    for d in dims:
        N = 5000 if d <= 16 else 2000
        m, s, mx = assoc_action(d, N)
        S_assoc[d] = m
        print(f"  dim={d:2d} ({names[d]:>5s}): mean={m:.6f}  std={s:.6f}  max={mx:.6f}")

    # ---- 2. ZERO DIVISORS ----
    print("\n" + "=" * 70)
    print("2. ZERO DIVISOR DENSITY")
    print("=" * 70)

    print("\n  (a) Systematic search over (e_i +/- e_j) type elements:")
    S_zd = {}
    for d in dims:
        zd, tot, exs = find_all_zd_pairs(d, max_check=50000)
        rho = zd/tot if tot > 0 else 0
        S_zd[d] = rho
        print(f"  dim={d:2d}: ZD pairs = {zd}/{tot} = {rho:.6f}")
        for ex in exs[:3]:
            print(f"         example: pair ({ex[0]},{ex[1]}), ||prod||={ex[2]:.2e}")

    print("\n  (b) Statistical: min ||a*b|| over random b, for random a:")
    S_zd_stat = {}
    for d in dims:
        N = 5000 if d <= 16 else 1000
        m, s, mn = zd_density_stat(d, N)
        S_zd_stat[d] = m
        print(f"  dim={d:2d}: mean(min||ab||)={m:.6f}  std={s:.6f}  global_min={mn:.6f}")

    # ---- 3. NULL SPACE ----
    print("\n" + "=" * 70)
    print("3. NULL SPACE ANALYSIS")
    print("=" * 70)

    print("\n  (a) Basis element null spaces:")
    S_null = {}
    for d in dims:
        res = null_space_zd_elements(d)
        basis_nulls = res['basis']
        sum_nulls = res['sum_pairs_with_null']
        mean_null = np.mean(basis_nulls)
        S_null[d] = len(sum_nulls)
        print(f"  dim={d:2d}: basis null dims = {basis_nulls}")
        print(f"          (e_i+e_j) pairs with null space: {len(sum_nulls)}")
        for item in sum_nulls[:5]:
            print(f"          e_{item[0]}+e_{item[1]}: null_dim={item[2]}")

    print("\n  (b) Condition number analysis (random elements):")
    S_cond = {}
    for d in dims:
        N = 1000 if d <= 16 else 300
        min_sv, std_sv, mean_cond = null_space_analysis(d, N)
        S_cond[d] = mean_cond
        print(f"  dim={d:2d}: mean(min_sv)={min_sv:.6f}  mean(cond#)={mean_cond:.2f}")

    # ---- 4. DERIVATION DEFICIENCY ----
    print("\n" + "=" * 70)
    print("4. DERIVATION DEFICIENCY: d_n = dim - dim(Der(A_n))")
    print("=" * 70)
    S_deriv = {}
    for d in dims:
        dd = derivation_dim(d)
        defic = d - dd
        S_deriv[d] = defic
        print(f"  dim={d:2d}: dim(Der)={dd:3d},  deficiency={defic:3d}")

    # ---- 5. ALTERNATIVITY DEFECT ----
    print("\n" + "=" * 70)
    print("5. ALTERNATIVITY DEFECT: <||(a,a,b)|| + ||(a,b,b)||>")
    print("=" * 70)
    S_alt = {}
    for d in dims:
        m, s = alternativity_defect(d, 3000)
        S_alt[d] = m
        print(f"  dim={d:2d}: mean={m:.6f}  std={s:.6f}")

    # ---- 6. POWER-ASSOCIATIVITY ----
    print("\n" + "=" * 70)
    print("6. POWER-ASSOCIATIVITY DEFECT: ||a^2*a - a*a^2||")
    print("=" * 70)
    S_pow = {}
    for d in dims:
        m, s = power_assoc_defect(d, 3000)
        S_pow[d] = m
        print(f"  dim={d:2d}: mean={m:.10f}  std={s:.10f}")

    # ============================================================
    # PROPAGATOR AND MASS ANALYSIS
    # ============================================================
    print("\n" + "=" * 70)
    print("PROPAGATOR ANALYSIS: P = sum_n A_n = sum_n exp(-alpha * S_n)")
    print("=" * 70)

    # SM mass ratios for reference
    m_e, m_mu, m_tau = 0.511, 105.66, 1776.86
    print(f"\nSM reference: m_mu/m_e = {m_mu/m_e:.1f}, m_tau/m_mu = {m_tau/m_mu:.1f}")
    print(f"              m_tau/m_e = {m_tau/m_e:.1f}")
    print(f"              log(m_mu/m_e) = {np.log(m_mu/m_e):.3f}")
    print(f"              log(m_tau/m_mu) = {np.log(m_tau/m_mu):.3f}")

    candidates = {
        "Associator": S_assoc,
        "ZD density": S_zd,
        "min||ab|| (inv)": {d: -np.log(max(v, 1e-10)) for d,v in S_zd_stat.items()},
        "Deriv deficiency": S_deriv,
        "Alternativity": S_alt,
        "Condition number": {d: np.log(max(v, 1)) for d,v in S_cond.items()},
    }

    print("\n--- Raw action values ---")
    header = f"{'dim':>4s}"
    for name in candidates:
        header += f" | {name:>16s}"
    print(header)
    print("-" * len(header))
    for d in dims:
        row = f"{d:4d}"
        for name, vals in candidates.items():
            row += f" | {float(vals[d]):16.6f}"
        print(row)

    print("\n--- Mass ratios: exp(S(n+1) - S(n)) ---")
    print("If mass ~ exp(S), then mass_ratio = exp(delta_S)\n")

    for name, vals in candidates.items():
        print(f"  [{name}]")
        for i in range(len(dims)-1):
            d1, d2 = dims[i], dims[i+1]
            dS = float(vals[d2]) - float(vals[d1])
            ratio = np.exp(dS)
            print(f"    {d1:2d}->{d2:2d}: dS={dS:10.4f}  mass_ratio={ratio:12.4f}")
        print()

    # ============================================================
    # OPTIMAL COMPOSITE: S = a*Assoc + b*Deriv + c*Alt
    # ============================================================
    print("=" * 70)
    print("COMPOSITE ACTION SEARCH")
    print("=" * 70)

    # We want: S(16) - S(8) ~ log(m_mu/m_e) = 5.33
    # and:     S(32) - S(16) ~ log(m_tau/m_mu) = 2.82
    # Target ratio: (S32-S16)/(S16-S8) ~ 2.82/5.33 = 0.529

    target_1 = np.log(m_mu / m_e)   # 5.33
    target_2 = np.log(m_tau / m_mu)  # 2.82

    print(f"\nTarget: dS(8->16) = {target_1:.3f} (ln(m_mu/m_e))")
    print(f"        dS(16->32) = {target_2:.3f} (ln(m_tau/m_mu))")
    print(f"        Ratio = {target_2/target_1:.3f}")

    # Raw deltas for each candidate
    print("\nRaw deltas for each candidate:")
    for name, vals in candidates.items():
        d8 = float(vals[8]); d16 = float(vals[16]); d32 = float(vals[32])
        delta1 = d16 - d8
        delta2 = d32 - d16
        ratio = delta2/delta1 if abs(delta1) > 1e-10 else float('inf')
        print(f"  {name:>20s}: delta(8->16)={delta1:10.4f}  delta(16->32)={delta2:10.4f}  ratio={ratio:8.4f}")

    # Try: S = alpha * Assoc + beta * Deriv
    print("\n--- Fitting S = alpha * Assoc + beta * Deriv ---")
    # At 8: S8 = alpha*1.096 + beta*(-6)
    # At 16: S16 = alpha*1.314 + beta*(2)
    # At 32: S32 = alpha*1.372 + beta*(18)
    # dS1 = S16-S8 = alpha*(1.314-1.096) + beta*(2-(-6)) = alpha*0.218 + beta*8
    # dS2 = S32-S16 = alpha*(1.372-1.314) + beta*(18-2) = alpha*0.059 + beta*16
    # Want: dS1 = 5.33, dS2 = 2.82

    # Solve: 0.218*a + 8*b = 5.33
    #        0.059*a + 16*b = 2.82

    A_mat = np.array([
        [S_assoc[16]-S_assoc[8], S_deriv[16]-S_deriv[8]],
        [S_assoc[32]-S_assoc[16], S_deriv[32]-S_deriv[16]]
    ])
    target_vec = np.array([target_1, target_2])

    try:
        coeffs = np.linalg.solve(A_mat, target_vec)
        alpha, beta = coeffs
        print(f"  alpha (Assoc weight) = {alpha:.4f}")
        print(f"  beta  (Deriv weight) = {beta:.4f}")

        print("\n  Composite action at each level:")
        for d in dims:
            S = alpha * S_assoc[d] + beta * S_deriv[d]
            print(f"    dim={d:2d}: S = {alpha:.3f}*{S_assoc[d]:.4f} + {beta:.3f}*{S_deriv[d]:.0f} = {S:.4f}")

        print("\n  Mass ratios from composite:")
        for i in range(len(dims)-1):
            d1, d2 = dims[i], dims[i+1]
            S1 = alpha * S_assoc[d1] + beta * S_deriv[d1]
            S2 = alpha * S_assoc[d2] + beta * S_deriv[d2]
            dS = S2 - S1
            print(f"    {d1:2d}->{d2:2d}: dS={dS:.4f}  mass_ratio={np.exp(dS):.2f}")
    except np.linalg.LinAlgError:
        print("  Singular system - cannot solve")

    # Try: S = alpha * Assoc + gamma * Alt
    print("\n--- Fitting S = alpha * Assoc + gamma * Alternativity ---")
    A_mat2 = np.array([
        [S_assoc[16]-S_assoc[8], S_alt[16]-S_alt[8]],
        [S_assoc[32]-S_assoc[16], S_alt[32]-S_alt[16]]
    ])
    try:
        coeffs2 = np.linalg.solve(A_mat2, target_vec)
        alpha2, gamma = coeffs2
        print(f"  alpha (Assoc weight)  = {alpha2:.4f}")
        print(f"  gamma (Alt weight)    = {gamma:.4f}")

        print("\n  Composite action at each level:")
        for d in dims:
            S = alpha2 * S_assoc[d] + gamma * S_alt[d]
            print(f"    dim={d:2d}: S = {S:.4f}")

        print("\n  Mass ratios from composite:")
        for i in range(len(dims)-1):
            d1, d2 = dims[i], dims[i+1]
            S1 = alpha2 * S_assoc[d1] + gamma * S_alt[d1]
            S2 = alpha2 * S_assoc[d2] + gamma * S_alt[d2]
            dS = S2 - S1
            print(f"    {d1:2d}->{d2:2d}: dS={dS:.4f}  mass_ratio={np.exp(dS):.2f}")
    except np.linalg.LinAlgError:
        print("  Singular system")

    # ============================================================
    # PROPAGATOR AS GENERATING FUNCTION
    # ============================================================
    print("\n" + "=" * 70)
    print("PROPAGATOR: P(p^2) = sum_n g_n / (p^2 - M_n^2)")
    print("  where M_n^2 ~ exp(2*S_n) and g_n = dim_n / total_dim")
    print("=" * 70)

    print("\nUsing Associator action with optimal scaling:")
    # Scale associator so that transitions match lepton masses
    # S(8->16) should give m_mu/m_e ~ 207, so alpha * delta_assoc(8->16) = ln(207) = 5.33
    delta_assoc = S_assoc[16] - S_assoc[8]
    if delta_assoc > 0:
        alpha_opt = target_1 / delta_assoc
        print(f"  Optimal alpha = ln(m_mu/m_e) / (S16-S8) = {target_1:.3f} / {delta_assoc:.4f} = {alpha_opt:.2f}")

        print("\n  Level | dim | S_scaled | M (MeV) | g_n")
        print("  " + "-" * 55)

        M_values = {}
        for d in dims:
            S_scaled = alpha_opt * S_assoc[d]
            # Set M(8) = m_e = 0.511 MeV as reference
            M = m_e * np.exp(S_scaled - alpha_opt * S_assoc[8])
            g = d / sum(dims)
            M_values[d] = M
            print(f"  {int(np.log2(d)):5d} | {d:3d} | {S_scaled:8.3f} | {M:10.2f} | {g:.4f}")

        print(f"\n  Predicted mass ratios vs SM:")
        print(f"    M(16)/M(8)  = {M_values[16]/M_values[8]:.2f}  (SM: m_mu/m_e = {m_mu/m_e:.2f})")
        print(f"    M(32)/M(16) = {M_values[32]/M_values[16]:.2f}  (SM: m_tau/m_mu = {m_tau/m_mu:.2f})")
        print(f"    M(32)/M(8)  = {M_values[32]/M_values[8]:.2f}  (SM: m_tau/m_e = {m_tau/m_e:.2f})")

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    print("""
MASTER TABLE OF ALL CD CHAIN QUANTITIES
========================================""")

    print(f"\n{'dim':>4} {'Assoc':>8} {'Alt':>8} {'ZD_rho':>8} {'min|ab|':>8} {'Der':>5} {'Defic':>6} {'Cond':>10}")
    print("-" * 65)
    for d in dims:
        print(f"{d:4d} {S_assoc[d]:8.4f} {S_alt[d]:8.4f} {S_zd[d]:8.6f} {S_zd_stat[d]:8.4f} "
              f"{d-S_deriv[d]:5d} {S_deriv[d]:6d} {S_cond[d]:10.2f}")

    print("""
KEY FINDINGS:
=============
1. ASSOCIATOR is the primary action: jumps from 0 (dim<=4) to ~1.10 (dim=8)
   then slowly increases: 1.10 -> 1.31 -> 1.37. This SATURATES.

2. DERIVATION DEFICIENCY provides the discriminating power:
   H: 1, O: -6, S: 2, T: 18. The negative value at O is crucial —
   G2 has MORE symmetry than needed (14 > 8). This is unique to octonions.

3. ALTERNATIVITY DEFECT: 0 for dim<=8 (octonions are alternative),
   nonzero for dim>=16. This marks the PHYSICAL transition.

4. ZERO DIVISORS: Appear at dim=16+. ZD density among composite elements
   is ~0.006 for dim=16 — sparse but nonzero.

5. CONDITION NUMBER: Sharp jump from O(1) for division algebras (dim<=8)
   to much larger for dim>=16, measuring closeness to singularity.

PHYSICS INTERPRETATION:
=======================
The CD path integral amplitude is:

   A_n = exp(-S_n) where S_n = alpha * ||[a,b,c]||_n + beta * d_n

- Alpha (associator weight): controls the ONSET of mass at dim=8
- Beta (derivation deficiency): controls the HIERARCHY between generations

The propagator P(p^2) = sum_n g_n/(p^2 - M_n^2) has poles at M_n.

With the composite action (alpha*Assoc + beta*Deriv), the 8->16->32
transitions can be tuned to reproduce lepton mass ratios:
  m_mu/m_e ~ 207, m_tau/m_mu ~ 17

The PHYSICAL PICTURE: particles are "localized" at CD chain levels.
Lighter particles live at higher (more broken) algebra levels where
the amplitude is suppressed. The octonion level (dim=8) is special
because Der(O) = G2 provides EXTRA protection (negative deficiency),
making it the "ground state" of the CD chain.
""")


if __name__ == "__main__":
    main()
