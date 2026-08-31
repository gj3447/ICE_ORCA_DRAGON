# Raw-C Qswitch-to-Q0 kappa projective-sensitivity sign transport

## Independent question

On the exact current correlated $K\times\Lambda$ strip, does the selected
actual projective derivative $h=\partial_\kappa\rho$ remain strictly negative
at $Q_0=-4$ after the already certified $Q_{\rm switch}=-29/10$ seed?

This is a new bounded endpoint question aimed at the next missing P1 link. It
does not differentiate the complete declared boundary functional and does not
reuse the correlated Gamma face signs as derivative evidence.

## Exact Wronskian transport

Normalize the selected actual direction at the switch by $U(Q_{\rm switch})=1$
and write $Y=\partial_\kappa U$ at fixed $\lambda$. The parameter-dependent
normalization gives

\[
Y(Q_{\rm switch})=0,
\qquad
Y_Q(Q_{\rm switch})=-h(Q_{\rm switch}).
\]

For

\[
A=36\pi^4e^{2Q}+6\pi^2\lambda e^{3Q/2}-\kappa^2,
\]

the actual and variational equations are

\[
U_{QQ}=AU,
\qquad
Y_{QQ}=AY-2\kappa U.
\]

Thus the cross-Wronskian $W=UY_Q-U_QY$ obeys

\[
W_Q=-2\kappa U^2,
\qquad
W(Q_{\rm switch})=-h(Q_{\rm switch})>0.
\]

Because $Q_0<Q_{\rm switch}$ and $\kappa>0$,

\[
W(Q_0)=W(Q_{\rm switch})
       +2\kappa\int_{Q_0}^{Q_{\rm switch}}U(Q)^2\,dQ
       >0.
\]

The hash-pinned sign-strip transfer gives a nonzero full-corridor endpoint
chart $0<U(Q_0)<7$. Therefore

\[
h(Q_0)=-\frac{W(Q_0)}{U(Q_0)^2}<0.
\]

Combining the independent switch floor
$-h(Q_{\rm switch})>\kappa_{\rm left}/20$ with $U(Q_0)^2<49$ gives the
explicit conservative one-sided margin

\[
h(Q_0)<-\frac{\kappa_{\rm left}}{980}<0.
\]

No pole-free claim on every intermediate projective chart is needed or made:
the linear $U,Y,W$ evolution remains regular through a possible intermediate
zero, and only the already certified nonzero endpoint $U(Q_0)$ is divided by.

## Explicit boundary

Even a successful result is only a selected projective derivative sign at
$Q_0$. It supplies no two-sided numerical $h(Q_0)$ enclosure, reference-state
kappa variation, complete differentiated minus tail, $\partial_\kappa G$,
mixed derivative, transversality, uniqueness, selector, continuation,
velocity, global roots, absolute $\Gamma_1$ amplitude/sign, nonreal Weyl or
spectral data, RAQ, BFV, physical product, likelihood or physics.

## Controlled execution

The frozen input SHA-256 is
`aec9d889b1a2a557bd0a3f8bd17d5224b1e29dae244403ff64b5a29d2addcab7` and
the pre-run runner SHA-256 is
`469a713097ccf64d1184e020d970ff1fab8977711045528b3a17316eab762d68`.
Before the clean source commit, `jq empty`, `uv run python -m py_compile`,
`git diff --check`, and `./ice status` passed. The source commit, first
controlled `./ice run`, actual result hash and post-run validations remain to
be recorded; this paragraph is not evidence that the calculation has run.
