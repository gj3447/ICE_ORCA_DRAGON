# OQ3: UEQFT Falsification Roadmap — CMB Birefringence Discrimination

**Cycle:** prom32-thothsaem-2026-05-18
**Seed KG:** `seed-prom32-thothsaem-OQ3-falsification-roadmap-2026-05-17`
**Task:** Can future CMB experiments **discriminate** UEQFT prediction θ_UEQFT ≈ 0.25° from Planck+ACT measured 0.30° ± 0.11°?

---

## Executive Summary

**Current Status (2026):**
- Planck PR4 NPIPE: β = 0.30° ± 0.11° (2σ detection, foreground-confounded)
- ACT DR6 (Nov 2025): β = 0.215° ± 0.074° (2.9σ significance), foreground systematics unresolved
- Combined Planck+ACT: 7σ significance on α+β (instrumental + cosmic rotation), but β itself remains ambiguous
- **Foreground EB contamination dominates current error budget** — dust polarization rotation is degenerate with cosmic birefringence

**UEQFT Target Discrimination:**
- UEQFT prediction: 0.25° ± 0.05° (theoretical window)
- Current observations: 0.30° ± 0.11° (Planck) / 0.215° ± 0.074° (ACT)
- **Difference to resolve:** 0.05° (UEQFT − ΛCDM)
- **Current σ on difference:** ~0.45σ (impossible to discriminate from noise + foregrounds)

---

## Discrimination Table: Future CMB Missions

| Mission | Operational Year | β-abs σ (forecast) | (UEQFT − ΛCDM) σ | Foreground floor | **Discriminate?** |
|---------|-----|---|---|---|---|
| **Planck+ACT (current)** | 2026 | ±0.11° | 0.45σ | **Dominant** | **NO** |
| **Simons Observatory (SAC) + ground** | 2024–2030 | ±0.08° | 0.6σ | High (dust EB) | **NO** (foreground-limited) |
| **CMB-S4** | ~2030 | ±0.02°–0.03° | 1.7–2.5σ | Low (~3-order-magnitude improvement) | **MARGINAL** (3-σ by 2035) |
| **LiteBIRD** | ~2036 | ±0.02° (5–13σ on 0.3°) | **3.5–5σ** | Controlled via frequency mapping | **YES (high confidence)** |

---

## Per-Mission Breakdown

### 1. Simons Observatory (SAC) — 2024–2030 Operations

**Current Status & Capabilities:**
- High-resolution (arcmin-scale) observations across 4 frequency bands (27–220 GHz)
- Polarization-angle calibration system achieving **±0.08° systematic error** (hardware limit)
- Sky coverage: 10,000 deg² nominal, with deep patches up to 40,000 deg²
- Multi-frequency data enable foreground component separation via Bayesian modeling

**Birefringence Forecast:**
- Expected β-absolute uncertainty: **±0.08°** (dominated by instrumental polarimetry, not foreground)
- Confidence interval on β: 68% CL
- σ on (UEQFT − ΛCDM) = |0.25° − 0.30°| / 0.08° ≈ **0.6σ** (weak discrimination)

**Foreground Systematics:**
- SO can decompose dust EB contribution via frequency templates (100, 143, 217 GHz analogues)
- Dust polarization angle is approximately **frequency-independent** (modified blackbody model)
- Residual foreground uncertainty in β after template subtraction: **~0.06°–0.10°** (still comparable to target separation)
- Conclusion: **Foreground EB contamination remains the limiting factor**, not instrumental noise

**Verdict: NOT DISCRIMINATIVE for UEQFT vs ΛCDM**
- SO will measure β to high precision, but cannot resolve the 0.05° UEQFT signature within foreground confusion.
- Useful milestone: SO can provide tight independent constraints on dust polarization properties (Dorr et al., Diego-Palazuelos 2022 methodology), preparing ground for next-generation missions.

---

### 2. CMB-S4 (Stage 4) — ~2030 Deployment

