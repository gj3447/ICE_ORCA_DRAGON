# Phase 29 — zero-lapse uniform kernel and BFV measure control

## Outcome

The Phase-27 zero-lapse pole has now been separated into its pointwise and
operator meanings.  At the frozen homogeneous boundary, the leading
two-coordinate kernel has the form

\[
K_N(\Delta q)
\sim
\frac{1}{N}
\exp\left[
\frac{i}{2N}\Delta q^TM\Delta q-iN\mathcal U_0
\right].
\]

At $\Delta q=0$ this diverges as $1/N$, but for real lapse its
identity-normalized quadratic distribution, in the local flat endpoint measure
used in this frozen control, obeys

\[
\boxed{K_{N\to0}(q_+,q_-)=\delta^{(2)}_{\rm flat}(q_+-q_-)}.
\]

The pole is therefore the short-time normalization of the identity kernel,
not by itself a removable infinity or a probability divergence.

This closes only the leading frozen pointwise-versus-distributional question.
It does not derive the physical Wheeler--DeWitt endpoint measure, its factor
ordering, an all-orders uniform kernel, or a global lapse contour.

For an open interval with fixed endpoint configurations, proper-time gauge
leaves the lapse modulus with a $T$-independent measure in the declared
fixed-$s$ reduced BFV normalization.  The reduced Dirichlet ghost factor is a
constant after the coordinate and ghost Jacobians are included.  It does
**not** cancel the $1/N$ identity-kernel scaling.

Trying to cancel the pole by inserting an extra factor of $N$ changes the
physical object:

\[
-\frac{i}{H-i0}
\longrightarrow
-\frac{1}{(H-i0)^2},
\]

and on the full line

\[
2\pi\delta(H)
\longrightarrow
2\pi i\delta'(H).
\]

Thus a hand-chosen endpoint power is not a renormalization; it changes the
Green function or rigging distribution.

One further obstruction is exact.  The homogeneous kinetic form has one
negative and one positive eigenvalue.  Either imaginary-lapse sign damps one
direction and amplifies the other.  A conformal-field contour must therefore
be specified together with the lapse contour before a complex endpoint
parametrix or global thimble coefficient can be defined.

## 1. Frozen short-time metric

As in Phases 24--28, reduced units are

\[
M_{\rm P}=M=1.
\]

At

\[
a_0=3.5668031935672753,
\qquad
\phi_0=1.0185809464006637,
\]

the quadratic kinetic matrix in the Phase-27 normalization is

\[
M=2\pi^2
\begin{pmatrix}
-6a_0&0\\
0&a_0^3
\end{pmatrix}
=
\begin{pmatrix}
-422.435237965&0\\
0&895.709502254
\end{pmatrix}.
\]

The full potential coefficient in the kernel exponent is

\[
\mathcal U_0
=2\pi^2\left[-3a_0+a_0^3V(\phi_0)\right]
=2.98719256735.
\]

The leading Lorentzian short-time parametrix is

\[
K_N^{(0)}(\Delta q)
=
\frac{[\det_{\mathcal C}M]^{1/2}}{2\pi iN}
\exp\left[
\frac{i}{2N}\Delta q^TM\Delta q-iN\mathcal U_0
\right],
\]

On real $N$, the square-root branch $\det_{\mathcal C}^{1/2}$ is fixed here by
the requirement $K_{N\to0}=+\delta^{(2)}_{\rm flat}$ under the declared local
flat $d a\,d\phi$ endpoint measure.  A different physical WDW measure would
carry the corresponding density factor; that measure and its factor ordering
are not derived here.  Continuation to imaginary $N$, including the negative
kinetic/conformal contour and phase, also remains unfixed.  The raw Van Vleck
and normalized magnitudes are

\[
|\det D|^{1/2}
=\frac{615.1253992}{|N|}+O(|N|),
\]

\[
|K_N^{(0)}(0)|
=\frac{97.9002479}{|N|}+O(|N|).
\]

The difference is the usual two-dimensional $(2\pi)^{-1}$ kernel
normalization.

## 2. Distributional identity limit

For one kinetic eigenvalue $m$, pair the normalized Fresnel kernel with a
Gaussian test function $e^{-\alpha x^2/2}$.  Analytic continuation from
$N=0$ gives

\[
\int dx\,K_{m,N}(x)e^{-\alpha x^2/2}
=
\left(1+\frac{i\alpha N}{m}\right)^{-1/2}.
\]

For the two opposite-sign eigenvalues,

\[
\langle K_N,f_{\alpha_g,\alpha_s}\rangle
=
\left(1+\frac{i\alpha_gN}{m_g}\right)^{-1/2}
\left(1+\frac{i\alpha_sN}{m_s}\right)^{-1/2}
\longrightarrow1.
\]

