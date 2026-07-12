#!/usr/bin/env python3
"""Wilmot-Theta discrimination analysis: enumerate canonical 3-forms on Im(S)=R^15
and measure sigma/Psi/G2/random residuals for each. Reuses the CD machinery from
aut_s3_direct_product_test.py.  Two CD sign conventions tested.
"""
import numpy as np
np.set_printoptions(precision=4, suppress=True)

def cd_tables(sign_conj_left=1, sign_doubling=1):
    """Build 16x16x16 structure tensor for a CD convention.
    (a,b)(c,d) = ( a c - sign_conj_left * conj(d) b ,  sign_doubling*(d a) + b conj(c) )
    sign choices select distinct-but-valid conventions."""
    def double(mul, conj, n):
        def mul2(x, y):
            a, b = x[:n], x[n:]
            c, d = y[:n], y[n:]
            left = mul(a, c) - sign_conj_left * mul(conj(d), b)
            right = sign_doubling * mul(d, a) + mul(b, conj(c))
            return np.concatenate([left, right])
        def conj2(x):
            a, b = x[:n], x[n:]
            return np.concatenate([conj(a), -b])
        return mul2, conj2, 2 * n
    mul = lambda a, b: a * b
    conj = lambda a: a.copy()
    n = 1
    for _ in range(4):
        mul, conj, n = double(mul, conj, n)
    dim = n
    e = np.eye(dim)
    T = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            T[i, j] = mul(e[i], e[j])
    return T

