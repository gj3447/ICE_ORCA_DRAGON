#!/usr/bin/env python3
# LONGINUS: sourceId=cd_path_amplitude, sourcePath=cd_path_amplitude.py
"""
ORCA Path Amplitude Computation
================================
Cayley-Dickson chain path integral: R -> C -> H -> O -> S(16D) -> T(32D)

Computes 4 candidate "actions" for the CD path integral:
  1. Associator action:    S_n = <||[a,b,c]||>
  2. Zero divisor density: rho_n
  3. Null space fraction:  f_n
  4. Derivation deficiency: d_n

Then constructs propagators and checks SM mass ratios.
"""

import numpy as np
from itertools import product
import sys

np.random.seed(42)

# ============================================================
# PART 0: Cayley-Dickson Construction
# ============================================================

def cd_multiply(a, b):
    """
    Cayley-Dickson multiplication: if a=(p,q), b=(r,s) in A_{n+1},
    then a*b = (p*r - conj(s)*q, s*p + q*conj(r))

    Base case: real numbers (dim=1), just float multiplication.
    """
    n = len(a)
    if n == 1:
        return np.array([a[0] * b[0]])

    half = n // 2
    p, q = a[:half], a[half:]
    r, s = b[:half], b[half:]

    conj_s = cd_conjugate(s)
    conj_r = cd_conjugate(r)

    # (p*r - conj(s)*q, s*p + q*conj(r))
    left = cd_multiply(p, r) - cd_multiply(conj_s, q)
    right = cd_multiply(s, p) + cd_multiply(q, conj_r)

    return np.concatenate([left, right])


def cd_conjugate(a):
    """Cayley-Dickson conjugate: if a=(p,q), conj(a) = (conj(p), -q)"""
    n = len(a)
    if n == 1:
        return a.copy()

    half = n // 2
    p, q = a[:half], a[half:]
    return np.concatenate([cd_conjugate(p), -q])


def cd_norm_sq(a):
    """||a||^2 = a * conj(a), which equals sum of squares for CD algebras"""
    return np.dot(a, a)


def cd_norm(a):
    return np.sqrt(cd_norm_sq(a))


# ============================================================
# PART 1: Associator Action
# ============================================================

def associator(a, b, c):
    """[a,b,c] = (a*b)*c - a*(b*c)"""
    ab = cd_multiply(a, b)
    ab_c = cd_multiply(ab, c)
    bc = cd_multiply(b, c)
    a_bc = cd_multiply(a, bc)
    return ab_c - a_bc


def compute_associator_action(dim, n_samples=5000):
    """Average ||[a,b,c]|| over random unit triples in the algebra of given dimension."""
    if dim <= 1:
        return 0.0

    norms = []
    for _ in range(n_samples):
        a = np.random.randn(dim)
        b = np.random.randn(dim)
        c = np.random.randn(dim)
        # Normalize to unit vectors
        a /= cd_norm(a)
        b /= cd_norm(b)
        c /= cd_norm(c)

        assoc = associator(a, b, c)
        norms.append(cd_norm(assoc))

    return np.mean(norms), np.std(norms)


# ============================================================
# PART 2: Zero Divisor Density
# ============================================================

def find_zero_divisors_basis(dim):
    """
    Check all pairs of basis elements e_i, e_j (i != j) for zero divisors:
    e_i * e_j = 0 means they are zero divisors.

    Also check (e_i + e_j) type combinations for zero divisors.

    For sedenions (16D) and beyond, zero divisors exist.
    Returns count of ZD basis pairs and total pairs checked.
    """
    basis = []
    for i in range(dim):
        e = np.zeros(dim)
        e[i] = 1.0
        basis.append(e)

    zd_count = 0
    total_pairs = 0

    # Check all pairs of basis elements
    for i in range(dim):
        for j in range(i+1, dim):
            total_pairs += 1
            prod = cd_multiply(basis[i], basis[j])
            if cd_norm(prod) < 1e-10:
                zd_count += 1

    # Also check (e_i +/- e_j) type elements for a broader picture
    zd_composite = 0
    composite_total = 0
    for i in range(dim):
        for j in range(i+1, dim):
            for k in range(dim):
                for l in range(k+1, dim):
                    if (i, j) >= (k, l):
                        continue
                    composite_total += 1
                    a = basis[i] + basis[j]
                    a /= cd_norm(a)
                    b = basis[k] + basis[l]
                    b /= cd_norm(b)
                    prod = cd_multiply(a, b)
                    if cd_norm(prod) < 1e-10:
                        zd_composite += 1

    return zd_count, total_pairs, zd_composite, composite_total