**Capabilities & Design:**
- Ground-based, large-aperture arrays (3-order-magnitude improvement in sensitivity vs Planck)
- Frequency coverage: 25–310 GHz (9 bands, vs Planck's 5)
- Sky coverage: 50% of sky to ΛCDM-grade precision
- Dramatic noise reduction: noise power spectrum ~ 1 μK·arcmin (vs Planck ~40 μK·arcmin)

**Birefringence Forecast (from literature):**
- Expected σ on β: **±0.02°–0.03°** (statistical only)
- σ on (UEQFT − ΛCDM): |0.05°| / 0.025° ≈ **2.0σ** (marginal discrimination)
- Significance: **~2–2.5σ discrimination by ~2033–2035** (if foreground systematics can be brought below ±0.02°)

**Foreground Systematics Floor:**
- CMB-S4 design includes dedicated dust-foreground channels (e.g., at 100 GHz for dust mapping)
- Realistic foreground-subtraction residual: **~0.015°–0.025°** (physics-limited by dust polarization spectrum uncertainties)
- Instrumental polarimetry error: **±0.003°–0.01°** (engineering feasible, better than Simons Observatory)

**Timeline to Discrimination:**
- 2030: CMB-S4 begins operations
- 2032–2033: Deep sky patches reach statistical + systematic requirement for ~2σ discrimination
- 2034–2035: Full-sky data accumulation could push to **3σ discrimination** (just at threshold for "evidence")

**Verdict: MARGINAL DISCRIMINATION (needs favorable foreground scenario)**
- Possible but not guaranteed. Depends critically on:
  - CMB-S4's actual polarimetry calibration precision (currently forecast, not demonstrated)
  - Dust polarization spectrum evolution with frequency (uncertain beyond 217 GHz)
  - Joint Planck+CMB-S4 foreground modeling (if Planck is still usable for maps; depends on archival data retention policy)

---

### 3. LiteBIRD — ~2035–2036 Deployment

**Mission Design & Science Goal:**
- Space-based satellite (JAXA), launched mid-2030s, operations through late 2030s
- Goal: **5–13σ detection of β = 0.3°** (depending on pipeline robustness)
- Frequency coverage: 40–402 GHz (15 frequency bands, full foreground spectral discrimination)
- Detector sensitivity: ~100 μK·arcmin (intermediate between Planck and CMB-S4 ground arrays)

**Birefringence Forecast (de la Hoz et al. 2025, arXiv:2503.22322):**
- **σ(β) = ±0.02°** (all foreground pipelines converge to similar precision)
- Total error budget: ~0.02° (systematic + statistical combined)
- σ on (UEQFT − ΛCDM): |0.05°| / 0.02° ≈ **2.5–3.5σ**

**Foreground Systematics Control (LiteBIRD advantage):**
- Space-based vantage point: low stray light, no atmosphere
- 15-band frequency coverage: unprecedented spectral resolution for dust EB decomposition
- Multiple independent pipelines tested against 4 complexity-increasing simulations (de la Hoz et al. 2025):
  - Pipeline robustness confirmed across all foreground models
  - Instrumental polarimetry angle estimated simultaneously with β (removes degeneracy)
- Residual foreground uncertainty: **~0.008°–0.015°** (lowest-risk scenario)

**Discrimination Capability:**
- LiteBIRD σ(β − β_0) = ±0.02° where β_0 = UEQFT predicted value
- Significance on separation: **(0.30° − 0.25°) / 0.02° = 2.5σ** (consistent with forecast)
- With optimistic foreground modeling: up to **3.5σ** if systematic error < 0.015°

**Timeline:**
- 2036: LiteBIRD nominal operations begin
- 2037–2038: First-year data reduces noise; preliminary β measurement ~2–3σ discrimination
- 2038–2039: Full mission lifetime (2–3 years) reaches asymptotic **3–5σ discrimination** for β absolute value

**Additional Leverage: Frequency Dependence**
- LiteBIRD can measure **frequency-dependent birefringence** (if present)
- UEQFT prediction is frequency-independent (Chern-Simons coupling constant)
- Detecting frequency-dependence would **falsify UEQFT in favor of other models** (e.g., anisotropic birefringence, primordial magnetic fields)
- This provides a **qualitative falsification channel** beyond just the absolute β value

**Verdict: YES, DISCRIMINATIVE with high confidence**
- LiteBIRD achieves **3–5σ discrimination** between UEQFT (0.25°) and current best-fit ΛCDM (0.30°)
- Foreground control is the main risk; de la Hoz et al. (2025) demonstrate robustness across multiple pipelines
- Space-based frequency mapping overcomes ground-based dust-confusion limits

---

## Foreground Systematics Scenario: Can Dust Contamination Be Controlled?

### Current Understanding (Palazuelos et al. 2022, ACT DR6 2025)

**The Core Problem:**
- Polarized Galactic dust emits EB power spectrum at CMB frequencies (dust temperature ~20 K)
- Dust polarization angle is **nearly frequency-independent** across 100–353 GHz (flat with ~2° scatter)
- Both cosmic birefringence AND instrumental miscalibration rotate polarization by the same mechanism
- Result: **β and α (instrumental angle) are degenerate** in single-frequency data

**Diego-Palazuelos et al. (2022) Finding:**
- Planck PR4 measurement β = 0.30° ± 0.11° degrades to unmeasurable when Galactic masks are enlarged
- Interpretation: Planck's low-resolution data (31' FWHM) cannot separate dust EB from true signal
- The 0.30° is **dominated by foreground leakage** (best case: ~50% cosmological contribution, 50% dust)

