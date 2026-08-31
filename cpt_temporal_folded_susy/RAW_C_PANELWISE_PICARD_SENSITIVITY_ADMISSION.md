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
