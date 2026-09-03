# Geometry–energy: minimal verification route

Date: 2026-09-03

Status: **DESIGN_ONLY**. This is a human-facing comparator and falsification
route for the sidecar topic `geometry-energy-unification`. It is not an ICE
action, a canonical-graph node, evidence, an execution plan, or a physics
claim. No calculation in this repository has completed any step below.

The purpose is modest: replace “curvature is energy” with a smallest declared
action whose bookkeeping equivalences, degrees of freedom, and correlated
observables can be tested. Passing a comparator does not establish geometry–
energy unification; a null result is equally useful.

The machine-readable companion is
[`ice-comparator-protocol.v1.json`](../../research/benchmarks/ice-comparator-protocol.v1.json).
Inspect it with `./ice comparator validate|summary|show|trace`; those commands are
read-only and never invoke either external solver.

## Answer first

The first usable calibration is not a new ICE model. It is the following chain:

```text
JBD limit
  -> Hu–Sawicki n=1 f(R) comparator
  -> Jordan/Einstein frame quotient with matter and boundary data
  -> one locked parameter vector
  -> H(z) + growth/lensing + tensor propagation
  -> independently maintained linear-solver comparison
  -> only then: decide whether an explicit ICE action is admissible for testing
```

The same parameter vector must be used at every arrow. A separate fit for
background, growth, lensing, or gravitational waves is flexibility, not a
common mechanism.

## A calibration action, not an ICE derivation

### JBD reference limit

Use the Jordan/matter-frame scalar–tensor normalization

\[
S_{\rm JBD}={1\over16\pi}\int d^4x\sqrt{-g}
\left[\Phi R-{\omega_{\rm BD}\over\Phi}(\nabla\Phi)^2-2V(\Phi)\right]
+S_m[g,\psi].
\]

The calibration check is the appropriate constant-\(\Phi\), large-
\(\omega_{\rm BD}\) general-relativity limit under the declared potential,
matter coupling, and boundary conditions. It is a convention/limit check, not
evidence that ICE is Jordan–Brans–Dicke gravity.

### Hu–Sawicki \(n=1\) comparator

The first finite-parameter covariant model is metric \(f(R)\):

\[
S_{\rm HS}={M_{\rm Pl}^2\over2}\int d^4x\sqrt{-g}
\left[R+f_{\rm HS}(R)\right]+S_m[g,\psi],
\]

\[
f_{\rm HS}(R)=-m^2{c_1(R/m^2)\over c_2(R/m^2)+1},
\qquad m^2=H_0^2\Omega_m.
\]

