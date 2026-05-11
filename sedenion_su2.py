# LONGINUS: sourceId=sedenion_su2, sourcePath=sedenion_su2.py
"""
Construct SU(2) representations from 4D null spaces of sedenion zero-divisor pairs.

Sedenions = 16D Cayley-Dickson algebra built from octonions.
Standard CD construction: (a1,a2)(b1,b2) = (a1*b1 - conj(b2)*a2, b2*a1 + a2*conj(b1))
"""

import numpy as np
from itertools import combinations, product

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ============================================================
# STEP 0: Build sedenion multiplication table via CD construction
# ============================================================

def cd_multiply(a, b, n):
    """
    Multiply two elements in the 2^n-dimensional Cayley-Dickson algebra.
    a, b are numpy arrays of length 2^n.
    n=0: reals, n=1: complex, n=2: quaternions, n=3: octonions, n=4: sedenions
    """
    dim = 2**n
    assert len(a) == dim and len(b) == dim

    if n == 0:
        return a * b

    half = dim // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]

    # conj in sub-algebra: negate all imaginary parts
    def conj_sub(x):
        c = -x.copy()
        c[0] = x[0]  # real part unchanged
        return c

    # (a1,a2)(b1,b2) = (a1*b1 - conj(b2)*a2, b2*a1 + a2*conj(b1))
    part1 = cd_multiply(a1, b1, n-1) - cd_multiply(conj_sub(b2), a2, n-1)
    part2 = cd_multiply(b2, a1, n-1) + cd_multiply(a2, conj_sub(b1), n-1)

    return np.concatenate([part1, part2])


def build_sedenion_mult_table():
    """Build 16x16x16 structure constants for sedenions."""
    n = 4  # sedenions
    dim = 16
    table = np.zeros((dim, dim, dim), dtype=float)

    for i in range(dim):
        for j in range(dim):
            ei = np.zeros(dim)
            ej = np.zeros(dim)
            ei[i] = 1.0
            ej[j] = 1.0
            prod = cd_multiply(ei, ej, n)
            table[i, j, :] = prod

    return table

print("Building sedenion multiplication table...")
MULT = build_sedenion_mult_table()

# Verify: e0 is identity
print("\nVerification: e0 * e_i = e_i for all i?",
      np.allclose(MULT[0], np.eye(16)))

# Verify: e_i * e_i = -e0 for i>0
for i in range(1, 16):
    prod = MULT[i, i]
    expected = np.zeros(16)
    expected[0] = -1.0
    if not np.allclose(prod, expected):
        print(f"  WARNING: e{i}^2 != -1, got {prod}")
print("All e_i^2 = -1 for i=1..15: ",
      all(np.allclose(MULT[i,i,0], -1) and np.allclose(np.sum(np.abs(MULT[i,i,1:])), 0) for i in range(1,16)))

# ============================================================
# STEP 1: Left multiplication operator and null space
# ============================================================

def left_mult_matrix(a):
    """Return 16x16 matrix L_a such that L_a @ x = a*x in sedenion algebra."""
    dim = 16
    L = np.zeros((dim, dim))
    for j in range(dim):
        ej = np.zeros(dim)
        ej[j] = 1.0
        # L_a @ e_j = a * e_j
        prod = np.zeros(dim)
        for k in range(dim):
            if a[k] != 0:
                prod += a[k] * MULT[k, j]
        L[:, j] = prod
    return L

print("\n" + "="*70)
print("STEP 1: Analyze zero-divisor pair e1 + e10")
print("="*70)

# Construct a = e1 + e10
a = np.zeros(16)
a[1] = 1.0   # e1 (octonion sector)
a[10] = 1.0  # e10 (sedenion sector, = e2*e8 in CD)

La = left_mult_matrix(a)
print(f"\nL_a for a = e1+e10, shape: {La.shape}")
print(f"Rank of L_a: {np.linalg.matrix_rank(La, tol=1e-10)}")

