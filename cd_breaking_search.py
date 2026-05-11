# LONGINUS: sourceId=cd_breaking_search, sourcePath=cd_breaking_search.py
"""
Systematic search for a 5th algebraic breaking type in the Cayley-Dickson chain.
Tests identities that might HOLD at 32D but FAIL at 64D.
"""

import numpy as np
from itertools import product as iprod
import sys

np.random.seed(42)

# ============================================================
# Cayley-Dickson algebra implementation
# ============================================================

def cd_conj(a):
    """Conjugate in Cayley-Dickson algebra."""
    n = len(a)
    if n == 1:
        return a.copy()  # real numbers: conj is identity
    half = n // 2
    a1, a2 = a[:half], a[half:]
    return np.concatenate([cd_conj(a1), -a2])

def cd_mul(a, b):
    """
    Cayley-Dickson multiplication:
    (a1,a2)(b1,b2) = (a1*b1 - conj(b2)*a2, b2*a1 + a2*conj(b1))
    """
    n = len(a)
    assert len(b) == n, f"Dimension mismatch: {len(a)} vs {len(b)}"
    if n == 1:
        return a * b  # real multiplication
    half = n // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]

    part1 = cd_mul(a1, b1) - cd_mul(cd_conj(b2), a2)
    part2 = cd_mul(b2, a1) + cd_mul(a2, cd_conj(b1))
    return np.concatenate([part1, part2])

def cd_norm(a):
    """Norm of a CD element."""
    return np.sqrt(np.sum(a**2))

def rand_unit(dim):
    """Random unit vector in R^dim."""
    v = np.random.randn(dim)
    return v / np.linalg.norm(v)

def cd_power(a, n):
    """Compute a^n using repeated multiplication (left-to-right)."""
    if n == 0:
        result = np.zeros_like(a)
        result[0] = 1.0
        return result
    if n == 1:
        return a.copy()
    result = a.copy()
    for _ in range(n - 1):
        result = cd_mul(result, a)
    return result

def cd_commutator(a, b):
    """[a,b] = ab - ba"""
    return cd_mul(a, b) - cd_mul(b, a)

def cd_associator(a, b, c):
    """(a,b,c) = (ab)c - a(bc)"""
    return cd_mul(cd_mul(a, b), c) - cd_mul(a, cd_mul(b, c))

def error(lhs, rhs):
    """Relative error between two CD elements."""
    diff = np.linalg.norm(lhs - rhs)
    scale = max(np.linalg.norm(lhs), np.linalg.norm(rhs), 1e-15)
    return diff / scale

# ============================================================
# Identity testers — each returns (lhs, rhs) for error computation
# ============================================================

def test_moufang_1(a, b, c):
    """M1: a(b(ac)) = ((ab)a)c"""
    lhs = cd_mul(a, cd_mul(b, cd_mul(a, c)))
    rhs = cd_mul(cd_mul(cd_mul(a, b), a), c)
    return lhs, rhs

def test_moufang_2(a, b, c):
    """M2: ((ca)b)a = c(a(ba))"""
    lhs = cd_mul(cd_mul(cd_mul(c, a), b), a)
    rhs = cd_mul(c, cd_mul(a, cd_mul(b, a)))
    return lhs, rhs

def test_moufang_3(a, b, c):
    """M3: (ab)(ca) = a((bc)a)"""
    lhs = cd_mul(cd_mul(a, b), cd_mul(c, a))
    rhs = cd_mul(a, cd_mul(cd_mul(b, c), a))
    return lhs, rhs

def test_left_bol(a, b, c):
    """Left Bol: a(b(ac)) = (a(ba))c"""
    lhs = cd_mul(a, cd_mul(b, cd_mul(a, c)))
    rhs = cd_mul(cd_mul(a, cd_mul(b, a)), c)
    return lhs, rhs

def test_right_bol(a, b, c):
    """Right Bol: ((ca)b)a = c((ab)a)"""
    lhs = cd_mul(cd_mul(cd_mul(c, a), b), a)
    rhs = cd_mul(c, cd_mul(cd_mul(a, b), a))
    return lhs, rhs

