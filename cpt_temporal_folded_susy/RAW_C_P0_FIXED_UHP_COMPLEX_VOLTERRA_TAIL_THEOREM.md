# Raw-\(C\) \(p=0\) fixed-UHP complex Volterra tail theorem

## Decision and exact scope

This is one **supporting workbench theorem**, not a core Gate-1 result.  It asks
only whether the raw-\(C\) equation

\[
u''(Q)=A(Q,z)u(Q),\qquad
A=36\pi^4e^{2Q}+6\pi^2z e^{3Q/2},
\]

has a uniquely normalized recessive solution on

\[
Q\ge4,\qquad
\operatorname{Re}z\in[-1/16,1/16],\quad
\operatorname{Im}z\in[15/16,17/16],\qquad p=0,
\]

and whether its pair \((u(4,z),u'(4,z))\) can be enclosed outwardly.  It does
not transport that pair to \(Q_0=-4\), form a boundary ratio, or compute a
Weyl function.

The proof below is self-contained.  Olver is a complex progressive-path
method comparator, while [DLMF §2.7(iii)](https://dlmf.nist.gov/2.7#iii) is
used only as the official real-positive Liouville--Green comparator.  The
DLMF real theorem is not silently transferred to this complex coefficient.

## 1. A single analytic branch and a progressive path

Write

\[
A=36\pi^4e^{2Q}(1+\delta),\qquad
\delta(Q,z)=\frac{z e^{-Q/2}}{6\pi^2}.
\]

The closed target box lies strictly inside the open disk \(|z|<9/8\), since
its largest modulus is \(\sqrt{290}/16<9/8\).  For all \(z\) in that disk and
all \(Q\ge4\), the elementary bounds \(e^{-2}<1/7\) and \(\pi^2>9\) give

\[
|\delta|
<\frac{(9/8)(1/7)}{6\cdot9}
=\frac1{336}=:\eta<1.
\]

Consequently \(1+\delta\) stays in the right half-plane.  For the principal
square root,

\[
(\operatorname{Re}\sqrt w)^2
=\frac{|w|+\operatorname{Re}w}{2}
\ge \operatorname{Re}w,
\]

so taking \(w=1+\delta\) gives the lower bound used below.  Fix

\[
P(Q,z)=\sqrt{A(Q,z)}
=6\pi^2e^Q\sqrt{1+\delta(Q,z)}
\]

with both square roots principal.  The principal-square-root identity gives

\[
\operatorname{Re}P
\ge6\pi^2e^Q\sqrt{1-\eta}>0.
\]

With

\[
X(Q,z)=\int_4^Q P(t,z)\,dt,
\]

every forward segment of the real \(Q\) half-line is therefore progressive:

\[
\operatorname{Re}(X(s,z)-X(q,z))
\ge6\pi^2\sqrt{1-\eta}\,(e^s-e^q)>0
\quad(s>q\ge4).
\]

This statement is about the declared tail path.  It is not a Stokes-wall
classification for a family of distinct saddle critical values.

## 2. Exact Liouville--Green transform

Set

\[
u=P^{-1/2}W(X).
\]

Because \(X'=P\), the coefficient of \(W_X\) cancels exactly and direct
differentiation gives

\[
W_{XX}=(1+\psi)W,
\qquad
\psi=-\frac rA
=\frac{4AA''-5(A')^2}{16A^3},
\]

where

\[
r=\frac{(P^{-1/2})''}{P^{-1/2}}
=\frac{5(A')^2}{16A^2}-\frac{A''}{4A}.
\]

Here \(\delta'=-\delta/2\) and \(\delta''=\delta/4\), so another exact
simplification is

\[
r=\frac{16+20\delta+9\delta^2}{64(1+\delta)^2}.
\]

The runner checks all of these identities symbolically; the identity, not a
sampled residual, is used on the full half-line.

## 3. Volterra equation and contraction

Define the WKB reference and transformed correction by

\[
u_0=P^{-1/2}e^{-X},\qquad W=e^{-X}H.
\]

Variation of constants for \(W_{XX}-W=\psi W\), along the declared real
\(Q\) path, gives the exact equation

\[
H(q)=1+\frac12\int_q^\infty
\left[1-e^{-2(X(s)-X(q))}\right]
\psi(s)P(s)H(s)\,ds. \tag{1}
\]

Progressiveness implies

\[
\frac12\left|1-e^{-2(X(s)-X(q))}\right|\le1.
\]

The residual identity and \(|1+\delta|\ge1-\eta\) yield

\[
|r|\le
R_{\rm bar}:=
\frac{16+20\eta+9\eta^2}{64(1-\eta)^2},
\]

and hence

\[
\int_q^\infty|\psi P|\,ds
=\int_q^\infty\left|\frac rP\right|ds
\le\frac{R_{\rm bar}e^{-q}}
{6\pi^2\sqrt{1-\eta}}.
\]

At \(q=4\), using \(e^{-4}<1/49\), \(\pi^2>9\), and
\(1/\sqrt{1-\eta}\le1/(1-\eta)\), this is bounded by the exact rational

\[
V_{\rm bar}:=
\frac{R_{\rm bar}}{6\cdot9\cdot49(1-\eta)}
\approx9.5686003677\times10^{-5}<10^{-4}<1. \tag{2}
\]

Thus the right-hand side of (1) is a contraction on
\(C_b([q,\infty))\) with the supremum norm.  It has a unique fixed point and

\[
|H-1|\le q_{\rm bar},\qquad
q_{\rm bar}:=\frac{V_{\rm bar}}{1-V_{\rm bar}}
\approx9.5695160364\times10^{-5}. \tag{3}
\]

The same integrable majorant bounds the differentiated kernel, so dominated
convergence justifies differentiating the improper integral in (1) with
respect to \(X(q)\).  This gives

\[
H_X(q)=-\int_q^\infty
e^{-2(X(s)-X(q))}\psi(s)P(s)H(s)\,ds,
\]

so the same bound gives \(|H_X|\le q_{\rm bar}\).  The tail norm in (2)
tends to zero as \(q\to\infty\), hence \(H\to1\) and

\[
\lim_{Q\to\infty}\frac{u(Q,z)}{u_0(Q,z)}=1.
\]

The ratio limit fixes the scalar once the reference \(u_0\) has been defined;
the base choice \(X(4,z)=0\) fixes that reference convention.  Uniqueness is
only in this normalized bounded-\(H\) recessive class.

## 4. Parameter holomorphy

On the open disk \(|z|<9/8\), \(A\) is nonzero on the full tail and the
chosen branches, \(X\), \(\psi\), and the Volterra kernel are holomorphic in
\(z\).  The bound (2) is uniform.  The Neumann series therefore converges
normally on compact parameter subsets, so \(H\), \(u\), and \(u'\) are
holomorphic there.  This supplies an open neighborhood of the closed target
box; a closed rectangle by itself is not being called a holomorphy domain.

## 5. Outward endpoint enclosure

At \(Q_+=4\), \(X=0\).  Put

\[
\ell=\frac{P'}P=1-\frac{\delta}{4(1+\delta)}.
\]

Then

\[
u_0(4)=P(4)^{-1/2},\qquad
u_0'(4)=-\left(P(4)+\frac{\ell(4)}2\right)u_0(4),
\]

and (3) gives the uniform absolute corrections

\[
|u(4)-u_0(4)|\le |u_0(4)|q_{\rm bar},
\]

\[
|u'(4)-u_0'(4)|
\le q_{\rm bar}\left(|u_0'(4)|+|P(4)u_0(4)|\right). \tag{4}
\]

The runner evaluates the box-valued WKB pair and the exact rational constants
with outward `acb`/`arb` arithmetic at 128 and 256 bits.  It then adds the
full complex radius in (4) to each real and imaginary component.  This loses
correlation but is a safe rectangular enlargement.  No `acb` integral or
complex ODE solver is used; precision-tier overlap is only a same-backend
consistency check.

## Source boundary

- [Olver, *Asymptotics and Special Functions* (1997 reprint), Chapter 6](https://math.nist.gov/opsf/books/olver.html)
  is the standard comparison for complex-variable error bounds and progressive
  paths.  Equations (1)--(4) and every model-specific bound are nevertheless
  derived here.
- [DLMF §2.7(iii)](https://dlmf.nist.gov/2.7#iii) explicitly points to Olver
  for complex extensions; its displayed theorem is retained only as a
  real-positive comparator.
- [Eckhardt--Gesztesy--Nichols--Teschl, arXiv:1208.4677](https://arxiv.org/abs/1208.4677)
  remains the singular Weyl--Titchmarsh terminology baseline.  It does not turn
  this tail pair into \(m(z)\), a spectral measure, or RAQ.

## Run state and non-conclusions

The source definition has not yet entered Python execution.  An initial
control-plane attempt under the old stem
`raw_c_p0_fixed_uhp_complex_volterra_tail_theorem` was rejected with exit 2:
the `_p0_` substring matched the repository's numbered-Phase token guard.
No result was created.  The neutral runner stem below removes that naming
collision without changing the calculation.  After this rename is committed
cleanly, it must be run only through:

```text
./ice run raw_c_fixed_uhp_complex_volterra_tail_theorem
```

Even a passing run cannot establish any of the following:

- validated \(Q_+=4\to Q_0=-4\) transport or a boundary map;
- a nonzero denominator for a boundary ratio or a singular Weyl \(m(z)\);
- spectral measure or multiplicity, Stieltjes inversion, or nonzero-\(p\)
  direct-integral assembly;
- a rigging test space/map, physical product, or RAQ completion;
- \(C/H\) equivalence, Gate-1 core progress, a physics
  discovery, or a TOE claim.

Those fields remain explicitly null or false, and the runner never schedules
an automatic descendant.