# SVD to find null space
U, S, Vh = np.linalg.svd(La)
print(f"Singular values: {S}")

null_mask = S < 1e-10
null_dim = np.sum(null_mask)
print(f"Null space dimension: {null_dim}")

# Null space basis (rows of Vh corresponding to zero singular values)
null_basis = Vh[~(S > 1e-10)].T  # columns are null vectors
# More robust: use the last null_dim rows of Vh
null_basis = Vh[-null_dim:].T  # shape (16, null_dim)
print(f"Null basis shape: {null_basis.shape}")

# Verify null space
for k in range(null_basis.shape[1]):
    v = null_basis[:, k]
    res = La @ v
    assert np.allclose(res, 0, atol=1e-10), f"Null vector {k} not in null space! residual={np.linalg.norm(res)}"
print("All null vectors verified: L_a @ v = 0")

# Print null basis vectors (which basis elements they involve)
print("\nNull space basis vectors (nonzero components):")
for k in range(null_basis.shape[1]):
    v = null_basis[:, k]
    nonzero = [(i, v[i]) for i in range(16) if abs(v[i]) > 1e-10]
    print(f"  v{k}: {nonzero}")

# ============================================================
# STEP 2: Find quaternionic structure in the 4D null space
# ============================================================

print("\n" + "="*70)
print("STEP 2: Search for quaternionic structure in the 4D null space")
print("="*70)

def project_to_nullspace(M, null_basis):
    """Project a 16x16 matrix M onto the null space.
    Returns a null_dim x null_dim matrix."""
    return null_basis.T @ M @ null_basis

def find_quaternionic_structure(null_basis):
    """
    Search for J1, J2, J3 acting on the 4D null space satisfying:
    J1^2 = J2^2 = J3^2 = -I
    J1 J2 = J3

    Strategy: Use right-multiplication by sedenion basis elements,
    projected onto the null space.
    """
    dim = null_basis.shape[1]
    print(f"  Null space dimension: {dim}")

    # Try right-multiplication operators R_{e_i} projected onto null space
    # R_{e_i}(x) = x * e_i
    candidates = []

    def right_mult_matrix(b):
        """16x16 matrix R_b: R_b @ x = x * b"""
        R = np.zeros((16, 16))
        for j in range(16):
            ej = np.zeros(16)
            ej[j] = 1.0
            prod = np.zeros(16)
            for k in range(16):
                if b[k] != 0:
                    prod += b[k] * MULT[j, k]
            R[:, j] = prod
        return R

    # First check: does right multiplication by e_i map null space to itself?
    print("\n  Checking which R_{e_i} preserve the null space:")
    preserving = []
    for i in range(1, 16):  # skip e0=identity
        ei = np.zeros(16)
        ei[i] = 1.0
        Ri = right_mult_matrix(ei)

        # Check if Ri maps null space into null space
        # Project Ri|_null onto null space: if Ri preserves null space,
        # then null_basis.T @ Ri @ null_basis should be the full action
        # and Ri @ null_basis should lie in the column span of null_basis

        image = Ri @ null_basis  # 16 x null_dim
        # Project image onto null space
        proj = null_basis @ (null_basis.T @ image)
        residual = np.linalg.norm(image - proj)

        if residual < 1e-10:
            J = null_basis.T @ Ri @ null_basis
            # Check if J^2 = -I
            J2 = J @ J
            is_minus_I = np.allclose(J2, -np.eye(dim), atol=1e-10)
            print(f"    R_e{i}: preserves null space, J^2={'−I' if is_minus_I else 'other'}")
            if is_minus_I:
                preserving.append((i, J))
                candidates.append((i, J))
        # else: doesn't preserve null space

    if not preserving:
        print("  No right-multiplication operators preserve the null space with J^2=-I")

    # Also try LEFT multiplication by octonion-sector elements
    print("\n  Checking L_{e_i} (restricted to null space) for i in octonion sector:")
    for i in range(1, 8):
        ei = np.zeros(16)
        ei[i] = 1.0
        Li = left_mult_matrix(ei)

        image = Li @ null_basis
        proj = null_basis @ (null_basis.T @ image)
        residual = np.linalg.norm(image - proj)

        if residual < 1e-10:
            J = null_basis.T @ Li @ null_basis
            J2 = J @ J
            is_minus_I = np.allclose(J2, -np.eye(dim), atol=1e-10)
            print(f"    L_e{i}: preserves null space, J^2={'−I' if is_minus_I else 'other'}")
            if is_minus_I:
                candidates.append((f"L{i}", J))

    # Try sedenion-sector left multiplication
    print("\n  Checking L_{e_i} for i in sedenion sector (8..15):")
    for i in range(8, 16):
        ei = np.zeros(16)
        ei[i] = 1.0
        Li = left_mult_matrix(ei)

        image = Li @ null_basis
        proj = null_basis @ (null_basis.T @ image)
        residual = np.linalg.norm(image - proj)

        if residual < 1e-10:
            J = null_basis.T @ Li @ null_basis
            J2 = J @ J
            is_minus_I = np.allclose(J2, -np.eye(dim), atol=1e-10)
            print(f"    L_e{i}: preserves null space, J^2={'−I' if is_minus_I else 'other'}")
            if is_minus_I:
                candidates.append((f"Ls{i}", J))

    return candidates

