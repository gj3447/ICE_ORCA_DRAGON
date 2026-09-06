import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Real bosonic boundary algebra for the CPT-sewing design

This file formalizes only the global-coordinate, real bosonic calculation in
`docs/research/ICE_CPT_SEWING_ORIGINAL_CYCLE_CONSTRUCTION_DESIGN_2026-09-06.md`,
Section 2.  It does not construct a quantum CPT lift, a BFV boundary relation,
a seam action, an integration cycle, or a physical state.

`omega` is the coordinate evaluation of `d (p_a da + p_phi dphi)` on two
tangent vectors.  It is deliberately not a theorem about differential forms on
a manifold.
-/

namespace CptSewing

/-- The real homogeneous boundary phase-space coordinates `(a, phi; pa, pphi)`. -/
structure Phase where
  a : ℝ
  phi : ℝ
  pa : ℝ
  pphi : ℝ

/-- A coordinate tangent vector to `Phase`. -/
structure Tangent where
  da : ℝ
  dphi : ℝ
  dpa : ℝ
  dpphi : ℝ

/-- The declared real bosonic momentum reflection. -/
def momentumReflection (z : Phase) : Phase :=
  ⟨z.a, z.phi, -z.pa, -z.pphi⟩

/-- The coordinate tangent map of `momentumReflection`. -/
def dMomentumReflection (v : Tangent) : Tangent :=
  ⟨v.da, v.dphi, -v.dpa, -v.dpphi⟩

/-- The canonical one-form evaluated at a point and a tangent vector. -/
def alpha (z : Phase) (v : Tangent) : ℝ :=
  z.pa * v.da + z.pphi * v.dphi

/-- Coordinate evaluation of `d alpha` on two tangent vectors. -/
def omega (v w : Tangent) : ℝ :=
  v.dpa * w.da - w.dpa * v.da + v.dpphi * w.dphi - w.dpphi * v.dphi

/-- The plus convention for the two-boundary canonical primitive. -/
def sumPrimitive (z₁ z₂ : Phase) (v : Tangent) : ℝ :=
  alpha z₁ v + alpha z₂ v

/-- The minus convention for the two-boundary canonical primitive. -/
def differencePrimitive (z₁ z₂ : Phase) (v : Tangent) : ℝ :=
  alpha z₁ v - alpha z₂ v

theorem momentumReflection_involutive (z : Phase) :
    momentumReflection (momentumReflection z) = z := by
  cases z
  simp [momentumReflection]

theorem dMomentumReflection_involutive (v : Tangent) :
    dMomentumReflection (dMomentumReflection v) = v := by
  cases v
  simp [dMomentumReflection]

theorem alpha_momentumReflection (z : Phase) (v : Tangent) :
    alpha (momentumReflection z) (dMomentumReflection v) = -alpha z v := by
  cases z
  cases v
  simp [alpha, momentumReflection, dMomentumReflection] <;> ring

theorem omega_momentumReflection (v w : Tangent) :
    omega (dMomentumReflection v) (dMomentumReflection w) = -omega v w := by
  cases v
  cases w
  simp [omega, dMomentumReflection] <;> ring

/-- The plus primitive vanishes on the graph of momentum reflection. -/
theorem sum_seam_zero (z : Phase) (v : Tangent) :
    alpha z v + alpha (momentumReflection z) (dMomentumReflection v) = 0 := by
  rw [alpha_momentumReflection]
  ring

/-- The minus primitive vanishes on the identity graph. -/
theorem identity_difference_seam_zero (z : Phase) (v : Tangent) :
    alpha z v - alpha z v = 0 := by
  ring

/--
The plus primitive vanishes in every configuration tangent direction exactly
when the two boundary momenta are opposite.  No relation is assumed here.
-/
theorem sumPrimitive_forall_iff (z₁ z₂ : Phase) :
    (∀ v : Tangent, sumPrimitive z₁ z₂ v = 0) ↔
      z₂.pa = -z₁.pa ∧ z₂.pphi = -z₁.pphi := by
  constructor
  · intro h
    have hpa := h ⟨1, 0, 0, 0⟩
    have hpphi := h ⟨0, 1, 0, 0⟩
    constructor
    · simp [sumPrimitive, alpha] at hpa
      linarith
    · simp [sumPrimitive, alpha] at hpphi
      linarith
  · rintro ⟨hpa, hpphi⟩ v
    simp [sumPrimitive, alpha, hpa, hpphi] <;> ring

