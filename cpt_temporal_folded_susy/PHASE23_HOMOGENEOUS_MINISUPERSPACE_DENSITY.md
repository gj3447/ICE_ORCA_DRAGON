# Phase 23 — homogeneous minisuperspace rigging-map density control

## Outcome

This phase asks the next question after the finite-mode density of Phase 22:
can a Wheeler--DeWitt-type constraint be turned into a positive two-sheet
density without treating the formal symbol \(\delta(\hat C)\) as an ordinary
trace-class projector?

In the bounded model studied here, the answer has two parts:

\[
\boxed{
\text{full-lapse rigging}
+\text{ an explicit clock/frequency choice}
+\text{ a supplied trace-class bridge }B_L
\Longrightarrow \rho_+\geq0,\quad \operatorname{Tr}\rho_+=1 .
}
\tag{P230}
\]

But

\[
\boxed{
\text{the constraint, CPT-like reality, and zero signed current alone}
\not\Longrightarrow
\text{a unique seam density.}
}
\tag{P231}
\]

The calculation therefore constructs a genuine positive, normalized density
on a chosen regulated physical Hilbert space.  It does **not** derive that
density from the closed Starobinsky cap, CPT/Pin, or local supergravity.  The
preparation length \(L\), the compact spectral regulator, the positive-frequency
orientation, and the toy anti-linear pairing remain supplied inputs.

The continuous Gaussian seed calculation in Section 1 and the compact
spectral density in Section 4 are two separate calibrations.  This phase does
not derive the compact bridge or its weights by evolving that seed.

