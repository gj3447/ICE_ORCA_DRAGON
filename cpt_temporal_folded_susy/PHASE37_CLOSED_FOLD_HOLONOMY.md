# Phase 37 — closed simple-fold holonomy and the supercharge gate

## Result

Phase 37 replaces the two separately based open laterals of Phase 36 by an
actual closed continuation around the same simple fold.  Both numerical BVP
roots are transported continuously around one counterclockwise loop in the
complex proper-time plane and compared in one fixed fiber at the original
basepoint.

On all three recorded finite radii,

\[
r\in\{2\times10^{-4},10^{-3},5\times10^{-3}\},
\]

the roots exchange:

\[
R_\gamma=P=
\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad P^2=I.
\]

When the sampled reduced endpoint determinant is lifted continuously rather
than reset to a principal square root at every point, the associated inverse
square-root transport is, up to a constant basepoint rephasing,

\[
L_\gamma\simeq
\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Its recorded conjugacy invariants are

\[
\boxed{
\operatorname{tr}L_\gamma=0,
\quad \det L_\gamma=1,
\quad L_\gamma^2=-I,
\quad L_\gamma^4=I.
}
\]

Here "continuously" means the minimal-jump lift of the recorded nonzero
samples, conditional on there being no unresolved extra winding between
samples.  It is not a zero-free theorem for the continuum path.

Thus two turns return the BVP root to its original sheet but give the sampled
reduced inverse square root a central sign:

\[
\boxed{\text{root return }=+1,\qquad
       \text{reduced half-form return }=-1.}
\]

This is the first calculation in the programme that transports one local
section around a closed loop and tests its return in the same basepoint
fiber.  Consequently the displayed conjugacy class is stronger than a raw
comparison of two independently trivialized open paths.

The result does **not** turn the fold into a physical supercharge.  The same
exact executable proves that bare root-swap holonomy leaves the Phase-17
parity-controlled basis equivalence intact.  It also keeps root sheets, Airy
solutions, relative cycles, Stokes data, bosonic half-forms, fermion
Pfaffians, and Pin lifts as different objects.

The direction verdict is therefore precise:

\[
\boxed{
\text{global-obstruction/holonomy language is productive for the fold,}
}
\]

\[
\boxed{
\text{but root holonomy alone is not yet physical temporal SUSY.}
}
\]

## 1. What is closed in this calculation

Let

\[
z=T_c-T,
\qquad u^2=z,
\]

with the numerical fold at

\[
T_c=9.788625568081242.
\]

The loop starts at the real pre-fold basepoint $T_*=T_c-r$, winds once
counterclockwise around $T_c$, and returns to exactly the same $T_*$.
Both roots are solved at every step using the previous root as the next
initial guess.  They are not reordered by their instantaneous real part.

For the canonical local cover,

\[
u_+(\theta)=+\sqrt r\,e^{i\theta/2},
\qquad
u_-(\theta)=-\sqrt r\,e^{i\theta/2}.
\]

Hence one base loop exchanges the two roots, and following both lifted paths
in succession closes the path on the root cover.

This closure matters.  In Phase 36 the upper and lower continuations used
different companion contour bases, so their first duals could not be treated
as two images of one physical incoming dual.  Phase 37 does not identify a
BVP root with that missing dual.  It instead asks a narrower well-posed
question: does one continuously tracked **root/determinant section** return
to itself after its lifted closed path?

## 2. Numerical root transport

At each radius the two start roots are ordered by the oriented soft
coordinate $x$:

\[
(I_-,I_+)=(x<0,x>0).
\]

One enclosing loop gives

\[
I_-\longmapsto I_+,
\qquad
I_+\longmapsto I_-.
\]

The largest endpoint swap error among all six paths is

\[
2.72\times10^{-13}.
\]

The largest half-BVP residual is below

\[
4.8\times10^{-15},
\]

and the largest independently reintegrated sampled full-endpoint residual is

\[
4.79\times10^{-11}.
\]

The maximum continuation step divided by the minimum instantaneous root
separation is $0.0329$.  This is a numerical continuity guard against a
solver jump from one root to the other.

The smallest-radius positive-root path was also repeated with 25 rather than
49 points.  Its final center and determinant phase agree with the finer path
to much better than the declared thresholds.  Both runs use the same thirteen
determinant angles, so this refines the BVP continuation mesh, not the
determinant sampling.  It is not a convergence theorem.

Finally, the positive root was followed for one uninterrupted $4\pi$
continuation with 97 BVP points.  No solver or half-form reference is reset
at the intermediate basepoint crossing.  It returns to the starting root
with

\[
\Delta\arg d=2\pi,
\qquad
g(4\pi)/g(0)=-0.999999999993,
\]

and agrees with the return obtained by stitching the two independently
solved one-turn root paths.  A secant predictor is used only to remain inside
the same ill-conditioned nonlinear-solver basin; the BVP residual remains
below $3.3\times10^{-15}$.

## 3. Continuous reduced determinant lift

For every sampled stationary solution, the code recomputes the reduced
endpoint Jacobi block

\[
B_v=\frac{\partial(q_f)}{\partial(v_i)}
\]

by an independent full flow and records

\[
d=\det B_v.
\]

Thirteen determinant samples are taken on each enclosing path.  Across all
six paths,

\[
\min \sigma_{\min}(B_v)=0.0573869,
\]

and the largest adjacent determinant-phase increment is

\[
0.307762<\pi.
\]

The minimal-jump phase is therefore unwrapped on the sampled mesh,
conditional on no intersample alias winding.  For each starting sheet $s$,
the transported half-form is

\[
g_s(\theta)
=\exp\!\left[-\frac12
 \bigl(\log|d_s(\theta)|+i\,\widetilde{\arg}d_s(\theta)\bigr)
 \right].
\]

At the endpoint it is compared with the fixed reference half-form of the
destination root at the original basepoint.  A constant change of those two
reference phases conjugates $L_\gamma$; it cannot change its trace,
determinant, characteristic polynomial, or central square.
The recorded reference convention uses the principal argument in
$(-\pi,\pi]$ once at each basepoint root; it is never reset along a path.

At the smallest radius the numerical matrix is approximately

\[
L_\gamma=
\begin{pmatrix}
0 & 0.999999999993\\
-0.999999999994 & 0
\end{pmatrix},
\]

with

\[
\lVert L_\gamma^2+I\rVert=1.83\times10^{-11}.
\]

The same check passes at the other two radii.  The worst recorded fourth
power error is

\[
\lVert L_\gamma^4-I\rVert=3.67\times10^{-11}.
\]

## 4. Where the central sign comes from

Along the two lifted root paths in succession, the recorded phases obey

\[
\Delta\arg d=2\pi,
\qquad
\Delta\arg x=2\pi,
\qquad
\Delta\arg(d/x)=0
\]

to approximately $10^{-14}$ on every radius.  Hence the sampled local data
are consistent with

\[
d=x\,\widehat d,
\]

where the sampled hard quotient $\widehat d=d/x$ has no net phase winding
on the lifted return path.  The inverse square root therefore acquires

\[
\exp\!\left(-\frac{i}{2}\Delta\arg d\right)=-1.
\]

This does not prove that $\widehat d$ is analytic and zero-free throughout
the enclosed disk.  The calculation excludes zeros only at the sampled
points and only for this reduced homogeneous block.  Zeros or aliased extra
winding between samples, as well as zeros on other solution sheets or in
omitted inhomogeneous, fermionic, lapse, and ghost modes, remain open.

## 5. Winding-zero and mutation controls

### 5.1 Nonenclosing loop

A second numerical loop is centered at

\[
T_c-8\times10^{-4}
\]

with radius $2\times10^{-4}$.  It does not enclose the fold.  The tracked
positive root returns to itself, its determinant phase changes by only

\[
1.57\times10^{-15},
\]

and its inverse-square-root transport differs from $+1$ by approximately

\[
1.6\times10^{-12}.
\]

Thus the recorded order-four result is tied to enclosing the fold, not to
arbitrary complex continuation.

### 5.2 Principal-root reset mutant

If a principal square root is chosen afresh at every point, only the root
permutation remains:

\[
P^2=I.
\]

That mutation deletes the continuous lift and misses

\[
L_\gamma^2=-I.
\]

The exact audit rejects it.

### 5.3 Reverse and rephasing controls

For the reversed loop,

\[
L_{\gamma^{-1}}=L_\gamma^{-1},
\qquad
L_{\gamma^{-1}}L_\gamma=I.
\]

For an arbitrary constant diagonal rephasing $B$,

\[
L_\gamma\longmapsto BL_\gamma B^{-1}
\]

leaves every recorded conjugacy invariant unchanged.  The raw off-diagonal
phase is therefore not the observable content.

## 6. Typed matrices: equal algebra is not equal physics

The exact layer records the following matrices in distinct spaces.

| Typed object | Matrix property | Meaning |
|---|---|---|
| root-sheet $P$ | $\operatorname{tr}=0,\det=-1,P^2=I$ | exchanges the two local BVP roots |
| Airy solution | $I$ | $\operatorname{Ai}$ and $\operatorname{Bi}$ are single-valued at the ordinary point $z=0$ |
| Phase-36 Gauss--Manin $G$ | $\operatorname{tr}=0,\det=-1,G^2=I$ | changes a declared relative-cycle basis |
| Phase-36 Stokes $S_\downarrow$ | unipotent, $(\lambda-1)^2$ | changes a lateral contour basis |
| reduced half-form $L$ | $\operatorname{tr}=0,\det=1,L^2=-I$ | transports the sampled $d^{-1/2}$ section |

Indeed,

\[
G=SPS^{-1}
\]

for an exact invertible $S$.  This is a useful warning: even complete
conjugacy invariants do not identify two maps that act on different physical
spaces.  Root monodromy is not thereby a Gauss--Manin cycle map, and neither
is automatically a quantum symmetry generator.

The full Airy kernel may remain single-valued after its saddle pieces,
Stokes jumps, and analytic coefficients are recombined.  The separate-saddle
half-form sign must not be copied directly into a physical wavefunction.

## 7. What this says about the Phase-17 supercharge idea

Phase 17 found an exact parity-controlled unitary $W$ relating the local
and sheet-exchange matrices,

\[
WQ_{\rm local}W^\dagger=Q_X.
\]

Phase 37 checks that the bare root swap $P$ commutes with this $W$.
Therefore

\[
\boxed{
\text{root-swap monodromy alone does not make }Q_X
\text{ physically distinct.}
}
\]

There are two possible ways forward, and they require new input:

1. an independently physical sheet-localized source or localization net
   that $W$ fails to preserve; or
2. distinct derived bosonic and fermionic holonomies whose global
   intertwiner equation restricts the allowed charge.

For the second possibility, Phase 37 evaluates only the conditional finite
witness

\[
H_B=P,
\qquad H_F=\eta P,
\qquad H_FQ=QH_B,
\]

for $\eta\in\{1,-1,i,-i\}$.  The result is

| $\eta$ | declared $Q_X=P$ compatible? | $\dim\ker$ on $\mathrm{span}\{I,P\}$ | all $2\times2$ intertwiner dimension |
|---:|:---:|---:|---:|
| $+1$ | yes | 2 | 2 |
| $-1$ | no | 0 | 2 |
| $+i$ | no | 0 | 0 |
| $-i$ | no | 0 | 0 |

The $\eta=-1$ row is an important self-application check.  The specific
$Q_X=P$ fails, yet other exact sheet intertwiners survive.  Failure of one
candidate is not a total no-go.  Conversely, a nonzero toy intertwiner does
not establish a conserved, fermion-odd Lorentz spinor or a local-SUGRA
constraint.

No physical $H_F$ is derived here.  The displayed dimensions count only
complex matrices in a declared finite sheet-map space; they are not numbers
of preserved supercharges.

## 8. Why this is not yet a Pin or Pfaffian result

The computed object is the inverse square root of a reduced bosonic endpoint
Jacobi determinant.  A physical one-loop line would schematically include

\[
\mathcal L_{\rm 1loop}
=
[\det{}'\mathcal O_B]^{-1/2}
\otimes\operatorname{Pf}(\mathcal D_F)
\otimes\det\mathcal M_{\rm ghost}
\otimes\cdots.
\]

The fermion Pfaffian sign cannot be reconstructed from its determinant: the
exact audit exhibits two antisymmetric matrices with identical determinant
and opposite Pfaffian.  It also exhibits a nonzero reduced block embedded in
a singular full operator.  These controls forbid the inferences

\[
\text{reduced }d\neq0
\Longrightarrow
\text{full BFV nondegeneracy}
\]

and

\[
\text{bosonic }L^2=-I
\Longrightarrow
\text{fermionic Pin holonomy}.
\]

A spacetime Pin statement still requires the Clifford reflection lift,
its square and cocycle, the fermionic Pfaffian line and spectral flow, the
ghost sector, a common domain, anomaly cancellation, and the BFV/BV quantum
master equation.

## 9. Philosophical interpretation

The useful idea survives in a narrower and more rigorous form:

> A sheet is not made physical by its name.  What can become invariant is
> the obstruction encountered when one tries to choose the same local
> section consistently around a closed path.

At every point on the loop one may choose a perfectly ordinary local basis.
Nothing locally forbids diagonalization.  The nontrivial content appears
only on return: the continuously transported section cannot be identified
with its initial one without the recorded exchange and central phase.

That is what topology contributes here: not a new local force, but a failure
of global trivialization.

The recursive lesson is equally important.  Apply the same criterion to the
proposed interpretation itself:

- if root labels are conventional, keep only conjugacy invariants;
- if the half-form is bosonic and reduced, do not call it a fermion Pin line;
- if a monodromy acts on roots, do not silently move it to the cycle space;
- if a matrix intertwines two toy fibers, do not call it a conserved
  spacetime supercharge;
- if the full Airy function is single-valued, do not assign a separate-saddle
  sign directly to the physical amplitude.

The calculation therefore validates the **method** of looking for global
obstructions while rejecting the premature identity

\[
\text{root-sheet holonomy}=\text{temporal SUSY generator}.
\]

## 10. Claim boundary

Computed:

- exact typed root, Airy-solution, cycle, Stokes, and reduced-half-form
  matrices and their conjugacy invariants;
- exact reverse-loop, rephasing, principal-reset, Pfaffian-sign, and
  reduced-versus-full mutation controls;
- exact conditional sheet-intertwiner dimensions for four declared
  boson/fermion phase relations;
- six same-basepoint enclosing BVP paths on three finite radii;
- one coarse/fine BVP-mesh comparison, one uninterrupted two-turn return,
  and one nonenclosing numerical control;
- sampled determinant, soft-coordinate, and hard-quotient phase lifts.

Open and not computed:

- a theorem excluding zeros or aliased winding between determinant samples,
  on other sheets, or for omitted modes;
- the original lapse-field relative cycle, all good ends, and global signed
  intersection coefficients;
- the regular hard determinant and complete
  $\operatorname{Ai}/\operatorname{Ai}'$ uniform-kernel coefficients;
- a spacetime Pin lift, fermion Pfaffian phase, spectral flow, or anomaly
  cancellation;
- a full joint field--lapse BFV/SUGRA operator, physical cohomology, quantum
  master equation, or WDW state;
- a conserved spinorial supercharge, a persistent SUSY-breaking order
  parameter, boson/fermion pole splitting, or a SUSY scale.

## 11. Next calculation

The next gate is not another denser local loop.  It is to specify one
regulated original lapse-field relative cycle, transport it from the origin
prescription through the fold, enumerate the relevant upward cycles and good
ends, and calculate the signed global intersections and hard CFU
coefficients.  Only after a physical saddle combination is fixed should its
full boson--fermion--ghost determinant/Pfaffian line be lifted and the global
supergravity intertwiner or anomaly tested.

## 12. Reproduction

Direct locked-environment run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase37_closed_fold_holonomy.py
```

Workbench entry point:

```bash
./ice run phase37_closed_fold_holonomy
```

The final payload contains

```json
{"exact_checks": 18, "numerical_checks": 8}
```

The executable prints one deterministic `PHASE37_RESULT=` JSON payload,
writes no files, and is silent when imported.

## Primary-source boundary

- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655)
  supplies the coalescing-saddle/Airy framework, not the numerical closed
  BVP paths or their reduced determinant lift.
- [Witten](https://arxiv.org/abs/1001.2933) supplies the relative-cycle and
  Picard--Lefschetz framework, not the missing original gravitational cycle
  or global intersection coefficients.
- [Witten](https://arxiv.org/abs/1508.04715) supplies fermion
  Pfaffian/reflection-anomaly requirements, not a Pin or Pfaffian lift of the
  present reduced bosonic determinant.
- [Freed--Hopkins](https://arxiv.org/abs/1604.06527) supplies the reflection
  positivity and invertible-phase framework, not a physical fermionic
  holonomy or supercharge in this model.
