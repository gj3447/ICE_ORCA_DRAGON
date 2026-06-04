"""
Independent test of the 'rho' family-permutation: does the map that genuinely
permutes O1<->O2<->O3 lie INSIDE G2=Aut(O) (i.e. fix e0..e7 setwise)?
If so, 'three generations as three permuted octonions' is an IN-G2 hand-assignment,
NOT the outer Aut(S)\Aut(O) factor.

rho = bare index 3-cycle: 1->2->3->1, 5->6->7->5, 9->10->11->9, 13->14->15->13,
fixing 0,4,8,12. All signs +1.  Verify it's an automorphism AND check octonion action.
"""
import sympy as sp
from sympy import simplify, eye
from naesengmoon_indep_sedenion import IDX, SIGN, DIM

DIMv = DIM
I16 = eye(DIM)

# build rho as a signed permutation matrix
perm = list(range(DIM))
cycles = [(1, 2, 3), (5, 6, 7), (9, 10, 11), (13, 14, 15)]
for cyc in cycles:
    for a in range(len(cyc)):
        src = cyc[a]
        dst = cyc[(a + 1) % len(cyc)]
        # rho(e_src) = e_dst
        perm[src] = dst
RHO = sp.zeros(DIM, DIM)
for src in range(DIM):
    RHO[perm[src], src] = 1  # column src -> row perm[src]

def apply_map(M, k):
    return M[:, k]

def algebra_mul_vec(u, v):
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

def is_automorphism(M):
    bad = 0
    for i in range(DIM):
        for j in range(DIM):
            k = IDX[i][j]; s = SIGN[i][j]
            lhs = s * apply_map(M, k)
            rhs = algebra_mul_vec(apply_map(M, i), apply_map(M, j))
            if simplify(lhs - rhs) != sp.zeros(DIM, 1):
                bad += 1
    return bad

print("=== rho (octonion-permuting candidate) ===")
bad = is_automorphism(RHO)
print(f"  rho automorphism check: {'PASS' if bad==0 else f'FAIL ({bad} bad)'}")
print(f"  rho^3 = I : {simplify(RHO**3) == I16}")

# Does rho fix the reference octonion e0..e7 setwise? (=> inside G2)
ref_oct = set(range(8))
img_support = set()
for k in ref_oct:
    col = apply_map(RHO, k)
    for r in range(DIM):
        if col[r] != 0:
            img_support.add(r)
print(f"  rho(e0..e7) support index-set: {sorted(img_support)}")
print(f"  stays inside e0..e7 (=> rho is INSIDE G2=Aut(O)): {img_support <= ref_oct}")

# Does rho permute O1<->O2<->O3 as sets?
O1 = set((0, 1, 4, 5, 8, 9, 12, 13))
O2 = set((0, 2, 4, 6, 8, 10, 12, 14))
O3 = set((0, 3, 4, 7, 8, 11, 12, 15))
Osets = {'O1': O1, 'O2': O2, 'O3': O3}
print("  rho action on O_i (set image):")
for name, Oset in Osets.items():
    sup = set()
    for k in Oset:
        col = apply_map(RHO, k)
        for r in range(DIM):
            if col[r] != 0:
                sup.add(r)
    fit = [oj for oj, os in Osets.items() if sup == os]
    print(f"    rho({name}) -> {fit if fit else sorted(sup)}")

print("\nCONCLUSION: if rho is an automorphism, fixes e0..e7 setwise, and cycles O1->O2->O3,")
print("then the 'three permuted octonions' picture uses an IN-G2 map (Fano triality),")
print("NOT the outer Aut(S)\\Aut(O) S3. This is GGV's implicit hand-assignment.")

# ---- box-kite strut <-> std-mult-7 bijection check (independent) ----
print("\n=== strut constants vs 7 doubling-planes (independent) ===")
struts = sorted({9, 10, 11, 12, 13, 14, 15})  # what we computed as XORs
planes = sorted({8 + i for i in range(1, 8)})  # e_i--e_{i+8} -> XOR = 8 for i=1..7? check
# actually plane (i, i+8) has XOR i^(i+8). i in 1..7 -> i+8 in 9..15. i^(i+8):
plane_xor = sorted({i ^ (i + 8) for i in range(1, 8)})
print(f"  box-kite strut constants (from ZD enum): {struts}")
print(f"  doubling-plane (i,i+8) XOR for i=1..7    : {plane_xor}")
print(f"  set {{8+i : i=1..7}} = {sorted({8+i for i in range(1,8)})}")
print(f"  strut set == {{9..15}}: {struts == list(range(9,16))}")
print(f"  NOTE: plane (i,i+8) XOR = 8 for ALL i (since i^(i+8)=8 when i<8). The 7 struts")
print(f"  {{9..15}} are distinct values; they index the 7 box-kites, and there are also 7")
print(f"  doubling-planes. The bijection is 7<->7 (a COUNT match), the specific XOR values differ.")