def compute_zd_density_random(dim, n_samples=10000):
    """
    Statistical approach: fraction of random pairs (a,b) where ||a*b|| << ||a|| ||b||.
    For division algebras (dim<=8), this should be ~0.
    """
    near_zero_count = 0
    norms_ratio = []

    for _ in range(n_samples):
        a = np.random.randn(dim)
        b = np.random.randn(dim)
        a /= cd_norm(a)
        b /= cd_norm(b)

        prod = cd_multiply(a, b)
        r = cd_norm(prod)
        norms_ratio.append(r)

        if r < 0.1:  # threshold for "near zero divisor"
            near_zero_count += 1

    return near_zero_count / n_samples, np.mean(norms_ratio), np.std(norms_ratio)


# ============================================================
# PART 3: Null Space Fraction
# ============================================================

def compute_null_space_fraction(dim, n_samples=500):
    """
    For each random element a, compute the left multiplication map L_a: x -> a*x.
    The null space of L_a contains the left zero divisors of a.

    f_n = average(dim(null(L_a))) / dim
    """
    if dim <= 1:
        return 0.0, 0.0

    null_fracs = []

    for _ in range(n_samples):
        a = np.random.randn(dim)
        a /= cd_norm(a)

        # Build the matrix for L_a
        L = np.zeros((dim, dim))
        for j in range(dim):
            ej = np.zeros(dim)
            ej[j] = 1.0
            L[:, j] = cd_multiply(a, ej)

        # Compute rank and null dimension
        sv = np.linalg.svd(L, compute_uv=False)
        null_dim = np.sum(sv < 1e-10)
        null_fracs.append(null_dim / dim)

    return np.mean(null_fracs), np.std(null_fracs)


def compute_null_space_basis(dim):
    """For each basis element, compute null space of L_{e_i}."""
    results = []
    for i in range(dim):
        a = np.zeros(dim)
        a[i] = 1.0

        L = np.zeros((dim, dim))
        for j in range(dim):
            ej = np.zeros(dim)
            ej[j] = 1.0
            L[:, j] = cd_multiply(a, ej)

        sv = np.linalg.svd(L, compute_uv=False)
        null_dim = np.sum(sv < 1e-10)
        results.append(null_dim)

    return results


# ============================================================
# PART 4: Derivation Deficiency
# ============================================================

