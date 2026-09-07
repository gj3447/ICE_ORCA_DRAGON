import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Isomorphisms

/-!
# Rank-one positive quotient from a constrained dual functional

This file formalizes a deliberately small algebraic part of the dual-state
construction.  A nonzero complex-linear functional `T : V →ₗ[ℂ] ℂ` induces an
injective map from `V / ker T` to `ℂ`; because its codomain is one-dimensional,
nonzeroness makes that map surjective as well.  Pulling back `conj z * w`
therefore gives a positive definite rank-one form on that quotient.

The optional `quotientK` section only records a function which preserves the
kernel equivalence relation and has the declared conjugation covariance.  It
does not formalize an antilinear structure on `V`, ghosts, a BFV charge, a
CPT orientation reversal, an observable star algebra, or a physical Hilbert
space.
-/

namespace CptSewing.DualQuotient

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The quotient which removes the null directions of a dual functional. -/
abbrev StateQuotient (T : V →ₗ[ℂ] ℂ) := V ⧸ LinearMap.ker T

/-- `T` factored through its kernel quotient. -/
noncomputable def quotientFunctional (T : V →ₗ[ℂ] ℂ) : StateQuotient T →ₗ[ℂ] ℂ :=
  (LinearMap.ker T).liftQ T le_rfl

@[simp]
theorem quotientFunctional_mk (T : V →ₗ[ℂ] ℂ) (v : V) :
    quotientFunctional T (Submodule.Quotient.mk v) = T v :=
  rfl

/-- The induced functional has no remaining kernel. -/
theorem quotientFunctional_injective (T : V →ₗ[ℂ] ℂ) :
    Function.Injective (quotientFunctional T) := by
  apply LinearMap.ker_eq_bot.mp
  exact Submodule.ker_liftQ_eq_bot' _ _ rfl

/-- A nonzero complex-linear functional onto `ℂ` is surjective. -/
theorem functional_surjective_of_ne_zero (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0) :
    Function.Surjective T := by
  obtain ⟨v, hv⟩ : ∃ v : V, T v ≠ 0 := by
    by_contra h
    apply hT
    ext x
    apply Classical.byContradiction
    intro hx
    exact h ⟨x, hx⟩
  intro z
  refine ⟨(z * (T v)⁻¹) • v, ?_⟩
  rw [T.map_smul, smul_eq_mul, mul_assoc, inv_mul_cancel₀ hv, mul_one]

/-- The nonzero functional identifies its quotient with `ℂ`. -/
noncomputable def quotientEquivComplex (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0) :
    StateQuotient T ≃ₗ[ℂ] ℂ :=
  T.quotKerEquivOfSurjective (functional_surjective_of_ne_zero T hT)

@[simp]
theorem quotientEquivComplex_mk (T : V →ₗ[ℂ] ℂ) (hT : T ≠ 0) (v : V) :
    quotientEquivComplex T hT (Submodule.Quotient.mk v) = T v :=
  LinearMap.quotKerEquivOfSurjective_apply_mk T _ v

/-- The rank-one form induced by the quotient functional. -/
noncomputable def quotientForm (T : V →ₗ[ℂ] ℂ)
    (q r : StateQuotient T) : ℂ :=
  starRingEnd ℂ (quotientFunctional T q) * quotientFunctional T r

/-- The form is Hermitian. -/
theorem quotientForm_hermitian (T : V →ₗ[ℂ] ℂ) (q r : StateQuotient T) :
    starRingEnd ℂ (quotientForm T q r) = quotientForm T r q := by
  simp [quotientForm, mul_comm]

/-- The quotient form is linear in its right slot. -/
theorem quotientForm_add_right (T : V →ₗ[ℂ] ℂ)
    (q r s : StateQuotient T) :
    quotientForm T q (r + s) = quotientForm T q r + quotientForm T q s := by
  simp [quotientForm, mul_add]

/-- The quotient form is linear in its right slot over `ℂ`. -/
theorem quotientForm_smul_right (T : V →ₗ[ℂ] ℂ)
    (c : ℂ) (q r : StateQuotient T) :
    quotientForm T q (c • r) = c • quotientForm T q r := by
  simp [quotientForm, smul_eq_mul, mul_left_comm]

/-- The quotient form is conjugate-additive in its left slot. -/
theorem quotientForm_add_left (T : V →ₗ[ℂ] ℂ)
    (q r s : StateQuotient T) :
    quotientForm T (q + r) s = quotientForm T q s + quotientForm T r s := by
  simp [quotientForm, add_mul]

/-- The quotient form is conjugate-linear in its left slot over `ℂ`. -/
theorem quotientForm_smul_left (T : V →ₗ[ℂ] ℂ)
    (c : ℂ) (q r : StateQuotient T) :
    quotientForm T (c • q) r =
      starRingEnd ℂ c • quotientForm T q r := by
  simp [quotientForm, smul_eq_mul, mul_comm, mul_left_comm]

