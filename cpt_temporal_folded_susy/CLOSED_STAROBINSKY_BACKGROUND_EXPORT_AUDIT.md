# Closed Starobinsky background export audit

## Scope

This independent bounded calculation derives leading potential-slow-roll
background quantities for

\[
V(\phi)=\frac{3M^2}{4}(1-e^{-\sqrt{2/3}\phi})^2
\]

in reduced Planck units.  It pins the historical Phase 19 evidence file as the
source of the improved-Cecotti potential, but does not run, copy, replay or
compare the historical bounce ODE calculation.

The input \(N_*\in\{50,55,60\}\) is a pivot e-fold parameter in the
potential integral.  It is not the historical closed-bounce \(N_{\rm acc}\),
and it supplies neither a reheating map nor an initial-condition selection.

## Exact formulas

With \(\alpha=\sqrt{2/3}\) and \(x=e^{-\alpha\phi}\),

\[
\frac{V'}V=\frac{2\alpha x}{1-x},\qquad
\epsilon_V=\frac{4}{3}\frac{x^2}{(1-x)^2},
\qquad
\eta_V=\frac{4}{3}\frac{x(2x-1)}{(1-x)^2}.
\]

The potential-slow-roll endpoint is

\[
t_{\rm end}=e^{\alpha\phi_{\rm end}}=1+\frac2{\sqrt3},
\qquad
\phi_{\rm end}=\alpha^{-1}\log t_{\rm end}.
\]

For \(t=e^{\alpha\phi}\), the pivot equation is

\[
N_* = \frac34\left[(t_*-\log t_*)
-(t_{\rm end}-\log t_{\rm end})\right].
\]

The export uses only

\[
H_*=\sqrt{V_*/3},\quad
\mathcal P_{\cal R}=\frac{V_*}{24\pi^2\epsilon_{V*}},\quad
\mathcal P_T=\frac{2H_*^2}{\pi^2},\quad
n_s=1-6\epsilon_{V*}+2\eta_{V*},\quad r=16\epsilon_{V*}.
\]

These are leading slow-roll background formulas.  They are not a closed-FRW
mode calculation, a Born--Oppenheimer/decoherence result, a Boltzmann-code
input, or an observational likelihood fit.

## Observed execution

The clean committed runner was executed through

```text
./ice run closed_starobinsky_background_export_audit
```

It returned
`KEEP_STAROBINSKY_LEADING_SLOW_ROLL_BACKGROUND_EXPORT_NOT_CLOSED_EVOLUTION_OR_LIKELIHOOD`.
All 6 exact checks and all 9 bounded residual checks passed.  The exported
central row at input `N_star=55` is

\[
\phi_*=5.3528685235,\quad H_*=6.4178161666\times10^{-6},\quad
\mathcal P_{\cal R}=2.3858758082\times10^{-9},
\]

\[
n_s=0.9649772222,\qquad r=0.0034982993.
\]

The result artifact SHA-256 is
`af6334f0c8a3f745ecfedd37280a8cae457f2ec7adfb5effb3b33f29dbc193e1`.
The historical Phase-19 evidence was hash-checked but its solver was not run.
All closed-mode, reheating, BO/decoherence, CLASS/Cobaya, likelihood, and
physical-claim fields remain null.
