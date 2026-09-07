import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Dual.Defs

/-!
# Degree-reversed dual sewing for a three-term complex

This file uses the algebraic dual and reverses cochain degree.  It is not the
coefficient-only dual obtained by applying the same ghosts on the same test
complex.  The evaluation pairing is bilinear; no antilinear CPT operation or
positive inner product is asserted.
-/

namespace CptSewing.GradedDualSewing

variable {C0 C1 C2 E : Type*}
  [AddCommGroup C0] [Module ℂ C0]
  [AddCommGroup C1] [Module ℂ C1]
  [AddCommGroup C2] [Module ℂ C2]
  [AddCommGroup E] [Module ℂ E]

abbrev Dual (C : Type*) [AddCommGroup C] [Module ℂ C] := Module.Dual ℂ C

/-- The degree-zero differential on the degree-reversed dual complex. -/
def dualDifferential0 (q1 : C1 →ₗ[ℂ] C2) : Dual C2 →ₗ[ℂ] Dual C1 :=
  q1.dualMap

/-- The degree-one differential carries the sign required by the evaluation
Ward identity. -/
def dualDifferential1 (q0 : C0 →ₗ[ℂ] C1) : Dual C1 →ₗ[ℂ] Dual C0 :=
  -q0.dualMap

/-- A three-term cochain complex induces a square-zero degree-reversed dual
complex. -/
theorem dual_differential_square
    (q0 : C0 →ₗ[ℂ] C1) (q1 : C1 →ₗ[ℂ] C2) (hSquare : q1.comp q0 = 0) :
    (dualDifferential1 q0).comp (dualDifferential0 q1) = 0 := by
  ext lambda u
  have h := LinearMap.congr_fun hSquare u
  change -(lambda (q1 (q0 u))) = 0
  rw [show q1 (q0 u) = 0 by simpa [LinearMap.comp_apply] using h]
  simp

/-- Ward identity pairing degree zero of the original complex with degree two
of its reversed dual. -/
theorem ward_degree_zero
    (q0 : C0 →ₗ[ℂ] C1) (lambda : Dual C1) (u : C0) :
    (dualDifferential1 q0 lambda) u + lambda (q0 u) = 0 := by
  change -lambda (q0 u) + lambda (q0 u) = 0
  simp

/-- Ward identity pairing degree one of the original complex with degree one
of its reversed dual. -/
theorem ward_degree_one
    (q1 : C1 →ₗ[ℂ] C2) (lambda : Dual C2) (v : C1) :
    lambda (q1 v) - (dualDifferential0 q1 lambda) v = 0 := by
  change lambda (q1 v) - lambda (q1 v) = 0
  simp

/-- A dual top detector is closed exactly when it annihilates original
degree-one boundaries. -/
theorem top_detector_closed_iff
    (q1 : C1 →ₗ[ℂ] C2) (lambda : Dual C2) :
    dualDifferential0 q1 lambda = 0 ↔ ∀ v : C1, lambda (q1 v) = 0 := by
  constructor
  · intro h v
    have hv := LinearMap.congr_fun h v
    simpa [dualDifferential0, LinearMap.dualMap_apply] using hv
  · intro h
    ext v
    simpa [dualDifferential0, LinearMap.dualMap_apply] using h v

/-- A closed detector with nonzero evaluation proves that the corresponding
original top element is not a boundary. -/
theorem detector_witnesses_top_nonboundary
    (q1 : C1 →ₗ[ℂ] C2) (lambda : Dual C2) (z : C2)
    (hClosed : dualDifferential0 q1 lambda = 0) (hDetect : lambda z ≠ 0) :
    z ∉ LinearMap.range q1 := by
  rintro ⟨v, rfl⟩
  have h := LinearMap.congr_fun hClosed v
  exact hDetect (by simpa [dualDifferential0, LinearMap.dualMap_apply] using h)

/-- A split finite label map gives an exact evaluation identity for the
corresponding top representatives. -/
theorem section_evaluation
    (R : C2 →ₗ[ℂ] E) (J : E →ₗ[ℂ] C2) (hRJ : R.comp J = LinearMap.id)
    (lambda : Dual E) (e : E) :
    (lambda.comp R) (J e) = lambda e := by
  have h := LinearMap.congr_fun hRJ e
  change lambda (R (J e)) = lambda e
  rw [show R (J e) = e by simpa [LinearMap.comp_apply] using h]

/-- A finite label functional whose pullback is a closed top detector proves
the selected section representative non-boundary whenever it evaluates
nontrivially. -/
theorem section_detector_witnesses_top_nonboundary
    (q1 : C1 →ₗ[ℂ] C2) (R : C2 →ₗ[ℂ] E) (J : E →ₗ[ℂ] C2)
    (hRJ : R.comp J = LinearMap.id) (lambda : Dual E) (e : E)
    (hClosed : dualDifferential0 q1 (lambda.comp R) = 0)
    (hDetect : lambda e ≠ 0) : J e ∉ LinearMap.range q1 := by
  apply detector_witnesses_top_nonboundary q1 (lambda.comp R) (J e) hClosed
  rw [section_evaluation R J hRJ lambda e]
  exact hDetect

end CptSewing.GradedDualSewing
