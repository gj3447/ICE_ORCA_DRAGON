# Phase 36 — local Airy/Gauss--Manin fold connection

## Result

The local connection problem left open by Phases 33--35 is now fixed in a
declared oriented Airy contour basis.  The tracked real Phase-25 root is the
decaying Airy saddle.  The standard declared local decay contour
\(\Gamma_0\) through that saddle represents

\[
\boxed{\operatorname{Ai}(z)=-J_U(z)-J_L(z)}.
\]

This local representation does not prove that the uncomputed original
gravitational relative cycle equals \(\Gamma_0\).

Clockwise and counterclockwise continuation use the same local
Gauss--Manin matrix after their outgoing bases are ordered separately, but
their upward-dual images are different:

\[
\boxed{K_{\rm tracked}\longmapsto-K_U\quad({\rm CW})},
\qquad
\boxed{K_{\rm tracked}\longmapsto-K_L\quad({\rm CCW})}.
\]

Both choices were realized by direct prescribed-complex-
\(T\) boundary-value continuations on three shrinking semicircles.  The
upper-
\(T\)/CW path reaches the Phase-34 upper arm; the lower-
\(T\)/CCW path reaches its lower conjugate.  Both pass the same local
endpoint, action-gap, and sampled determinant tests.

Therefore the result has two layers:

\[
\boxed{\text{exact local Airy/Gauss--Manin connection: fixed}},
\]

\[
\boxed{
\text{upper versus lower lateral selection from Phases 32 and 35: not fixed}.
}
\]

This is a concrete local nonselection counterexample, not a failure of the
connected saddle or fold.  It does not compute a full joint BFV cycle, a
global Picard--Lefschetz coefficient, or a quantum state.

## 1. Canonical sign and decay-ray contours

Use the Airy exponent

\[
f(t,z)=\frac{t^3}{3}-zt,
\qquad e^{f(t,z)}.
\]

The physical Phase-34 soft coordinate \(x\) has positive orientation along
the recorded real sheet.  The frozen canonical maps are

\[
u=-\alpha x,
\qquad t=-u.
\]

Thus the recorded \(x>0\) root maps to

\[
u=-\sqrt\zeta,
\qquad t=+\sqrt z,
\qquad
f(+\sqrt z,z)=-\frac23z^{3/2}.
\]

It is the decaying \(\operatorname{Ai}\) saddle.  This sign is also checked by
continuing the actual Phase-25 real branch to
\(T_c-2\times10^{-4}\), where

\[
x_{\rm tracked}=+0.0167743402730
\]

and the endpoint determinant is positive.

The three oriented decay-ray contours are

\[
D_-:\arg t=-\frac\pi3,
\quad
D_+:\arg t=+\frac\pi3,
\quad
D_\pi:\arg t=\pi,
\]

\[
\Gamma_0:D_-\to D_+,
\quad
\Gamma_L:D_+\to D_\pi,
\quad
\Gamma_U:D_\pi\to D_-.
\]

Their oriented chain relation is

\[
\Gamma_0+\Gamma_L+\Gamma_U=0.
\]

With \(\omega=e^{2\pi i/3}\), freeze

\[
J_0=\operatorname{Ai}(z),
\qquad
J_L=\omega\operatorname{Ai}(\omega z),
\qquad
J_U=\omega^2\operatorname{Ai}(\omega^2z).
\]

In arm order \((U,L)\),

\[
\begin{pmatrix}J_U\\J_L\end{pmatrix}
=\frac12
\begin{pmatrix}-1&-i\\-1&i\end{pmatrix}
\begin{pmatrix}\operatorname{Ai}\\\operatorname{Bi}\end{pmatrix},
\]

\[
\begin{pmatrix}\operatorname{Ai}\\\operatorname{Bi}\end{pmatrix}
=
\begin{pmatrix}-1&-1\\i&-i\end{pmatrix}
\begin{pmatrix}J_U\\J_L\end{pmatrix}.
\]

The executable verifies that these matrices are exact inverses.  In
particular, local regularity does not reduce the two-dimensional Airy
solution space to one arm.

