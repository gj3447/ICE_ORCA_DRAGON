# Classical two-clock comparison on the closed-FRW \(V=0\) component

## Observed result

After the scoped harness repair, the committed bounded run returned

```text
KEEP_V0_CLASSICAL_SCALAR_AND_TRACE_MOMENTUM_CLOCKS_AGREE_ON_OVERLAP_Q_CLOCK_TURNS
```

All 17 exact checks passed, with 5 separately recorded theorem/scope guards.
Thus \(\phi\) and \(P\) give mutually inverse classical clock charts on their
overlap, while \(Q\) has an FP zero at \(P=0\) and must be split into two
branches.  No quantum clock equivalence follows.

## Scope

This bounded, unnumbered calculation compares two classical clocks on the
already derived component

\[
p>0,\qquad R=3p^2-2P^2>0,\qquad C=0.
\]

The clocks are the massless scalar \(\phi\) and the geometric trace momentum
\(P=ap_a/2\).  The log-scale variable \(Q=2\log a\) is retained as a failure
control.  The calculation constructs classical complete observables only.  It
does not define a quantum clock change, raw-\(C\) physical inner product,
Born--Oppenheimer correction, decoherence functional or likelihood.

## Dirac coordinate and clock factors

On shell,

\[
e^{2Q}=\frac{R}{72\pi^4},\qquad
\Phi=\phi-\sqrt{\frac32}\,
\operatorname{atanh}\!\left(\sqrt{\frac23}\frac{P}{p}\right).
\]

The invariant is weak rather than strong off shell:

\[
\{\Phi,C\}=\frac{3p}{2R}C\approx0,\qquad \{p,C\}=0.
\]

The two selected clock factors are positive on the declared orbit,

\[
\{\phi,C\}=\frac{e^{-3Q/2}p}{2\pi^2}>0,
\]

\[
\{P,C\}=-C_Q\approx12\pi^2e^{Q/2}>0.
\]

In contrast,

\[
\{Q,C\}=-\frac{e^{-3Q/2}P}{3\pi^2}
\]

vanishes at \(P=0\).  Thus \(Q\) requires separate expanding and contracting
clock charts.

## Complete observables

At scalar-clock reading \(\tau\),

\[
P_\phi(\tau)=\sqrt{\frac32}\,p\,
\tanh\!\left[\sqrt{\frac23}(\tau-\Phi)\right],
\]

\[
Q_\phi(\tau)=\frac12\log
\frac{3p^2-2P_\phi(\tau)^2}{72\pi^4}.
\]

At trace-momentum reading \(\sigma\), with
\(|\sigma|<\sqrt{3/2}\,p\),

\[
\phi_P(\sigma)=\Phi+\sqrt{\frac32}\,
\operatorname{atanh}\!\left(\sqrt{\frac23}\frac{\sigma}{p}\right),
\]

\[
Q_P(\sigma)=\frac12\log
\frac{3p^2-2\sigma^2}{72\pi^4}.
\]

The executable checks current-reading recovery, the inverse relation
\(P_\phi(\phi_P(\sigma))=\sigma\), equality of the two \(Q\) descriptions,
monotonicity, and weak gauge invariance for functions of \((\Phi,p)\).

## Boundary

Classical agreement on the overlap does not imply unitary equivalence after
quantization.  That later question requires the raw-\(C\) spectral/RAQ
construction, physical inner product, self-adjoint clock observables and a
controlled quantum reduction map.  A \(V\ne0\) bounce is also separate: the
scalar and geometric clock factors must be checked anew and may vanish at its
time-symmetric point.

## Execution

```text
./ice run v0_two_clock_relational_observable_comparison
VALID_RUN; 17/17 exact checks; 5 theorem guards
```

The successful result artifact has outer SHA-256
`f343f789f59299d1defac0a8d6ea8450236b2273459d00ee24453f679b68d58e`.

## First execution observation

The first committed-source run produced a valid artifact but selected the KILL
row with 16/17 exact checks.  The sole failed check was the monotonicity
identity

\[
\frac{dP_\phi}{d\tau}=p\operatorname{sech}^2
\left[\sqrt{\frac23}(\tau-\Phi)\right].
\]

The runner asked generic `simplify` to reduce
\(1-\tanh^2u-\operatorname{sech}^2u\); it did not apply the hyperbolic
identity.  All formula, inverse-map, clock-factor and domain checks passed.
This is recorded as a harness false negative, not contrary clock evidence.
The failed raw artifact is preserved in Git history before any repair.