candidates = find_quaternionic_structure(null_basis)

print(f"\n  Total candidates with J^2 = -I: {len(candidates)}")
for label, J in candidates:
    print(f"    {label}: J =\n{J}")

# ============================================================
# STEP 2b: Check quaternion algebra among candidates
# ============================================================

print("\n" + "="*70)
print("STEP 2b: Check if candidates form quaternion algebra")
print("="*70)

if len(candidates) >= 2:
    print("  Checking all pairs for J_a J_b = -J_b J_a (anticommutation):")
    quaternion_triples = []
    for idx_a in range(len(candidates)):
        for idx_b in range(idx_a+1, len(candidates)):
            la, Ja = candidates[idx_a]
            lb, Jb = candidates[idx_b]
            comm = Ja @ Jb + Jb @ Ja
            anticomm = np.allclose(comm, 0, atol=1e-10)
            if anticomm:
                # J3 = J1 @ J2
                Jc = Ja @ Jb
                Jc2 = Jc @ Jc
                is_minus_I = np.allclose(Jc2, -np.eye(Ja.shape[0]), atol=1e-10)
                print(f"    {la}, {lb}: anticommute={anticomm}, J1J2 squares to -I: {is_minus_I}")
                if is_minus_I:
                    quaternion_triples.append((la, lb, Ja, Jb, Jc))
            else:
                print(f"    {la}, {lb}: do NOT anticommute")

    if quaternion_triples:
        print(f"\n  Found {len(quaternion_triples)} quaternionic triple(s)!")
        la, lb, J1, J2, J3 = quaternion_triples[0]
        print(f"  Using triple: ({la}, {lb}, {la}*{lb})")
        print(f"  J1 =\n{J1}")
        print(f"  J2 =\n{J2}")
        print(f"  J3 = J1@J2 =\n{J3}")

        # Full quaternion checks
        print(f"\n  Verification:")
        print(f"    J1^2 = -I: {np.allclose(J1@J1, -np.eye(4), atol=1e-10)}")
        print(f"    J2^2 = -I: {np.allclose(J2@J2, -np.eye(4), atol=1e-10)}")
        print(f"    J3^2 = -I: {np.allclose(J3@J3, -np.eye(4), atol=1e-10)}")
        print(f"    J1@J2 = J3: {np.allclose(J1@J2, J3, atol=1e-10)}")
        print(f"    J2@J1 = -J3: {np.allclose(J2@J1, -J3, atol=1e-10)}")
        print(f"    J2@J3 = J1: {np.allclose(J2@J3, J1, atol=1e-10)}")
        print(f"    J3@J1 = J2: {np.allclose(J3@J1, J2, atol=1e-10)}")

