# Phase 24 — connected Euclidean Starobinsky interval Hessian

## Outcome

The connected $S^3\times I$ minisuperspace calculation is reproducible from
the frozen action.  It gives a genuinely nonzero mixed boundary response,

\[
K_{+-}=\frac{\partial^2 I}{\partial q_-\partial q_+}\ne0,
\qquad q_\pm=(a_\pm,\phi_\pm),
\]

whereas a factorized endpoint action has $K_{+-}=0$.  When endpoint
variations preserve the Hamiltonian constraint by solving the proper length
as a modulus, the mixed block has one nonzero direction:

\[
\boxed{\operatorname{rank}K_{+-}=1}
\]

at this saddle, up to a fourth-order finite-difference error that converges to
zero.  This rank-one result is a Hamilton--Jacobi constraint statement.  It is
not by itself a quantum-entanglement result.

The full real-boundary Hessian is indefinite and the scalar Schur complement
obtained by naively integrating the scale factors is also indefinite.  Thus
the calculation does **not** produce a positive full gravitational density
matrix.  One positive scalar two-mode Gaussian diagnostic is exhibited after
both endpoint scale factors are fixed; its $0.08756$-nat entropy is a conditional
flat-measure diagnostic, not a physical seam entropy.

## 1. Frozen model and supplied benchmark

Reduced Planck units and the Starobinsky mass unit are fixed by

\[
M_{\rm P}=M=1,
\qquad
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\phi}\right)^2.
\]

After the standard Dirichlet gravitational boundary reduction, the real
Euclidean minisuperspace action is

\[
I_E=2\pi^2\int d\tau\left[
-3a(a'^2+1)+a^3\left(\frac12\phi'^2+V(\phi)\right)
\right].
\]

The unconstrained Euler--Lagrange equations are

