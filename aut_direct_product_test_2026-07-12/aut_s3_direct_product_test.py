#!/usr/bin/env python3
"""ICE ORCA DRAGON — Aut(𝕊) direct-vs-semidirect decision test (2026-07-12).

Pre-registered (lakatotree ice-orca-dragon / tag aut_s3_direct_product_test):
  hard_core claims "Aut(𝕊) = G₂ × S₃" with × = DIRECT product.
  A direct product requires the outer S₃ = ⟨σ,Ψ⟩ to CENTRALIZE the G₂ = Aut(𝕆)
  subgroup, i.e. conjugation-by-σ and conjugation-by-Ψ act as the IDENTITY on the
  Lie algebra g₂ = Der(𝕊).

METHOD (avoids the REJECTED g2_octonion_inner_derivation_artifact category error:
  it does NOT transport the alternative-algebra derivation formula onto the
  non-alternative sedenions). Instead Der(𝕊) is computed DIRECTLY as the linear
  null-space of the derivation defining equation
        D(x·y) = D(x)·y + x·D(y)   for all basis x,y,
  solved over gl(16). Expected dim = 14 = dim g₂.

  Then conjugation-by-φ (φ ∈ {σ,Ψ}) restricted to Der(𝕊) is represented as a
  14×14 matrix A_φ in a fixed basis of Der(𝕊). DIRECT product ⟺ A_σ = A_Ψ = I.

NOVEL METRIC  s3_centralizes_g2_max_conj_matrix_minus_I_infnorm
             = max( ‖A_σ − I‖_∞ , ‖A_Ψ − I‖_∞ ).
  PREDICTION (direct): < 1e-9.
  FALSIFIER (semidirect): O(1) → hard_core "×" must become "⋊".

CONTROLS (discrimination, anti-numerology):
  (C1) normalizer residual: ‖ project(φ D φ⁻¹  out of span Der(𝕊)) ‖  — must be 0
       for genuine automorphisms σ,Ψ (theorem: Aut maps Der→Der). Confirms the
       computed Der(𝕊) and the automorphism property are consistent.
  (C2) a FAKE non-automorphism map F must FAIL to preserve Der(𝕊) (normalizer
       residual ≫ 0), proving the whole apparatus discriminates and is not a
       tautology that passes everything.

All numbers COMPUTED. σ (order 2) is an exact integer/rational matrix; Ψ (order 3)
uses √3 (float). Residuals are reported to full precision.
"""
import numpy as np
import json, hashlib, sys, os

np.set_printoptions(precision=3, suppress=True)

# ---------------------------------------------------------------------------
# 1. Cayley–Dickson tower  ℝ→ℂ→ℍ→𝕆→𝕊 : build 16×16 structure so that
#    e_i · e_j = sum_k T[i,j,k] e_k.  Convention: (a,b)(c,d)=(ac − d̄ b, d a + b c̄).
# ---------------------------------------------------------------------------
def cd_tables():
    # represent algebra elements at each level as real vectors; build mult + conj
    def double(mul, conj, n):
        # elements are pairs (a,b), a,b in R^n  -> R^{2n}
        def mul2(x, y):
            a, b = x[:n], x[n:]
            c, d = y[:n], y[n:]
            # ac - conj(d) b
            left = mul(a, c) - mul(conj(d), b)
            # d a + b conj(c)
            right = mul(d, a) + mul(b, conj(c))
            return np.concatenate([left, right])
        def conj2(x):
            a, b = x[:n], x[n:]
            return np.concatenate([conj(a), -b])
        return mul2, conj2, 2 * n
    # base: reals
    mul = lambda a, b: a * b
    conj = lambda a: a.copy()
    n = 1
    for _ in range(4):              # 1->2->4->8->16
        mul, conj, n = double(mul, conj, n)
    dim = n                          # 16
    e = np.eye(dim)
    T = np.zeros((dim, dim, dim))
    for i in range(dim):
        for j in range(dim):
            T[i, j] = mul(e[i], e[j])
    return T, dim

T, DIM = cd_tables()

def prod(x, y):
    """multiply two 16-vectors via structure tensor."""
    return np.einsum('i,j,ijk->k', x, y, T)

def Lmat(x):
    """left-multiplication matrix L_x : v -> x·v."""
    return np.einsum('i,ijk->kj', x, T)

def Rmat(y):
    """right-multiplication matrix R_y : v -> v·y."""
    return np.einsum('j,ijk->ki', y, T)

# sanity: e0 identity, e_i^2=-1 for i>=1, non-associative
e = np.eye(DIM)
assert np.allclose(prod(e[0], e[3]), e[3])
assert np.allclose(prod(e[5], e[5]), -e[0])
assoc = prod(prod(e[1] + e[10], e[1] + e[10]), e[4]) - prod(e[1] + e[10], prod(e[1] + e[10], e[4]))
non_associative = not np.allclose(assoc, 0)   # sedenions genuinely non-assoc
# octonion subalgebra e0..e7 alternative check
alt = prod(prod(e[1], e[1]), e[2]) - prod(e[1], prod(e[1], e[2]))
octonion_alternative = np.allclose(alt, 0)

