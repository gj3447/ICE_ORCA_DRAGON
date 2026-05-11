# LONGINUS: sourceId=queue_05_coleman_weinberg, sourcePath=queue_05_coleman_weinberg.py
"""
Queue 5: Coleman-Weinberg 1-loop Potential Generation
======================================================
V_1loop(φ) = (1/64π²) Σ_i (-1)^{F_i} m_i(φ)⁴ log(m_i²/Λ²)

ICE setup:
- Higgs field φ (Hermitian scalar on ZD pair null space)
- Fermion 입자: M_f(φ) = y_f φ (Yukawa-like)
- Gauge boson: M_V(φ) = g φ

With proper (n_f, n_b) balance, V_eff develops minimum at non-zero φ.
"""
import numpy as np
from scipy.optimize import minimize_scalar, minimize

np.set_printoptions(precision=4, suppress=True)


def CW_potential(phi, n_fermion=6, n_boson=3, y_f=1.0, g=1.0, Lambda=1.0):
    """
    Coleman-Weinberg effective potential.
    φ: Higgs VEV (real positive for simplicity)
    n_fermion, n_boson: 유효 degrees of freedom
    y_f: fermion Yukawa coupling
    g: gauge coupling
    Lambda: RG scale
    """
    if phi <= 0:
        return 0.0  # tree level at origin, 1-loop contribution vanishes

    # Fermion contribution (negative for Dirac fermion, even power)
    m_f2 = (y_f * phi) ** 2
    V_fermion = -n_fermion * m_f2**2 / (64 * np.pi**2) * (
        np.log(m_f2 / Lambda**2 + 1e-30) - 1.5
    )

    # Boson contribution (positive)
    m_b2 = (g * phi) ** 2
    V_boson = n_boson * m_b2**2 / (64 * np.pi**2) * (
        np.log(m_b2 / Lambda**2 + 1e-30) - 1.5
    )

    return V_fermion + V_boson


def scan_minimum(n_f, n_b, y_f=1.0, g=1.0, Lambda=1.0):
    """φ > 0 에서 V(φ) 최솟값 scan"""
    phis = np.linspace(0.01, 5.0, 500)
    V_vals = [CW_potential(p, n_f, n_b, y_f, g, Lambda) for p in phis]
    min_idx = np.argmin(V_vals)
    return phis[min_idx], V_vals[min_idx], phis, V_vals


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 5: COLEMAN-WEINBERG POTENTIAL GENERATION")
    print("=" * 60 + "\n")

    print("1-loop V_eff(φ) = (1/64π²) Σ (-1)^F m⁴ [log(m²/Λ²) - 3/2]")
    print()

    # Scenario: ICE inspired
    # 7 fermion-like (from G₂ fundamental), 3 gauge boson (Higgs doublet 4DoF - 1 massless)
    scenarios = [
        {"n_f": 3, "n_b": 4, "label": "SM-like (3 gen × 1 → 3 fermion, 4 EW boson)"},
        {"n_f": 6, "n_b": 3, "label": "ICE orbit-like (6 eaten, 3 gauge)"},
        {"n_f": 7, "n_b": 3, "label": "G₂ fundamental fermion (7 f, 3 b)"},
        {"n_f": 1, "n_b": 3, "label": "Reverse: 1 f, 3 b → SSB"},
    ]

    results = {}
    for sc in scenarios:
        nf, nb = sc["n_f"], sc["n_b"]
        phi_min, V_min, phis, Vs = scan_minimum(nf, nb)
        print(f"[Scenario] {sc['label']}")
        print(f"  (n_f={nf}, n_b={nb})")
        print(f"  φ_min = {phi_min:.4f}")
        print(f"  V(φ_min) = {V_min:.6e}")
        print(f"  V(0) = {CW_potential(0.001, nf, nb):.6e}")

        # SSB 여부 판정
        if V_min < -1e-4:
            print(f"  → ✅ SSB! φ_min > 0 (non-trivial vacuum)")
        elif abs(V_min) < 1e-4:
            print(f"  → ⚠️ 거의 flat")
        else:
            print(f"  → ❌ V(φ_min) ≥ V(0), trivial vacuum")
        print()

        results[sc["label"]] = {
            "n_f": nf, "n_b": nb,
            "phi_min": float(phi_min),
            "V_min": float(V_min),
            "ssb": V_min < -1e-4
        }

    # Critical analysis: SSB 조건
    print("[Analytical Check] SSB 조건 derivation")
    print("  CW 1-loop: V''(0) ~ (n_f y_f² - n_b g²)")
    print("  μ²_eff < 0 필요 (즉 n_f y_f² > n_b g²)")
    print()

    for n_f, n_b in [(3, 4), (6, 3), (7, 3), (1, 3)]:
        delta = n_f - n_b  # simple case y_f = g = 1
        print(f"  (n_f={n_f}, n_b={n_b}): n_f - n_b = {delta} "
              f"{'→ SSB 조건 충족' if delta > 0 else '→ trivial'}")
    print()

    # ICE specific: find optimal (n_f, n_b) combinations
    print("[ICE-specific] 7-orbit structure에 맞는 (n_f, n_b)")
    print("  Higgs 1개 = 1 orbit 선택 → 6 orbit eaten + 1 survives")
    print("  → 1 massive fermion (Higgs-eaten GS 6개)")
    print("  → 3 gauge boson (W±, Z analog) from SU(2)×U(1) breaking")
    print("  → 7 fermion from G₂ fundamental as matter content")
    print()

    # visualize
    print("[Plot data] 주 scenario의 V(φ) 곡선")
    nf, nb = 7, 3
    phis = np.linspace(0.01, 3.0, 50)
    Vs = [CW_potential(p, nf, nb) for p in phis]
    import itertools
    print(f"  (n_f={nf}, n_b={nb})")
    for p, V in zip(phis[::10], Vs[::10]):
        print(f"    φ={p:.2f}: V={V:.4e}")

    import json
    with open("/Users/lagyeongjun/CD/AGENT/queue_05_cw_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("=" * 60)
    print("VERDICT")
    print("=" * 60)
    any_ssb = any(r["ssb"] for r in results.values())
    if any_ssb:
        best = max(results.items(), key=lambda x: -x[1]["V_min"])
        print(f"  ✅ CW SSB 생성 확인!")
        print(f"  Best: {best[0]}")
        print(f"      φ_VEV = {best[1]['phi_min']:.4f} (scale × Λ)")
        print(f"      → V_eff potential 자연 생성 → Higgs μ², λ 유도 가능")
    else:
        print(f"  ⚠️ 현재 parameter에서 SSB 안됨")
    print(f"\nResults → queue_05_cw_results.json")
