# Gate 1 — closed-FRW \(V=0\) componentwise off-shell Darboux chart

## Outcome

The preceding calculation had only established a classical **on-shell**
relational coordinate \(\Phi_*\) and endpoint potential \(B_0=P\) on one
frozen part of the closed-FRW \(V=0\) constraint surface.  The present bounded
calculation connects that result to one exact **off-shell classical Darboux
chart** on the open component

\[
\mathcal U_+
=\left\{(Q,P,\phi,p):p>0,\ R=3p^2-2P^2>0\right\}.
\]

For every real constraint value \(c\), define \(Q(c,P,p)\) by the unique
positive scale-factor root of \(C=c\), and set

\[
W(c,P,p)=-\int_0^P Q(c,u,p)\,du,
\qquad
T=W_c,
\qquad
\Phi=\phi+W_p.
\]

The exact result is

\[
\boxed{(Q,P,\phi,p)\longmapsto(T,c,\Phi,p)}
\]

as a smooth symplectomorphism from \(\mathcal U_+\) onto its open image.  Its
endpoint potential is

\[
B=PQ+W-cT-pW_p,
\]

so that

\[
P\,dQ+p\,d\phi=c\,dT+p\,d\Phi+dB,
\qquad
S_D=S_0-[B]_1^2.
\]

On \(c=0\), the chart recovers the preceding \(\Phi_*\) exactly and gives
\(B_0=P\).  The frozen verdict was therefore

```text
KEEP_V0_CLASSICAL_COMPONENTWISE_OFFSHELL_DARBOUX_CHART
```

All 18 executable exact checks and three independent-root numerical checks
passed.  Eight analytic scope guards were recorded separately and independently
reviewed; they are not added to the executable exact-check count.  The run made
six root calls, no quadratures, no ODE calls, and no descendant calculation.

This closes only the classical chart on \(\mathcal U_+\).  It is not a chart
on all components, a normalized quantum endpoint-state transformation, a
ghost/BFV construction, the old fixed-\(a\) kernel, a full-real-lapse
distributional \(\delta(C)\) kernel, a global gauge atlas, a physical original
cycle, a physics result, or a TOE.  Gate 1 remains
`OPEN_PARTIAL_PROGRESS`, global promotion remains `PROHIBITED`, and
`automatic_next=null`.

## 1. Source and interpretation boundary

Henneaux–Teitelboim–Vergara supply the general canonical endpoint framework:
changing endpoint canonical data requires the corresponding boundary
potential, and this must be distinguished from a complete gauge-fixed quantum
path integral.  They do not derive the mixed generator \(W\) used here, its
closed-FRW chart, or a normalized quantum transform.

Banihashemi–Jacobson supply reduced-phase-space, momentum-integration, and
lapse-contour context.  Their result does not derive this curved closed-FRW
component, choose a replacement BFV source, or turn a local trace chart into a
global gauge theorem.

Marolf supplies the full-real-lapse distributional physical-inner-product
path integral as a comparison boundary.  No spectral measure, regulator
removal, or \(\delta(C)\) kernel is computed below, and the classical
symplectomorphism is not promoted to such a quantum kernel.

Primary sources:

- M. Henneaux, C. Teitelboim, and J. D. Vergara,
  [*Gauge invariance for generally covariant systems*](https://doi.org/10.1016/0550-3213(92)90166-9),
  Nucl. Phys. B 387 (1992) 391–418, arXiv:hep-th/9205092.
- B. Banihashemi and T. Jacobson,
  [*On the lapse contour in the gravitational path integral*](https://doi.org/10.1103/PhysRevD.111.066014),
  Phys. Rev. D 111 (2025) 066014, arXiv:2405.10307.
- D. Marolf,
  [*Path integrals and instantons in quantum gravity: Minisuperspace models*](https://doi.org/10.1103/PhysRevD.53.6979),
  Phys. Rev. D 53 (1996) 6979–6990, arXiv:gr-qc/9602019.

These references bound the interpretation.  The equations and checks below
are repository calculations.

## 2. Constraint root and regular component

Use the canonical trace variables

\[
Q=2\log a,
\qquad
P=\frac{ap_a}{2},
\qquad
\{Q,P\}=1,
\qquad
a=e^{Q/2}>0.
\]

With \(V(\phi)=0\) and the positive-curvature term retained,

\[
C(Q,P,p)
=-\frac{P^2}{6\pi^2a^3}
+\frac{p^2}{4\pi^2a^3}
-6\pi^2a
=\frac{R}{12\pi^2a^3}-6\pi^2a,
\qquad
R=3p^2-2P^2.
\]

Writing the off-shell constraint value as \(c=C\), its scale-factor equation
is

\[
F(A;c,P,p)
=72\pi^4A^4+12\pi^2cA^3-R=0,
\qquad A=a>0.
\]

For \(R>0\), \(F(0)=-R<0\) and the positive quartic term dominates as
\(A\to\infty\), so a positive root exists.  If \(c\ge0\), \(F\) is strictly
increasing for \(A>0\).  If \(c<0\), its only positive turning point is

\[
A_t=-\frac{c}{8\pi^2},
\]

and

\[
F(A_t)
=-\frac{512\pi^4R+3c^4}{512\pi^4}<0.
\]

The curve therefore crosses zero exactly once after that turning point.  This
defines a unique smooth \(A(c,P,p)>0\) for every real \(c\) on
\(\mathcal U_+\).

The regularity factor is

\[
D:=-C_Q
=\frac{R+24\pi^4A^4}{8\pi^2A^3}>0.
\]

On \(C=c\), the same quantity is

\[
D=\frac32c+12\pi^2A.
\]

The first form establishes positivity; the second is a useful on-root
identity.  The direct implicit derivatives are

\[
Q_c=-\frac1D,
\qquad
Q_P=\frac{C_P}{D},
\qquad
Q_p=\frac{C_p}{D}.
\]

Finally, if the endpoint \((P,p)\) lies in \(R>0\), every point on the straight
integration segment from \(u=0\) to \(u=P\) does too, because

\[
3p^2-2u^2=R(P,p)+2(P^2-u^2)>0
\]

with the same conclusion for either sign of \(P\).  Hence \(W\) never crosses
the chart boundary inside its defining integral.

## 3. Mixed generator and Darboux proof

For

\[
W(c,P,p)=-\int_0^P Q(c,u,p)\,du,
\]

smooth differentiation gives

\[
W_P=-Q,
\qquad
T_P=W_{cP}=-Q_c=\frac1D>0,
\qquad
\Phi_P=W_{pP}=-Q_p=-\frac{C_p}{D}.
\]

The differential of \(W\) is

\[
dW=T\,dc-Q\,dP+W_p\,dp.
\]

With \(\Phi=\phi+W_p\), direct differentiation of

\[
B=PQ+W-cT-pW_p
\]

then gives

\[
dB=P\,dQ-c\,dT-p\,dW_p
\]

and therefore

\[
\boxed{P\,dQ+p\,d\phi=c\,dT+p\,d\Phi+dB.}
\]

This one-form identity proves the canonical transformation.  The runner also
checks it independently through the full Poisson matrix and obtains

\[
\{T,c\}=1,
\qquad
\{\Phi,p\}=1,
\qquad
\{T,\Phi\}=\{T,p\}=\{c,\Phi\}=\{c,p\}=0,
\]

together with

\[
\det\frac{\partial(T,c,\Phi,p)}{\partial(Q,P,\phi,p)}=1.
\]

The inverse is componentwise rather than global over all phase space.  At
fixed \((c,p)\), \(T_P=1/D>0\), while the normalization gives
\(T(c,0,p)=0\).  Thus \(P\) is uniquely recovered from \(T\) on the chart
image; the unique constraint root recovers \(Q\), and
\(\phi=\Phi-W_p\).  Nothing here says that the image is a rectangular global
fundamental region or that other components have no Gribov copies.

## 4. Endpoint action and recovery of the preceding result

If the original endpoint variation is

\[
[P\,\delta Q+p\,\delta\phi]_1^2,
\]

then the transformed classical action

\[
\boxed{S_D=S_0-[B]_1^2}
\]

has endpoint variation

\[
[c\,\delta T+p\,\delta\Phi]_1^2.
\]

This is a classical variational statement for fixed new endpoint coordinates.
It does not by itself give a quantum endpoint wave function, integration
measure, phase convention, operator ordering, domain, or unitarity theorem.

At \(c=0\), the positive root is explicit:

\[
Q_0(P,p)=\frac12\log\!\left(\frac{3p^2-2P^2}{72\pi^4}\right).
\]

The normalized generator derivative becomes

\[
W_{0,p}
=-\sqrt{\frac32}\,
\operatorname{artanh}\!\left(\sqrt{\frac23}\frac{P}{p}\right),
\]

so

\[
\boxed{
\Phi\big|_{c=0}
=\phi-\sqrt{\frac32}\,
\operatorname{artanh}\!\left(\sqrt{\frac23}\frac{P}{p}\right)
=\Phi_*.
}
\]

For the boundary potential,

\[
\frac{\partial B_0}{\partial P}
=P\,Q_{0,P}+p\,Q_{0,p}=1,
\qquad
B_0(0,p)=0,
\]

and hence

\[
\boxed{B_0=P.}
\]

Thus \(S_D|_{c=0}=S_0-[P]\), exactly recovering the prior relational action.
The prior finite flow used the oriented generator \(F=-P\), so \(B_0=-F\)
only within that shell-flow ledger.  It does not identify this Darboux action
with the distinct HTV improved-static action or prove equality with the old
fixed-\(a\) kernel.

The canonical gauge factor is also local and exact:

\[
\{T,c\}=1,
\qquad
\delta(P-P_f)D=\delta(T-T_f)
\]

on the connected \(D>0\) component.  This is a coordinate identity, not a
ghost action, nilpotent BRST charge, gauge fermion, global FP theorem, or
determinant-line orientation.

## 5. Independent numerical root control

The proof above is exact.  A fixed 100-digit benchmark independently compared
400-step sign-bracket bisection with arbitrary-precision polynomial roots at

\[
p=1,
\qquad
P=\frac12,
\qquad
c\in\{-0.2,0,0.2\}.
\]

| \(c\) | positive \(A\) | \(D\) | positive roots | normalized residual |
| ---: | ---: | ---: | ---: | ---: |
| \(-0.2\) | 0.138257021945486 | 16.0745053472961 | 1 | \(1.143\times10^{-101}\) |
| \(0\) | 0.137404831970170 | 16.2735760121248 | 1 | 0 |
| \(0.2\) | 0.136568208021258 | 16.4744902432260 | 1 | \(2.286\times10^{-101}\) |

The largest cross-method discrepancy was below
\(1.8\times10^{-102}\), against the frozen \(10^{-70}\) tolerance.  This is
an implementation sanity check at three points, not an empirical replication
or a substitute for the exact uniqueness proof.

## 6. What is now connected, and what remains open

The repository's narrow logical chain is now

```text
local trace simple-root reduction
  -> on-shell Phi_* and S0-[P]
  -> U_plus off-shell classical Darboux chart and S0-[B]
  -> normalized quantum endpoints / BFV source / delta(C) kernel still open
  -> physical original cycle and global n_sigma still open
```

The first three entries are not interchangeable.  In particular:

1. the old on-shell result is recovered as the \(c=0\) restriction, not
   overwritten;
2. the new result is classical and componentwise, not a full quantum
   replacement endpoint problem;
3. local FP cancellation does not supply the missing ghost, antighost,
   multiplier, BRST, source-discretization, global-copy, or orientation data;
4. the full-real-lapse \(\delta(C)\) kernel and the original Picard–Lefschetz
   cycle are independent uncomputed obligations;
5. no open obligation authorizes an automatic diagnostic phase.

The five frozen terminal decision rows are all reachable in memory.  The
actual run selected the full scoped `KEEP`; any scientific NONPASS would have
written one terminal `VALID_RUN` row rather than recursively creating another
research task.  Integrity or schema failure alone raises without a result.

## 7. Reproduction and provenance

Frozen command:

```bash
./ice run cpt_temporal_folded_susy/gate1_v0_offshell_darboux_chart
```

Observed output:

```text
exit 0
VALID_RUN
18/18 exact PASS
8 analytic scope guards recorded separately and reviewed
3/3 numerical PASS
6 root calls, 0 quadratures, 0 ODE calls, 0 descendants
```

Tracked inputs and outputs:

- `GATE1_V0_OFFSHELL_DARBOUX_CHART_INPUTS.json`
- `gate1_v0_offshell_darboux_chart.py`
- `GATE1_V0_OFFSHELL_DARBOUX_CHART_RESULT.json`

Definition commit:
`626230f4f5f35c3374c62774787ff6ac7b4cd990`.
Raw-result commit:
`7e18e4bee6ab6a6d34ac7a5dc5e2f1b5b3c1fdfb`.

The raw result is 22,218 bytes.  Its outer SHA-256 is
`6fcae74d9344984682c097731906ef1d4b1c01c4862c42ba54db7c464a7659f7`;
its canonical payload SHA-256 without the self field is
`38bfaee2fee30399bc3f1c16c17c0330bc97f6343306a9f5860d296b67a11cd5`.
The result re-verifies the frozen input, runner, and six upstream artifact
hashes, and all 29 executable/guard/numerical IDs are unique.

Three independent read-only audits were completed before this report was
frozen: an exact mathematics/sign/hash audit, a literature/BFV scope audit,
and an ontology/schema/count audit.  They found no conclusion-changing error.
The scope audit required the eight analytic guards to remain visibly separate
from the 18 executable exact checks, and confirmed that
`full_off_shell_canonical_transform=null` refers to the uncomputed
all-component/global completion rather than contradicting the kept
componentwise chart.
