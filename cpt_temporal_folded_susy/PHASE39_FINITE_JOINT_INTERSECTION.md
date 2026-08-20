# Phase 39 — finite-cutoff full-joint local intersection pilot

## Outcome

Phase 39 performs the calculation that Phase 38 could only name, at the
smallest nontrivial configuration cutoff. One explicit nonlinear two-segment
midpoint action is defined on

\[
X_2=\mathbb C_{a_1}\times\mathbb C_{\phi_1}\times\mathbb C_T^*.
\]

Its discrete joint saddle is re-solved, one finite-radius, finite-time
three-real-dimensional chart patch approximating the upward
Picard--Lefschetz manifold is integrated in the full field--lapse space, its
tangent frame is transported with the variational equation, and the local
orientation is evaluated directly in all six real ambient directions:

\[
\epsilon_x=\operatorname{sgn}\det_{\mathbb R}
[V_\Gamma(x),V_{\mathcal K}(x)].
\]

For the frozen post-feasibility inputs,

\[
\boxed{\epsilon_x(r=0.3)=+1,\qquad \epsilon_x(r=0.2)=+1.}
\]

These are configuration-only coordinate signs for two local intersection
candidates. They are not inferred from the Phase-32 lapse projection, do not
inherit its momentum--configuration normalization, and are not a global
Picard--Lefschetz coefficient. The finite arms, field box, other saddles,
other upward components, reintersections, Stokes chamber, and good ends remain
incomplete. Therefore

\[
\boxed{
\texttt{complete\_global\_signed\_intersection\_vector=null},\qquad
\texttt{global\_n\_sigma=null}.
}
\]

Gate 1 remains
`OPEN_PARTIAL_LOCAL_FULL_SPACE_INTERSECTION_PILOT`. The executable passes
12 exact and 17 numerical checks and its final production run exits zero.

## 1. Provenance and epistemic status

The input was frozen in
`PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json` before the production run.
The final manifest bytes have:

- SHA256:
  `b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4`
- commit:
  `750d19e76827ce78c9322e9fac6b494ade1f2bbf`

This is a post-feasibility workflow freeze, not a preregistration. Approximate
saddle and intersection locations had already been inspected while deciding
whether the calculation was feasible. The positive sign is consequently an
explicit construction and algorithm witness, not an out-of-sample
prediction.

The frozen choices include:

- cutoff \(m=2\);
- the Phase-25 equal-endpoint benchmark;
- one finite lower-bypass Gaussian lift anchored at the constant endpoint
  history rather than at the target saddle;
- cap radii \(r=0.3,0.2\), field window
  \(|y_a|,|y_\phi|\leq0.25\), and finite lapse-arm cutoff \(R=1.2\);
- a constant positive Hermitian local-Morse-whitened metric selected after
  the feasibility pilot;
- ambient order
  \((\Re a_1,\Im a_1,\Re\phi_1,\Im\phi_1,\Re T,\Im T)\);
- parameter orders \((y_a,y_\phi,\psi)\) and
  \((\alpha,\beta,\tau)\);
- fail-closed global outputs.

No desired local sign, global coefficient, SUSY scale, or cosmological target
is an input.

## 2. Explicit joint action

For \(m=2\), \(h=1/2\), fixed endpoints

\[
(a_0,\phi_0)=(a_2,\phi_2)
=(3.5668031935672753,1.0185809464006637),
\]

and

\[
V(\phi)=\frac34(1-e^{-\sqrt{2/3}\phi})^2,
\]

the production scalar is

\[
S_2=2\pi^2\sum_{e=0}^{1}\left[
\frac{-6a_{e+1/2}(\Delta a_e)^2
+a_{e+1/2}^3(\Delta\phi_e)^2}{2Th}
+Th(-3a_{e+1/2}+a_{e+1/2}^3V(\phi_{e+1/2}))
\right].
\]

Because the endpoints are equal and there is one interior node, the two
midpoint elements are exactly identical. SymPy constructs this scalar first
and differentiates the same expression to obtain all three joint equations
and the full Hessian. The action contains neither `Abs` nor conjugation. It
is holomorphic on \(X_2\) and has a generically nonzero simple pole at
\(T=0\).

Thus the result is not a Hessian sampled from the old continuum BVP, and
\(T=0\) is an excluded divisor rather than a numerical endpoint through
which a trajectory may be reset.

