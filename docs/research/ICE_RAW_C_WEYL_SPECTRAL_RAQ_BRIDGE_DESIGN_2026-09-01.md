# Raw-\(C\) Weyl--spectral--RAQ bridge design

> Status: execution-free, repository-local method and convention record.
> It is not a physics claim, computation evidence, a research contract, or
> authority to launch a successor calculation.  The raw result files remain
> the calculation ledgers.

## Decision

The real corridor result and the nonreal spectral programme must remain two
different statements.

- The real calculation has already established, on its exact small rectangle,
  one unique simple \(\kappa\)-transverse zero of the selected normalized
  functional \(G(\kappa,\lambda)\) for every fixed \(\lambda\), together with
  a continuous selector \(\kappa_*(\lambda)\).  This is the complete claim in
  its present scope.
- One declared measurable, \(p\)-preserving raw-\(C\) self-adjoint extension
  already exists: \(\Gamma_{1,p}=0\) for Lebesgue-a.e. \(p\).  It is the P4
  engineering baseline, not a physically unique extension.
- The existing \(M_{\rm cut}=-\Gamma_1/\Gamma_0\) calculation and fixed
  upper-half-plane branch box are finite-cutoff and branch calibrations only.
  They are not the selected extension's singular Weyl function, spectral
  measure, or RAQ construction.
- Before any Stieltjes inversion, the raw positive-second-derivative
  convention requires a reciprocal and a fixed leading-coefficient factor.
  Once an actual singular endpoint ratio \(M\) has been constructed with the
  boundary normalization below, the selected-extension Herglotz coordinate is

  \[
  m_{\Gamma_1=0}(z;p)=-\frac{1}{2\hbar^2M(z;p)},
  \qquad M(z;p)=-\frac{\Gamma_{1,p}u_{+,z}}
                       {\Gamma_{0,p}u_{+,z}}.
  \]

The next scientific obstruction is therefore not another real-root search and
not construction of a first a.e.-\(p\) self-adjoint extension.  It is an actual
complex endpoint theorem, first as a \(p=0\) method certificate and then
uniformly on compact \(p\)-bands away from zero.  At \(p=0\), the existing
direct-integral artifact is provenance for the declared boundary-line
convention only: endpoint classification and the boundary maps must be
established independently because an a.e.-\(p\) result does not determine its
null singleton.  Spectral measure, the \(p\to0\) threshold, RAQ, and
raw-\(C\)/selected-\(H\) equivalence are later independent gates.

## What is already reusable

| Object | Repository status | Reusable role | It does not supply |
| --- | --- | --- | --- |
| Fixed-\(\lambda\) real root theorem | `VALID_RUN`, exact declared corridor | A later real-axis pole/shell cross-check | A nonreal endpoint, \(z\)-analyticity, a residue, or a measure |
| \(\Gamma_{1,p}=0\) direct-integral extension | One declared measurable decomposable self-adjoint extension | The fixed domain and boundary line for P4 | Physical selection, general \(p\)-mixing extensions, spectral resolution, or RAQ |
| Finite \(M_{\rm cut}\) proxy | Stable sampled upper-half-plane sign and Green--Lagrange regression | Numerical regression for a later endpoint construction | Cutoff removal, analytic \(M\), selected \(m\), or Stieltjes inversion |
| Fixed \(p=0\) branch box | Principal square-root cut separation and positive real-part bound | One complex-tail precondition | The recessive solution, endpoint Wronskians, or any global \(p\) statement |
| Selected densitized \(H\) KL/RAQ result | A separate selected-\(H\) construction | A comparison target after raw-\(C\) RAQ exists | Raw-\(C\) RAQ or quantum equivalence under \(H=fC\) |

The primary singular Sturm--Liouville reference supplies the maximal/minimal
operator, self-adjoint extension, singular Weyl, spectral transform and
multiplicity framework.  It does not prove this model's endpoint bounds or
measurable \(p\)-uniform construction.  Likewise, the RAQ references specify
rigging-map obligations but do not prove convergence or positivity for this
operator.

