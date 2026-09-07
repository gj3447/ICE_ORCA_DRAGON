import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Normalized fixed-scale canonical BRST closure

These are finite real-polynomial consequences of the declared `a = 2`,
`p_a = 0` canonical face equations.  Here `p = p_phi / pi^2` and
`z = exp (-β φ)` is represented only by the real condition `0 < z`.

The mapping from the actual Starobinsky Hamiltonian and BRST vector field to
these normalized equations is an analytic/CAS-audited input.  This module does
not construct a boundary BFV manifold, a bulk-induced BV--BFV pair, a quantum
state, a CPT action, or a sewing kernel.
-/

namespace CptSewing.CanonicalBoundary

/-- The two normalized face equations force the exceptional potential value. -/
theorem potential_eq_two_thirds {p z : ℝ}
    (hH : p ^ 2 / 32 - 12 + 12 * (1 - z) ^ 2 = 0)
    (hHa : -3 * p ^ 2 / 64 - 6 + 18 * (1 - z) ^ 2 = 0) :
    (1 - z) ^ 2 = (2 : ℝ) / 3 := by
  nlinarith [hH, hHa]

/-- The same face equations fix the normalized scalar momentum square. -/
theorem momentum_sq_eq_128 {p z : ℝ}
    (hH : p ^ 2 / 32 - 12 + 12 * (1 - z) ^ 2 = 0)
    (hHa : -3 * p ^ 2 / 64 - 6 + 18 * (1 - z) ^ 2 = 0) :
    p ^ 2 = 128 := by
  nlinarith [hH, hHa]

/--
At the exceptional face root, the next free-ghost tangency coefficient cannot
vanish on the real positive-`z` body.  `p * z * (1-z) = 0` is the normalized
coefficient of the next BRST tangency condition, not a new ghost convention.
-/
theorem no_real_free_ghost_full_tangency {p z : ℝ}
    (hH : p ^ 2 / 32 - 12 + 12 * (1 - z) ^ 2 = 0)
    (hHa : -3 * p ^ 2 / 64 - 6 + 18 * (1 - z) ^ 2 = 0)
    (hz : 0 < z) (hnext : p * z * (1 - z) = 0) : False := by
  have hF : (1 - z) ^ 2 = (2 : ℝ) / 3 :=
    potential_eq_two_thirds hH hHa
  have hp2 : p ^ 2 = 128 := momentum_sq_eq_128 hH hHa
  rcases mul_eq_zero.mp hnext with hpz | hone
  · rcases mul_eq_zero.mp hpz with hp | hz0
    · rw [hp] at hp2
      norm_num at hp2
    · linarith
  · have hz1 : z = 1 := by linarith
    rw [hz1] at hF
    norm_num at hF

end CptSewing.CanonicalBoundary
