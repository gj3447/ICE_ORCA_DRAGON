# Declared raw-\(C\) constant-boundary direct-integral extension

## Question and scope

The preceding raw-\(C\) audit classified the declared weighted fibers but deliberately
selected no boundary condition.  This independent, non-numbered calculation declares
one additional datum in order to test the direct-integral step itself:

\[
\Gamma_{1,p}u=0\qquad\text{for Lebesgue-a.e. }p.
\]

It is a constant line in the real reference-boundary coordinates below.  It is not
necessarily constant in travelling-wave coordinates, and it is not derived from
\(H=fC\), parity, RAQ, BFV, or a physical boundary principle.

The calculation may establish only one selected, \(p\)-preserving decomposable
self-adjoint extension of the already declared raw-\(C\) differential expression.  It
does not construct a raw-\(C\) spectral transform, group average, rigging map,
physical inner product, \(C/H\) equivalence, or a general extension that mixes
different \(p\) fibers.

## Declared reference field

For

\[
C_p=f^{-1}\left[2\hbar^2\partial_Q^2+3p^2-72\pi^4e^{2Q}\right],
\qquad f(Q)=12\pi^2e^{3Q/2},
\]

let \(c_p,s_p\) be the real zero-energy pair fixed at \(Q_0=-4\):

\[
2\hbar^2y''+(3p^2-72\pi^4e^{2Q})y=0,
\]

\[
c_p(-4)=1,\quad c_p'(-4)=0,\qquad
s_p(-4)=0,\quad s_p'(-4)=1.
\]

There is no first-derivative term, hence

\[
W(c_p,s_p)=1.
\]

At the limit-circle minus end, define maximal-domain boundary maps by Wronskian
limits:

\[
\Gamma_{0,p}u=\lim_{Q\to-\infty}W(u,s_p),\qquad
\Gamma_{1,p}u=-\lim_{Q\to-\infty}W(u,c_p).
\]

The scalar Green form is proportional to

\[
\overline{\Gamma_{0,p}u}\Gamma_{1,p}v
-\overline{\Gamma_{1,p}u}\Gamma_{0,p}v.
\]

Thus \(\Gamma_{1,p}=0\) is Lagrangian.  With the previously pinned one-limit-circle,
one-limit-point classification, the relevant fiber domain is

\[
\mathcal D(C_{p,\Gamma})=
\{u\in\mathcal D(C_{p,\max}):\Gamma_{1,p}u=0\}.
\]

## Measurable direct-integral obligation

The coefficient and the finite-\(Q\) initial data depend continuously and evenly on
\(p\).  Initial-value parameter dependence therefore supplies a continuous, hence
measurable, reference field on compact \(Q\) intervals.  The runner then applies a
separately named measurable-extension theorem guard: a measurable Wronskian
boundary graph together with the pinned maximal-fiber field gives weak measurability
of one nonreal resolvent on a countable dense compact-support set.  Subject to that
explicit theorem scope, direct-integral theory gives

\[
C_\Gamma=\int_{\mathbb R}^{\oplus} C_{p,\Gamma}\,dp,
\]

with graph-norm domain

\[
\mathcal D(C_\Gamma)=
\left\{\psi:\ \psi(p)\in\mathcal D(C_{p,\Gamma})\ \mathrm{a.e.},\
\int\|C_{p,\Gamma}\psi(p)\|^2dp<\infty\right\}.
\]

This is one declared construction only.  It does not classify the general
von-Neumann unitary between the full deficiency spaces, which can mix \(p\)
fibers.

Because the coefficient and the normalized pair are even in \(p\),

\[
(P\psi)(p,Q)=\psi(-p,Q)
\]

preserves the declared domain.  The singleton \(p=0\) is still Lebesgue-null;
parity invariance does not create an origin atom or a \(p>0/p<0\) gluing law.

## Bounded diagnostics and fail-closed boundary

The runner uses finite-interval initial-value diagnostics from \(Q_0=-4\) to the
endpoint-near compact set \(Q\in\{-8,-6,-4,-3\}\), only for Wronskian conservation
and \(p\leftrightarrow-p\) parity.  Those diagnostics do not compute
endpoint limits, nonreal resolvents, spectral density, or a group average.

The result must leave the following null: raw-\(C\) spectral resolution, raw-\(C\)
rigging map and physical product, \(C/H\) equivalence or unitary intertwiner,
general \(p\)-mixing extensions, origin/gluing data, endpoint transform, absolute
BFV measure, inhomogeneous closure, quantum anomaly, relational/decoherence and
observational claims.

## Intended execution

After independent review, clean commit, and only through the repository control
plane:

```text
./ice run raw_c_constant_boundary_direct_integral
```

No command has been run while this draft is being prepared.
