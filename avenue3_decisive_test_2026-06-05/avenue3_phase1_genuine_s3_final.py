"""
FINAL: distinguish the GENUINE Aut(S)\\Aut(O) S3 (GGV psi/eps, mixes e_i with e_{i+8})
from the 'family permutation' that actually sits INSIDE G2=Aut(O).

Key rigor point (task): the S3 must be the genuine Aut(S)/Aut(O) factor, NOT a hand-picked
permutation. The GGV psi (2pi/3 rotation in e_i--e_{i+8} planes) DOES mix the original
octonion units e_1..e_7 with the new units e_9..e_15, so it is NOT an automorphism of the
reference octonion O={e0..e7}. We verify psi is genuinely outside Aut(O), find its genuine
order-2 partner, confirm the order-6 group, and confirm its octonion ACTION.
"""
import itertools as it
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
I = sp.eye(DIM)
half = sp.Rational(1,2); sqrt3 = sp.sqrt(3)

def vmul_M(u, v):
    res = sp.zeros(DIM, 1)
    for i in range(DIM):
        if u[i]==0: continue
        for j in range(DIM):
            if v[j]==0: continue
            k,s = table[i][j]; res[k]+=u[i]*v[j]*s
    return res

def is_automorphism(M):
    cols=[M[:,j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k,s=table[i][j]
            if sp.simplify(s*cols[k]-vmul_M(cols[i],cols[j]))!=sp.zeros(DIM,1):
                return False
    return True

# psi (genuine, cross-sign +1 confirmed earlier)
def build_psi(sc=1):
    M=sp.zeros(DIM,DIM); M[0,0]=1; M[8,8]=1
    for i in range(1,8):
        j=i+8
        M[i,i]=-half; M[j,i]=sc*sqrt3*half
        M[j,j]=-half; M[i,j]=-sc*sqrt3*half
    return M
psi = build_psi(1)
print("psi: Aut(S) =", is_automorphism(psi), "; psi^3=I:", sp.simplify(psi**3-I)==sp.zeros(DIM,DIM))

# Find genuine order-2 partner eps that mixes e_i,e_{i+8}: a reflection in those planes.
# General reflection in e_i--e_{i+8} plane: e_i -> cos e_i + sin e_{i+8}, e_{i+8}-> sin e_i - cos e_{i+8}.
# The natural eps with eps psi eps = psi^{-1}: a reflection. Try eps0: e_i->e_i, e_{i+8}->-e_{i+8}
# (GGV's a+be8->a-be8). We test it AND a family of plane-reflections for genuine Aut(S).
def plane_reflection(theta_num, theta_den_pi):
    """reflection across line at angle; param by simple rationals. We instead brute a small set."""
    pass

# Candidate A: GGV eps  e_i->e_i, e_{i+8}->-e_{i+8}, e8->e8
def eps_A():
    M=sp.eye(DIM)
    for i in range(9,16): M[i,i]=-1
    return M
# Candidate B: e_i->-e_i, e_{i+8}->e_{i+8}
def eps_B():
    M=sp.eye(DIM)
    for i in range(1,8): M[i,i]=-1
    return M
# Candidate C: full conjugation e_i->-e_i (i>=1) i.e. negate ALL imaginary (this is x->conj(x), an anti-aut not aut)
# Candidate D: reflection e_i<->e_{i+8} (swap), e8->e8
def eps_D():
    M=sp.eye(DIM); M[8,8]=1; M[0,0]=1
    for i in range(1,8):
        j=i+8
        M[i,i]=0; M[j,j]=0
        M[j,i]=1; M[i,j]=1
    return M
# Candidate E: e_i -> e_{i+8}, e_{i+8}->e_i with a sign, search signs
print("\nTesting order-2 candidates that mix the e_i--e_{i+8} planes:")
for name, M in [('eps_A (e_{i+8}->-e_{i+8})',eps_A()),
                ('eps_B (e_i->-e_i)',eps_B()),
                ('eps_D (swap e_i<->e_{i+8})',eps_D())]:
    isa = is_automorphism(M)
    o2 = sp.simplify(M*M-I)==sp.zeros(DIM,DIM)
    print(f"  {name}: Aut(S)={isa}, order2={o2}")

# Brute search: eps as a reflection in planes with arbitrary signed swap pattern.
# eps: for i=1..7 pick one of: (i,i+8) block = [[a,b],[c,d]] with a,d,b,c in {0,+-1} forming
# an order-2 orthogonal map that's a reflection. Reflections: diag(1,-1),diag(-1,1),[[0,1],[1,0]],[[0,-1],[-1,0]].
# All 7 planes must use the SAME block (to commute with psi properly / be uniform). Test 4 blocks.
blocks = {
 'R1=diag(1,-1)':((1,0),(0,-1)),
 'R2=diag(-1,1)':((-1,0),(0,1)),
 'R3=swap':((0,1),(1,0)),
 'R4=-swap':((0,-1),(-1,0)),
}
print("\nUniform plane-reflection eps candidates (e8,e0 fixed):")
genuine_eps = []
for bname,((a,b),(c,d)) in blocks.items():
    M=sp.zeros(DIM,DIM); M[0,0]=1; M[8,8]=1
    for i in range(1,8):
        j=i+8
        M[i,i]=a; M[j,i]=c; M[i,j]=b; M[j,j]=d
    isa=is_automorphism(M); o2=sp.simplify(M*M-I)==sp.zeros(DIM,DIM)
    dih = sp.simplify(M*psi*M - psi*psi)==sp.zeros(DIM,DIM)  # M psi M = psi^2 = psi^-1
    print(f"  {bname}: Aut(S)={isa}, order2={o2}, dihedral(M psi M=psi^-1)={dih}")
    if isa and o2 and dih:
        genuine_eps.append((bname,M))

assert genuine_eps, "no genuine order-2 partner found"
ename, eps = genuine_eps[0]
print(f"\n  CHOSEN eps = {ename}")

# group <eps, psi>
def closure(gens):
    elements={tuple(sp.nsimplify(x) for x in I):I}; frontier=[I]
    while frontier:
        g=frontier.pop()
        for h in gens:
            p=sp.simplify(g*h); key=tuple(sp.nsimplify(x) for x in p)
            if key not in elements: elements[key]=p; frontier.append(p)
        if len(elements)>30: break
    return elements
G = closure([eps,psi])
print(f"  |<eps,psi>| = {len(G)} (S3=6)")
print("  relations: eps^2=I:", sp.simplify(eps*eps-I)==sp.zeros(DIM,DIM),
      "; psi^3=I:", sp.simplify(psi**3-I)==sp.zeros(DIM,DIM),
      "; eps psi eps = psi^-1:", sp.simplify(eps*psi*eps - psi*psi)==sp.zeros(DIM,DIM))

# NOT Aut(O): psi maps e0..e7 OUT of e0..e7?
refO=set(range(8))
for name,M in [('psi',psi),('eps',eps)]:
    img=set()
    for i in sorted(refO):
        col=M[:,i]; img.update(r for r in range(DIM) if col[r]!=0)
    verdict = 'GENUINE Aut(S) minus Aut(O)' if not img.issubset(refO) else 'inside Aut(O)!'
    print(f"  {name}: e0..e7 -> spans {sorted(img)}; stays in e0..e7? {img.issubset(refO)} ({verdict})")

# What does this genuine S3 do to O1,O2,O3? (psi rotates WITHIN each -> stabilizes setwise)
O1={0,1,4,5,8,9,12,13}; O2={0,2,4,6,8,10,12,14}; O3={0,3,4,7,8,11,12,15}
print("\n  Action of genuine S3 on the 3 GGV octonions (psi rotates within planes):")
for name,M in [('psi',psi),('eps',eps)]:
    for on,oset in [('O1',O1),('O2',O2),('O3',O3)]:
        img=set()
        for i in sorted(oset):
            col=M[:,i]; img.update(r for r in range(DIM) if col[r]!=0)
        match=[n2 for n2,s2 in [('O1',O1),('O2',O2),('O3',O3)] if img==s2]
        print(f"    {name}: {on} -> {match if match else sorted(img)}")