## Why the real corridor is not a Weyl calculation

In the current convention the Fourier fiber is

\[
\mathcal H_{C,p}=L^2(\mathbb R_Q,f(Q)dQ),\qquad
f(Q)=12\pi^2e^{3Q/2},
\]

\[
C_p=f^{-1}\left[
2\hbar^2\partial_Q^2+3p^2-72\pi^4e^{2Q}
\right].
\]

The spectral equation \(C_pu=zu\) is

\[
u''=\left[
\frac{36\pi^4}{\hbar^2}e^{2Q}
+\frac{z f(Q)}{2\hbar^2}
-\frac{3p^2}{2\hbar^2}
\right]u.
\]

With \(\hbar=1\), \(p^2=2\kappa^2/3\), and real \(z=\lambda\), this is the
equation used by the real P1 lane.  P1 proves a local characteristic dispersion
statement: for each real \(\lambda\) in one slab, exactly one \(\kappa\) in one
corridor satisfies the selected boundary equation.  Its strict
\(\partial_\kappa G\) bound is transverse in the external fiber parameter.

A spectral measure at fixed \(p\), however, requires the nonreal resolvent and
the boundary behavior as a function of \(z\).  In particular, the present
\(\partial_\kappa G\) is not \(\partial_z\Gamma_1\), an eigenfunction norm, a
pole residue, or the boundary value \(\operatorname{Im}m(E+i0)\).  It may later
enter a \(p\)-shell/coarea calculation, but only after the true spectral
normalization and the \(p\leftrightarrow\kappa\) Jacobian have been fixed.

## Boundary-coordinate and Weyl convention audit

The repository uses the ordinary Wronskian and the zero-energy real reference
pair at \(Q_0=-4\):

\[
W(c_p,s_p)=1,
\qquad
\Gamma_{0,p}u=\lim_{Q\to-\infty}W(u,s_p),
\qquad
\Gamma_{1,p}u=-\lim_{Q\to-\infty}W(u,c_p).
\]

Consequently

\[
u=\Gamma_0(u)c_p+\Gamma_1(u)s_p
\]

in boundary coordinates, and the minus-end symplectic form is

\[
W(\bar u,v)\big|_-
=\overline{\Gamma_0(u)}\Gamma_1(v)
-\overline{\Gamma_1(u)}\Gamma_0(v).
\]

The selected line is \(\Gamma_1=0\).  Hence

\[
M=-\frac{\Gamma_1(u_+)}{\Gamma_0(u_+)}
\]

vanishes when the plus-recessive solution satisfies the selected line.  That
makes \(M\) a useful characteristic coordinate, but not the selected
extension's Weyl coordinate.

To match the singular Weyl--Titchmarsh normalization, note that the formal
Sturm--Liouville leading coefficient for raw \(C_p\) is
\(P_{\rm SL}=-2\hbar^2\).  Its quasi-Wronskian is therefore

\[
W_{\rm SL}=P_{\rm SL}W=-2\hbar^2W.
\]

Choose a real-entire fundamental pair \((\theta_{z,p},\phi_{z,p})\) with

\[
(\Gamma_0\phi,\Gamma_1\phi)=(1,0),\qquad
(\Gamma_0\theta,\Gamma_1\theta)
=\left(0,\frac{1}{2\hbar^2}\right).
\]

Then \(\phi\) satisfies the selected boundary condition at the limit-circle
minus end and

\[
W_{\rm SL}(\theta,\phi)=1.
\]

Writing the plus-end \(L^2\) solution as

\[
u_{+,z}=2\hbar^2\Gamma_1(u_{+,z})
\left(\theta_{z,p}+m_p(z)\phi_{z,p}\right)
\]

gives

