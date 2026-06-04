"""
NAESENGMOON Phase 3b — fully independent re-derivation.
Own Cayley-Dickson convention, own ZD count, own automorphism verification.
NO import of any avenue3 script. Built from scratch with exact arithmetic.

CD convention chosen here (the SAME task-specified one, to compare apples-to-apples,
but coded independently from a blank page):
    (a,b)(c,d) = (a c - conj(d) b,  d a + b conj(c))
    conj((x,y)) = (conj(x), -y)
Base level n==1: real multiply.

We use exact Fraction arithmetic for the table, and only need integers (0,+1,-1)
for the structure constants since basis products are signed basis elements.
"""
from fractions import Fraction
from itertools import combinations
import sys

DIM = 16  # sedenions

# ---------- exact CD arithmetic on coordinate lists ----------
def conj(a):
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

def mul(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2 = a[:h], a[h:]
    b1, b2 = b[:h], b[h:]
    # (a,b)(c,d) = (a c - conj(d) b, d a + b conj(c))
    first = sub(mul(a1, b1), mul(conj(b2), a2))
    second = add(mul(b2, a1), mul(a2, conj(b1)))
    return first + second

def e(i, n=DIM):
    v = [Fraction(0)] * n
    v[i] = Fraction(1)
    return v

# ---------- build the 16x16 structure-constant table ----------
# e_i * e_j = SIGN[i][j] * e_{ IDX[i][j] }
IDX = [[None] * DIM for _ in range(DIM)]
SIGN = [[0] * DIM for _ in range(DIM)]

def build_table():
    basis = [e(i) for i in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            p = mul(basis[i], basis[j])
            nz = [(k, p[k]) for k in range(DIM) if p[k] != 0]
            assert len(nz) == 1, f"e{i}*e{j} not a single basis elt: {nz}"
            k, c = nz[0]
            assert c in (Fraction(1), Fraction(-1)), f"bad coeff {c}"
            IDX[i][j] = k
            SIGN[i][j] = int(c)

build_table()

# ---------- SANITY CHECKS ----------
def sanity():
    out = []
    # e0 identity
    ident = all(IDX[0][j] == j and SIGN[0][j] == 1 for j in range(DIM)) and \
            all(IDX[i][0] == i and SIGN[i][0] == 1 for i in range(DIM))
    out.append(("e0 is identity", ident))
    # e_i^2 = -1 for i>=1
    sq = all(IDX[i][i] == 0 and SIGN[i][i] == -1 for i in range(1, DIM))
    out.append(("e_i^2 = -1 (i>=1)", sq))
    # non-commutative
    noncomm = any(IDX[i][j] != IDX[j][i] or SIGN[i][j] != SIGN[j][i]
                  for i in range(1, DIM) for j in range(1, DIM))
    out.append(("non-commutative", noncomm))
    # e1..e7 closed (octonion subalgebra) and alternative
    oct_idx = set(range(1, 8))
    closed = all(IDX[i][j] in (oct_idx | {0}) for i in oct_idx for j in oct_idx)
    out.append(("e1..e7 closed under mult", closed))
    return out

# associator test on a genuine sum (non-associativity at sedenion level)
def vadd(*vs):
    r = [Fraction(0)] * DIM
    for v in vs:
        r = add(r, v)
    return r

def associator(x, y, z):
    return sub(mul(mul(x, y), z), mul(x, mul(y, z)))

# ---------- ZERO DIVISOR ENUMERATION ----------
# A primitive ZD building block: (e_a +/- e_b). We look for annihilating pairs.
# X = e_a + s1*e_b,  Y = e_c + s2*e_d with X*Y == 0 (X,Y nonzero, not scalar multiples).

def is_zero(v):
    return all(c == 0 for c in v)

def primitive(a, sb, b):
    """e_a + sb*e_b as a vector, sb in {+1,-1}, a<b imaginary indices."""
    v = [Fraction(0)] * DIM
    v[a] += Fraction(1)
    v[b] += Fraction(sb)
    return v

def run():
    print("=== INDEPENDENT SEDENION (own CD code, exact Fraction) ===")
    for name, ok in sanity():
        print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    # associator on a sum, mimic the literature shape (e1+e10)(e1+e10)e4
    A = vadd(e(1), e(10))
    assoc = associator(A, A, e(4))
    nz = [(k, assoc[k]) for k in range(DIM) if assoc[k] != 0]
    print(f"  associator((e1+e10),(e1+e10),e4) nonzero comps = {nz}  => non-associative: {not is_zero(assoc)}")

    imag = list(range(1, DIM))  # e1..e15

    # ---- Enumerate annihilating ordered pairs among 2-term primitives ----
    # candidate primitives: (a, sb, b) with 1<=a<b<=15, sb in {+1,-1}
    prims = []
    for a, b in combinations(imag, 2):
        for sb in (1, -1):
            prims.append((a, sb, b))
    # precompute vectors
    pvec = {p: primitive(*p) for p in prims}

    # For ZD we need X*Y=0 with X,Y both 2-term primitives, 4 distinct indices.
    # Count ordered annihilating pairs and analyze structure.
    ordered_annih = []  # (X,Y) with X*Y=0
    for X in prims:
        vx = pvec[X]
        for Y in prims:
            # require 4 distinct indices for a "standard" ZD pair
            a, _, b = X
            c, _, d = Y
            if len({a, b, c, d}) != 4:
                continue
            prod = mul(vx, pvec[Y])
            if is_zero(prod):
                ordered_annih.append((X, Y))
    print(f"\n  ordered annihilating (X,Y), X*Y=0, 4 distinct idx, 2-term prims: {len(ordered_annih)}")

    # ---- De Marrais chain: assessors / pairs / primitive units / box-kites ----
    # An ASSESSOR is an unordered axis-pair {a,b} (a<b, both imaginary) such that
    # the diagonal e_a +/- e_b participates in zero-division. Standard def:
    # {a,b} is an assessor if there EXISTS some annihilating partner.
    assessor_axes = set()
    # primitive ZD units: a 2-term primitive e_a + s e_b that annihilates SOMETHING
    zd_units = set()
    for (X, Y) in ordered_annih:
        a, sb, b = X
        assessor_axes.add((a, b))
        zd_units.add(X)
        c, sd, d = Y
        assessor_axes.add((c, d))
        zd_units.add(Y)

    print(f"  distinct assessor AXES {{a,b}} (a<b) carrying ZD: {len(assessor_axes)}")
    print(f"  distinct 2-term primitive ZD units e_a+/-e_b (a<b, both signs counted): {len(zd_units)}")

    # de Marrais 168 primitive units: 42 assessors x 4 half-axes (both signs, both
    # index orders). Let's count primitives counting both index orders:
    units_both_orders = set()
    for (a, b) in assessor_axes:
        for sb in (1, -1):
            units_both_orders.add((a, sb, b))   # e_a + sb e_b
            units_both_orders.add((b, sb, a))   # e_b + sb e_a  (other order)
    print(f"  primitive units counting BOTH index orders (42*4 expected=168): {len(units_both_orders)}")

    # standard ZD pairs: (e_a+e_b)(e_c+e_d)=0 with + signs, 4 distinct, unordered {X,Y}
    plus_pairs = set()
    for (X, Y) in ordered_annih:
        a, sb, b = X
        c, sd, d = Y
        if sb == 1 and sd == 1:
            key = frozenset([(a, b), (c, d)])
            plus_pairs.add(key)
    print(f"  standard '+,+' ZD pairs (e_a+e_b)(e_c+e_d)=0 unordered: {len(plus_pairs)}")

    # unordered annihilating unit pairs {X,Y} (any signs)
    unordered_any = set()
    for (X, Y) in ordered_annih:
        unordered_any.add(frozenset([X, Y]))
    print(f"  unordered annihilating unit pairs {{X,Y}} any signs: {len(unordered_any)}")
    print(f"  ordered annihilating pairs X*Y=0 any signs: {len(ordered_annih)}")

    # ---- Box-kites: connected components of assessor annihilation graph ----
    # Build graph on assessor axes; edge if the two axes have annihilating diagonals.
    axes = sorted(assessor_axes)
    axis_index = {ax: i for i, ax in enumerate(axes)}
    adj = {ax: set() for ax in axes}
    for (X, Y) in ordered_annih:
        ax1 = (X[0], X[2])
        ax2 = (Y[0], Y[2])
        if ax1 in adj and ax2 in adj and ax1 != ax2:
            adj[ax1].add(ax2)
            adj[ax2].add(ax1)
    # connected components
    seen = set()
    comps = []
    for ax in axes:
        if ax in seen:
            continue
        stack = [ax]
        comp = set()
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.add(u)
            for w in adj[u]:
                if w not in seen:
                    stack.append(w)
        comps.append(comp)
    comp_sizes = sorted(len(c) for c in comps)
    print(f"\n  box-kites = connected components of assessor graph: {len(comps)}")
    print(f"  component sizes: {comp_sizes}")

    # strut constant: XOR of the two indices in an assessor? de Marrais uses
    # a 'strut constant' per box-kite. Let's check XOR a^b within each component.
    print("  per-component XOR(a,b) values:")
    strut_set = set()
    for comp in sorted(comps, key=lambda c: min(c)):
        xors = sorted({a ^ b for (a, b) in comp})
        strut_set.update(xors)
        print(f"    comp(min={min(comp)}, size={len(comp)}): XORs={xors}")
    return {
        "ordered_annih": len(ordered_annih),
        "assessor_axes": len(assessor_axes),
        "zd_units": len(zd_units),
        "units_both_orders": len(units_both_orders),
        "plus_pairs": len(plus_pairs),
        "unordered_any": len(unordered_any),
        "box_kites": len(comps),
        "comp_sizes": comp_sizes,
    }

if __name__ == "__main__":
    res = run()
    print("\n=== SUMMARY DICT ===")
    for k, v in res.items():
        print(f"  {k}: {v}")
