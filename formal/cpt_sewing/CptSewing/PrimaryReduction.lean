import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Dual.Defs

/-!
The primary-constraint contraction of a two-constraint complex. The analytic
integral operators and Cauchy uniqueness are supplied in the adjacent derivation;
this file proves the algebraic chain maps, homotopy and exactness criteria.
-/

namespace CptSewing.PrimaryReduction

variable {V E : Type*} [AddCommGroup V] [Module ℂ V]
  [AddCommGroup E] [Module ℂ E]

def q0 (H p : Module.End ℂ V) (u : V) : V × V := (H u, p u)
def q1 (H p : Module.End ℂ V) (xy : V × V) : V := H xy.2 - p xy.1

theorem project_q0 (H p : Module.End ℂ V) (R : V →ₗ[ℂ] E)
    (hRp : ∀ u, R (p u) = 0) (u : V) : R (q0 H p u).2 = 0 := hRp u

theorem project_q1 (H p : Module.End ℂ V) (h : Module.End ℂ E)
    (R : V →ₗ[ℂ] E) (hRp : ∀ u, R (p u) = 0)
    (hRH : ∀ u, R (H u) = h (R u)) (xy : V × V) :
    R (q1 H p xy) = h (R xy.2) := by
  simp [q1, hRH, hRp]

theorem include_chain (H p : Module.End ℂ V) (h : Module.End ℂ E)
    (J : E →ₗ[ℂ] V) (hHJ : ∀ e, H (J e) = J (h e)) (e : E) :
    q1 H p (0, J e) = J (h e) := by simp [q1, hHJ]

theorem projection_section (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hRJ : ∀ e, R (J e) = e) (e : E) : R (J e) = e := hRJ e

theorem homotopy_degree_zero (H p K : Module.End ℂ V)
    (hKp : ∀ u, K (p u) = u) (u : V) : K (q0 H p u).2 = u := hKp u

theorem homotopy_degree_one (H p K : Module.End ℂ V)
    (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hKp : ∀ u, K (p u) = u) (hpK : ∀ u, p (K u) = u - J (R u))
    (hHK : ∀ u, H (K u) = K (H u)) (xy : V × V) :
    q0 H p (K xy.2) + (-K (q1 H p xy), 0) = xy - (0, J (R xy.2)) := by
  apply Prod.ext
  · simp [q0, q1, hHK, hKp, sub_eq_add_neg, add_comm, add_left_comm]
  · simp [q0, hpK]

theorem homotopy_degree_two (H p K : Module.End ℂ V)
    (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hpK : ∀ u, p (K u) = u - J (R u)) (z : V) :
    q1 H p (-K z, 0) = z - J (R z) := by simp [q1, hpK]

theorem closed_degree_one_exact_of_reduced_injective
    (H p K : Module.End ℂ V) (h : Module.End ℂ E)
    (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hRp : ∀ u, R (p u) = 0) (hRH : ∀ u, R (H u) = h (R u))
    (hKp : ∀ u, K (p u) = u) (hpK : ∀ u, p (K u) = u - J (R u))
    (hHK : ∀ u, H (K u) = K (H u)) (hh : Function.Injective h)
    (xy : V × V) (hc : q1 H p xy = 0) : q0 H p (K xy.2) = xy := by
  have hRy : R xy.2 = 0 := by
    apply hh
    have hz := project_q1 H p h R hRp hRH xy
    simpa [hc] using hz.symm
  have he := homotopy_degree_one H p K R J hKp hpK hHK xy
  rw [hc, hRy, map_zero, map_zero, neg_zero] at he
  change q0 H p (K xy.2) + 0 = xy - 0 at he
  simpa only [add_zero, sub_zero] using he

theorem top_exact_iff_reduced_exact
    (H p K : Module.End ℂ V) (h : Module.End ℂ E)
    (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hRp : ∀ u, R (p u) = 0) (hRH : ∀ u, R (H u) = h (R u))
    (hHJ : ∀ e, H (J e) = J (h e))
    (hpK : ∀ u, p (K u) = u - J (R u)) (z : V) :
    (∃ xy, q1 H p xy = z) ↔ ∃ e, h e = R z := by
  constructor
  · rintro ⟨xy, he⟩
    refine ⟨R xy.2, ?_⟩
    rw [← project_q1 H p h R hRp hRH xy, he]
  · rintro ⟨e, he⟩
    refine ⟨(-K z, J e), ?_⟩
    simp only [q1, hHJ, he, map_neg, hpK, sub_neg_eq_add]
    simp [sub_eq_add_neg, add_left_comm]

theorem same_projection_diff_exact (H p K : Module.End ℂ V)
    (R : V →ₗ[ℂ] E) (J : E →ₗ[ℂ] V)
    (hpK : ∀ u, p (K u) = u - J (R u))
    (z w : V) (he : R z = R w) : q1 H p (-K (z - w), 0) = z - w := by
  simpa [map_sub, he] using homotopy_degree_two H p K R J hpK (z - w)

/-- A primary left inverse gives an explicit transpose preimage. Analytic
continuity of K, when available, makes this construction preserve continuous
functionals as well; continuity is not a hypothesis formalized here. -/
theorem dual_primary_right_inverse (p K : Module.End ℂ V)
    (hKp : ∀ u, K (p u) = u) (T : Module.Dual ℂ V) :
    (T.comp K).comp p = T := by
  ext u
  simp [LinearMap.comp_apply, hKp]

end CptSewing.PrimaryReduction
