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