The executable verifies monotone convergence on five decreasing lapse values.
More generally, in momentum space the real-lapse multiplier satisfies

\[
e^{-iNh(p)}\longrightarrow1,
\qquad
|e^{-iNh(p)}|=1.
\]

Dominated convergence therefore extends the local-flat-measure identity limit
to Schwartz test functions for this frozen quadratic real-lapse control.  At
the same time, the diagonal value grows exactly as $1/N$.

This shows why the order of operations matters:

\[
\int_0^\epsilon\frac{dN}{N}=\infty
\qquad\text{at fixed }\Delta q=0,
\]

whereas after pairing the normalized $d=2$ kernel with its endpoint
coordinates,

\[
\int_0^\epsilon dN\,\langle K_N,f\rangle
=\epsilon f(0)+O(\epsilon^2)
\]

is locally finite.  A diagonal pointwise criterion is therefore too strong
for the operator kernel.

## 3. Open-interval BFV/Faddeev--Popov measure

For

\[
S=\int_0^1ds\,[p_A\dot q^A-N\mathcal C],
\]

fixed endpoint configurations require the gauge parameter to vanish at both
ends.  Since

\[
\delta N=\dot\epsilon,
\qquad
\epsilon(0)=\epsilon(1)=0,
\]

the proper-time modulus

\[
T=\int_0^1Nds
\]

is gauge invariant and remains to be integrated.

In the gauge $\dot N=0$, the nonzero-mode FP operator is
$-\partial_s^2$ with Dirichlet ghost endpoints.  On a unit coordinate
interval, with the zeta reference scale fixed to one,

\[
\det_\zeta(-\partial_s^2)=2.
\]

If the same bare operator and reference scale are instead written as
$-\partial_\tau^2$ on a coordinate interval of length $L$, then

\[
\det_\zeta(-\partial_\tau^2)=2L.
\]

That $L$ is not a physical extra modulus weight.  The operator obtained from
the fixed-$s$ gauge is $-L^2\partial_\tau^2$; zeta scaling gives

\[
\det_\zeta(-L^2\partial_\tau^2)=2.
\]

Equivalently, for any positive gauge-condition rescaling,

\[
\delta(f\chi)\det(fM)=\delta(\chi)\det M.
\]

An isolated determinant factor can therefore be moved between the delta
functional, ghost determinant, and measure.  Within this fixed-$s$ reduced
gauge and BFV normalization, the open-interval reduced modulus measure is, up
to an overall convention,

\[
\boxed{dT},
\]

not $T\,dT$ inserted to cancel the short-time kernel.  This statement concerns
the lapse modulus; it does not fix the physical endpoint configuration-space
measure.  The familiar $dT/T$
of a closed loop involves a residual rigid-translation zero mode and must not
be imported into this open fixed-endpoint problem.

## 4. Why an inserted lapse power changes the theory

The positive half-line spectral integral is

\[
G_0(H)
=\int_0^\infty dN\,e^{-iN(H-i0)}
=-\frac{i}{H-i0},
\]

and satisfies

\[
HG_0=-i\mathbf1
\]

in the zero-regulator limit.  Multiplying the measure by $N$ instead gives

\[
G_1(H)
=\int_0^\infty dN\,N e^{-iN(H-i0)}
=-\frac{1}{(H-i0)^2},
\]

which is a different, double-pole Green function.

Likewise,

\[
\int_{-\infty}^{\infty}dN\,e^{-iNH}
=2\pi\delta(H),
\]

but

\[
\int_{-\infty}^{\infty}dN\,N e^{-iNH}
=2\pi i\delta'(H),
\]

and

\[
H\delta'(H)=-\delta(H)\ne0.
\]

Thus an endpoint power selected only to improve pointwise convergence fails
the original sourced-resolvent or WDW constraint-annihilation identity.
The distribution $\delta'(H)$ remains supported on $H=0$; what fails is
annihilation by $H$.

## 5. Lateral bypass is an off-diagonal question

The algebraic control

\[
\frac1N\exp\left(\frac{A}{N}+BN\right)
\]

has a small-circle residue

\[
\sum_{k=0}^\infty\frac{(AB)^k}{(k!)^2}
=I_0(2\sqrt{AB}).
\]

Even after multiplying by $N$, the off-diagonal essential singularity has
residue

\[
\sum_{k=0}^\infty
\frac{A^{k+1}B^k}{(k+1)!k!}
=\sqrt{\frac AB}\,I_1(2\sqrt{AB}).
\]

Therefore canceling the diagonal $1/N$ factor does not generally eliminate
the difference between lateral bypasses.  The full off-diagonal parametrix,
its determinant phase, and its declared contour are required.

For every fixed bounded spectral truncation, a zero-radius endpoint arc has a
vanishing norm bound.  The obstruction in gravity is that the spectrum and
kinetic form are unbounded and indefinite, so that this limit is not uniform.

