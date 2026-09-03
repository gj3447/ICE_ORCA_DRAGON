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

## Observed bounded run

The clean committed definition at
`949cb4b91beacb361faeef07215df15d77f46708` was executed through the repository
control plane:

```text
./ice run raw_c_fixed_uhp_complex_volterra_tail_theorem
```

It exited 0 and printed:

```text
RAW_C_P0_FIXED_UHP_COMPLEX_VOLTERRA_TAIL_THEOREM_RESULT={"automatic_next":null,"controls_passed":8,"controls_total":8,"result_sha256":"bcb823fe4857b196f01001bc15fe5a1122116e8f887b633b4e687669d297d32f","result_size_bytes":32782,"run_status":"VALID_RUN","theorem_guards_verified":2,"verdict":"CERTIFY_P0_FIXED_UHP_COMPLEX_TAIL_CONTRACTION_AND_RECESSIVE_QPLUS_ENCLOSURE"}
```

All eight controls and both theorem/scope guards passed.  The exact rational
bounds are

\[
V_{\rm bar}=\frac{120871}{1263204600}
=9.568600367668\ldots\times10^{-5},
\qquad
q_{\rm bar}=\frac{120871}{1263083729}
=9.569516036415\ldots\times10^{-5}.
\]

Both outward precision tiers returned the same displayed enclosure.  For the
whole declared \(z\) box,

\[
\operatorname{Re}u(4)\in
[0.01758442059068738,\ 0.01758904669168299],
\]

\[
\operatorname{Im}u(4)\in
[-1.23610560771409\times10^{-5},\ -7.73530591911376\times10^{-6}],
\]

\[
\operatorname{Re}u'(4)\in
[-56.88681021695615,\ -56.85282377603820],
\]

\[
\operatorname{Im}u'(4)\in
[-0.04946956370148212,\ -0.01548514480126426].
\]

The uniform correction radii used to enlarge the WKB box were
\(1.68302589657929\times10^{-6}\) for the value and
\(0.0108846625976797\) for the derivative.  These are enclosures of the
actual infinity-normalized recessive tail pair at \(Q_+=4\), not transport to
\(Q_0\) and not a boundary ratio.

Provenance:

- input SHA-256:
  `d17b1f1c4c6434bf233e6d4e14b6d3081d6412352193b7936c3dcb4650bd00de`;
- runner SHA-256:
  `d207e4a6493f689f69cf8106a6a05963a26f896c76abf5d342aabf2f5b666401`;
- result-file SHA-256:
  `bcb823fe4857b196f01001bc15fe5a1122116e8f887b633b4e687669d297d32f`;
- canonical payload SHA-256 with its self field removed:
  `a257f2efe4e8cd0b98f8fd2e17608a7f13f67d36f24c90033be33958b3e65e51`;
- runtime: Python 3.13.5, SymPy 1.14.0 and `python-flint==0.9.0`.

An independent read-only audit recomputed both result hashes, matched the
committed runner and input, checked all eight controls, both guards, the two
precision tiers and every null boundary, and found no scientific mismatch.
It identified the stale pre-run prose that this observed-run section now
replaces.

Two failed attempts are retained as implementation history, not scientific
evidence.  The old `_p0_` runner stem was rejected by the Phase-token guard
with exit 2 before Python execution.  The first neutral-stem run at commit
`e23fc58164ec3b636a78536a30913728051f5bd9` entered Python but exited 1 before
writing a result because `python-flint` 0.9 has no `acb.inv()` method.  Commit
`949cb4b` replaced it with `acb(1) / value`; only the subsequent exit-0 run is
evidence.

The earlier blocker note is intentionally retained at its input-pinned hash
as the historical no-run boundary.  This result supersedes its missing-tail
statement, but not its warning against calling an untransported WKB or
\(Q_+=4\) pair a Weyl endpoint certificate.

## Non-conclusions

This passing run does not establish any of the following:

- validated \(Q_+=4\to Q_0=-4\) transport or a boundary map;
- a nonzero denominator for a boundary ratio or a singular Weyl \(m(z)\);
- spectral measure or multiplicity, Stieltjes inversion, or nonzero-\(p\)
  direct-integral assembly;
- a rigging test space/map, physical product, or RAQ completion;
- \(C/H\) equivalence, Gate-1 core progress, a physics
  discovery, or a TOE claim.

Those fields remain explicitly null or false, and the runner never schedules
an automatic descendant.
