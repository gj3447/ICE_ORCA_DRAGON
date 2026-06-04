"""
How does the genuine S3 (psi) act on the GGV ladder operators A1,A2,A3?

GGV eqns 59-61 define (as left-multiplication elements / sedenion combos):
  A1^dag = 1/(2 sqrt2)(e1 + i e5 + e9 + i e13)
  A2^dag = 1/(2 sqrt2)(e2 + i e6 + e10 + i e14)
  A3^dag = 1/(2 sqrt2)(e3 + i e7 + e11 + i e15)
Each A_i lives in O_i. The complex sedenion C(x)S means coefficients are complex (i is the
external/Clifford imaginary, NOT a sedenion unit).

GGV's mechanism (their words, p.10): the three generations are NOT three octonions used
separately; instead all three O_i build ONE generation's ladder ops, and the ORDER-3 psi
generates the two ADDITIONAL generations by acting on these ladder operators.

We test: does psi (order-3 sedenion automorphism, extended C-linearly to C(x)S) map the
SET {A1,A2,A3} of ladder operators among themselves / produce 3 distinct images? We compute
psi(A_i^dag) in the sedenion basis and report.

NOTE: i (external) is inert under psi. psi acts only on sedenion units e1..e15.
"""
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table=build_table(); half=sp.Rational(1,2); sqrt3=sp.sqrt(3); ii=sp.I

def build_psi(sc=1):
    M=sp.zeros(DIM,DIM);M[0,0]=1;M[8,8]=1
    for i in range(1,8):
        j=i+8;M[i,i]=-half;M[j,i]=sc*sqrt3*half;M[j,j]=-half;M[i,j]=-sc*sqrt3*half
    return M
psi=build_psi(1)

# complex coefficient vectors length 16
def cvec(terms):
    v=[sp.Integer(0)]*DIM
    for idx,coef in terms:
        v[idx]+=coef
    return sp.Matrix(v)

c = 1/(2*sp.sqrt(2))
A1=cvec([(1,c),(5,c*ii),(9,c),(13,c*ii)])
A2=cvec([(2,c),(6,c*ii),(10,c),(14,c*ii)])
A3=cvec([(3,c),(7,c*ii),(11,c),(15,c*ii)])

def apply_psi(vec):
    return sp.simplify(psi*vec)

print("psi acting on ladder operators (external i inert):")
for name,A in [('A1',A1),('A2',A2),('A3',A3)]:
    img=apply_psi(A)
    nz=[(k,sp.simplify(img[k])) for k in range(DIM) if sp.simplify(img[k])!=0]
    print(f"  psi({name}) nonzero comps: {nz}")
    # express as combination of A1,A2,A3 (and their conjugates) if possible
    # check if img is a scalar multiple of some A_j
    for jn,Aj in [('A1',A1),('A2',A2),('A3',A3)]:
        # ratio test on first shared nonzero comp
        ratios=set()
        ok=True
        for k in range(DIM):
            a=sp.simplify(img[k]); b=sp.simplify(Aj[k])
            if b==0 and a!=0: ok=False; break
            if b!=0:
                ratios.add(sp.simplify(a/b))
        if ok and len(ratios)==1:
            print(f"      = {list(ratios)[0]} * {jn}")

# Also: psi^3 = I means {A_i, psi A_i, psi^2 A_i} is an orbit of size dividing 3.
print("\norbit sizes under <psi> (order 3):")
for name,A in [('A1',A1),('A2',A2),('A3',A3)]:
    orbit=[A]
    cur=A
    for _ in range(2):
        cur=sp.simplify(psi*cur); orbit.append(cur)
    distinct=[]
    for o in orbit:
        if not any(sp.simplify(o-d)==sp.zeros(DIM,1) for d in distinct):
            distinct.append(o)
    print(f"  {name}: orbit has {len(distinct)} distinct images under {{I,psi,psi^2}}")