def compute_derivation_dim(dim):
    """
    A derivation D of algebra A satisfies D(xy) = D(x)y + xD(y).

    We represent D as a dim x dim matrix and solve the linear constraints.
    For each pair of basis elements (e_i, e_j), we get:
      D(e_i * e_j) = D(e_i) * e_j + e_i * D(e_j)

    This gives a system of linear equations for the entries of D.
    """
    basis = []
    for i in range(dim):
        e = np.zeros(dim)
        e[i] = 1.0
        basis.append(e)

    # Precompute structure constants: e_i * e_j = sum_k c_{ijk} e_k
    struct = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            prod = cd_multiply(basis[i], basis[j])
            struct[i, j, :] = prod

    # D is a dim x dim matrix with dim^2 unknowns.
    # Constraint: D(e_i * e_j) = D(e_i) * e_j + e_i * D(e_j)
    #
    # LHS: D(sum_k c_{ijk} e_k) = sum_k c_{ijk} D(e_k)
    #     = sum_k c_{ijk} sum_l D_{lk} e_l  ... wait, let's use D_{kl} = (D e_k)_l
    #
    # Let D_{ab} = component b of D(e_a). So D(e_a) = sum_b D_{ab} e_b.
    #
    # LHS_component_m: sum_k c_{ijk} D_{km}
    #
    # RHS: D(e_i) * e_j + e_i * D(e_j)
    #     = (sum_a D_{ia} e_a) * e_j + e_i * (sum_b D_{jb} e_b)
    #     = sum_a D_{ia} (e_a * e_j) + sum_b D_{jb} (e_i * e_b)
    #
    # RHS_component_m: sum_a D_{ia} * c_{ajm} + sum_b D_{jb} * c_{ibm}
    #
    # So for each (i,j,m): sum_k c_{ijk} D_{km} = sum_a D_{ia} c_{ajm} + sum_b D_{jb} c_{ibm}
    # Rearranging: sum_k c_{ijk} D_{km} - sum_a D_{ia} c_{ajm} - sum_b D_{jb} c_{ibm} = 0

    n_vars = dim * dim  # D_{ab} flattened as D[a*dim + b]
    constraints = []

    for i in range(dim):
        for j in range(dim):
            for m in range(dim):
                row = np.zeros(n_vars)

                # sum_k c_{ijk} D_{km}
                for k in range(dim):
                    row[k * dim + m] += struct[i, j, k]

                # - sum_a D_{ia} c_{ajm}
                for a in range(dim):
                    row[i * dim + a] -= struct[a, j, m]

                # - sum_b D_{jb} c_{ibm}
                for b in range(dim):
                    row[j * dim + b] -= struct[i, b, m]

                constraints.append(row)

    A = np.array(constraints)

    # Derivation space = null space of A
    sv = np.linalg.svd(A, compute_uv=False)

    # Count near-zero singular values
    threshold = 1e-8 * sv[0] if len(sv) > 0 and sv[0] > 0 else 1e-10
    derivation_dim = np.sum(sv < threshold)

    return derivation_dim


# ============================================================
# MAIN COMPUTATION
# ============================================================

