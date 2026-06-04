"""
Find the GENUINE order-2 automorphism (and clarify what S3 permutes).

Two distinct things in GGV:
  (A) The Brown-form S3 = <eps, psi> acting via the 2pi/3 rotation in e_i--e_{i+8}
      planes (psi) and an involution (eps). This S3 STABILIZES each O_i (rotates
      within them). It is the Aut(S)/Aut(O) factor and provides the "threefold
      multiplicity" -> 3 generations by acting on the LADDER OPERATORS A_i.
  (B) A *different* automorphism that permutes the index-triples (1,2,3)->(2,3,1)
      etc., which permutes O1<->O2<->O3 as SETS (a "color/family" relabeling).

We (1) find the genuine order-2 automorphism in OUR table to complete S3 with psi,
(2) test whether a signed permutation realizing O1->O2->O3->O1 is also an automorphism,
and report BOTH honestly.
"""
import itertools
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
half = sp.Rational(1, 2)
sqrt3 = sp.sqrt(3)

def vmul_M(u, v):
    res = sp.zeros(DIM, 1)
    for i in range(DIM):
        if u[i] == 0: continue
        for j in range(DIM):
            if v[j] == 0: continue
            k, s = table[i][j]
            res[k] += u[i] * v[j] * s
    return res

def is_automorphism(M):
    cols = [M[:, j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k, s = table[i][j]
            lhs = s * cols[k]
            rhs = vmul_M(cols[i], cols[j])
            if sp.simplify(lhs - rhs) != sp.zeros(DIM, 1):
                return False
    return True

def build_psi(sc=1):
    M = sp.zeros(DIM, DIM); M[0,0]=1; M[8,8]=1
    for i in range(1,8):
        j=i+8
        M[i,i]=-half; M[j,i]=sc*sqrt3*half
        M[j,j]=-half; M[i,j]=-sc*sqrt3*half
    return M
psi = build_psi(1)

# (1) Find genuine order-2 automorphism among SIGNED maps fixing e0 and the
#     {O_i} structure. Candidates: sign-flip patterns on subsets of imaginary units.
#     We try: flip e_{i+8} for i=1..7 plus optionally flip e8, and combos. Also try
#     "conjugation in O" forms. We search a modest family and report which are Aut(S).
def signflip(indices):
    M = sp.eye(DIM)
    for i in indices:
        M[i,i] = -1
    return M

print("Searching order-2 signed-diagonal automorphisms (fixing e0)...")
found_eps = []
# try flipping the doubled block {8..15}, {9..15}, {8}, and individual reflections that
# correspond to conjugation by a unit. Conjugation x->u x u^{-1} for unit u is an
# inner automorphism. Test inner automorphisms by e1..e15.
def inner_by(u_idx):
    """phi(x) = e_u * x * e_u^{-1}; e_u^{-1} = -e_u for imaginary unit. Build matrix."""
    M = sp.zeros(DIM, DIM)
    for j in range(DIM):
        ej = sp.zeros(DIM,1); ej[j]=1
        # e_u * e_j
        k1,s1 = table[u_idx][j]
        tmp = sp.zeros(DIM,1); tmp[k1]=s1
        # (e_u e_j) * e_u^{-1}, e_u^{-1} = -e_u (since e_u^2=-1)
        k2,s2 = table[k1][u_idx]
        val = sp.zeros(DIM,1); val[k2] = s1*s2*(-1)
        M[:,j] = val
    return M

inner_auts = []
for u in range(1,DIM):
    M = inner_by(u)
    if is_automorphism(M):
        # order?
        o = 1; P = M
        while sp.simplify(P - sp.eye(DIM)) != sp.zeros(DIM,DIM) and o < 8:
            P = sp.simplify(P*M); o += 1
        inner_auts.append((u,o))
print(f"  inner automorphisms x->e_u x e_u^(-1) that are Aut(S): "
      f"{len(inner_auts)} of 15 (orders: {sorted(set(o for _,o in inner_auts))})")

# Among inner auts of order 2, find one that together with psi generates S3.
order2 = [u for u,o in inner_auts if o==2]
print(f"  order-2 inner auts: e_u for u in {order2}")

I = sp.eye(DIM)
def group_order(gens):
    elements = {tuple(sp.nsimplify(x) for x in I): I}
    frontier=[I]
    while frontier:
        g=frontier.pop()
        for h in gens:
            p=sp.simplify(g*h)
            key=tuple(sp.nsimplify(x) for x in p)
            if key not in elements:
                elements[key]=p; frontier.append(p)
        if len(elements) > 100: break
    return len(elements)

# Try eps = inner_by(8) (conjugation by e8) — natural candidate for a+be8 -> a - be8 analog
for cand in [8] + order2[:4]:
    eps = inner_by(cand)
    if not is_automorphism(eps):
        continue
    # check eps psi eps^-1 = psi^-1 (dihedral)
    relation = sp.simplify(eps*psi*eps - psi*psi)  # eps psi eps = psi^2 (since eps^2=1)
    is_dih = relation == sp.zeros(DIM,DIM)
    go = group_order([eps,psi])
    print(f"  eps=inner_by(e{cand}): Aut={True}, eps^2=I:{sp.simplify(eps*eps-I)==sp.zeros(DIM,DIM)}, "
          f"dihedral(eps psi eps = psi^2):{is_dih}, |<eps,psi>|={go}")

# (2) Does a signed permutation realizing O1->O2->O3 (index family rotation) exist as Aut(S)?
# Family rotation on the "color" triple: 1->2->3->1, 5->6->7->5, 9->10->11->9, 13->14->15->13,
# fixing 4,8,12 and e0. Build the permutation (no signs first), then search signs.
print("\nFamily-rotation automorphism search (O1->O2->O3 as sets)...")
# base permutation pi on indices:
perm = {0:0,4:4,8:8,12:12}
for (a,b,c) in [(1,2,3),(5,6,7),(9,10,11),(13,14,15)]:
    perm[a]=b; perm[b]=c; perm[c]=a
# This maps O1={1,4,5,8,9,12,13}-> {2,4,6,8,10,12,14}=O2 etc. check:
imgO1 = set(perm[i] for i in [0,1,4,5,8,9,12,13])
print(f"  base perm sends O1 -> {sorted(imgO1)} (O2={sorted({0,2,4,6,8,10,12,14})})")

def perm_matrix_with_signs(perm, signs):
    M = sp.zeros(DIM,DIM)
    for j in range(DIM):
        M[perm[j], j] = signs.get(j,1)
    return M

# brute force signs over the 12 moved indices is 2^12=4096; test for automorphism.
moved = [i for i in range(DIM) if perm[i]!=i]
found_family = None
import itertools as it
count_checked=0
for bits in it.product((1,-1), repeat=len(moved)):
    signs = {moved[k]:bits[k] for k in range(len(moved))}
    M = perm_matrix_with_signs(perm, signs)
    count_checked+=1
    if is_automorphism(M):
        found_family = (signs, M)
        break
print(f"  checked {count_checked} signings; family-rotation automorphism found: {found_family is not None}")
if found_family:
    signs, M = found_family
    o=1; P=M
    while sp.simplify(P-I)!=sp.zeros(DIM,DIM) and o<8:
        P=sp.simplify(P*M); o+=1
    print(f"    order = {o}; signs on moved indices = {signs}")
    # confirm it permutes the three octonions
    for on,oset in [('O1',{0,1,4,5,8,9,12,13}),('O2',{0,2,4,6,8,10,12,14}),('O3',{0,3,4,7,8,11,12,15})]:
        img=set()
        for i in sorted(oset):
            col=M[:,i]
            img.update(r for r in range(DIM) if col[r]!=0)
        print(f"    {on} -> spans {sorted(img)}")
