import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Finite ghost-algebra control for a boundary-sewing Ward defect

This is a finite coefficient-table calculation, not a construction of a
continuum BFV measure or a relative integration class.  The four degree-one
generators are ordered `(c1,c2,r1,r2)`.  The definitions below give the
degree-one--degree-two exterior product with that order explicitly, so the
needed anticommutation signs are not assumed as a Ward identity.
-/

namespace CptSewing.SeamWard

/-- Degree-one part of the exterior algebra on `(c1,c2,r1,r2)`. -/
structure G1 where
  c1 : ℝ
  c2 : ℝ
  r1 : ℝ
  r2 : ℝ

/-- Ordered degree-two coefficients: 12, 13, 14, 23, 24, 34. -/
structure G2 where
  c1c2 : ℝ
  c1r1 : ℝ
  c1r2 : ℝ
  c2r1 : ℝ
  c2r2 : ℝ
  r1r2 : ℝ

/-- Ordered degree-three coefficients: 123, 124, 134, 234. -/
structure G3 where
  c1c2r1 : ℝ
  c1c2r2 : ℝ
  c1r1r2 : ℝ
  c2r1r2 : ℝ

def zero1 : G1 := ⟨0, 0, 0, 0⟩
def zero3 : G3 := ⟨0, 0, 0, 0⟩

def add1 (x y : G1) : G1 :=
  ⟨x.c1 + y.c1, x.c2 + y.c2, x.r1 + y.r1, x.r2 + y.r2⟩

def scale1 (t : ℝ) (x : G1) : G1 := ⟨t * x.c1, t * x.c2, t * x.r1, t * x.r2⟩
def scale3 (t : ℝ) (x : G3) : G3 :=
  ⟨t * x.c1c2r1, t * x.c1c2r2, t * x.c1r1r2, t * x.c2r1r2⟩

/-- The degree-one exterior product, written as a six-entry coefficient table. -/
def wedge11 (x y : G1) : G2 :=
  ⟨x.c1 * y.c2 - x.c2 * y.c1,
   x.c1 * y.r1 - x.r1 * y.c1,
   x.c1 * y.r2 - x.r2 * y.c1,
   x.c2 * y.r1 - x.r1 * y.c2,
   x.c2 * y.r2 - x.r2 * y.c2,
   x.r1 * y.r2 - x.r2 * y.r1⟩

/-- The degree-one--degree-two exterior product, with the same generator order. -/
def wedge12 (x : G1) (y : G2) : G3 :=
  ⟨x.c1 * y.c2r1 - x.c2 * y.c1r1 + x.r1 * y.c1c2,
   x.c1 * y.c2r2 - x.c2 * y.c1r2 + x.r2 * y.c1c2,
   x.c1 * y.r1r2 - x.r1 * y.c1r2 + x.r2 * y.c1r1,
   x.c2 * y.r1r2 - x.r1 * y.c2r2 + x.r2 * y.c2r1⟩

theorem g3_ext (x y : G3)
    (h123 : x.c1c2r1 = y.c1c2r1) (h124 : x.c1c2r2 = y.c1c2r2)
    (h134 : x.c1r1r2 = y.c1r1r2) (h234 : x.c2r1r2 = y.c2r1r2) : x = y := by
  cases x
  cases y
  simp_all

def c1 : G1 := ⟨1, 0, 0, 0⟩
def c2 : G1 := ⟨0, 1, 0, 0⟩
def r1 : G1 := ⟨0, 0, 1, 0⟩
def r2 : G1 := ⟨0, 0, 0, 1⟩

/-- The ghost factor `(c2+c1) ∧ (r2-r1)` from the proposed two-history sewing. -/
def cSum : G1 := add1 c1 c2
def rDifference : G1 := add1 r2 (scale1 (-1) r1)
def kernelGhost : G2 := wedge11 cSum rDifference

theorem cSum_wedge_kernel_zero : wedge12 cSum kernelGhost = zero3 := by
  apply g3_ext <;> norm_num [wedge12, kernelGhost, wedge11, cSum, rDifference,
    add1, scale1, c1, c2, r1, r2, zero3]

theorem r1_minus_r2_wedge_kernel_zero :
    wedge12 (add1 r1 (scale1 (-1) r2)) kernelGhost = zero3 := by
  apply g3_ext <;> norm_num [wedge12, kernelGhost, wedge11, cSum, rDifference,
    add1, scale1, c1, c2, r1, r2, zero3]

theorem c1_wedge_kernel_nonzero : wedge12 c1 kernelGhost ≠ zero3 := by
  intro h
  have h123 := congrArg G3.c1c2r1 h
  norm_num [wedge12, kernelGhost, wedge11, cSum, rDifference, add1, scale1,
    c1, c2, r1, r2, zero3] at h123

/-- The degree-one constraint ghost `h1*c1+h2*c2`. -/
def constraintGhost (h1 h2 : ℝ) : G1 := add1 (scale1 h1 c1) (scale1 h2 c2)

/-- The finite ghost Ward defect is exactly the constraint difference times `c1 ∧ k`. -/
theorem constraintGhost_wedge_kernel (h1 h2 : ℝ) :
    wedge12 (constraintGhost h1 h2) kernelGhost =
      scale3 (h1 - h2) (wedge12 c1 kernelGhost) := by
  apply g3_ext <;> dsimp [wedge12, constraintGhost, kernelGhost, wedge11,
    cSum, rDifference, add1, scale1, scale3, c1, c2, r1, r2] <;> ring

/-- A scalar regulator that depends only on `N1-N2` is unchanged by diagonal shifts. -/
def differenceRegulator (f : ℝ → ℝ) (n1 n2 : ℝ) : ℝ := f (n1 - n2)

theorem differenceRegulator_diagonal_shift (f : ℝ → ℝ) (n1 n2 t : ℝ) :
    differenceRegulator f (n1 + t) (n2 + t) = differenceRegulator f n1 n2 := by
  exact congrArg f (by ring : (n1 + t) - (n2 + t) = n1 - n2)

/-- Starobinsky's potential in the positive chart coordinate `y=exp(-β φ)`. -/
noncomputable def starobinskyY (y : ℝ) : ℝ := (3 : ℝ) / 4 * (1 - y) ^ 2

/-- The `a=1` Lorentzian potential contribution used in the finite witness. -/
noncomputable def potentialContribution (y : ℝ) : ℝ := 2 * Real.pi ^ 2 * starobinskyY y

theorem potential_witness_difference :
    potentialContribution 1 - potentialContribution ((1 : ℝ) / 2) =
      -3 * Real.pi ^ 2 / 8 := by
  unfold potentialContribution starobinskyY
  ring

end CptSewing.SeamWard