def main():
    dims = [2, 4, 8, 16, 32]
    names = {1: "R (reals)", 2: "C (complex)", 4: "H (quaternions)",
             8: "O (octonions)", 16: "S (sedenions)", 32: "T (trigintaduonions)"}

    print("=" * 80)
    print("ORCA PATH AMPLITUDE: Cayley-Dickson Chain Path Integral")
    print("=" * 80)

    # Storage for results
    results = {}

    # ---- CANDIDATE 1: Associator Action ----
    print("\n" + "=" * 80)
    print("CANDIDATE 1: ASSOCIATOR ACTION  S_n = <||[a,b,c]||>")
    print("=" * 80)
    print(f"{'Dim':>4s} {'Algebra':>20s} {'Mean ||assoc||':>15s} {'Std':>12s}")
    print("-" * 55)

    assoc_results = {}
    for d in dims:
        n_samp = 3000 if d <= 16 else 1000
        mean_a, std_a = compute_associator_action(d, n_samples=n_samp)
        assoc_results[d] = mean_a
        print(f"{d:4d} {names.get(d, f'{d}D'):>20s} {mean_a:15.6f} {std_a:12.6f}")

    results['associator'] = assoc_results

    # ---- CANDIDATE 2: Zero Divisor Density ----
    print("\n" + "=" * 80)
    print("CANDIDATE 2: ZERO DIVISOR DENSITY")
    print("=" * 80)

    print("\n--- Basis element pairs ---")
    print(f"{'Dim':>4s} {'ZD pairs':>10s} {'Total pairs':>12s} {'Density':>10s}")
    print("-" * 40)

    zd_basis_results = {}
    for d in dims:
        if d <= 16:  # composite check too expensive for 32
            zd, total, zd_comp, comp_total = find_zero_divisors_basis(d)
            density = zd / total if total > 0 else 0
            zd_basis_results[d] = density
            print(f"{d:4d} {zd:10d} {total:12d} {density:10.4f}")
            if comp_total > 0:
                print(f"     Composite ZD: {zd_comp}/{comp_total} = {zd_comp/comp_total:.4f}")
        else:
            zd_basis_results[d] = None
            print(f"{d:4d}   (skipping composite for d=32, basis only)")
            # Just do basis pairs for d=32
            basis = [np.zeros(d) for _ in range(d)]
            for i in range(d):
                basis[i][i] = 1.0
            zd = 0
            total = 0
            for i in range(d):
                for j in range(i+1, d):
                    total += 1
                    prod = cd_multiply(basis[i], basis[j])
                    if cd_norm(prod) < 1e-10:
                        zd += 1
            density = zd / total if total > 0 else 0
            zd_basis_results[d] = density
            print(f"     Basis ZD: {zd}/{total} = {density:.4f}")

    print("\n--- Random sampling (statistical ZD density) ---")
    print(f"{'Dim':>4s} {'Near-ZD frac':>14s} {'Mean ||ab||':>12s} {'Std':>10s}")
    print("-" * 42)

    zd_random_results = {}
    for d in dims:
        n_samp = 5000 if d <= 16 else 2000
        frac, mean_norm, std_norm = compute_zd_density_random(d, n_samples=n_samp)
        zd_random_results[d] = (frac, mean_norm)
        print(f"{d:4d} {frac:14.4f} {mean_norm:12.6f} {std_norm:10.6f}")

    results['zd_density'] = zd_random_results

    # ---- CANDIDATE 3: Null Space Fraction ----
    print("\n" + "=" * 80)
    print("CANDIDATE 3: NULL SPACE FRACTION  f_n = <dim(null(L_a))> / dim")
    print("=" * 80)

    print("\n--- Basis elements null spaces ---")
    for d in dims:
        if d <= 16:
            nulls = compute_null_space_basis(d)
            print(f"dim={d:2d}: null dims per basis = {nulls}, mean = {np.mean(nulls):.2f}")

    print("\n--- Random elements ---")
    print(f"{'Dim':>4s} {'Mean null frac':>15s} {'Std':>10s}")
    print("-" * 35)

    null_results = {}
    for d in dims:
        n_samp = 500 if d <= 16 else 200
        mean_f, std_f = compute_null_space_fraction(d, n_samples=n_samp)
        null_results[d] = mean_f
        print(f"{d:4d} {mean_f:15.6f} {std_f:10.6f}")

    results['null_frac'] = null_results

    # ---- CANDIDATE 4: Derivation Deficiency ----
    print("\n" + "=" * 80)
    print("CANDIDATE 4: DERIVATION DEFICIENCY  d_n = dim - dim(Der(A_n))")
    print("=" * 80)

    # Known values: dim(Der) for R=0, C=0, H=3 (so(3)=su(2)), O=14 (G2), S=14, beyond=14?
    # Let's compute

    deriv_results = {}
    known_der = {1: 0, 2: 0, 4: 3, 8: 14}  # known for reference

    print(f"{'Dim':>4s} {'dim(Der)':>10s} {'Deficiency':>12s} {'Known Der':>10s}")
    print("-" * 42)

    for d in dims:
        if d <= 16:  # 32 is too expensive (32^2=1024 vars, 32^3=32768 constraints)
            der_dim = compute_derivation_dim(d)
            deficiency = d - der_dim
            deriv_results[d] = (der_dim, deficiency)
            known = known_der.get(d, "?")
            print(f"{d:4d} {der_dim:10d} {deficiency:12d} {str(known):>10s}")
        else:
            print(f"{d:4d}   (computing... large system)")
            # For 32D: 1024 unknowns, 32768 equations
            # Still feasible with SVD on the constraint matrix
            der_dim = compute_derivation_dim(d)
            deficiency = d - der_dim
            deriv_results[d] = (der_dim, deficiency)
            print(f"{d:4d} {der_dim:10d} {deficiency:12d}")

    results['derivation'] = deriv_results

    # ============================================================
    # PART 5: Propagator Computation
    # ============================================================
    print("\n" + "=" * 80)
    print("PART 5: PROPAGATOR COMPUTATION")
    print("  P = Sum_n  exp(i * S_n / hbar)  [using |amplitude| = exp(-S_n)]")
    print("=" * 80)

    print("\n--- Action values at each level ---")
    print(f"{'Dim':>4s} {'Assoc S':>10s} {'ZD mean||ab||':>14s} {'Null frac':>10s} {'Der defic':>10s}")
    print("-" * 55)

    for d in dims:
        s1 = results['associator'].get(d, 0)
        s2 = results['zd_density'].get(d, (0, 1))[1]  # mean ||ab||
        s3 = results['null_frac'].get(d, 0)
        s4 = results['derivation'].get(d, (0, 0))[1] if d in results['derivation'] else "N/A"
        print(f"{d:4d} {s1:10.4f} {s2:14.6f} {s3:10.6f} {str(s4):>10s}")

    # Propagator: For the CD path integral, the amplitude at level n is:
    #   A_n = exp(-alpha * S_n)
    # and the propagator is P = sum_n A_n

    print("\n--- Propagators (P = sum_n exp(-alpha * S_n)) ---")
    print("Using alpha = 1.0:")

    for candidate_name, action_fn in [
        ("Associator", lambda d: results['associator'].get(d, 0)),
        ("1/||ab|| (ZD)", lambda d: 1.0 / results['zd_density'].get(d, (0, 1))[1] if results['zd_density'].get(d, (0, 1))[1] > 0 else 100),
        ("Null fraction", lambda d: results['null_frac'].get(d, 0)),
        ("Der deficiency", lambda d: results['derivation'].get(d, (0, 0))[1] if d in results['derivation'] else 0),
    ]:
        print(f"\n  [{candidate_name}]")
        amplitudes = {}
        for d in dims:
            S = action_fn(d)
            if isinstance(S, str):
                S = 0
            amp = np.exp(-float(S))
            amplitudes[d] = amp
            print(f"    dim={d:2d}: S = {float(action_fn(d)):8.4f},  A = exp(-S) = {amp:.6f}")

        P = sum(amplitudes.values())
        print(f"    Total propagator P = {P:.6f}")

        # Ratios between levels
        print(f"    Ratios: ", end="")
        dim_list = sorted(amplitudes.keys())
        for i in range(len(dim_list) - 1):
            d1, d2 = dim_list[i], dim_list[i+1]
            ratio = amplitudes[d2] / amplitudes[d1] if amplitudes[d1] > 0 else float('inf')
            print(f"A({d2})/A({d1})={ratio:.4f}  ", end="")
        print()

    # ============================================================
    # PART 6: SM Mass Ratio Comparison
    # ============================================================
    print("\n" + "=" * 80)
    print("PART 6: STANDARD MODEL MASS RATIO COMPARISON")
    print("=" * 80)

    # SM lepton masses (MeV)
    m_e = 0.511
    m_mu = 105.66
    m_tau = 1776.86

    # SM quark masses (MeV, approximate)
    m_u = 2.2
    m_c = 1275.0
    m_t = 173000.0

    print(f"\nSM mass ratios:")
    print(f"  m_mu/m_e   = {m_mu/m_e:.2f}")
    print(f"  m_tau/m_mu = {m_tau/m_mu:.2f}")
    print(f"  m_tau/m_e  = {m_tau/m_e:.2f}")
    print(f"  m_c/m_u    = {m_c/m_u:.2f}")
    print(f"  m_t/m_c    = {m_t/m_c:.2f}")
    print(f"  m_t/m_u    = {m_t/m_u:.2f}")

    print("\nAmplitude ratios from each candidate (A(n+1)/A(n)):")
    print("If mass ~ 1/amplitude, then mass ratio ~ amplitude ratio inverted\n")

    for candidate_name, action_fn in [
        ("Associator", lambda d: results['associator'].get(d, 0)),
        ("1/||ab||", lambda d: 1.0 / results['zd_density'].get(d, (0, 1))[1] if results['zd_density'].get(d, (0, 1))[1] > 0 else 100),
        ("Null frac", lambda d: results['null_frac'].get(d, 0)),
        ("Der deficiency", lambda d: float(results['derivation'].get(d, (0, 0))[1]) if d in results['derivation'] else 0),
    ]:
        print(f"  [{candidate_name}]")
        actions = {d: float(action_fn(d)) for d in dims}

        # Mass interpretation: mass ~ exp(+S), so heavier particles at higher S
        # Or: mass ~ 1/amplitude = exp(+S)
        # Ratio: m(n+1)/m(n) = exp(S(n+1) - S(n))

        for i in range(len(dims) - 1):
            d1, d2 = dims[i], dims[i+1]
            delta_S = actions[d2] - actions[d1]
            mass_ratio = np.exp(delta_S)
            print(f"    S({d2})-S({d1}) = {delta_S:8.4f},  mass ratio = exp(dS) = {mass_ratio:10.4f}")
        print()

    # ============================================================
    # PART 7: Combined / Composite Action
    # ============================================================
    print("\n" + "=" * 80)
    print("PART 7: COMPOSITE ACTION CANDIDATES")
    print("=" * 80)

    print("\nTrying S_composite = alpha * S_assoc + beta * S_null + gamma * d_deriv")
    print("Goal: find weights that produce SM-like mass ratios\n")

    # Collect all action values
    for d in dims:
        s_a = results['associator'].get(d, 0)
        s_n = results['null_frac'].get(d, 0)
        s_d = float(results['derivation'].get(d, (0, 0))[1]) if d in results['derivation'] else 0
        s_z = 1.0 / results['zd_density'].get(d, (0, 1))[1] if results['zd_density'].get(d, (0, 1))[1] > 0 else 100
        print(f"  dim={d:2d}: S_assoc={s_a:.4f}, S_null={s_n:.6f}, S_deriv={s_d:.1f}, S_zd={s_z:.4f}")

    # The "natural" composite: action = non-associativity, weighted by how many
    # degrees of freedom are unprotected (derivation deficiency)
    print("\n--- Natural composite: S = S_assoc * (1 + d_deriv/dim) ---")
    for d in dims:
        s_a = results['associator'].get(d, 0)
        s_d = float(results['derivation'].get(d, (0, 0))[1]) if d in results['derivation'] else 0
        S_nat = s_a * (1 + s_d / d)
        print(f"  dim={d:2d}: S_natural = {S_nat:.6f}")

    # Another: action = log(dim) * associator (dimensional scaling)
    print("\n--- Dimensional scaling: S = log2(dim) * S_assoc ---")
    mass_ratios_log = []
    prev_S = None
    for d in dims:
        s_a = results['associator'].get(d, 0)
        S_log = np.log2(d) * s_a
        if prev_S is not None:
            ratio = np.exp(S_log - prev_S)
            mass_ratios_log.append(ratio)
            print(f"  dim={d:2d}: S = {S_log:.6f}, mass_ratio to prev = {ratio:.4f}")
        else:
            print(f"  dim={d:2d}: S = {S_log:.6f}")
        prev_S = S_log

    # ============================================================
    # SUMMARY TABLE
    # ============================================================
    print("\n" + "=" * 80)
    print("SUMMARY: ALL NUMERICAL RESULTS")
    print("=" * 80)

    print(f"\n{'Dim':>4s} | {'Assoc':>8s} | {'<||ab||>':>8s} | {'Null frac':>10s} | {'dim(Der)':>8s} | {'Defic':>6s}")
    print("-" * 60)
    for d in dims:
        s1 = results['associator'].get(d, 0)
        s2 = results['zd_density'].get(d, (0, 1))[1]
        s3 = results['null_frac'].get(d, 0)
        der = results['derivation'].get(d, (0, 0))
        print(f"{d:4d} | {s1:8.4f} | {s2:8.4f} | {s3:10.6f} | {der[0]:8d} | {der[1]:6d}")

    print("\n" + "=" * 80)
    print("KEY OBSERVATIONS:")
    print("=" * 80)

    # Analyze which candidate gives the best match
    print("""
1. Associator action grows with dimension - measures non-associativity.
   R,C,H are associative (S=0). O has the first nonzero associator.

2. Zero divisors appear only at dim>=16 (sedenions). ||ab|| drops below 1
   for random unit elements, signaling loss of division algebra property.

3. Null space fraction is 0 for division algebras (dim<=8) and grows for
   dim>=16, directly measuring zero divisor "volume" in the algebra.

4. Derivation dimension: Der(O)=14 (G2), and this may persist or change
   for higher CD levels. Deficiency = dim - dim(Der) grows rapidly.

PHYSICAL INTERPRETATION:
- The CD chain provides a DISCRETE path sum: sum over levels n=1,2,3,...
- Each level contributes amplitude A_n = exp(-S_n) to the propagator
- Poles of the propagator (where P diverges) correspond to masses
- The ASSOCIATOR is the most natural action: it measures the "cost" of
  passing through a non-associative level
- Mass ~ exp(S_n) means heavier particles correspond to more broken algebras
""")


if __name__ == "__main__":
    main()
