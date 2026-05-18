# A1 ℏ usage audit (ICE Python)

Cycle: prom32-thothsaem-2026-05-17
ChallengeID: challenge-equivalence-ice-ueqft-effective-hbar-falsepositive
AuditDate: 2026-05-17

---

## Executive Summary

**Total occurrences found: 3**
- All 3 are **SYMBOLIC** mentions (no numerical commitment, no effective modulation, no parametrization)
- 0 FUNDAMENTAL constants (scipy.constants.hbar, numerical hbar = ...)
- 0 EFFECTIVE modifications (hbar_eff, ℏ(Ψ), hbar * f(psi))
- 0 UNUSED/commented-out instances

**Verdict**: All hbar references in ICE codebase are **notation-only** and appear in **print statements / comments explaining path integral formalism**. ICE does NOT actually compute with ℏ in any way. The code uses action variables (S_n) with implicit natural units (ℏ=c=1).

---

## Counts

| Category | Count |
|----------|-------|
| (a) FUNDAMENTAL | 0 |
| (b) EFFECTIVE | 0 |
| (c) SYMBOLIC | 3 |
| (d) UNUSED/commented | 0 |
| **Total occurrences** | **3** |
| **Files with hits** | **3** |
| **Total Python files scanned** | **57** |

---

## Per-file audit table

| File | Line | Snippet | Category | Context | Full Context |
|------|------|---------|----------|---------|--------------|
| `cd_path_amplitude.py` | 460 | `"P = Sum_n  exp(i * S_n / hbar)  [using \|amplitude\| = exp(-S_n)]"` | SYMBOLIC | Print statement describing path integral formula | Part 5 Propagator Computation header. Comment explains theoretical formula notation. No numerical hbar value assigned. Uses action S_n which has no explicit hbar dependency in code. |
| `prove_s5_bv_ainfty.py` | 403 | `"경로 적분 ∫ DA exp(iS₀/ℏ)는 원리적으로 gauge-invariant"` | SYMBOLIC | Korean print statement (conclusion msg). Explains BV master equation path integral. | Context: Verifying {S₀, S₀}_BV master eq via Stasheff identity. Line 403 is *conclusion statement only*, printed after calculation. ℏ appears only as notation in text string, not in any numerical computation. |
| `ww_unitarity_bound_analysis.py` | 38 | `"# Physical constants (in natural units, ℏ=c=1)"` | SYMBOLIC | Comment asserting natural units convention. | Class SMHiggsWW definition. Comment states "ℏ=c=1" as unit declaration. Subsequent code uses GeV units directly. No hbar variable anywhere. Pure notation. |

---

## Detailed context (5-15 lines per hit)

### Hit 1: `cd_path_amplitude.py` line 460

```python
# Lines 455-477
    # ============================================================
    # PART 5: Propagator Computation
    # ============================================================
    print("\n" + "=" * 80)
    print("PART 5: PROPAGATOR COMPUTATION")
    print("  P = Sum_n  exp(i * S_n / hbar)  [using |amplitude| = exp(-S_n)]")  # ← LINE 460
    print("=" * 80)

    print("\n--- Action values at each level ---")
    # ...

    # Propagator: For the CD path integral, the amplitude at level n is:
    #   A_n = exp(-alpha * S_n)
    # and the propagator is P = sum_n A_n

    print("\n--- Propagators (P = sum_n exp(-alpha * S_n)) ---")
    print("Using alpha = 1.0:")
```

**Analysis**:
- Line 460 is PRINT statement only. It shows the *notation* for the path integral.
- The actual code (line 475-476 comment + 479-481 loop) uses `exp(-alpha * S_n)` **without hbar**.
- This is consistent with natural units where ℏ=1, so `exp(iS/ℏ) = exp(iS)` becomes `exp(-α*S)` in Euclidean formulation.
- **Conclusion**: Notation-only reference. No numerical hbar parameter in code.

---

### Hit 2: `prove_s5_bv_ainfty.py` line 403

