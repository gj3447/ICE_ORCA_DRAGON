# Phase 34 — directed reduced-dual continuation through the fold

## Result

The right positive-real projected dual inherited from Phases 28 and 32 reaches
the Phase-25 Dirichlet fold.  On the frozen reflection-symmetric
fixed-boundary stationary family, it has a bounded continuation into a
conjugate pair of complex sheets.  The upper sheet was continued from

\[
T_c=9.788625568081242
\]

to

\[
T=13+2.89138959974\,i.
\]

At every frozen point its constant-\(\operatorname{Im}W\) tangent is a
positive reparametrization of

\[
\frac{dT}{ds}=-\overline{W_T}
\]

in the declared flat complex-\(T\) metric.  Complex conjugation supplies the
lower sheet.  No sampled endpoint-Jacobi zero occurs, and the bounded lapse
bases cannot meet the Phase-32 imaginary axis or its \(r\leq0.1\) endpoint
caps.

This is a **reduced stationary-family continuation**, not the full joint
field--lapse Picard--Lefschetz dual.  It does not determine a global
intersection coefficient.

## 1. Frozen fold and soft orientation

The equal Phase-24 boundaries remain

\[
q_\partial=
(3.56680319356728,1.01858094640066;
 3.56680319356728,1.01858094640066).
\]

The Phase-25 fold data are

\[
c_c=(1.24799533026157,0.100167953906586),
\]

\[
v_R=(0.996483931960381,-0.0837840876585722).
\]

The singular vector has an arbitrary overall sign.  Phase 34 removes that
ambiguity by requiring

\[
\lVert v_R\rVert=1,
\qquad (v_R)_a>0,
\]

and defines the oriented midpoint soft coordinate

\[
u=v_R^{\mathsf T}(c-c_c).
\]

Thus \(+u\) is the real sheet with the larger midpoint scale factor.

At \(\delta=T_c-T=2\times10^{-4}\), the two actual real solutions give

| sheet | \(u\) | \(W\) | \(W_T\) | endpoint residual |
|---:|---:|---:|---:|---:|
| \(-u\) | \(-0.01674743720\) | \(-1157.017567807\) | \(-72.74004841\) | \(2.51\times10^{-14}\) |
| \(+u\) | \(+0.01677434027\) | \(-1157.017304686\) | \(-74.71344631\) | \(1.29\times10^{-13}\) |

Both have \(W_T<0\).  Therefore the projected flat-\(T\) dual has
\(dT/ds=-W_T>0\) on both sheets near the fold.

With

\[
u_\pm=\pm R\sqrt{\delta}+O(\delta),
\qquad \delta=T_c-T,
\]

and \(dT/ds>0\), one has

\[
u_+\frac{du_+}{ds}
=u_-\frac{du_-}{ds}
=-\frac{R^2}{2}\frac{dT}{ds}<0.
\]

Consequently both real sheets are oriented into \(u=0\).  This statement is
about the projected base flow; it does not construct a smooth full-field
gradient chart at the degenerate Hessian.

## 2. Airy seed and its sign

The last Phase-33 two-sheet data give

\[
\frac{|\Delta W|}{\delta^{3/2}}
=C=93.0272067265,
\]

\[
R=1.18517380847,
\qquad
W_{T,c}=-73.7258537571.
\]

The two singular actions lie half an action gap from their common regular
part.  For the upper continuation, the leading imaginary singular action is
\(+C\tau^{3/2}/2\), where

\[
\tau=\operatorname{Re}T-T_c>0.
\]

The regular term contributes
\(W_{T,c}\operatorname{Im}T\).  Constant phase therefore fixes

\[
\operatorname{Im}T
=\kappa\tau^{3/2}+O(\tau^{5/2}),
\qquad
\kappa=\frac{C}{2|W_{T,c}|}
=0.630899487668.
\]

With the orientation of Section 1, the corresponding midpoint seed is

\[
u=-iR\sqrt\tau+O(\tau).
\]

Thus the **upper** \(T\) arm has \(\operatorname{Im}u<0\).  The lower arm is
the complex conjugate:

\[
T_-(\tau)=\overline{T_+(\tau)},
\qquad
u_-(\tau)=\overline{u_+(\tau)}.
\]

For the first five points,

\[
\frac{\operatorname{Im}T}{\tau^{3/2}}
=(0.63089664,0.63086783,0.63083181,0.63072367,0.63054319)
\]

at
\(\tau=(0.0002,0.001,0.002,0.005,0.01)\).  A log--log fit gives

\[
p=1.49986759
\]

for \(\operatorname{Im}T\propto\tau^p\), and the smallest-\(\tau\) ratio
differs from \(\kappa\) by \(2.84\times10^{-6}\).

## 3. Constant phase and directed flow

Write the tracked branch as

\[
T(x)=x+i y(x),
\qquad
W_T=A+iB.
\]

Hamilton--Jacobi differentiation along the stationary family gives

