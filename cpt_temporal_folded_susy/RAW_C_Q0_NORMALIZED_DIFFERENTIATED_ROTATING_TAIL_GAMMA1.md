# Raw-C Q0-normalized differentiated rotating-tail Gamma_1 functional

## Question and scope

This bounded calculation takes the certified root-1 projective endpoint data
at \(Q_0=-4\) and asks whether the declared boundary functional divided by
that endpoint amplitude, together with its local \(\lambda\)-derivative, can
be enclosed after a finite left cutoff and an analytic complete-tail bound.

For \(U=u/u(Q_0)\), \(Z=\partial_\lambda U\), and the pinned
lambda-independent reference \(c_p\), it evolves

\[
Y=(U,U_Q,Z,Z_Q,c_p,c_{p,Q}).
\]

The Q0 seed is \(U=1\), \(U_Q=-x_0-1/2-\rho(Q_0)\), \(Z=0\),
\(Z_Q=-s(Q_0)\), \(c_p=1\), \(c_{p,Q}=0\). At each cutoff \(Q_c\),
the finite Wronskians receive analytic rotating-frame tail radii:

\[
g=\frac{\Gamma_{1,p}(u)}{u(Q_0)}=-W(U,c_p)(Q_c)+\operatorname{tail},
\qquad
\partial_\lambda g=-W(Z,c_p)(Q_c)+\operatorname{differentiated\ tail}.
\]

The scope is root bracket 1, the negative and positive punctured real
lambda boxes, plus a lambda-zero convention regression. It is a
Q0-normalized/projective functional calculation, not an absolute amplitude
calculation.

## Method and controls

The runner hash-pins the Q0 projective result and the selected declared
Gamma_1 boundary convention. It also hash-pins the older hybrid runner only
for its exact-rational interval-Taylor and whole-step-majorant semantics;
none of that runner's result is evidence here.

The six-state actual-derivative Taylor recurrence uses order 12 and complete
\(D_{13}|h|^{13}/13!\) remainders on the full parameter boxes. It uses

- \(Q_c=-10\) with 24 and 48 steps for discretization refinement;
- \(Q_c=-12\) with 32 steps for a complete-tail cutoff control;
- 80- and 120-decimal Arb tiers.

The left-tail radii bound both \(\lambda aUc_p\) and
\(aUc_p+\lambda aZc_p\). Thus the differentiated omitted tail is not
silently replaced by the older non-differentiated correction estimate.

## Explicit nonclaims

Even if a displayed finite interval happens to omit zero, this runner does
not claim an absolute actual \(\Gamma_1\) value or sign, a zero/root,
continuation or velocity. It also does not construct a Weyl function,
spectral measure, RAQ object, or physical/empirical result.

## Execution

This is pre-run. After the runner and input are committed, the only allowed
scientific execution is:

```text
./ice run raw_c_q0_normalized_differentiated_rotating_tail_gamma1
```

No result is recorded here yet. A result, if produced, must report the actual
command output, input/runner/result hashes, every failed control if any, and
the distinction between finite projective facts and all excluded claims.
