#!/usr/bin/env python3
"""ICE ORCA DRAGON — IG-RUEQFT locality-fix cheapest oracle falsifier (2026-07-12).

Naesengmoon (wf_e71379d7-ed4) verdict on the claim "IG-RUEQFT's gauge group-averaging
ρ_A → ρ_A^G = (1/N)∫DU U ρ_A U† REPAIRS the non-locality of the entanglement term
(turns S_ent into a bulk LOCAL Lagrangian density)" = FAIL, load-bearing finding:
gauge-averaging acts on the gauge index only and PRESERVES the Casini-Huerta area law,
so S_inv stays surface-supported (non-local), not a bulk density ∫d^dx ℒ(φ,∂φ).

This script upgrades that JUDGMENT-lens argument to an ORACLE (exact computation) in a
concrete free (Gaussian) model, exactly as the cheapest falsifier prescribes.

DECISIVE METRIC (what a bulk LOCAL density would require):
  A bulk local density ℒ_ent(x) ⇒ S = ∫_A ℒ ⇒ S ∝ VOLUME(A) = L^d  (extensive).
  A non-local (area-law, entangling-surface) functional ⇒ S ∝ BOUNDARY(A) ~ L^{d-1}
  (for 2D free fermions, S ~ c·L·ln L — Gioev-Klich/Widom, log-enhanced area law).
  ⇒ test S_A / VOLUME  and  S_inv / VOLUME as L grows:
       → const  ⇒ bulk local density (claim PASSES, area law defeated)
       → 0      ⇒ still boundary/area-law (claim FAILS — non-locality preserved)

MODEL: 2D free fermion, square lattice N×N (torus), tight-binding H=-Σ_<ij> c_i†c_j,
Fermi sea (occupy ε(k)<0). Region A = L×L block. U(1) charge symmetry.
  S_A     = Σ_k H2(ν_k), ν_k = eigenvalues of the block correlation matrix C_A (Peschel).
  gauge-invariant / group-averaged (charge-dephased) entropy S_inv is EXACTLY bracketed:
       S_A ≤ S_inv ≤ S_A + H(P_A),   H(P_A) = Shannon entropy of the charge N_A in A
       (Poisson-binomial over the ν_k; charge superselection = the U(1) gauge-averaging,
        Casini-Huerta-Rosabal / Donnelly-Wall). Both bounds are computed exactly.
If BOTH S_A/L^2 → 0 and (S_A+H)/L^2 → 0, then S_inv/L^2 → 0 for the whole bracket ⇒
group-averaging cannot yield a bulk local density. Area law survives. Naesengmoon oracle-confirmed.
"""
import numpy as np
import json, hashlib, os

def H2(nu):
    nu = np.clip(nu, 1e-14, 1 - 1e-14)
    return -(nu * np.log(nu) + (1 - nu) * np.log1p(-nu))

def fermi_sea_corr(N):
    """C(dx,dy) = (1/N^2) Σ_{k: ε(k)<0} e^{i k·r}, ε(k) = -2(cos kx + cos ky)."""
    ks = 2 * np.pi * np.arange(N) / N
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    occ = (np.cos(KX) + np.cos(KY)) > 1e-12          # ε<0 strictly (exclude zero-modes)
    filling = occ.mean()
    # C(dx,dy) via inverse FFT of the occupation mask
    Cr = np.fft.ifft2(occ.astype(float))             # (1/N^2) Σ_k occ e^{-i k·r} = C(-r); real part symmetric
    return np.real(Cr), filling

def block_corr_matrix(Cr, L):
    """L×L block correlation matrix (L^2 × L^2), Toeplitz in each axis."""
    N = Cr.shape[0]
    coords = [(x, y) for x in range(L) for y in range(L)]
    n = len(coords)
    M = np.empty((n, n))
    for a, (x1, y1) in enumerate(coords):
        for b, (x2, y2) in enumerate(coords):
            M[a, b] = Cr[(x1 - x2) % N, (y1 - y2) % N]
    return M

def poisson_binomial_entropy(nu):
    """H of N_A = Σ_k Bernoulli(ν_k)  (each eigenmode occupied w.p. ν_k, independent)."""
    p = np.array([1.0])
    for v in np.clip(nu, 0, 1):
        p = np.convolve(p, [1 - v, v])
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))

def run(N=64, Ls=(4, 6, 8, 10, 12, 14, 16)):
    Cr, filling = fermi_sea_corr(N)
    rows = []
    for L in Ls:
        M = block_corr_matrix(Cr, L)
        nu = np.linalg.eigvalsh(M)                    # symmetric ⇒ real eigenvalues in [0,1]
        S_A = float(np.sum(H2(nu)))
        H_P = poisson_binomial_entropy(nu)            # charge-fluctuation entropy (gauge-avg addition)
        vol = L * L
        rows.append({
            "L": L, "volume_L2": vol,
            "S_A": S_A, "H_charge": H_P,
            "S_inv_lower(=S_A)": S_A, "S_inv_upper(=S_A+H)": S_A + H_P,
            "S_A_over_volume": S_A / vol,
            "S_inv_upper_over_volume": (S_A + H_P) / vol,
            "S_A_over_LlnL": S_A / (L * np.log(L)),   # area-law coefficient (should ~plateau)
        })
    return {"lattice_N": N, "filling": filling, "rows": rows}

if __name__ == "__main__":
    out = run()
    # verdict logic: bulk-local ⇔ S/volume → const; non-local ⇔ S/volume → 0
    r = out["rows"]
    vol_ratio_first, vol_ratio_last = r[0]["S_inv_upper_over_volume"], r[-1]["S_inv_upper_over_volume"]
    lnl_first, lnl_last = r[1]["S_A_over_LlnL"], r[-1]["S_A_over_LlnL"]  # skip L=4 (small)
    out["decisive"] = {
        "S_inv_upper_over_volume_trend": f"{vol_ratio_first:.4f} (L={r[0]['L']}) -> {vol_ratio_last:.4f} (L={r[-1]['L']})",
        "decreasing_toward_zero": bool(vol_ratio_last < vol_ratio_first * 0.75),
        "S_A_over_LlnL_plateau": f"{lnl_first:.4f} -> {lnl_last:.4f} (area-law coeff ~stable)",
        "verdict": None,
    }
    localized = vol_ratio_last > vol_ratio_first * 0.9   # would need ~constant ratio
    out["decisive"]["verdict"] = (
        "BULK_LOCAL_DENSITY (S∝volume) — claim would PASS" if localized else
        "NON_LOCAL area-law PRESERVED (S/volume→0, S~L·lnL) — group-averaging does NOT localize; "
        "IG-RUEQFT locality-fix claim FAILS at the oracle level, confirming the naesengmoon judgment verdict."
    )
    src = open(__file__).read()
    out["script_sha256"] = hashlib.sha256(src.encode()).hexdigest()
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RESULT.json")
    json.dump(out, open(p, "w"), indent=2)
    print(json.dumps(out, indent=2))