## 6. Conformal-sign obstruction

Write the kinetic eigenvalues as

\[
m_g=-\mu_g<0,
\qquad
m_s=+\mu_s>0.
\]

For $N=+i\tau$, the exponent contains

\[
-\frac{\mu_gx_g^2}{2\tau}
+\frac{\mu_sx_s^2}{2\tau};
\]

the gravitational direction is damped and the scalar direction grows.  For
$N=-i\tau$, the signs reverse.  Hence

\[
\boxed{
\text{no single imaginary-lapse sign damps both homogeneous directions}
}.
\]

One must specify a simultaneous contour for the negative kinetic/conformal
direction.  This contour also fixes the square-root phase of the determinant
and can affect the allowed relative homology.

## 7. Trace-class and state interpretation

The $N\to0$ operator is the identity, whose Hilbert--Schmidt norm in a
$D$-dimensional cutoff is

\[
\|\mathbf1_D\|_{\rm HS}^2=D.
\]

It diverges as the cutoff is removed and is not a normalized density.  The
full-line group average is a constraint-supported rigging distribution, not
automatically trace class.  The half-line object is a Green function with an
identity source.  Neither is yet a full quantum seam state.

## 8. Verdict

| Question | Result |
|---|---|
| Is the raw $1/N$ behavior a genuine short-time effect? | **Yes.** |
| Does it obstruct the leading quadratic distributional parametrix? | **No; it is the delta-kernel normalization.** |
| Does the open-line Dirichlet ghost cancel it? | **No; the full reduced FP factor is $T$-independent.** |
| May one insert $N$ as a renormalization? | **No; it changes the resolvent and group average.** |
| Does one lapse Wick rotation damp both directions? | **No.** |
| Is the positive half-line a WDW projector? | **No; it is sourced.** |
| Is the full-line object a normalized state? | **No; it is a rigging distribution.** |
| Is the lateral PL coefficient now fixed? | **No.** |

The calculation strengthens the connected-seam program at the local operator
level while ruling out a tempting shortcut.  It resolves the leading frozen
quadratic interpretation of the zero-lapse pole; it does not resolve the full
Phase-27/28 global endpoint gate.  The pole is not removed and must be retained
and interpreted distributionally.  The next genuine gate is the
conformal/BFV contour together with the physical endpoint measure and complete
gauge-reduced determinant.

## Scope

Included:

- the frozen two-coordinate quadratic short-time parametrix;
- exact Gaussian-test controls and the Fourier--Schwartz distributional limit;
- reduced open-interval Dirichlet-ghost scaling;
- half-line versus full-line operator identities;
- an algebraic lateral-residue control;
- the homogeneous opposite-sign damping obstruction.

Excluded:

- an interacting all-orders endpoint parametrix;
- local lapse and shift fields beyond minisuperspace;
- a gauge-fixed graviton, matter, gravitino, and ghost determinant;
- a conformal-field thimble and determinant phase;
- a global relative-homology intersection number;
- the physical WDW endpoint measure and factor ordering;
- a positive trace-class WDW/seam density or selection of $\phi_0$.

## Primary references

- J. J. Halliwell, “Derivation of the Wheeler–DeWitt equation from a path
  integral for minisuperspace models,”
  [DOI:10.1103/PhysRevD.38.2468](https://doi.org/10.1103/PhysRevD.38.2468).
  Used for the BFV minisuperspace measure and lapse-range distinction; it does
  not fix the physical endpoint measure of this seam model.
- C. Teitelboim, “Quantum Mechanics of the Gravitational Field in
  Asymptotically Flat Space,”
  [DOI:10.1103/PhysRevD.28.310](https://doi.org/10.1103/PhysRevD.28.310).
  Used for the positive-proper-time causal/source boundary.
- J. A. García, J. D. Vergara, and L. F. Urrutia, “BRST–BFV quantization and
  the Schwinger action principle,”
  [arXiv:hep-th/9511092](https://arxiv.org/abs/hep-th/9511092).
  Used for endpoint BRST boundary conditions and boundary terms; it does not
  determine this gravitational determinant.
- G. W. Gibbons, S. W. Hawking, and M. J. Perry, “Path integrals and the
  indefiniteness of the gravitational action,”
  [DOI:10.1016/0550-3213(78)90161-X](https://doi.org/10.1016/0550-3213(78)90161-X).
  Used for the conformal-direction contour obstruction.
- D. Marolf, “Refined Algebraic Quantization: Systems with a single
  constraint,” [arXiv:gr-qc/9508015](https://arxiv.org/abs/gr-qc/9508015).
  Used for the full-line rigging-map boundary, not for trace-class positivity.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py
```

The executable emits eighteen exact checks, seven numerical checks, and one
`PHASE29_RESULT=` JSON payload.  It writes no files.