## 3. Genuine discrete saddle, without a saddle census

The positive-\(T\) critical point is

\[
(a_1,\phi_1,T)_\sigma=
(3.590472030474745,\ 0.9934626322043222,\ 0.8160508821989653),
\]

\[
S_2(z_\sigma)=1.6338899787306218,\qquad
\max_I|\partial_I S_2|=2.73\times10^{-12}.
\]

In the frozen dimensionless reference coordinates, the Hessian spectrum is

\[
(-2.63473378238\times10^4,\ -3.67679978769,
4.59873115693\times10^3),
\]

with inertia \((2_-,1_+)\).

A six-seed real search finds four distinct roots in its bounded ledger:

| \(a_1\) | \(\phi_1\) | \(T\) | \(S_2\) | inertia |
|---:|---:|---:|---:|---:|
| -0.3002159125 | -0.4433350533 | -7.5960704250 | +1426.45024045 | \((2_-,1_+)\) |
| -0.3002159125 | -0.4433350533 | +7.5960704250 | -1426.45024045 | \((1_-,2_+)\) |
| 3.5904720305 | 0.9934626322 | -0.8160508823 | -1.6338899787 | \((1_-,2_+)\) |
| 3.5904720305 | 0.9934626322 | +0.8160508822 | +1.6338899787 | \((2_-,1_+)\) |

This is a nonuniqueness warning, not a complete critical-point census. The
negative-\(a\) roots cannot be silently removed from the declared complex
integration space without a new domain or relative-cycle argument.

## 4. Frozen Hermitian metric and an upward-flow chart patch

Introduce dimensionless reference coordinates

\[
z=Dw,\qquad
D=\operatorname{diag}(3.5668031935672753,1.0185809464006637,0.7).
\]

At the new saddle, write

\[
H_w=O\Lambda O^T,\qquad \det O=+1,
\]

and freeze

\[
L=O|\Lambda|^{-1/2},\qquad w=w_\sigma+L\xi.
\]

The Euclidean Hermitian metric in \(\xi\) is held constant along every
trajectory and gives

\[
L^TH_wL=\operatorname{diag}(-1,-1,+1)
\]

to numerical precision. It is a valid positive PL-flow metric for this
finite pilot, but it is not derived from quantum gravity and metric-homotopy
invariance is not established.

For the \(e^{-S_2}\) convention, the dual upward flow is

\[
\dot\xi=-\overline{\partial_\xi S_2},\qquad
\frac{d}{d\tau}\Re S_2=-\|\partial_\xi S_2\|^2,\qquad
\frac{d}{d\tau}\Im S_2=0.
\]

The identities are checked symbolically and along both numerical
trajectories. The maximum sampled imaginary-action drifts are
\(2.1\times10^{-25}\) and \(5.2\times10^{-26}\).

With eigenvalues ordered negative, negative, positive, the local upward frame
is \((-e_1,-e_2,ie_3)\). Starting from a radius \(10^{-4}\) sphere, the code
integrates the three-real-dimensional local parameterization and transports
the \(\alpha,\beta\) tangents. The flow vector is the third tangent. A doubled
radius \(2\times10^{-4}\) is a control.

The finite-radius linear sphere is only a local approximation to the exact
nonlinear unstable manifold. The radius control supports the local witness;
it does not replace an \(\epsilon\to0\) certificate.

## 5. Independently anchored regulated chain

The lower lapse bypass is

\[
N\in[-R,-r]\cup\{re^{i\theta}:-\pi\leq\theta\leq0\}\cup[r,R],
\qquad T=iN,
\]

oriented from negative to positive \(N\). On the right \(T\)-cap,

\[
\psi=\arg T=\theta+\frac\pi2,\qquad
-\frac\pi2\leq\psi\leq\frac\pi2,
\]

and

\[
a_1=a_\partial+e^{i(\psi/2-\pi/2)}y_a,\qquad
\phi_1=\phi_\partial+e^{i\psi/2}y_\phi,\qquad
T=re^{i\psi}.
\]

The half-angles are continuously unwrapped from Phase 32 rather than reset
with a principal root at each sample. Their endpoint values define continuous
field planes on the two finite arms.

