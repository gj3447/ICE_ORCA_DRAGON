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

## Observed result

The controlled run returned `VALID_RUN` with verdict
`CERTIFY_UNIFORM_NEGATIVE_Q0_KAPPA_PROJECTIVE_SENSITIVITY_ONLY`. All 9/9
exact or structural checks and all three theorem-scope guards passed. The
certified statement is exactly

\[
h(Q_0)<-\frac{\kappa_{\rm left}}{980}
=-\frac{5125180435678962497905662710537123}
        {2484595176447329626933538282536960000}<0.
\]

The endpoint chart reused by the proof is

\[
4.58064385278783566005740167935448502126555530
<U(Q_0)<
6.14669473244510418422732355435448502126555530.
\]

This closes the selected actual projective-sign leg to $Q_0$ only. It is a
workbench calculation, not a model-level or empirical physics discovery.

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
the executed runner SHA-256 is
`c821e103dbd65769ea478ea232230bc7ff42db35b96c68d9ff9375daf14e6272`.
The clean source was introduced in commit
`6d2a659475f5fbb787833e47d14c16e0e23f676b`. The first controlled
`./ice run` stopped before writing a result because `python-flint` rejected a
decimal string passed directly to `fmpq`; this parser defect carried no
scientific result. Commit `e2c31f53124fc558aa530a108c2682dbc6b1f0b4`
replaced it with the repository's exact `Fraction`-to-`fmpq` pattern. The
second controlled run produced the 10,810-byte result with SHA-256
`cf80dae45e381ecc92e0a5cff62c0255aba779637e511ab3942764d4ef0faaa3`
and payload digest
`7c89c3cdfd404b85374d1fc88896ea478678ad3c4088b931ef2172a40b117b9f`.
Post-run `./ice ontology validate` passed with 1,525 nodes, 3,908
edges, 429/429 verified hashes and zero errors; its 70 unresolved external
bridge warnings were pre-existing. `npm run check` passed strict typechecking
and all 69/69 tests.
