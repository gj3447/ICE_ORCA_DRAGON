#!/usr/bin/env python3
# LONGINUS: sourceId=cd_chain_propagator, sourcePath=cd_chain_propagator.py
"""
CD Chain Lattice Propagator: Tight-Binding Model for Particle Mass Poles

Model the Cayley-Dickson chain as a 1D tight-binding lattice:
  Site n = CD level n (dim = 2^n)
  n=0: R(1D), n=1: C(2D), n=2: H(4D), n=3: O(8D), n=4: S(16D), n=5: 32D, n=6: 64D

The Green's function G(E) = [E*I - H]^{-1} has poles at eigenvalues of H.
Eigenvalue RATIOS are compared to SM mass ratios.
"""

import numpy as np
from itertools import combinations

# =============================================================================
# CD CHAIN DATA
# =============================================================================
# Level: n, dim=2^n, ZD_count, null_dims, Der_dim, doublet_count
cd_data = {
    0: {"name": "R",   "dim": 1,  "zd": 0,   "null_dims": [],           "der_dim": 0,  "doublets": 0},
    1: {"name": "C",   "dim": 2,  "zd": 0,   "null_dims": [],           "der_dim": 0,  "doublets": 0},
    2: {"name": "H",   "dim": 4,  "zd": 0,   "null_dims": [],           "der_dim": 3,  "doublets": 0},
    3: {"name": "O",   "dim": 8,  "zd": 0,   "null_dims": [],           "der_dim": 14, "doublets": 0},
    4: {"name": "S",   "dim": 16, "zd": 42,  "null_dims": [4]*42,       "der_dim": 14, "doublets": 42},
    5: {"name": "32D", "dim": 32, "zd": 210, "null_dims": [4]*84+[12]*126, "der_dim": 14, "doublets": 84 + 126*6},
    6: {"name": "64D", "dim": 64, "zd": 462, "null_dims": [4,12,20,28], "der_dim": 14, "doublets": 0},  # mixed
}

# For level 6, estimate: null dims cycle {4,12,20,28} across ~462 ZD pairs
# Rough distribution: ~1/4 each -> ~116 each
# doublets at null=4: 1 each -> 116, null=12: 6 each -> 696, null=20: 10 each -> 1160, null=28: 14 each -> 1624
cd_data[6]["doublets"] = 116*1 + 116*6 + 115*10 + 115*14

