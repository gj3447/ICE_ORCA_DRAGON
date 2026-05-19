# LONGINUS: sourceId=cd_breaking_search2, sourcePath=cd_breaking_search2.py
"""
Deep search for 5th algebraic breaking: more exotic identities.
Focus on identities involving 4+ elements, nested structures, and
properties that are known to hold in specific loop classes.
"""

import numpy as np
np.random.seed(123)

# ============================================================
# Cayley-Dickson core (same as before)
# ============================================================

def cd_conj(a):
    n = len(a)
    if n == 1:
        return a.copy()
    half = n // 2
    return np.concatenate([cd_conj(a[:half]), -a[half:]])

def cd_mul(a, b):
    n = len(a)
    if n == 1:
        return a * b
    half = n // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    part1 = cd_mul(a1, b1) - cd_mul(cd_conj(b2), a2)
    part2 = cd_mul(b2, a1) + cd_mul(a2, cd_conj(b1))
    return np.concatenate([part1, part2])

def cd_norm(a):
    return np.sqrt(np.sum(a**2))

def rand_unit(dim):
    v = np.random.randn(dim)
    return v / np.linalg.norm(v)

def cd_power(a, n):
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

def cd_inv(a):
    """Multiplicative inverse: conj(a)/||a||^2"""
    return cd_conj(a) / np.sum(a**2)

def error(lhs, rhs):
    diff = np.linalg.norm(lhs - rhs)
    scale = max(np.linalg.norm(lhs), np.linalg.norm(rhs), 1e-15)
    return diff / scale

def error_abs(val):
    """Absolute error from zero."""
    return np.linalg.norm(val)

N = 150  # samples per test

def test_identity(name, test_fn, dims=[8, 16, 32, 64], n_args=3):
    """Generic tester. test_fn takes (dim) and returns list of errors."""
    results = {}
    for dim in dims:
        errors = []
        for _ in range(N):
            args = [rand_unit(dim) for _ in range(n_args)]
            e = test_fn(*args)
            errors.append(e)
        results[dim] = (np.mean(errors), np.std(errors), np.max(errors), np.min(errors))
    return results

print("=" * 100)
print("  DEEP SEARCH FOR 5th BREAKING TYPE IN CAYLEY-DICKSON CHAIN")
print("  Testing across dims: 8, 16, 32, 64")
print(f"  Samples per test: {N}")
print("=" * 100)

all_results = {}

# ============================================================
# 1. FOUR-VARIABLE IDENTITIES (more likely to show new breaking)
# ============================================================

def four_var_assoc_chain(a, b, c, d):
    """((ab)c)d vs a(b(cd)) — full 4-variable associativity.
    Not expected to hold, but check if the ERROR PATTERN changes."""
    lhs = cd_mul(cd_mul(cd_mul(a, b), c), d)
    rhs = cd_mul(a, cd_mul(b, cd_mul(c, d)))
    return error(lhs, rhs)

def four_var_pentagonal(a, b, c, d):
    """Pentagon identity / Mac Lane coherence:
    Check if a((bc)d) = (a(bc))d relates to ((ab)c)d in a structured way.
    Test: a((bc)d) - ((ab)c)d + (a(bc))d - a(b(cd)) + (ab)(cd) = 0 ?
    This is a generalized associahedron relation."""
    t1 = cd_mul(a, cd_mul(cd_mul(b, c), d))
    t2 = cd_mul(cd_mul(cd_mul(a, b), c), d)
    t3 = cd_mul(cd_mul(a, cd_mul(b, c)), d)
    t4 = cd_mul(a, cd_mul(b, cd_mul(c, d)))
    t5 = cd_mul(cd_mul(a, b), cd_mul(c, d))
    val = t1 - t2 + t3 - t4 + t5
    scale = max(cd_norm(t1), cd_norm(t2), 1e-10)
    return np.linalg.norm(val) / scale

def four_var_teichmüller(a, b, c, d):
    """Teichmüller identity: sum of 5 associators.
    (a,b,cd) - (a,bc,d) + (ab,c,d) - a(b,c,d) - (a,b,c)d
    Should = 0 in any ring. Let's verify and check numerical stability."""
    def assoc(x, y, z):
        return cd_mul(cd_mul(x, y), z) - cd_mul(x, cd_mul(y, z))
    cd_prod = cd_mul(c, d)
    bc_prod = cd_mul(b, c)
    ab_prod = cd_mul(a, b)
    t1 = assoc(a, b, cd_prod)
    t2 = assoc(a, bc_prod, d)
    t3 = assoc(ab_prod, c, d)
    t4 = cd_mul(a, assoc(b, c, d))
    t5 = cd_mul(assoc(a, b, c), d)
    val = t1 - t2 + t3 - t4 - t5
    scale = max(cd_norm(t1), cd_norm(t2), cd_norm(t3), 1e-10)
    return np.linalg.norm(val) / scale