# ============================================================
# STEP 3: Construct su(2) generators
# ============================================================

print("\n" + "="*70)
print("STEP 3: Construct su(2) generators from quaternionic structure")
print("="*70)

if quaternion_triples:
    la, lb, J1, J2, J3 = quaternion_triples[0]

    # su(2) generators: T_k = -i/2 * J_k  (but we work with real matrices)
    # In real form, J1, J2, J3 already generate so(3) ~ su(2)
    # The Lie algebra: [J1, J2] = 2*J3 etc.

    print("  Commutation relations (should give [Ja,Jb] = 2*Jc cyclically):")
    comm12 = J1 @ J2 - J2 @ J1
    comm23 = J2 @ J3 - J3 @ J2
    comm31 = J3 @ J1 - J1 @ J3
    print(f"    [J1,J2] = 2*J3? {np.allclose(comm12, 2*J3, atol=1e-10)}")
    print(f"    [J2,J3] = 2*J1? {np.allclose(comm23, 2*J1, atol=1e-10)}")
    print(f"    [J3,J1] = 2*J2? {np.allclose(comm31, 2*J2, atol=1e-10)}")

    # Standard su(2) generators: T_k = J_k / 2
    T1 = J1 / 2.0
    T2 = J2 / 2.0
    T3 = J3 / 2.0

    print(f"\n  su(2) generators T_k = J_k/2:")
    print(f"    [T1,T2] = T3? {np.allclose(T1@T2 - T2@T1, T3, atol=1e-10)}")
    print(f"    [T2,T3] = T1? {np.allclose(T2@T3 - T3@T2, T1, atol=1e-10)}")
    print(f"    [T3,T1] = T2? {np.allclose(T3@T1 - T1@T3, T2, atol=1e-10)}")

    # Casimir operator
    C = T1@T1 + T2@T2 + T3@T3
    print(f"\n  Casimir C = T1^2 + T2^2 + T3^2 =\n{C}")
    print(f"  C = c*I? eigenvalues of C: {np.linalg.eigvalsh(C)}")
    casimir_val = C[0,0]
    print(f"  Casimir value: {casimir_val}")
    print(f"  For spin j, C = -j(j+1)*I. So j(j+1) = {-casimir_val}")
    j_val = (-1 + np.sqrt(1 + 4*(-casimir_val))) / 2
    print(f"  => j = {j_val}")

    # ============================================================
    # STEP 3b: Diagonalize T3 to see the representation
    # ============================================================
    print("\n  Diagonalizing T3 to find weight structure:")
    eigenvalues_T3, eigenvecs_T3 = np.linalg.eigh(T3)
    # T3 is real antisymmetric, so eigenvalues are purely imaginary
    # Use general eigensolver
    eigenvalues_T3_c, eigenvecs_T3_c = np.linalg.eig(T3)
    print(f"  T3 eigenvalues: {eigenvalues_T3_c}")
    print(f"  T3 matrix:\n{T3}")

    # For real antisymmetric matrices, work with iT3 which is Hermitian
    iT3 = 1j * T3
    evals_iT3, evecs_iT3 = np.linalg.eigh(iT3)
    print(f"\n  Eigenvalues of i*T3 (weights): {evals_iT3}")
    print(f"  These are the m values of the representation")

# ============================================================
# STEP 4: Compare with octonion-sector quaternionic su(2)
# ============================================================

print("\n" + "="*70)
print("STEP 4: Compare with 'old' octonion quaternionic su(2)")
print("="*70)

# The octonion subalgebra lives in e0..e7
# Standard quaternion subalgebra: e1, e2, e3 with e1*e2=e3
# These generate an su(2) via left multiplication on the FULL 16D space