def test_malcev(a, b, c):
    """Malcev: J(a,b,ac) = J(a,b,c)*a where J(x,y,z)=(xy)z+(yz)x+(zx)y"""
    def jacobi(x, y, z):
        return cd_mul(cd_mul(x, y), z) + cd_mul(cd_mul(y, z), x) + cd_mul(cd_mul(z, x), y)
    ac = cd_mul(a, c)
    lhs = jacobi(a, b, ac)
    rhs = cd_mul(jacobi(a, b, c), a)
    return lhs, rhs

def test_right_flexibility(a, b):
    """a(b(ab)) = (ab)(ab)"""
    ab = cd_mul(a, b)
    lhs = cd_mul(a, cd_mul(b, ab))
    rhs = cd_mul(ab, ab)
    return lhs, rhs

def test_higher_order_flex(a, b):
    """(ba)((ba)a) = ((ba)b)(aa)"""
    ba = cd_mul(b, a)
    aa = cd_mul(a, a)
    lhs = cd_mul(ba, cd_mul(ba, a))
    rhs = cd_mul(cd_mul(ba, b), aa)
    return lhs, rhs

def test_linearized_flex(a, b, c):
    """a(bc) + c(ba) = (ab)c + (cb)a"""
    lhs = cd_mul(a, cd_mul(b, c)) + cd_mul(c, cd_mul(b, a))
    rhs = cd_mul(cd_mul(a, b), c) + cd_mul(cd_mul(c, b), a)
    return lhs, rhs

def test_power_assoc_5(a):
    """a^2 * a^3 = a^5"""
    a2 = cd_mul(a, a)
    a3 = cd_mul(a2, a)
    a5 = cd_mul(cd_mul(a3, a), a)  # a^5 = ((a^3)a)a
    lhs = cd_mul(a2, a3)
    return lhs, a5

def test_power_assoc_4(a):
    """(a^2)^2 = a^4"""
    a2 = cd_mul(a, a)
    lhs = cd_mul(a2, a2)
    a3 = cd_mul(a2, a)
    a4 = cd_mul(a3, a)
    return lhs, a4

def test_power_assoc_high(a, m, n):
    """a^m * a^n = a^(m+n) for higher orders"""
    am = cd_power(a, m)
    an = cd_power(a, n)
    amn = cd_power(a, m + n)
    lhs = cd_mul(am, an)
    return lhs, amn

def test_jacobi_commutator(a, b, c):
    """[a,[b,c]] + [b,[c,a]] + [c,[a,b]] = 0"""
    bc = cd_commutator(b, c)
    ca = cd_commutator(c, a)
    ab = cd_commutator(a, b)
    result = cd_commutator(a, bc) + cd_commutator(b, ca) + cd_commutator(c, ab)
    zero = np.zeros_like(result)
    return result, zero

def test_norm_product(a, b):
    """||ab|| / (||a|| ||b||) — should be 1 for composition algebras"""
    ab = cd_mul(a, b)
    ratio = cd_norm(ab) / (cd_norm(a) * cd_norm(b))
    return ratio

def test_cross_right_alt(a, b):
    """a(b^2) = (ab)b — right alternative on cross-sector"""
    b2 = cd_mul(b, b)
    lhs = cd_mul(a, b2)
    rhs = cd_mul(cd_mul(a, b), b)
    return lhs, rhs

def test_cross_left_alt(a, b):
    """(a^2)b = a(ab) — left alternative on cross-sector"""
    a2 = cd_mul(a, a)
    lhs = cd_mul(a2, b)
    rhs = cd_mul(a, cd_mul(a, b))
    return lhs, rhs