print("\n--- FOUR-VARIABLE IDENTITIES ---")
for name, fn in [
    ('4-var assoc chain', four_var_assoc_chain),
    ('Pentagon relation', four_var_pentagonal),
    ('Teichmuller identity', four_var_teichmüller),
]:
    res = test_identity(name, fn, n_args=4)
    all_results[name] = res
    print(f"\n  {name}:")
    for dim in [8, 16, 32, 64]:
        m, s, mx, mn = res[dim]
        print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 2. ELASTICITY / IP-LOOP IDENTITIES
# ============================================================

def test_elasticity(a, b):
    """Elasticity: (ab)(ba) = (a(bb))a ...
    Actually test: (ab)(ba) = a((bb)a) — related to Moufang but different."""
    ab = cd_mul(a, b)
    ba = cd_mul(b, a)
    bb = cd_mul(b, b)
    lhs = cd_mul(ab, ba)
    rhs = cd_mul(a, cd_mul(bb, a))
    return error(lhs, rhs)

def test_LC_identity(a, b, c):
    """LC identity: a(b(cb)) = ((ab)c)b — holds in LC loops"""
    lhs = cd_mul(a, cd_mul(b, cd_mul(c, b)))
    rhs = cd_mul(cd_mul(cd_mul(a, b), c), b)
    return error(lhs, rhs)

def test_RC_identity(a, b, c):
    """RC identity: ((ba)c)a = b(a(ca)) — holds in RC loops"""
    lhs = cd_mul(cd_mul(cd_mul(b, a), c), a)
    rhs = cd_mul(b, cd_mul(a, cd_mul(c, a)))
    return error(lhs, rhs)

def test_C_identity(a, b, c):
    """C-loop identity: a(b(cb)) = ((ab)c)b AND ((ba)c)a = b(a(ca))
    Average of LC + RC errors."""
    e1 = test_LC_identity(a, b, c)
    e2 = test_RC_identity(a, b, c)
    return (e1 + e2) / 2

def test_nuclear_square(a, b):
    """Nuclear square: (a^2)(b^2) = (ab)^2 ... holds in what structures?"""
    a2 = cd_mul(a, a)
    b2 = cd_mul(b, b)
    ab = cd_mul(a, b)
    lhs = cd_mul(a2, b2)
    rhs = cd_mul(ab, ab)
    return error(lhs, rhs)

def test_automorphic_inverse(a, b):
    """AIP: (ab)^{-1} = a^{-1} b^{-1}"""
    ab = cd_mul(a, b)
    lhs = cd_inv(ab)
    rhs = cd_mul(cd_inv(a), cd_inv(b))
    return error(lhs, rhs)

def test_anti_automorphic_inverse(a, b):
    """AAIP: (ab)^{-1} = b^{-1} a^{-1}"""
    ab = cd_mul(a, b)
    lhs = cd_inv(ab)
    rhs = cd_mul(cd_inv(b), cd_inv(a))
    return error(lhs, rhs)

print("\n--- LOOP THEORY IDENTITIES ---")
for name, fn, nargs in [
    ('Elasticity: (ab)(ba)=a((bb)a)', test_elasticity, 2),
    ('LC-loop: a(b(cb))=((ab)c)b', test_LC_identity, 3),
    ('RC-loop: ((ba)c)a=b(a(ca))', test_RC_identity, 3),
    ('Nuclear-square: (a^2)(b^2)=(ab)^2', test_nuclear_square, 2),
    ('AIP: (ab)^-1 = a^-1 b^-1', test_automorphic_inverse, 2),
    ('AAIP: (ab)^-1 = b^-1 a^-1', test_anti_automorphic_inverse, 2),
]:
    res = test_identity(name, fn, n_args=nargs)
    all_results[name] = res
    print(f"\n  {name}:")
    for dim in [8, 16, 32, 64]:
        m, s, mx, mn = res[dim]
        print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 3. HIGHER-ORDER POWER TESTS
# ============================================================

