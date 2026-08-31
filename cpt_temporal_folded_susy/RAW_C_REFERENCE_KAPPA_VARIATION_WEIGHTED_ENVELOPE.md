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

No calculation was executed before source-only commit
`617ba23041654b487925bc6fbd4000c2e1ddb82f`.

The first result-producing command was

```text
./ice run raw_c_reference_kappa_variation_weighted_envelope
```

It exited zero in 1.96 seconds and reported `VALID_RUN`, verdict
`CERTIFY_UNIFORM_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_ONLY`, exact or
structural checks 16/16, outward controls 3/3 and three theorem guards.

## Result

The intersection of the 80- and 120-digit outward evaluations gives

| quantity | enclosed value shown to 45 digits |
| --- | ---: |
| $q_{\rm left}$ | 0.290962180742840827552040829801635884038757170 |
| $B_c$ | 1.33771399164390410687468914054144215751538829 |
| $\|c_\kappa\|_{L^2(a)}$ envelope | 0.418465532171176100466048575415978980246723075 |
| $\|D\|_{L^2(a)}$ envelope | 1.05554486215269862345786236329806936644506481 |

The last row therefore safely implies the rounded uniform statement
$\|D\|_{L^2(a)}\le 1.055544862153$. The underlying final intersection width
is below $3.88\times10^{-120}$; equal printed endpoints above reflect the
45-digit display, not a claim of exact rational equality.

The raw result is 17,875 bytes with SHA-256
`b6f5b60018142d53537955393e4e660528d905583f10161fa014bb5fe52a8c33`.
Deleting its self-digest field and canonicalizing with sorted compact JSON
independently reproduces payload SHA-256
`bb50111f524a965aa1f7595aa42f9db93c5b01787da29563ffff05f5ef1fa6e6`.
An independent `jq` assertion also confirmed all 16 exact/structural checks,
all three controls, all three guards and every required fail-closed output.

The first ontology validation correctly failed because the compact snapshot
omitted `payload.numerical_checks` while declaring three numerical controls at
top level. Adding that matching count changed no calculation or raw result.
The next validation passed: 1,530 nodes, 3,917 edges and 430/430 stored hashes
collection-wide; the CPT graph has 1,388 nodes, 3,630 edges and 385/385 hashes.
The 70 unresolved external-bridge warnings predate this result and remain
warnings, not hidden errors.

## Workbench interpretation

This calculation removes only the fixed-reference weighted-envelope subproblem
from the current P1 gap. It does not produce a new physical effect. The next
scientific obstruction is a finite two-sided actual-plus kappa-variation seed
and the complete combined kappa-differentiated minus tail. Until those exist,
`partial_kappa g`, transversality, uniqueness, a correlated-root selector and
root velocity remain prohibited interpretations.
