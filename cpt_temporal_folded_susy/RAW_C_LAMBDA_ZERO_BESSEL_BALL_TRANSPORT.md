# Lambda-zero raw-\(C\) Bessel ball transport anchor

## Narrow question and answer

For the declared real raw-\(C\) fiber at exactly \(\lambda=0\), set

\[
x=6\pi^2e^Q,\qquad \kappa=\sqrt{3/2}\,|p|.
\]

Then

\[
u_{QQ}=(36\pi^4e^{2Q}-\kappa^2)u
\]

becomes

\[
x^2u_{xx}+xu_x-(x^2-\kappa^2)u=0.
\]

The recessive direction is therefore represented exactly by

\[
u_+(Q;\kappa)=K_{i\kappa}(6\pi^2e^Q).
\]

The bounded run certified this exact transport direction on
\(Q\in[-4,+\infty)\) and certified five disjoint sign-changing brackets
for the endpoint characteristic

\[
F(\kappa)=\partial_Q u_+(-4;\kappa)
=-\frac{x_0}{2}
 \left[K_{i\kappa-1}(x_0)+K_{i\kappa+1}(x_0)\right],
\qquad x_0=6\pi^2e^{-4}.
\]

This closes only the \(\lambda=0\), real-axis endpoint-transport anchor. It
does not calculate \(F_\lambda\), a spectral measure, RAQ, quantum
constraint-rescaling equivalence, quantum gravity, or a TOE.

## Why the characteristic is real and continuous

The modified-Bessel order symmetry and conjugation identities give, for
real \(x>0\) and real \(\kappa\),

\[
\overline{K_{i\kappa}(x)}=K_{-i\kappa}(x)=K_{i\kappa}(x).
\]

Together with analytic dependence on the order, this makes \(F(\kappa)\)
real and continuous on the real axis. This is the hypothesis needed before
the intermediate value theorem may turn certified opposite endpoint signs
into an existence statement. The runner records it as a separate theorem
guard rather than treating a complex ball whose imaginary component
contains zero as a reality proof.

The special-function identities and conventions are sourced from
[DLMF §§10.25, 10.27--10.29](https://dlmf.nist.gov/10). The emitted
enclosures come from locked `python-flint==0.9.0`, whose midpoint-radius
semantics follow the [Arb paper](https://arxiv.org/abs/1611.02831). The
sources do not themselves prove this repository-specific certificate.

## Node-safe exact transport

No numerical fundamental matrix is propagated across the exponentially
stiff interval. The exact \(K\) direction supplies the full \(+\infty\) to
\(Q_0=-4\) transport at \(\lambda=0\). The independent exact solution
direction is checked through

\[
W_Q\!\left(K_{i\kappa}(x(Q)),I_{i\kappa}(x(Q))\right)=1.
\]

On every certified bracket band the Arb Wronskian ball contains one and
excludes zero. This avoids both an ill-conditioned raw fundamental matrix
and a one-chart Riccati variable that would fail at zeros of \(u\).

## Observed certificate

The clean committed definition was executed through the repository control
plane:

```text
./ice run raw_c_lambda_zero_bessel_ball_transport
```

It returned `VALID_RUN` with 4/4 exact checks, 35/35 ball checks, and five
theorem/scope guards. Each of the following disjoint intervals has width

\[
\frac{1}{20282409603651670423947251286016}
\approx4.93038\times10^{-32}
\]

and contains at least one real sign-changing zero:

| bracket | approximate location used only as a label |
|---:|---:|
| 1 | 2.02252723895536301335 |
| 2 | 3.93713906776970846766 |
| 3 | 5.40716563938147389511 |
| 4 | 6.71336772070695068054 |
| 5 | 7.92314731172988837047 |

The exact rational endpoints are retained in the result JSON. Opposite
signs prove at least one root per interval; they do not prove uniqueness,
exclude an even number of extra roots, or prove that these five exhaust
\(\kappa\in[0,8]\).

Across the five full bracket bands:

- \(|K_{i\kappa}(x_0)|\) has a certified lower bound as small as
  \(3.52033034178232\times10^{-6}\), still strictly nonzero;
- the weakest Wronskian absolute lower bound is greater than
  \(0.999999999999999999999999999995\);
- the exact Bessel versus WKB normalized log-derivative discrepancy at
  \(Q=4\) is at most \(1.1954630\times10^{-8}\).

The last discrepancy lies inside the separately proved Liouville--Green
budget. The runner reconstructs that budget with outward-rounded Arb
operations from the upstream exact rationals

\[
R_{\rm bar}=\frac{2500100000}{9999800001},\qquad
\eta_{\rm bar}=\frac1{100000},
\]

instead of importing its rounded decimal rendering. It obtains

\[
V_{\rm bar}=
\frac{125005000000000}{1322960310396898677},\qquad
\frac{2(e^{V_{\rm bar}/2}-1)}{2-e^{V_{\rm bar}/2}}
\in 9.4495547830311922\times10^{-5}\ \text{(outward ball)}.
\]

The 80- and 120-decimal computations are same-backend precision repeats,
not independent implementations. The 120-decimal bracket must nest inside
the 80-decimal bracket, and every accepted sign must exclude zero.

## Remaining first-priority gap

Differentiating the fiber equation at \(\lambda=0\) gives

\[
v''-A_0v=A_\lambda u,
\qquad
A_0=36\pi^4e^{2Q}-\kappa^2,
\qquad
A_\lambda=6\pi^2e^{3Q/2}.
\]

The existing plus-tail theorem does not enclose the differentiated boundary
datum. The next independent calculation must first derive a
parameter-differentiated Volterra/Liouville--Green tail enclosure and then
propagate \((u,u',v,v')\), or equivalent Prüfer/projective variables,
through node crossings. Until that succeeds, \(F_\lambda\), nonreal Weyl
data, the raw-\(C\) spectral measure, and RAQ remain explicit nulls.

## Provenance

- input SHA-256: `ba09a1c7d85cd77830f816526991d6f2cc62562a6dd74efa94ef8bbc104486c4`;
- runner SHA-256: `3944d549d8a31d4ab126206dfa77f2aaa669dc3fb24598040e7e6b7d662d131e`;
- result-file SHA-256: `6f4d9ecf358dcef6826907058699c83a6e60c300d531e86197097d6cb5bfde2e`;
- canonical result payload SHA-256, excluding its self field:
  `5bd3f7b3b435b693da95c7d3b2c528c63328a45964683f011eac191b1827ff92`.

