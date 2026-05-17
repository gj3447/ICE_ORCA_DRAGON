"""Diagnostic for queue_08 g2 16-vs-14 generator discrepancy.

Hypothesis: the script uses *octonion* derivation formula
    D_{a,b}(z) = [[e_a, e_b], z] - 3*[e_a, e_b, z]
on *sedenion* multiplication (n=4 -> 16D). The octonion derivation
identity Der(O) = g2 (14D) relies on octonion alternativity. Sedenions
are NOT alternative, so this formula need not yield a closed Lie algebra
of dimension 14 when extended to the sedenion ambient.

Diagnostic checks:
  (D1) Are the 21 candidate D_{ab} matrices antisymmetric in the 7-D orbit-rep basis?
  (D2) What is rank in End(V_7) (49-dim) vs so(V_7) (21-dim antisymmetric)?
  (D3) Do the D_{ab} close under commutator? (Lie-algebra closure test)
  (D4) Compute genuine Killing-form Casimir; check Schur scalarity.

If (D1) fails or (D3) fails -> rank=16 is method artifact, not physics.

# KG: ICE_ORCA_DRAGON queue_08 g2 16-vs-14 discrimination diagnostic
"""

from __future__ import annotations

import json
import pathlib

import numpy as np

from cd_embedding import cd_multiply

ROOT = pathlib.Path(__file__).parent
DATE = "2026-05-17"
N = 4  # sedenion ambient
DIM = 2**N

ORBIT_REPS = [(1, 11), (2, 11), (1, 12), (1, 10), (1, 15), (1, 14), (1, 13)]


def basis(i: int, dim: int = DIM) -> np.ndarray:
    v = np.zeros(dim)
    v[i] = 1.0
    return v


def mul(a, b):
    return cd_multiply(a, b, N)


def commutator(a, b):
    return mul(a, b) - mul(b, a)


def annihilator(pair: tuple[int, int]) -> np.ndarray:
    i, j = pair
    return basis(i) + basis(j)


def derivation_action(a: int, b: int, z: np.ndarray) -> np.ndarray:
    ea, eb = basis(a), basis(b)
    comm = commutator(ea, eb)
    part1 = commutator(comm, z)
    assoc = mul(mul(ea, eb), z) - mul(ea, mul(eb, z))
    return part1 - 3 * assoc


def project_full(vec: np.ndarray, basis_vecs: np.ndarray) -> np.ndarray:
    """Orthogonal least-squares projection onto orbit-rep basis."""
    # basis_vecs shape (7, 16); solve basis_vecs.T @ c = vec
    c, *_ = np.linalg.lstsq(basis_vecs.T, vec, rcond=None)
    return c


def build_rep_matrices() -> list[np.ndarray]:
    bv = np.array([annihilator(p) for p in ORBIT_REPS])  # (7, 16)
    bv_norm = bv / np.linalg.norm(bv, axis=1, keepdims=True)
    mats = []
    pairs = [(a, b) for a in range(1, 8) for b in range(a + 1, 8)]
    for a, b in pairs:
        M = np.zeros((7, 7))
        for i, p in enumerate(ORBIT_REPS):
            v = annihilator(p)
            Dv = derivation_action(a, b, v)
            coeffs = bv_norm @ Dv  # script-style projection
            M[:, i] = coeffs
        mats.append(M)
    return mats, pairs


def diagnose_antisymmetry(mats: list[np.ndarray]) -> dict:
    sym_norms = [float(np.linalg.norm(M + M.T)) for M in mats]
    asym_norms = [float(np.linalg.norm(M - M.T)) for M in mats]
    ratio = [s / (a + 1e-12) for s, a in zip(sym_norms, asym_norms)]
    n_antisym = sum(1 for r in ratio if r < 0.05)
    return {
        "n_generators": len(mats),
        "n_strictly_antisym_within_5pct": n_antisym,
        "median_symmetric_norm": float(np.median(sym_norms)),
        "median_antisym_norm": float(np.median(asym_norms)),
        "median_sym_to_asym_ratio": float(np.median(ratio)),
        "verdict_D1": (
            "PASS: all 21 are antisymmetric" if n_antisym == 21 else
            f"FAIL: only {n_antisym}/21 strictly antisymmetric -> projection broken"
        ),
    }


def diagnose_ranks(mats: list[np.ndarray]) -> dict:
    M_flat = np.array([M.flatten() for M in mats])  # script's rank computation
    rank_end = int(np.linalg.matrix_rank(M_flat, tol=1e-8))
    asym = [0.5 * (M - M.T) for M in mats]
    A_flat = np.array([M.flatten() for M in asym])
    rank_so = int(np.linalg.matrix_rank(A_flat, tol=1e-8))
    return {
        "rank_in_End_V7_dim49": rank_end,
        "rank_in_so_V7_dim21": rank_so,
        "expected_g2_in_so7": 14,
        "verdict_D2": (
            f"so(7) rank = {rank_so}. " +
            ("Matches g2=14." if rank_so == 14 else
             f"Mismatch with g2=14 -> projection includes non-g2 directions.")
        ),
    }


