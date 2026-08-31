# Raw-\(C\) nonreal Weyl proxy

## Narrow question

For the already declared \(p\)-preserving \(\Gamma_{1,p}=0\) extension, can a
finite-cutoff upper-half-plane calculation form a stable proxy

\[
M_{\rm cut}(z;p)=-\frac{\Gamma_{1,p}u_{+,z}}
                         {\Gamma_{0,p}u_{+,z}},
\qquad \operatorname{Im}z>0,
\]

without treating the previously computed real characteristic roots as a Weyl
function?  The operator-theoretic reference is Eckhardt--Gesztesy--Nichols--Teschl,
[arXiv:1208.4677v2](https://arxiv.org/abs/1208.4677v2).  That source fixes the
singular Weyl--Titchmarsh scope; it does not compute this fiber.

## Conventions and checks

The runner uses

\[
u''=\left(36\pi^4e^{2Q}+6\pi^2ze^{3Q/2}-\frac32p^2\right)u,
\qquad f(Q)=12\pi^2e^{3Q/2},
\]

and the zero-energy pair normalized at \(Q_0=-4\), with
\(\Gamma_0=W(u,s_p)\) and \(\Gamma_1=-W(u,c_p)\).  The minus sign in
\(M=-\Gamma_1/\Gamma_0\) compensates for the raw operator's positive
second-derivative convention.  On a finite interval,

\[
W(\bar u,u)'=i\,\operatorname{Im}(z)f|u|^2
\]

provides an independent sign and normalization check.

The preregistered grid is \(p\in\{0,1,2\}\) and
\(z\in\{i/2,i,1+i/2\}\).  It compares \(Q_+=1.6\) with \(1.4\),
\(Q_-=-14\) with \(-12\), DOP853 with tighter RK45, and \(p\) with \(-p\).

## Fail-closed scope

Even if every check passes, this is only a double-precision finite-cutoff
calibration.  It does not establish the singular endpoint limit, analytic Weyl
function, spectral measure or multiplicity, dense RAQ test space, positive
rigging form, physical product, or \(C/H\) equivalence.  A failed cutoff or
solver comparison leaves P4 at the selected-extension result.

## Execution

```text
./ice run raw_c_nonreal_weyl_proxy
```

The observed result is intentionally filled only after a clean committed runner
is executed through the workbench control plane.

## Observed result (2026-08-31 UTC)

```text
./ice run raw_c_nonreal_weyl_proxy
VALID_RUN; exact 5/5; numerical 72/72; theorem guards 4; ODE calls 54
KEEP_FINITE_CUTOFF_NONREAL_WEYL_PROXY_ONLY_SPECTRAL_MEASURE_RAQ_OPEN
```

Across the nine declared \((p,z)\) samples, every main proxy had positive
imaginary part, ranging from about `0.11832595` to `0.90739238`.  The maximum
finite Green--Lagrange relative residual was `4.2996e-11`; the maximum DOP853
versus tighter-RK45 shift was `3.0602e-10`; the maximum minus-cutoff shift was
`3.0229e-4`; the maximum plus-cutoff shift was `2.1124e-11`; and direct
\(p\leftrightarrow-p\) differences were zero at the recorded precision.

These controls support retaining the finite proxy only.  They do not validate
the singular endpoint limit or authorize Stieltjes inversion.  The next P4
question, if separately undertaken, is an interval-validated nonreal endpoint
construction followed by a separately controlled boundary-value/inversion
calculation.  The result file SHA-256 is
`b8d61b098128dde72aa2a9805b122dc4e2dd235efe9ca1c71d2b19da108d8ce3`.