def test_power_high_order(a):
    """Test a^m * a^n = a^(m+n) for large m,n up to 12."""
    max_err = 0.0
    for (m, n) in [(5,5), (5,6), (6,6), (4,7), (3,8), (5,7), (6,7)]:
        am = cd_power(a, m)
        an = cd_power(a, n)
        amn = cd_power(a, m + n)
        lhs = cd_mul(am, an)
        e = error(lhs, amn)
        if e > max_err:
            max_err = e
    return max_err

print("\n--- HIGHER-ORDER POWER ASSOCIATIVITY ---")
res = test_identity('Power a^m*a^n=a^(m+n), m+n up to 13', test_power_high_order, n_args=1)
all_results['High-power-assoc'] = res
for dim in [8, 16, 32, 64]:
    m, s, mx, mn = res[dim]
    print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 4. DERIVATION / INNER MAPPING IDENTITIES
# ============================================================

def test_inner_map_assoc(a, b, c):
    """Inner mapping group property:
    R(a,b) = R_a R_b R_{ab}^{-1} where R_x(y) = yx.
    Test if R(a,b) is an automorphism:
    R(a,b)(cd) = R(a,b)(c) * R(a,b)(d)
    This should hold in groups (associative case) but what about CD?"""
    d = rand_unit(len(a))  # need 4th element
    ab = cd_mul(a, b)
    ab_inv = cd_inv(ab)
    def R_map(x):
        return cd_mul(cd_mul(cd_mul(x, a), b), ab_inv)
    cd_prod = cd_mul(c, d)
    lhs = R_map(cd_prod)
    rhs = cd_mul(R_map(c), R_map(d))
    return error(lhs, rhs)

print("\n--- INNER MAPPING / DERIVATION ---")
res = test_identity('Inner-map automorphism', test_inner_map_assoc, n_args=3)
all_results['Inner-map-auto'] = res
for dim in [8, 16, 32, 64]:
    m, s, mx, mn = res[dim]
    print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 5. NORM SUBMULTIPLICATIVITY AND SPECTRUM
# ============================================================

def test_norm_detailed(a, b):
    """||ab||^2 vs ||a||^2 ||b||^2"""
    ab = cd_mul(a, b)
    lhs = cd_norm(ab)**2
    rhs = cd_norm(a)**2 * cd_norm(b)**2
    return abs(lhs - rhs) / max(rhs, 1e-15)

print("\n--- NORM COMPOSITION ---")
res = test_identity('Norm: ||ab||^2 / ||a||^2||b||^2 - 1', test_norm_detailed, n_args=2)
all_results['Norm-composition'] = res
for dim in [8, 16, 32, 64]:
    m, s, mx, mn = res[dim]
    print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 6. QUADRATIC IDENTITY (x^2 - 2Re(x)x + ||x||^2 = 0)
# This should always hold in CD algebras. Verify.
# ============================================================

def test_quadratic(a):
    """x^2 - 2*Re(x)*x + ||x||^2 * 1 = 0"""
    a2 = cd_mul(a, a)
    one = np.zeros_like(a)
    one[0] = 1.0
    val = a2 - 2*a[0]*a + np.sum(a**2)*one
    return np.linalg.norm(val) / max(cd_norm(a2), 1e-15)

print("\n--- QUADRATIC IDENTITY ---")
res = test_identity('Quadratic: x^2 - 2Re(x)x + ||x||^2 = 0', test_quadratic, n_args=1)
all_results['Quadratic'] = res
for dim in [8, 16, 32, 64]:
    m, s, mx, mn = res[dim]
    print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 7. WEAK ASSOCIATIVITY PROPERTIES
# ============================================================

def test_right_power_alt(a, b):
    """Right power alternative: (ab^n)b = a(b^{n+1}) for n=2,3,4"""
    max_err = 0.0
    for n in [2, 3, 4, 5]:
        bn = cd_power(b, n)
        bn1 = cd_power(b, n+1)
        lhs = cd_mul(cd_mul(a, bn), b)
        rhs = cd_mul(a, bn1)
        e = error(lhs, rhs)
        if e > max_err:
            max_err = e
    return max_err

def test_left_power_alt(a, b):
    """Left power alternative: b(b^n a) = b^{n+1} a for n=2,3,4"""
    max_err = 0.0
    for n in [2, 3, 4, 5]:
        bn = cd_power(b, n)
        bn1 = cd_power(b, n+1)
        lhs = cd_mul(b, cd_mul(bn, a))
        rhs = cd_mul(bn1, a)
        e = error(lhs, rhs)
        if e > max_err:
            max_err = e
    return max_err