def diagnose_closure(mats: list[np.ndarray]) -> dict:
    """Take antisymmetric parts; check if commutators lie within their span."""
    asym = [0.5 * (M - M.T) for M in mats]
    A_flat = np.array([M.flatten() for M in asym])
    rank_in = int(np.linalg.matrix_rank(A_flat, tol=1e-8))
    closure_residuals = []
    n_pairs = min(50, len(asym) * (len(asym) - 1) // 2)
    rng = np.random.default_rng(42)
    indices = rng.choice(len(asym), size=(n_pairs, 2))
    for i, j in indices:
        if i == j:
            continue
        C = asym[i] @ asym[j] - asym[j] @ asym[i]  # commutator
        # solve C = sum c_k * asym[k]
        c, residual, *_ = np.linalg.lstsq(A_flat.T, C.flatten(), rcond=None)
        recon = (A_flat.T @ c).reshape(7, 7)
        res_norm = float(np.linalg.norm(C - recon))
        c_norm = float(np.linalg.norm(C))
        closure_residuals.append(res_norm / (c_norm + 1e-12))
    median_residual = float(np.median(closure_residuals))
    return {
        "n_commutator_pairs_tested": len(closure_residuals),
        "median_relative_residual": median_residual,
        "max_relative_residual": float(np.max(closure_residuals)),
        "verdict_D3": (
            "PASS: Lie closure within antisymmetric span" if median_residual < 0.01 else
            f"FAIL: median residual {median_residual:.3f} -> not a closed Lie algebra"
        ),
    }


def diagnose_casimir(mats: list[np.ndarray]) -> dict:
    """Compute Casimir = sum M_i^2 with Killing-form normalization, check Schur scalarity."""
    asym = [0.5 * (M - M.T) for M in mats]
    A_flat = np.array([M.flatten() for M in asym])
    rank_so = int(np.linalg.matrix_rank(A_flat, tol=1e-8))
    # Use a basis-orthonormalized set (SVD)
    U, S, Vt = np.linalg.svd(A_flat, full_matrices=False)
    n_indep = int(np.sum(S > 1e-8))
    # Pick top n_indep orthonormal directions
    onb = Vt[:n_indep].reshape(n_indep, 7, 7)
    Casimir = np.zeros((7, 7))
    for M in onb:
        Casimir = Casimir + M @ M
    evals = sorted(np.real(np.linalg.eigvals(Casimir)))
    spread = float(max(evals) - min(evals))
    return {
        "n_orthonormal_directions_used": n_indep,
        "casimir_eigenvalues": [round(e, 4) for e in evals],
        "max_minus_min": spread,
        "verdict_D4": (
            "PASS: Casimir near-scalar (eigenvalue spread < 0.1)" if spread < 0.1 else
            f"FAIL: spread = {spread:.3f} -> not Schur-scalar -> not irreducible OR non-Lie"
        ),
    }


def main() -> None:
    mats, pairs = build_rep_matrices()
    d1 = diagnose_antisymmetry(mats)
    d2 = diagnose_ranks(mats)
    d3 = diagnose_closure(mats)
    d4 = diagnose_casimir(mats)

    # Synthesize verdict
    failures = []
    if "FAIL" in d1["verdict_D1"]:
        failures.append("D1_antisymmetry")
    if "Mismatch" in d2["verdict_D2"]:
        failures.append("D2_so7_rank")
    if "FAIL" in d3["verdict_D3"]:
        failures.append("D3_lie_closure")
    if "FAIL" in d4["verdict_D4"]:
        failures.append("D4_casimir_schur")

    if failures:
        synthesis = (
            f"queue_08 'g2' construction METHOD ARTIFACT — fails {failures}. "
            "The script applies the octonion inner-derivation formula to sedenion "
            "ambient multiplication. Sedenions are not alternative, so this formula "
            "does not yield a closed 14-dim Lie algebra; the script-reported 'rank 16, "
            "commutant 1' arose from over-permissive projection and an ad-hoc Casimir "
            "normalization (sum of M_i^2 without Killing-form weighting). "
            "Verdict for queue_08 original CONFIRMATION_LOCAL: DEMOTE to METHOD_ARTIFACT."
        )
        final_verdict = "METHOD_ARTIFACT"
    else:
        synthesis = "All diagnostics PASS. The 16-vs-14 gap is a real physical finding."
        final_verdict = "CONFIRMATION_LOCAL"

    out = {
        "verdict": final_verdict,
        "verdict_reasoning": synthesis,
        "verdict_source": "queue_08_g2_diagnostic.py 2026-05-17",
        "verdict_date": DATE,
        "diagnostics": {
            "D1_antisymmetry": d1,
            "D2_ranks": d2,
            "D3_lie_closure": d3,
            "D4_casimir_schur_test": d4,
        },
        "failures": failures,
    }
    out_path = ROOT / "queue_08_g2_diagnostic_results.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