## 2. Gauss--Manin cycle and upward-dual maps

For CW continuation, order the bases as

\[
\Gamma_{\rm in}^{\rm CW}=(\Gamma_0,\Gamma_L),
\qquad
\Gamma_{\rm out}^{\rm CW}=(\Gamma_U,\Gamma_L).
\]

Then

\[
\Gamma_{\rm in}^{\rm CW}
=G\Gamma_{\rm out}^{\rm CW},
\qquad
G=
\begin{pmatrix}-1&-1\\0&1\end{pmatrix},
\qquad G^{-1}=G.
\]

For CCW continuation, the frozen orders are instead

\[
\Gamma_{\rm in}^{\rm CCW}=(\Gamma_0,\Gamma_U),
\qquad
\Gamma_{\rm out}^{\rm CCW}=(\Gamma_L,\Gamma_U),
\]

and the same displayed \(G\) relates the two ordered bases.  The common
matrix does **not** mean that the geometrical outgoing arm is the same; its
first outgoing basis vector is \(\Gamma_U\) in the CW chart and
\(\Gamma_L\) in the CCW chart.

Preservation of the cycle--dual pairing requires the upward cycles to obey

\[
K_{\rm in}=G^{-T}K_{\rm out},
\qquad
G^{-T}=
\begin{pmatrix}-1&0\\-1&1\end{pmatrix}.
\]

Consequently the same tracked incoming dual maps to \(-K_U\) in the CW
chart and \(-K_L\) in the CCW chart.  This is the exact algebraic
counterexample to inferring a unique outgoing arm from local fold
regularity.

## 3. Enhanced lateral/Stokes basis

In the frozen enhanced lateral convention,

\[
E_-=\Gamma_L,
\qquad
E_+=-\Gamma_U=\Gamma_0+\Gamma_L.
\]

The corresponding downward and upward Stokes matrices are

\[
S_\downarrow=
\begin{pmatrix}1&0\\1&1\end{pmatrix},
\qquad
S_\uparrow=S_\downarrow^{-T}
=\begin{pmatrix}1&-1\\0&1\end{pmatrix}.
\]

Both have determinant one.  Reversing a crossing uses the relevant inverse.
These are cycle/dual basis changes.  They must not be identified with the
permutation of the two numerical BVP roots described below.

## 4. Determinant half phase and the double-counting guard

Phase 35 fixed the local endpoint-basis convention

\[
d_U\sim-iC\sqrt\tau,
\qquad
d_L\sim+iC\sqrt\tau,
\qquad C>0.
\]

In arm order \((U,L)\), one relative square-root lift and the corresponding
inverse-square-root lift are therefore

\[
L_{\sqrt d}=
\operatorname{diag}
\left(\epsilon_Ue^{-i\pi/4},
      \epsilon_Le^{+i\pi/4}\right),
\]

\[
L_{d^{-1/2}}=
\operatorname{diag}
\left(\epsilon_Ue^{+i\pi/4},
      \epsilon_Le^{-i\pi/4}\right),
\qquad \epsilon_U,\epsilon_L\in\{+1,-1\}.
\]

The endpoint calculation does not determine the two signs.  With one
declared finite-dimensional trivialization, the bare BVP-root lateral ratio
is

\[
iP,
\qquad
P=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
(iP)^2=-I.
\]

This bare root/determinant monodromy is not the cycle matrix \(G\), and it is
not a global Maslov or intersection coefficient.

There is also a mandatory uniformization guard.  For the canonical fold

\[
\Phi(u,\zeta)=\frac{u^3}{3}-\zeta u,
\qquad u_{\rm track}=-\sqrt\zeta,
\]

the soft endpoint factor is

\[
s(\zeta)=-\frac{\Phi''(u_{\rm track})}{2}=\sqrt\zeta.
\]

If

\[
d=s(\zeta)\,\widehat d,
\]

then the separate-saddle factor contains

\[
d^{-1/2}=\widehat d^{-1/2}\zeta^{-1/4}.
\]