/-- Its diagonal is the ordinary complex norm square of the induced coordinate. -/
theorem quotientForm_diag_real (T : V →ₗ[ℂ] ℂ) (q : StateQuotient T) :
    (quotientForm T q q).re = Complex.normSq (quotientFunctional T q) := by
  unfold quotientForm
  rw [← Complex.normSq_eq_conj_mul_self]
  simp

/-- The quotient form has nonnegative real diagonal. -/
theorem quotientForm_diag_nonneg (T : V →ₗ[ℂ] ℂ) (q : StateQuotient T) :
    0 ≤ (quotientForm T q q).re := by
  rw [quotientForm_diag_real]
  exact Complex.normSq_nonneg _

/-- The only null vector of the induced form is the zero quotient class. -/
theorem quotientForm_diag_eq_zero_iff (T : V →ₗ[ℂ] ℂ) (q : StateQuotient T) :
    (quotientForm T q q).re = 0 ↔ q = 0 := by
  constructor
  · intro h
    apply quotientFunctional_injective T
    have hnorm : Complex.normSq (quotientFunctional T q) = 0 := by
      rwa [← quotientForm_diag_real]
    have hzero : quotientFunctional T q = 0 := Complex.normSq_eq_zero.mp hnorm
    simpa using hzero
  · rintro rfl
    simp [quotientForm, quotientFunctional]

/-- A kernel-respecting map on representatives descends to the quotient. -/
noncomputable def quotientK (T : V →ₗ[ℂ] ℂ) (K : V → V)
    (hK : ∀ ⦃x y : V⦄, x - y ∈ LinearMap.ker T → K x - K y ∈ LinearMap.ker T) :
    StateQuotient T → StateQuotient T :=
  Quotient.map' K (by
    intro x y hxy
    exact (LinearMap.ker T).quotientRel_def.mpr
      (hK ((LinearMap.ker T).quotientRel_def.mp hxy)))

/-- Conjugation covariance of `T` alone forces `K` to preserve the kernel relation. -/
theorem covariance_preserves_kernel (T : V →ₗ[ℂ] ℂ) (K : V → V)
    (hCov : ∀ v : V, T (K v) = starRingEnd ℂ (T v)) :
    ∀ ⦃x y : V⦄, x - y ∈ LinearMap.ker T → K x - K y ∈ LinearMap.ker T := by
  intro x y hxy
  change T (K x - K y) = 0
  have hxy_zero : T (x - y) = 0 := hxy
  calc
    T (K x - K y) = T (K x) - T (K y) := by rw [map_sub]
    _ = starRingEnd ℂ (T x) - starRingEnd ℂ (T y) := by rw [hCov, hCov]
    _ = starRingEnd ℂ (T (x - y)) := by simp only [map_sub]
    _ = starRingEnd ℂ 0 := by rw [hxy_zero]
    _ = 0 := by simp

@[simp]
theorem quotientK_mk (T : V →ₗ[ℂ] ℂ) (K : V → V) (hK) (v : V) :
    quotientK T K hK (Submodule.Quotient.mk v) = Submodule.Quotient.mk (K v) :=
  rfl

/-- An involution on representatives remains an involution after quotienting. -/
theorem quotientK_involutive (T : V →ₗ[ℂ] ℂ) (K : V → V) (hK)
    (hInv : Function.Involutive K) : Function.Involutive (quotientK T K hK) := by
  intro q
  refine Submodule.Quotient.induction_on _ q ?_
  intro v
  rw [quotientK_mk, quotientK_mk]
  exact congrArg Submodule.Quotient.mk (hInv v)

/-- Declared representative covariance gives quotient-level conjugation covariance. -/
theorem quotientFunctional_quotientK (T : V →ₗ[ℂ] ℂ) (K : V → V) (hK)
    (hCov : ∀ v : V, T (K v) = starRingEnd ℂ (T v)) (q : StateQuotient T) :
    quotientFunctional T (quotientK T K hK q) = starRingEnd ℂ (quotientFunctional T q) := by
  refine Submodule.Quotient.induction_on _ q ?_
  intro v
  simpa using hCov v

/-- Under the stated covariance assumption, the quotient form is `K`-covariant. -/
theorem quotientForm_quotientK_covariant (T : V →ₗ[ℂ] ℂ) (K : V → V) (hK)
    (hCov : ∀ v : V, T (K v) = starRingEnd ℂ (T v)) (q r : StateQuotient T) :
    quotientForm T (quotientK T K hK q) (quotientK T K hK r) =
      starRingEnd ℂ (quotientForm T q r) := by
  rw [quotientForm, quotientFunctional_quotientK T K hK hCov,
    quotientFunctional_quotientK T K hK hCov]
  simp [quotientForm]

end CptSewing.DualQuotient
