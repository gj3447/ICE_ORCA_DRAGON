import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Tactic.Ring

/-!
# Finite-rank corrections on a separated quotient carrier

This is abstract Hilbert-space algebra.  The analytic facts that a finite-rank
range lies in a chosen carrier, and that the Cauchy-dual span has trivial
intersection with that carrier, are hypotheses here.  No PDE, closure,
self-adjoint-extension, or BFV/CPT construction is formalized.
-/

namespace CptSewing.FiniteRankCorrection

variable {W E : Type*} [NormedAddCommGroup W] [InnerProductSpace ℂ W]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- Equality of quotient actions and the three displayed adjoint relations
force the corresponding adjoint intertwining. -/
theorem adjoint_intertwining_of_quotient_action
    (R : W →ₗ[ℂ] E) (Rstar : E →ₗ[ℂ] W)
    (K Kstar : Module.End ℂ W) (A Astar : Module.End ℂ E)
    (hRAdjoint : ∀ u e, inner ℂ (R u) e = inner ℂ u (Rstar e))
    (hKAdjoint : ∀ u v, inner ℂ (K u) v = inner ℂ u (Kstar v))
    (hAAdjoint : ∀ x e, inner ℂ (A x) e = inner ℂ x (Astar e))
    (hRK : R.comp K = A.comp R) :
    Kstar.comp Rstar = Rstar.comp Astar := by
  ext e
  apply ext_inner_left ℂ
  intro u
  have h := LinearMap.congr_fun hRK u
  calc
    inner ℂ u (Kstar (Rstar e)) = inner ℂ (K u) (Rstar e) :=
      (hKAdjoint u (Rstar e)).symm
    _ = inner ℂ (R (K u)) e := (hRAdjoint (K u) e).symm
    _ = inner ℂ (A (R u)) e := by
      rw [show R (K u) = A (R u) by simpa [LinearMap.comp_apply] using h]
    _ = inner ℂ (R u) (Astar e) := hAAdjoint (R u) e
    _ = inner ℂ u (Rstar (Astar e)) := hRAdjoint u (Astar e)

/-- If the adjoint image of the quotient-dual span lies in a carrier disjoint
from that span, a finite-rank correction has zero label adjoint action. -/
theorem label_adjoint_zero_of_range_separation
    (P : Submodule ℂ W) (R : W →ₗ[ℂ] E) (Rstar : E →ₗ[ℂ] W)
    (K Kstar : Module.End ℂ W) (A Astar : Module.End ℂ E)
    (hRAdjoint : ∀ u e, inner ℂ (R u) e = inner ℂ u (Rstar e))
    (hKAdjoint : ∀ u v, inner ℂ (K u) v = inner ℂ u (Kstar v))
    (hAAdjoint : ∀ x e, inner ℂ (A x) e = inner ℂ x (Astar e))
    (hRK : R.comp K = A.comp R)
    (hRange : ∀ e : E, Kstar (Rstar e) ∈ P)
    (hSeparated : ∀ e : E, Rstar e ∈ P → e = 0) : Astar = 0 := by
  have hInter := adjoint_intertwining_of_quotient_action
    R Rstar K Kstar A Astar hRAdjoint hKAdjoint hAAdjoint hRK
  ext e
  apply hSeparated
  have h := hRange e
  have hApply := LinearMap.congr_fun hInter e
  rw [show Kstar (Rstar e) = Rstar (Astar e) by
        simpa [LinearMap.comp_apply] using hApply] at h
  exact h

/-- A zero adjoint action forces the corresponding label action to vanish. -/
theorem label_zero_of_adjoint_zero
    (A Astar : Module.End ℂ E)
    (hAAdjoint : ∀ x e, inner ℂ (A x) e = inner ℂ x (Astar e))
    (hAstar : Astar = 0) : A = 0 := by
  ext x
  apply (inner_self_eq_zero (𝕜 := ℂ)).mp
  calc
    inner ℂ (A x) (A x) = inner ℂ x (Astar (A x)) := hAAdjoint x (A x)
    _ = 0 := by rw [LinearMap.congr_fun hAstar]; simp