def test_jordan_triple(a, b, c):
    """Jordan triple product: (abc + cba)/2 symmetry
    Test: {a,b,{a,b,c}} = {a, b{a,b}, c} where {x,y,z} = (xyz+zyx)/2
    This is the Jordan triple product identity."""
    def jtp(x, y, z):
        return 0.5 * (cd_mul(cd_mul(x, y), z) + cd_mul(cd_mul(z, y), x))
    # Jordan identity: {a, b, {a,b,c}} vs {a, {b,a,b}, c}
    # i.e. J(a,b,J(a,b,c)) = J(a, (bab+bab)/2, c) = J(a, bab, c)
    inner = jtp(a, b, c)
    lhs = jtp(a, b, inner)
    bab = cd_mul(cd_mul(b, a), b)
    rhs = jtp(a, bab, c)
    return lhs, rhs

def test_flexibility(a, b):
    """Flexibility: a(ba) = (ab)a"""
    lhs = cd_mul(a, cd_mul(b, a))
    rhs = cd_mul(cd_mul(a, b), a)
    return lhs, rhs

def test_di_assoc(a, b):
    """Di-associativity check: subalgebra generated by two elements.
    Test (ab)a = a(ba) AND a(ab) = (aa)b ... etc.
    More precisely: (a^2)b = a(ab) for any a,b (left alternative)."""
    a2 = cd_mul(a, a)
    lhs = cd_mul(a2, b)
    rhs = cd_mul(a, cd_mul(a, b))
    return lhs, rhs

def test_middle_moufang_variant(a, b, c):
    """Variant: (ab)(ca) = (a(bc))a"""
    lhs = cd_mul(cd_mul(a, b), cd_mul(c, a))
    rhs = cd_mul(cd_mul(a, cd_mul(b, c)), a)
    return lhs, rhs

def test_associator_alternating(a, b, c):
    """Associator is alternating: (a,b,c) = -(b,a,c)"""
    lhs = cd_associator(a, b, c)
    rhs = -cd_associator(b, a, c)
    return lhs, rhs

def test_associator_skew(a, b, c):
    """Associator skew-symmetry: (a,b,c) = -(a,c,b)"""
    lhs = cd_associator(a, b, c)
    rhs = -cd_associator(a, c, b)
    return lhs, rhs

def test_malcev_identity_v2(a, b, c):
    """Malcev identity (alternative form):
    ((ab)c)a + ((ba)c)a - b((ac)a) - a((ac)b) ...
    Actually: J(a,b,ac) = J(a,b,c)a (same as above, but let's also try):
    (a,b,[a,c]) + (a,c,[a,b]) = 0 where (x,y,z) is associator, [x,y] commutator
    This is another characterization of Malcev algebras."""
    ac_comm = cd_commutator(a, c)
    ab_comm = cd_commutator(a, b)
    lhs = cd_associator(a, b, ac_comm) + cd_associator(a, c, ab_comm)
    rhs = np.zeros_like(a)
    return lhs, rhs

# ============================================================
# Main testing framework
# ============================================================