The anchor is the constant endpoint history, not the saddle being tested.
This prevents the most immediate circularity. Nevertheless the chain is
still declared rather than physically selected. Uniform decay on its arms
and field-box faces, homology to a physical original cycle, and an
\(R,Y\to\infty\) limit are unproved.

The cap tangent includes

\[
\partial_\psi a_1=\frac i2(a_1-a_\partial),\qquad
\partial_\psi\phi_1=\frac i2(\phi_1-\phi_\partial),\qquad
\partial_\psi T=iT.
\]

Dropping the first two terms would reduce the calculation toward a lapse
projection and could change the full determinant.

## 6. Direct six-real-dimensional intersections

The equations

\[
\Gamma(y_a,y_\phi,\psi)
=\mathcal K(\alpha,\beta,\tau)
\]

are solved in six real coordinates:

| \(r\) | \(y_a\) | \(y_\phi\) | \(\alpha\) | \(\beta\) | \(\tau\) | max residual |
|---:|---:|---:|---:|---:|---:|---:|
| 0.3 | \(2.51\times10^{-18}\) | \(-4.87866146\times10^{-4}\) | 1.8402186306 | \(-4.16\times10^{-16}\) | 10.5779535911 | \(2.64\times10^{-9}\) |
| 0.2 | \(6.98\times10^{-16}\) | \(+5.46706059\times10^{-4}\) | 1.8461179444 | \(-1.18\times10^{-18}\) | 11.3917410827 | \(3.48\times10^{-8}\) |

Both roots lie far inside the field window and on the observed real-symmetry
component \(\beta\simeq0\). The \(\beta\) tangent is not deleted: it is
transported and retained in the full \(6\times6\) matrix.

Positive column normalization removes meaningless tangent magnitudes without
changing the sign:

| \(r\) | direct sign | normalized \(\sigma_{\min}\) | condition number | max tangent FD error |
|---:|---:|---:|---:|---:|
| 0.3 | +1 | 0.0752060 | 18.7875 | \(1.33\times10^{-5}\) |
| 0.2 | +1 | 0.0696581 | 20.2776 | \(2.41\times10^{-3}\) |

The \(r=0.2\) \(\beta\) tangent has raw norm \(1.33\times10^4\), making its
finite-difference control stiff. The 0.24% discrepancy is nevertheless much
smaller than the normalized transversality gap.

The root solver differentiates \(\Gamma-\mathcal K\), so its Jacobian is
\([V_\Gamma,-V_\mathcal K]\). Since either chart has real dimension three,

\[
\operatorname{sgn}\det[V_\Gamma,V_\mathcal K]
=-\operatorname{sgn}\det[V_\Gamma,-V_\mathcal K].
\]

The code checks this twice: from the assembled analytic tangent matrix and
from the finite-difference Jacobian returned by the actual six-variable
solver. The latter is also compared entrywise with the positively row-scaled
assembled Jacobian; the spectral relative errors are
\(1.76\times10^{-3}\) and \(1.07\times10^{-3}\) at the two caps. Reversing
the first \(\Gamma\) parameter or first
\(\mathcal K\) parameter leaves the root fixed and flips the direct sign.

The lapse-only coordinate sign also happens to be +1. It is recorded only as
a contrast and is not used to obtain the six-dimensional sign.

## 7. Bounded controls

At \(r=0.3\), doubling the initial sphere radius changes the flow time from
10.57795 to 9.88477 but preserves

\[
\epsilon_x=+1,\qquad \sigma_{\min}=0.0752060
\]

at a nearby root.

A separate first-hit ledger samples \(3\times3\) points on each of six
normalized cubed-sphere faces. It records 54 samples including overlaps:

- 33 reach the declared \(r=0.3\) cap inside the field window;
- 21 leave the finite flow-norm box;
- the best coarse membership residual is \(2.30\times10^{-2}\);
- continuous coverage, root exhaustion, and overlap deduplication are not
  claimed.

The numerically resolved, locally transverse candidate comes from a finer
49-angle real-component scan followed by the full six-variable solve. No
interval Newton or Krawczyk certificate is supplied. The cubed-face ledger is
only an atlas/pole smoke test and does not exclude other complex-direction
intersections.

## 8. Why Gate 1 remains open

