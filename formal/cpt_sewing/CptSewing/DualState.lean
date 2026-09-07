import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Ring

/-!
# Finite rank-one dual-state coefficient algebra

This file contains only identities for the complex coefficient form
`starRingEnd ℂ z * w`.  It does not prove existence of a PDE solution or make an RAQ,
observable-algebra, physical-state, or physical CPT claim.
-/

namespace CptSewing.DualState

/-- The rank-one sesquilinear coefficient form. -/
def rankOne (z w : ℂ) : ℂ := starRingEnd ℂ z * w

/-- The rank-one coefficient is Hermitian under interchange. -/
theorem rankOne_hermitian (z w : ℂ) :
    starRingEnd ℂ (rankOne z w) = rankOne w z := by
  simp [rankOne, mul_comm]

/-- The diagonal real part is nonnegative and vanishes exactly at zero. -/
theorem rankOne_diag_positive_definite (z : ℂ) :
    0 ≤ (rankOne z z).re ∧ ((rankOne z z).re = 0 ↔ z = 0) := by
  have hdiag : (rankOne z z).re = Complex.normSq z := by
    unfold rankOne
    rw [← Complex.normSq_eq_conj_mul_self]
    simp
  constructor
  · rw [hdiag]
    exact Complex.normSq_nonneg z
  · rw [hdiag]
    exact Complex.normSq_eq_zero

/-- Conjugating both coefficients conjugates the rank-one form. -/
theorem rankOne_conj_covariant (z w : ℂ) :
    rankOne (starRingEnd ℂ z) (starRingEnd ℂ w) = starRingEnd ℂ (rankOne z w) := by
  simp [rankOne]

/-- A coefficient in the kernel gives a zero pairing against every second coefficient. -/
theorem rankOne_left_zero (w : ℂ) : rankOne 0 w = 0 := by
  unfold rankOne
  simp

end CptSewing.DualState
