# Raw-C reference kappa-variation weighted envelope

## Independent question

On the exact current real $K$ corridor, can the declared
reference $c_\kappa$ be differentiated with respect to $\kappa$ and its
variation be bounded on the entire minus half-line in the weight needed by a
later differentiated-tail calculation?

The pinned $\Lambda$ slab is only a provenance/context label here:
$c_\kappa$, $D$, and the envelope are lambda-independent.

This question is deliberately reference-only. It neither differentiates the
selected actual plus solution nor forms $\partial_\kappa G$.

## Equation and fixed reference data

With $x=6\pi^2e^Q$, $V=x^2$ and $Q_0=-4$, the pinned reference solves

\[
c_{\kappa,QQ}=(V-\kappa^2)c_\kappa,
\qquad c_\kappa(Q_0)=1,
\qquad c_{\kappa,Q}(Q_0)=0.
\]

The initial data do not depend on $\kappa$. Hence
$D=\partial_\kappa c_\kappa$ obeys

\[
D_{QQ}=(V-\kappa^2)D-2\kappa c_\kappa,
\qquad D(Q_0)=D_Q(Q_0)=0.
\]

The modified-Bessel equation underlying the inherited coefficient convention
is NIST DLMF 10.25.1. The new calculation below is an exact rotating-frame
comparison over the repository-pinned finite-IVP reference, not a fresh
Bessel evaluation.

## Full-minus-half-line comparison

For

\[
y=(c_\kappa,c_{\kappa,Q}/\kappa),
\qquad d=(D,D_Q/\kappa),
\]

the free first-order part is a Euclidean skew rotation. Its perturbation norm
is at most $V/\kappa$. On the declared positive corridor,

\[
q_{\rm left}
=\int_{-\infty}^{Q_0}\frac{V(Q)}{\kappa_{\rm left}}\,dQ
=\frac{18\pi^4e^{-8}}{\kappa_{\rm left}},
\qquad B_c=e^{q_{\rm left}},
\]

so $\|y(Q)\|\le B_c$. Backward variation of constants for $d$, whose forcing
has norm $2|c_\kappa|$, then gives

\[
\|d(Q)\|\le 2B_c^2(Q_0-Q).
\]

With $a(Q)=6\pi^2e^{3Q/2}$ and
$\int_0^\infty t^2e^{-3t/2}dt=16/27$, this implies

\[
\|D\|_{L^2(a;(-\infty,Q_0])}
\le \frac{8\sqrt2\pi}{3}e^{-3}B_c^2.
\]

The bound is finite even though the comparison permits linear pointwise
growth toward $Q=-\infty$. It is a magnitude envelope, not a pointwise
interval or a tail value.

## Explicit boundary

Even a successful run supplies only the reference-state weighted envelope.
It supplies no two-sided $h(Q_0)$ enclosure, actual-plus $\kappa$ variation,
complete differentiated minus tail, $\partial_\kappa G$, mixed derivative,
transversality, uniqueness, selector, velocity, global roots, absolute
$\Gamma_1$ amplitude/sign, nonreal Weyl or spectral data, RAQ, BFV,
likelihood or physics.

## Controlled execution

The pre-run source freeze is:

- input SHA-256:
  `6267420934202ce75e61230d7875cfcae74e460e52562a12d359fc7565fc4bd3`;
- runner SHA-256:
  `3a8696d3c0034ed0d57a7e601d1c5ef899129563c94389be640e0d3a824f7efa`;
- `jq empty` passed for the input, `uv run python -m py_compile` passed for
  the runner, and `./ice list --json` discovered the unnumbered runner;
- independent read-only mathematics, code/provenance and scope audits passed.
  Their hardening requests (three explicit norm checks, real rather than
  positive symbolic state values, one counted DLMF source, and lambda as a
  context-only label) are incorporated in this freeze.

No calculation was executed before the source-only commit. The clean source
commit, first `./ice run`, actual outward envelope and post-run validations
will be added only after that controlled run.
