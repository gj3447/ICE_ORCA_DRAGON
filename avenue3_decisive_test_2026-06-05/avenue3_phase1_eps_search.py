"""
Exhaustive-ish search for the genuine order-2 automorphism eps that completes S3=<eps,psi>.
psi is the verified 2pi/3 rotation in e_i--e_{i+8} planes (genuine Aut(S)\\Aut(O)).
We search eps among orthogonal maps that act block-diagonally on the 7 planes
{e_i,e_{i+8}} (i=1..7), each plane independently one of the 8 order-<=2 orthogonal 2x2
blocks, plus optional sign on e8. We KEEP only genuine Aut(S) with eps^2=I and
eps psi eps = psi^{-1}. Report ALL solutions and whether each is genuinely outside Aut(O).
"""
import itertools as it
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table=build_table(); I=sp.eye(DIM); half=sp.Rational(1,2); sqrt3=sp.sqrt(3)

def vmul_M(u,v):
    res=sp.zeros(DIM,1)
    for i in range(DIM):
        if u[i]==0: continue
        for j in range(DIM):
            if v[j]==0: continue
            k,s=table[i][j]; res[k]+=u[i]*v[j]*s
    return res
def is_automorphism(M):
    cols=[M[:,j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k,s=table[i][j]
            if sp.simplify(s*cols[k]-vmul_M(cols[i],cols[j]))!=sp.zeros(DIM,1): return False
    return True
def build_psi(sc=1):
    M=sp.zeros(DIM,DIM);M[0,0]=1;M[8,8]=1
    for i in range(1,8):
        j=i+8;M[i,i]=-half;M[j,i]=sc*sqrt3*half;M[j,j]=-half;M[i,j]=-sc*sqrt3*half
    return M
psi=build_psi(1)

# order<=2 orthogonal integer 2x2 blocks (reflections + diag identity is order1, skip pure I per-plane
# but allow it since global must be order2): det=+-1, B^2=I.
cand_blocks=[]
for a in (-1,0,1):
    for b in (-1,0,1):
        for c in (-1,0,1):
            for d in (-1,0,1):
                B=sp.Matrix([[a,b],[c,d]])
                if B*B==sp.eye(2):
                    cand_blocks.append((a,b,c,d))
cand_blocks=list(set(cand_blocks))
print(f"order<=2 integer 2x2 blocks: {len(cand_blocks)}")

# Instead of 8^7 (too big), use the constraint: eps psi eps = psi^-1 forces each plane's
# block B to satisfy B*R*B = R^{-1} where R = [[-1/2,-sqrt3/2],[sqrt3/2,-1/2]] is the
# per-plane rotation. Solve per-plane.
R=sp.Matrix([[-half,-sqrt3*half],[sqrt3*half,-half]])
Rinv=R.inv()
good_blocks=[B for B in cand_blocks
             if sp.Matrix([[B[0],B[1]],[B[2],B[3]]])*R*sp.Matrix([[B[0],B[1]],[B[2],B[3]]])==Rinv]
print(f"per-plane blocks B with B R B = R^-1: {len(good_blocks)} -> {good_blocks}")

# Now eps must use, per plane, one of good_blocks. e8 sign: +-1. Try uniform first, then mixed.
def assemble(blocks_per_plane, e8sign):
    M=sp.zeros(DIM,DIM); M[0,0]=1; M[8,8]=e8sign
    for idx,i in enumerate(range(1,8)):
        j=i+8; a,b,c,d=blocks_per_plane[idx]
        M[i,i]=a; M[i,j]=b; M[j,i]=c; M[j,j]=d
    return M

solutions=[]
# uniform across planes:
for B in good_blocks:
    for e8s in (1,-1):
        M=assemble([B]*7, e8s)
        if M*M==I and is_automorphism(M):
            solutions.append(('uniform',B,e8s,M))
print(f"\nUNIFORM eps solutions (genuine Aut(S), order2, dihedral): {len(solutions)}")
for tag,B,e8s,M in solutions:
    refO=set(range(8)); img=set()
    for i in range(8):
        col=M[:,i]; img.update(r for r in range(DIM) if col[r]!=0)
    genuine = not img.issubset(refO)
    print(f"  block={B}, e8sign={e8s}: e0..e7 stays in O? {img.issubset(refO)} -> "
          f"{'GENUINE outside Aut(O)' if genuine else 'inside Aut(O)'}")

# If no uniform, try mixed (could be large; only if needed)
if not solutions:
    print("\nNo uniform solution; trying mixed per-plane (bounded)...")
    cnt=0
    for combo in it.product(good_blocks, repeat=7):
        for e8s in (1,-1):
            M=assemble(list(combo), e8s)
            if M*M==I and is_automorphism(M):
                solutions.append(('mixed',combo,e8s,M)); cnt+=1
                if cnt>=5: break
        if cnt>=5: break
    print(f"  mixed solutions found: {cnt}")

# Take first genuine solution, build group, verify octonion action
if solutions:
    tag,B,e8s,eps = solutions[0]
    def closure(gens):
        E={tuple(sp.nsimplify(x) for x in I):I}; fr=[I]
        while fr:
            g=fr.pop()
            for h in gens:
                p=sp.simplify(g*h); key=tuple(sp.nsimplify(x) for x in p)
                if key not in E: E[key]=p; fr.append(p)
            if len(E)>30: break
        return E
    G=closure([eps,psi])
    print(f"\nFINAL S3: |<eps,psi>|={len(G)}; eps^2=I:{eps*eps==I}; psi^3=I:{sp.simplify(psi**3-I)==sp.zeros(DIM,DIM)}; "
          f"eps psi eps = psi^-1:{sp.simplify(eps*psi*eps-psi*psi)==sp.zeros(DIM,DIM)}")
    O1={0,1,4,5,8,9,12,13};O2={0,2,4,6,8,10,12,14};O3={0,3,4,7,8,11,12,15}
    print("  Octonion action (psi rotates within planes, stabilizes each O_i setwise):")
    for name,M in [('psi',psi),('eps',eps)]:
        line=[]
        for on,oset in [('O1',O1),('O2',O2),('O3',O3)]:
            img=set()
            for i in sorted(oset):
                col=M[:,i]; img.update(r for r in range(DIM) if col[r]!=0)
            m=[n2 for n2,s2 in [('O1',O1),('O2',O2),('O3',O3)] if img==s2]
            line.append(f"{on}->{m[0] if m else 'mixed'}")
        print(f"    {name}: {', '.join(line)}")
