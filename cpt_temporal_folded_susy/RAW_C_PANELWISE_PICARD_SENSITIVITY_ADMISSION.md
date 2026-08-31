# Raw-C panelwise Picard sensitivity admission audit

This is intentionally a prerequisite audit, not a claimed Picard calculation.
The current sharp-direction result bounds the actual nonzero-lambda direction,
but all six endpoint intervals include zero and its nonlinear estimate is only
the global bound \(0\le J_{\rho^2}\le J_0\).

For one fixed plus-end normalization,

\[
(\partial_\lambda\rho)_x=
\left(2+\frac{1+2\rho}{x}\right)\partial_\lambda\rho-
\sqrt{\frac{x}{C}}.
\]

A rigorous affine panel calculation therefore requires an actual-lambda
normalized entering sensitivity interval, an outward rho tube plus Picard
remainder on every panel, and the actual declared Gamma_1 endpoint remainder.
The existing lambda-zero declared-boundary derivative and direction-only
Liouville--Green tail do not supply those inputs. The runner records that
absence and returns a fail-closed verdict; it never infers a sensitivity, sign,
root continuation, spectrum, RAQ, or physics result.

## Observed result (2026-08-31 UTC)

```text
./ice run raw_c_panelwise_picard_sensitivity_admission
VALID_RUN; exact 3/3; admitted=false
PANELWISE_PICARD_AFFINE_SENSITIVITY_NOT_ADMITTED
```

All six inherited endpoint intervals still contain zero.  The result names
three absent prerequisites: an actual nonzero-\(\lambda\) normalized
\(\partial_\lambda\rho(Q_+)\) enclosure, actual-\(\rho\) panel tubes with
Picard remainders, and a sharp actual declared-\(\Gamma_1\) remainder including
the complete minus tail.  No ODE, quadrature, root solve, finite difference or
sampling call was made.  The result file SHA-256 is
`086efedecc034e10e36ce2f306e2daf8255236aa3c67ea3e062c1e733f9883c4`.