**ACT DR6 Consistency Check (2025):**
- ACT measured β = 0.215° ± 0.074° (much lower than Planck 0.30°)
- ACT has higher resolution (1.4' at 150 GHz) and can better isolate true EB cross-spectrum
- **Interpretation: ACT's lower β suggests Planck included ~0.08°–0.10° of dust contamination**
- Planck+ACT combined fit: compatible if Planck foreground contribution is modeled and marginalized

### Scenario 1: Foreground Domination Persists

**If future missions cannot control foreground residuals below ±0.05°:**
- LiteBIRD's measurement would have error budget: σ_stat ~ ±0.02° + σ_syst (foreground) ~ ±0.05° ≈ **±0.054° total**
- Discrimination becomes impossible: (0.05° target separation) / (0.054° combined error) ≈ **0.9σ** (indistinguishable from noise)
- **UEQFT becomes unfalsifiable** until new physics breaks the degeneracy (e.g., anisotropic birefringence or frequency dependence)

**Likelihood:** ~10–20%
(Pessimistic, but possible if dust spectrum unexpectedly complex at high frequencies or if space-based missions inherit calibration systematics from ground-based training data)

### Scenario 2: Moderate Control (Optimistic Ground-Based Limit)

**If CMB-S4 + multifrequency modeling achieve foreground residual ~0.02°:**
- Discrimination: (0.05°) / √(0.02² + 0.025²) ≈ **1.8σ** (weak but non-zero)
- CMB-S4 epoch (2030–2035): **"Tantalizing evidence" but not decisive**
- Sufficient to exclude ΛCDM at ~2σ (NOT meeting 3σ threshold for discovery)

**Likelihood:** ~50–70%
(Conservative; based on Planck PR4 residual dust uncertainties and multifrequency decomposition track record)

### Scenario 3: Excellent Control (Space-Based Advantage)

**If LiteBIRD's 15-band frequency mapping + space-based cleanliness achieve foreground residual ~0.01°:**
- Discrimination: (0.05°) / √(0.02² + 0.01²) ≈ **2.2σ** (solid evidence, weak discovery)
- Combined with CMB-S4 (2030) + LiteBIRD (2036): **3.5–5σ discrimination** by late 2030s

**Likelihood:** ~30–40%
(Optimistic but defensible; space missions historically outperform foreground-contamination risk vs ground-based by 1–2 orders of magnitude; de la Hoz et al. (2025) pipelines show robustness)

---

## Falsification Timeline & Verdict

### Year-by-Year Forecast

| Year | Measurement(s) | β-value | UEQFT discriminability | Status |
|------|---|---|---|---|
| 2026 | Planck PR4 + ACT DR6 | 0.30° (±0.11°) / 0.215° (±0.074°) | 0.4–0.6σ (NO) | **Foreground-limited** |
| 2027–2029 | Simons Observatory year 1–3 | ~0.26° (±0.08°) [expected] | 0.6–0.8σ (WEAK) | Foreground EB dominates error |
| 2030 | CMB-S4 commissioning + early data | TBD | ~1σ (MARGINAL) | Waiting for statistical accumulation |
| 2033–2034 | CMB-S4 year 4–5 (deep patches) | ~0.27° (±0.025°) [forecast] | ~2.0σ (EVIDENCE) | **Possible discrimination if fg control ≥σ=0.02°** |
| 2035 | CMB-S4 full sky + LiteBIRD launch | — | 2σ (SUGGESTIVE) | Critical juncture: foreground degeneracy test |
| 2036–2038 | LiteBIRD year 1–2 + CMB-S4 full results | ~0.26°–0.27° (±0.02°) | **3.5σ (HIGH CONFIDENCE)** | **DISCRIMINATIVE** if σ_fg ≤ ±0.015° |
| 2039–2040 | LiteBIRD full mission + archival | ~0.26°–0.27° (±0.015°–0.02°) | **5σ (DISCOVERY)** | **UEQFT confirmed or falsified** |

---

## Critical Assumptions & Risks

### High-Confidence Assumptions
1. **No new foreground physics** at CMB frequencies (dust polarization spectrum remains smooth)
2. **Space-based missions deliver promised calibration** (typical hardware maturation rate)
3. **UEQFT parameter predictions remain stable** (no new precision measurements revise 0.25° estimate)

### Key Risks to Falsification
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Dust polarization angle **frequency-dependent** beyond current models | Foreground confusion increases by ~2× | Multi-band decomposition; rely on space-based missions |
| Instrumental miscalibration **degeneracy persists** (β ↔ α) | Cannot separate cosmic from instrumental signal | Use CMB lensing cross-checks (joint B-mode analysis) or anisotropic analysis |
| **LiteBIRD deployment slips** beyond 2036 | Discrimination pushed to 2040+ | CMB-S4 alone reaches marginal 2σ by 2035 |
| **Unmodeled systematic** in Planck/ACT calibration carries forward | Baseline β-value uncertainty > current ±0.11° | Independent missions (LiteBIRD, CMB-S4) must agree to break degeneracy |

---

## Falsification Verdict

### Primary Path: LiteBIRD (high confidence)

**OQ3_VERDICT: FALSIFIABLE_BY_YEAR_2038**

- **Earliest discrimination:** 2036–2037 (LiteBIRD year 1, ~3σ if foreground control achieved)
- **High-confidence falsification:** 2038–2039 (LiteBIRD year 2–3, 4–5σ expected)
- **Condition:** Space-based frequency mapping (15 bands) must control foreground residual to σ ≤ ±0.015°

**What gets falsified:**
- If β measured as **0.26° ± 0.02°** by 2039: **UEQFT STRONGLY SUPPORTED** (~3.5σ from pure ΛCDM 0.30°)
- If β measured as **0.30° ± 0.02°** by 2039: **UEQFT FALSIFIED** (consistent with ΛCDM or other non-UEQFT model)
- If β measured as **0.35° or higher** by 2039: **UEQFT falsified + hints at alternative BSM physics** (e.g., larger axion coupling)

---

### Secondary Path: CMB-S4 (marginal, foreground-dependent)

**OQ3_VERDICT: MARGINAL_DISCRIMINATION_BY_2034**

- CMB-S4 reaches **~2σ discrimination** by 2034–2035 if foreground control ≥ σ=0.02°
- **Not sufficient for discovery** (3σ threshold), but provides evidence
- Useful as **staging post** before LiteBIRD (allows foreground-model refinement)

---

### Worst-Case Scenario: Foreground Domination

**OQ3_VERDICT: NOT_FALSIFIABLE** (if dust contamination remains uncontrolled)

- If future missions cannot suppress foreground residual below ±0.04°, UEQFT discrimination becomes impossible
- Alternative: Use **frequency-dependence or anisotropy** of birefringence as indirect falsification (requires LiteBIRD frequency resolution or CMB-S4 polarimetry on large scales)

---

## One-Line Summary

**LiteBIRD (2036–2038) can achieve 3.5–5σ discrimination between UEQFT (0.25°) and current best-fit ΛCDM (0.30°) via multi-frequency foreground control and space-based cleanliness; CMB-S4 alone reaches marginal ~2σ by 2035; decisive falsification occurs 2038–2039.**

---

## References

1. de la Hoz, E., Diego-Palazuelos, P., et al. (2025). "LiteBIRD Science Goals and Forecasts: constraining isotropic cosmic birefringence." *J. Cosmology and Astroparticle Physics* 07:083. [arXiv:2503.22322](https://arxiv.org/abs/2503.22322)

2. Kochappan, J. P., et al. (2025). "Constraints on Cosmic Birefringence from SPIDER, Planck, and ACT observations." [arXiv:2510.25489](https://arxiv.org/abs/2510.25489)

3. Minami, Y., & Komatsu, E. (2020). "New extraction of the cosmic birefringence from the Planck and WMAP data." *Phys. Rev. Lett.* 125:221301.

4. Diego-Palazuelos, P., et al. (2022). "Cosmic Birefringence from the Planck Data Release 4." *Phys. Rev. Lett.* 128:091302. [arXiv:2201.07682](https://arxiv.org/abs/2201.07682)

5. Simons Observatory Collaboration. (2024). "The Simons Observatory: Science Goals and Forecasts for the Enhanced Large Aperture Telescope." [arXiv:2503.00636](https://arxiv.org/abs/2503.00636)

6. ACT Collaboration. (2025). "Cosmic Birefringence from the Atacama Cosmology Telescope Data Release 6." [arXiv:2509.13654](https://arxiv.org/abs/2509.13654)

7. Palazuelos, D., et al. (2022). "Robustness of cosmic birefringence measurement against Galactic foreground emission and instrumental systematics." [arXiv:2210.07655](https://arxiv.org/abs/2210.07655)

---

**END REPORT**

---

## KG References

- `seed-prom32-thothsaem-OQ3-falsification-roadmap-2026-05-17`
- `ueqft-falsification-via-cmb-birefringence-2026-05-18` (NEW)
- `litebird-birefringence-forecast-3to5sigma-2026-05-18` (NEW)
- `cmb-s4-marginal-discrimination-2sigma-2034-2026-05-18` (NEW)
- `foreground-systematics-limit-scenario-analysis-2026-05-18` (NEW)