The Airy function already replaces the singular
\(\zeta^{-1/4}\) soft-mode asymptotic.  A uniform kernel may therefore
multiply the Airy term by a derived regular hard quotient
\(\widehat d^{-1/2}\), but it must **not** multiply
\(d^{-1/2}\) by the Airy function again.  Phase 36 enforces this exact
no-double-counting rule; it does not yet construct the physical or regulated
\(\widehat d\).

## 5. Direct complex-BVP continuation

The fold is

\[
T_c=9.788625568081242,
\]

with physical soft direction

\[
v_R=(0.996483931960381,-0.0837840876585722).
\]

At each radius

\[
r\in\{2\times10^{-4},10^{-3},5\times10^{-3}\},
\]

the script first solves both real endpoint roots at \(T=T_c-r\).  It then
prescribes

\[
T_{\rm CW}(\theta)=T_c+r e^{i\theta},
\qquad \theta:\pi\to0,
\]

or

\[
T_{\rm CCW}(\theta)=T_c+r e^{i\theta},
\qquad \theta:-\pi\to0,
\]

and solves four real endpoint equations for the complex midpoint
\((a_c,\phi_c)\) at every step.  There are four paths per radius: two
incoming roots times two laterals.  Nine points on each path independently
reintegrate the full variational system and record \(\det B_v\).

Use numerical incoming order

\[
(I_-,I_+)=(x<0,x>0\text{ tracked Ai})
\]

and numerical outgoing order

\[
(O_-,O_+)=(\operatorname{Im}x<0,
            \operatorname{Im}x>0).
\]

The measured root maps are

\[
R_{\rm upper\ T/CW}=P=
\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
R_{\rm lower\ T/CCW}=I.
\]

Thus the tracked \(I_+\) root reaches \(O_-\), the Phase-34 upper
\(U\) arm, through CW continuation and reaches \(O_+\), the lower
\(L\) arm, through CCW continuation.  Again, \(R\) labels analytic BVP
roots; it is not \(G\), \(S\), or an intersection matrix.

## 6. Numerical results

Define the oriented action gap by

\[
\Delta W=W_{I_+}-W_{I_-}
\]

and lift

\[
\zeta=\left(\frac{3\Delta W}{4}\right)^{2/3}
\]

with the logarithm continuously anchored at the positive real incoming
gap.  The observed phase rotations are \(-3\pi/2\) on CW paths and
\(+3\pi/2\) on CCW paths.

The main finite-resolution results are:

| \(r\) | \(\Delta\arg\Delta W\) CW/CCW | \(\Delta\arg d\) CW, \(I_-/I_+\) | \(\Delta\arg d\) CCW, \(I_-/I_+\) | mean \(\zeta/(T_c-T)\), CW |
|---:|---:|---:|---:|---:|
| \(2\times10^{-4}\) | \(-4.7123889804/+4.7123889847\) | \(-1.580898974/-1.560693680\) | \(+1.580898974/+1.560693680\) | \(16.9479105124+4.35801\times10^{-5}i\) |
| \(10^{-3}\) | \(-4.7123889799/+4.7123889807\) | \(-1.593367124/-1.548225530\) | \(+1.593367124/+1.548225530\) | \(16.9479105153+2.17849\times10^{-4}i\) |
| \(5\times10^{-3}\) | \(-4.7123889804/+4.7123889805\) | \(-1.621049573/-1.520543080\) | \(+1.621049573/+1.520543080\) | \(16.9479105167+1.10093\times10^{-3}i\) |

At the smallest radius,

\[
\frac{\zeta}{T_c-T}=
\begin{cases}
16.9478390699,&\theta=\pi,\\
16.9479105081+7.14043\times10^{-5}i,&\theta=\pi/2,\\
16.9479819070+O(10^{-14})i,&\theta=0.
\end{cases}
\]

The maximum deviation from the path mean is
\(8.37\times10^{-5}\), increasing with radius.  These three finite
semicircles are consistent with one locally analytic CFU coordinate and an
approach to a real-positive coefficient near \(16.94791\).  They do not by
themselves prove analyticity or an error-certified zero-radius limit.

The smallest sampled endpoint-Jacobi singular value over all paths is

\[
\sigma_{\min}=0.0573869029855.
\]

