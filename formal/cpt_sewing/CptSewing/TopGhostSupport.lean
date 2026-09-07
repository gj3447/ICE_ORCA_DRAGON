import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Dual.Lemmas

/-!
# Abstract top-ghost support test

This module records the two-constraint coordinate-ghost algebra only.  For
coefficient carrier `V`, the degree-zero differential is `(H u, p u)` and
the degree-one to top-ghost differential is `H y - p x`, where `x` is the
`c` coefficient and `y` is the `rho` coefficient.  It does not construct the
Starobinsky distributions, choose a continuous dual or half-density space,
quantize a BV--BFV boundary theory, or construct CPT/sewing data.

In particular, the last theorem is conditional on surjectivity of `p` on the
*selected coefficient carrier*.  It may be applied to a chosen transpose or
distributional completion only after that carrier and its operator domain are
actually supplied.
-/

namespace CptSewing.TopGhostSupport

variable {V E : Type*} [AddCommGroup V] [Module ℂ V]
  [AddCommGroup E] [Module ℂ E]

/-- Degree-zero BRST coefficients in the ordered `(c, rho)` basis. -/
def q0 (H p : Module.End ℂ V) (u : V) : V × V := (H u, p u)

/-- The coefficient of `c rho` after applying the coordinate-ghost BRST map. -/
def q1 (H p : Module.End ℂ V) (xy : V × V) : V := H xy.2 - p xy.1

/-- There is no degree-three monomial for two coordinate ghosts. -/
def q2 (_z : V) : V := 0

/-- Commuting constraints make the two-step coordinate-ghost complex nilpotent. -/
theorem q1_q0 (H p : Module.End ℂ V) (u : V)
    (hComm : H.comp p = p.comp H) : q1 H p (q0 H p u) = 0 := by
  unfold q1 q0
  have h := LinearMap.congr_fun hComm u
  exact sub_eq_zero.mpr (by simpa [LinearMap.comp_apply] using h)

omit [Module ℂ V] in
/-- Every top-ghost coefficient is closed in the two-ghost complex. -/
theorem top_closed (z : V) : q2 z = 0 := rfl

/-- A common constraint-annihilating functional kills every top exact term. -/
theorem detector_kills_q1 (H p : Module.End ℂ V) (T : V →ₗ[ℂ] E)
    (hTH : T.comp H = 0) (hTp : T.comp p = 0) (xy : V × V) :
    T (q1 H p xy) = 0 := by
  unfold q1
  rw [map_sub]
  have hH := LinearMap.congr_fun hTH xy.2
  have hp := LinearMap.congr_fun hTp xy.1
  rw [show T (H xy.2) = 0 by simpa [LinearMap.comp_apply] using hH]
  rw [show T (p xy.1) = 0 by simpa [LinearMap.comp_apply] using hp]
  simp

/-- A nonzero detector value proves that a top coefficient is not exact. -/
theorem not_in_range_of_detector (H p : Module.End ℂ V) (T : V →ₗ[ℂ] E)
    (hTH : T.comp H = 0) (hTp : T.comp p = 0) (z : V) (hTz : T z ≠ 0) :
    ¬ ∃ xy : V × V, q1 H p xy = z := by
  rintro ⟨xy, hxy⟩
  apply hTz
  rw [← hxy]
  exact detector_kills_q1 H p T hTH hTp xy

/-- A split family of common constraint annihilators detects a nonzero
top-ghost class carried by its section. -/
theorem section_combination_exact_implies_zero
    (H p : Module.End ℂ V) (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hRJ : R.comp J = LinearMap.id) (hRH : R.comp H = 0) (hRp : R.comp p = 0)
    (v : E) (hExact : ∃ xy : V × V, q1 H p xy = J v) : v = 0 := by
  rcases hExact with ⟨xy, hxy⟩
  have hRj : R (J v) = v := by
    have h := LinearMap.congr_fun hRJ v
    simpa [LinearMap.comp_apply] using h
  calc
    v = R (J v) := hRj.symm
    _ = R (q1 H p xy) := by rw [hxy]
    _ = 0 := detector_kills_q1 H p R hRH hRp xy

/-- A nonzero finite label therefore gives a nontrivial top-ghost class on
the stated coefficient carrier. -/
theorem section_combination_not_exact
    (H p : Module.End ℂ V) (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hRJ : R.comp J = LinearMap.id) (hRH : R.comp H = 0) (hRp : R.comp p = 0)
    (v : E) (hv : v ≠ 0) : ¬ ∃ xy : V × V, q1 H p xy = J v := by
  intro hExact
  exact hv (section_combination_exact_implies_zero H p R J hRJ hRH hRp v hExact)

/-- A chosen preimage under the primary constraint makes a top coefficient
exact.  This is the algebraic form of a Heaviside primitive in a coordinate
distributional realization; no such realization is constructed here. -/
theorem exact_of_p_preimage (H p : Module.End ℂ V) (v z : V)
    (hpv : p v = z) : q1 H p (-v, 0) = z := by
  simp [q1, hpv]

/-- If the chosen coefficient-space realization makes `p` surjective, every
top-ghost coefficient is exact.  This condition must not be inferred for a
test carrier from a separate statement about its algebraic dual. -/
theorem all_top_exact_of_surjective_p (H p : Module.End ℂ V)
    (hpSurjective : Function.Surjective p) (z : V) :
    ∃ xy : V × V, q1 H p xy = z := by
  rcases hpSurjective z with ⟨v, hpv⟩
  exact ⟨(-v, 0), exact_of_p_preimage H p v z hpv⟩

/-- The algebraic dual constraints still commute when the original ones do.
This uses the algebraic transpose, not an adjoint of a chosen Hilbert-space
realization. -/
theorem dual_constraints_commute (H p : Module.End ℂ V)
    (hComm : H.comp p = p.comp H) :
    H.dualMap.comp p.dualMap = p.dualMap.comp H.dualMap := by
  rw [LinearMap.dualMap_comp_dualMap, LinearMap.dualMap_comp_dualMap]
  exact congrArg LinearMap.dualMap hComm.symm

/-- On the algebraic coefficient dual, injectivity of the original primary
constraint makes its transpose surjective.  Hence all algebraic-dual
top-ghost coefficients are exact.  No conclusion about a continuous dual,
distribution topology, or half-density completion follows from this theorem. -/
theorem all_top_exact_in_algebraic_dual (H p : Module.End ℂ V)
    (hpInjective : Function.Injective p) (z : Module.Dual ℂ V) :
    ∃ xy : Module.Dual ℂ V × Module.Dual ℂ V,
      q1 H.dualMap p.dualMap xy = z := by
  exact all_top_exact_of_surjective_p H.dualMap p.dualMap
    (LinearMap.dualMap_surjective_of_injective hpInjective) z

end CptSewing.TopGhostSupport