\[
m_p(z)=\frac{\Gamma_0(u_{+,z})}
              {2\hbar^2\Gamma_1(u_{+,z})}
=-\frac{1}{2\hbar^2M(z;p)}.
\]

This sign is also the one compatible with the upper-half-plane identity.  If
the true plus endpoint has zero Wronskian flux, then for the ordinary
Wronskian

\[
W(\bar u,u)'=
\frac{i\,\operatorname{Im}z}{\hbar^2}f|u|^2.
\]

After the corresponding boundary normalization this becomes

\[
\frac{\operatorname{Im}m_p(z)}{\operatorname{Im}z}
=\|\theta_{z,p}+m_p(z)\phi_{z,p}\|^2_{L^2(f,dQ)}>0.
\]

Thus \(-1/M\), not \(1/M\), preserves the upper half-plane; the additional
\(2\hbar^2\) is fixed by the raw leading coefficient.  A different real-entire
fundamental pair changes a singular \(m\)-function and its measure by the
standard allowed normalization transformation.  The pair above must therefore
be pinned before comparing measures across \(p\) or against selected \(H\).

This algebra fixes the target convention only.  The current
\(M_{\rm cut}\) has no singular endpoint limit, so none of analyticity,
\(\Gamma_1\ne0\) on \(\mathbb C\setminus\mathbb R\), the Herglotz identity,
the poles, or the measure has yet been established for the actual model.

## Ordered gates

The labels below are logical checkpoints, not numbered research phases or
runner names.

| Gate | Required construction | Accept only if | Hold or reject if |
| --- | --- | --- | --- |
| Baseline | Reuse the committed a.e.-\(p\), \(\Gamma_1=0\) decomposable extension and the convention above as provenance. | The weighted Hilbert space, spectral equation, exact Green form, boundary maps, selected line and source normalization are pinned together; a \(p=0\) method unit independently re-establishes its endpoint classification and maps. | An a.e.-\(p\) theorem is silently specialized to the null singleton, a finite-IVP diagnostic is treated as an endpoint resolvent, the extension is called physically selected, or general \(p\)-mixing domains are silently excluded. |
| Endpoint method | On the existing fixed UHP box at \(p=0\), adopt the same declared boundary-line convention and construct the actual plus-recessive solution and both singular minus-end boundary limits. | The fixed-fiber endpoint classification/maps, a normalization-fixed complex Volterra/Liouville--Green contraction, outward tail remainders, validated compact transport, cutoff-independent boundary limits, nonzero selected denominator and the analytic/Herglotz identities all close uniformly in \(z\). | The a.e. direct integral, samples, double-precision solver agreement, positive \(\operatorname{Im}M_{\rm cut}\), or branch separation alone are promoted to a \(p=0\) endpoint theorem. |
| Nonzero-\(p\) bands | Repeat the endpoint construction uniformly on each declared compact \(K\Subset\mathbb R\setminus\{0\}\). | The \((p,z)\) coefficient, tail bounds, denominator separation, resolvent bounds and boundary maps are jointly measurable in \(p\), analytic in \(z\), and uniform on \(K\). | A few sampled \(p\)'s, evenness under \(p\mapsto-p\), or finite-\(Q\) parameter continuity substitutes for a measurable uniform field. |
| Fiber spectral transform | Apply the Herglotz representation and Stieltjes--Livšic inversion to the selected \(m_p\), then build the fiber transform. | The measure is obtained from actual boundary values, the transform is proved unitary, its inverse and multiplication domain are identified, and fiber multiplicity follows under checked hypotheses. | The finite proxy is inverted, or a scalar fiber measure is called the full direct-integral measure. |
| Threshold and global assembly | Analyze \(p\to0\), then assemble the measurable direct integral of the fiber transforms and measures. | Normalization-compatible resolvent/\(m_p\)/measure limits, possible threshold resonance/eigenvalue/atom, local integrability, the two \(\pm p\) sectors and global multiplicity are explicitly resolved. | The statement “\(p=0\) is Lebesgue-null” is used to discard threshold behavior, or a \(p=0\) method box is promoted to an a.e.-\(p\) theorem. |
| Raw-\(C\) RAQ | Choose a dense invariant test space in the global spectral representation and construct the zero-fiber rigging form. | Group averaging has a declared convergence/distributional topology; \(p/t\) interchange and disintegration are justified; the zero-energy density/atom case is classified; reality, positivity, constraint annihilation and observable intertwining hold; the null quotient is completed. | “A spectral measure exists” is treated as RAQ, a formal \(\delta(C)\) is normalized without a test space, or a divergent/vanishing/atomic zero fiber is hidden. |
| \(C/H\) comparison | Compare raw \(C_\Gamma\) with the already selected densitized \(H=fC\) construction. | An explicit domain-preserving unitary/intertwiner carries the selected extension, spectral transforms, observables, test spaces and rigging forms, including the \(p\to0\) threshold. | Classical rescaling, matching formal differential equations away from an endpoint, or agreement at sampled nonzero \(p\) is called quantum equivalence. |

