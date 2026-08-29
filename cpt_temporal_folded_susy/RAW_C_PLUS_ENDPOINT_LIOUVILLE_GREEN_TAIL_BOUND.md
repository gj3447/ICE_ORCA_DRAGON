# Real raw-\(C\) plus-end Liouville--Green tail bound

## Narrow question

This draft bounds only the positive-\(Q\) tail of the declared real raw-\(C\)
fiber equation

\[
u''=A u,\qquad
A=36\pi^4e^{2Q}+6\pi^2\lambda e^{3Q/2}-\kappa^2,
\]

on

\[
Q\ge4,\qquad |\lambda|\le10^{-4},\qquad 0\le\kappa\le8,
\qquad p=\sqrt{2/3}\,\kappa .
\]

It is an analytic, bounded endpoint-tail diagnostic.  It deliberately does
not integrate from \(Q=4\) to \(Q_0=-4\), nor select a global fiber domain.

## Elementary uniform bound

Write \(A=A_0(1+\delta)\), where

\[
A_0=36\pi^4e^{2Q},\qquad
\delta=\frac{\lambda e^{-Q/2}}{6\pi^2}
  -\frac{\kappa^2e^{-2Q}}{36\pi^4}.
\]

Using only \(\pi>3\) and \(e^2>7\), the runner obtains rational uniform
envelopes on the full declared box:

\[
|\delta|\le d_0<\bar\eta=10^{-5},\qquad
|\delta'|\le2\bar\eta,\qquad |\delta''|\le4\bar\eta.
\]

Thus \(A>0\) without a turning point in this tail.  For the decaying
Liouville--Green proxy

\[
w=A^{-1/4}\exp\left(-\int_4^Q\sqrt{A(s)}\,ds\right),
\]

the exact residual is

\[
\frac{w''}{w}-A
=\frac{5(A')^2}{16A^2}-\frac{A''}{4A}
=\frac14+\frac{h}{4}+\frac{5h^2}{16}
 -\frac{\delta''}{4(1+\delta)},\qquad
h=\frac{\delta'}{1+\delta}.
\]

The last form gives the deliberately conservative bound

\[
|r|\le R_{\rm bar}
=\frac14+\frac{3\bar\eta}{2(1-\bar\eta)}
 +\frac{5\bar\eta^2}{4(1-\bar\eta)^2}.
\]

Consequently the source-form tail-control integral at \(Q_+=4\) is bounded
by

\[
V\le \frac{R_{\rm bar}e^{-4}}
 {6\pi^2\sqrt{1-\bar\eta}}
\le V_{\rm bar},
\]

where the second, rational bound uses \(e^{-4}<1/7^2\), \(\pi^2>9\), and
\(1/\sqrt{1-\bar\eta}\le1/(1-\bar\eta)\).

## What the cited theorem supplies

[DLMF §2.7(iii), especially 2.7.23--2.7.25](https://dlmf.nist.gov/2.7.iii)
is the only primary theorem source.  Once the runner has checked the
positive smooth tail and finite \(V_{\rm bar}\), this supports the stated
Liouville--Green error form

\[
f_{\mathrm{DLMF}}=A,\qquad g_{\mathrm{DLMF}}=0,\qquad
f_{\mathrm{DLMF}}^{-1/4}
\bigl(f_{\mathrm{DLMF}}^{-1/4}\bigr)''
=\frac{r}{\sqrt A},
\]

and hence

\[
|\epsilon|,\quad \tfrac12A^{-1/2}|\epsilon'|
\le E_{\rm bar}=e^{V_{\rm bar}/2}-1.
\]

For the recessive solution with the theorem's asymptotic normalization, the
runner also records

\[
\frac{|(\log u)'-(\log w)'|}{\sqrt A}
\le\frac{2E_{\rm bar}}{1-E_{\rm bar}}.
\]

This is a \(\sqrt A\)-normalized log-derivative *difference*, not a relative
error against \((\log w)'\).  It is a tail statement, not a propagated
statement at \(Q_0\).

## Explicit non-conclusions

No result from this calculation can supply any of the following:

- validated \(Q_+=4\to Q_0\) transport or an endpoint value of \(F\) or
  \(F_\lambda\);
- nonreal resolvent, Weyl \(m\)-function, spectral density, or a
  \(\delta(C)\) measure;
- a raw-\(C\) rigging map, physical inner product, or RAQ completion;
- quantum \(C\leftrightarrow H\) equivalence, BFV anomaly freedom,
  phenomenology, a physics claim, or a TOE claim.

The input hash-pins the prior operator-domain, direct-integral,
zero-shell-census, and finite-cutoff local \(F_\lambda\) results precisely so
this tail calculation cannot silently promote any of their open obligations.

## Execution protocol

The definition alone is not a scientific result.  A clean committed runner
may be executed only through the repository control plane:

```text
./ice run raw_c_plus_endpoint_liouville_green_tail_bound
```
