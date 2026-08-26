# Gate 1 — closed-FRW \(V=0\) trace endpoint action

## Outcome

The bounded calculation found an exact classical **local on-shell relational
endpoint action** for the static trace slice on the frozen closed-FRW
\(V=0\), \(p_\phi=+1\) component:

\[
\boxed{
R=3p_\phi^2-2P^2>0,
\qquad
D=\{P,C\}>0
}
\]

and selected the predeclared verdict

```text
KEEP_V0_LOCAL_ON_SHELL_RELATIONAL_ENDPOINT_ACTION
```

The time-dependent trace condition \(P=f(s)\) is retained as an exact
classical same-constraint-orbit control, not as a second independently
promoted construction.  The result closes the local triangle formed by

1. the relational endpoint coordinate and boundary action;
2. the finite endpoint flow from \(P=f\) to the static slice \(P=0\); and
3. the local Faddeev–Popov reduction.

This narrows the replacement endpoint route beyond the preceding result,
which only killed appending a trace delta to the unchanged proper-time source.
It does **not** construct a full off-shell BFV action, normalized endpoint
states, the old fixed-\(a\) kernel equivalence, the full-real-lapse
distributional \(\delta(\hat C)\) physical-inner-product kernel,
a global fundamental region, a physical cycle, physics, or a TOE.

The successful execution passed 16 exact checks, seven separately scoped
theorem guards, and five numerical checks using six quadratures.  It made zero
root calls, zero ODE calls, and started zero descendants.  Gate 1 therefore
remains `OPEN_PARTIAL_PROGRESS`, `global_promotion=PROHIBITED`, and
`automatic_next=null`.

## 1. Source boundary

Henneaux–Teitelboim–Vergara supply the framework used here: endpoint data must
be accompanied by the boundary term appropriate to their canonical chart;
canonical gauges require endpoint transversality; endpoint states on a gauge
orbit must be related; and the canonical limit contains the constraint delta,
gauge delta, and FP determinant.  They do not supply this model-specific
on-shell action, a quantum endpoint-state completion, or global admissibility.

Banihashemi–Jacobson motivate imposing a genuine constraint-plus-trace-gauge
FP reduction before the lower-lateral momentum-first convergence argument.
They do not construct the endpoint action used below.  Their degenerate
spatially flat homogeneous \(V=0\) example does not apply directly: the
present control retains the closed-FRW curvature term \(-6\pi^2a\).

Marolf's full-real-lapse distributional \(\delta(\hat C)\)
physical-inner-product or group-averaging kernel remains the comparison
target.  On continuous zero spectrum this is not asserted to be an idempotent
projection operator.  No such kernel or lapse-contour equivalence is
calculated here.

Primary sources:

- M. Henneaux, C. Teitelboim, and J. D. Vergara,
  [*Gauge invariance for generally covariant systems*](https://doi.org/10.1016/0550-3213(92)90166-9),
  Nucl. Phys. B 387 (1992) 391, arXiv:hep-th/9205092.
- M. Banihashemi and T. Jacobson,
  [*On the lapse contour*](https://doi.org/10.1103/PhysRevD.111.066014),
  Phys. Rev. D 111 (2025) 066014, arXiv:2405.10307.
- D. Marolf,
  [*Path integrals and instantons in quantum gravity: Minisuperspace models*](https://doi.org/10.1103/PhysRevD.53.6979),
  Phys. Rev. D 53 (1996) 6979, arXiv:gr-qc/9602019.

## 2. Exact closed-FRW control

Use the canonical trace variables

\[
Q=2\log a,
\qquad
P=\frac{ap_a}{2},
\qquad
\{Q,P\}=1,
\qquad
P\,dQ=p_a\,da.
\]

For \(V(\phi)=0\), while retaining positive spatial curvature, the constraint
is

\[
C=
-\frac{P^2}{6\pi^2a^3}
+\frac{p_\phi^2}{4\pi^2a^3}
-6\pi^2a.
\]

Writing

\[
R=3p_\phi^2-2P^2,
\]

the runner proves

\[
12\pi^2a^3C=R-72\pi^4a^4.
\]

The constraint root is therefore

\[
Q_*(P,p_\phi)
=\frac12\log\!\left(\frac{R}{72\pi^4}\right),
\]

and the trace FP bracket obeys the off-shell identity

\[
D:=\{P,C\}=-C_Q
=\frac32C+12\pi^2a.
\]

Hence, on shell,

\[
\boxed{D=12\pi^2a>0.}
\]

The frozen benchmark is

\[
p_\phi=1,
\qquad
P_1=\frac14,
\qquad
P_2=\frac12.
\]

Throughout \(0\le P\le1/2\),

\[
R\ge\frac52,
\]

so neither the logarithmic chart nor the FP determinant reaches its local
horizon.  Since \(dP/d\mu=D>0\), each endpoint has one monotone local hit of
the static slice \(P=0\).  This is a componentwise statement, not a global
copy census.

## 3. Relational endpoint coordinate

Define

\[
\Phi_*
=\phi-\sqrt{\frac32}\,
\operatorname{artanh}\!\left(
\sqrt{\frac23}\frac{P}{p_\phi}
\right).
\]

Exact differentiation gives

\[
\frac{\partial\Phi_*}{\partial P}
=-\frac{3p_\phi}{R},
\qquad
\frac{\partial\Phi_*}{\partial p_\phi}
=\frac{3P}{R},
\]

and the runner verifies

\[
\{\Phi_*,C\}\big|_{C=0}=0.
\]

More importantly, the shell symplectic potential decomposes exactly as

\[
\boxed{
P\,dQ_*+p_\phi\,d\phi
=p_\phi\,d\Phi_*+dP.
}
\]

Thus the local on-shell endpoint potential for fixed relational data is

\[
B_{\rm red}=P,
\qquad
S_{\rm imp}=S_0-[P]_{1}^{2}.
\]

This is the precise meaning of `LOCAL_ENDPOINT_COMPLETION` in the verdict.  It
does not claim that a full off-shell canonical chart and quantum endpoint
wave-function transform have already been built.

The old fixed-\(Q\) chart fails static endpoint transversality because

\[
C_P\big|_{P=0}=0.
\]

The swapped trace chart instead tests \(-C_Q=D\), which is nonzero on the
declared component.  Therefore the new endpoint problem cannot be identified
with the old fixed-\(a\) endpoint problem without a state/action transform.

## 4. Finite endpoint flow

For a finite constraint flow taking an endpoint \(P_i\) to the static slice,
the HTV boundary integrand reduces on shell to

\[
\frac{P C_P+p_\phi C_{p_\phi}-C}{D}=1.
\]

Consequently,

\[
\boxed{
F_i=\int_{P_i}^{0}dP'=-P_i.
}
\]

At the benchmark,

\[
F_1=-\frac14,
\qquad
F_2=-\frac12,
\qquad
F_1-F_2=\frac14.
\]

This explicit finite generator is the part that the earlier trace-gauge
admissibility result left open.

## 5. Local FP measure

Let \(\chi=P-f\).  In the ordered variables

\[
(\chi,C,\Phi_*,p_\phi)
\]

relative to

\[
(Q,P,\phi,p_\phi),
\]

the exact Jacobian is \(D\).  On this connected \(D>0\) component,

\[
\boxed{
dQ\,dP\,d\phi\,dp_\phi\,
\delta(C)\delta(P-f)D
=d\Phi_*\,dp_\phi.
}
\]

The signed ghost determinant and absolute delta-function Jacobian happen to
agree here because \(D>0\).  The result does not turn that local coincidence
into a global determinant-line orientation.

## 6. Time-dependent same-constraint-orbit control

Freeze

\[
f(s)=\frac14+\frac{s}{4},
\qquad 0\le s\le1.
\]

Gauge preservation gives

\[
\dot P=N D=\dot f,
\qquad
\boxed{N=\frac{\dot f}{D}>0.}
\]

For the distinct mixed fixed-\((P,\phi)\) endpoint polarization,

\[
S_{[P,\phi]}=S_0-[PQ]_{1}^{2}
=\int\left(-Q\dot P+p_\phi\dot\phi-NC\right)ds.
\]

After solving \(P=f(s)\) and \(C=0\),

\[
S_{\rm red}
=\int\left(p_\phi\dot\phi-\dot f\,Q_*\right)ds,
\qquad
\boxed{H_{\rm red}=+\dot f\,Q_*.}
\]

This is an auxiliary variational problem, separate from the relational
fixed-\(\Phi_*\) action selected by the verdict.  In particular, its pure
orbit value is generally

\[
S_{[P,\phi]}^{\rm orbit}
=P_2-P_1-(P_2Q_2-P_1Q_1),
\]

not zero.  The plus sign in \(H_{\rm red}\) is fixed by the boundary
transform.  Exact implicit differentiation,

\[
Q_{*,y}=\frac{C_y}{D},
\qquad y\in\{P,p_\phi\},
\]

reconstructs the full constrained \(Q\)- and \(\phi\)-velocities.  This is a
replacement endpoint problem, not an extra gauge delta appended to the old
constant-lapse source.

Define the orbit parameters

\[
T=\int_{P_1}^{P_2}\frac{dP}{D(P)},
\qquad
\mu_i=\int_{P_i}^{0}\frac{dP}{D(P)}.
\]

Oriented path concatenation gives the exact identity

\[
\boxed{T+\mu_2-\mu_1=0.}
\]

The raw canonical pure-gauge orbit action follows from the shell one-form:

\[
S_{0,\rm raw}^{\rm td}=P_2-P_1=\frac14.
\]

Since \(F_i=-P_i\), the directed finite-flow boundary quantity is

\[
[F]_{1}^{2}=F_2-F_1=-\frac14.
\]

It first gives the raw action of the endpoint-flowed static representative:

\[
S_{0,\rm raw}^{\rm static}
=S_{0,\rm raw}^{\rm td}+[F]_{1}^{2}
=0.
\]

With the HTV improved-static convention, the finite boundary term is then
subtracted from that raw static action:

\[
S_{\rm HTV}^{\rm static}
=S_{0,\rm raw}^{\rm static}-[F]_{1}^{2}
=\frac14.
\]

The fixed-\(\Phi_*\) relational variational problem is a third ledger:

\[
S_{\rm rel}
=S_{0,\rm raw}^{\rm td}-[P]_{1}^{2}
=0.
\]

The numerical equality
\(S_{0,\rm raw}^{\rm static}=S_{\rm rel}=0\) on this pure-gauge benchmark
does not identify the two variational problems or their endpoint states.

## 7. Independent numerical control

At 90 decimal digits, mpmath tanh–sinh quadrature returned

```text
T   =  0.015061791827002973963714448295444799927360029737717
mu1 = -0.014729604078831877086499170141806851540232259723326
mu2 = -0.029791395905834851050213618437251651467592289461043
```

A separate mpmath 48-node Gauss–Legendre rule agreed with each value to better
than the frozen relative tolerance \(10^{-60}\).  Its
oriented closure residual was

\[
4.301\times10^{-89},
\]

while the tanh–sinh values closed to the working-precision zero.  These
quadratures check a smooth one-dimensional finite-flow integral; they do not
replace the exact algebraic endpoint checks.

## 8. Execution and provenance

The frozen command was

```bash
./ice run cpt_temporal_folded_susy/gate1_v0_trace_endpoint_completion
```

The first invocation stopped before emitting a result at the implicit-root
derivative check.  The cause was a harness error: the shell substitution had
been applied only to the right-hand expression instead of to the complete
symbolic residual.  Commit `e1485de` applies the shell to each whole residual
and then simplifies it.  No scientific threshold or benchmark changed.

The next invocation exited 0, but an independent audit then found a genuine
Ragnarok risk in the harness: scientific NONPASS checks raised before a
result could be written, and only the KEEP decision row was reachable.  The
same audit also required separation of the relational \(S_0-[P]\) problem
from the auxiliary mixed \(S_0-[PQ]\) problem.

Commit `b3d7946` changed scientific NONPASS into a valid terminal result and
made the frozen KEEP, REDIRECT, KILL, and INCONCLUSIVE rows all reachable.  A
read-only in-memory branch audit exercised all four rows.  Hash, schema, and
internal partition mutations still fail before result emission; arbitrary
arguments are rejected.  Open dependencies explicitly carry no execution
authority.

One later command was rejected by the control plane before Python execution
because this report draft was untracked inside the calculation directory.  It
changed no result.  After preserving the draft outside the core directory, a
post-Ragnarok frozen invocation exited 0.

A final primary-source audit then separated the raw endpoint-flow action, the
HTV improved-static action, and the relational action exactly as above, and
replaced overly strong projector terminology for Marolf's continuous-spectrum
\(\delta(\hat C)\) kernel.  Commit `541edc8` froze that distinction before
the final result was regenerated.  The last frozen invocation exited 0 after
about 3.05 seconds and wrote one 21,615 byte result; the local relational
verdict did not change.  Independent post-run checks verified all stored
exact, numerical, and theorem-guard statuses, the zero scientific-NONPASS
count, the input and runner hashes, and the canonical payload self-hash.

```text
input SHA-256   f8ea44a52139e74eda81e0fbaf7d7c60cd1d46342c3cc824b608c35b997871d6
runner SHA-256  36cb11409760f39eb34678736903c705127188fc60a1a76e4de5059e20d5ba2a
result SHA-256  7e16ff45f14078dea9fa0726e2489d22299aa35e573fa89047143794712be28a
payload hash    5a030c04d56d91e137bf34a623f8382df248b4974541d59571152f43988cff68
```

## 9. What changed, and what remains open

Computed fact:

- on the frozen closed-FRW \(V=0\), \(p_\phi=+1\), \(R>0\), \(D>0\)
  component, the
  relational endpoint coordinate, boundary potential, finite static hit,
  finite endpoint generator, local FP reduction, reduced/full flow, and
  orbit/action triangles all agree exactly.

Interpretation:

- the prior local trace-gauge ingredient now has a classical local on-shell
  relational endpoint action in this control sector;
- the time-dependent trace path is best understood as a gauge-related control
  for that action, not an independently accumulated route.

Still-open hypotheses and constructions:

- a full off-shell canonical chart and HTV-compatible ghost, antighost, and
  multiplier endpoint conditions;
- a normalized endpoint-state transform and full replacement BFV measure;
- a bounded replacement-source discretization distinct from the old
  constant-lapse fixed-\(a\) source;
- comparison with the full-real-lapse distributional \(\delta(\hat C)\)
  physical-inner-product kernel and regulator removal;
- global orbit coverage, determinant-line orientation, and a physical
  original cycle.

Those dependencies are explicitly `NOT_EXECUTION_AUTHORIZATION`, not
automatically spawned phases.  No observation in this calculation supports a
physics or TOE claim.
