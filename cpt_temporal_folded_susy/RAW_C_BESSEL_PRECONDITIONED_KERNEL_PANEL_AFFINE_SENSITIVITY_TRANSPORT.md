# Raw-C Bessel-preconditioned kernel-panel affine transport

## Question and scope

For root bracket 1 and the two punctured real lambda boxes, this bounded
calculation asks whether the exact lambda-zero modified-Bessel direction and
the committed (s(4)=\partial_\lambda\rho(4)) anchor produce a positive
sensitivity and a narrow actual-direction tube at
(Q_{\mathrm{switch}}=-29/10).

It does **not** evaluate the declared \(\Gamma_1\), separate its sign, continue
a root, or construct Weyl, spectral, RAQ, quantum-gravity, or empirical data.

## Method

With (x=6\pi^2e^Q), subtract the exact lambda-zero Bessel Riccati solution
from the actual nonzero-lambda family.  Both

\[
p=\frac{\rho_\lambda-\rho_0}{\lambda},\qquad
s=\partial_\lambda\rho_\lambda
\]

obey affine equations whose coefficients lie between
(2-1/x) and (2+3/x) under the committed
(\rho_\lambda,\rho_0\in[-1,1]) barrier.  Their backward comparison kernels
are therefore

\[
e^{-2(t-a)}(a/t)^3,\qquad e^{-2(t-a)}(t/a).
\]

The exponential-weighted forcing integrals are enclosed by 512 and 1024
monotone kernel panels through (t-a=24); the remaining positive tail is
bounded analytically. Two Arb/acb precision tiers evaluate the exact Bessel
base and retain only overlapping outward intervals. The same conservative
coefficient envelope is evaluated separately for the pointwise sensitivity
`s` and the mean-value quotient `p`; equality of their reported outer boxes
does not identify the two functions.

“Kernel-panel” refers only to these monotone integral sums. This calculation
does not construct the panel-specific absolute rho Picard tubes required by
the later differentiated Gamma_1 transport.

## Execution

Pending clean committed-run execution:

```text
./ice run raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport
```

The raw result JSON is the check-ledger source of truth.  This report will be
updated with the observed verdict and intervals after that command runs.
