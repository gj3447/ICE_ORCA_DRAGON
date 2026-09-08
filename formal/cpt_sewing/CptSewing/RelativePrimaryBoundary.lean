import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
Finite linear-generator model for the relative primary boundary reduction.

The slots (n, pi, rho, b) are ordinary complex coefficients; n denotes the
shifted tangent coefficient N - N0 at an endpoint. rho and b only record
odd-slot labels: this is neither a Grassmann superalgebra nor a
formalization of a BV measure, quantum pushforward, interval kernel, or
physical product. The signed super-BFV formulas are analytic inputs.
-/

namespace CptSewing.RelativePrimaryBoundary

abbrev Primary := Fin 4 → ℂ

def n (x : Primary) : ℂ := x 0
def pi (x : Primary) : ℂ := x 1
def rho (x : Primary) : ℂ := x 2
def b (x : Primary) : ℂ := x 3

def q (x : Primary) : Primary := fun i =>
  if i = 0 then -rho x else if i = 3 then pi x else 0

def qLin : Module.End ℂ Primary where
  toFun := q
  map_add' := by
    intro x y
    funext i
    fin_cases i
    · simp [q, rho, pi, add_comm]
    · simp [q, rho, pi]
    · simp [q, rho, pi]
    · simp [q, rho, pi]
  map_smul' := by
    intro c x
    funext i
    fin_cases i <;> simp [q, rho, pi]

def M (x : Primary) : Prop := pi x = 0 ∧ b x = 0
def PN0 (x : Primary) : Prop := n x = 0 ∧ rho x = 0

def mProj : Module.End ℂ Primary where
  toFun := fun x i => if i = 0 ∨ i = 2 then x i else 0
  map_add' := by
    intro x y
    funext i
    fin_cases i <;> simp
  map_smul' := by
    intro c x
    funext i
    fin_cases i <;> simp

def auxProj : Module.End ℂ Primary where
  toFun := fun x i => if i = 1 ∨ i = 3 then x i else 0
  map_add' := by
    intro x y
    funext i
    fin_cases i <;> simp
  map_smul' := by
    intro c x
    funext i
    fin_cases i <;> simp

/-- Scalar coefficient of pi delta-n plus b delta-rho. -/
def alphaCoeff (x : Primary) (dn drho : ℂ) : ℂ := pi x * dn + b x * drho

theorem q_nilpotent (x : Primary) : qLin (qLin x) = 0 := by
  funext i
  fin_cases i <;> simp [qLin, q, rho, pi]

theorem mProj_mem_M (x : Primary) : M (mProj x) := by
  constructor <;> simp [pi, b, mProj]

theorem auxProj_mem_PN0 (x : Primary) : PN0 (auxProj x) := by
  constructor <;> simp [n, rho, auxProj]

theorem projections_sum (x : Primary) : mProj x + auxProj x = x := by
  funext i
  fin_cases i <;> simp [mProj, auxProj]

theorem q_stable_M {x : Primary} (hx : M x) : M (qLin x) := by
  rcases hx with ⟨hpi, _⟩
  constructor
  · simp [pi, qLin, q]
  · simpa [b, qLin, q] using hpi

theorem q_stable_PN0 {x : Primary} (hx : PN0 x) : PN0 (qLin x) := by
  rcases hx with ⟨_, hrho⟩
  constructor
  · simpa [n, qLin, q] using hrho
  · simp [rho, qLin, q]

theorem q_mem_M_iff (x : Primary) : M (qLin x) ↔ pi x = 0 := by
  constructor
  · intro h
    have hb : b (qLin x) = 0 := h.2
    simpa [b, qLin, q] using hb
  · intro h
    constructor
    · simp [pi, qLin, q]
    · simpa [b, qLin, q] using h

theorem q_mem_PN0_iff (x : Primary) : PN0 (qLin x) ↔ rho x = 0 := by
  constructor
  · intro h
    have hn : n (qLin x) = 0 := h.1
    simpa [n, qLin, q] using hn
  · intro h
    constructor
    · simpa [n, qLin, q] using h
    · simp [rho, qLin, q]

theorem M_inter_PN0_eq_zero {x : Primary} (hM : M x) (hP : PN0 x) : x = 0 := by
  funext i
  fin_cases i
  · simpa [n] using hP.1
  · simpa [pi] using hM.1
  · simpa [rho] using hP.2
  · simpa [b] using hM.2

theorem alphaCoeff_vanishes_on_M {x : Primary} (hx : M x) (dn drho : ℂ) :
    alphaCoeff x dn drho = 0 := by
  rcases hx with ⟨hpi, hb⟩
  simp [alphaCoeff, hpi, hb]

theorem alphaCoeff_vanishes_on_PN0_tangent (x : Primary) :
    alphaCoeff x 0 0 = 0 := by
  simp [alphaCoeff]

theorem q_commutes_mProj : qLin.comp mProj = mProj.comp qLin := by
  apply LinearMap.ext
  intro x
  funext i
  fin_cases i <;> simp [LinearMap.comp_apply, qLin, q, mProj, rho, pi]

theorem q_commutes_auxProj : qLin.comp auxProj = auxProj.comp qLin := by
  apply LinearMap.ext
  intro x
  funext i
  fin_cases i <;> simp [LinearMap.comp_apply, qLin, q, auxProj, rho, pi]

end CptSewing.RelativePrimaryBoundary
