"""
Independent verification of the genuine S3 = Aut(S)\Aut(O).
Build psi (order 3) and eps (order 2) AS LINEAR MAPS from scratch, then VERIFY
phi(e_i e_j) = phi(e_i) phi(e_j) on ALL 256 basis products with EXACT sympy.
Then independently re-run the S3-character / irrep-multiplicity computation.

NO trust in Phase 1/2 matrices: I construct psi, eps from the geometric description
and check they are automorphisms purely from my own multiplication table.
"""
import sympy as sp
from sympy import Rational, sqrt, simplify, Matrix, eye, trace
from naesengmoon_indep_sedenion import IDX, SIGN, DIM

s3 = sqrt(3)
half = Rational(1, 2)

# ---- build psi: 2pi/3 rotation in each e_i--e_{i+8} plane (i=1..7), e0,e8 special ----
# psi(e_i)   = -1/2 e_i + (sqrt3/2) e_{i+8}
# psi(e_{i+8})= -(sqrt3/2) e_i - 1/2 e_{i+8}
# psi(e0)=e0, psi(e8)=e8
PSI = sp.zeros(DIM, DIM)
PSI[0, 0] = 1
PSI[8, 8] = 1
for i in range(1, 8):
    j = i + 8
    # column i = image of e_i  (PSI[:,i] = psi(e_i))
    PSI[i, i] = -half
    PSI[j, i] = s3 * half
    # column j = image of e_{i+8}
    PSI[i, j] = -s3 * half
    PSI[j, j] = -half

# ---- build eps: per-plane diag(1,-1), e8 sign -1, e0 fixed ----
# eps(e_i)=e_i (i=1..7), eps(e_{i+8})=-e_{i+8}, eps(e8)=-e8, eps(e0)=e0
EPS = sp.zeros(DIM, DIM)
EPS[0, 0] = 1
EPS[8, 8] = -1
for i in range(1, 8):
    EPS[i, i] = 1
    EPS[i + 8, i + 8] = -1

def apply_map(M, vec_index):
    """image of basis e_k under linear map M = column k of M, as a sympy column vector."""
    return M[:, vec_index]

def basis_vec(k):
    v = sp.zeros(DIM, 1)
    v[k] = 1
    return v

def algebra_mul_vec(u, v):
    """multiply two sympy column vectors using the structure table (bilinear)."""
    out = sp.zeros(DIM, 1)
    for i in range(DIM):
        if u[i] == 0:
            continue
        for j in range(DIM):
            if v[j] == 0:
                continue
            k = IDX[i][j]
            out[k] += u[i] * v[j] * SIGN[i][j]
    return out

def is_automorphism(M, name):
    """check phi(e_i e_j) = phi(e_i) phi(e_j) for all 256 pairs."""
    bad = 0
    for i in range(DIM):
        for j in range(DIM):
            k = IDX[i][j]
            s = SIGN[i][j]
            lhs = s * apply_map(M, k)           # phi(e_i e_j) = s * phi(e_k)
            rhs = algebra_mul_vec(apply_map(M, i), apply_map(M, j))  # phi(e_i)*phi(e_j)
            if simplify(lhs - rhs) != sp.zeros(DIM, 1):
                bad += 1
    print(f"  {name}: automorphism check over 256 products -> {'PASS' if bad==0 else f'FAIL ({bad} bad)'}")
    return bad == 0

print("=== INDEPENDENT S3 AUTOMORPHISM VERIFICATION ===")
psi_ok = is_automorphism(PSI, "psi (order-3 rotation)")
eps_ok = is_automorphism(EPS, "eps (order-2 reflection)")

# group relations
I16 = eye(DIM)
psi3 = simplify(PSI**3)
eps2 = simplify(EPS**2)
rel = simplify(EPS * PSI * EPS - PSI**2)  # eps psi eps = psi^-1 = psi^2
print(f"  psi^3 = I : {psi3 == I16}")
print(f"  eps^2 = I : {eps2 == I16}")
print(f"  eps psi eps = psi^2 (dihedral S3 relation) : {rel == sp.zeros(DIM,DIM)}")

# does psi move e0..e7 OUT of the reference octonion? (the Aut(S)\Aut(O) test)
moved = []
for i in range(1, 8):
    img = apply_map(PSI, i)
    # is the image supported only on indices 0..7?
    support_out = any(img[k] != 0 for k in range(8, DIM))
    if support_out:
        moved.append(i)
print(f"  psi moves these reference-octonion units OUT of e0..e7: {moved}")
print(f"  => psi is OUTER (NOT in Aut(O)=G2): {len(moved) > 0}")

# group order
elements = set()
def mat_key(M):
    return tuple(simplify(M).reshape(1, DIM*DIM))
gens = [I16, PSI, EPS]
frontier = [I16]
seen = {mat_key(I16)}
prod_list = [I16]
changed = True
group = [I16]
# BFS closure
queue = [I16]
keys = {mat_key(I16)}
while queue:
    g = queue.pop()
    for h in (PSI, EPS):
        gh = simplify(g * h)
        k = mat_key(gh)
        if k not in keys:
            keys.add(k)
            group.append(gh)
            queue.append(gh)
