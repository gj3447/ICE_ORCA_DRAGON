import Mathlib.Data.Set.Function
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Data.Complex.Basic

/-!+# Algebraic repaired boundary carrier and the minimal two-ghost complex

The boundary map and constraint maps are abstract inputs. These statements prove
closure of the iterated-boundary carrier and the coefficient complex; they do not
prove a differential-operator realization, a graph norm closure, or self-adjointness.
The primary injectivity hypothesis in the last theorem is supplied analytically
by compact N-collars in the previous audit. It is not assumed for dual states.
-/

namespace CptSewing.BFVCore

section Carrier

variable {V B : Type*}

/-- All iterated boundary conditions, with a declared zero boundary value. -/
def repairedCore (H p : V → V) (boundary : V → B) (zeroBoundary : B) : Set V :=
  {v | ∀ k m : ℕ, boundary ((H^[k]) ((p^[m]) v)) = zeroBoundary}

theorem core_boundary (H p : V → V) (boundary : V → B) (z : B)
    {v : V} (hv : v ∈ repairedCore H p boundary z) : boundary v = z := by
  simpa only [Function.iterate_zero_apply] using hv 0 0

theorem core_primary_stable (H p : V → V) (boundary : V → B) (z : B) :
    Set.MapsTo p (repairedCore H p boundary z) (repairedCore H p boundary z) := by
  intro v hv k m
  simpa only [Function.iterate_succ_apply] using hv k (m + 1)

theorem core_H_stable (H p : V → V) (boundary : V → B) (z : B)
    (commute : Function.Commute H p) :
    Set.MapsTo H (repairedCore H p boundary z) (repairedCore H p boundary z) := by
  intro v hv k m
  rw [← commute.iterate_right m v]
  simpa only [Function.iterate_succ_apply] using hv (k + 1) m

/-- Every carrier stable under both maps and satisfying the boundary condition
is contained in the iterated carrier. No completeness or topology is asserted. -/
theorem stable_boundary_carrier_subset_core (H p : V → V) (boundary : V → B)
    (z : B) (D : Set V) (stableH : Set.MapsTo H D D) (stableP : Set.MapsTo p D D)
    (traceZero : ∀ v ∈ D, boundary v = z) : D ⊆ repairedCore H p boundary z := by
  intro v hv k m
  exact traceZero _ (stableH.iterate k (stableP.iterate m hv))

end Carrier

section MinimalComplex

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- Degree zero to degree one, ordered as coefficients of c and rho. -/
def d0 (H p : V →ₗ[ℂ] V) (v : V) : V × V := (H v, p v)

/-- Degree one to degree two, with coefficient H beta - p alpha. -/
def d1 (H p : V →ₗ[ℂ] V) (v : V × V) : V := H v.2 - p v.1

theorem minimal_complex_square_zero (H p : V →ₗ[ℂ] V)
    (commute : Function.Commute (H : V → V) (p : V → V)) (v : V) :
    d1 H p (d0 H p v) = 0 := by
  change H (p v) - p (H v) = 0
  exact sub_eq_zero.mpr (commute v)

theorem degree_zero_closed_iff (H p : V →ₗ[ℂ] V) (v : V) :
    d0 H p v = 0 ↔ H v = 0 ∧ p v = 0 := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · intro h
    exact Prod.ext h.1 h.2

/-- A primary-injective test carrier has no nonzero degree-zero cycles.
This theorem concerns tests, not the dual of that carrier. -/
theorem degree_zero_trivial_of_primary_injective (H p : V →ₗ[ℂ] V)
    (primaryInjective : Function.Injective (p : V → V)) (v : V) :
    d0 H p v = 0 ↔ v = 0 := by
  constructor
  · intro hv
    apply primaryInjective
    simpa only [map_zero] using ((degree_zero_closed_iff H p v).mp hv).2
  · intro hv
    subst v
    simp [d0]

end MinimalComplex

end CptSewing.BFVCore