For the last gate, \(f(Q)=12\pi^2e^{3Q/2}\) is neither a bounded multiplier
with bounded inverse nor a harmless constant on the relevant Hilbert spaces.
The relation \(H=fC\) therefore cannot determine operator domains, extensions,
spectral measures, or rigging maps by itself.

## The \(p=0\) threshold is small in measure, not automatically small in RAQ

The selected direct integral is defined only up to Lebesgue-a.e. equality, so
the singleton \(p=0\) does not create an auxiliary-space atom or a gluing law.
That is why the existing fixed box is correctly only a method-development
scope.

Nevertheless, RAQ probes the zero-energy spectral fiber.  A family of densities
may diverge, vanish, acquire a threshold resonance, or fail to be locally
integrable as \(p\to0\), even though the singleton itself has base measure
zero.  The selected-\(H\) construction already illustrates why a weight with
\(1/|p|\)-type behavior cannot be dismissed by the singleton argument.  Raw
\(C\) therefore needs a separate threshold theorem rather than either adding
or deleting an origin sector by convention.

## What spectral measure still has to prove

For each accepted fiber, the desired output is not merely a plotted
\(\operatorname{Im}m\).  It is a measure \(\mu_p\) and a unitary transform

\[
\mathcal F_p:\mathcal H_{C,p}\longrightarrow L^2(\mathbb R,d\mu_p),
\qquad
\mathcal F_p C_{p,\Gamma}\mathcal F_p^{-1}=M_E,
\]

with the source-normalized generalized eigenfunction \(\phi_{E,p}\).  The
Stieltjes--Livšic inversion must use the actual selected \(m_p\):

\[
\mu_p((E_1,E_2])=
\lim_{\delta\downarrow0}\lim_{\epsilon\downarrow0}
\frac1\pi\int_{E_1+\delta}^{E_2+\delta}
\operatorname{Im}m_p(E+i\epsilon)\,dE.
\]

This display uses the stated sequential shifted-endpoint convention for
\((E_1,E_2]\); it is not an unconditional pointwise-density formula.  Endpoint
atoms and the singular part of the measure must be classified separately.

The full operator then requires measurability of the field of transforms and
measures.  Even if each scalar separated fiber has multiplicity one after the
singular Weyl hypotheses are checked, the full \(p\)-direct integral retains
distinct \(+p\) and \(-p\) sectors unless an independently justified quotient
or gluing identifies them.  Fiber multiplicity one is therefore not global
multiplicity one.

## What RAQ still has to prove

Suppose, only for orientation, that near \(E=0\)

\[
d\mu_p(E)=w(E,p)dE+d\mu_p^\perp(E).
\]

On a test space whose spectral representatives are sufficiently regular in
\(E\) and controlled in \(p\), a full-real-parameter group average would
formally give

