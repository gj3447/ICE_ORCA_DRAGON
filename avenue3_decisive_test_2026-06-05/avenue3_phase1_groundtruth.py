"""
Avenue-3 Phase 1 — Ground truth for sedenion zero-divisor structure + Aut(S)=G2 x S3.

Built from scratch, independent of existing ICE code. Uses EXACT-ARITHMETIC (sympy Rational
+ integers) so that "product == 0" is decided with NO floating-point tolerance.

CD convention (FIXED, used consistently everywhere below):
    (a, b)(c, d) = (a c - conj(d) b,  d a + b conj(c))
This is the task-specified convention. Basis e0..e15. e1..e7 span an octonion subalgebra.

Everything is COMPUTED and printed. No asserted literature numbers are used as inputs;
they are only compared against at the end.
"""
import itertools
from fractions import Fraction as F

# ----------------------------------------------------------------------
# 1. Cayley-Dickson multiplication with exact rational arithmetic
# ----------------------------------------------------------------------
def conj(a):
    """CD conjugate. Real (len 1): identity. Else (x,y)->(conj(x),-y)."""
    n = len(a)
    if n == 1:
        return [a[0]]
    h = n // 2
    x, y = a[:h], a[h:]
    return conj(x) + [-v for v in y]

def add(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def smul(s, a):
    return [s * v for v in a]

def mul(a, b):
    """CD product, convention (a,b)(c,d) = (a c - conj(d) b, d a + b conj(c))."""
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2 = a[:h], a[h:]
    b1, b2 = b[:h], b[h:]
    # first  = a1*b1 - conj(b2)*a2
    first = sub(mul(a1, b1), mul(conj(b2), a2))
    # second = b2*a1 + a2*conj(b1)
    second = add(mul(b2, a1), mul(a2, conj(b1)))
    return first + second

DIM = 16
def e(i, dim=DIM):
    v = [F(0)] * dim
    v[i] = F(1)
    return v

def is_zero(a):
    return all(v == 0 for v in a)

# ----------------------------------------------------------------------
# 2. Build the 16x16 sign/index table:  e_i * e_j = sign * e_k
# ----------------------------------------------------------------------
def build_table(dim=DIM):
    """Returns table[i][j] = (k, sign)."""
    table = [[None] * dim for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            p = mul(e(i, dim), e(j, dim))
            nz = [(idx, val) for idx, val in enumerate(p) if val != 0]
            assert len(nz) == 1, f"e{i}*e{j} not a single basis element: {nz}"
            k, val = nz[0]
            assert val in (F(1), F(-1)), f"unexpected coeff {val}"
            table[i][j] = (k, int(val))
    return table

# ----------------------------------------------------------------------
# 3. Basic algebra sanity checks
# ----------------------------------------------------------------------
def basic_checks(table, dim=DIM):
    out = {}
    # e0 identity
    out['e0_identity'] = all(table[0][j] == (j, 1) and table[j][0] == (j, 1) for j in range(dim))
    # e_i^2 = -1 for i>=1, e0^2=+e0
    out['ei_sq_minus1'] = all(table[i][i] == (0, -1) for i in range(1, dim))
    # non-commutative: exists i,j with e_i e_j != e_j e_i
    noncomm = any(table[i][j] != table[j][i] for i in range(dim) for j in range(dim))
    out['noncommutative'] = noncomm
    # non-associative: exists i,j,k with (e_i e_j) e_k != e_i (e_j e_k)
    def prod3_left(i, j, k):
        k1, s1 = table[i][j]
        k2, s2 = table[k1][k]
        return (k2, s1 * s2)
    def prod3_right(i, j, k):
        k1, s1 = table[j][k]
        k2, s2 = table[i][k1]
        return (k2, s1 * s2)
    nonassoc = any(prod3_left(i, j, k) != prod3_right(i, j, k)
                   for i in range(dim) for j in range(dim) for k in range(dim))
    out['nonassociative'] = nonassoc
    # non-alternative at sedenion level. The BASIS-only test (e_i,e_i,e_j) is degenerate
    # because e_i^2 = -e0 (scalar) always associates. The genuine test uses a SUM x=e_a+e_b
    # and checks the left-alternative law (x,x,y) = (xx)y - x(xy) != 0.
    def assoc_eq(i, j, k):
        return prod3_left(i, j, k) == prod3_right(i, j, k)
    def vmul_local(u, v):
        res = [F(0)] * dim
        for a in range(dim):
            if u[a] == 0: continue
            for b in range(dim):
                if v[b] == 0: continue
                kk, sg = table[a][b]
                res[kk] += u[a] * v[b] * sg
        return res
    nonalt = False
    for a in range(1, dim):
        for b in range(a + 1, dim):
            x = [F(0)] * dim; x[a] = F(1); x[b] = F(1)
            for c in range(1, dim):
                y = [F(0)] * dim; y[c] = F(1)
                if vmul_local(vmul_local(x, x), y) != vmul_local(x, vmul_local(x, y)):
                    nonalt = True; break
            if nonalt: break
        if nonalt: break
    out['nonalternative'] = nonalt
    # The octonion subalgebra e0..e7 IS alternative: same sum-based test inside 1..7 NEVER fails.
    oct_alt = True
    for a in range(1, 8):
        for b in range(a + 1, 8):
            x = [F(0)] * dim; x[a] = F(1); x[b] = F(1)
            for c in range(1, 8):
                y = [F(0)] * dim; y[c] = F(1)
                if vmul_local(vmul_local(x, x), y) != vmul_local(x, vmul_local(x, y)):
                    oct_alt = False; break
            if not oct_alt: break
        if not oct_alt: break
    out['octonion_subalg_alternative'] = oct_alt
    return out

# ----------------------------------------------------------------------
# 4. Enumerate zero divisors of the form (e_i +/- e_j)
# ----------------------------------------------------------------------
def find_zero_divisors(table, dim=DIM):
    """
    Find primitive zero divisors: products (e_a + s*e_b)(e_c + t*e_d) = 0
    with a<b, c<d, s,t in {+1,-1}, indices in 1..15 (imaginary units only).
    Returns structures for counting per de Marrais / Cawagas terminology.
    """
    def vmul(u, v):
        # u,v are length-dim coefficient lists; multiply using table (linear extension)
        res = [F(0)] * dim
        for i in range(dim):
            if u[i] == 0:
                continue
            for j in range(dim):
                if v[j] == 0:
                    continue
                k, sgn = table[i][j]
                res[k] += u[i] * v[j] * sgn
        return res

    imag = list(range(1, dim))  # e1..e15

    # All "primitive" elements e_a + s e_b (a<b in 1..15, s = +/-1)
    prim_elements = []
    for a, b in itertools.combinations(imag, 2):
        for s in (1, -1):
            vec = [F(0)] * dim
            vec[a] = F(1)
            vec[b] = F(s)
            prim_elements.append(((a, b, s), vec))

    # An ORDERED zero divisor: (X)(Y) = 0 with X = e_a+s e_b, Y = e_c+t e_d, X,Y != 0.
    # Count distinct ordered annihilating pairs and distinct elements that participate.
    ordered_pairs = []
    for (lab1, X) in prim_elements:
        for (lab2, Y) in prim_elements:
            if vmul(X, Y) == [F(0)] * dim:
                ordered_pairs.append((lab1, lab2))

    # "168 primitive unit zero divisors": de Marrais counts the number of distinct
    # primitive elements D = e_a +/- e_b that are zero divisors (i.e. there EXISTS a
    # nonzero Y of the same primitive form with D*Y = 0).
    zd_elements = set()
    for (lab1, lab2) in ordered_pairs:
        zd_elements.add(lab1)
    n_primitive_units = len(zd_elements)

    # Standard ZD pairs (unordered {X, Y}), counting an annihilating relationship.
    # de Marrais: 84 pairs.  We collect unordered {lab1,lab2} where X*Y=0.
    # NOTE: zero-divisor annihilation is generally one-sided & direction matters,
    # so we also report the ordered count and the symmetric-pair count separately.
    unordered_pairs = set()
    for (lab1, lab2) in ordered_pairs:
        unordered_pairs.add(frozenset((lab1, lab2)) if lab1 != lab2 else None)
    unordered_pairs.discard(None)

    return {
        'n_prim_elements_total': len(prim_elements),
        'ordered_annihilating_pairs': ordered_pairs,
        'n_ordered_pairs': len(ordered_pairs),
        'n_primitive_unit_zds': n_primitive_units,
        'zd_elements': zd_elements,
        'n_unordered_pairs': len(unordered_pairs),
        'unordered_pairs': unordered_pairs,
    }

# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 1 GROUND TRUTH — sedenion ZD structure + Aut(S)")
    print("CD convention: (a,b)(c,d) = (ac - conj(d)b, da + b conj(c))")
    print("=" * 70)

    table = build_table()
    print("\n[1] 16x16 multiplication table built (exact arithmetic).")

    bc = basic_checks(table)
    print("\n[1b] Basic algebra checks:")
    for k, v in bc.items():
        print(f"      {k:35s} = {v}")

    print("\n[2] Enumerating zero divisors of primitive form (e_a +/- e_b)...")
    zd = find_zero_divisors(table)
    print(f"      total primitive elements e_a+/-e_b (a<b in 1..15): {zd['n_prim_elements_total']}")
    print(f"      ordered annihilating pairs (X*Y=0):                {zd['n_ordered_pairs']}")
    print(f"      distinct primitive-unit zero divisors:             {zd['n_primitive_unit_zds']}")
    print(f"      unordered annihilating pairs {{X,Y}}:                {zd['n_unordered_pairs']}")