At high curvature the usual background calibration is
\(c_1/c_2\simeq6\Omega_\Lambda/\Omega_m\). The run declaration must choose a
single remaining model parameter such as \(f_{R0}\), rather than retuning
\(c_1,c_2\) independently for each consumer. This is the comparator introduced
by [Hu and Sawicki](https://arxiv.org/abs/0705.1158), not an ICE result.

For the scalar–tensor quotient, where \(f_{RR}\ne0\), introduce

\[
F=1+f_R(\chi),\qquad U(F)=\chi(F-1)-f(\chi),
\]

so that the auxiliary-field action is

\[
S={M_{\rm Pl}^2\over2}\int\sqrt{-g}\,[F R-U(F)]+S_m[g,\psi].
\]

With \(g^E_{\mu\nu}=F g^J_{\mu\nu}\), the matter term becomes
\(S_m[(F^{-1}g^E),\psi]\). Thus a frame comparison is invalid if it
transforms the gravitational variables but not matter rods/clocks, the boundary
functional, or the declared initial data. The \(f(R)\)–scalar-tensor relation is
the standard \(\omega_{\rm BD}=0\), potential-bearing calibration; it does not
make a frame label an observable. The comparison target is therefore an
invariant or matter-operational quantity of the kind organized by
[Järv–Kuusk–Saal–Vilson](https://arxiv.org/abs/1411.1947), not equality of raw
field coordinates.

## Observable contract

Raw coordinate potentials are not the claimed result. Fix the matter metric,
then compare gauge-invariant or operationally defined quantities on the same
parameter vector

\[
\theta=(f_{R0},H_0,\Omega_m,\Omega_b,\ldots).
\]

The minimum consumer set is:

| Consumer | Required output | Why it is independent |
| --- | --- | --- |
| Background | \(H(z)\), and a dimensionless distance/redshift relation | Homogeneous expansion |
| Scalar structure | \(f\sigma_8(z)\) and either \(\mu(a,k),\eta(a,k)\) or a lensing/\(\Sigma\) observable | Matter clustering versus metric response |
| Tensor | \(c_T\), tensor kinetic normalization/Planck-mass running, and where applicable \(d_L^{\rm GW}/d_L^{\rm EM}\) | Propagation of a distinct spin sector |

For Hu–Sawicki \(f(R)\), \(c_T=1\) is an expected null control; a tensor-speed
departure is not the sought signal. Any changing tensor normalization/friction
must still be derived from the same action and \(\theta\).

## A0–A5 admission and kill table

| Unit | One deliverable | Required choice controls | Kill or retained status |
| --- | --- | --- | --- |
| A0 — declaration | Action, matter metric/coupling, finite \(\theta\), boundary functional/domain, EFT validity scale | State allowed gauge, frame, boundary, initial-state, and cutoff families before solving | Missing object: `UNSPECIFIED`; no computation is meaningful |
| A1 — analytic audit | Euler–Lagrange and Bianchi/Noether identities; scalar/tensor quadratic kinetic signs; JBD/GR limit | Gauge constraint count, \(1+f_R>0\), \(f_{RR}>0\) on the declared viable branch, and stated boundary variation | Negative kinetic/gradient mode, a tachyonic instability on the declared physical/EFT timescale, a singular map, or a pure LHS–RHS rewrite: scoped KILL/relabel |
| A2 — frame quotient | One matter-defined dimensionless observable calculated in both Jordan and Einstein variables | Invertible transformation; transformed matter, boundary term, normalization, and initial data | Disagreement beyond declared numerical error: quotient/domain failure, not new physics |
| A3 — same-coupling consumers | \(H(z)\), scalar growth/lensing, and tensor output from one locked \(\theta\) | Gauge-invariant output definition; no per-sector retuning; matched GR and effective-fluid nulls | Only background, independently fitted sectors, or GR degeneracy: no common-mechanism claim |
| A4 — dual solver | Same convention adapter and output grid in EFTCAMB and hi_class | Independently maintained implementations—not independent physical derivations—with matching initial conditions, units, gauge-invariant extraction, and interpolation | Solver disagreement: `INCONCLUSIVE`; agreement does not exclude an action-to-code mapping error common to both |
| A5 — robustness | Selection/cutoff/boundary stability ledger | Gauge/frame family, physical boundary/initial family, \(k/\Lambda_{\rm EFT}\), \(k_{\max}\), resolution and sampling refinement | Effect disappears under an equivalent choice or lies outside EFT domain: KILL or narrow scope |

An allowed choice is not an arbitrary new theory or physically distinct boundary
state. It is a predeclared family intended to represent the same physical
content. This is the repository-wide distinction in the
[choice-invariance policy](../decisions/ICE_CHOICE_INVARIANCE_CROSS_DOMAIN_PROMOTION_2026-09-02.md).

## Dual solver protocol

[EFTCAMB](https://arxiv.org/abs/1312.5742) evolves full linear single-field EFT
dynamics without assuming a quasi-static approximation and includes stability
checks. [hi_class](https://arxiv.org/abs/1605.06102) independently implements a
broad Horndeski class with Brans–Dicke examples; an \(f(R)\) comparison must
enter through the explicitly audited scalar–tensor/Horndeski mapping. The
common model must be mapped into both programs before comparing declared scalar
and tensor outputs. Agreement is a conditional numerical cross-check only,
never independent physical validation or ICE evidence; it cannot exclude a
mapping error shared by both adapters.
[The multi-code comparison](https://arxiv.org/abs/1709.09135) shows that
sub-percent agreement can be obtained for declared benchmark families; that is
the calibration precedent, not a discovery threshold.

The following externally observed revisions are pinned for a future comparator
packet. Neither tool is installed in this repository, and license review plus
the declared compiler/dependency lock remain required before any use.

| Tool | Repository | Required pin before execution | Status |
| --- | --- | --- | --- |
| H-EFTCAMB/EFTCAMB | <https://github.com/EFTCAMB/EFTCAMB> | `16d9c4e9f85751e30efd0a53b177941713078904` (observed 2026-09-03); release/patch provenance, compiler and CLASS/CAMB dependency lock still required | `NOT_INSTALLED—NO EXECUTION; LICENSE REVIEW REQUIRED` |
| hi_class | <https://github.com/hiclass-code/hi_class_public> | `0009f51d89e6465c79e570b496c66fc90058fa77` (observed 2026-09-03); release/patch provenance, compiler and CLASS dependency lock still required | `NOT_INSTALLED—NO EXECUTION; LICENSE REVIEW REQUIRED` |

The source frameworks are [Gubitosi–Piazza–Vernizzi](https://arxiv.org/abs/1210.0201)
and [Bellini–Sawicki](https://arxiv.org/abs/1404.3713). They organize a class of
models and observables; they do not supply an ICE action.

## External comparator boundaries

The multi-messenger measurement of GW170817/GRB 170817A constrains the
gravity–light speed difference to approximately
\(-3\times10^{-15}\lesssim(c_g-c)/c\lesssim7\times10^{-16}\), so a late-time
model predicting \(c_T\ne1\) is an early empirical kill candidate. See the
official [LIGO–Virgo/Fermi/INTEGRAL paper](https://arxiv.org/abs/1710.05834).

[DESI DR2](https://arxiv.org/abs/2503.14738) is a background-data comparator,
not a modified-gravity selection. The official [DES Year-3 3x2pt
analysis](https://arxiv.org/abs/2105.13549) illustrates why clustering and weak
lensing are distinct consumers. Neither collaboration result is ICE evidence.

## Independent folded Wess–Zumino context

This is a parallel classification lane, not a bridge into the geometry route.

| Scoped CPT result | Correct reading | What it does not do |
| --- | --- | --- |
| [Phase 17](../../cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md) | Standard support-local \(Q\) has zero cross-half blocks; a fundamental doubled-sheet \(Q^X=X_s\otimes q\) is a finite positive-energy algebra witness | Does not give a physical sheet anchor, common positive domain, conserved charge, Pin lift, or constraint closure |
| [Phase 18](../../cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md) | In its free instantaneous-seam class, \(m_{B,\rm pole}^2=m_{F,\rm pole}^2\) and \(\Delta m_{\rm pole}^2=0\) | Does not derive persistent breaking, an interacting spectrum, or a geometry action |

These are context-only inputs to the CPT Gate-4 question about a physical
fermion-odd charge/common domain. They neither advance the geometry comparator
nor receive evidence from it. In particular, a successful A0–A5 comparator
would still not close CPT Gates 1–5.

The boundary/domain check reuses rather than reinvents the established
distinction between a bulk supersymmetric action and a compatible
bulk-plus-boundary variational problem in
[Belyaev–van Nieuwenhuizen](https://arxiv.org/abs/0801.2377), together with the
self-adjoint-extension geometry reviewed by
[Asorey–Ibort–Marmo](https://arxiv.org/abs/1510.08136). Neither source supplies
the missing ICE seam.

## What this route cannot claim

It cannot claim that curvature is energy, that Hu–Sawicki gravity is viable in
the required full sense, that data favor modified gravity, that an ICE action
exists, that a folded-SUSY construction exists, or that the two lanes share a
mechanism. Any future bounded calculation remains subject to human review and
does not receive execution authority from this document.

## First eligible bounded unit

If a later user request authorizes implementation, start with A0–A1 for the JBD
calibration only: freeze one convention/parameter/boundary ledger and derive its
field equations, constraint identity, scalar degree-of-freedom count, and stated
GR-limit check. Do not install a solver, scan Hu–Sawicki parameters, or call a
likelihood in that unit. The result may open the comparator audit only after an
independent analytic check; it cannot automatically create a successor run.