# Build the "old" su(2) from L_{e1}, L_{e2}, L_{e3} restricted to null space
if quaternion_triples:
    print("  Old su(2) from octonion quaternion subalgebra {e1,e2,e3}:")

    for i in [1, 2, 3]:
        ei = np.zeros(16)
        ei[i] = 1.0
        Li = left_mult_matrix(ei)
        image = Li @ null_basis
        proj = null_basis @ (null_basis.T @ image)
        residual = np.linalg.norm(image - proj)
        print(f"    L_e{i} preserves null space? residual = {residual:.2e}")

    # Check other quaternion triples in the octonion:
    # Fano plane triples for octonions
    fano_triples = [
        (1,2,3), (1,4,5), (1,7,6), (2,4,6), (2,5,7), (3,4,7), (3,6,5)
    ]

    print("\n  Checking all Fano plane triples for null-space preservation:")
    for (i,j,k) in fano_triples:
        preserves = True
        Js = []
        for idx in [i,j,k]:
            ei = np.zeros(16)
            ei[idx] = 1.0
            Li = left_mult_matrix(ei)
            image = Li @ null_basis
            proj = null_basis @ (null_basis.T @ image)
            residual = np.linalg.norm(image - proj)
            if residual > 1e-10:
                preserves = False
                break
            Js.append(null_basis.T @ Li @ null_basis)

        if preserves:
            # Check quaternion relations
            prod = Js[0] @ Js[1]
            sign = 1 if np.allclose(prod, Js[2], atol=1e-10) else (-1 if np.allclose(prod, -Js[2], atol=1e-10) else 0)
            print(f"    ({i},{j},{k}): preserves null space, e{i}*e{j}={'+'if sign==1 else '-' if sign==-1 else '?'}e{k}")
        else:
            print(f"    ({i},{j},{k}): does NOT preserve null space")

# ============================================================
# STEP 5: Check universality across different ZD pairs
# ============================================================

print("\n" + "="*70)
print("STEP 5: Check su(2) structure across multiple ZD pairs")
print("="*70)

def get_null_space(i, j):
    """Get null space of L_{e_i + e_j}."""
    a = np.zeros(16)
    a[i] = 1.0
    a[j] = 1.0
    La = left_mult_matrix(a)
    U, S, Vh = np.linalg.svd(La)
    null_dim = np.sum(S < 1e-10)
    if null_dim == 0:
        return None
    null_b = Vh[-null_dim:].T
    return null_b

def check_quaternionic_from_right_mult(null_b):
    """Check which right-mult operators preserve null space and give J^2=-I."""
    dim = null_b.shape[1]
    cands = []
    for idx in range(1, 16):
        ei = np.zeros(16)
        ei[idx] = 1.0
        # Right multiplication
        R = np.zeros((16, 16))
        for col in range(16):
            ec = np.zeros(16)
            ec[col] = 1.0
            prod = np.zeros(16)
            for k in range(16):
                if ei[k] != 0:
                    prod += ei[k] * MULT[col, k]
            R[:, col] = prod

        image = R @ null_b
        proj = null_b @ (null_b.T @ image)
        residual = np.linalg.norm(image - proj)

        if residual < 1e-10:
            J = null_b.T @ R @ null_b
            J2 = J @ J
            if np.allclose(J2, -np.eye(dim), atol=1e-10):
                cands.append((idx, J))
    return cands

# Check a selection of cross-sector ZD pairs
print("  Checking quaternionic structure for various ZD pairs (e_i + e_j, i<8, j>=8):")
print(f"  {'Pair':<12} {'Null dim':<10} {'#J^2=-I cands':<15} {'Has quat triple'}")
print(f"  {'-'*50}")

