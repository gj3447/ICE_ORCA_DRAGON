# Phase 21 — connected two-sheet Gaussian seam control

## Result first

The normalized path integral canonically identifies the no-seam baseline, but
it does not force us to subtract that baseline:

\[
\boxed{
R=\frac{Z_{+-}(C)}{Z_+(0)Z_-(0)},\qquad
R-1=\text{chosen zero-cross-sheet exclusion},\qquad
W_{\rm cross}=\log R=\text{connected vacuum generator}.
}
\tag{E217}
\]

Normalization proves \(R(C=0)=1\) and therefore canonically identifies the
no-seam term.  If one additionally chooses to remove the term with no
cross-sheet insertion, the remainder is exactly \(R-1\).  That exclusion is a
physical choice; normalization alone does not impose it.  Moreover, \(R-1\) still
contains products of connected vacuum components.  The linked-cluster object
is \(\log R\), and neither quantity is automatically a probability over
universes or flux sectors.

The executable returns **27 exact PASS and 7 numerical PASS** checks:

~~~bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py
~~~

This is a positive Euclidean Gaussian control, not a solved three-form SUGRA
or Wheeler–DeWitt path integral.  In particular, dividing every sector by its
own decoupled partition function is a normalization convention, not a derived
flat prior over flux labels.

## 1. Exact one-mode seam integral

Take one real mode on each sheet and define

\[
S_E(x_+,x_-)
=\frac12A_+x_+^2+\frac12A_-x_-^2-Cx_+x_-,
\]

\[
\mathcal M=
\begin{pmatrix}
A_+&-C\\
-C&A_-
\end{pmatrix},
\qquad
\det\mathcal M=A_+A_--C^2.
\tag{E218}
\]

The real Euclidean integral is convergent exactly when

\[
A_+>0,\qquad A_->0,\qquad C^2<A_+A_-.
\]

