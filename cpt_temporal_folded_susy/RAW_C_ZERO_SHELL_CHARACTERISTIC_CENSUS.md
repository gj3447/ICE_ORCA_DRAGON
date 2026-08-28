# Declared raw-\(C\) zero-shell characteristic census

## Scope

This is a bounded characteristic-root census for one already declared raw-\(C\)
boundary line.  It does not compute a spectral measure or a physical Hilbert
space.

The pinned raw-\(C\) zero-energy fiber uses

\[
z=\frac{6\pi^2e^Q}{\hbar},
\qquad
\kappa=\sqrt{\frac32}\frac{|p|}{\hbar}.
\]

At positive real \(z\), the inherited plus-end limit-point classification
selects the decaying solution, up to scale,

\[
u_+(Q;\kappa)=K_{i\kappa}(z).
\]

The calculation fixes \(\hbar=1\), \(Q_0=-4\),

\[
z_0=6\pi^2e^{-4},\qquad \kappa\in[0,8],
\]

with 70-digit arithmetic, 2048 grid segments, 160 bisection steps per
sign-changing bracket, and a root-procedure cap of 32.

## Boundary reduction

The selected real reference pair is normalized by

\[
c_p(Q_0)=1,\qquad c_p'(Q_0)=0.
\]

The boundary convention is

\[
\Gamma_{1,p}(u)=-W(u,c_p)\big|_{Q_0}.
\]

For \(u=K_{i\kappa}(z)\), the sign is explicit:

\[
W(K,c_p)=Kc_p'-\partial_QK\,c_p=-\partial_QK
\quad\text{at }Q_0,
\]

and therefore

\[
\Gamma_{1,p}(K)=\partial_QK=z\partial_zK.
\]

The finite characteristic equation is consequently

\[
F(\kappa):=z_0\partial_zK_{i\kappa}(z_0)
=-\frac{z_0}{2}
\left[K_{i\kappa-1}(z_0)+K_{i\kappa+1}(z_0)\right]=0.
\]

For \(p=0\), \(\kappa=0\), and

\[
F(0)=z_0K_0'(z_0)=-z_0K_1(z_0)<0.
\]

Thus the origin is not a root of this declared characteristic condition.  This
does not add or exclude a separately declared origin-supported sector.

## Census protocol

The runner evaluates the recurrence form of \(F\) on the fixed grid, records
only adjacent intervals with a sign change, and refines each with bisection.
For every reported root it checks:

- recurrence residual;
- agreement with an independent centered \(z\)-derivative of \(K_{i\kappa}\);
- final bracket width;
- numerical imaginary residue at real \(\kappa,z_0\);
- root ordering and separation; and
- exact \(p\leftrightarrow-p\) parity.

The latter follows because \(\kappa\) contains \(|p|\): each listed
\(\kappa\) corresponds to both

\[
p=+\sqrt{\frac23}\kappa,
\qquad
p=-\sqrt{\frac23}\kappa
\quad(\hbar=1).
\]

This is specifically a sign-changing-grid census.  It does not rule out an
even-multiplicity, tangential, or sub-grid root.

## What this cannot establish

Even an exact census of the displayed roots would not be RAQ.  To form a
rigging contribution one still needs, at minimum,

\[
\frac{d\lambda_j(p)}{dp},
\]

or an appropriate transverse spectral-density replacement, together with
spectral normalization and a specified rigging-map test space.  This runner
does not calculate eigenvalue branches \(\lambda_j(p)\), their
transversality, \(\delta(C)\) derivative weights, a spectral measure, raw-\(C\)
group averaging, a physical inner product, or \(C\leftrightarrow H\)
equivalence.

It also leaves BFV, continuum determinant-line, inhomogeneous, observational,
physics, and TOE outputs null.

## Intended execution

After independent review and clean commit, use only the repository control
plane:

```text
./ice run raw_c_zero_shell_characteristic_census
```

No runner was executed during preparation of this draft.