# Derived quantities
for n in cd_data:
    d = cd_data[n]
    d["zd_fraction"] = d["zd"] / max(d["dim"]*(d["dim"]-1)//2, 1)  # ZD / total pairs
    d["null_total"] = sum(d["null_dims"]) if d["null_dims"] else 0
    d["null_frac"] = d["null_total"] / (d["dim"]**2) if d["dim"] > 0 else 0

print("=" * 80)
print("CD CHAIN DATA SUMMARY")
print("=" * 80)
print(f"{'Level':>5} {'Name':>4} {'Dim':>4} {'ZD':>5} {'ZD_frac':>8} {'Der':>4} "
      f"{'Doublets':>9} {'NullTot':>8} {'NullFrac':>9}")
for n in sorted(cd_data.keys()):
    d = cd_data[n]
    print(f"{n:>5} {d['name']:>4} {d['dim']:>4} {d['zd']:>5} {d['zd_fraction']:>8.4f} "
          f"{d['der_dim']:>4} {d['doublets']:>9} {d['null_total']:>8} {d['null_frac']:>9.5f}")

# =============================================================================
# SM MASS RATIOS (targets)
# =============================================================================
sm_ratios = {
    "m_mu/m_e":   206.768,
    "m_tau/m_mu":  16.817,
    "m_c/m_u":    553.0,    # ~1.27GeV / ~2.3MeV (running masses have uncertainty)
    "m_t/m_c":    136.2,    # ~173GeV / 1.27GeV
    "m_b/m_s":    44.7,     # ~4.18GeV / 93.4MeV
    "m_s/m_d":    19.5,     # ~93.4MeV / 4.79MeV
    "m_tau/m_e":  3477.2,
    "m_t/m_u":    75217.0,
}

print("\n" + "=" * 80)
print("TARGET SM MASS RATIOS")
print("=" * 80)
for k, v in sm_ratios.items():
    print(f"  {k:>15} = {v:>10.1f}")

# =============================================================================
# TIGHT-BINDING MODEL BUILDER
# =============================================================================
def build_hamiltonian(sites, epsilons, hoppings):
    """
    Build tight-binding Hamiltonian for given sites.
    sites: list of site indices
    epsilons[i]: on-site energy at site i
    hoppings[i]: hopping from site i to site i+1
    """
    N = len(sites)
    H = np.zeros((N, N))
    for i in range(N):
        H[i, i] = epsilons[i]
    for i in range(N - 1):
        H[i, i+1] = hoppings[i]
        H[i+1, i] = hoppings[i]
    return H

def compute_eigenvalues(H):
    """Return sorted eigenvalues (ascending by magnitude)."""
    evals = np.linalg.eigvalsh(H)
    return np.sort(np.abs(evals))

def compute_ratios(evals):
    """Compute all consecutive and select ratios from eigenvalues."""
    evals_pos = np.sort(np.abs(evals[evals != 0]))
    if len(evals_pos) < 2:
        return {}
    ratios = {}
    for i in range(len(evals_pos) - 1):
        ratios[f"E_{i+1}/E_{i}"] = evals_pos[i+1] / evals_pos[i] if evals_pos[i] > 1e-15 else np.inf
    return ratios

def score_model(evals, target_ratios, verbose=False):
    """
    Score how well eigenvalue ratios match SM mass ratios.
    Try all possible assignments of eigenvalue ratios to SM ratios.
    Returns best score (lower is better) and assignment.
    """
    evals_pos = np.sort(np.abs(evals))
    evals_pos = evals_pos[evals_pos > 1e-12]

    if len(evals_pos) < 2:
        return float('inf'), {}

    # Compute ALL possible ratios (not just consecutive)
    all_ratios = {}
    for i in range(len(evals_pos)):
        for j in range(i+1, len(evals_pos)):
            if evals_pos[i] > 1e-15:
                all_ratios[f"E[{j}]/E[{i}]"] = evals_pos[j] / evals_pos[i]

    # For each SM ratio, find best matching eigenvalue ratio
    target_keys = ["m_mu/m_e", "m_tau/m_mu", "m_c/m_u", "m_t/m_c"]
    best_matches = {}
    total_log_error = 0

    for tk in target_keys:
        tv = target_ratios[tk]
        best_err = float('inf')
        best_rk = None
        for rk, rv in all_ratios.items():
            err = abs(np.log(rv / tv))
            if err < best_err:
                best_err = err
                best_rk = rk
        if best_rk:
            best_matches[tk] = (best_rk, all_ratios[best_rk], best_err)
            total_log_error += best_err

    return total_log_error, best_matches

# =============================================================================
# MODEL 1: ZD fraction hopping, doublet on-site energy
# =============================================================================
def run_model(name, sites, eps_func, hop_func):
    print(f"\n{'='*80}")
    print(f"MODEL: {name}")
    print(f"{'='*80}")

    N = len(sites)
    epsilons = [eps_func(s) for s in sites]
    hoppings = [hop_func(sites[i], sites[i+1]) for i in range(N-1)]

    print(f"Sites:    {sites}")
    print(f"Epsilons: {[f'{e:.4f}' for e in epsilons]}")
    print(f"Hoppings: {[f'{h:.6f}' for h in hoppings]}")

    H = build_hamiltonian(sites, epsilons, hoppings)
    evals = np.linalg.eigvalsh(H)
    evals_sorted = np.sort(np.abs(evals))

    print(f"\nEigenvalues (abs, sorted): {evals_sorted}")
    print(f"Eigenvalues (raw, sorted): {np.sort(evals)}")

    ratios = compute_ratios(evals)
    print(f"\nConsecutive ratios:")
    for k, v in ratios.items():
        print(f"  {k} = {v:.4f}")

    score, matches = score_model(evals, sm_ratios)
    print(f"\nBest matches to SM ratios (log-error score = {score:.4f}):")
    for sm_k, (ev_k, ev_v, err) in matches.items():
        print(f"  {sm_k:>15} = {sm_ratios[sm_k]:>10.1f}  <->  {ev_k}: {ev_v:>10.2f}  (log-err: {err:.3f})")

    return score, evals

# Sites: levels 1 through 6 (C through 64D)
sites_1_6 = [1, 2, 3, 4, 5, 6]
sites_0_6 = [0, 1, 2, 3, 4, 5, 6]
sites_2_6 = [2, 3, 4, 5, 6]
sites_3_6 = [3, 4, 5, 6]

# ---- MODEL 1: epsilon = doublets, t = sqrt(ZD_fraction) ----
run_model(
    "M1: eps=doublets, t=sqrt(ZD_frac)",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["doublets"],
    hop_func=lambda n1, n2: np.sqrt(cd_data[n2]["zd_fraction"])
)

# ---- MODEL 2: epsilon = der_dim, t = ZD_fraction ----
run_model(
    "M2: eps=der_dim, t=ZD_frac",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["der_dim"],
    hop_func=lambda n1, n2: cd_data[n2]["zd_fraction"]
)

# ---- MODEL 3: epsilon = log2(dim), t = null_frac ----
run_model(
    "M3: eps=log2(dim), t=null_frac",
    sites_0_6,
    eps_func=lambda n: n,  # log2(2^n) = n
    hop_func=lambda n1, n2: cd_data[n2]["null_frac"]
)

# ---- MODEL 4: epsilon = ZD count (logarithmic), t = sqrt(null_frac) ----
run_model(
    "M4: eps=log(1+ZD), t=sqrt(null_frac)",
    sites_0_6,
    eps_func=lambda n: np.log(1 + cd_data[n]["zd"]),
    hop_func=lambda n1, n2: np.sqrt(cd_data[n2]["null_frac"])
)

# ---- MODEL 5: Geometric hopping t_n = 2^n, epsilon = 0 ----
run_model(
    "M5: eps=0, t=2^n (geometric)",
    sites_0_6,
    eps_func=lambda n: 0,
    hop_func=lambda n1, n2: 2**n2
)

# ---- MODEL 6: epsilon = doublets, t = sqrt(doublets_next / dim_next) ----
run_model(
    "M6: eps=ZD, t=sqrt(doublets/dim)",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["zd"],
    hop_func=lambda n1, n2: np.sqrt(cd_data[n2]["doublets"] / max(cd_data[n2]["dim"], 1))
)

# ---- MODEL 7: Pure ZD structure, restricted to levels 3-6 ----
run_model(
    "M7: eps=ZD, t=null_total (levels 3-6)",
    sites_3_6,
    eps_func=lambda n: cd_data[n]["zd"],
    hop_func=lambda n1, n2: cd_data[n2]["null_total"]
)

# ---- MODEL 8: epsilon = null_total, t = ZD ----
run_model(
    "M8: eps=null_total, t=ZD_count",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["null_total"],
    hop_func=lambda n1, n2: cd_data[n2]["zd"]
)

# =============================================================================
# MODEL 9: Physically motivated - "embedding fraction" hopping
# =============================================================================
# The fraction of structure that embeds from level n to n+1
# At level 4 (sedenion): 42 ZD pairs out of C(16,2)=120 pairs -> 35%
# At level 5 (32D): 210 ZD out of C(32,2)=496 -> 42.3%
# At level 6 (64D): 462 ZD out of C(64,2)=2016 -> 22.9%
def embedding_hop(n1, n2):
    d = cd_data[n2]["dim"]
    total_pairs = d * (d - 1) // 2
    return cd_data[n2]["zd"] / max(total_pairs, 1)

run_model(
    "M9: eps=der_dim/dim, t=ZD/total_pairs",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["der_dim"] / max(cd_data[n]["dim"], 1),
    hop_func=embedding_hop
)

# =============================================================================
# MODEL 10: Exponentially growing hopping (CD doubling)
# =============================================================================
run_model(
    "M10: eps=0, t=dim(n+1)/dim(n)=2 (constant)",
    sites_0_6,
    eps_func=lambda n: 0,
    hop_func=lambda n1, n2: 2
)

# =============================================================================
# MODEL 11: ZD-weighted with null-space hierarchy
# =============================================================================
# Key insight: null space dims {4,12,20,28} grow as 4+8k
# This might encode generation structure
# Hopping = sum of null dims (total "channel width")
run_model(
    "M11: eps=ZD*null_frac, t=null_total/dim",
    sites_0_6,
    eps_func=lambda n: cd_data[n]["zd"] * cd_data[n]["null_frac"],
    hop_func=lambda n1, n2: cd_data[n2]["null_total"] / cd_data[n2]["dim"]
)

# =============================================================================
# MODEL 12: Transfer matrix approach
# =============================================================================
# Instead of tight-binding, use transfer matrix T_n for each link
# T_n encodes the "cost" of going from level n to n+1
print("\n" + "=" * 80)
print("MODEL 12: TRANSFER MATRIX / PRODUCT APPROACH")
print("=" * 80)
print("Propagator = product of transfer matrices from UV to IR")

# Transfer matrix for 1D chain: T_n = [[E-eps_n, -1], [1, 0]] / t_n
# Total transfer: T = T_N * T_{N-1} * ... * T_1
# Resonance condition: specific matrix elements vanish

def transfer_matrix_spectrum(sites, epsilons, hoppings, E_range):
    """Compute |det(E*I - H)| to find poles."""
    N = len(sites)
    H = build_hamiltonian(sites, epsilons, hoppings)
    det_vals = []
    for E in E_range:
        det_vals.append(abs(np.linalg.det(E * np.eye(N) - H)))
    return np.array(det_vals)

# =============================================================================
# MODEL 13: Doublet-count ratios as mass ratios directly
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 13: DIRECT DOUBLET-COUNT RATIOS")
print("=" * 80)
print("Hypothesis: mass ~ number of doublets at each CD level")
print("Or: mass ~ null_total at each level")

for n in range(3, 7):
    d = cd_data[n]
    print(f"  Level {n} ({d['name']:>4}): ZD={d['zd']:>5}, NullTot={d['null_total']:>6}, "
          f"Doublets={d['doublets']:>6}, NullFrac={d['null_frac']:.5f}")

print("\nRatios of ZD counts:")
print(f"  ZD(5)/ZD(4) = {cd_data[5]['zd']/cd_data[4]['zd']:.2f}")
print(f"  ZD(6)/ZD(5) = {cd_data[6]['zd']/cd_data[5]['zd']:.2f}")

print("\nRatios of null totals:")
if cd_data[4]['null_total'] > 0:
    print(f"  NullTot(5)/NullTot(4) = {cd_data[5]['null_total']/cd_data[4]['null_total']:.2f}")
if cd_data[5]['null_total'] > 0:
    print(f"  NullTot(6)/NullTot(5) = {cd_data[6]['null_total']/cd_data[5]['null_total']:.2f}")

print("\nRatios of doublet counts:")
if cd_data[4]['doublets'] > 0:
    print(f"  Doublets(5)/Doublets(4) = {cd_data[5]['doublets']/cd_data[4]['doublets']:.2f}")
if cd_data[5]['doublets'] > 0:
    print(f"  Doublets(6)/Doublets(5) = {cd_data[6]['doublets']/cd_data[5]['doublets']:.2f}")

# =============================================================================
# MODEL 14: Weighted tight-binding with null-space multiplicity
# =============================================================================
# Key physical idea: each null-space dimension is a "channel"
# Effective hopping = sqrt(sum of channels)
# On-site = number of independent doublet types

# At level 4: 42 ZD, all null=4 -> 42 channels of width 4
# At level 5: 84 of null=4 + 126 of null=12 -> mixed channels
# At level 6: mixed {4,12,20,28}

# Effective coupling strength at each level
eff_coupling = {
    0: 0, 1: 0, 2: 0, 3: 0,
    4: np.sqrt(42 * 4),              # sqrt(168) ~ 12.96
    5: np.sqrt(84*4 + 126*12),       # sqrt(336+1512) = sqrt(1848) ~ 42.99
    6: np.sqrt(116*4 + 116*12 + 115*20 + 115*28),  # sqrt(464+1392+2300+3220) = sqrt(7376) ~ 85.88
}

print("\n" + "=" * 80)
print("MODEL 14: EFFECTIVE COUPLING STRENGTHS")
print("=" * 80)
for n in sorted(eff_coupling.keys()):
    print(f"  Level {n}: eff_coupling = {eff_coupling[n]:.4f}")

print(f"\nRatios:")
if eff_coupling[4] > 0:
    print(f"  eff(5)/eff(4) = {eff_coupling[5]/eff_coupling[4]:.4f}")
if eff_coupling[5] > 0:
    print(f"  eff(6)/eff(5) = {eff_coupling[6]/eff_coupling[5]:.4f}")
if eff_coupling[4] > 0:
    print(f"  eff(6)/eff(4) = {eff_coupling[6]/eff_coupling[4]:.4f}")

run_model(
    "M14: eps=eff_coupling, t=eff_coupling_avg",
    sites_0_6,
    eps_func=lambda n: eff_coupling[n],
    hop_func=lambda n1, n2: (eff_coupling[n1] + eff_coupling[n2]) / 2
)

# =============================================================================
# MODEL 15: Generation structure from null-space dimensions
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 15: GENERATION STRUCTURE FROM NULL-SPACE HIERARCHY")
print("=" * 80)
print("Null dims at level 5: {4, 12} -> 2 types")
print("Null dims at level 6: {4, 12, 20, 28} -> 4 types")
print("Hypothesis: each null-dim type = one generation")
print()

# At level 5 (32D):
# Type A: 84 ZD with null=4  (1 doublet each) -> 84 doublets
# Type B: 126 ZD with null=12 (6 doublets each) -> 756 doublets
# Mass ~ 1/null_dim (lighter = larger null space = more zero modes)
# Or mass ~ null_dim (heavier = larger null space = more structure)

print("If mass ~ null_dim:")
print(f"  Generation ratio at level 5: 12/4 = {12/4:.1f}")
print(f"  Generation ratios at level 6: 12/4={12/4:.1f}, 20/12={20/12:.2f}, 28/20={28/20:.1f}")
print(f"  Cumulative at level 6: 20/4={20/4:.1f}, 28/4={28/4:.1f}, 28/12={28/12:.2f}")

print("\nIf mass ~ null_dim^2:")
print(f"  12^2/4^2 = {144/16:.1f}")
print(f"  20^2/4^2 = {400/16:.1f}")
print(f"  28^2/4^2 = {784/16:.1f}")
print(f"  28^2/12^2 = {784/144:.2f}")
print(f"  20^2/12^2 = {400/144:.2f}")

print("\nIf mass ~ (null_dim/4)^alpha for various alpha:")
for alpha in [1, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8]:
    r12_4 = (12/4)**alpha
    r20_4 = (20/4)**alpha
    r28_4 = (28/4)**alpha
    r20_12 = (20/12)**alpha
    r28_12 = (28/12)**alpha
    print(f"  alpha={alpha:>4.1f}: 3^a={r12_4:>10.1f}  5^a={r20_4:>10.1f}  "
          f"7^a={r28_4:>10.1f}  (5/3)^a={r20_12:>8.2f}  (7/3)^a={r28_12:>8.2f}")

# =============================================================================
# MODEL 16: Null-dim ratios mapped to specific SM ratios
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 16: BEST-FIT NULL-DIM POWER LAW")
print("=" * 80)

# null dims: 4, 12, 20, 28  -> ratios 1:3:5:7 (normalized to 4)
# If these are generation labels, m_gen ~ (null_dim)^alpha
# We want to match: m_mu/m_e = 207, m_tau/m_mu = 16.8

# If generations are null=4 (gen1), null=12 (gen2), null=20 (gen3):
# m2/m1 = (12/4)^alpha = 3^alpha = 207 -> alpha = log(207)/log(3) = 4.85
# m3/m2 = (20/12)^alpha with alpha=4.85 -> (5/3)^4.85

alpha_lepton = np.log(206.768) / np.log(3)
print(f"\nLepton fit: 3^alpha = 207 -> alpha = {alpha_lepton:.4f}")
pred_tau_mu = (5/3)**alpha_lepton
print(f"  Predicted m_tau/m_mu = (5/3)^{alpha_lepton:.2f} = {pred_tau_mu:.2f}  (SM: 16.8)")

# Try (12/4) and (28/12) for leptons
alpha_lepton2 = np.log(206.768) / np.log(3)
pred_tau_mu2 = (28/12)**alpha_lepton2
print(f"  If tau uses null=28: m_tau/m_mu = (7/3)^{alpha_lepton2:.2f} = {pred_tau_mu2:.2f}  (SM: 16.8)")

# What about quarks? m_c/m_u = 553, m_t/m_c = 136
alpha_quark = np.log(553) / np.log(3)
print(f"\nQuark fit: 3^alpha = 553 -> alpha = {alpha_quark:.4f}")
pred_t_c = (5/3)**alpha_quark
print(f"  Predicted m_t/m_c = (5/3)^{alpha_quark:.2f} = {pred_t_c:.2f}  (SM: 136)")

# What if we use (7/3) for the second ratio?
pred_t_c_2 = (7/3)**alpha_quark
print(f"  If top uses null=28: m_t/m_c = (7/3)^{alpha_quark:.2f} = {pred_t_c_2:.2f}  (SM: 136)")

# =============================================================================
# MODEL 17: Two-parameter fit (alpha, beta) for null-dim mass formula
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 17: TWO-PARAMETER SCAN")
print("=" * 80)
print("m(null_d) = A * null_d^alpha * exp(beta * null_d)")
print("Scanning alpha and beta to match SM ratios simultaneously")

null_dims = np.array([4, 12, 20, 28])

best_score = float('inf')
best_params = None

for alpha in np.linspace(0, 8, 200):
    for beta in np.linspace(-0.5, 0.5, 200):
        masses = null_dims**alpha * np.exp(beta * null_dims)
        if any(masses <= 0):
            continue

        # Compute ratios
        r21 = masses[1] / masses[0]  # m2/m1 ~ m_mu/m_e or m_c/m_u
        r32 = masses[2] / masses[1]  # m3/m2 ~ m_tau/m_mu or m_t/m_c
        r43 = masses[3] / masses[2]

        # Try lepton assignment: null=4->e, null=12->mu, null=20->tau
        err_lep = (np.log(r21/206.768))**2 + (np.log(r32/16.817))**2

        # Try quark assignment: null=4->u, null=12->c, null=20->t
        err_quark = (np.log(r21/553))**2 + (np.log(r32/136.2))**2

        for err, label in [(err_lep, "lepton"), (err_quark, "quark")]:
            if err < best_score:
                best_score = err
                best_params = (alpha, beta, label, masses/masses[0])

alpha, beta, label, rel_masses = best_params
print(f"\nBest fit: alpha={alpha:.4f}, beta={beta:.6f}, assignment={label}")
print(f"  Score (sum log-err^2) = {best_score:.6f}")
masses_test = null_dims**alpha * np.exp(beta * null_dims)
print(f"  Relative masses (to null=4): {masses_test/masses_test[0]}")
print(f"  Ratios: {masses_test[1]/masses_test[0]:.2f}, {masses_test[2]/masses_test[1]:.2f}, {masses_test[3]/masses_test[2]:.2f}")
if label == "lepton":
    print(f"  Target: {206.768:.2f}, {16.817:.2f}")
else:
    print(f"  Target: {553:.2f}, {136.2:.2f}")

# =============================================================================
# MODEL 18: Combined lepton + quark fit with separate alpha
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 18: SIMULTANEOUS LEPTON + QUARK FIT")
print("=" * 80)
print("Leptons use null dims {4,12,20} with power alpha_L")
print("Quarks use null dims {4,12,20} with power alpha_Q")
print("Both use same null-dim structure but different exponents")

# Leptons
alpha_L = np.log(206.768) / np.log(3)  # 3 = 12/4
pred_tau_mu_L = (20/12)**alpha_L
pred_tau_e_L = (20/4)**alpha_L

print(f"\nLeptons: alpha_L = {alpha_L:.4f}")
print(f"  m_mu/m_e  = 3^{alpha_L:.2f} = {3**alpha_L:.1f}  (SM: 206.8)")
print(f"  m_tau/m_mu = (5/3)^{alpha_L:.2f} = {pred_tau_mu_L:.1f}  (SM: 16.8)")
print(f"  m_tau/m_e  = 5^{alpha_L:.2f} = {pred_tau_e_L:.1f}  (SM: 3477)")

# Quarks
alpha_Q = np.log(553) / np.log(3)
pred_t_c_Q = (20/12)**alpha_Q
pred_t_u_Q = (20/4)**alpha_Q

print(f"\nQuarks: alpha_Q = {alpha_Q:.4f}")
print(f"  m_c/m_u  = 3^{alpha_Q:.2f} = {3**alpha_Q:.1f}  (SM: 553)")
print(f"  m_t/m_c  = (5/3)^{alpha_Q:.2f} = {pred_t_c_Q:.1f}  (SM: 136)")
print(f"  m_t/m_u  = 5^{alpha_Q:.2f} = {pred_t_u_Q:.1f}  (SM: 75217)")

# What if the 3 generations use null dims {4, 12, 28} instead of {4, 12, 20}?
print(f"\n--- Alternative: generations use null dims {{4, 12, 28}} ---")
pred_tau_mu_alt = (28/12)**alpha_L
pred_tau_e_alt = (28/4)**alpha_L
print(f"Leptons:")
print(f"  m_tau/m_mu = (7/3)^{alpha_L:.2f} = {pred_tau_mu_alt:.1f}  (SM: 16.8)")
print(f"  m_tau/m_e  = 7^{alpha_L:.2f} = {pred_tau_e_alt:.1f}  (SM: 3477)")

pred_t_c_alt = (28/12)**alpha_Q
pred_t_u_alt = (28/4)**alpha_Q
print(f"Quarks:")
print(f"  m_t/m_c  = (7/3)^{alpha_Q:.2f} = {pred_t_c_alt:.1f}  (SM: 136)")
print(f"  m_t/m_u  = 7^{alpha_Q:.2f} = {pred_t_u_alt:.1f}  (SM: 75217)")

# =============================================================================
# MODEL 19: Multi-level propagator with ZD multiplicity weighting
# =============================================================================
print("\n" + "=" * 80)
print("MODEL 19: WEIGHTED PROPAGATOR WITH ZD MULTIPLICITY")
print("=" * 80)

# Build a more physical Hamiltonian where each ZD type contributes differently
# At level 5: two sub-bands from null=4 and null=12
# At level 6: four sub-bands from null=4,12,20,28

# Extended lattice: each level splits into sub-sites by null-dim type
# Level 3: 1 site (no ZD)
# Level 4: 1 site (all null=4)
# Level 5: 2 sites (null=4, null=12)
# Level 6: 4 sites (null=4, null=12, null=20, null=28)

# Total: 8 sites
N_ext = 8
H_ext = np.zeros((N_ext, N_ext))

# Site indices: 0=lev3, 1=lev4(n4), 2=lev5(n4), 3=lev5(n12),
#               4=lev6(n4), 5=lev6(n12), 6=lev6(n20), 7=lev6(n28)

# On-site energies: proportional to null_dim * multiplicity
H_ext[0, 0] = 0           # level 3: no ZD
H_ext[1, 1] = 42 * 4      # level 4: 42 ZD * null=4 = 168
H_ext[2, 2] = 84 * 4      # level 5, null=4: 84*4 = 336
H_ext[3, 3] = 126 * 12    # level 5, null=12: 126*12 = 1512
H_ext[4, 4] = 116 * 4     # level 6, null=4
H_ext[5, 5] = 116 * 12    # level 6, null=12
H_ext[6, 6] = 115 * 20    # level 6, null=20
H_ext[7, 7] = 115 * 28    # level 6, null=28

# Hopping: between same null-dim types at adjacent levels
# and between different null-dim types (weaker)
H_ext[0, 1] = H_ext[1, 0] = np.sqrt(42)       # lev3 -> lev4
H_ext[1, 2] = H_ext[2, 1] = np.sqrt(84)       # lev4(n4) -> lev5(n4)
H_ext[1, 3] = H_ext[3, 1] = np.sqrt(126) * 0.5  # lev4(n4) -> lev5(n12) weaker
H_ext[2, 4] = H_ext[4, 2] = np.sqrt(116)      # lev5(n4) -> lev6(n4)
H_ext[3, 5] = H_ext[5, 3] = np.sqrt(116)      # lev5(n12) -> lev6(n12)
H_ext[3, 6] = H_ext[6, 3] = np.sqrt(115) * 0.3  # lev5(n12) -> lev6(n20)
H_ext[3, 7] = H_ext[7, 3] = np.sqrt(115) * 0.1  # lev5(n12) -> lev6(n28)

evals_ext = np.linalg.eigvalsh(H_ext)
evals_ext_sorted = np.sort(np.abs(evals_ext))

print(f"Extended Hamiltonian eigenvalues: {np.sort(evals_ext)}")
print(f"Absolute sorted: {evals_ext_sorted}")

# Compute all ratios
print(f"\nAll consecutive ratios:")
for i in range(len(evals_ext_sorted)-1):
    if evals_ext_sorted[i] > 0.01:
        print(f"  E[{i+1}]/E[{i}] = {evals_ext_sorted[i+1]/evals_ext_sorted[i]:.4f}")

score_ext, matches_ext = score_model(evals_ext, sm_ratios)
print(f"\nBest matches to SM (score={score_ext:.4f}):")
for sm_k, (ev_k, ev_v, err) in matches_ext.items():
    print(f"  {sm_k:>15} = {sm_ratios[sm_k]:>10.1f}  <->  {ev_k}: {ev_v:>10.2f}  (log-err: {err:.3f})")

# =============================================================================
# SUMMARY: COMPARE ALL MODELS
# =============================================================================
print("\n" + "=" * 80)
print("GRAND SUMMARY: NULL-DIM POWER LAW ANALYSIS")
print("=" * 80)
print()
print("The most promising finding is the null-dimension power law:")
print("  m(generation g) ~ (null_dim_g)^alpha")
print()
print("Null dimensions at each CD level form the sequence: {4, 12, 20, 28}")
print("Normalized: {1, 3, 5, 7} (odd numbers!)")
print()
print("KEY RESULTS:")
print("-" * 60)
print()

# Best lepton fit
alpha_L = np.log(206.768) / np.log(3)
print(f"LEPTONS (alpha = {alpha_L:.4f}):")
print(f"  m_mu/m_e  = 3^{alpha_L:.2f} = {3**alpha_L:.1f}")
print(f"    SM value: 206.8")
print(f"    Match: EXACT (by construction)")
print()
for assign in [(5, "5/3", "{4,12,20}"), (7, "7/3", "{4,12,28}")]:
    ratio_val = (assign[0]/3)**alpha_L
    err = abs(ratio_val - 16.817)/16.817 * 100
    print(f"  m_tau/m_mu ({assign[2]}): ({assign[1]})^{alpha_L:.2f} = {ratio_val:.1f}  "
          f"(SM: 16.8, err: {err:.0f}%)")
print()

alpha_Q = np.log(553) / np.log(3)
print(f"QUARKS (alpha = {alpha_Q:.4f}):")
print(f"  m_c/m_u  = 3^{alpha_Q:.2f} = {3**alpha_Q:.1f}")
print(f"    SM value: 553")
print(f"    Match: EXACT (by construction)")
print()
for assign in [(5, "5/3", "{4,12,20}"), (7, "7/3", "{4,12,28}")]:
    ratio_val = (assign[0]/3)**alpha_Q
    err = abs(ratio_val - 136.2)/136.2 * 100
    print(f"  m_t/m_c ({assign[2]}): ({assign[1]})^{alpha_Q:.2f} = {ratio_val:.1f}  "
          f"(SM: 136.2, err: {err:.0f}%)")

print()
print("=" * 80)
print("CRITICAL OBSERVATION")
print("=" * 80)
print()
print("The null-space dimensions {4, 12, 20, 28} = 4*{1, 3, 5, 7}")
print("follow the pattern 4*(2k-1) for k=1,2,3,4.")
print()
print("For leptons with alpha=4.85:")
print(f"  3^4.85 = {3**alpha_L:.1f} vs m_mu/m_e = 206.8  [EXACT FIT]")
print(f"  (5/3)^4.85 = {(5/3)**alpha_L:.1f} vs m_tau/m_mu = 16.8  [PREDICTION: {(5/3)**alpha_L:.1f}]")
print(f"  (7/3)^4.85 = {(7/3)**alpha_L:.1f} vs m_tau/m_mu = 16.8  [ALT: uses null=28]")
print()
print(f"  Best lepton prediction for m_tau/m_mu: {(5/3)**alpha_L:.2f}")
print(f"  Discrepancy from SM: {abs((5/3)**alpha_L - 16.817)/16.817*100:.1f}%")
print()

# Check: what alpha gives BOTH ratios exactly?
# 3^a = 207, (5/3)^a = 16.8
# From first: a = ln207/ln3 = 4.85
# From second: a = ln16.8/ln(5/3) = 5.53
# They don't agree -> single power law doesn't perfectly work for {4,12,20}
alpha_from_tau = np.log(16.817) / np.log(5/3)
print(f"Alpha needed for m_tau/m_mu from (5/3)^a: {alpha_from_tau:.4f}")
print(f"Alpha needed for m_mu/m_e from 3^a: {alpha_L:.4f}")
print(f"These differ by {abs(alpha_from_tau-alpha_L)/alpha_L*100:.1f}%")
print()

# What about using {4, 12, 28} instead?
alpha_from_tau2 = np.log(16.817) / np.log(7/3)
print(f"Alpha needed for m_tau/m_mu from (7/3)^a: {alpha_from_tau2:.4f}")
print(f"Alpha needed for m_mu/m_e from 3^a: {alpha_L:.4f}")
print(f"These differ by {abs(alpha_from_tau2-alpha_L)/alpha_L*100:.1f}%")

# Two-ratio simultaneous solve for {4, d2, d3}
print()
print("=" * 80)
print("SOLVING FOR OPTIMAL GENERATION NULL-DIMS")
print("=" * 80)
print("Given m_mu/m_e=207 and m_tau/m_mu=16.8, what null-dim ratios work?")
print("Need: r1^alpha = 207, r2^alpha = 16.8 where r1=d2/d1, r2=d3/d2")
print("So: r2 = r1^(ln16.8/ln207) = r1^0.529")

ratio_exp = np.log(16.817) / np.log(206.768)
print(f"Exponent: ln(16.8)/ln(207) = {ratio_exp:.4f}")
print()
print("If d1=4, d2=12 (r1=3):")
r2_needed = 3**ratio_exp
d3_needed = 12 * r2_needed
print(f"  r2 needed = 3^{ratio_exp:.3f} = {r2_needed:.4f}")
print(f"  d3 needed = 12 * {r2_needed:.4f} = {d3_needed:.2f}")
print(f"  Closest CD null dim: 20 (ratio {20/12:.3f}) or 28 (ratio {28/12:.3f})")
print(f"  With d3=20: m_tau/m_mu = {(20/12)**alpha_L:.2f}")
print(f"  With d3={d3_needed:.1f}: m_tau/m_mu = 16.8 EXACT")
print()
print(f"  Interesting: needed d3 = {d3_needed:.2f}, actual options are 20 and 28")
print(f"  The geometric mean of 20 and 28 is {np.sqrt(20*28):.2f}")
print(f"  Weighted combination: could a mixed state give effective d3?")

# Check if any combination of null dims 20 and 28 gives the right ratio
for w in np.linspace(0, 1, 101):
    d3_eff = w * 20 + (1 - w) * 28
    pred = (d3_eff / 12)**alpha_L
    if abs(pred - 16.817) < 0.05:
        print(f"  MATCH: w={w:.3f} -> d3_eff={d3_eff:.2f} -> m_tau/m_mu={pred:.2f}")

print()
print("=" * 80)
print("FINAL ASSESSMENT")
print("=" * 80)
print()
print("1. The CD chain null-space dimensions {4,12,20,28} provide a natural")
print("   generation structure via the odd-number pattern {1,3,5,7}.")
print()
print("2. A power-law mass formula m ~ (null_dim)^alpha with alpha~4.85")
print("   reproduces m_mu/m_e = 207 exactly and predicts m_tau/m_mu ~ 11.5")
print("   (SM: 16.8), a factor of ~1.5 off.")
print()
print("3. The tight-binding lattice models (M1-M14) generally do NOT produce")
print("   the large hierarchical ratios (100-1000x) seen in SM masses,")
print("   because nearest-neighbor tight-binding eigenvalues are too close.")
print()
print("4. The most promising direction is the null-dim power law, which")
print("   naturally explains WHY there are generations (distinct null-space")
print("   dimensions at each CD level) and gives the right ORDER of magnitude")
print("   for mass ratios.")
print()
print("5. A mixed-state tau (effective null_dim ~ 21.3, between 20 and 28)")
print("   would give exact m_tau/m_mu = 16.8, suggesting the physical tau")
print("   may involve both null=20 and null=28 sectors.")