\[
a''=\frac{1-a'^2}{2a}-\frac a4\phi'^2-\frac a2V,
\qquad
\phi''+3\frac{a'}a\phi'=V_{,\phi},
\]

\[
\mathcal C
=a'^2-1-\frac{a^2}{3}\left(\frac12\phi'^2-V\right)=0.
\]

On the constraint surface only, the scale-factor equation reduces to

\[
a''=-\frac a3\left(\phi'^2+V\right),
\qquad
a''_{\rm full}-a''_{\mathcal C=0}=-\frac{\mathcal C}{2a}.
\]

This distinction is immaterial for the constrained saddle but essential for
the fixed-length off-shell mutation in Section 5.

This phase deliberately supplies two calibration values:

\[
\phi_{\rm center}=1,
\qquad T_0=0.7.
\]

They are not selected by CPT, Pin, an inflation target, or a probability
peak.  Reflection about the interval center gives

\[
q_0=(3.56680319357,1.01858094640,
     3.56680319357,1.01858094640),
\]

\[
I(q_0)=1.40669054283430.
\]

The endpoint velocities are

\[
v_-=(0.09984512855,-0.10663777161),
\qquad
v_+=(-0.09984512855,0.10663777161).
\]

## 2. What is varied

For nearby boundary data, the solver varies

\[
(a'_-,\phi'_-,T)
\]

and imposes the two right-endpoint conditions together with
$\mathcal C=0$.  Therefore $T_0=0.7$ is the length only at the displayed
base saddle; the proper length is a solved modulus under endpoint
variations.  This distinction is decisive.

The canonical endpoint gradient is

\[
\nabla I=(-p_-,p_+),
\]

\[
p_a=-12\pi^2aa',
\qquad
p_\phi=2\pi^2a^3\phi'.
\]

The Hessian is obtained by a five-point derivative of this Hamilton--Jacobi
gradient.  The two smallest step sizes are Richardson extrapolated.

## 3. Connected Hessian and mixed singular spectrum

The extrapolated boundary Hessian, in the order
$(a_-,\phi_-,a_+,\phi_+)$, is

\[
H\simeq
\begin{pmatrix}
-177.349951&1002.772291&1013.888781&949.305806\\
1002.772291&3467.690971&949.305806&888.836655\\
1013.888781&949.305806&-177.349951&1002.772291\\
949.305806&888.836655&1002.772291&3467.690971
\end{pmatrix}.
\]

Hence

\[
K_{+-}\simeq
\begin{pmatrix}
1013.888781&949.305806\\
949.305806&888.836655
\end{pmatrix}.
\]

The Richardson singular spectrum is

\[
\sigma(K_{+-})
=\left(1902.7254364,\;1.30\times10^{-9}\right).
\]

The small-to-large singular ratios at successive step sizes are

\[
8.67\times10^{-7},\quad
5.34\times10^{-8},\quad
3.33\times10^{-9},\quad
2.07\times10^{-10}.
\]

Their observed convergence orders are $4.02,4.01,4.01$, as expected for
the five-point stencil.  The second singular value is therefore a numerical
derivative error, not a second physical channel.

## 4. Why the constrained block has rank one

The Hamilton principal function satisfies a constraint at each boundary:

\[
\mathcal H_+(q_+,\partial_+I)=0,
\qquad
\mathcal H_-(q_-,-\partial_-I)=0.
\]

Differentiating the first equation with respect to $q_-$, and the second
with respect to $q_+$, gives

\[
v_-^T K_{+-}=0,
\qquad
K_{+-}v_+=0,
\qquad
v_\pm^A=\frac{\partial\mathcal H_\pm}{\partial p_{\pm A}}.
\]

The normalized numerical residuals of these two identities are

\[
8.37\times10^{-13},
\qquad
3.28\times10^{-12}.
\]

Since the $2\times2$ mixed block is nonzero but has one left and one right
null direction, it has rank one at this non-caustic saddle.

Under separate invertible endpoint coordinate changes, the mixed block
transforms as

\[
K'_{+-}=J_-^T K_{+-}J_+.
\]

Thus its rank is invariant under those configuration-coordinate
reparametrizations.  Its singular values are not invariant, and the statement
does not cover changes of polarization, clock, or canonical transformations.

## 5. Fixed-length mutation

If $T=0.7$ is instead held fixed for every perturbed endpoint and the
Hamiltonian constraint is not imposed off the base saddle, then

\[
\sigma(K_{+-}^{T\,\mathrm{fixed}})
=(1297.02951,613.38930).
\]

The mixed block is full rank.  Consequently:

\[
\boxed{
\text{connectedness gives }K_{+-}\ne0,
\quad
\text{the Hamiltonian constraint removes one direction.}
}
\]

The rank-one result must not be attributed to connected geometry alone.

## 6. Conditional scalar Gaussian

Fixing both endpoint scale factors, $\delta a_-=\delta a_+=0$, leaves

\[
K_\phi=
\begin{pmatrix}
3467.690971&888.836655\\
888.836655&3467.690971
\end{pmatrix},
\]

whose eigenvalues are $2578.854316$ and $4356.527626$.  Its normalized
off-diagonal **precision coupling** is

\[
\kappa_K
=\frac{(K_\phi)_{12}}
{\sqrt{(K_\phi)_{11}(K_\phi)_{22}}}
=0.256319454.
\]

For the supplied flat $d\phi_-d\phi_+$ measure, the corresponding position
covariance is

\[
\Sigma_\phi=(2K_\phi)^{-1},
\qquad
\rho_\phi
=\frac{(\Sigma_\phi)_{12}}
{\sqrt{(\Sigma_\phi)_{11}(\Sigma_\phi)_{22}}}
=-0.256319454.
\]

Thus the positive number previously denoted by $r$ is the precision coupling,
not the Pearson position correlation.  In a pure two-real-mode Gaussian
reading, the Schmidt magnitude is

\[
|t|=\frac{\kappa_K}{1+\sqrt{1-\kappa_K^2}}
=0.130336866,
\]

with normalized Schmidt probabilities

\[
p_n=(1-|t|^2)|t|^{2n},
\qquad n=0,1,2,\ldots.
\]

\[
S_G
=-\log(1-|t|^2)-\frac{|t|^2}{1-|t|^2}\log |t|^2
=0.087559403\ \mathrm{nats}.
\]

This is a **fixed-$a$, flat-measure, pure-bipartite Gaussian diagnostic**.
A cylinder normally defines a transfer kernel, not automatically a state in
$\mathcal H_+\otimes\mathcal H_-$.  A Choi/reflection prescription, the
physical boundary measure, and trace normalization are required before the
number can be called entanglement entropy.

## 7. Why this is not yet a positive gravitational state

The complete boundary Hessian has eigenvalues

\[
(-1191.996828,-31.810200,2579.612412,5224.876656).
\]

It therefore has two negative boundary directions.  Moreover, formally
integrating the scale factors on the real contour gives the scalar Schur
precision

\[
K_{\phi\mid a}\simeq
\begin{pmatrix}
1191.286530&-1389.967527\\
-1389.967527&1191.286530
\end{pmatrix},
\]

with eigenvalues

\[
(-198.680997,2581.254058).
\]

The real Gaussian remains indefinite.  These boundary-Hessian signs are not
the Morse spectrum of the bulk Dirichlet fluctuation operator: bulk modes
vanishing at both boundaries need not appear in the $4\times4$ response.
The converse is also true--fixing $a_\pm$ does not prove that the bulk saddle
has an acceptable contour.

The missing gates are:

1. a lapse/conformal Picard--Lefschetz contour and its intersection number;
2. the gauge-fixed primed bulk fluctuation operator and Faddeev--Popov ghosts;
3. an outgoing/outgoing or Choi reflection defining two boundary factors;
4. a physical WDW/BFV inner product and trace-class test;
5. the gravitino--Goldstino--ghost Calderón blocks and local-SUSY Ward
   identities.

## 8. Exact scope

Established:

- a real connected homogeneous Starobinsky $S^3\times I$ saddle for the
  explicitly supplied benchmark;
- a nonfactorizing classical cross-boundary response;
- one nonzero constraint-reduced homogeneous cross direction;
- a full-rank fixed-length control;
- a positive fixed-scale scalar subblock and its conditional Gaussian
  diagnostic;
- an indefinite full real-boundary Hessian and indefinite real-contour Schur
  complement.

Not established:

- a dominant or even contributing gravitational thimble;
- a positive quantum density matrix or physical two-universe entanglement;
- a global clock-independent singular spectrum;
- a full bulk negative-mode count;
- a CPT/Pin or local-supergravity completion;
- selection of $\phi_0$, $n$, $a_0$, e-folds, or a SUSY-breaking scale.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py
```

The executable emits six exact checks, fourteen numerical checks, and one
machine-readable `PHASE24_RESULT` record.  It writes no files.

## Primary references and their boundary

- J. J. Halliwell, *Derivation of the Wheeler--DeWitt equation from a path
  integral for minisuperspace models*, Phys. Rev. D **38** (1988) 2468,
  <https://doi.org/10.1103/PhysRevD.38.2468>.  This supports the
  lapse/constraint and ordering boundary, not the numerical saddle above.
- A. O. Barvinsky and D. V. Nesterov, *Quantum effective action in
  spacetimes with branes and boundaries*,
  <https://arxiv.org/abs/hep-th/0512291>.  This supports the relation between
  boundary response and bulk operators, not a positive seam state.
- G. W. Gibbons, S. W. Hawking, and M. J. Perry, *Path integrals and the
  indefiniteness of the gravitational action*, Nucl. Phys. B **138** (1978)
  141, <https://doi.org/10.1016/0550-3213(78)90161-X>.  This is the contour
  warning; the present phase does not solve it.
- W. Donnelly and L. Freidel, *Local subsystems in gauge theory and gravity*,
  <https://arxiv.org/abs/1601.04744>.  This motivates the boundary
  factorization caveat and does not establish a two-universe Hilbert space.
- L. Bombelli, R. K. Koul, J. Lee, and R. D. Sorkin, *Quantum source of
  entropy for black holes*, Phys. Rev. D **34** (1986) 373,
  <https://doi.org/10.1103/PhysRevD.34.373>.  This supports the pure-Gaussian
  Schmidt-entropy control, not its interpretation as gravitational seam
  entropy.
- J. J. Halliwell and J. Louko, *Steepest-descent contours in the path-integral
  approach to quantum cosmology. I. The de Sitter minisuperspace model*,
  Phys. Rev. D **39** (1989) 2206,
  <https://doi.org/10.1103/PhysRevD.39.2206>.  This motivates the missing
  contour/intersection gate; the present phase does not compute it.
