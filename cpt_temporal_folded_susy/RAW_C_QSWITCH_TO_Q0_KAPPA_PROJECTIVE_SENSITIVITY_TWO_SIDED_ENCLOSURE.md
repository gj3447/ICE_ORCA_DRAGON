# Raw-C Qswitch-to-Q0 kappa projective-sensitivity two-sided enclosure

## Independent question

Can the already certified two-sided selected projective sensitivity at
$Q_{\rm switch}=-29/10$ be turned into a finite two-sided enclosure at
$Q_0=-4$, without transporting the actual variation $Y=\partial_\kappa U$
or differentiating the declared $\Gamma_1$ tail?

This is distinct from the earlier one-sided Wronskian sign result. The goal is
only a finite scale-invariant endpoint seed for a later, separately authorized
normalized-tail calculation.

## Minimal Wronskian-integral state

At fixed lambda, switch-normalize the selected actual direction by
$U(Q_{\rm switch})=1$. With $Y=\partial_\kappa U$ and

\[
W=U Y_Q-U_QY,
\qquad W_Q=-2\kappa U^2,
\]

the normalization gives $Y(Q_{\rm switch})=0$ and
$W(Q_{\rm switch})=-h(Q_{\rm switch})=p_{\rm switch}$.
Introduce only

\[
J_Q=-U^2,
\qquad J(Q_{\rm switch})=0.
\]

Because $Q_0<Q_{\rm switch}$,

\[
J(Q_0)=\int_{Q_0}^{Q_{\rm switch}}U(Q)^2\,dQ\ge0,
\qquad
W(Q_0)=p_{\rm switch}+2\kappa J(Q_0),
\]

and the desired projective derivative is

\[
h(Q_0)=-\frac{W(Q_0)}{U(Q_0)^2}.
\]

Thus the calculation propagates only $(U,U_Q,J)$. It reuses the pinned
coefficient derivatives and whole-step majorants, with an exact Taylor jet
and D13 remainder for $J$ obtained from derivatives of $-U^2$.

## Planned controls

- exact 16/32 partitions from $Q_{\rm switch}$ to $Q_0$;
- 80/120-decimal outward transfer rows;
- segment-refinement and cross-precision overlap for $U,U_Q,J$;
- intersection with the independently pinned nonzero $U(Q_0)$ chart;
- a finite two-sided $h(Q_0)$ interval whose upper endpoint is consistent
  with the earlier strict one-sided margin.

No numerical width target is imported from an unrelated calculation.

## Explicit boundary

Even success would not supply pointwise $Y$, a pole-free chart on the open
leg, an actual or reference differentiated tail, $\partial_\kappa G$,
$\partial_\kappa\Gamma_1$, a mixed derivative, transversality, root
monotonicity or uniqueness, selector, velocity, global roots, absolute
$\Gamma_1$ orientation, nonreal Weyl data, spectral measure, RAQ, BFV,
likelihood or physics.

## Controlled execution

The pre-run source freeze is:

- input SHA-256:
  `18718b766da4cc7d4dc57163bb2d92236a882f5aa99b3eeaaa4a95934e8a27cb`;
- runner SHA-256:
  `1b3437200caa1d57e8605f817325de960063e3ec2df2af1c209719bb4d240ca8`;
- `jq empty` passed for the input, `uv run python -m py_compile` passed for
  the runner, and `./ice list --json` discovered the unnumbered runner;
- independent mathematics, code/provenance and scope audits found no formula,
  remainder-order or claim-boundary blocker. Their hardening requests replaced
  a tautological W check by the conserved identity $W_Q-2\kappa J_Q=0$,
  tightened the prior-margin comparison, and added exact Q0-sign scope checks.

No calculation is run before a clean source-only commit. The source commit,
first `./ice run`, actual outward intervals and all failed or passed
validations will be added after controlled execution.