all_results = []
for i in range(1, 8):
    for j in range(8, 16):
        nb = get_null_space(i, j)
        if nb is None or nb.shape[1] != 4:
            null_d = 0 if nb is None else nb.shape[1]
            print(f"  e{i}+e{j:<3}    {null_d:<10} {'N/A':<15} N/A")
            continue

        cands = check_quaternionic_from_right_mult(nb)

        # Check for quaternion triples
        has_triple = False
        triple_labels = None
        for ia in range(len(cands)):
            for ib in range(ia+1, len(cands)):
                la, Ja = cands[ia]
                lb, Jb = cands[ib]
                comm = Ja @ Jb + Jb @ Ja
                if np.allclose(comm, 0, atol=1e-10):
                    Jc = Ja @ Jb
                    if np.allclose(Jc @ Jc, -np.eye(4), atol=1e-10):
                        has_triple = True
                        triple_labels = (la, lb)
                        break
            if has_triple:
                break

        cand_labels = [c[0] for c in cands]
        print(f"  e{i}+e{j:<3}    {4:<10} {len(cands):<15} {has_triple} {cand_labels if cands else ''}")
        all_results.append((i, j, nb, cands, has_triple))

# ============================================================
# STEP 5b: Compare the su(2) algebras across different ZD pairs
# ============================================================

print("\n" + "="*70)
print("STEP 5b: Compare su(2) algebras across ZD pairs (gauge universality)")
print("="*70)

# For pairs that have quaternionic structure, extract the triple and compare
triples_found = []
for (i, j, nb, cands, has_triple) in all_results:
    if not has_triple or len(cands) < 2:
        continue
    # Find a triple
    for ia in range(len(cands)):
        for ib in range(ia+1, len(cands)):
            la, Ja = cands[ia]
            lb, Jb = cands[ib]
            comm = Ja @ Jb + Jb @ Ja
            if np.allclose(comm, 0, atol=1e-10):
                Jc = Ja @ Jb
                if np.allclose(Jc @ Jc, -np.eye(4), atol=1e-10):
                    triples_found.append((i, j, la, lb, Ja, Jb, Jc, nb))
                    break
        else:
            continue
        break

print(f"  Found {len(triples_found)} ZD pairs with quaternionic triples")

if len(triples_found) >= 2:
    print("\n  Comparing the right-mult indices used across pairs:")
    for (i, j, la, lb, Ja, Jb, Jc, nb) in triples_found[:10]:
        print(f"    e{i}+e{j}: R_e{la}, R_e{lb}")

# ============================================================
# STEP 6: Check doublet decomposition (weak isospin structure)
# ============================================================

print("\n" + "="*70)
print("STEP 6: Check doublet decomposition of the 4D null space under su(2)")
print("="*70)

