# LONGINUS: sourceId=cd_final_quick, sourcePath=cd_final_quick.py
"""Quick final summary: basis census for 8,16 only (32 and 64 too slow for full),
plus pattern analysis."""
import numpy as np
np.random.seed(42)

def cd_conj(a):
    n = len(a)
    if n == 1: return a.copy()
    half = n // 2
    return np.concatenate([cd_conj(a[:half]), -a[half:]])

def cd_mul(a, b):
    n = len(a)
    if n == 1: return a * b
    half = n // 2
    a1, a2 = a[:half], a[half:]
    b1, b2 = b[:half], b[half:]
    return np.concatenate([
        cd_mul(a1, b1) - cd_mul(cd_conj(b2), a2),
        cd_mul(b2, a1) + cd_mul(a2, cd_conj(b1))
    ])

def basis(dim, i):
    e = np.zeros(dim)
    e[i] = 1.0
    return e

print("FULL BASIS ASSOCIATIVITY CENSUS (small dims):")
for dim in [8, 16]:
    total = nonassoc = 0
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                ei, ej, ek = basis(dim, i), basis(dim, j), basis(dim, k)
                lhs = cd_mul(cd_mul(ei, ej), ek)
                rhs = cd_mul(ei, cd_mul(ej, ek))
                total += 1
                if np.linalg.norm(lhs - rhs) > 1e-10:
                    nonassoc += 1
    print(f"  dim={dim}: {nonassoc}/{total} non-assoc ({100*nonassoc/total:.1f}%)")

# For 32 and 64, sample first 16 basis elements only (as a structural probe)
print("\nSAMPLED BASIS CENSUS (first 16 elements only):")
for dim in [32, 64, 128]:
    total = nonassoc = 0
    for i in range(16):
        for j in range(16):
            for k in range(16):
                ei, ej, ek = basis(dim, i), basis(dim, j), basis(dim, k)
                lhs = cd_mul(cd_mul(ei, ej), ek)
                rhs = cd_mul(ei, cd_mul(ej, ek))
                total += 1
                if np.linalg.norm(lhs - rhs) > 1e-10:
                    nonassoc += 1
    print(f"  dim={dim} (first 16 basis): {nonassoc}/{total} non-assoc ({100*nonassoc/total:.1f}%)")

# Check a targeted question: do the UPPER-HALF basis elements at 64D
# show different associativity patterns than upper-half at 32D?
print("\nUPPER-HALF BASIS CENSUS:")
for dim in [32, 64]:
    half = dim // 2
    total = nonassoc = 0
    # Pick 8 indices from upper half
    upper_idx = list(range(half, min(half+8, dim)))
    for i in upper_idx:
        for j in upper_idx:
            for k in upper_idx:
                ei, ej, ek = basis(dim, i), basis(dim, j), basis(dim, k)
                lhs = cd_mul(cd_mul(ei, ej), ek)
                rhs = cd_mul(ei, cd_mul(ej, ek))
                total += 1
                if np.linalg.norm(lhs - rhs) > 1e-10:
                    nonassoc += 1
    print(f"  dim={dim} upper[{half}:{half+8}]: {nonassoc}/{total} non-assoc ({100*nonassoc/total:.1f}%)")

# Cross-layer: lower-half x upper-half
print("\nCROSS-LAYER (lower x upper x lower):")
for dim in [32, 64]:
    half = dim // 2
    total = nonassoc = 0
    lower = list(range(min(8, half)))
    upper = list(range(half, min(half+8, dim)))
    for i in lower:
        for j in upper:
            for k in lower:
                ei, ej, ek = basis(dim, i), basis(dim, j), basis(dim, k)
                lhs = cd_mul(cd_mul(ei, ej), ek)
                rhs = cd_mul(ei, cd_mul(ej, ek))
                total += 1
                if np.linalg.norm(lhs - rhs) > 1e-10:
                    nonassoc += 1
    print(f"  dim={dim} L-U-L: {nonassoc}/{total} non-assoc ({100*nonassoc/total:.1f}%)")

print("\nDone.")