# ---------------------------------------------------------------------------
# 2. Der(𝕊) as null-space of the derivation defining equation.
#    Unknown D is 16×16 (256 entries). For every ordered basis pair (i,j):
#        D(e_i·e_j) − D(e_i)·e_j − e_i·D(e_j) = 0   (a 16-vector, 16 eqns)
#    Row-assemble M (256*16 rows × 256 cols), null space = Der(𝕊).
# ---------------------------------------------------------------------------
def build_derivation_constraints():
    rows = []
    for i in range(DIM):
        for j in range(DIM):
            eij = prod(e[i], e[j])            # 16-vector = e_i e_j (basis-combo)
            # D(e_i e_j) = sum_p eij[p] * D[:,p]  -> linear in D entries (row a, col p)
            # D(e_i) e_j = R_{e_j} D e_i ; entry: (R_{e_j})[a,r] * D[r,i]
            # e_i D(e_j) = L_{e_i} D e_j ; entry: (L_{e_i})[a,r] * D[r,j]
            Rj = Rmat(e[j]); Li = Lmat(e[i])
            for a in range(DIM):              # 16 component equations
                row = np.zeros((DIM, DIM))    # coefficient on D[r,c]
                # + D(e_i e_j)_a = sum_p eij[p] D[a,p]
                row[a, :] += eij
                # - (D(e_i) e_j)_a = - sum_r Rj[a,r] D[r,i]
                row[:, i] -= Rj[a, :]
                # - (e_i D(e_j))_a = - sum_r Li[a,r] D[r,j]
                row[:, j] -= Li[a, :]
                rows.append(row.reshape(-1))
    return np.array(rows)

M = build_derivation_constraints()
# null space via SVD
U, s, Vt = np.linalg.svd(M, full_matrices=True)
tol = 1e-8 * s[0]
null_mask = s < tol if len(s) == Vt.shape[0] else np.r_[s, np.zeros(Vt.shape[0]-len(s))] < tol
# number of near-zero singular values among the 256 right-singular directions
sv_full = np.zeros(Vt.shape[0]); sv_full[:len(s)] = s
der_dim = int(np.sum(sv_full < tol))
der_basis_vecs = Vt[sv_full < tol]           # each is a flattened 16x16 derivation
DER = [v.reshape(DIM, DIM) for v in der_basis_vecs]

# verify each computed D really satisfies derivation law (independent recheck)
def is_derivation(D):
    worst = 0.0
    for i in range(DIM):
        for j in range(DIM):
            lhs = D @ prod(e[i], e[j])
            rhs = prod(D @ e[i], e[j]) + prod(e[i], D @ e[j])
            worst = max(worst, np.max(np.abs(lhs - rhs)))
    return worst
der_law_residual = max(is_derivation(D) for D in DER) if DER else float('nan')

# ---------------------------------------------------------------------------
# 3. The genuine outer S₃ = ⟨σ, Ψ⟩  (from avenue3 prereg, verified genuine Aut(𝕊)).
#    σ (ε, order 2): e_i↦e_i (i=1..7),  e_{i+8}↦−e_{i+8} (i=0..7)  [i.e. e8..e15 ↦ −]
#    Ψ (ψ, order 3): 2π/3 rotation in the seven e_i—e_{i+8} planes (i=1..7); e8↦e8.
#        ψ(e_i)=−½e_i+ (√3/2)e_{i+8},  ψ(e_{i+8})=−½e_{i+8} −(√3/2)e_i,  ψ(e8)=e8, e0 fixed.
# ---------------------------------------------------------------------------
def sigma_matrix():
    S = np.eye(DIM)
    for k in range(8, 16):       # e8..e15 -> -e_k
        S[k, k] = -1.0
    return S

def psi_matrix():
    P = np.zeros((DIM, DIM))
    P[0, 0] = 1.0                # e0 fixed
    P[8, 8] = 1.0                # e8 fixed
    c, sq = -0.5, np.sqrt(3) / 2
    for i in range(1, 8):        # e_i, e_{i+8}
        j = i + 8
        # ψ(e_i)=c e_i + sq e_j
        P[i, i] += c;  P[j, i] += sq
        # ψ(e_{i+8})=c e_j - sq e_i
        P[j, j] += c;  P[i, j] += -sq
    return P

SIG = sigma_matrix()
PSI = psi_matrix()

def is_automorphism(phi):
    worst = 0.0
    for i in range(DIM):
        for j in range(DIM):
            lhs = phi @ prod(e[i], e[j])
            rhs = prod(phi @ e[i], phi @ e[j])
            worst = max(worst, np.max(np.abs(lhs - rhs)))
    return worst

sigma_auto_res = is_automorphism(SIG)          # cross-check tree G1 (0/256)
psi_auto_res = is_automorphism(PSI)
sigma_order = None
Mp = np.eye(DIM)
for k in range(1, 8):
    Mp = Mp @ SIG
    if np.allclose(Mp, np.eye(DIM)): sigma_order = k; break
