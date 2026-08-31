# Fixed-metric zonal scalar-matter \(DH\) falsifier

## Question and boundary

On the fixed unit-\(S^3\) background \(q_{ab}=a^2\gamma_{ab}\), this bounded
calculation asks whether the **matter-only** canonical bracket

\[
\{D_\phi[v],H_\phi[N]\}
\]

equals \(H_\phi[\mathcal L_vN]\).  The tested packet is

\[
v^a=a^{-2}D^aQ_1,\qquad N=Q_2,\qquad
\theta=Q_1+Q_2,\qquad \xi=Q_1+Q_2,
\]

at field cutoffs \(L=2,3\).  Mixing even and odd modes avoids the
parity-protected zero-equals-zero result of the earlier candidate
\(\theta=Q_2,\xi=Q_1\).

For a fixed metric and a non-Killing shift, direct canonical differentiation
predicts the decomposition

\[
\{D_\phi[v],H_\phi[N]\}
=H_\phi[\mathcal L_vN]+R_{q\,\mathrm{fixed}},
\]

\[
R_{q\,\mathrm{fixed}}
=\frac12\int\!\sqrt\gamma\,N\left[
-a^{-3}\xi^2D_av^a+a|D\theta|^2D_av^a
-2aD_{(a}v_{b)}D^a\theta D^b\theta
\right].
\]

The runner independently compares the modal coefficient calculation with
direct \(\chi\)-integration of both \(H_\phi[\mathcal L_vN]\) and this strain
term.  It separately compares ambient-before-project and \(L\)-only brackets,
so a cutoff remainder cannot be relabelled as the fixed-metric residual.
The kinetic and gradient pieces of the strain residual are also retained
separately, so an isolated cancellation at one background scale cannot be
mistaken for a functional identity.

The harmonic/product/Hamiltonian helpers are reused from the hash-pinned
fixed-background \(HH\) runner.  The continuum reference convention comes
from ADM and the canonical DH relation summarized by Thiemann; the
three-sphere harmonic paper is a convention check, not a generator of this
answer.

## Non-claims

This is not the gravity-plus-matter ADM \(DH\) bracket, the full HDA or its
Jacobi identity, an anomaly calculation, BFV/BRST nilpotency, or a physical
prediction.  In the full canonical system the gravitational diffeomorphism
generator also transforms the metric; this runner only measures the term
lost when that action is absent.

## Controlled command

```text
./ice run closed_s3_zonal_v0_scalar_matter_dh_fixed_metric_falsifier
```

Observed coefficients and hashes are added only after the clean committed
runner is executed.
