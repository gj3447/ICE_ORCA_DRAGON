# Raw-C Bessel-preconditioned node-safe switch-to-Q0 sensitivity transfer

## Question and scope

For root bracket 1 and the two punctured real lambda boxes, this bounded
calculation asks whether the certified actual direction and sensitivity at

\[
Q_{\mathrm{switch}}=-29/10
\]

can be transported to \(Q_0=-4\) without evolving a Riccati quotient through
the interior, where that quotient chart need not remain finite. The intended
outputs are only a finite endpoint
state and the projective quantities \(\rho(Q_0)\) and
\(s(Q_0)=\partial_\lambda\rho(Q_0)\).

It does **not** evaluate the declared \(\Gamma_1\), its complete minus-tail
remainder or sign, continue a root, or construct Weyl, spectral, RAQ or
physical data.

## Reused compact-transfer machinery

The runner hash-pins and imports the exact-rational partition, coefficient
derivative convention, outward interval primitives and whole-step majorant
semantics from
`raw_c_actual_nonzero_lambda_hybrid_validated_transfer.py`. It does not inherit
that calculation's broad \(\rho\in[-1,1]\) switch box or failed width verdict.
The actual switch boxes instead come directly from the successful
Bessel-preconditioned kernel-panel result.

For each fixed parameter, choose the nonzero amplitude scale
\(v(Q_{\rm switch})=1\) and put \(w=\partial_\lambda v\). Then

\[
Y=(v,v_Q,w,w_Q),\qquad
Y_Q=
\begin{pmatrix}
0&1&0&0\\
A&0&0&0\\
0&0&0&1\\
a&0&A&0
\end{pmatrix}Y,
\]

where

\[
A=x^2+\lambda a-\kappa^2,\qquad
a=\frac{x^{3/2}}{\sqrt{6\pi^2}},\qquad
x=6\pi^2e^Q.
\]

The switch seed is

\[
v=1,\quad v_Q=-(x+\tfrac12+\rho),\quad w=0,\quad w_Q=-s.
\]

This lambda-dependent rescaling changes neither the projective direction nor
its parameter derivative. The smooth four-state system is propagated with
order-12 interval Taylor enclosures over both 16- and 32-segment exact
partitions at 80 and 120 decimal digits. Division occurs only at \(Q_0\), and
only after the interval for \(v(Q_0)\) excludes zero:

\[
\rho(Q_0)=-\frac{v_Q}{v}-x_0-\frac12,
\qquad
s(Q_0)=\frac{v_Qw-vw_Q}{v^2}.
\]

The lambda-zero row must contain both the exact modified-Bessel endpoint
direction and the independently certified node-safe Green value of
\(s(Q_0)\). These are regression controls, not independent physical evidence.

## Execution

The runner and input manifest must be committed before execution through the
bounded control plane:

```text
./ice run raw_c_bessel_preconditioned_node_safe_switch_to_q0_sensitivity_transfer
```

No result has yet been recorded in this report.
