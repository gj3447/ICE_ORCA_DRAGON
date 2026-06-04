"""
Complete the GENUINE S3 that permutes the three GGV octonions O1,O2,O3 as sets,
and verify all S3 properties + NOT-Aut(O) in OUR CD convention.

We found rho (order 3): index map 1->2->3->1, 5->6->7->5, 9->10->11->9, 13->14->15->13,
  fixing 0,4,8,12 (all signs +1) -- a genuine automorphism cycling O1->O2->O3.
Now find tau (order 2): a transposition automorphism, e.g. swap the (2<->3) family,
  i.e. 2<->3, 6<->7, 10<->11, 14<->15, fixing 1,5,9,13 and 0,4,8,12.
  This swaps O2<->O3 and fixes O1. Search signs for genuine automorphism.
Then <rho,tau> should be S3 (order 6), acting on {O1,O2,O3} as the full symmetric group.
"""
import itertools as it
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
I = sp.eye(DIM)

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
            if sp.simplify(s*cols[k] - vmul_M(cols[i], cols[j])) != sp.zeros(DIM, 1):
                return False
    return True

def perm_signed(perm, signs):
    M = sp.zeros(DIM, DIM)
    for j in range(DIM):
        M[perm[j], j] = signs.get(j, 1)
    return M

O1 = {0,1,4,5,8,9,12,13}; O2 = {0,2,4,6,8,10,12,14}; O3 = {0,3,4,7,8,11,12,15}
octs = [('O1',O1),('O2',O2),('O3',O3)]

def oct_image(M):
    """Which octonion each O_i maps onto (as coordinate subspace)."""
    res = {}
    for name, oset in octs:
        img = set()
        for i in sorted(oset):
            col = M[:, i]
            img.update(r for r in range(DIM) if col[r] != 0)
        match = [n2 for n2, s2 in octs if img == s2]
        res[name] = match[0] if match else f"!{sorted(img)}"
    return res

# rho (order 3 family cycle), all signs +1
rho_perm = {0:0,4:4,8:8,12:12}
for (a,b,c) in [(1,2,3),(5,6,7),(9,10,11),(13,14,15)]:
    rho_perm[a]=b; rho_perm[b]=c; rho_perm[c]=a
rho = perm_signed(rho_perm, {})
print("rho: Aut(S)=", is_automorphism(rho), " octonion action:", oct_image(rho))

# tau: swap families 2<->3 : 2<->3,6<->7,10<->11,14<->15 ; fix 1,5,9,13,0,4,8,12. search signs.
tau_perm = {i:i for i in range(DIM)}
for (a,b) in [(2,3),(6,7),(10,11),(14,15)]:
    tau_perm[a]=b; tau_perm[b]=a
moved = [i for i in range(DIM) if tau_perm[i]!=i]
tau = None
for bits in it.product((1,-1), repeat=len(moved)):
    signs={moved[k]:bits[k] for k in range(len(moved))}
    M = perm_signed(tau_perm, signs)
    if is_automorphism(M):
        tau = M; tau_signs = signs; break
print("tau (swap O2<->O3): found Aut(S)=", tau is not None)
if tau is not None:
    print("   tau signs:", tau_signs, " octonion action:", oct_image(tau))
    print("   tau^2 = I:", sp.simplify(tau*tau - I) == sp.zeros(DIM,DIM))

# group <rho, tau>
def closure(gens):
    elements = {tuple(sp.nsimplify(x) for x in I): I}
    frontier=[I]
    while frontier:
        g=frontier.pop()
        for h in gens:
            p=sp.simplify(g*h)
            key=tuple(sp.nsimplify(x) for x in p)
            if key not in elements:
                elements[key]=p; frontier.append(p)
        if len(elements)>50: break
    return elements

elts = closure([rho, tau])
print(f"\n|<rho,tau>| = {len(elts)} (S3 order = 6)")

# S3 relations: rho^3=I, tau^2=I, tau rho tau = rho^{-1}
print("  rho^3 = I:", sp.simplify(rho**3 - I)==sp.zeros(DIM,DIM))
print("  tau^2 = I:", sp.simplify(tau*tau - I)==sp.zeros(DIM,DIM))
print("  tau rho tau = rho^-1 (=rho^2):", sp.simplify(tau*rho*tau - rho*rho)==sp.zeros(DIM,DIM))

# action on the 3 octonions: collect permutations realized -> should be all 6 of S3
perms_on_octs = set()
for M in elts.values():
    oi = oct_image(M)
    perms_on_octs.add((oi['O1'],oi['O2'],oi['O3']))
print(f"\n  distinct permutations induced on (O1,O2,O3): {len(perms_on_octs)}")
for p in sorted(perms_on_octs):
    print("    ", p)

# NOT Aut(O): does any non-identity element fix the reference octonion e0..e7 setwise
# AND act as an automorphism of it? The S3 must move units OUT of {1..7} for genuine
# non-Aut(O). Check rho and tau on reference O = {0..7}.
refO = set(range(8))
print("\nNOT-Aut(O={e0..e7}) check:")
for name, M in [('rho',rho),('tau',tau)]:
    img=set()
    for i in sorted(refO):
        col=M[:,i]; img.update(r for r in range(DIM) if col[r]!=0)
    print(f"  {name}: e0..e7 -> spans {sorted(img)} ; stays in e0..e7? {img.issubset(refO)}")

# Also: is rho an automorphism of the SINGLE octonion O1 restricted? No — it MOVES O1 to O2,
# so it cannot be an automorphism of any single octonion. Confirm rho(O1) != O1.
print("\n  rho moves O1 to:", oct_image(rho)['O1'], "(not O1 => not an automorphism of O1) ")
print("  This S3 permutes the THREE octonions; it is NOT a subgroup of Aut(single O).")

# Cross-check: does this rho/tau S3 commute with / sit beside G2? Verify it is NOT inside
# the G2 that fixes e1..e7 (G2 fixes the reference octonion setwise; rho does not even
# fix O1). Already shown.

# Save the verified generators
import json
def mat_to_list(M):
    return [[str(M[r,c]) for c in range(DIM)] for r in range(DIM)]
json.dump({'rho_perm':rho_perm,'tau_signs':{str(k):v for k,v in tau_signs.items()},
           'group_order':len(elts),'octonion_perms':[list(p) for p in sorted(perms_on_octs)]},
          open('avenue3_verified_s3.json','w'), indent=2)
print("\nSaved verified S3 to avenue3_verified_s3.json")
