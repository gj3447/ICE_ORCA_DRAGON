# Gate 1 — Starobinsky \(m=2\) naive local-lapse gauge test

## Outcome

The bounded result is

```text
KILL_NAIVE_MIDPOINT_TWO_LOCAL_LAPSE_UNFIXING_AT_CERTIFIED_M2_SADDLE
```

The frozen equal-endpoint midpoint action can be extended from one proper-time
variable to two segment-local lapse variables in the obvious algebraic way.
That extension restricts exactly to the old action, but its relative-lapse
direction is not a gauge zero mode at the certified positive-real saddle.  A
strict Arb/Krawczyk enclosure proves that the saddle exists uniquely within the
frozen box and that the full extended Hessian is invertible there.

This retires only
`NAIVE_MIDPOINT_TWO_LOCAL_LAPSE_UNFIXING` near that certified saddle.  It does
not rule out a newly derived first-order constraint lattice, a perfect or
improved gauge-preserving action, a continuum-first time-dependent trace
source, or a constraint-adapted improved-static source.  No BFV source,
relative cycle, global intersection coefficient, physical result, or TOE claim
is produced.

## 1. Exact candidate action

With the fixed endpoint \((a_b,\phi_b)\), set

\[
A=a_b+\frac{x}{2},\qquad
\Phi=\phi_b+\frac{q}{2},
\]

\[
V(\Phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\Phi}\right)^2,
\qquad
K=-6Ax^2+A^3q^2,
\qquad
W=-3A+A^3V(\Phi).
\]

The frozen proper-time action is exactly

\[
S_2(x,q,T)=\frac{4\pi^2K}{T}+2\pi^2WT,
\qquad T\ne0.
\]

The tested candidate introduces

\[
N_0=T+r,\qquad N_1=T-r
\]

and no other new field.  Applying the same midpoint rule separately to the two
segments gives

\[
\begin{aligned}
S_{\mathrm{loc}}(x,q,T,r)
&=2\pi^2\left[
K\left(\frac1{N_0}+\frac1{N_1}\right)
+\frac{W}{2}(N_0+N_1)
\right]\\
&=\frac{4\pi^2KT}{T^2-r^2}+2\pi^2WT .
\end{aligned}
\]

Thus

\[
S_{\mathrm{loc}}(x,q,T,0)=S_2(x,q,T),
\]

but the extension introduces two new divisors \(T-r=0\) and \(T+r=0\).
Equality on the \(r=0\) slice is not equality of measures, cycles, or BFV
sources.

## 2. Relative-lapse curvature

Exact differentiation gives

\[
\partial_rS_{\mathrm{loc}}
=\frac{8\pi^2KTr}{(T^2-r^2)^2},
\qquad
\left.\partial_r^2S_{\mathrm{loc}}\right|_{r=0}
=\frac{8\pi^2K}{T^3}.
\]

All mixed entries with the \(r\) direction vanish at \(r=0\).  Therefore, at
any exact stationary point \(y_*=(x_*,q_*,T_*)\) of \(S_2\),

\[
H_{\mathrm{loc}}(y_*,0)
=\operatorname{diag}\!\left(
H_{S_2}(y_*),\frac{8\pi^2K(y_*)}{T_*^3}
\right),
\]

\[
\det H_{\mathrm{loc}}
=\frac{8\pi^2K}{T^3}\det H_{S_2}.
\]

For the endpoint-preserving two-element lapse variation already fixed in the
repository,

\[
\delta(N_0,N_1)=(2\epsilon,-2\epsilon),
\qquad \delta T=0,
\qquad \delta r=2\epsilon.
\]

Hence its proposed gauge generator is nonzero in the \(r\) direction.

## 3. Computer-assisted proof

The runner did not reuse the old floating saddle as an exact root.  It froze a
box of uniform radius \(10^{-55}\) around

\[
\begin{aligned}
x_0&=0.0236688369074702269682774014574800709571954294264750849239483,\\
q_0&=-0.0251183141963413803838389432132798317422952401980562213133411,\\
T_0&=0.816050882198965292374365861002243412362617790046994654691017.
\end{aligned}
\]

At 300-bit precision, python-flint/Arb outward-rounded ball arithmetic gave a
strict Krawczyk inclusion in all three coordinates.  It therefore certifies
one unique zero of \(\nabla S_2\) **within this box**.  The same enclosure gives

| certified quantity | enclosing value | zero excluded |
|---|---:|:---:|
| \(K\) | \(0.01688691492046650567929968568824807\ldots\) | yes |
| \(8\pi^2K/T^3\) | \(2.45351282152588807358593650152211148\ldots\) | yes |
| \(\det H_{S_2}\) | \(68880973.05375388796696460656014798\ldots\) | yes |
| \(\det H_{\mathrm{loc}}\) | \(169000350.54656436853150872058030407\ldots\) | yes |

The raw result records the full outward lower and upper enclosures, not only
the displayed decimal summaries.

For a twice-differentiable finite action with an off-shell infinitesimal gauge
identity

\[
(\partial_AS)R^A=0,
\]

differentiation at an exact stationary point implies