\[
\eta(\psi)[\varphi]
\sim 2\pi\int_{\mathbb R}
w(0,p)\,overline{\widehat\psi(0,p)}\widehat\varphi(0,p)\,dp,
\]

with the constant depending on the pinned Fourier convention.  This formula
is not yet an output.  It is valid only after proving the needed Fubini or
distributional interchange, excluding or separately treating a zero-energy
atom and singular component, and controlling the \(p\to0\) weight.  The
rigging map must then satisfy reality, positivity, constraint invariance and
observable intertwining before quotienting its null space and completing the
physical Hilbert space.

In particular, a zero-energy atom makes the unregularized full-real-parameter
average diverge; it is not an extra finite positive term.  Retaining such a
sector would require an explicitly different rigging or renormalization
prescription and a new comparison of its normalization.

## Smallest next bounded work unit

The next useful calculation, if separately opened, is one clean unnumbered
`p=0` endpoint-method runner on the already audited UHP box.  It should not
attempt a spectral measure or RAQ.  Its manifest should freeze:

1. the a.e.-\(p\) selected-extension artifact as provenance, an independent
   \(p=0\) endpoint classification/boundary-map audit, the raw spectral
   equation, ordinary and quasi-Wronskian conventions, and the
   \(-1/(2\hbar^2M)\) target;
2. the exact \(p=0\), \(z\)-box and finite matching points;
3. the plus-tail Volterra kernel, contraction radius and analytic remainder;
4. the compact complex interval transport and an independent precision tier;
5. the complete minus-tail Wronskian-limit enclosure for \(\Gamma_0,\Gamma_1\);
6. a nonzero \(\Gamma_1\) enclosure throughout the UHP box;
7. conjugation, analyticity and Green--Lagrange/Herglotz checks;
8. null outputs for \(p\)-band/global measure, multiplicity, RAQ, \(C/H\),
   BFV, empirical and physics conclusions.

The result may say “actual endpoint coordinate on one \(p=0\) box” only if all
eight groups close.  Otherwise it must retain the exact failed tail,
transport, denominator, or analyticity condition as the result.  No outcome
automatically creates the nonzero-\(p\) band calculation.

## Source roles and non-roles

- [Eckhardt, Gesztesy, Nichols and Teschl, arXiv:1208.4677](https://arxiv.org/abs/1208.4677)
  supplies the singular Sturm--Liouville extension, Weyl and spectral-transform
  framework.  Its Herglotz/Stieltjes representation applies here only after
  the pinned selected boundary normalization is proved to define an ordinary
  Nevanlinna \(m\).  It does not supply this model's endpoint estimates or
  \(p\)-uniform field.
- [Marolf, arXiv:gr-qc/9508015](https://arxiv.org/abs/gr-qc/9508015),
  [Giulini--Marolf, arXiv:gr-qc/9812024](https://arxiv.org/abs/gr-qc/9812024),
  [Giulini--Marolf, arXiv:gr-qc/9902045](https://arxiv.org/abs/gr-qc/9902045),
  and [Giulini, arXiv:gr-qc/0003040](https://arxiv.org/abs/gr-qc/0003040)
  supply the RAQ, test-space, rigging-map and conditional group-averaging
  framework.  They do not establish convergence or a physical product here.
- [Louko and Martínez-Pascual, arXiv:1107.1092](https://arxiv.org/abs/1107.1092)
  is the explicit warning that classically equivalent constraint rescalings
  can encounter self-adjointness, extension and superselection ambiguity.  It
  does not decide the raw-\(C\)/selected-\(H\) comparison in this repository.

## Explicit nonclaims

This design does not construct an actual singular endpoint, resolvent, Weyl
function, spectral measure, spectral multiplicity, raw-\(C\) rigging map,
physical product, \(C/H\) equivalence, BFV measure, state, observable,
likelihood, new physical phenomenon, or physics discovery.  It separates the
minimum proofs needed to make any later one of those statements meaningful.
