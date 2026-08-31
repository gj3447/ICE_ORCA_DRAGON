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

## Execution history

The first command stopped before calculation because the upstream decimal
integrity guard sent a long decimal string through an integer-only `fmpq`
constructor. No result was written. Commit `1b160df` changed only that guard
to exact SymPy rational parsing.

The next clean committed execution was:

```text
./ice run raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport
```

It returned `VALID_RUN` and
`UNRESOLVED_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_TRANSPORT`. The common
actual-sensitivity and MVT envelopes at the switch were

```text
[0.08636945814095968, 0.14690505220523635]
```

and both actual-rho boxes had width about `1.772e-5`, below the declared
`1e-4` target. However, all four side controls failed. The raw result SHA-256
was `56131512878c652e3b91e5b0d144d9824adb2a252f9f6c964a880fbc1e992876`.

Inspection localized the failure to generic symmetric-ball multiplication of
the sign-fixed lambda interval by positive `p`. It was rigorous but wider than
the four-endpoint real interval product and crossed the lambda-zero Bessel
base artificially. Commit `ddeba15` replaces only this multiplication with
the outward endpoint-product hull.

The clean committed rerun of the same command then returned `VALID_RUN` and

```text
CERTIFY_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_SWITCH_SENSITIVITY_AND_DIRECTION_SIGN
```

All 7 exact identities, 13 outward controls and 3 theorem-scope guards passed.
The 80/120-decimal intersection gives, separately for both punctured lambda
boxes,

```text
s(Q_switch), p(Q_switch)
  in [0.0863694581409596797514691277026974,
      0.1469050522052363452006115837573849].
```

The lambda-zero Bessel direction at the switch is enclosed by

```text
[-0.5525229389240662628288325668436928,
 -0.5525229389240662628288325667475361].
```

For the negative lambda box the actual direction lies in

```text
[-0.5525376294293425688154136669149152,
 -0.5525229397877114750515509303917638],
```

strictly below the Bessel box. For the positive lambda box it lies in

```text
[-0.5525229380604210506061142031994651,
 -0.5525082484187899568422514666763137],
```

strictly above it. Both actual-direction widths are
`1.4689641631093763863e-5`, below the declared `1e-4` target.

The final result SHA-256 is
`d326398ac06e36b55dfe49a565f72de223fabe68a68907d6aa128ea09a4aef3b`;
the runner and input hashes recorded inside it are respectively
`a87af1f9450016027e5e6e54b93904ed65e8ebf2b7118d238f9959133626f6d4`
and `194b219f1b5b8740acd6ffa36c7d6980e02285a89a7b14eb8bb77c49e32010e9`.

This closes only the Bessel-relative switch certificate. Panel-specific
absolute-rho Picard tubes, differentiated node-safe transfer from
`Q_switch` to `Q0=-4`, the complete declared minus-tail Gamma_1 functional,
Gamma_1 sign, root continuation and every spectral, RAQ or physical output
remain null.