\[
H_{AB}R^B=0.
\]

The certified invertible \(H_{\mathrm{loc}}\) has no such nonzero vector, while
the declared relative-lapse generator has \(R^r=2\).  The tested extension is
therefore not an exact endpoint-preserving reparametrization gauge action near
this saddle.

This argument concerns the displayed pushed-forward configuration action.  It
does not exclude a larger first-order action whose extra variables and
constraints change the Hessian and boundary problem.

## 4. What changed in the requested sequence

| Requested construction | Status after this audit |
|---|---|
| Named chain/end model and exact joint \(m=2\) action | The bosonic action and conditional Pham--Witten relative-chain type remain fixed; no production chain is admitted. |
| Replacement-gauge FP/BFV source | Direct \(V=0\) transplant was already retired.  The naive two-local-lapse unfixing of the Starobinsky midpoint action is now also retired at the certified saddle.  No BFV source is constructed. |
| Source and limit order including \(N=0\) | Still blocked.  The BFV multiplier locus and the proper-time/local-lapse divisors must not be conflated. |
| \(U_1/U'_1\), overlaps and orientation transport | Still blocked by the missing common source and determinant/orientation local system. |
| End/divisor census and candidate completeness | Still open.  The new \(T\pm r=0\) divisors belong only to the retired candidate and are not a complete end census. |
| Independent mathematical review and preregistration | Three post-run read-only audits found no algebra, interval, hash, citation, or scope blocker.  Human mathematical sign-off and independent custody are still absent, so preregistration remains closed. |

`UNIQUE_LATERAL`, `STOKES_SPLIT`, and `NO_ADMISSIBLE_LIFT` remain unevaluated.
Missing values remain null, not zero.

## 5. Outcome-bound route change

- Unexpected outcome: the most obvious same-action local-lapse extension is
  an exact \(r=0\) restriction but has no discrete gauge null direction at the
  certified saddle.
- Retired mechanism:
  `NAIVE_MIDPOINT_TWO_LOCAL_LAPSE_UNFIXING`, in this exact scope only.
- Live competitors:
  `PERFECT_OR_IMPROVED_DISCRETE_GAUGE_SOURCE`,
  `CONTINUUM_FIRST_TIME_DEPENDENT_TRACE_SOURCE_WITH_CONTROLLED_DISCRETIZATION`,
  and `STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE`.
- Next discriminating question: can an exact Hamilton-principal-function cell
  action, or another proved gauge-preserving construction, produce one
  same-model finite BFV source with a controlled map to the frozen midpoint
  kernel?
- Changed selection: solve that source construction before \(N=0\), cover
  descent, end census, or source-to-fold transport.

The literature supports this ordering but does not supply the repository
result.  Bahr--Dittrich--Steinhaus explain why naive discretizations generally
break reparametrization symmetry and why an exactly invariant discrete path
integral is a stronger construction.  Dittrich--Höhn show that a variational
discrete system needs an actual constraint/symmetry analysis; the word
“variational” does not establish first-class gauge freedom.  Neither source
selects a unique replacement for this model.

## 6. Execution and review

- Planner checkpoint: `research-agent:ca0690e93d5ecb927655`
- Input/runner commit before execution:
  `daa52c4fb6e0796032dada4cee4caceac5757448`
- Command: `./ice run gate1_m2_starobinsky_naive_local_lapse_gauge_test`
- Observed result: `VALID_RUN`; 10/10 exact checks, 6/6 certified interval
  checks, and 3/3 theorem/scope guards
- Input SHA-256:
  `3f7382a5ceb00ec58e8187235312eebfafc0168cd196110d82dcf1a3bb602477`
- Runner SHA-256:
  `7fb2b6f3a4a5af59dc01306092bb42e663d8c2761fffd64a78972ff0225f79c9`
- Raw result SHA-256:
  `547856814bbb430a52d37ccbd1c660d2b098d0ff7dd0568a2205ddb566226fcc`
- Canonical payload SHA-256 excluding its self field:
  `005dd1f4fda97b71a084914d1f52e4692835972611c7afef41f7a99fb8910808`
- Automatic descendants: zero

Independent read-only audits recomputed the raw and canonical payload hashes,
checked the exact action and Hessian factorization, inspected the full Arb
enclosures and Krawczyk inclusion, and reviewed the Noether and citation
ceilings.  They found no blocker.  This is independent AI review, not the
human mathematical review or independent custody required for preregistration.

## Primary sources and artifacts

- [Raw result](GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST_RESULT.json)
- [Input manifest](GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST_INPUTS.json)
- [Bounded runner](gate1_m2_starobinsky_naive_local_lapse_gauge_test.py)
- [Bahr, Dittrich, and Steinhaus, *Perfect discretization of reparametrization invariant path integrals*](https://arxiv.org/abs/1101.4775)
- [Dittrich and Höhn, *Constraint analysis for variational discrete systems*](https://arxiv.org/abs/1303.4294)
- [Krawczyk and Neumaier, *An improved interval Newton operator*](https://doi.org/10.1016/0022-247X(86)90303-3)
