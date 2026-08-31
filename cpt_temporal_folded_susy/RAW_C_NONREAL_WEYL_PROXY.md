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