Executable:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py
```

The executable records 32 exact checks and 4 numerical checks.  No fit is used.

## 1. Constraint and full-lapse rigging map

Use a single hyperbolic constraint

\[
\hat C=p_T^2-\hat h .
\tag{P232}
\]

For a spectral value \(c\) of \(\hat C\), the Abel-regulated full real lapse
average is

\[
P_\epsilon(c)
=\frac{1}{2\pi}\int_{-\infty}^{\infty}dN\,
e^{iNc-\epsilon |N|}
=\frac{\epsilon}{\pi(c^2+\epsilon^2)}
\xrightarrow[\epsilon\to0^+]{}\delta(c).
\tag{P233}
\]

It has unit spectral integral.  A Gaussian lapse regulator gives the second
delta sequence

\[
P^G_\epsilon(c)
=\frac{e^{-c^2/\epsilon^2}}{\sqrt\pi\,\epsilon}.
\tag{P234}
\]

These are distributional rigging kernels, not bounded projectors on the
kinematical Hilbert space.  Indeed,

\[
P^G_\epsilon(0)=\frac{1}{\sqrt\pi\,\epsilon}\longrightarrow\infty.
\tag{P235}
\]

For a normalized factorized Gaussian seed with constraint-space width
\(\lambda\), the regulated rigging norm is calculated exactly:

\[
\langle f,P^G_\epsilon f\rangle_{\mathrm{kin}}
=\frac{1}{\sqrt\pi\sqrt{\lambda^2+\epsilon^2}}.
\tag{P236}
\]

After dividing by the square root of this norm, the on-shell factor reduces
to the normalized chosen physical profile.  This explicitly implements the route from a
kinematical seed to shell data; it does not merely start with an already
on-shell wavefunction.

The lapse range matters.  The positive half-line gives

\[
\int_0^\infty dN\,e^{iNc-\epsilon N}
=\frac{1}{\epsilon-ic},
\tag{P237}
\]

which is a Green-function resolvent, not the even full-lapse delta kernel.
Likewise, a naive Euclidean factor \(e^{-s\hat C}\) diverges on the negative
spectrum of a hyperbolic constraint.  The group-averaging lapse \(N\) must
therefore not be identified with the state-preparation length \(L\) introduced
below.

This use of group averaging follows the refined-algebraic-quantization
framework, while the distinction between induced and Klein--Gordon products
is the one emphasized for reparametrization-invariant systems by
[Marolf](https://arxiv.org/abs/gr-qc/9508015) and
[Hartle--Marolf](https://arxiv.org/abs/gr-qc/9703021).  Those references frame
the construction; they do not derive the particular regulator used here.

## 2. Compact positive-frequency control

To make the trace question unambiguous, regulate the homogeneous coordinate by

\[
q\in(0,\pi),\qquad
u_n(q)=\sqrt{\frac2\pi}\sin(nq),\qquad n\geq1,
\tag{P238}
\]

and choose

\[
\hat h=-\partial_q^2+\mu^2,qquad
E_n=\sqrt{n^2+\mu^2},\qquad \mu>0.
\tag{P239}
\]

The constraint roots are \(p_T=\pm E_n\), and

\[
\delta(p_T^2-E_n^2)
=\frac{\delta(p_T-E_n)+\delta(p_T+E_n)}{2E_n}.
\tag{P240}
\]

For the explicit gauge \(T=\tau\), the Faddeev--Popov factor
\(|\{T-\tau,C\}|=2E_n\) cancels the simple-root Jacobian on either chosen
branch.  The normalized frequency modes are

\[
u_{n,+}(T,q)=\frac{u_n(q)e^{-iE_nT}}{\sqrt{2E_n}},
\qquad
u_{n,-}(T,q)=\frac{u_n(q)e^{+iE_nT}}{\sqrt{2E_n}}.
\tag{P241}
\]

The integrated Klein--Gordon current is \(+1\) for \(u_{n,+}\) and \(-1\)
for \(u_{n,-}\).  Group averaging contains both roots.  Positivity therefore
requires either the induced product or an explicit clock and frequency
orientation; it is not supplied by the quadratic constraint alone.

In particular, equal \(+\) and \(-\) branch amplitudes can have zero signed
current while having nonzero induced norm.  Hence

\[
J_T=0
\quad\not\Longrightarrow\quad
\Psi=0
\quad\text{and}\quad
J_T=0
\quad\not\Longrightarrow\quad
\text{a unique state}.
\tag{P242}
\]

## 3. Local current is not a probability density

Even after selecting positive frequency, the local Klein--Gordon current need
not be pointwise positive.  The exact two-mode witness

\[
\Psi(T,q)=
\frac{\sin q\,e^{-iT}+\sin(2q)e^{-2iT}}{\sqrt{3\pi}}
\tag{P243}
\]

satisfies

\[
\partial_Tj_T-\partial_qj_q=0,
\qquad
\int_0^\pi dq\,j_T=1.
\tag{P244}
\]

Nevertheless, at \(T=0\) and \(\cos q=-3/8\),

\[
\boxed{j_T=-\frac{55}{768\pi}<0.}
\tag{P245}
\]

The positive object in this control is the integrated physical inner product
or the density operator constructed on that Hilbert space, not the local
current interpreted point by point as a Born density.

## 4. A trace-class two-sheet density after the constraint

On the selected positive-frequency physical space, define

\[
A=\sqrt{\hat h},\qquad B_L=e^{-LA},\qquad L>0.
\tag{P246}
\]

This is a relational bridge input, separate from lapse group averaging.  Take
two independently constrained copies, called \(L\) and \(R\), and equip each
copy with its selected outward-positive induced product.  The labels below are
sheet labels, not the positive/negative Klein--Gordon frequency labels of
Section 2.  Since
\(E_n>n\),

\[
Z_L=\operatorname{Tr}e^{-2LA}
=\sum_{n=1}^{\infty}e^{-2LE_n}
<\sum_{n=1}^{\infty}e^{-2Ln}
=\frac1{e^{2L}-1}.
\tag{P247}
\]

Thus \(B_L\) is Hilbert--Schmidt and the paired state

\[
|\Sigma_L\rangle
=\frac1{\sqrt{Z_L}}
\sum_{n=1}^{\infty}e^{-LE_n}
|n\rangle_L\otimes\Theta_{\rm toy}|n\rangle_R
\tag{P248}
\]

is normalizable.  Its one-sheet reduction is

\[
\boxed{
\rho_+=\frac{e^{-2LA}}{Z_L},
\qquad
\rho_+\geq0,
\qquad
\operatorname{Tr}\rho_+=1.
}
\tag{P249}
\]

The executable checks the normalized rank-one purification, Hermiticity,
idempotence, partial trace, positive eigenweights, and
\([A,\rho_+]=0\) in a three-level exact truncation.  For \(\mu=L=1\), the
infinite spectral sum converges numerically to

\[
Z_L=0.072625937359366,
\tag{P250}
\]

with a recorded cutoff increment below \(1.9\times10^{-15}\).

The relative weights are not predicted:

\[
\frac{p_2}{p_1}=e^{-2L(E_2-E_1)},
\qquad
\partial_L\log\frac{p_2}{p_1}=-2(E_2-E_1)<0.
\tag{P251}
\]

Different supplied \(L\) therefore give different normalized states.  The
operator \(\Theta_{\rm toy}\) is only an anti-linear spectral pairing.  It is
not a four-dimensional Clifford/Pin lift and does not prove CPT invariance of
the gravitational path integral.

## 5. The homogeneous zero root remains singular

The simple-root construction fails when \(E=0\).  The Abel regulator becomes

\[
P_\epsilon(p_T^2)
=\frac{\epsilon}{\pi(p_T^4+\epsilon^2)},
\tag{P252}
\]

and its integral is

\[
\int_{-\infty}^{\infty}dp_T\,P_\epsilon(p_T^2)
=\frac1{\sqrt{2\epsilon}}
\longrightarrow\infty.
\tag{P253}
\]

At the same point the clock determinant is \(2E=0\).  Replacing the constraint
by \(C_{\rm lin}=p_T-A\) makes the root regular, but preselects a time
orientation and is not equivalent to the original quadratic, branch-symmetric
constraint.

A cap Hessian zero mode is a separate issue.  It can be removed from a
determinant only after exhibiting an actual saddle family
\(z=\partial_\lambda q_{\rm cl}\), its primed determinant, the
collective-coordinate Jacobian, and the measure over \(\lambda\).  The
previously free Starobinsky value \(\phi_0\) is not known to be a gauge mode and
must not be divided out by assertion.

Compactness also matters.  For a massless box of radius \(R\),

\[
Z_R=\frac1{e^{2L/R}-1}
\sim\frac{R}{2L},
\qquad R\to\infty.
\tag{P254}
\]

The trace-class property is therefore not regulator-independent in this
control.

## 6. What this says about the full seam state

The calculation separates four logically different operations:

1. The constraint and full lapse range define a distributional rigging map in
   the continuous spectral calibration.
2. A clock/frequency choice or an induced product supplies a positive physical
   inner product.
3. In the independent compact calibration, a separate bridge \(B_L\) supplies
   relative spectral weights.
4. Only then does normalization produce a density operator.

The first operation does not determine the third.  CPT-like branch pairing
restricts how states are paired but does not fix \(L\) or the coefficients.
Consequently this phase does not select

\[
n_*,\qquad \phi_0,\qquad a_0,\qquad F_{\rm eff},
\qquad N_{\rm e-fold},\qquad \Delta n_k.
\]

For the actual symmetric closed-FRW neck, \(p_a=p_\phi=0\).  Therefore
\(a\) or \(\phi\) used directly as an intrinsic clock has a vanishing
Faddeev--Popov determinant at the seam.  The next calculation must use an
extrinsic or two-patch clock, or avoid deparametrization and perform refined
algebraic quantization directly.

The decisive next gate is:

\[
\boxed{
\begin{gathered}
\text{actual closed Starobinsky complex-cap constraint and contour}\\
+\text{factor ordering and physical current}\\
+\text{primed determinant and collective-coordinate measure}
\end{gathered}
\Longrightarrow
\text{a cap-derived }B\text{ and regulator-independent density?}
}
\tag{P255}
\]

Only if that gate succeeds should the calculation be extended to the coupled
gravitino--Goldstino--ghost boundary operator, local-SUGRA constraints, and
BRST cohomology.

## 7. Frozen scope

Established in this phase:

- exact full-real-lapse Abel and Gaussian rigging kernels;
- an explicit kinematical-seed to normalized-shell calculation;
- the distinction between full-lapse rigging and half-lapse resolvents;
- simple-root shell Jacobian and clock-gauge cancellation;
- positive integrated norm after an explicit branch/clock choice;
- a conserved current with an exact negative local-density witness;
- a positive trace-class two-sheet density for supplied \(L>0\) at a compact
  regulator;
- quadratic zero-root and massless decompactification obstructions.

Not established:

- the exact closed \(k=+1\) Starobinsky/Cecotti Wheeler--DeWitt operator;
- a Picard--Lefschetz contour or a cap-derived value of \(L\);
- factor-ordering, clock-patch, or regulator independence;
- a physical Born measure over universe initial data;
- a four-dimensional Pin lift;
- three-form, membrane, gravitino, Goldstino, ghost, or BRST completion;
- a selected flux, inflaton initial value, curvature radius, or persistent
  supersymmetry-breaking scale.

The bounded conclusion is therefore

\[
\boxed{
\begin{gathered}
\text{a positive trace-class density can be supplied after explicit}\\
\text{regulator, branch, and }B_L\text{ choices;}\\
\text{the cosmological seam density remains open.}
\end{gathered}
}
\tag{P256}
\]