psi_order = None
Mp = np.eye(DIM)
for k in range(1, 8):
    Mp = Mp @ PSI
    if np.allclose(Mp, np.eye(DIM), atol=1e-9): psi_order = k; break

# ---------------------------------------------------------------------------
# 4. Conjugation action on Der(𝕊):  D -> φ D φ⁻¹.  Express in DER basis => A_φ.
#    Build via least-squares projection onto span(DER) (orthonormalize first).
# ---------------------------------------------------------------------------
# orthonormal basis B (14 vecs of length 256) from DER
Bmat = np.array([D.reshape(-1) for D in DER])          # (14,256)
# already orthonormal (rows of Vt), but re-orthonormalize defensively
Q, _ = np.linalg.qr(Bmat.T)                            # (256,14)
Q = Q[:, :der_dim]

def conj_action_matrix(phi):
    phinv = np.linalg.inv(phi)
    cols = []
    normalizer_res = 0.0
    for k in range(der_dim):
        D = Q[:, k].reshape(DIM, DIM)
        Dc = (phi @ D @ phinv).reshape(-1)             # φ D φ⁻¹  as 256-vec
        coeff = Q.T @ Dc                               # projection onto span
        recon = Q @ coeff
        normalizer_res = max(normalizer_res, np.max(np.abs(Dc - recon)))
        cols.append(coeff)
    A = np.array(cols).T                               # (14,14)
    return A, normalizer_res

A_sig, norm_res_sig = conj_action_matrix(SIG)
A_psi, norm_res_psi = conj_action_matrix(PSI)
I14 = np.eye(der_dim)
dev_sig = float(np.max(np.abs(A_sig - I14)))
dev_psi = float(np.max(np.abs(A_psi - I14)))
NOVEL_METRIC = max(dev_sig, dev_psi)

# ---------------------------------------------------------------------------
# 5. Control C2 — a FAKE non-automorphism must NOT preserve Der(𝕊).
# ---------------------------------------------------------------------------
def fake_matrix():
    F = np.eye(DIM)
    F[1, 2] = 0.7; F[2, 1] = -0.4; F[3, 5] = 0.9   # arbitrary, breaks multiplicativity
    return F
FAKE = fake_matrix()
fake_auto_res = is_automorphism(FAKE)              # should be large (not an auto)
_, fake_norm_res = conj_action_matrix(FAKE)        # should be large (moves Der out of span)

# ---------------------------------------------------------------------------
# 6. Verdict + receipt
# ---------------------------------------------------------------------------
direct_product = NOVEL_METRIC < 1e-9
report = {
    "test": "aut_s3_direct_product_test",
    "date": "2026-07-12",
    "sanity": {
        "sedenion_non_associative": bool(non_associative),
        "octonion_subalgebra_alternative": bool(octonion_alternative),
    },
    "der_S": {
        "dimension_computed": der_dim,
        "expected_g2_dim": 14,
        "dim_matches_g2": der_dim == 14,
        "singular_gap": {"sv_14th_smallest_kept": float(sorted(sv_full)[13]),
                          "sv_15th": float(sorted(sv_full)[14])},
        "derivation_law_recheck_residual": float(der_law_residual),
        "method": "direct null-space of D(xy)=D(x)y+xD(y); NO octonion-formula transport",
    },
    "S3_generators": {
        "sigma_order": sigma_order, "psi_order": psi_order,
        "sigma_automorphism_residual": float(sigma_auto_res),
        "psi_automorphism_residual": float(psi_auto_res),
    },
    "controls": {
        "C1_normalizer_residual_sigma": float(norm_res_sig),
        "C1_normalizer_residual_psi": float(norm_res_psi),
        "C2_fake_automorphism_residual": float(fake_auto_res),
        "C2_fake_normalizer_residual": float(fake_norm_res),
        "C2_discriminates": bool(fake_norm_res > 1e-6),
    },
    "NOVEL_METRIC_s3_centralizes_g2_max_conj_matrix_minus_I_infnorm": NOVEL_METRIC,
    "A_sigma_dev_from_I": dev_sig,
    "A_psi_dev_from_I": dev_psi,
    "prereg_threshold": 1e-9,
    "verdict": {
        "direct_product_confirmed": bool(direct_product),
        "structure": "G₂ × S₃ (DIRECT)" if direct_product else "G₂ ⋊ S₃ (SEMIDIRECT) — hard_core '×' would need '⋊'",
    },
}
src = open(__file__).read()
report["script_sha256"] = hashlib.sha256(src.encode()).hexdigest()

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RESULT.json")
json.dump(report, open(out_path, "w"), indent=2, ensure_ascii=False)
print(json.dumps(report, indent=2, ensure_ascii=False))
print("\nNOVEL_METRIC =", NOVEL_METRIC, "-> prereg PASS" if direct_product else "-> prereg FAIL (semidirect)")
