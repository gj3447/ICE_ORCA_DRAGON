import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Dual.Defs

/-!
# Finite quotient lifts and the adjoint-domain obstruction

This file is finite abstract algebra.  It records the exact lift supplied by
a split quotient map and the obstruction obtained when a constraint is
injective on a test carrier but a proposed lift must also preserve an adjoint
on that carrier.  It does not construct a PDE observable, a self-adjoint
extension, a rigging map, or a BFV/CPT operation.
-/

namespace CptSewing.QuotientLift

variable {V E : Type*} [AddCommGroup V] [Module ℂ V]
  [AddCommGroup E] [Module ℂ E]

/-- A finite label action lifted along a chosen section of `R`. -/
def quotientLift (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V) (A : Module.End ℂ E) :
    Module.End ℂ V :=
  J.comp (A.comp R)

/-- The lift has the declared action after applying the quotient map. -/
theorem quotientLift_action (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (A : Module.End ℂ E) (hRJ : R.comp J = LinearMap.id) :
    R.comp (quotientLift R J A) = A.comp R := by
  ext v
  change R (J (A (R v))) = A (R v)
  have h := LinearMap.congr_fun hRJ (A (R v))
  simpa [LinearMap.comp_apply] using h

/-- Constraint annihilation by `R` makes every split lift kill the constraint
on its right.  This alone is not a strong or weak commutant statement. -/
theorem quotientLift_kills_right (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (A : Module.End ℂ E) (p : Module.End ℂ V) (hp : R.comp p = 0) :
    (quotientLift R J A).comp p = 0 := by
  ext v
  change J (A (R (p v))) = 0
  have h := LinearMap.congr_fun hp v
  have hpv : R (p v) = 0 := by simpa [LinearMap.comp_apply] using h
  rw [hpv]
  simp

/-- Applying the quotient map on the left and the section on the right
recovers the original finite label action. -/
theorem quotientLift_sandwich (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (A : Module.End ℂ E) (hRJ : R.comp J = LinearMap.id) :
    (R.comp (quotientLift R J A)).comp J = A := by
  ext e
  change R (J (A (R (J e)))) = A e
  have h1 := LinearMap.congr_fun hRJ (A (R (J e)))
  have h2 := LinearMap.congr_fun hRJ e
  rw [show R (J (A (R (J e)))) = A (R (J e)) by
        simpa [LinearMap.comp_apply] using h1]
  rw [show R (J e) = e by simpa [LinearMap.comp_apply] using h2]

/-- A nonzero finite label action has a nonzero split lift. -/
theorem quotientLift_ne_zero (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (A : Module.End ℂ E) (hRJ : R.comp J = LinearMap.id) (hA : A ≠ 0) :
    quotientLift R J A ≠ 0 := by
  intro hLift
  apply hA
  have hSandwich := quotientLift_sandwich R J A hRJ
  rw [hLift] at hSandwich
  simpa using hSandwich.symm

/-- If a proposed action has the desired quotient action, its difference from
the chosen split lift is invisible after applying `R`. -/
theorem correction_killed_by_quotient (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (A : Module.End ℂ E) (O : Module.End ℂ V) (hRJ : R.comp J = LinearMap.id)
    (hRO : R.comp O = A.comp R) :
    R.comp (O - quotientLift R J A) = 0 := by
  ext v
  change R (O v - J (A (R v))) = 0
  rw [map_sub]
  have h1 := LinearMap.congr_fun hRO v
  have h2 := LinearMap.congr_fun (quotientLift_action R J A hRJ) v
  rw [show R (O v) = A (R v) by simpa [LinearMap.comp_apply] using h1]
  rw [show R (J (A (R v))) = A (R v) by
        simpa [quotientLift, LinearMap.comp_apply] using h2]
  simp

/-- An injective constraint rules out a right-killing endomorphism which also
commutes with that constraint on the stated carrier. -/
theorem zero_of_injective_commutes_kills_right (p O : Module.End ℂ V)
    (hpInjective : Function.Injective p) (hOp : O.comp p = 0)
    (hComm : p.comp O = O.comp p) : O = 0 := by
  ext v
  apply hpInjective
  have hcomm := LinearMap.congr_fun hComm v
  have hkill := LinearMap.congr_fun hOp v
  have hpOv : p (O v) = 0 := by
    rw [show p (O v) = O (p v) by simpa [LinearMap.comp_apply] using hcomm]
    simpa [LinearMap.comp_apply] using hkill
  simpa using hpOv

section StarObstruction

variable {W : Type*} [NormedAddCommGroup W] [InnerProductSpace ℂ W]

/-- If `p` is symmetric and injective on a carrier, a right-killing map with
an adjoint that also acts on that same carrier has zero adjoint. -/
theorem adjoint_zero_of_injective_symmetric_kills_right
    (p O Ostar : Module.End ℂ W) (hpInjective : Function.Injective p)
    (hpSymmetric : ∀ u v : W, inner ℂ (p u) v = inner ℂ u (p v))
    (hAdjoint : ∀ u v : W, inner ℂ (O u) v = inner ℂ u (Ostar v))
    (hOp : O.comp p = 0) : Ostar = 0 := by
  ext v
  apply hpInjective
  have horthogonal : ∀ u : W, inner ℂ u (p (Ostar v)) = 0 := by
    intro u
    calc
      inner ℂ u (p (Ostar v)) = inner ℂ (p u) (Ostar v) :=
        (hpSymmetric u (Ostar v)).symm
      _ = inner ℂ (O (p u)) v := (hAdjoint (p u) v).symm
      _ = 0 := by
        have h := LinearMap.congr_fun hOp u
        rw [show O (p u) = 0 by simpa [LinearMap.comp_apply] using h]
        simp
  have hself : inner ℂ (p (Ostar v)) (p (Ostar v)) = 0 :=
    horthogonal (p (Ostar v))
  simpa using (inner_self_eq_zero.mp hself)

/-- Under the same carrier assumptions the proposed lift itself is zero. -/
theorem zero_of_injective_symmetric_adjoint_kills_right
    (p O Ostar : Module.End ℂ W) (hpInjective : Function.Injective p)
    (hpSymmetric : ∀ u v : W, inner ℂ (p u) v = inner ℂ u (p v))
    (hAdjoint : ∀ u v : W, inner ℂ (O u) v = inner ℂ u (Ostar v))
    (hOp : O.comp p = 0) : O = 0 := by
  have hOstar := adjoint_zero_of_injective_symmetric_kills_right
    p O Ostar hpInjective hpSymmetric hAdjoint hOp
  ext u
  apply inner_self_eq_zero.mp
  calc
    inner ℂ (O u) (O u) = inner ℂ u (Ostar (O u)) := hAdjoint u (O u)
    _ = 0 := by rw [LinearMap.congr_fun hOstar]; simp

end StarObstruction

end CptSewing.QuotientLift
