import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Finite Green-boundary-jet algebra for the Ward-face discriminator

This file contains only real finite boundary-jet identities for the bilinear
Green face expression used by the declared seam calculation.  It does not
formalize distributions, a limiting kernel, a BFV functional measure, or an
original relative cycle.
-/

namespace CptSewing.WardFace

/--
The real one-face Green bilinear expression in the convention
`B = ⟨u, [H,S] v⟩`.  Here `u,du,v,dv` are independent boundary jets and `k`
is the declared face kinetic coefficient.
-/
def faceFlux (k u du v dv : ℝ) : ℝ := k * (u * dv - du * v)

/-- Interchanging the two real boundary jets reverses the Green face flux. -/
theorem faceFlux_antisymmetric (k u du v dv : ℝ) :
    faceFlux k u du v dv = -faceFlux k v dv u du := by
  unfold faceFlux
  ring

/-- A common Dirichlet condition cancels the finite face flux. -/
theorem faceFlux_common_dirichlet (k du dv : ℝ) :
    faceFlux k 0 du 0 dv = 0 := by
  unfold faceFlux
  ring

/-- A common real Robin coefficient cancels the finite face flux. -/
theorem faceFlux_common_robin (k r u v : ℝ) :
    faceFlux k u (r * u) v (r * v) = 0 := by
  unfold faceFlux
  ring

/-- The declared upper scale-face coefficient. -/
noncomputable def scaleUpperFaceK : ℝ := -1 / (48 * Real.pi ^ 2)

/-- A finite boundary-jet witness has the stated nonzero upper-face flux. -/
theorem scaleUpperFace_witness_value :
    faceFlux scaleUpperFaceK 1 0 1 1 = -1 / (48 * Real.pi ^ 2) := by
  unfold faceFlux scaleUpperFaceK
  ring

/-- The same finite witness cannot have vanishing upper-face flux. -/
theorem scaleUpperFace_witness_nonzero :
    faceFlux scaleUpperFaceK 1 0 1 1 ≠ 0 := by
  rw [scaleUpperFace_witness_value]
  have hpiSquared : Real.pi ^ 2 ≠ 0 := pow_ne_zero 2 Real.pi_ne_zero
  have hden : (48 : ℝ) * Real.pi ^ 2 ≠ 0 :=
    mul_ne_zero (by norm_num) hpiSquared
  exact div_ne_zero (by norm_num) hden


/-!
No ghost-projection coefficient is asserted here: extracting a `c1*g`
coefficient requires the separate graded kernel, Berezin orientation and dual
fiber convention.  Those data are not boundary-jet facts.
-/

end CptSewing.WardFace