print(f"  |<psi,eps>| = {len(group)}  (expect 6 = S3)")

# ================= CHARACTER / IRREP DECOMPOSITION =================
# S3 char table. Classes: e (size1), rot=3-cycles (size2), ref=transpositions (size3)
# irreps: triv (1,1,1), sign (1,1,-1), std (2,-1,0)
CHAR = {'triv': {'e':1,'rot':1,'ref':-1*0+1},  # fix below
        }
CHAR = {
    'triv': {'e': 1, 'rot': 1, 'ref': 1},
    'sign': {'e': 1, 'rot': 1, 'ref': -1},
    'std':  {'e': 2, 'rot': -1, 'ref': 0},
}
CLASS_SIZE = {'e': 1, 'rot': 2, 'ref': 3}

def char_of_subrep(cols):
    """cols: list of sympy column vectors spanning an S3-invariant subspace.
    Returns character dict on {e,rot,ref} or None per class if not invariant."""
    B = Matrix.hstack(*cols)
    # reduce to independent columns
    rref, piv = B.rref()
    Bind = B[:, list(piv)]
    rk = Bind.rank()
    G = (Bind.T * Bind)
    Ginv = G.inv()
    chi = {}
    for cl, g in {'e': I16, 'rot': PSI, 'ref': EPS}.items():
        gB = simplify(g * Bind)
        # invariance: columns of gB must lie in span(Bind)
        if Matrix.hstack(Bind, gB).rank() != rk:
            chi[cl] = None
            continue
        R = simplify(Ginv * Bind.T * g * Bind)
        chi[cl] = simplify(trace(R))
    return chi

def decompose(chi):
    out = {}
    for irr in CHAR:
        s = sum(CLASS_SIZE[c] * chi[c] * CHAR[irr][c] for c in ('e', 'rot', 'ref'))
        out[irr] = simplify(Rational(s, 6))
    return out

print("\n=== INDEPENDENT CHARACTER DECOMPOSITION ===")

# (A) full 16-dim sedenion module: character = trace of each group elt
chiS = {'e': trace(I16), 'rot': trace(PSI), 'ref': trace(EPS)}
print(f"  S (16-dim): char {chiS} -> {decompose(chiS)}")

# (B) Im(S) = e1..e15 (drop e0). Project out e0.
cols_imS = [basis_vec(k) for k in range(1, DIM)]
chi_imS = char_of_subrep(cols_imS)
print(f"  Im(S) (15-dim): char {chi_imS} -> {decompose(chi_imS)}")

# (C) span(e8)
chi_e8 = char_of_subrep([basis_vec(8)])
print(f"  span(e8): char {chi_e8} -> {decompose(chi_e8)}")

# (D) H = span(e0,e4,e8,e12)
chi_H = char_of_subrep([basis_vec(k) for k in (0, 4, 8, 12)])
print(f"  H=span(e0,e4,e8,e12): char {chi_H} -> {decompose(chi_H)}")

# (E) 14-dim seven doubling planes e1..e7,e9..e15
cols14 = [basis_vec(k) for k in list(range(1, 8)) + list(range(9, 16))]
chi14 = char_of_subrep(cols14)
print(f"  14-dim seven-planes: char {chi14} -> {decompose(chi14)}")

# (F) each GGV octonion O1,O2,O3 (8-dim each)
O1 = (0, 1, 4, 5, 8, 9, 12, 13)
O2 = (0, 2, 4, 6, 8, 10, 12, 14)
O3 = (0, 3, 4, 7, 8, 11, 12, 15)
for name, Oset in [('O1', O1), ('O2', O2), ('O3', O3)]:
    chiO = char_of_subrep([basis_vec(k) for k in Oset])
    print(f"  {name} (8-dim): char {chiO} -> {decompose(chiO)}")

# (G) psi-orbit module of a single ladder seed e1
seed = basis_vec(1)
orbit = [seed, simplify(PSI * seed), simplify(PSI * PSI * seed)]
chi_orb = char_of_subrep(orbit)
B_orb = Matrix.hstack(*orbit)
print(f"  psi-orbit of e1: {len(orbit)} vectors, rank={B_orb.rank()}, char {chi_orb} -> {decompose(chi_orb)}")

# Does S3 STABILIZE each O_i setwise, or PERMUTE them?
def maps_set_to(M, Oset):
    """which index-set does basis O_set map onto (as spans)? Return 'stabilize'/'other'."""
    img_support = set()
    for k in Oset:
        col = apply_map(M, k)
        for r in range(DIM):
            if col[r] != 0:
                img_support.add(r)
    return img_support

print("\n=== O_i STABILIZE vs PERMUTE under genuine S3 ===")
Osets = {'O1': set(O1), 'O2': set(O2), 'O3': set(O3)}
for gname, M in [('psi', PSI), ('eps', EPS)]:
    for Oname, Oset in Osets.items():
        sup = maps_set_to(M, Oset)
        # which O_j (if any) does the image-support fit inside?
        fit = [oj for oj, os in Osets.items() if sup <= os]
        print(f"  {gname}({Oname}) support index-set fits inside: {fit if fit else 'NONE (escapes all O_j)'}")