if triples_found:
    # Take the first triple
    i, j, la, lb, J1, J2, J3, nb = triples_found[0]
    print(f"  Using ZD pair e{i}+e{j}, quaternion triple R_e{la}, R_e{lb}")

    T1, T2, T3 = J1/2, J2/2, J3/2

    # The 4D null space under su(2) should decompose as representations
    # For spin-1/2 doublet: 4D = two doublets (2+2) or one spin-3/2 (4D)

    # Casimir
    C = T1@T1 + T2@T2 + T3@T3
    print(f"\n  Casimir operator C = T1^2+T2^2+T3^2:")
    print(f"  {C}")
    evals_C = np.linalg.eigvalsh(C)
    print(f"  Eigenvalues of C: {evals_C}")

    # For j=1/2: C = -3/4 * I  (since T_k are real antisymmetric, T_k^2 has negative eigenvalues)
    # For j=3/2: C = -15/4 * I

    if np.allclose(evals_C, evals_C[0] * np.ones(4), atol=1e-10):
        print(f"  C is proportional to identity: C = {evals_C[0]:.6f} * I")
        jj1 = -evals_C[0]
        print(f"  j(j+1) = {jj1:.6f}")
        j_spin = (-1 + np.sqrt(1 + 4*jj1)) / 2
        print(f"  => j = {j_spin:.6f}")

        if abs(j_spin - 0.5) < 0.01:
            print(f"\n  *** 4D null space is a SPIN-1/2 (DOUBLET x 2) representation! ***")
            print(f"  This decomposes as TWO doublets of su(2)")
            print(f"  (4D real = 2D complex = one complex doublet under complexified su(2))")
        elif abs(j_spin - 1.5) < 0.01:
            print(f"\n  *** 4D null space is a SPIN-3/2 representation! ***")
    else:
        print(f"  C is NOT proportional to identity => reducible representation")
        print(f"  Eigenvalues suggest decomposition into irreps")

        # Find the irrep decomposition
        unique_evals = np.unique(np.round(evals_C, 8))
        for ev in unique_evals:
            mult = np.sum(np.abs(evals_C - ev) < 1e-6)
            jj1 = -ev
            j_spin = (-1 + np.sqrt(1 + 4*jj1)) / 2
            print(f"    Eigenvalue {ev:.6f}: multiplicity {mult}, j = {j_spin:.4f}")

    # Complexified analysis
    print(f"\n  Complexified analysis:")
    print(f"  Working with iT3 (Hermitian):")
    iT3 = 1j * T3
    evals_m, evecs_m = np.linalg.eigh(iT3)
    print(f"  Eigenvalues of iT3 (m-values): {evals_m}")

    # Check raising/lowering operators
    Tplus = T1 + 1j * T2
    Tminus = T1 - 1j * T2
    print(f"\n  T+ = T1 + iT2:\n{Tplus}")
    print(f"  T- = T1 - iT2:\n{Tminus}")

    # In the eigenbasis of iT3
    P = evecs_m  # columns are eigenvectors
    iT3_diag = P.conj().T @ iT3 @ P
    Tp_diag = P.conj().T @ Tplus @ P
    Tm_diag = P.conj().T @ Tminus @ P

    print(f"\n  In iT3 eigenbasis:")
    print(f"  iT3 (diag):\n{np.real_if_close(iT3_diag)}")
    print(f"  T+ :\n{np.real_if_close(Tp_diag)}")
    print(f"  T- :\n{np.real_if_close(Tm_diag)}")

# ============================================================
# STEP 6b: Explicit doublet identification
# ============================================================

print("\n" + "="*70)
print("STEP 6b: Explicit doublet identification")
print("="*70)

