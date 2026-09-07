import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Finite complementary-polarization seam jets

This module records only the boundary-jet algebra of the complementary
Neumann/Dirichlet Cauchy construction.  It does not construct the Cauchy
solutions, prove their Green identity, supply BFV ghosts, or define a BV
pushforward or an original integration cycle.

The pairing is complex-bilinear.  It is deliberately not a positive
sesquilinear physical inner product.
-/

namespace CptSewing.SeamPolarization

/-- Boundary value and coordinate `∂_a` derivative jet at the selected face. -/
structure Jet where
  q : ℂ
  p : ℂ

/-- The finite bilinear Green-face pairing in the declared order. -/
def seamFlux (k : ℝ) (x y : Jet) : ℂ :=
  (k : ℂ) * (x.q * y.p - x.p * y.q)

/-- The Neumann Lagrangian boundary condition. -/
def IsNeumann (x : Jet) : Prop := x.p = 0

/-- The Dirichlet Lagrangian boundary condition. -/
def IsDirichlet (x : Jet) : Prop := x.q = 0

/-- Kinematic complex conjugation on the finite boundary jet. -/
def K (x : Jet) : Jet := ⟨starRingEnd ℂ x.q, starRingEnd ℂ x.p⟩

/-- The same Neumann polarization has zero bilinear seam flux. -/
theorem seamFlux_neumann_neumann (k : ℝ) {x y : Jet}
    (hx : IsNeumann x) (hy : IsNeumann y) : seamFlux k x y = 0 := by
  simp only [IsNeumann] at hx hy
  simp [seamFlux, hx, hy]

/-- The same Dirichlet polarization has zero bilinear seam flux. -/
theorem seamFlux_dirichlet_dirichlet (k : ℝ) {x y : Jet}
    (hx : IsDirichlet x) (hy : IsDirichlet y) : seamFlux k x y = 0 := by
  simp only [IsDirichlet] at hx hy
  simp [seamFlux, hx, hy]

/-- Complementary Neumann/Dirichlet jets retain the expected coefficient. -/
theorem seamFlux_neumann_dirichlet (k : ℝ) {x y : Jet}
    (hx : IsNeumann x) (hy : IsDirichlet y) :
    seamFlux k x y = (k : ℂ) * x.q * y.p := by
  simp only [IsNeumann] at hx
  simp only [IsDirichlet] at hy
  simp [seamFlux, hx, hy]

/-- The actual upper-face coefficient for the fixed Weyl operator. -/
noncomputable def upperFaceK : ℝ := -1 / (48 * Real.pi ^ 2)

/-- Unit complementary jets witness a nonzero upper-face pairing. -/
theorem upperFace_unit_witness :
    seamFlux upperFaceK ⟨1, 0⟩ ⟨0, 1⟩ =
      (-1 / (48 * Real.pi ^ 2) : ℝ) := by
  simp [seamFlux, upperFaceK]

/-- The complementary unit witness cannot vanish. -/
theorem upperFace_unit_witness_nonzero :
    seamFlux upperFaceK ⟨1, 0⟩ ⟨0, 1⟩ ≠ 0 := by
  rw [upperFace_unit_witness]
  norm_cast
  have hpiSquared : Real.pi ^ 2 ≠ 0 := pow_ne_zero 2 Real.pi_ne_zero
  have hden : (48 : ℝ) * Real.pi ^ 2 ≠ 0 :=
    mul_ne_zero (by norm_num) hpiSquared
  exact div_ne_zero (by norm_num) hden

/-- Kinematic conjugation preserves the Neumann polarization. -/
theorem K_preserves_neumann (x : Jet) (hx : IsNeumann x) : IsNeumann (K x) := by
  simp only [IsNeumann] at hx ⊢
  simp [K, hx]

/-- Kinematic conjugation preserves the Dirichlet polarization. -/
theorem K_preserves_dirichlet (x : Jet) (hx : IsDirichlet x) : IsDirichlet (K x) := by
  simp only [IsDirichlet] at hx ⊢
  simp [K, hx]

/-- With real kinetic coefficient, K conjugates rather than exchanges seam flux. -/
theorem seamFlux_K_covariant (k : ℝ) (x y : Jet) :
    seamFlux k (K x) (K y) = starRingEnd ℂ (seamFlux k x y) := by
  unfold seamFlux K
  simp

end CptSewing.SeamPolarization
