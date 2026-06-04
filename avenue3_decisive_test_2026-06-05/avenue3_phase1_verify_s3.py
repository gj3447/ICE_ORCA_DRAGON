"""
VERIFY (not assert) the genuine S3 = Aut(S)/Aut(O) in MY CD convention.

GGV (arXiv:2306.13098, eqns 42-55) give generators of the extra S3:
   epsilon (order 2):  e_i -> e_i,  e_{i+8} -> -e_{i+8},  for i=1..7;  e8 -> e8 ; e0->e0
   psi     (order 3):  e_i     -> -1/2 e_i     + (sqrt3/2) e_{i+8}
                       e_{i+8} -> -1/2 e_{i+8}  - (sqrt3/2) e_i        (sign of cross term
                       fixed by the requirement phi(xy)=phi(x)phi(y) -- we SEARCH the sign)
                       e8 -> e8 ; e0 -> e0
The Brown (1967) general form is a 2pi/3 rotation in the seven e_i--e_{i+8} planes.
Crucially the CROSS-TERM SIGN must be chosen so the map is a genuine automorphism in
OUR table; we test all 4 sign combinations and KEEP only the ones that pass phi(xy)=phi(x)phi(y).
"""
import itertools
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
# 16x16 structure constants as sympy matrix-of-(k,sign)
def basis_prod_vec(i, j):
    k, s = table[i][j]
    v = [sp.Integer(0)] * DIM
    v[k] = sp.Integer(s)
    return sp.Matrix(v)

sqrt3 = sp.sqrt(3)
half = sp.Rational(1, 2)

def apply_linear(M, vec):
    """M is 16x16 sympy matrix (columns = images of e_j). vec is length-16 list."""
    return M * sp.Matrix(vec)

def vmul_M(u, v):
    """multiply two coefficient column-vectors u,v (sympy) via the table."""
    res = sp.zeros(DIM, 1)
    for i in range(DIM):
        ui = u[i]
        if ui == 0:
            continue
        for j in range(DIM):
            vj = v[j]
            if vj == 0:
                continue
            k, s = table[i][j]
            res[k] += ui * vj * s
    return res

def is_automorphism(M):
    """Check phi(e_i e_j) = phi(e_i) phi(e_j) for ALL basis i,j. M columns = phi(e_j)."""
    cols = [M[:, j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k, s = table[i][j]
            lhs = s * cols[k]                  # phi(e_i e_j) = s * phi(e_k)
            rhs = vmul_M(cols[i], cols[j])      # phi(e_i) phi(e_j)
            if sp.simplify(lhs - rhs) != sp.zeros(DIM, 1):
                return False
    return True

# ---- build epsilon ----
def build_epsilon():
    M = sp.zeros(DIM, DIM)
    M[0, 0] = 1
    for i in range(1, DIM):
        if i == 8:
            M[8, 8] = 1
        elif 1 <= i <= 7:
            M[i, i] = 1
        elif 9 <= i <= 15:
            M[i, i] = -1   # e_{i+8} for i in 1..7  -> indices 9..15
    return M

# ---- build psi with searchable cross-sign ----
def build_psi(sign_cross):
    """psi(e_i) = -1/2 e_i + sc * (sqrt3/2) e_{i+8};
       psi(e_{i+8}) = -1/2 e_{i+8} - sc*(sqrt3/2) e_i ; e8->e8 ; e0->e0.
       sign_cross = +1 or -1."""
    M = sp.zeros(DIM, DIM)
    M[0, 0] = 1
    M[8, 8] = 1
    sc = sp.Integer(sign_cross)
    for i in range(1, 8):
        j = i + 8  # 9..15
        # column i = image of e_i
        M[i, i] = -half
        M[j, i] = sc * sqrt3 * half
        # column j = image of e_{i+8}
        M[j, j] = -half
        M[i, j] = -sc * sqrt3 * half
    return M

eps = build_epsilon()
print("epsilon is automorphism of S:", is_automorphism(eps))

psi_results = {}
for sc in (+1, -1):
    psi = build_psi(sc)
    ok = is_automorphism(psi)
    psi_results[sc] = (psi, ok)
    print(f"psi (cross-sign {sc:+d}) is automorphism of S: {ok}")

# pick a passing psi
psi = None
for sc in (+1, -1):
    if psi_results[sc][1]:
        psi = psi_results[sc][0]
        chosen_sc = sc
        break
assert psi is not None, "no psi sign gave an automorphism -- table/convention mismatch!"
print(f"  -> using psi with cross-sign {chosen_sc:+d}")

# ---- group relations: eps^2 = I, psi^3 = I, eps psi = psi^2 eps ----
I = sp.eye(DIM)
print("\nGROUP RELATIONS:")
print("  eps^2 = I:", sp.simplify(eps*eps - I) == sp.zeros(DIM, DIM))
psi3 = sp.simplify(psi*psi*psi)
print("  psi^3 = I:", psi3 == I)
print("  psi != I:", sp.simplify(psi - I) != sp.zeros(DIM, DIM))
print("  psi^2 != I:", sp.simplify(psi*psi - I) != sp.zeros(DIM, DIM))
lhs = sp.simplify(eps*psi)
rhs = sp.simplify(psi*psi*eps)
print("  eps*psi = psi^2*eps (dihedral S3 relation):", sp.simplify(lhs - rhs) == sp.zeros(DIM, DIM))

# group order: generate <eps,psi>
def matkey(M):
    return tuple(sp.nsimplify(x) for x in M)
gens = [eps, psi]
elements = {tuple(I): I}
frontier = [I]
while frontier:
    g = frontier.pop()
    for h in gens:
        p = sp.simplify(g*h)
        key = tuple(sp.nsimplify(x) for x in p)
        if key not in elements:
            elements[key] = p
            frontier.append(p)
print(f"  |<eps,psi>| = {len(elements)} (S3 has order 6)")

# ---- permutation of the three octonions ----
O1 = {0,1,4,5,8,9,12,13}
O2 = {0,2,4,6,8,10,12,14}
O3 = {0,3,4,7,8,11,12,15}
octs = {'O1': O1, 'O2': O2, 'O3': O3}

def image_subspace_indices(M, idxset):
    """Return the set of basis indices that the images of {e_i: i in idxset} span,
    IF the image is itself a coordinate subspace (a permutation-with-signs of a coord subspace).
    Otherwise return None."""
    spanned = set()
    pure = True
    for i in sorted(idxset):
        col = M[:, i]
        nz = [r for r in range(DIM) if col[r] != 0]
        spanned.update(nz)
    return spanned

print("\nOCTONION PERMUTATION under epsilon and psi:")
for name, M in [('epsilon', eps), ('psi', psi)]:
    print(f"  {name}:")
    for on, oset in octs.items():
        img = image_subspace_indices(M, oset)
        # which octonion does the image equal?
        match = [n2 for n2, s2 in octs.items() if img == s2]
        print(f"    {on}={sorted(oset)} -> spans {sorted(img)}  == {match if match else 'NOT a single octonion'}")

# ---- NOT an automorphism of the reference octonion O={e1..e7} ----
refO = set(range(0,8))
print("\nNOT-Aut(O) CHECK (reference octonion e0..e7):")
for name, M in [('epsilon', eps), ('psi', psi)]:
    img = image_subspace_indices(M, refO)
    stays = img.issubset(refO)
    print(f"  {name}: image of e0..e7 spans {sorted(img)} ; stays inside e0..e7? {stays}")
