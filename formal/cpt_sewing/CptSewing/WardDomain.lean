import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Finite boundary-domain jet algebra

This file proves finite complex Green-flux and real scalar-jet identities.
It does not assert an operator-domain theorem, a distributional boundary
limit, a BFV measure, or a physical CPT sewing prescription.
-/

namespace CptSewing.WardDomain

/-- The finite sesquilinear Green face flux. -/
def sesquiFlux (k u du v dv : ℂ) : ℂ :=
  k * (starRingEnd ℂ u * dv - starRingEnd ℂ du * v)

/-- Substituting a common complex Robin coefficient isolates its imaginary part. -/
theorem sesquiFlux_robin_formula (k r u v : ℂ) :
    sesquiFlux k u (r * u) v (r * v) =
      k * ((r - starRingEnd ℂ r) * starRingEnd ℂ u * v) := by
  unfold sesquiFlux
  simp only [map_mul]
  ring

/-- A common real Robin coefficient cancels the finite sesquilinear flux. -/
theorem sesquiFlux_real_robin (k u v : ℂ) (r : ℝ) :
    sesquiFlux k u ((r : ℂ) * u) v ((r : ℂ) * v) = 0 := by
  rw [sesquiFlux_robin_formula]
  simp

/-- The normal scalar jet expression at a face. -/
def scalarH0 (f f1 w u0 u1 u2 : ℝ) : ℝ :=
  -f * u2 - f1 * u1 + w * u0

/-- Its first normal a-derivative jet, with tangential derivatives suppressed. -/
def scalarH1 (f f1 f2 w w1 u0 u1 u2 u3 : ℝ) : ℝ :=
  -f * u3 - 2 * f1 * u2 - f2 * u1 + w1 * u0 + w * u1

/-- The finite Robin residual for the scalar jet expression. -/
def robinResidual (f f1 f2 w w1 r u0 u1 u2 u3 : ℝ) : ℝ :=
  scalarH1 f f1 f2 w w1 u0 u1 u2 u3 - r * scalarH0 f f1 w u0 u1 u2

/-- A Dirichlet quadratic-jet witness has the displayed normal expression. -/
theorem scalarH0_dirichlet_quadratic (f f1 w z : ℝ) :
    scalarH0 f f1 w 0 0 (2 * z) = -2 * f * z := by
  unfold scalarH0
  ring

/-- A cubic zero-jet witness has a Robin residual independent of the coefficient. -/
theorem robinResidual_cubic_zerojet (f f1 f2 w w1 r z : ℝ) :
    robinResidual f f1 f2 w w1 r 0 0 0 (6 * z) = -6 * f * z := by
  unfold robinResidual scalarH0 scalarH1
  ring

/-- If its leading normal coefficient and cubic amplitude are nonzero, this residual is nonzero. -/
theorem robinResidual_cubic_zerojet_nonzero (f f1 f2 w w1 r z : ℝ)
    (hf : f ≠ 0) (hz : z ≠ 0) :
    robinResidual f f1 f2 w w1 r 0 0 0 (6 * z) ≠ 0 := by
  rw [robinResidual_cubic_zerojet]
  exact mul_ne_zero (mul_ne_zero (by norm_num : (-6 : ℝ) ≠ 0) hf) hz

end CptSewing.WardDomain