\[
\frac{dW}{dx}=W_T(1+i y').
\]

The constant-phase equation is therefore

\[
0=\operatorname{Im}\frac{dW}{dx}=B+A y',
\qquad
y'=-\frac{B}{A}.
\]

Every recorded point has \(A=\operatorname{Re}W_T<0\).  Hence

\[
1+i y'
=\frac{-\overline{W_T}}{-A},
\]

where \(-A>0\).  The fixed-\(\operatorname{Re}T\) continuation is therefore
pointwise parallel, with the same orientation, to the reduced dual field
\(-\overline{W_T}\).  It also obeys

\[
\frac{d\operatorname{Re}W}{dx}
=\frac{A^2+B^2}{A}<0.
\]

This identity uses the declared flat Hermitian metric on the complex
\(T\)-plane.  Multiplication by a positive scalar Hermitian factor changes
only the parametrization in one complex dimension.  A field-dependent joint
metric, its off-diagonal field--lapse blocks, and its full gradient flow were
not computed.

## 4. Boundary-value construction

For each fixed \(x=\operatorname{Re}T\), Phase 34 solves for

\[
(y,\operatorname{Re}a_c,\operatorname{Im}a_c,
    \operatorname{Re}\phi_c,\operatorname{Im}\phi_c).
\]

Starting from

\[
q(0)=(a_c,0,\phi_c,0),
\]

it integrates from the reflection center to the right boundary on
\(s\in[0,1]\):

\[
\frac{dq}{ds}=\frac{T}{2}F(q),
\qquad
\frac{dS_{1/2}}{ds}=\frac{T}{2}L(q).
\]

The five root equations are

\[
\operatorname{Re/Im}(a(1)-a_\partial)=0,
\quad
\operatorname{Re/Im}(\phi(1)-\phi_\partial)=0,
\quad
\operatorname{Im}(2S_{1/2})=0.
\]

The left-boundary velocity of the reflected full interval is minus the
right-half endpoint velocity.  Phase 34 then independently reintegrates the
full interval and the complex variational system

\[
\frac{dM}{ds}=T A(q)M,
\qquad M(0)=I_4.
\]

The endpoint Jacobi block is

\[
B_v=M_{(a,\phi),(\dot a,\dot\phi)}.
\]

Continuation uses the previous root as the next guess, with
\(\Delta\tau\leq0.01\) near the fold and \(\Delta\tau\leq0.04\) thereafter.

## 5. Robust bounded table

Only points through \(\operatorname{Re}T=13\) enter the frozen pass gates.
The table reports the upper arm; the lower arm is its conjugate.

| \(\tau\) | \(T\) | \(a_c\) | \(\phi_c\) | \(\operatorname{Re}W\) | \(W_T\) | full endpoint residual | \(\sigma_{\min}(B_v)\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0002 | \(9.788825568+0.000001784i\) | \(1.248055-0.016703i\) | \(0.100140+0.001404i\) | -1157.046928 | \(-73.7294+0.9867i\) | \(4.50\times10^{-11}\) | 0.05780 |
| 0.001 | \(9.789625568+0.000019950i\) | \(1.248291-0.037352i\) | \(0.100030+0.003136i\) | -1157.105949 | \(-73.7434+2.2067i\) | \(4.64\times10^{-11}\) | 0.12923 |
| 0.002 | \(9.790625568+0.000056423i\) | \(1.248588-0.052832i\) | \(0.099892+0.004430i\) | -1157.179800 | \(-73.7609+3.1211i\) | \(4.56\times10^{-11}\) | 0.18275 |
| 0.005 | \(9.793625568+0.000222994i\) | \(1.249476-0.083569i\) | \(0.099478+0.006979i\) | -1157.401856 | \(-73.8136+4.9371i\) | \(4.64\times10^{-11}\) | 0.28886 |
| 0.01 | \(9.798625568+0.000630543i\) | \(1.250958-0.118268i\) | \(0.098793+0.009811i\) | -1157.773620 | \(-73.9014+6.9870i\) | \(4.63\times10^{-11}\) | 0.40831 |
| 0.02 | \(9.808625568+0.001782422i\) | \(1.253925-0.167489i\) | \(0.097432+0.013707i\) | -1158.523424 | \(-74.0772+9.8952i\) | \(4.59\times10^{-11}\) | 0.57688 |
| 0.05 | \(9.838625568+0.007033422i\) | \(1.262852-0.265924i\) | \(0.093444+0.020882i\) | -1160.823119 | \(-74.6064+15.7116i\) | \(5.16\times10^{-11}\) | 0.90952 |
| 0.1 | \(9.888625568+0.019835157i\) | \(1.277817-0.378626i\) | \(0.087112+0.027704i\) | -1164.824028 | \(-75.4940+22.3727i\) | \(5.07\times10^{-11}\) | 1.28034 |
| 0.2 | \(9.988625568+0.055764145i\) | \(1.308071-0.542463i\) | \(0.075668+0.034268i\) | -1173.459232 | \(-77.2904+32.0599i\) | \(5.46\times10^{-11}\) | 1.79534 |
| 0.5 | \(10.288625568+0.216193420i\) | \(1.401237-0.888197i\) | \(0.050466+0.035100i\) | -1204.466113 | \(-82.8351+52.5174i\) | \(6.36\times10^{-11}\) | 2.78310 |
| 1.0 | \(10.788625568+0.590260671i\) | \(1.562514-1.316274i\) | \(0.029039+0.023136i\) | -1273.069869 | \(-92.4473+77.8674i\) | \(9.46\times10^{-11}\) | 3.86616 |
| 1.7 | \(11.488625568+1.242130275i\) | \(1.795292-1.802227i\) | \(0.016482+0.009781i\) | -1403.310527 | \(-106.2971+106.6669i\) | \(6.43\times10^{-10}\) | 5.00799 |
| 2.211374432 | \(12+1.774406550i\) | \(1.968086-2.113435i\) | \(0.011496+0.004204i\) | -1522.102692 | \(-116.5522+125.1180i\) | \(1.16\times10^{-9}\) | 5.73162 |
| 3.211374432 | \(13+2.891389600i\) | \(2.309548-2.657646i\) | \(0.005396-0.000621i\) | -1807.116953 | \(-136.7778+157.3752i\) | \(2.39\times10^{-9}\) | 7.04089 |

Across this table:

- the largest five-equation root residual is \(9.94\times10^{-11}\);
- the largest \(|\operatorname{Im}W|\) is \(9.94\times10^{-11}\);
- the smallest sampled \(\sigma_{\min}(B_v)\) is \(0.05780\);
- upper/lower reintegrations are conjugate to displayed precision.

The flow-direction check is not obtained by substituting the
Hamilton--Jacobi slope back into its own algebraic identity.  At six selected
points, the code independently re-solves the same five-equation BVP at
\(\tau-h\) and \(\tau+h\), then forms the centered derivative

\[
\frac{y(\tau+h)-y(\tau-h)}{2h}.
\]

Its largest normalized difference from \(-\operatorname{Im}W_T/
\operatorname{Re}W_T\) is \(1.29\times10^{-6}\).  The largest neighboring
center jump is \(1.98\times10^{-3}\), the largest centered midpoint defect is
\(4.52\times10^{-6}\), and all twelve neighboring roots remain on the
\(\operatorname{Im}T>0,\operatorname{Im}u<0\) sheet.  This supplies a
non-tautological numerical direction and branch-continuity gate in addition
to the exact identity of Section 3.

The positive sampled Jacobi singular values show that no **sampled** second
Dirichlet caustic occurs.  They do not exclude a zero between sampling points,
on another complex sheet, or in an inhomogeneous mode.

## 6. Bounded intersection statement

The Phase-32 declared full-line lapse contour maps under \(T=iN\) to the
imaginary \(T\) axis away from its endpoint bypass.  Its recorded caps have

\[
|T|=r\leq0.1.
\]

The tracked upper and lower arms use \(\operatorname{Re}T\) itself as a
monotonically increasing chart and satisfy

\[
9.788825568\leq\operatorname{Re}T\leq13.
\]

Their lapse bases therefore cannot meet either the imaginary axis or those
caps anywhere on this bounded continuation.  This is stronger than a check
of the displayed points because every continuation solve is performed at a
prescribed positive \(\operatorname{Re}T>T_c\).

It is still not a global intersection computation.  An uncontinued dual arm,
another stationary sheet, a good end, or a joint field--lapse cycle can change
the global relative-homology problem.

## 7. Claim boundary

Supported in the frozen homogeneous reduced model:

- both actual real fixed-boundary sheets are projected into the fold;
- the Airy \(3/2\) seed selects conjugate upper/lower complex sheets;
- the upper constant-phase branch is directed like
  \(-\overline{W_T}\) in the declared reduced metric;
- a robust table continues that branch through \(\operatorname{Re}T=13\);
- no sampled endpoint-Jacobi zero or bounded lapse-base intersection is seen.

Open and not computed:

- the full joint field--lapse metric and gradient flow;
- the Airy connection matrix and oriented determinant-line transport;
- all complex sheets, good ends, infinity, and unsampled Jacobi zeros;
- the complete relative cycles and global \(n_\sigma\);
- inhomogeneous fluctuations, a WDW density, or a physical state.

In particular, the phrase “directed dual continuation” in this phase always
means the **reduced stationary-family** object defined above.

## 8. Reproduction

Direct locked run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py
```

Workbench entry point:

```bash
./ice run phase34_directed_fold_dual_continuation
```

Expected result:

```text
5 exact checks passed
9 numerical checks passed
```

The executable prints one deterministic `PHASE34_RESULT=` JSON payload and
writes no files.

## Primary-source boundaries

- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655)
  supplies the local coalescing-saddle/Airy framework, not this numerical
  branch or its global contour.
- [Witten](https://arxiv.org/abs/1001.2933) supplies the relative-cycle and
  Picard--Lefschetz framework, not the missing original joint cycle here.
- [Halliwell--Louko](https://doi.org/10.1103/PhysRevD.42.3997) documents lapse
  contour sensitivity in minisuperspace, not this fold's determinant line.
- The below-origin prescription is inherited from Phase 32.  Phase 34 does
  not extend its primary-source attribution into a theorem about the present
  unreduced mixed-sign field Gaussian.
