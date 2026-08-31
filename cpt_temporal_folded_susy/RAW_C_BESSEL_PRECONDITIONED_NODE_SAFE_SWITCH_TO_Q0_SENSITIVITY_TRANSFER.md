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
Bessel-preconditioned kernel-panel result. The compact propagation itself is
the raw four-state Taylor system below; “Bessel-preconditioned” describes its
hash-pinned switch seed and lambda-zero regressions, not a Bessel basis used
at every compact step.

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

The committed runner was executed through the bounded control plane:

```text
./ice run raw_c_bessel_preconditioned_node_safe_switch_to_q0_sensitivity_transfer
```

It returned `VALID_RUN` with verdict
`CERTIFY_FINITE_BESSEL_PRECONDITIONED_NODE_SAFE_SWITCH_TO_Q0_PROJECTIVE_SENSITIVITY_TRANSFER`.
All 6/6 exact checks and 331/331 outward controls passed; three theorem-scope
guards were recorded. Same-backend precision overlap and the 16/32-segment
refinement overlap are enclosure-stability controls, not independent evidence.

## Certified finite endpoint intersections

The intersections below are over the 80/120-digit and 16/32-segment ladder.
`v(Q0)` excludes zero in every row, so the displayed projective quotient is
defined. The two nonzero-lambda sensitivity rows also exclude zero.

| box | \(v(Q_0)\) | \(\rho(Q_0)\) | \(s(Q_0)\) | widths / zero status |
| --- | --- | --- | --- | --- |
| negative \(\lambda\) | [5.30770644786230253666, 5.30780616310380640933] | [-1.58463563193614172397, -1.58459605260835141726] | [0.12844506812689360231, 0.15662300844269338995] | widths \(9.9715\times10^{-5}\), \(3.9579\times10^{-5}\), \(2.8178\times10^{-2}\); \(v,s\ne0\) |
| positive \(\lambda\) | [5.30777863751128690401, 5.30787835306383796469] | [-1.58462126943330312989, -1.58458169054411664311] | [0.12844368604419287294, 0.15662118561158422381] | widths \(9.9716\times10^{-5}\), \(3.9579\times10^{-5}\), \(2.8177\times10^{-2}\); \(v,s\ne0\) |
| \(\lambda=0\) regression | [5.30779239980468047061, 5.30779240082670433545] | [-1.58460866124756947064, -1.58460866097260088888] | [0.12845312173885758966, 0.15661282280052546412] | widths \(1.0220\times10^{-9}\), \(2.7497\times10^{-10}\), \(2.8160\times10^{-2}\); \(v,s\ne0\) |

This closes only the finite projective transport claim: the local projective
\(s(Q_0)=\partial_\lambda\rho(Q_0)\) interval is positive on each specified
punctured real lambda box. It is not an absolute-normalization statement,
and it does **not** certify a \(Q_0\) mean-value comparison
\(\rho_\lambda-\rho_0\), a negative/positive side separation relative to
\(\rho_0(Q_0)\), or any continuation across \(\lambda=0\).

## Resource accounting and provenance

- 12 Arb Bessel evaluations; 288 compact Taylor steps across 12
  precision/segment/parameter rows; order 12; two precision tiers.
- Zero ODE, root, quadrature, finite-difference and sampling calls.
- Result SHA-256: `dd84bf217b119b910f7928a946f0133b0be5f6fd8e6061c7f2d9f844102c6d2a`.
  Payload self-hash: `0c7d40498a7f023a4c542d7da32f04febef9b004cd68473591dcb6e402e3c14d`.
- Runner SHA-256: `d3da303cb973efed027a425d12973b81d0c3c0113cf3111b8588eab28dfcdfb1`.
  Input SHA-256: `b1668b5eb06eda2552ed519022932a70dbb3e54faadbe9bac9a5c4086d4d3762`.

## Explicit nonclaims and next gap

This result does **not** evaluate the actual declared \(\Gamma_1\), its
complete minus-tail remainder, or any \(\Gamma_1\) sign/zero. It therefore
does not support root continuation or velocity, a nonreal Weyl function,
spectral measure, RAQ completion, or a physical/empirical claim. The next
separate mathematical question is a differentiated rotating-frame
minus-tail functional for the declared \(\Gamma_1\), using this endpoint
state as input; it must not be treated as automatically authorized by this
finite transport result.