def test_power_flex(a, b):
    """Power flexibility: a^n (b a^n) = (a^n b) a^n for various n"""
    max_err = 0.0
    for n in [2, 3, 4]:
        an = cd_power(a, n)
        lhs = cd_mul(an, cd_mul(b, an))
        rhs = cd_mul(cd_mul(an, b), an)
        e = error(lhs, rhs)
        if e > max_err:
            max_err = e
    return max_err

print("\n--- POWER-RELATED WEAK ASSOCIATIVITY ---")
for name, fn in [
    ('Right-power-alt: (ab^n)b = a(b^{n+1})', test_right_power_alt),
    ('Left-power-alt: b(b^n a) = b^{n+1} a', test_left_power_alt),
    ('Power-flex: a^n(ba^n) = (a^n b)a^n', test_power_flex),
]:
    res = test_identity(name, fn, n_args=2)
    all_results[name] = res
    print(f"\n  {name}:")
    for dim in [8, 16, 32, 64]:
        m, s, mx, mn = res[dim]
        print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 8. GENERALIZED BOL / BRUCK IDENTITIES
# ============================================================

def test_bruck(a, b):
    """Bruck identity: ((ab)b^{-1})b = a(bb) ... hmm
    Actually Bruck / K-loop: (a(ba))^{-1} = a^{-1}(b^{-1}a^{-1})"""
    aba = cd_mul(a, cd_mul(b, a))
    lhs = cd_inv(aba)
    rhs = cd_mul(cd_inv(a), cd_mul(cd_inv(b), cd_inv(a)))
    return error(lhs, rhs)

def test_left_bol_inverse(a, b):
    """In a left Bol loop: (a(ba))^{-1} = a^{-1}(b^{-1}a^{-1})
    Compare with AAIP."""
    aba = cd_mul(a, cd_mul(b, a))
    lhs = cd_inv(aba)
    rhs = cd_mul(cd_inv(a), cd_mul(cd_inv(b), cd_inv(a)))
    return error(lhs, rhs)

def test_extra_loop(a, b, c):
    """Extra loop identity: (a(bc))a = (ab)(ca)
    Same as middle Moufang, tested again for completeness with different sampling."""
    lhs = cd_mul(cd_mul(a, cd_mul(b, c)), a)
    rhs = cd_mul(cd_mul(a, b), cd_mul(c, a))
    return error(lhs, rhs)

def test_cc_loop(a, b, c):
    """CC-loop (conjugacy closed): a(b(ca)) = ((ab)c)a ... relates LC/RC
    Actually: La conj = inner auto. Test: (a\\(ab))c = b(a\\(ac))
    where a\\x = a^{-1} x"""
    a_inv = cd_inv(a)
    lhs_inner = cd_mul(a_inv, cd_mul(a, b))  # should be b if alternative
    lhs = cd_mul(lhs_inner, c)
    rhs_inner = cd_mul(a_inv, cd_mul(a, c))  # should be c
    rhs = cd_mul(b, rhs_inner)
    return error(lhs, rhs)

print("\n--- BOL / BRUCK / EXTRA / CC LOOP ---")
for name, fn, nargs in [
    ('Bruck: (a(ba))^-1 = a^-1(b^-1 a^-1)', test_bruck, 2),
    ('Extra-loop: (a(bc))a = (ab)(ca)', test_extra_loop, 3),
    ('CC-loop cancellation', test_cc_loop, 3),
]:
    res = test_identity(name, fn, n_args=nargs)
    all_results[name] = res
    print(f"\n  {name}:")
    for dim in [8, 16, 32, 64]:
        m, s, mx, mn = res[dim]
        print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 9. COMMUTATOR-ASSOCIATOR INTERACTION
# ============================================================

def test_comm_assoc_relation(a, b, c):
    """[a, (b,c,a)] + [(a,b,c), a] = 0 ?
    Or: the associator commutes with elements in certain patterns."""
    assoc_bca = cd_mul(cd_mul(b, c), a) - cd_mul(b, cd_mul(c, a))
    assoc_abc = cd_mul(cd_mul(a, b), c) - cd_mul(a, cd_mul(b, c))
    comm1 = cd_mul(a, assoc_bca) - cd_mul(assoc_bca, a)
    comm2 = cd_mul(assoc_abc, a) - cd_mul(a, assoc_abc)
    val = comm1 + comm2
    scale = max(cd_norm(comm1), cd_norm(comm2), 1e-15)
    return np.linalg.norm(val) / scale