def run_tests(dim, n_samples=100):
    """Run all identity tests for a given dimension."""
    results = {}

    print(f"\n{'='*60}")
    print(f"  TESTING DIMENSION = {dim}  ({n_samples} samples each)")
    print(f"{'='*60}")

    # --- 3-variable identities ---
    three_var_tests = {
        'Moufang-1: a(b(ac))=((ab)a)c': test_moufang_1,
        'Moufang-2: ((ca)b)a=c(a(ba))': test_moufang_2,
        'Moufang-3: (ab)(ca)=a((bc)a)': test_moufang_3,
        'Left-Bol: a(b(ac))=(a(ba))c': test_left_bol,
        'Right-Bol: ((ca)b)a=c((ab)a)': test_right_bol,
        'Malcev: J(a,b,ac)=J(a,b,c)a': test_malcev,
        'Linearized-Flex: a(bc)+c(ba)=(ab)c+(cb)a': test_linearized_flex,
        'Mid-Moufang-Var: (ab)(ca)=(a(bc))a': test_middle_moufang_variant,
        'Assoc-Alternating: (a,b,c)=-(b,a,c)': test_associator_alternating,
        'Assoc-Skew: (a,b,c)=-(a,c,b)': test_associator_skew,
        'Malcev-v2: (a,b,[a,c])+(a,c,[a,b])=0': test_malcev_identity_v2,
        'Jordan-Triple-Product': test_jordan_triple,
    }

    for name, test_fn in three_var_tests.items():
        errors = []
        for _ in range(n_samples):
            a, b, c = rand_unit(dim), rand_unit(dim), rand_unit(dim)
            lhs, rhs = test_fn(a, b, c)
            errors.append(error(lhs, rhs))
        mean_err = np.mean(errors)
        std_err = np.std(errors)
        max_err = np.max(errors)
        results[name] = (mean_err, std_err, max_err)
        status = "PASS" if mean_err < 0.01 else "FAIL"
        print(f"  [{status}] {name}: mean={mean_err:.6f} std={std_err:.6f} max={max_err:.6f}")

    # --- 2-variable identities ---
    two_var_tests = {
        'Flexibility: a(ba)=(ab)a': test_flexibility,
        'Right-Flex: a(b(ab))=(ab)(ab)': test_right_flexibility,
        'Higher-Order-Flex: (ba)((ba)a)=((ba)b)(aa)': test_higher_order_flex,
        'Left-Alternative: (a^2)b=a(ab)': test_di_assoc,
        'Right-Alternative: a(b^2)=(ab)b': test_cross_right_alt,
        'Left-Alt-v2: (a^2)b=a(ab)': test_cross_left_alt,
    }

    for name, test_fn in two_var_tests.items():
        errors = []
        for _ in range(n_samples):
            a, b = rand_unit(dim), rand_unit(dim)
            lhs, rhs = test_fn(a, b)
            errors.append(error(lhs, rhs))
        mean_err = np.mean(errors)
        std_err = np.std(errors)
        max_err = np.max(errors)
        results[name] = (mean_err, std_err, max_err)
        status = "PASS" if mean_err < 0.01 else "FAIL"
        print(f"  [{status}] {name}: mean={mean_err:.6f} std={std_err:.6f} max={max_err:.6f}")

    # --- 1-variable (power associativity) ---
    power_tests = {}
    for (m, n) in [(2,3), (2,4), (3,3), (2,5), (3,4), (4,4), (2,6), (3,5), (4,5)]:
        tname = f'Power: a^{m}*a^{n}=a^{m+n}'
        errors = []
        for _ in range(n_samples):
            a = rand_unit(dim)
            lhs, rhs = test_power_assoc_high(a, m, n)
            errors.append(error(lhs, rhs))
        mean_err = np.mean(errors)
        std_err = np.std(errors)
        max_err = np.max(errors)
        results[tname] = (mean_err, std_err, max_err)
        status = "PASS" if mean_err < 0.01 else "FAIL"
        print(f"  [{status}] {tname}: mean={mean_err:.6f} std={std_err:.6f} max={max_err:.6f}")

    # --- Jacobi identity for commutators ---
    errors = []
    for _ in range(n_samples):
        a, b, c = rand_unit(dim), rand_unit(dim), rand_unit(dim)
        lhs, rhs = test_jacobi_commutator(a, b, c)
        errors.append(error(lhs, rhs))
    mean_err = np.mean(errors)
    std_err = np.std(errors)
    max_err = np.max(errors)
    results['Jacobi-Commutator'] = (mean_err, std_err, max_err)
    status = "PASS" if mean_err < 0.01 else "FAIL"
    print(f"  [{status}] Jacobi-Commutator: mean={mean_err:.6f} std={std_err:.6f} max={max_err:.6f}")

    # --- Norm product ratio ---
    ratios = []
    for _ in range(n_samples):
        a, b = rand_unit(dim), rand_unit(dim)
        r = test_norm_product(a, b)
        ratios.append(r)
    ratio_mean = np.mean(ratios)
    ratio_std = np.std(ratios)
    ratio_min = np.min(ratios)
    ratio_max = np.max(ratios)
    results['Norm-Ratio: ||ab||/(||a||||b||)'] = (abs(ratio_mean - 1.0), ratio_std, abs(ratio_max - 1.0))
    print(f"  [INFO] Norm-Ratio: mean={ratio_mean:.6f} std={ratio_std:.6f} min={ratio_min:.6f} max={ratio_max:.6f}")

    # --- Cross-sector tests (a in lower half, b in upper half) ---
    cross_tests = {
        'Cross-Right-Alt: a(b^2)=(ab)b [sectors]': test_cross_right_alt,
        'Cross-Left-Alt: (a^2)b=a(ab) [sectors]': test_cross_left_alt,
    }

    for name, test_fn in cross_tests.items():
        errors = []
        for _ in range(n_samples):
            # a in lower half, b in upper half
            a = np.zeros(dim)
            a[:dim//2] = np.random.randn(dim//2)
            a /= np.linalg.norm(a)
            b = np.zeros(dim)
            b[dim//2:] = np.random.randn(dim//2)
            b /= np.linalg.norm(b)
            lhs, rhs = test_fn(a, b)
            errors.append(error(lhs, rhs))
        mean_err = np.mean(errors)
        std_err = np.std(errors)
        max_err = np.max(errors)
        results[name] = (mean_err, std_err, max_err)
        status = "PASS" if mean_err < 0.01 else "FAIL"
        print(f"  [{status}] {name}: mean={mean_err:.6f} std={std_err:.6f} max={max_err:.6f}")

    return results

# ============================================================
# Run for 32D and 64D, then compare
# ============================================================

print("=" * 70)
print("  CAYLEY-DICKSON BREAKING SEARCH: dim=32 vs dim=64")
print("  Looking for identities that HOLD at 32D but FAIL at 64D")
print("=" * 70)

N_SAMPLES = 120

results_32 = run_tests(32, N_SAMPLES)
results_64 = run_tests(64, N_SAMPLES)

# ============================================================
# Summary comparison table
# ============================================================

print("\n")
print("=" * 90)
print("  COMPARISON TABLE: dim=32 vs dim=64")
print("=" * 90)
print(f"{'Identity':<50} {'32D mean':>10} {'64D mean':>10} {'Delta':>10} {'FLAG':>8}")
print("-" * 90)

flagged = []
for name in results_32:
    if name in results_64:
        m32 = results_32[name][0]
        m64 = results_64[name][0]
        delta = m64 - m32
        flag = ""
        if m32 < 0.01 and m64 > 0.1:
            flag = "**NEW**"
            flagged.append(name)
        elif m32 < 0.01 and m64 > 0.01:
            flag = "*MAYBE*"
            flagged.append(name)
        elif m32 < 0.05 and m64 > 0.05 and delta > 0.03:
            flag = "*DIFF*"
            flagged.append(name)
        print(f"  {name:<48} {m32:>10.6f} {m64:>10.6f} {delta:>+10.6f} {flag:>8}")

print("-" * 90)

if flagged:
    print(f"\n  *** FLAGGED IDENTITIES ({len(flagged)} found): ***")
    for name in flagged:
        m32 = results_32[name][0]
        m64 = results_64[name][0]
        print(f"    -> {name}")
        print(f"       32D: {m32:.6f}  |  64D: {m64:.6f}  |  RATIO: {m64/max(m32,1e-15):.1f}x")
    print()
else:
    print("\n  No new breaking types detected.\n")

# ============================================================
# Additional targeted test: check if any identity is *exactly*
# preserved at 32D (error < 1e-10) but broken at 64D
# ============================================================

print("=" * 90)
print("  PRECISION CHECK: Identities with near-zero error at 32D")
print("=" * 90)

for name in results_32:
    if name in results_64:
        m32 = results_32[name][0]
        m64 = results_64[name][0]
        if m32 < 1e-6:
            ratio = m64 / max(m32, 1e-15)
            print(f"  {name:<48} 32D={m32:.2e}  64D={m64:.2e}  ratio={ratio:.1f}x")

print("\nDone.")