def analyze(T, label):
    DIM = 16
    e = np.eye(DIM)
    def prod(x, y):
        return np.einsum('i,j,ijk->k', x, y, T)
    # sanity
    non_assoc = not np.allclose(prod(prod(e[1]+e[10], e[1]+e[10]), e[4]),
                                prod(e[1]+e[10], prod(e[1]+e[10], e[4])))
    alt = prod(prod(e[1], e[1]), e[2]) - prod(e[1], prod(e[1], e[2]))
    oct_alt = np.allclose(alt, 0)
    ei_sq = all(np.allclose(prod(e[i], e[i]), -e[0]) for i in range(1, 16))

    # ---- sigma, Psi (16x16) ----
    def sigma_matrix():
        S = np.eye(DIM)
        for k in range(8, 16):
            S[k, k] = -1.0
        return S
    def psi_matrix():
        P = np.zeros((DIM, DIM)); P[0, 0] = 1.0; P[8, 8] = 1.0
        c, sq = -0.5, np.sqrt(3)/2
        for i in range(1, 8):
            j = i + 8
            P[i, i] += c; P[j, i] += sq
            P[j, j] += c; P[i, j] += -sq
        return P
    SIG, PSI = sigma_matrix(), psi_matrix()

    def auto_res(phi):
        w = 0.0
        for i in range(DIM):
            for j in range(DIM):
                w = max(w, np.max(np.abs(phi @ prod(e[i], e[j]) - prod(phi @ e[i], phi @ e[j]))))
        return w
    sig_auto, psi_auto = auto_res(SIG), auto_res(PSI)

    # ---- inner product (standard basis is orthonormal for CD norm form) ----
    # metric = identity in this basis (e_i orthonormal). verify e_i . e_j = delta via norm.
    def ip(x, y):
        return float(np.dot(x, y))

    # ================= 3-FORM CANDIDATES on Im(S) (indices 1..15) =================
    IM = list(range(1, 16))

    # (i) phi_mult(x,y,z)=<x, y.z>  antisymmetrized over Im(S)
    Tm = np.zeros((16, 16, 16))
    for i in range(16):
        for j in range(16):
            for k in range(16):
                Tm[i, j, k] = ip(e[i], prod(e[j], e[k]))
    def alt3(A):
        # full antisymmetrization over 3 indices
        B = np.zeros_like(A)
        import itertools
        for p in itertools.permutations(range(3)):
            sign = 1
            # parity
            perm = list(p); s = 1
            for a in range(3):
                for b in range(a+1, 3):
                    if perm[a] > perm[b]: s = -s
            B += s * np.transpose(A, p)
        return B / 6.0
    PHI_MULT = alt3(Tm)
    # zero out real index 0 legs
    mask = np.ones((16,16,16))
    for ax in range(3):
        idx = [slice(None)]*3; idx[ax] = 0
        mask[tuple(idx)] = 0
    PHI_MULT = PHI_MULT * mask

    # (ii) phi_V : octonion associative calibration on span(e1..e7), extended by 0
    PHI_V = np.zeros((16, 16, 16))
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                PHI_V[i, j, k] = ip(e[i], prod(e[j], e[k]))
    # already antisymmetric on octonions; symmetrize-check then keep
    PHI_V = alt3(PHI_V)

    # (ii') phi_W : octonion calibration TRANSPORTED onto doubling block via the G2
    # partner map e_k <-> e_{k+8} (W =~ V as the 7-rep). Nonzero G2-invariant 3-form.
    PHI_W = np.zeros((16, 16, 16))
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                PHI_W[i+8, j+8, k+8] = ip(e[i], prod(e[j], e[k]))
    PHI_W = alt3(PHI_W)

    # (iii) phi_V + phi_W  (stabilizer exactly G2 candidate)
    PHI_VW = PHI_V + PHI_W

    # (iv) associator/non-composition 3-form D=Alt(<xy,z>-<x,yz>)
    Td = np.zeros((16, 16, 16))
    for i in range(16):
        for j in range(16):
            for k in range(16):
                Td[i, j, k] = ip(prod(e[i], e[j]), e[k]) - ip(e[i], prod(e[j], e[k]))
    PHI_ASSOC = alt3(Td) * mask

    forms = {"phi_mult(i)": PHI_MULT, "phi_V(ii)": PHI_V, "phi_W(ii')": PHI_W,
             "phi_V+phi_W(iii)": PHI_VW, "assoc_D(iv)": PHI_ASSOC}

    def pullback_res(Theta, M):
        Tp = np.einsum('ijk,ia,jb,kc->abc', Theta, M[:16,:16], M[:16,:16], M[:16,:16])
        return float(np.max(np.abs(Tp - Theta)))

    # ---- G2 positive control: exp of a Der(S) element ----
    def build_der():
        rows = []
        def Lmat(x): return np.einsum('i,ijk->kj', x, T)
        def Rmat(y): return np.einsum('j,ijk->ki', y, T)
        for i in range(16):
            for j in range(16):
                eij = prod(e[i], e[j]); Rj = Rmat(e[j]); Li = Lmat(e[i])
                for a in range(16):
                    row = np.zeros((16, 16)); row[a, :] += eij
                    row[:, i] -= Rj[a, :]; row[:, j] -= Li[a, :]
                    rows.append(row.reshape(-1))
        M = np.array(rows)
        U, s, Vt = np.linalg.svd(M, full_matrices=True)
        tol = 1e-8 * s[0]
        sv = np.zeros(Vt.shape[0]); sv[:len(s)] = s
        DER = [Vt[q].reshape(16, 16) for q in range(Vt.shape[0]) if sv[q] < tol]
        return DER
    DER = build_der()
    der_dim = len(DER)
    # exp via eigen/series
    try:
        from scipy.linalg import expm
    except Exception:
        def expm(A):
            R = np.eye(A.shape[0]); term = np.eye(A.shape[0])
            for nn in range(1, 30):
                term = term @ A / nn; R = R + term
            return R
    G2 = expm(0.37 * DER[0]) if der_dim > 0 else np.eye(16)
    g2_auto = auto_res(G2)

    rng = np.random.default_rng(7)
    Q, _ = np.linalg.qr(rng.standard_normal((16, 16)))  # random O(16); keep e0 fixed? no -> generic
    RAND = Q

    print(f"\n===== convention: {label} =====")
    print(f"  sanity: non_assoc={non_assoc} oct_alt={oct_alt} ei^2=-1:{ei_sq}")
    print(f"  sigma_auto_res={sig_auto:.2e}  psi_auto_res={psi_auto:.2e}  g2_auto_res={g2_auto:.2e}  der_dim={der_dim}")
    print(f"  {'form':<18}{'sigma':>12}{'Psi':>12}{'G2':>12}{'random':>12}   auto_preserved? discriminates?")
    results = {}
    for name, Th in forms.items():
        rs = pullback_res(Th, SIG); rp = pullback_res(Th, PSI)
        rg = pullback_res(Th, G2); rr = pullback_res(Th, RAND)
        nrm = float(np.max(np.abs(Th)))
        results[name] = (rs, rp, rg, rr, nrm)
        auto = (rs < 1e-9 and rp < 1e-9)
        disc = (rp > 1e-6 or rs > 1e-6)
        print(f"  {name:<18}{rs:>12.2e}{rp:>12.2e}{rg:>12.2e}{rr:>12.2e}   auto={auto!s:<6} disc={disc}")
    return results

TA = cd_tables(1, 1)
analyze(TA, "A_(ac-conj(d)b, da+b conj(c))  [Baez]")
# convention B = opposite algebra of A (x*_B y = y*_A x): a DISTINCT valid CD
# convention; sigma,Psi,G2 remain automorphisms of A^op iff of A.
TB = np.transpose(TA, (1, 0, 2))
analyze(TB, "B_opposite-algebra (y*_A x)")
