import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Tactic.Ring

/-!
# Abstract constrained dual algebra

This module separates the finite linear-algebraic consequence of a Green
identity from its analytic inputs.  In particular, it does not construct a
Cauchy solution, establish a Green identity for a differential operator, or
identify a kinematic conjugation with a full CPT action.

The hypotheses named `greenH`, `greenP`, `onShellH`, `onShellP`, and `witness`
are the places where a concrete analytic construction must supply evidence.
The Green hypotheses are deliberately pointwise in the selected bulk vector:
they do not assert that a boundary condition is preserved on every vector of
the ambient bulk space.
-/

namespace CptSewing.ConstrainedDual

open Module

variable {V S : Type*} [AddCommGroup V] [Module ℂ V]
variable [AddCommGroup S] [Module ℂ S]

/-- Dual functionals which annihilate both declared constraint ranges. -/
def constrainedDual (H p : Module.End ℂ V) : Submodule ℂ (Module.Dual ℂ V) :=
  H.dualMap.ker ⊓ p.dualMap.ker

/-- Membership spells out the two constraint-annihilation conditions. -/
theorem mem_constrainedDual_iff (H p : Module.End ℂ V) (T : Module.Dual ℂ V) :
    T ∈ constrainedDual H p ↔ T.comp H = 0 ∧ T.comp p = 0 := by
  rfl

/-- A constrained dual functional kills the `H` constraint pointwise. -/
theorem constrainedDual_apply_H {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u : V) :
    T (H u) = 0 := by
  exact LinearMap.congr_fun hT.1 u

/-- A constrained dual functional kills the `p` constraint pointwise. -/
theorem constrainedDual_apply_p {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u : V) :
    T (p u) = 0 := by
  exact LinearMap.congr_fun hT.2 u

/-- The span of both constraint ranges lies in the kernel of every constrained dual. -/
theorem constraint_span_le_ker {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) :
    Submodule.span ℂ (Set.range H ∪ Set.range p) ≤ T.ker := by
  refine Submodule.span_le.2 ?_
  intro x hx
  rcases hx with hx | hx
  · rcases hx with ⟨u, rfl⟩
    exact LinearMap.mem_ker.mpr (constrainedDual_apply_H hT u)
  · rcases hx with ⟨u, rfl⟩
    exact LinearMap.mem_ker.mpr (constrainedDual_apply_p hT u)

/-- The selected rank-one sesquilinear coefficient form. -/
def inducedForm (T : Module.Dual ℂ V) (u v : V) : ℂ :=
  starRingEnd ℂ (T u) * T v

/-- The induced form annihilates `H` in its left slot. -/
theorem inducedForm_H_left {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u v : V) :
    inducedForm T (H u) v = 0 := by
  simp [inducedForm, constrainedDual_apply_H hT u]

/-- The induced form annihilates `H` in its right slot. -/
theorem inducedForm_H_right {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u v : V) :
    inducedForm T u (H v) = 0 := by
  simp [inducedForm, constrainedDual_apply_H hT v]

/-- The induced form annihilates `p` in its left slot. -/
theorem inducedForm_p_left {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u v : V) :
    inducedForm T (p u) v = 0 := by
  simp [inducedForm, constrainedDual_apply_p hT u]

/-- The induced form annihilates `p` in its right slot. -/
theorem inducedForm_p_right {H p : Module.End ℂ V} {T : Module.Dual ℂ V}
    (hT : T ∈ constrainedDual H p) (u v : V) :
    inducedForm T u (p v) = 0 := by
  simp [inducedForm, constrainedDual_apply_p hT v]

/-- A nonzero analytic witness gives a strictly positive diagonal coefficient. -/
theorem inducedForm_diag_pos {T : Module.Dual ℂ V} {w : V}
    (hw : T w ≠ 0) :
    0 < (inducedForm T w w).re := by
  have hdiag : (inducedForm T w w).re = Complex.normSq (T w) := by
    unfold inducedForm
    rw [← Complex.normSq_eq_conj_mul_self]
    simp
  rw [hdiag]
  exact Complex.normSq_pos.mpr hw

/-- A separator witness proves that two choices have different quotient kernels. -/
theorem kernels_ne_of_separator (T U : Module.Dual ℂ V) (w : V)
    (hTw : T w = 0) (hUw : U w ≠ 0) :
    T.ker ≠ U.ker := by
  intro hker
  apply hUw
  apply LinearMap.mem_ker.mp
  rw [← hker]
  exact LinearMap.mem_ker.mpr hTw

/--
A selected Green-compatible bulk vector produces a constrained dual functional.

`greenH` and `greenP` are hypotheses supplied by an analytic Green identity;
`onShellH` and `onShellP` are the separate bulk on-shell hypotheses.
-/
theorem pairing_mem_constrainedDual
    (H p : Module.End ℂ V) (A B : Module.End ℂ S)
    (pair : S →ₗ[ℂ] Module.Dual ℂ V) (s : S)
    (greenH : ∀ u, pair s (H u) = pair (A s) u)
    (greenP : ∀ u, pair s (p u) = -(pair (B s) u))
    (onShellH : A s = 0) (onShellP : B s = 0) :
    pair s ∈ constrainedDual H p := by
  refine (mem_constrainedDual_iff H p (pair s)).2 ⟨?_, ?_⟩
  · ext u
    rw [LinearMap.comp_apply, greenH, onShellH]
    simp
  · ext u
    rw [LinearMap.comp_apply, greenP, onShellP]
    simp

/-- A selected Green-compatible on-shell vector with an explicit witness is a nonzero constrained dual. -/
theorem pairing_onShell_nonzero_constrainedDual
    (H p : Module.End ℂ V) (A B : Module.End ℂ S)
    (pair : S →ₗ[ℂ] Module.Dual ℂ V) (s : S) (w : V)
    (greenH : ∀ u, pair s (H u) = pair (A s) u)
    (greenP : ∀ u, pair s (p u) = -(pair (B s) u))
    (onShellH : A s = 0) (onShellP : B s = 0)
    (witness : pair s w ≠ 0) :
    ∃ T ∈ constrainedDual H p, T ≠ 0 := by
  refine ⟨pair s, pairing_mem_constrainedDual H p A B pair s greenH greenP onShellH onShellP, ?_⟩
  intro hzero
  apply witness
  rw [hzero]
  rfl

end CptSewing.ConstrainedDual