This finite matrix positivity is necessary for the toy integral; it is not a
proof of field-theoretic reflection positivity or Lorentzian unitarity.  Those
require the full Euclidean correlation system and reflection operation; see
[Osterwalder–Schrader II](https://doi.org/10.1007/BF01608978).

Writing

\[
\rho=\frac{C}{\sqrt{A_+A_-}},
\]

the sheet-normalized determinant is

\[
R
=\frac{\int dx_+dx_-\,e^{-S_E}}
{\left(\int dx_+e^{-A_+x_+^2/2}\right)
 \left(\int dx_-e^{-A_-x_-^2/2}\right)}
=\frac1{\sqrt{1-\rho^2}}.
\tag{E219}
\]

At \(C=0\), \(R=1\) exactly.  If one then chooses to remove the zero-insertion
contribution, the remainder is

\[
R-1
=\left\langle e^{Cx_+x_-}-1\right\rangle_0
\]

which contains only terms with at least one cross-sheet insertion.  This is
the precise sense in which the baseline is canonically identifiable and the
**chosen** exclusion has the form \(R-1\).

The covariance is

\[
\mathcal M^{-1}
=\frac1{A_+A_--C^2}
\begin{pmatrix}
A_-&C\\
C&A_+
\end{pmatrix},
\]

so

\[
\langle x_+x_-\rangle_c
=\frac{C}{A_+A_--C^2}
=\frac{\partial\log R}{\partial C}.
\tag{E220}
\]

This already separates the determinant ratio from a physical correlation:
\(R\) is even under \(C\mapsto-C\), whereas the cross correlation is odd.

## 2. Why \(R-1\) is not the connected vacuum functional

The exact expansions are

\[
R-1
=\frac{\rho^2}{2}
+\frac{3\rho^4}{8}
+\frac{5\rho^6}{16}+O(\rho^8),
\]

\[
W_{\rm cross}=\log R
=-\frac12\log(1-\rho^2)
=\frac{\rho^2}{2}
+\frac{\rho^4}{4}
+\frac{\rho^6}{6}+O(\rho^8).
\tag{E221}
\]

At fourth order,

\[
\frac38
=\underbrace{\frac14}_{\text{connected ring}}
+\underbrace{\frac18}_{\frac12(\rho^2/2)^2}.
\]

Hence \(R-1=e^{W_{\rm cross}}-1\) includes configurations with one or more
cross-connected components, including products of those components.  Calling
it the “connected correlator” or “connected probability” would be incorrect.
This moment-versus-cumulant distinction is the finite Gaussian instance of
the generalized cumulant expansion; see
[Kubo](https://doi.org/10.1143/JPSJ.17.1100).

For vectors \(x_\pm\), positive kernels \(A_\pm\), and cross kernel \(C\), let

\[
K=A_+^{-1/2}CA_-^{-1/2}.
\]

Then

\[
R=\det(1-K^TK)^{-1/2},
\]

\[
\boxed{
\log R
=\frac12\sum_{j=1}^{\infty}
\frac1j\operatorname{Tr}\!\left[(K^TK)^j\right].
}
\tag{E222}
\]

Finite-mode convergence requires every singular value of \(K\) to be below
one.  For infinitely many harmonics, an unregularized determinant needs at
least Hilbert–Schmidt decay,

\[
\sum_j s_j(K)^2<\infty.
\]

If this fails, normalizing by \(C=0\) does not remove all \(C\)-dependent UV
divergences.  A regulator and local counterterms are then still required.
Zeta regularization is a valid way to define functional determinants, but it
does not by itself turn flux labels into normalized probabilities.  A
\(\det_\zeta(\mathcal O/\mu^2)\) can retain scale/scheme dependence through
\(\zeta_{\mathcal O}(0)\); numerator–denominator heat-kernel terms and
seam-local counterterms must cancel or be fixed separately.  See
[Hawking's original determinant construction](https://doi.org/10.1007/BF01626516).

## 3. Single-flux tail: one success and one failure

As a bounded UV diagnostic, choose

\[
A_n=a_0+q^2n^2,\qquad n\in\mathbb Z.
\]

### Constant absolute cross coupling

If

\[
C_n=\kappa,\qquad 0<\kappa<a_0,
\]

then

\[
R_n-1
=\left[1-\frac{\kappa^2}{(a_0+q^2n^2)^2}\right]^{-1/2}-1
\sim\frac{\kappa^2}{2q^4n^4}.
\tag{E223}
\]

For one flux integer, both

\[
\sum_{n\in\mathbb Z}(R_n-1),
\qquad
\sum_{n\in\mathbb Z}\log R_n
\]

therefore converge.  With \(a_0=2,q=1,\kappa=1\), the exact high-precision
control gives

\[
\sum_n(R_n-1)=0.319002816952369856\ldots,
\]

\[
\sum_n\log R_n=0.304386389797735255\ldots.
\]

If, as an additional toy convention, one normalizes the positive remainder
with a flat base measure over sectors, then

\[
p_n^{\rm toy}
=\frac{R_n-1}{\sum_m(R_m-1)},
\qquad
p_0^{\rm toy}=0.4849503833765511\ldots.
\]

This is a normalized positive toy weighting under the imposed flat measure.
No exclusive event projector, density matrix, or decoherence functional has
been constructed, so it is not a conditional quantum-event probability or a
Born probability for a universe.

The unnormalized difference of sector partition functions is instead

\[
\Delta Z_n=Z_n(C)-Z_n(0)=Z_n(0)(R_n-1).
\]

For one real mode on each identical sheet,

\[
Z_n(0)=\frac{2\pi}{A_n},
\qquad
\Delta Z_n\sim\frac{\pi\kappa^2}{q^6n^6}.
\]

At the same numerical benchmark,

\[
\sum_n\Delta Z_n=0.776167636301807465\ldots,
\]

and normalization with \(\Delta Z_n\), rather than \(R_n-1\), changes the
normalized positive toy zero-sector weight under the respective imposed
measure from

\[
0.484950\ldots\quad\text{to}\quad0.626161\ldots.
\]

This difference is not an error: it exposes the missing sector measure.  Using
only \(R_n-1\) cancels the \(n\)-dependent \(Z_n(0)\) baseline and thereby
chooses a new prior over normalized sectors.

The dimensionality of the flux lattice also matters.  For the sheet-normalized
quantities \(R_n-1\) and \(\log R_n\), a radial \(n^{-4}\) tail on
\(\mathbb Z^d\) is summable only for

\[
d<4.
\]

For the unnormalized one-mode sector difference, the extra
\(Z_n(0)\sim n^{-2}\) changes the tail to \(n^{-6}\), so its corresponding
toy lattice sum converges for

\[
d<6.
\]

Thus a result that works for one flux can fail in a many-flux discretuum.
Under a compact three-form gauge group, a charge lattice, and charged
membranes, four-form flux can label discrete sectors and membrane solutions
can produce charge-determined flux jumps.  Connecting every adjacent label
additionally requires a primitive-charge membrane.  The weights and transition
dynamics are still additional physical data; see
[Bousso and Polchinski](https://doi.org/10.1088/1126-6708/2000/06/006) and
[Bandos et al.](https://doi.org/10.1007/JHEP07(2018)028).
Moreover, this positive real-boson toy determinant ratio is even in \(C_n\).
It cannot distinguish an oriented \(n\to n+1\) membrane transition from
\(n\to n-1\); an actual
membrane charge, tension, Wess–Zumino term, bounce/junction, zero/negative-mode
treatment, determinant prefactor, and boundary ensemble are still required.

### Constant relative cross coupling

If instead

\[
C_n=\eta A_n,\qquad 0<\eta<1,
\]

then

\[
R_n-1=(1-\eta^2)^{-1/2}-1,
\]

which is independent of \(n\).  Its flux sum diverges linearly with the
cutoff for every \(d\ge1\).  By contrast, the unnormalized sector difference
still contains \(Z_n(0)\sim n^{-2}\) and converges only for \(d<2\).  Therefore

\[
\boxed{
\text{reference subtraction alone does not guarantee flux normalizability.}
}
\tag{E224}
\]

The UV scaling of the actual seam kernel is decisive.

## 4. Relation to the proposed WDW subtraction

If a separate WDW calculation gives \(V_n\sim q^2n^2\), then the two positive
reference differences

\[
w_n^{\rm HH}=e^{\gamma/V_n}-1,
\qquad
w_n^{\rm T}=1-e^{-\gamma/V_n}
\]

both behave as \(n^{-2}\) for a single large flux integer.  On a
\(\mathbb Z^d\) lattice this is summable only for \(d<2\).  It repairs the
one-dimensional \(n\)-tail, but it is not derived by (E219).  The actual
three-form seam action must show why its normalized path integral produces
one of these quantities, including the sign and whether it enters the
wavefunction or the probability.

It also does not repair every direction:

- the HH \(V\to0\) divergence remains;
- a noncompact inflationary plateau can still leave a non-decaying
  \(\phi\)-tail;
- a multi-flux lattice has growing shell degeneracy;
- WDW probabilities require a specified physical inner product/current or a
  decoherence functional; they do not inherit a positive \(L^2\) Born measure
  automatically.

Ramanujan, Abel, or zeta finite parts can consistently define algebraic
objects.  For example,

\[
\sum_{n\in\mathbb Z}e^{-\epsilon|n|}
=\coth\frac{\epsilon}{2}
=\frac2\epsilon+\frac\epsilon6+O(\epsilon^3),
\]

so the symmetric constant tail has zero constant finite part after removing
\(2/\epsilon\).  But a positive constant mass on every integer cannot become
a countably additive probability of total mass zero.  Functional
regularization and probability normalization are different operations.

For a WDW state, probabilities require a specified inner product or a
decoherent-histories construction, not only a finite determinant.  A primary
analysis of that distinction is
[Halliwell](https://doi.org/10.1103/PhysRevD.80.124032); comparisons among
constraint-system formulations and induced products are discussed by
[Hartle and Marolf](https://doi.org/10.1103/PhysRevD.56.6247).

## 5. Bounded verdict

### Established

- dividing by the decoupled two-sheet partition function identifies the
  no-seam term as exactly \(1\);
- choosing to exclude that term gives \(R-1\), but normalization does not
  force the exclusion;
- \(\log R\), not \(R-1\), is the connected vacuum generator;
- the unnormalized sector difference is \(Z_n(0)(R_n-1)\), so summing only
  \(R_n-1\) assumes a flat measure over separately normalized sectors;
- a stable constant-absolute kernel with \(A_n\sim n^2\) yields a summable
  \(n^{-4}\) tail in the one-flux toy;
- a constant-relative kernel leaves a constant tail and still diverges;
- a regularized finite determinant is not yet a flux probability.

### Still open

- deriving \(A_n\) and \(C_n\) from a three-form SUGRA boundary state;
- membrane transition amplitudes and whether flux sectors decohere;
- the Lorentzian contour or a reflection-positive Euclidean construction;
- scalar, tensor, chiralino, gravitino, and ghost harmonic determinants;
- a joint measure over \(n\) and \(\phi\);
- an interior peak that predicts inflationary initial data.

The correct result is therefore

\[
\boxed{
\begin{gathered}
\text{normalization identifies the no-seam baseline, but its exclusion}\\
\text{is an extra weighting choice and does not derive }P(n,\phi_0)
\text{ or select inflation.}
\end{gathered}
}
\]

The next non-arbitrary calculation is to derive the harmonic- and
flux-dependent kernel \(C_{n\ell}\) from an actual three-form SUGRA seam state
or membrane action.  Only then should one form the regulated determinant and
ask whether its joint \(n,\phi\) measure has an interior normalizable peak.