/--
The minus primitive vanishes in every configuration tangent direction exactly
when the two boundary momenta agree.  No relation is assumed here.
-/
theorem differencePrimitive_forall_iff (z₁ z₂ : Phase) :
    (∀ v : Tangent, differencePrimitive z₁ z₂ v = 0) ↔
      z₂.pa = z₁.pa ∧ z₂.pphi = z₁.pphi := by
  constructor
  · intro h
    have hpa := h ⟨1, 0, 0, 0⟩
    have hpphi := h ⟨0, 1, 0, 0⟩
    constructor
    · simp [differencePrimitive, alpha] at hpa
      linarith
    · simp [differencePrimitive, alpha] at hpphi
      linarith
  · rintro ⟨hpa, hpphi⟩ v
    simp [differencePrimitive, alpha, hpa, hpphi] <;> ring

/-- The physical real chart used by the Starobinsky coordinate convention. -/
def InPhysicalChart (z : Phase) : Prop := 0 < z.a

theorem momentumReflection_preserves_physicalChart (z : Phase)
    (hz : InPhysicalChart z) : InPhysicalChart (momentumReflection z) := by
  simpa [InPhysicalChart, momentumReflection] using hz

/-- A nonzero tangent in the physical-chart interior for orientation controls. -/
def witnessPhase : Phase := ⟨1, 1, 1, 0⟩

/-- Vary only the scale factor at `witnessPhase`. -/
def witnessTangent : Tangent := ⟨1, 0, 0, 0⟩

theorem witness_in_physicalChart : InPhysicalChart witnessPhase := by
  norm_num [InPhysicalChart, witnessPhase]

/-- Wrong orientation: the plus primitive does not vanish on the identity graph. -/
theorem wrong_orientation_sum_identity :
    sumPrimitive witnessPhase witnessPhase witnessTangent = 2 := by
  norm_num [sumPrimitive, alpha, witnessPhase, witnessTangent]

/-- Wrong orientation: the minus primitive does not vanish on the reflection graph. -/
theorem wrong_orientation_difference_reflection :
    alpha witnessPhase witnessTangent -
        alpha (momentumReflection witnessPhase) (dMomentumReflection witnessTangent) = 2 := by
  norm_num [alpha, momentumReflection, dMomentumReflection, witnessPhase, witnessTangent]

/-- The declared Starobinsky potential in the reduced units of the source memo. -/
noncomputable def starobinskyPotential (phi : ℝ) : ℝ :=
  ((3 : ℝ) / 4) *
    (1 - Real.exp (-(Real.sqrt ((2 : ℝ) / 3)) * phi)) ^ 2

/-- The Lorentzian homogeneous Starobinsky Hamiltonian used in the source memo. -/
noncomputable def starobinskyHL (z : Phase) : ℝ :=
  -z.pa ^ 2 / (24 * Real.pi ^ 2 * z.a) +
    z.pphi ^ 2 / (4 * Real.pi ^ 2 * z.a ^ 3) -
    6 * Real.pi ^ 2 * z.a +
    2 * Real.pi ^ 2 * z.a ^ 3 * starobinskyPotential z.phi

/-- Momentum reflection preserves the Lorentzian Hamiltonian on the physical chart. -/
theorem starobinskyHL_momentumReflection (z : Phase) (_hz : InPhysicalChart z) :
    starobinskyHL (momentumReflection z) = starobinskyHL z := by
  simp [starobinskyHL, momentumReflection] <;> ring

/--
The Hamiltonian equality is algebraic in Lean's total real division.  This
separate theorem records the physical source chart `a > 0`, rather than using
the algebraic equality to extend the source through `a = 0`.
-/
theorem starobinskyHL_momentumReflection_onPhysicalChart (z : Phase)
    (hz : InPhysicalChart z) :
    InPhysicalChart (momentumReflection z) ∧
      starobinskyHL (momentumReflection z) = starobinskyHL z := by
  exact ⟨momentumReflection_preserves_physicalChart z hz,
    starobinskyHL_momentumReflection z hz⟩

end CptSewing