The largest sampled determinant phase increment is \(0.20586<\pi\).  The
largest half-BVP root residual is \(4.48\times10^{-15}\), and the largest
independently reintegrated full endpoint residual is
\(4.75\times10^{-11}\).  These are sampled finite-dimensional tests; they do
not exclude a zero between samples or on another sheet.

## 7. What the counterexample decides

The upper and lower tracked endpoints at the smallest radius have soft
coordinates

\[
x_U=-1.3451\times10^{-5}-0.0167611953192\,i,
\]

\[
x_L=-1.3451\times10^{-5}+0.0167611953192\,i.
\]

They are distinct conjugate roots.  Both solve the same fixed-boundary
problem, have nonzero sampled endpoint determinant, and possess the required
opposite action-gap and determinant phase windings.  Local cap regularity,
Airy regularity, and relative endpoint transport therefore leave both
laterals alive.

The Phase-32 lapse bypass is confined to origin caps with \(|T|\leq0.1\),
whereas the fold is at \(T_c\simeq9.7886\).  Its recorded projected crossing
can assign data to the incoming reduced dual, but it does not pass through
this fold chart and cannot locally distinguish \(-K_U\) from \(-K_L\).
Phase 35 transports the relative determinant on the already chosen upper
and lower branches; its unresolved signs \(\epsilon_U,\epsilon_L\) do not
supply the missing original-cycle choice.

Hence the strong inference

\[
\text{Phase 32 origin lateral}
+\text{Phase 35 relative determinant}
\Longrightarrow\text{unique outgoing fold arm}
\]

is contradicted locally.  The following stronger question remains open:

\[
\text{Does one complete regulated original relative cycle intersect only one
of the full upward cycles after all good ends are included?}
\]

That is a global relative-homology calculation, not another local fold fit.

## 8. Claim boundary

Computed:

- the exact oriented three-ray Airy contour relation;
- the exact \((\operatorname{Ai},\operatorname{Bi})\)-to-\((J_U,J_L)\)
  connection;
- the separately ordered CW and CCW Gauss--Manin cycle maps;
- the inverse-transpose upward-dual maps and enhanced lateral Stokes
  matrices;
- the relative endpoint-determinant half-phase layer, with its unresolved
  signs explicit;
- the exact soft-mode double-counting prohibition;
- twelve finite-radius prescribed-complex-\(T\) BVP paths and their root
  permutations, action-gap winding, CFU consistency, and sampled determinant
  phases.

Open and not computed:

- selection of CW/upper rather than CCW/lower by one declared complete
  original relative cycle;
- the regular hard determinant quotient \(\widehat d\) needed for an
  absolute uniform kernel;
- absolute determinant/Maslov signs, unsampled zeros, other sheets,
  inhomogeneous modes, and all good ends;
- a full joint field--lapse flow or regulated BFV/SUGRA superdeterminant;
- complete relative cycles and a global \(n_\sigma\);
- a WDW density, physical quantum state, initial-value peak, or SUSY scale.

## 9. Reproduction

Direct locked-environment run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase36_airy_gauss_manin_connection.py
```

Workbench entry point:

```bash
./ice run phase36_airy_gauss_manin_connection
```

The final payload contains

```json
{"exact_checks": 12, "numerical_checks": 9}
```

The executable prints one deterministic `PHASE36_RESULT=` JSON payload,
writes no files, and is silent when imported.

## Primary-source boundary

- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655)
  supplies the coalescing-saddle uniformization framework, not the original
  gravitational cycle or the numerical coefficient reported here.
- [Witten](https://arxiv.org/abs/1001.2933) supplies the relative-cycle,
  intersection, and Picard--Lefschetz framework, not the missing global
  coefficient for this model.
- [Halliwell--Louko](https://doi.org/10.1103/PhysRevD.42.3997) supplies the
  minisuperspace contour-sensitivity context, not this fold connection.
- [Banihashemi--Jacobson](https://doi.org/10.1103/PhysRevD.111.066014)
  motivates the separately declared below-origin full lapse prescription.
  It does not derive a unique upper/lower continuation at this distant fold.
