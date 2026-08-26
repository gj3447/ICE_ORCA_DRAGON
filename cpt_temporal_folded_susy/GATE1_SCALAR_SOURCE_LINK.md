# Gate 1 — ordered scalar phase-space/source-link control

> **Workbench status:** `VALID_RUN`
> **Authorization:** `GATE1_SOURCE_LINK_20260826_01`, consumed after one terminal invocation
> **Classification:** `GATE1_NONZERO_LAPSE_SCALAR_SOURCE_LINK_MATCHES_ZERO_LAPSE_DISTRIBUTION_OPEN`
> **Verdict:** `NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN`
> **Programme impact:** `NARROW`
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`; global promotion `PROHIBITED`

## Answer first

Inside one newly declared fixed-\(a\), \(m=2\), scalar phase-space control, the two ordered real
momenta integrate exactly to the inherited configuration action and carry a definite conjugate pair of
Fresnel phases. At fixed regulator the full Starobinsky integrand deforms from the real scalar line to
every declared

\[
\Gamma_\lambda:\quad q=u+i\lambda\psi/\kappa,
\qquad 0<\lambda\le1,
\]

without an orientation change. The equality survives the boundary limit on lapse tests supported away
from \(N=0\). Thus the specified **nonzero-lapse reduced scalar source link is `KEEP`**, with scalar
orientation ratio \(+1\).

This calculation does **not** establish the full \(q\)-paired distribution on tests whose support crosses
\(N=0\), choose \(\lambda=1\), recover a physical original joint cycle, or determine a global intersection
coefficient. Those outputs remain `OPEN` or `null`.

## What was actually run

```text
command: ./ice run cpt_temporal_folded_susy/gate1_scalar_source_link
exit: 0
observed wall time: 2.791651251 s
runner SHA-256: 896f73384368f2fb20779ca780acd7676abc794d45796a3577a965f169947fbe
input SHA-256: 182ab0d04b2869cf01be39e0f73c02919ca4c9c17867f267e3daea915247ebd1
result bytes: 11,117
result SHA-256: ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243
self-excluding payload SHA-256: a3e9f17e7a5d0838cd295427bd161aabb2260b9d15f32b3364b1794ad997d04b
exact checks: 16/16 PASS
theorem guards: 3/3 verified separately
numerical checks: 0
root / ODE / evaluator-reconciliation / descendants: 0 / 0 / 0 / 0
```

The Python 3.13.5 / SymPy 1.14.0 runner wrote exactly one adjacent result. The control plane checked the
clean core tree, runner and input hashes, exact no-argument invocation, stdout/stderr and artifact caps,
then decoded the result authorization, schema, hashes and null promotions. Its private exclusive launch
receipt remains under `.git`; success, failure or timeout would all have consumed the window.

## Provenance and declared status

The repository records enough to fix the following ingredients but not a literal physical-original
phase-space cycle:

- Phase 27 records \(T=iN\), fixed-real-\(q\) endpoint polarization and the below-origin side.
- Phase 30 records real configuration restrictions on nonzero real-lapse arms and a separate local
  Gaussian normalization.
- Phase 31 records the finite-cutoff canonical scalar action and stationary momenta, while leaving an
  absolute momentum-contour/determinant-line orientation open.
- Phase 32 declares a complex lift and local normalization; it does not derive a physical original joint
  cycle.

Accordingly this run declared

\[
p_0,p_1,u\in\mathbb R,qquad
\frac{dp_0\wedge dp_1\wedge du}{(2\pi\hbar)^2},
\]

with the order \(p_0\), then \(p_1\), then \(u\). This is explicitly
`NEW_BOUNDED_SCALAR_CONTROL_NOT_PHYSICAL_ORIGINAL`. It does not inherit the Phase-30 combined BFV
signature phase or a Phase-32/39 intersection sign.

[Witten, arXiv:1001.2933](https://arxiv.org/abs/1001.2933) supplies the relative-cycle/contour-deformation
framework only. [Banihashemi–Jacobson, arXiv:2405.10307](https://arxiv.org/abs/2405.10307) motivates the
below-origin lapse prescription in its stated momentum-first construction. Neither source selects this
scalar field lift, fixes a full determinant-line orientation, or turns it into a physical cycle.

## Exact momentum calculation

Set

\[
\mu=2\pi^2a^3,qquad z=N-i\epsilon,qquad T=iz,qquad
U(q)=2\pi^2\left[-3a+a^3V(\phi+q/2)\right],
\]

with \(\epsilon>0\) and Starobinsky
\(V(\varphi)=\tfrac34(1-e^{-\kappa\varphi})^2\),
\(\kappa=\sqrt{2/3}\). The inherited two-element scalar action reduces exactly to

\[
I_2=q(p_0-p_1)-\frac{z}{4\mu}(p_0^2+p_1^2)-zU(q).
\]

The unique scalar Gaussian stationary point is

\[
p_0^\star=\frac{2\mu q}{z}=\frac{4\pi^2a^3q}{z},
\qquad
p_1^\star=-\frac{2\mu q}{z}=-\frac{4\pi^2a^3q}{z}.
\]

Completing both squares gives

\[
I_2= -\frac{z}{4\mu}
\left[(p_0-p_0^\star)^2+(p_1-p_1^\star)^2\right]
+\frac{2\mu q^2}{z}-zU(q).
\]

Since \(\operatorname{Re}(iz)=\epsilon>0\), the ordered two-dimensional damped Gaussian is in its
principal domain. Including the declared measure,

\[
J_p(z)=\frac{1}{(2\pi\hbar)^2}
\int_{\mathbb R^2}dp_0\,dp_1\,
e^{-iz[(p_0-p_0^\star)^2+(p_1-p_1^\star)^2]/(4\mu\hbar)}
=\frac{\mu}{\pi i\hbar z}
=\frac{2\pi a^3}{\hbar T}.
\]

The on-shell action obeys

\[
i\left(\frac{2\mu q^2}{z}-zU(q)\right)
+\left(\frac{2\mu q^2}{T}+TU(q)\right)=0,
\]

so the Lorentzian and configuration integrands agree as
\(e^{iI_2/\hbar}=e^{-S_2/\hbar}\).

On the two nonzero real-lapse arms, writing \(n=|N|\), each ordered momentum contributes its principal
Fresnel phase:

\[
\begin{array}{c|c|c}
T & \text{one momentum} & J_p\\ \hline
+in & e^{-i\pi/4} & -i\,2\pi a^3/(\hbar n)\\
-in & e^{+i\pi/4} & +i\,2\pi a^3/(\hbar n)
\end{array}
\]

The products are conjugate. No additional sign is inserted inside this declared scalar momentum block;
this is not a statement about the full BFV/Maslov determinant line.

## Full-action contour deformation

For \(T=\rho e^{i\psi}\), \(|\psi|<\pi/2\), the frozen homotopy is

\[
q_s=u+i\,s\lambda\psi/\kappa,qquad 0\le s\le1.
\]

The integrand is entire in \(q\). The finite rectangular contour retains the actual connector measures
\(dq=du\) on horizontal pieces and
\(dq=i\lambda\psi\,ds/\kappa\) on vertical pieces. Its two end bounds are different:

1. As \(u\to+\infty\) at \(\operatorname{Re}T>0\), the kinetic quadratic coefficient is
   \[
   \operatorname{Re}\frac{2\mu}{T}=\frac{2\mu\cos\psi}{\rho}>0.
   \]
2. As \(u\to-\infty\), the full-rate Starobinsky term has phase defect
   \[
   d_s=(1-s\lambda)\psi
   \]
   and leading positive real coefficient proportional to \(\cos d_s>0\).

After removing the field cutoff at fixed \(\epsilon>0\), the boundary arms also retain two good ends for
every fixed \(0<\lambda\le1\):

\[
u\to-\infty:\quad \sin(\lambda\pi/2)>0,
\qquad
u\to+\infty:\quad
\operatorname{Re}S_2\sim
\frac{4\pi^3a^3\lambda}{\kappa n}\,u>0.
\]

Therefore the regulated real control and \(\Gamma_\lambda\) are equal before the lapse limit. Compactly
supported tests on each closed sub-arm away from zero permit \(\epsilon\downarrow0\), and equality is
independent of \(\lambda\) there. Taking \(\lambda\downarrow0\) on those arm distributions introduces no
scalar orientation jump. This establishes equality with the declared \(0<\lambda\le1\)
\(\Gamma_\lambda\) subfamily on the nonzero arms; it does not source-select \(\lambda=1\).

## Why the pure Gaussian shortcut is rejected

If the Starobinsky potential is dropped, then on either shifted boundary arm

\[
\operatorname{Re}S_{\rm kin}
=\frac{4\pi^3a^3\lambda}{\kappa n}\,u.
\]

It is positive as \(u\to+\infty\) but tends to \(-\infty\) as \(u\to-\infty\). Thus the kinetic-only
shifted contour has one exponentially growing end. A closed-form real-line pure Gaussian cannot certify
the affine source link. The negative end is repaired only by the full Starobinsky action in the fixed
limit order used above.

## Distributional boundary and the remaining open point

The momentum prefactor alone has the standard below-origin boundary value

\[
\lim_{\epsilon\downarrow0}J_p(N-i\epsilon)
=\frac{2\pi a^3}{\hbar}
\left[\pi\delta(N)-i\,\operatorname{PV}\frac1N\right].
\]

That does not determine the distribution obtained after pairing the **full configuration integral** with
test functions crossing \(N=0\). The separately reviewed analytic contour and boundary argument
establishes equality only on \(C_c^\infty((-R,0)\cup(0,R))\), with fixed \(R=6/5\). It does not establish contact terms, uniform
zero-lapse control or interchange of the field and lapse limits. The zero-including full \(q\)-paired
distribution therefore remains `OPEN`, not contradicted.

## Scoped verdict

The observed row of the pre-run frozen decision table is:

```text
run_status                                      = VALID_RUN
verdict                                         = NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN
reduced_affine_class_nonzero_arm_source_link    = KEEP
scalar_orientation_ratio                       = +1
zero_lapse_distribution                        = OPEN
phase_locked_representative_selected            = false
programme_impact                               = NARROW
Gate 1                                         = OPEN_PARTIAL_PROGRESS
global promotion                               = PROHIBITED
automatic_next                                 = null
```

An independent read-only algebra/hash audit recomputed the self-excluding digest, checked all 16 unique
executable exact result entries and three separately typed theorem guards, and rederived the momentum prefactor, arm
phases, positive and negative end coefficients and negative control. It found no conclusion-changing
error and did not rerun the one-shot runner.

## Explicit non-results

This result supplies none of the following:

- a recovered or unique physical original \((q,p,a,N,\mathrm{BFV})\) cycle;
- a \(\lambda=1\) physical selection principle;
- the zero-including full \(q\)-paired lapse distribution or contact terms;
- a varying-\(a\), \(p_a\), ghost, gauge or full determinant-line orientation;
- an \(R\to\infty\), \(m\to\infty\), cutoff or continuum theorem;
- a saddle/upward-cycle/sheet/Stokes/intersection census;
- a bounded/global signed sum, `global_n_sigma`, physics claim or TOE claim.

The next mathematical obstruction is now narrower: extend or reject the full \(q\)-paired distribution
through \(N=0\) and then embed the scalar control into a source-derived full joint/BFV cycle. No such
calculation or automatic descendant is authorized by this result.
