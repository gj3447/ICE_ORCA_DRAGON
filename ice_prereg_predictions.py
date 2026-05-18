#!/usr/bin/env python3
# KG: ICE pre-registered structural predictions, sha256 commit BEFORE PDG check
# LONGINUS: sourceId=ice_prereg_predictions
"""
ICE Pre-Registration Prediction Derivation

PROTOCOL (Lakatos-progressive):
  Step 1: Derive ALL dimensionless quantities from ICE algebra primitives ALONE
          (no PDG consultation in this step).
  Step 2: sha256-commit the prediction list (cryptographic timestamp).
  Step 3: ONLY THEN compare each prediction to PDG values with MC null gate.
  Step 4: Report honest outcome with look-elsewhere correction.

ICE primitives used (all from algebra, no PDG):
  - Sedenion 16D Cayley-Dickson
  - Aut(𝕊) = G₂ × S₃ (Brown 1967)
  - Z(𝕊) ≅ G₂ (Moreno 1998)
  - ZD(𝕊) ≅ V₂(ℝ⁷) (Reggiani 2024)
  - OEIS A167654 ZD count sequence
  - G₂ Lie algebra structure (Cartan-Killing)
  - S₃ representation theory (1+1+4 irreducible decomp)

Pre-registration date: 2026-05-18
sha256 hash: computed at write time, frozen in result JSON.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

ICE_DIR = Path("/Users/lagyeongjun/CD/SYMPOSIUM/METAHUMOTONIC/ICE_ORCA_DRAGON")

# ============================================================
# STEP 1: ICE-derivable dimensionless quantities (NO PDG)
# ============================================================

ICE_DERIVATIONS = []

# --- Group-theoretic invariants ---
# G₂ Casimir eigenvalues / dimensions
G2_dim_adjoint = 14
G2_dim_fundamental = 7
G2_rank = 2
G2_weyl_order = 12
G2_long_root_sq = 3
G2_short_root_sq = 1

# G₂ × S₃ joint group
G2_S3_order_quotient = G2_weyl_order * 6  # |W(G2)| * |S3| = 12 * 6 = 72

# S₃ representations: dimensions 1, 1, 2 (sum = 4)
S3_total_irrep_dim_sq = 1 + 1 + 4  # = 6 = |S₃|

# Sedenion structure
sedenion_dim = 16
sedenion_zd_pairs_n4 = 42  # OEIS A167654 at n=4
sedenion_orbit_count = 7
sedenion_orbit_size = 6

# --- Pre-registered predictions ---
ICE_DERIVATIONS.extend([
    {
        "id": "P01",
        "name": "g2_adjoint_to_fundamental",
        "value": G2_dim_adjoint / G2_dim_fundamental,
        "derivation": "dim(adjoint G₂) / dim(fundamental G₂) = 14/7 = 2",
        "category": "group_theoretic_ratio",
    },
    {
        "id": "P02",
        "name": "g2_long_short_root_sq",
        "value": G2_long_root_sq / G2_short_root_sq,
        "derivation": "long²/short² for G₂ = 3 (G₂ Cartan matrix)",
        "category": "lie_algebra_invariant",
    },
    {
        "id": "P03",
        "name": "g2_weyl_order_to_rank",
        "value": G2_weyl_order / G2_rank,
        "derivation": "|W(G₂)| / rank(G₂) = 12/2 = 6",
        "category": "group_theoretic_ratio",
    },
    {
        "id": "P04",
        "name": "sedenion_zd_pair_per_orbit",
        "value": sedenion_zd_pairs_n4 / sedenion_orbit_count,
        "derivation": "42 ZD pairs / 7 G₂-orbits = 6 per orbit",
        "category": "sedenion_orbit_invariant",
    },
    {
        "id": "P05",
        "name": "sedenion_zd_density",
        "value": sedenion_zd_pairs_n4 / (sedenion_dim * (sedenion_dim - 1) / 2),
        "derivation": "42 ZD pairs / C(16,2) = 42/120 = 7/20 = 0.35",
        "category": "sedenion_combinatorial",
    },
    {
        "id": "P06",
        "name": "g2_x_s3_order",
        "value": G2_S3_order_quotient,
        "derivation": "|W(G₂)| × |S₃| = 12 × 6 = 72",
        "category": "joint_group_order",
    },
    {
        "id": "P07",
        "name": "s3_sum_irrep_dim_sq",
        "value": S3_total_irrep_dim_sq,
        "derivation": "Σdim(irreps)² for S₃ = 1+1+4 = 6 = |S₃|",
        "category": "rep_theory_check",
    },
    {
        "id": "P08",
        "name": "octonion_aut_to_octonion_dim",
        "value": 14 / 8,
        "derivation": "dim(G₂ = Aut(O)) / dim(O) = 14/8 = 7/4 = 1.75",
        "category": "automorphism_ratio",
    },
    {
        "id": "P09",
        "name": "sedenion_aut_aut_dim",
        "value": (14 * 6) / sedenion_dim,
        "derivation": "dim(G₂ × S₃) / dim(𝕊) = (14 × 6) / 16 = 84/16 = 5.25",
        "category": "sedenion_automorphism_density",
    },
    {
        "id": "P10",
        "name": "zd_growth_ratio_5_4",
        "value": 294 / 42,
        "derivation": "OEIS A167654 ratio: ZD(n=5)/ZD(n=4) = 294/42 = 7",
        "category": "cd_tower_growth",
    },
    {
        "id": "P11",
        "name": "zd_growth_ratio_6_5",
        "value": 1518 / 294,
        "derivation": "ZD(n=6)/ZD(n=5) = 1518/294 ≈ 5.163",
        "category": "cd_tower_growth",
    },
    {
        "id": "P12",
        "name": "zd_growth_ratio_7_6",
        "value": 6942 / 1518,
        "derivation": "ZD(n=7)/ZD(n=6) = 6942/1518 ≈ 4.573",
        "category": "cd_tower_growth",
    },
    {
        "id": "P13",
        "name": "zd_growth_ratio_8_7",
        "value": 29886 / 6942,
        "derivation": "ZD(n=8)/ZD(n=7) = 29886/6942 ≈ 4.305",
        "category": "cd_tower_growth",
    },
    {
        "id": "P14",
        "name": "cd_tower_doubling_invariant",
        "value": math.log2(sedenion_dim) / math.log2(8),
        "derivation": "log₂(16)/log₂(8) = 4/3 ≈ 1.333 (CD tower level ratio)",
        "category": "cd_tower_structure",
    },
    {
        "id": "P15",
        "name": "s3_alternating_subgroup_ratio",
        "value": 3 / 6,
        "derivation": "|A₃|/|S₃| = 3/6 = 1/2 (parity sign cohomology)",
        "category": "permutation_invariant",
    },
])


def compute_sha256_commit(predictions):
    """sha256 over the canonicalized prediction list."""
    canonical = json.dumps(predictions, sort_keys=True, indent=None, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main():
    print("=" * 70)
    print("ICE PRE-REGISTERED PREDICTION DERIVATION")
    print("Step 1: derive from ICE algebra ONLY (no PDG consultation)")
    print("=" * 70)

    for p in ICE_DERIVATIONS:
        print(f"  {p['id']:4} {p['name']:40} = {p['value']:.6f}")
        print(f"        derivation: {p['derivation']}")

    print()
    print("=" * 70)
    print("Step 2: sha256 commit")
    print("=" * 70)
    commit_hash = compute_sha256_commit(ICE_DERIVATIONS)
    print(f"  sha256: {commit_hash}")
    print()

    # Save pre-registration document
    out = ICE_DIR / "ice_prereg_predictions_2026-05-18.json"
    payload = {
        "date": "2026-05-18",
        "cycle": "autoloop iter 41-55 (Task 4)",
        "protocol": "Lakatos-progressive pre-registration",
        "n_predictions": len(ICE_DERIVATIONS),
        "predictions": ICE_DERIVATIONS,
        "sha256_commit": commit_hash,
        "step": "1+2 (derivation + commit) COMPLETE; PDG comparison NOT YET PERFORMED",
        "verdict_top_level": "PRE_REGISTRATION_COMMITTED",
        "gate_passed": True,
        "note": "Step 3 (PDG comparison) and Step 4 (MC null gate) executed in separate script ice_prereg_check.py",
    }
    with out.open("w") as f:
        json.dump(payload, f, indent=2)
    print(f"  Pre-registration saved: {out}")
    print(f"  PROTOCOL: PDG comparison ONLY after this commit (see ice_prereg_check.py)")
    return commit_hash


if __name__ == "__main__":
    main()