/-- Combined finite-rank correction obstruction, with range and separation
supplied as explicit hypotheses rather than silently inferred from a PDE. -/
theorem label_zero_of_star_preserving_separated_correction
    (P : Submodule ℂ W) (R : W →ₗ[ℂ] E) (Rstar : E →ₗ[ℂ] W)
    (K Kstar : Module.End ℂ W) (A Astar : Module.End ℂ E)
    (hRAdjoint : ∀ u e, inner ℂ (R u) e = inner ℂ u (Rstar e))
    (hKAdjoint : ∀ u v, inner ℂ (K u) v = inner ℂ u (Kstar v))
    (hAAdjoint : ∀ x e, inner ℂ (A x) e = inner ℂ x (Astar e))
    (hRK : R.comp K = A.comp R)
    (hRange : ∀ e : E, Kstar (Rstar e) ∈ P)
    (hSeparated : ∀ e : E, Rstar e ∈ P → e = 0) : A = 0 := by
  apply label_zero_of_adjoint_zero A Astar hAAdjoint
  exact label_adjoint_zero_of_range_separation P R Rstar K Kstar A Astar
    hRAdjoint hKAdjoint hAAdjoint hRK hRange hSeparated

/-- A bounded rank-one correction supported on a carrier vector. -/
noncomputable def rankOneCorrection (w : W) : Module.End ℂ W where
  toFun := fun u => inner ℂ w u • w
  map_add' := by
    intro u v
    rw [inner_add_right, add_smul]
  map_smul' := by
    intro c u
    rw [inner_smul_right, smul_smul]
    rfl

/-- The rank-one correction is self-adjoint for the declared inner product. -/
theorem rankOneCorrection_self_adjoint (w u v : W) :
    inner ℂ (rankOneCorrection w u) v = inner ℂ u (rankOneCorrection w v) := by
  simp [rankOneCorrection, inner_smul_left, inner_smul_right, inner_conj_symm]
  ring

/-- A rank-one correction made from a quotient-null vector is quotient-null. -/
theorem quotient_kills_rankOneCorrection
    (R : W →ₗ[ℂ] E) (w : W) (hw : R w = 0) :
    R.comp (rankOneCorrection w) = 0 := by
  ext u
  change R (inner ℂ w u • w) = 0
  rw [R.map_smul, hw, smul_zero]

/-- If a symmetric constraint is injective and `w` is nonzero, the quotient-null
rank-one correction is genuinely constraint-active: it does not kill `p` on
its right. -/
theorem rankOneCorrection_comp_constraint_ne_zero
    (p : Module.End ℂ W) (w : W) (hpInjective : Function.Injective p)
    (hpSymmetric : ∀ u v : W, inner ℂ (p u) v = inner ℂ u (p v))
    (hw : w ≠ 0) : (rankOneCorrection w).comp p ≠ 0 := by
  intro hComp
  have h := LinearMap.congr_fun hComp (p w)
  have hzero : inner ℂ w (p (p w)) • w = 0 := by
    simpa [rankOneCorrection, LinearMap.comp_apply] using h
  have hpw : p w ≠ 0 := by
    intro hpw
    apply hw
    apply hpInjective
    simpa using hpw
  have hnorm : inner ℂ (p w) (p w) ≠ 0 :=
    (inner_self_ne_zero (𝕜 := ℂ)).mpr hpw
  have hrewrite : inner ℂ w (p (p w)) = inner ℂ (p w) (p w) :=
    (hpSymmetric w (p w)).symm
  rw [hrewrite] at hzero
  exact hw ((smul_eq_zero.mp hzero).resolve_left hnorm)

end CptSewing.FiniteRankCorrection