| object | status |
|---|---|
| negative lapse arm at \(-R\) | `FINITE_ARM_CUTOFF_UNRESOLVED` |
| positive lapse arm at \(+R\) | `FINITE_ARM_CUTOFF_UNRESOLVED` |
| straight-arm intersection searches | `NOT_PERFORMED` |
| later cap reintersections | `NOT_PERFORMED` |
| field-box faces | `FINITE_FIELD_WINDOW_UNRESOLVED` |
| \(T=0\) | `EXCLUDED_SIMPLE_ACTION_POLE` |
| nonhitting upward directions | `FLOW_TIME_BOX_EXIT_UNRESOLVED` or `FLOW_NORM_BOX_EXIT_UNRESOLVED` |
| other saddles and components | `NOT_EXHAUSTED` |
| Stokes chamber | `REAL_SADDLE_NOT_LATERALLY_CERTIFIED` |
| BFV/Pfaffian/Pin orientation | `NOT_PRESENT_IN_M2_CONFIGURATION_MODEL` |

A finite local sign is not yet an integer pairing in a completed relative
homology problem. The bounded-chain signed sum is therefore also null. A box
exit is not a good end. Moreover, all four recorded real critical actions
have zero imaginary part, so this slice is critical-phase degenerate and a
lateral Stokes chamber is required before a thimble basis can be promoted.

The \(m=2\) cutoff has one interior node fixed by reflection of the
equal-endpoint lattice. No reflection-odd history mode exists. Phase 39 tests
the full-joint algorithm and orientation bookkeeping but cannot test the
first extra mode's determinant-line contribution or predict an \(m=5\) sign.

## 9. Interpretation and gate status

The precise advance is

\[
\text{projected lapse crossing}
\longrightarrow
\text{one explicit local full-space intersection witness}.
\]

Phase 39 does not infer missing field data from the old projection. It adds a
new finite action, chain embedding, finite-radius upward-chart tangent, and
direct determinant. But

\[
\text{local witness}
\not\Rightarrow\text{physical original contour}
\not\Rightarrow\text{global }n_\sigma
\not\Rightarrow\text{BFV/Pin holonomy or quantum gravity}.
\]

| Gate | status after Phase 39 |
|---|---|
| 1. original joint cycle and global intersections | local \(m=2\) +1 witness; global vector null; OPEN |
| 2. hard CFU coefficients | exploratory work allowed; physical promotion depends on Gate 1 |
| 3. BFV/Pfaffian/Pin line | not computed |
| 4. spinorial charge/common domain | not computed |
| 5. persistent order/pole splitting | not computed |

## 10. Next calculation

The next calculation should preserve this API while adding what \(m=2\)
cannot see:

1. run the joint action and determinant at \(m=3\) or \(m=4\);
2. apply a signed endpoint-asymmetry mutation and take it back to zero,
   checking whether the root and \(\sigma_{\min}\) survive;
3. fix added-mode orientation with a discrete history/sine basis rather than
   comparing raw cutoff signs;
4. promote to the already feasible \(m=5\) joint saddle;
5. replace bounded first-hit sampling with all-component continuation and
   classify arms, field faces, singular exits, reintersections, and Stokes
   jumps as relative good or bad ends;
6. only after cutoff, metric-homotopy, regulator, anchor, and end stability
   propose a finite-cutoff candidate vector.

Gate-2 hard-CFU data may be explored in parallel, but no physical kernel
should be promoted without the Gate-1 typed cycle vector.

## 11. Reproduction

From the repository root:

    ./ice run phase39_finite_joint_intersection

The equivalent locked Python command is:

    uv run --locked python3 \
      cpt_temporal_folded_susy/phase39_finite_joint_intersection.py

The script reads the committed manifest, prints every check, and ends with
one machine-readable `PHASE39_RESULT=...` payload. It writes no files.

## References and scope

- Phase 30 supplies the midpoint action convention, but Phase 39 re-solves
  the nonlinear discrete critical point.
- Phase 32 supplies the lower full-lapse bypass and local configuration
  half-angle rays. It does not supply the Phase-39 joint sign.
- Phase 38 supplies the fail-closed global boundary and the warning against
  inverse reconstruction from projected data.
- Witten's Picard--Lefschetz framework fixes the relative-cycle language; it
  does not select this repository's finite chain or certify its good ends.

All numerical values above are repository calculations. No cited work
supplies the \(m=2\) saddle, transported tangent matrix, or local sign.