def test_triple_commutator(a, b, c):
    """[[a,b],c] + [[b,c],a] + [[c,a],b] — this is Jacobi again but
    let's check [[a,b],[c,d]] decomposition for 4 vars."""
    ab = cd_mul(a, b) - cd_mul(b, a)
    bc = cd_mul(b, c) - cd_mul(c, b)
    ca = cd_mul(c, a) - cd_mul(a, c)
    t1 = cd_mul(ab, c) - cd_mul(c, ab)
    t2 = cd_mul(bc, a) - cd_mul(a, bc)
    t3 = cd_mul(ca, b) - cd_mul(b, ca)
    val = t1 + t2 + t3
    scale = max(cd_norm(t1), cd_norm(t2), cd_norm(t3), 1e-15)
    return np.linalg.norm(val) / scale

print("\n--- COMMUTATOR-ASSOCIATOR INTERACTIONS ---")
for name, fn in [
    ('[a,(b,c,a)]+[(a,b,c),a]=0 ?', test_comm_assoc_relation),
    ('Triple-Jacobi: [[a,b],c]+cyc=0', test_triple_commutator),
]:
    res = test_identity(name, fn, n_args=3)
    all_results[name] = res
    print(f"\n  {name}:")
    for dim in [8, 16, 32, 64]:
        m, s, mx, mn = res[dim]
        print(f"    dim={dim:3d}: mean={m:.8f}  std={s:.8f}  max={mx:.8f}")

# ============================================================
# 10. THE BIG TABLE
# ============================================================

print("\n\n")
print("=" * 110)
print("  GRAND SUMMARY: BREAKING PATTERNS ACROSS CAYLEY-DICKSON CHAIN")
print("=" * 110)
print(f"  {'Identity':<52} {'8D':>9} {'16D':>9} {'32D':>9} {'64D':>9}  {'32->64':>8}")
print("-" * 110)

for name, res in all_results.items():
    m8  = res[8][0]
    m16 = res[16][0]
    m32 = res[32][0]
    m64 = res[64][0]

    flag = ""
    # Key check: holds at 32D (< 0.01) but breaks at 64D (> 0.05)
    if m32 < 0.01 and m64 > 0.05:
        flag = "***NEW***"
    elif m32 < 0.01 and m64 > 0.01:
        flag = "**MAYBE**"
    elif m32 < 1e-6 and m64 < 1e-6:
        flag = "(exact)"
    elif abs(m64 - m32) > 0.1 and m32 < 0.1:
        flag = "*CHECK*"

    print(f"  {name:<52} {m8:>9.5f} {m16:>9.5f} {m32:>9.5f} {m64:>9.5f}  {flag:>8}")

print("-" * 110)

# Check for any new breakings specifically
print("\n  BREAKING ANALYSIS:")
found_new = False
for name, res in all_results.items():
    m8, m16, m32, m64 = res[8][0], res[16][0], res[32][0], res[64][0]

    # Pattern: exact at some dim, broken at next
    breaks = []
    if m8 < 1e-4 and m16 > 0.01:
        breaks.append("8->16")
    if m16 < 1e-4 and m32 > 0.01:
        breaks.append("16->32")
    if m32 < 1e-4 and m64 > 0.01:
        breaks.append("32->64")

    if breaks:
        print(f"    {name}: breaks at {', '.join(breaks)}")
        if "32->64" in breaks:
            found_new = True
            print(f"      *** POTENTIAL 5th BREAKING TYPE! ***")
            print(f"      32D error: {m32:.2e}")
            print(f"      64D error: {m64:.2e}")

if not found_new:
    print("    No new 32->64 breaking found among these identities.")
    print("    All identities that hold at 32D also hold at 64D.")
    print("    All identities that fail at 32D also fail at 64D (possibly worse).")

print("\n  IDENTITIES THAT HOLD EVERYWHERE (dim 8-64):")
for name, res in all_results.items():
    m8, m16, m32, m64 = res[8][0], res[16][0], res[32][0], res[64][0]
    if max(m8, m16, m32, m64) < 1e-6:
        print(f"    * {name}")

print("\n  KNOWN BREAKING PATTERN CONFIRMATION:")
for name, res in all_results.items():
    m8, m16, m32, m64 = res[8][0], res[16][0], res[32][0], res[64][0]
    transitions = []
    if m8 < 0.01 < m16:
        transitions.append(f"breaks at 16D (octonion->sedenion)")
    if m16 < 0.01 < m32:
        transitions.append(f"breaks at 32D (sedenion->trigintaduonion)")
    if transitions:
        print(f"    * {name}: {'; '.join(transitions)}")

print("\nDone.")