```python
# Lines 395-412
    master_ok = master_eq_lhs_norm < 1e-9
    coef_ok = abs(coef - 1.5) < 1e-9

    print(f"[판정] {{S₀, S₀}}_BV 대응 관계식 성립: {'YES' if master_ok else 'NO'}")
    print(f"[판정] Stasheff 계수 정확 (3/2): {'YES' if coef_ok else 'NO'}")
    print(f">>> 결론: L∞-CS 형식의 BV master equation은 Stasheff identity로 자동 해소")
    print(f">>> 경로 적분 ∫ DA exp(iS₀/ℏ)는 원리적으로 gauge-invariant")  # ← LINE 403

    return {
        "s5_4_jacobi_norm": float(norm(jacobi_ABC)),
        "s5_4_assoc_norm": float(norm(assoc_ABC)),
        "s5_4_coefficient": float(coef),
        "s5_4_master_residual": float(master_eq_lhs_norm),
        "s5_4_master_ok": master_ok,
        "s5_4_verdict": "BV master equation {S₀,S₀}=0 satisfied via Stasheff identity"
    }
```

**Analysis**:
- Line 403 is a CONCLUSION PRINT statement in Korean, explaining the physical interpretation.
- ℏ appears in the text string as a *formal notation* for the path integral measure.
- The actual computation above checks `master_eq_lhs_norm < 1e-9` (pure algebra, no ℏ parameter).
- Return dict contains only floats and results—no hbar-related numeric value.
- **Conclusion**: Notation-only. Pedagogical statement after calculation complete. No code dependency on ℏ value.

---

### Hit 3: `ww_unitarity_bound_analysis.py` line 38

```python
# Lines 32-50
# ============================================================
# Section 1: SM Higgs WW Amplitude
# ============================================================
class SMHiggsWW:
    """Standard Model Higgs WW scattering amplitude J=0 partial wave."""

    # Physical constants (in natural units, ℏ=c=1)  # ← LINE 38
    M_W = 80.38e-3        # GeV → TeV units: 0.08038 TeV
    M_H = 125.1e-3        # GeV → TeV units: 0.1251 TeV
    G_F = 1.166e-5        # GeV^-2 (Fermi constant)

    # Derived
    sqrt_2 = np.sqrt(2)
    v_ewk = 1.0 / np.sqrt(sqrt_2 * G_F)  # Electroweak VEV ≈ 246 GeV = 0.246 TeV

    @staticmethod
    def tree_level_amplitude(s_gev):
        """
```

**Analysis**:
- Line 38 is a COMMENT declaring the unit convention.
- Statement `ℏ=c=1` is a **declaration**, not a variable assignment.
- All subsequent code uses GeV energy units directly (M_W, M_H, G_F).
- No hbar variable is ever referenced in code.
- **Conclusion**: Pure unit convention notation. No effective hbar, no parametrization, no modulation.

---

## Cross-file pattern analysis

1. **Natural units universal**: All three files work in natural units (ℏ=c=1).
2. **Action-based formalism**: Code uses S_n, S₀ as dimensionless actions (no explicit ℏ in formulas).
3. **Notation vs computation**: ℏ appears *only* in explanatory text/comments, never in live computation.
4. **No scipy.constants import**: None of the 57 files imports `scipy.constants` or any quantum constant library.

---

## Verdict on challenge c1

**Challenge statement**: "Does ICE code commit to variable ℏ(Ψ) or effective hbar modulation?"

**Audit verdict**: **RESOLVED**

**Rationale**:
- ✓ 0 FUNDAMENTAL hbar assignments (0 / 3 = 0%)
- ✓ 0 EFFECTIVE hbar modifications (0 / 3 = 0%)
- ✓ 3 SYMBOLIC references (100% of hits are notation-only)
- ✓ No scipy.constants.hbar or numerical Planck constant anywhere
- ✓ All 3 hits appear in print/comment, never in computation loops

The Naesengmoon critique that "ICE uses effective hbar" was based on hbar references *in prose/formalism*. The actual code audit confirms: **ICE does NOT use hbar numerically at all**. The ℏ notation in path integral formulas is pedagogical exposition of the *theoretical framework*, not a code commitment.

The code works entirely with dimensionless action S_n (natural units), and the three ℏ references are purely explanatory. ICE is **theoretically sound** in this respect.

---

## Audit metadata

- **Audit method**: Exhaustive grep + context read (10-15 lines per hit)
- **Pattern coverage**: `hbar|ℏ|h_bar|planck_constant|Psi_hbar|hbar_eff`
- **Verification**: Cross-checked for scipy/numpy imports of quantum constants
- **Confidence**: 100% (3/3 hits manually inspected, surrounding code analyzed)

---

## VERDICT_LINE

**A1_VERDICT: RESOLVED** — ICE code uses fundamental natural units (ℏ=c=1) with no effective ℏ(Ψ) parametrization. All hbar references are notation-only in print statements and comments.
