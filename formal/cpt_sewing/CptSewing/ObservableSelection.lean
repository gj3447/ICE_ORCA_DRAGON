import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Tactic.Ring

/-!
# Observable selection for a rank-one constrained quotient

This is finite algebra.  It records what a nonzero functional must satisfy for
an endomorphism to preserve its kernel, and the resulting obstruction to a
noncommuting scalar commutator.  It neither constructs a differential
observable nor identifies an abstract endomorphism with a BFV or CPT sewing
operation.
-/

namespace CptSewing.ObservableSelection

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The kernel preservation condition required for an endomorphism to descend
to the quotient by a selected functional. -/
def PreservesKernel (T : V →ₗ[ℂ] ℂ) (O : Module.End ℂ V) : Prop :=
  ∀ ⦃v : V⦄, v ∈ T.ker → O v ∈ T.ker

/-- A nonzero linear functional has a vector on which it is nonzero. -/
theorem exists_nonzero_witness (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0) :
    ∃ w : V, T w ≠ 0 := by
  by_contra h
  apply hT
  ext v
  apply Classical.byContradiction
  intro hv
  exact h ⟨v, hv⟩

/-- Kernel preservation is exactly the common-eigenfunctional condition. -/
theorem preservesKernel_iff_exists_eigenvalue (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0)
    (O : Module.End ℂ V) :
    PreservesKernel T O ↔ ∃ eigenvalue : ℂ, ∀ v : V, T (O v) = eigenvalue * T v := by
  constructor
  · intro h
    obtain ⟨w, hw⟩ := exists_nonzero_witness T hT
    refine ⟨T (O w) * (T w)⁻¹, ?_⟩
    intro v
    have hker : v - (T v * (T w)⁻¹) • w ∈ T.ker := by
      change T (v - (T v * (T w)⁻¹) • w) = 0
      rw [map_sub, map_smul]
      simp only [smul_eq_mul]
      calc
        T v - (T v * (T w)⁻¹) * T w =
            T v - T v * ((T w)⁻¹ * T w) := by ring
        _ = 0 := by rw [inv_mul_cancel₀ hw, mul_one, sub_self]
    have hzero : T (O (v - (T v * (T w)⁻¹) • w)) = 0 := h hker
    rw [map_sub, map_smul, map_sub, map_smul] at hzero
    simp only [smul_eq_mul] at hzero
    calc
      T (O v) = (T v * (T w)⁻¹) * T (O w) := sub_eq_zero.mp hzero
      _ = (T (O w) * (T w)⁻¹) * T v := by ring
  · rintro ⟨eigenvalue, heigenvalue⟩ v hv
    change T (O v) = 0
    rw [heigenvalue v, hv]
    simp

/-- An explicit witness that the selected quotient kernel is not preserved. -/
theorem kernel_failure_of_witness (T : V →ₗ[ℂ] ℂ) (O : Module.End ℂ V)
    {u : V} (hu : T u = 0) (hOu : T (O u) ≠ 0) :
    ¬ PreservesKernel T O := by
  intro h
  exact hOu (h hu)

/-- Two common eigenfunctional actions kill their commutator in the selected
functional. -/
theorem commutator_killed_of_common_eigenfunctional
    (T : V →ₗ[ℂ] ℂ) (A B : Module.End ℂ V) (α β : ℂ)
    (hA : ∀ v : V, T (A v) = α * T v)
    (hB : ∀ v : V, T (B v) = β * T v) (v : V) :
    T ((A * B - B * A) v) = 0 := by
  simp only [LinearMap.sub_apply, Module.End.mul_apply, map_sub, hA, hB]
  ring

/-- A nonzero scalar commutator cannot act on a nonzero rank-one quotient. -/
theorem scalar_commutator_forces_functional_zero
    (T : V →ₗ[ℂ] ℂ) (A B : Module.End ℂ V) (α β z : ℂ)
    (hA : ∀ v : V, T (A v) = α * T v)
    (hB : ∀ v : V, T (B v) = β * T v)
    (hComm : ∀ v : V, (A * B - B * A) v = z • v) (hz : z ≠ 0) :
    T = 0 := by
  ext v
  have hkill := commutator_killed_of_common_eigenfunctional T A B α β hA hB v
  have hzero : z * T v = 0 := by
    calc
      z * T v = T (z • v) := by simp [smul_eq_mul]
      _ = T ((A * B - B * A) v) := by rw [hComm v]
      _ = 0 := hkill
  exact (mul_eq_zero.mp hzero).resolve_left hz

/-- If a constraint already annihilates the functional, its only possible
eigenvalue on a nonzero selected quotient is zero. -/
theorem constraint_eigenvalue_eq_zero (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0)
    (p : Module.End ℂ V) (eigenvalue : ℂ) (hp : T.comp p = 0)
    (hEigen : ∀ v : V, T (p v) = eigenvalue * T v) : eigenvalue = 0 := by
  obtain ⟨w, hw⟩ := exists_nonzero_witness T hT
  have hpw : T (p w) = 0 := by
    have := LinearMap.congr_fun hp w
    simpa [LinearMap.comp_apply] using this
  rw [hEigen w] at hpw
  exact (mul_eq_zero.mp hpw).resolve_right hw

/-- The selected rank-one form transforms by the eigenvalue in its right slot. -/
def rankOneForm (T : V →ₗ[ℂ] ℂ) (u v : V) : ℂ :=
  starRingEnd ℂ (T u) * T v

theorem rankOneForm_eigen_right (T : V →ₗ[ℂ] ℂ) (O : Module.End ℂ V)
    (eigenvalue : ℂ) (hEigen : ∀ v : V, T (O v) = eigenvalue * T v) (u v : V) :
    rankOneForm T u (O v) = eigenvalue * rankOneForm T u v := by
  simp only [rankOneForm, hEigen]
  ring

theorem rankOneForm_eigen_left (T : V →ₗ[ℂ] ℂ) (O : Module.End ℂ V)
    (eigenvalue : ℂ) (hEigen : ∀ v : V, T (O v) = eigenvalue * T v) (u v : V) :
    rankOneForm T (O u) v = starRingEnd ℂ eigenvalue * rankOneForm T u v := by
  simp only [rankOneForm, hEigen, map_mul]
  ring

end CptSewing.ObservableSelection
