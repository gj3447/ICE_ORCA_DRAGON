# LONGINUS: sourceId=queue_04_hosotani_toy, sourcePath=queue_04_hosotani_toy.py
"""
Queue 4: Hosotani Mechanism Toy Model
======================================
G₂ 7-dim fundamental rep 상의 Wilson line holonomy 가 vacuum을 선택하는
메커니즘 demonstration.

Hosotani: V_eff(θ) = (1-loop) Σ_n c_n cos(n θ) with θ = Wilson line phase.
Minimum이 non-trivial θ_* 이면 SSB.

여기선 ICE-adapted toy version:
- 7 orbits → 7 Wilson line phases θ_1, ..., θ_7
- Fermion 1-loop 기여: V_f = Σ_k cos(θ_k) ((-1)^F로 repel)
- Bosonic 기여: V_b = -Σ_k cos(2 θ_k)
- Minimize → vacuum 선택
"""
import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=4, suppress=True)


def V_hosotani_toy(thetas, N_fermion=7, N_boson=1):
    """
    Simplified Hosotani effective potential.
    Thetas: 7-vector (G₂ Wilson line phases in fundamental rep).

    V = -Σ_n [N_fermion (-1)^n - N_boson] / n^4 * Σ_k cos(n θ_k)

    leading n=1 term: V ~ -(N_f - N_b) cos(θ_k)
    If N_f > N_b: minimum at θ_k = 0 (trivial)
    If N_f < N_b: minimum at θ_k = π (non-trivial SSB!)
    """
    # n=1 term (leading)
    V = 0.0
    for n in range(1, 5):
        coeff = ((-1)**n * N_fermion - N_boson) / (n**4)
        V -= coeff * np.sum(np.cos(n * thetas))
    return V


def break_degenerate_vacuum(thetas, epsilon=0.05):
    """
    Degenerate vacuum 허용 (symmetric minimum) 을 깨는 small perturbation.
    각 orbit에 다른 weight 부여하여 vacuum alignment.
    """
    # G₂ fundamental weights (6 short + 1 zero, conventional choice)
    # Use simple non-trivial structure: Gauss-like weight per orbit
    weights = np.array([1.0, 1.5, 2.0, 2.5, 1.2, 1.8, 0.8])
    return epsilon * np.sum(weights * np.cos(thetas))


def full_potential(thetas, N_f=3, N_b=1, epsilon=0.05):
    return V_hosotani_toy(thetas, N_f, N_b) + break_degenerate_vacuum(thetas, epsilon)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUEUE 4: HOSOTANI MECHANISM TOY MODEL")
    print("=" * 60 + "\n")

    print("Setup:")
    print("  - 7 Wilson line phases (G₂ fundamental rep)")
    print("  - Simplified 1-loop V_eff with fermion/boson contributions")
    print("  - Small symmetry-breaking perturbation to select unique vacuum")
    print()

    # Case 1: N_fermion > N_boson (trivial vacuum)
    print("[Case 1] N_fermion = 7 > N_boson = 1 (trivial symmetric vacuum 예상)")
    thetas_0 = np.zeros(7)
    V0 = V_hosotani_toy(thetas_0, N_fermion=7, N_boson=1)
    print(f"  V(θ = 0) = {V0:.4f}")
    thetas_pi = np.pi * np.ones(7)
    Vpi = V_hosotani_toy(thetas_pi, N_fermion=7, N_boson=1)
    print(f"  V(θ = π) = {Vpi:.4f}")
    print(f"  → 선호 vacuum: {'θ=0 (trivial)' if V0 < Vpi else 'θ=π (non-trivial)'}")
    print()

    # Case 2: N_fermion < N_boson (non-trivial SSB)
    print("[Case 2] N_fermion = 1 < N_boson = 3 (non-trivial vacuum 예상)")
    V0b = V_hosotani_toy(thetas_0, N_fermion=1, N_boson=3)
    Vpib = V_hosotani_toy(thetas_pi, N_fermion=1, N_boson=3)
    print(f"  V(θ = 0) = {V0b:.4f}")
    print(f"  V(θ = π) = {Vpib:.4f}")
    print(f"  → 선호 vacuum: {'θ=0' if V0b < Vpib else 'θ=π (SSB!)'}")
    print()

    # Case 3: Mixed + perturbation (realistic)
    print("[Case 3] Mixed + weight perturbation (ICE toy realistic)")
    # Try many random initial points, find minimum
    np.random.seed(42)
    best_V = np.inf
    best_theta = None
    all_minima = []

    for trial in range(30):
        x0 = np.random.uniform(-np.pi, np.pi, 7)
        res = minimize(full_potential, x0, args=(3, 1, 0.1),
                      method='BFGS')
        if res.success:
            all_minima.append((res.fun, res.x % (2 * np.pi)))
            if res.fun < best_V:
                best_V = res.fun
                best_theta = res.x % (2 * np.pi)

    print(f"  30회 랜덤 시작 중 최소값: V = {best_V:.4f}")
    print(f"  최소 vacuum θ = {best_theta}")
    print()

    # Vacuum alignment 판정
    # 7 phase 중 degenerate / non-degenerate
    unique_phases = np.round(np.sort(best_theta), 2)
    unique_count = len(set(unique_phases))
    print(f"  Vacuum의 distinct phases: {unique_count}")
    print(f"  phases: {unique_phases}")

    # Degenerate 깨짐 (= symmetry breaking) 있는지
    theta_spread = np.max(best_theta) - np.min(best_theta)
    print(f"  θ_max - θ_min = {theta_spread:.4f}")

    print()
    print("=" * 60)
    print("INTERPRETATION")
    print("=" * 60)
    if theta_spread < 0.1:
        print("  🔶 모든 θ_k 거의 같음 → G₂ symmetric vacuum")
        print("     (SSB 발생 안 함, boson/fermion balance 조정 필요)")
    elif unique_count <= 3:
        print(f"  🎯 {unique_count}개 distinct phase groups!")
        print(f"     G₂ → Subgroup 깨짐 (Hosotani 메커니즘 작동)")
        print(f"     Minimum이 단일 orbit 선택 가능성")
    else:
        print(f"  🔷 {unique_count} phases → 복잡 vacuum 구조")
        print(f"     full G₂ 깨짐 but 단순 1-orbit 선택 아님")

    print()
    print("  NOTE: 이건 toy model. 실제 ICE potential은:")
    print("    - FDA tower 전체 기여")
    print("    - 실제 fermion/gauge 구성")
    print("    - ICE coset Aut(𝕊)/stab 구조")
    print("  토이 결과는 mechanism 가능성 입증, 정량 결과 아님.")

    import json
    with open(__import__("pathlib").Path(__file__).resolve().parent / "queue_04_hosotani_results.json", "w") as f:
        json.dump({
            "case1_symmetric": {"V0": float(V0), "Vpi": float(Vpi)},
            "case2_ssb": {"V0": float(V0b), "Vpi": float(Vpib)},
            "case3_realistic": {
                "best_V": float(best_V),
                "best_theta": best_theta.tolist(),
                "unique_phases": [float(p) for p in unique_phases],
                "theta_spread": float(theta_spread),
                "distinct_phase_count": unique_count
            }
        }, f, indent=2, default=str)
    print(f"\nResults → queue_04_hosotani_results.json")