if triples_found:
    i, j, la, lb, J1, J2, J3, nb = triples_found[0]

    # J3 is a real antisymmetric 4x4 matrix
    # Its eigenvalues come in conjugate pairs: ±iλ
    # Find the 2D real eigenspaces

    # Eigendecomposition of J3
    evals, evecs = np.linalg.eig(J3)
    print(f"  J3 eigenvalues: {evals}")

    # J3 as block-diagonal in appropriate basis
    # Find orthogonal transformation to bring J3 to canonical form
    # For real antisymmetric matrix, Schur form gives 2x2 blocks
    from scipy.linalg import schur
    T_schur, Q = schur(J3, output='real')
    print(f"\n  Schur form of J3:\n{T_schur}")
    print(f"  Orthogonal basis Q:\n{Q}")

    # In the Schur basis, look at J1 and J2
    J1_schur = Q.T @ J1 @ Q
    J2_schur = Q.T @ J2 @ Q
    J3_schur = T_schur

    print(f"\n  J1 in Schur basis:\n{J1_schur}")
    print(f"  J2 in Schur basis:\n{J2_schur}")
    print(f"  J3 in Schur basis:\n{J3_schur}")

    # Check if the 4D splits into two 2D invariant subspaces
    # under all three J's simultaneously
    # If J3 is block diagonal with two 2x2 blocks, check if J1, J2 also respect this

    top_block_J1 = J1_schur[:2, :2]
    bot_block_J1 = J1_schur[2:, 2:]
    off_diag_J1 = np.linalg.norm(J1_schur[:2, 2:]) + np.linalg.norm(J1_schur[2:, :2])

    top_block_J2 = J2_schur[:2, :2]
    bot_block_J2 = J2_schur[2:, 2:]
    off_diag_J2 = np.linalg.norm(J2_schur[:2, 2:]) + np.linalg.norm(J2_schur[2:, :2])

    print(f"\n  Off-diagonal coupling in J1 (Schur basis): {off_diag_J1:.6e}")
    print(f"  Off-diagonal coupling in J2 (Schur basis): {off_diag_J2:.6e}")

    if off_diag_J1 < 1e-10 and off_diag_J2 < 1e-10:
        print(f"\n  *** The 4D null space decomposes into TWO 2D INVARIANT subspaces ***")
        print(f"  *** under the full su(2) algebra! ***")
        print(f"\n  Block 1 (rows 0,1): 2D irrep")
        print(f"    J1 = \n{top_block_J1}")
        print(f"    J2 = \n{top_block_J2}")
        print(f"    J3 = \n{J3_schur[:2,:2]}")
        print(f"\n  Block 2 (rows 2,3): 2D irrep")
        print(f"    J1 = \n{bot_block_J1}")
        print(f"    J2 = \n{bot_block_J2}")
        print(f"    J3 = \n{J3_schur[2:,2:]}")

        # Check if both blocks are equivalent representations
        # Two 2D real irreps of su(2) ~ quaternion imaginary units on R^2
        # They should be isomorphic (both are the fundamental rep on R^2)
        print(f"\n  Are the two 2D irreps equivalent?")
        # sigma_2 structure: J ~ [[0,-1],[1,0]]
        print(f"    Block 1 J3: {J3_schur[:2,:2].flatten()}")
        print(f"    Block 2 J3: {J3_schur[2:,2:].flatten()}")

        # Check: each 2D block is a spin-1/2 doublet
        # For spin-1/2 in real form: T_k are 2x2 antisymmetric ∝ epsilon
        for blk_idx, (b1, b2, b3) in enumerate([(top_block_J1, top_block_J2, J3_schur[:2,:2]),
                                                   (bot_block_J1, bot_block_J2, J3_schur[2:,2:])]):
            print(f"\n    Block {blk_idx+1} quaternion check:")
            print(f"      J1^2 = -I? {np.allclose(b1@b1, -np.eye(2), atol=1e-10)}")
            print(f"      J2^2 = -I? {np.allclose(b2@b2, -np.eye(2), atol=1e-10)}")
            print(f"      J3^2 = -I? {np.allclose(b3@b3, -np.eye(2), atol=1e-10)}")
            print(f"      J1@J2 = J3? {np.allclose(b1@b2, b3, atol=1e-10)}")

    else:
        print(f"\n  The su(2) acts IRREDUCIBLY on the 4D space")
        print(f"  => This is a single spin-3/2 or the decomposition needs a different basis")

# ============================================================
# STEP 7: Summary statistics
# ============================================================

print("\n" + "="*70)
print("STEP 7: SUMMARY")
print("="*70)

n_zd = len(all_results)
n_quat = sum(1 for r in all_results if r[4])  # has_triple=True
print(f"  Total cross-sector ZD pairs with 4D null space: {n_zd}")
print(f"  Of these, pairs with quaternionic structure: {n_quat}")
print(f"  Fraction: {n_quat}/{n_zd} = {n_quat/n_zd if n_zd > 0 else 0:.3f}")

# Collect the right-mult indices used
if triples_found:
    print(f"\n  Right-multiplication indices used in quaternionic triples:")
    idx_set = set()
    for (i, j, la, lb, Ja, Jb, Jc, nb) in triples_found:
        idx_set.add(la)
        idx_set.add(lb)
    print(f"    Indices: {sorted(idx_set)}")

    # Which sector are these indices in?
    oct_indices = [x for x in idx_set if x < 8]
    sed_indices = [x for x in idx_set if x >= 8]
    print(f"    Octonion sector (1-7): {sorted(oct_indices)}")
    print(f"    Sedenion sector (8-15): {sorted(sed_indices)}")

print("\n" + "="*70)
print("COMPUTATION COMPLETE")
print("="*70)
