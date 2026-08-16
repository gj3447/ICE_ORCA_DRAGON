# Phase 17 — real-line time fold algebra without a scalar clock

## Outcome

Here \(t\) is only the coordinate on the real line,

\[
t\in\mathbb R=\mathbb R_-\cup\{0\}\cup\mathbb R_+,
\]

not a rolling chiral field, a relational clock, or a background solution.
With that distinction enforced, the direct calculation gives a split but
useful result.

1. A standard support-local \(4d\;N=1\) supercharge acts at the same value of
   \(t\), so its two open-half cross blocks vanish exactly.
2. After folding the line into a fundamental two-sheet space, the charge
   \(Q^X_\alpha=X_s\otimes q_\alpha\) satisfies the standard fixed-positive-
   energy algebra and exchanges the sheets in both directions.  This is a
   genuine algebraic positive result.
3. Unfolding the same \(X_s\) as literal \(t\mapsto-t\) makes the operation
   nonlocal on the original line and reverses the signed time-translation
   generator.  A fixed \(t=0\) seam also preserves no nonzero ordinary
   Lorentzian-real \(N=1\) parameter.
4. A doubled real, Pin-like projector does exist and has real rank four.  It
   removes the single-copy reality obstruction, but an invariant action,
   common operator domain, conserved charge, and physical sheet observable
   remain to be constructed.

So the programme is **not an algebraic failure**.  The viable algebraic object is a
doubled-sheet theory with ordinary SUSY inside its fibers.  What fails is the
stronger identification of a standard local supercharge with bare reflection
between the two coordinate-time halves.

Executable:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py
```

The run returned exit 0 with **34 exact symbolic checks**.

## 1. Minimal positive-energy \(N=1\) fiber

At a generic massive rest-frame momentum \(p=(E,0,0,0)\), \(E>0\), take two
CAR modes

\[
c=\begin{pmatrix}0&1\\0&0\end{pmatrix},\quad
a_1=c\otimes I_2,\quad a_2=Z\otimes c,\quad
\Gamma_F=Z\otimes Z,\quad Z=\operatorname{diag}(1,-1),
\]

and

\[
q_\alpha=\sqrt{2E}\,a_\alpha .
\tag{E186}
\]

The four-dimensional Fock fiber then obeys

\[
\{q_\alpha,q_\beta\}=0,\qquad
\{q_\alpha,q_\beta^\dagger\}=2E\delta_{\alpha\beta}I_4,
\qquad \{\Gamma_F,q_\alpha\}=0.
\]

This is a rest-fiber realization of the standard super-Poincaré algebra
classified by
[Haag, Łopuszański and Sohnius](https://doi.org/10.1016/0550-3213(75)90279-5),
not a new spacetime algebra.

This is a fixed positive-energy fiber, not by itself a representation of a
sharp projector onto \(t>0\) in the energy basis.

## 2. Local and exchanging charges

Let the folded sheet space be spanned by \(|-\rangle,|+\rangle\), with

\[
Z_s=\begin{pmatrix}-1&0\\0&1\end{pmatrix},\qquad
X_s=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
\Pi_\pm=\frac{I_2\pm Z_s}{2}.
\]

The two exact candidates are

\[
Q^{\rm loc}_\alpha=I_s\otimes q_\alpha,
\qquad
Q^X_\alpha=X_s\otimes q_\alpha.
\tag{E187}
\]

Both satisfy

\[
(Q_\alpha)^2=0,\quad
\{Q_\alpha,Q_\beta\}=0,\quad
\{Q_\alpha,Q_\beta^\dagger\}=2E\delta_{\alpha\beta}I_8,
\quad
\{I_s\otimes\Gamma_F,Q_\alpha\}=0.
\]

Their sheet actions differ:

\[
\Pi_-Q^{\rm loc}_\alpha\Pi_+
=\Pi_+Q^{\rm loc}_\alpha\Pi_-=0,
\]

whereas each nonzero cross block of \(Q^X_\alpha\) has complex rank two in
both directions.  The tested one-way block
\(|+\rangle\langle-|\otimes q_\alpha\) is nilpotent and odd but fails the
standard adjoint closure.  Standard \(N=1\) therefore permits a unitary
two-way exchange, not an intrinsic one-way arrow of time.

The sheet sign must not be identified with fermion parity.  With
\(\Gamma_{\rm bad}=Z_s\otimes\Gamma_F\), the two minus signs cancel and
\([\Gamma_{\rm bad},Q^X_\alpha]=0\): the proposed charge becomes fermion-even.
Each sheet must instead contain a complete boson/fermion multiplet.

## 3. The algebra does not choose the fold

For every real \(\theta\),

\[
U_\theta=\cos\theta\,I_s+i\sin\theta\,X_s,
\qquad Q^{(\theta)}_\alpha=U_\theta\otimes q_\alpha
\tag{E188}
\]

has the same \(N=1\) closure, while its cross-block norm is proportional to
\(\sin^2\theta\).  Moreover, with the parity-controlled unitary

\[
W=I_s\otimes P_{F,+}+X_s\otimes P_{F,-},
\]

the executable proves

\[
WQ^{\rm loc}_\alpha W^\dagger=Q^X_\alpha.
\]

Thus a physical, basis-independent sheet anchor is essential.  Algebraic
closure alone cannot tell nature to choose the exchange basis.

## 4. Why literal reflection of the coordinate line is different

On the original history space let

\[
(R_t\psi)(t)=\psi(-t),\qquad P_t=-i\partial_t.
\]

Then

\[
R_tP_tR_t=-P_t,\qquad
\{P_t,R_tq_\alpha\}=0,\qquad
[P_t,R_tq_\alpha]\ne0.
\tag{E189}
\]

So \(R_tq_\alpha\) has the fixed-fiber CAR algebra but is neither same-point
local nor a standard translation-commuting spacetime supercharge.  Conversely,
any support-local differential operator maps a function supported in one open
half-line back into that half-line, forcing both open-half cross blocks to
zero.  A seam distribution at \(t=0\) is a boundary operator, not an exchange
of the two whole halves.

There is also a positivity obstruction.  A physical-adjoint anticommutator is
positive,

\[
\langle\psi,\{Q,Q^\dagger\}\psi\rangle
=\|Q\psi\|^2+\|Q^\dagger\psi\|^2\ge0,
\]

whereas the signed full-line generator \(P_t\) has both signs of spectrum.
Replacing it by \(|P_t|\) changes the algebra and makes the square-root charge
nonlocal in \(t\).

The executable's three-point symmetric grid is an exact finite control for
the reflection and sign reversal.  The continuum obstruction is the analytic
operator identity E189 together with the norm-square inequality above; no
claim that the finite grid proves a continuum domain theorem is made.

## 5. Temporal seam reality and the doubled opening

For an ordinary Lorentzian-real Weyl parameter
\(\bar\zeta=\zeta^\dagger\), the normal component of the standard closure
vector at a fixed \(t=0\) seam is

\[
v^0=\zeta\sigma^0\bar\zeta
=|\zeta_1|^2+|\zeta_2|^2.
\tag{E190}
\]

Tangency to the seam requires \(v^0=0\), hence \(\zeta=0\).  The executable
checks the real Hessian \(2I_4>0\).  If \(\zeta\) and \(\bar\zeta\) are instead
made independent complex variables, nonzero tangent solutions exist, but the
Lorentzian conjugacy condition has then been abandoned.

The projector diagnosis says the same thing.  A spatial normal has
\(\gamma_n^2=+1\), so \((1+\gamma_n)/2\) is a real half projector.  A temporal
normal has \(\gamma_0^2=-1\), so its rank-two projectors are the conjugate
complex pair \((1\pm i\gamma_0)/2\) and have no nonzero single-copy real fixed
parameter.

There is nevertheless an exact doubled real witness.  If \(K_s^2=-I_s\) is a
real complex structure on the sheet doublet, then

\[
J_{\rm fold}=K_s\otimes\gamma_0,\qquad
J_{\rm fold}^2=+I_8,\qquad
P_{\rm fold}=\frac{I_8+J_{\rm fold}}2,\qquad
\operatorname{rank}_{\mathbb R}P_{\rm fold}=4.
\tag{E191}
\]

This projector mixes the sheets.  It is the most concrete opening found in
Phase 17, but it is only a reality/projector witness.  It does not verify a
Pin\(^{\pm}\) Clifford lift, reflection square/cocycle, Majorana bilinear,
action, charge, positivity, junction condition, or observable, and it is not
yet known to be compatible with \(Q^X_\alpha\) on a common domain.
The required reflection lift and square/cocycle data would have to be fixed
in the sense discussed by
[Witten](https://arxiv.org/abs/1508.04715) and
[Freed and Hopkins](https://arxiv.org/abs/1604.06527), rather than inferred
from the rank-four projector alone.

The spatial-boundary constructions in
[Belyaev and van Nieuwenhuizen](https://arxiv.org/abs/0801.2377) and
[Di Pietro, Klinghoffer and Shamir](https://arxiv.org/abs/1502.05976) explicitly
use a spacelike normal.  They therefore provide a positive control, not a
license to replace their spatial coordinate by \(t\).  The wall/cosmology
continuation instead leads to pseudo-supersymmetry in
[Skenderis and Townsend](https://arxiv.org/abs/hep-th/0610253).

## 6. Time reversal, CPT, and Schwinger–Keldysh

Physical Wigner time reversal has the form \(\Theta_T=U K R_t\), including
complex conjugation \(K\), and is antiunitary.  It can conjugate the set of
supercharges as a discrete automorphism, but it is not a complex-linear
fermion-odd \(Q\).  Likewise, a CPT relation between pre- and post-
singularity histories can be a physically meaningful horizontal sewing, as
in the [CPT-symmetric-universe proposal](https://arxiv.org/abs/1803.08928),
without turning the two histories into particle superpartners.  A CPT theorem
for the laws also does not by itself prove that a chosen background, junction,
or state is CPT invariant.

The clean hybrid interpretation is therefore

\[
\text{sheet }-\ \xleftrightarrow{\ \mathrm{CPT/Pin\ sewing}\ }\
\text{sheet }+,
\qquad
\text{boson}\ \xleftrightarrow{\ Q_\pm\ }\ \text{fermion}
\quad\text{inside each sheet}.
\]

A genuine real-time timefold also exists in Schwinger–Keldysh theory, but its
fermionic generators obey the topological algebra

\[
Q_{\rm SK}^2=\bar Q_{\rm SK}^2
=\{Q_{\rm SK},\bar Q_{\rm SK}\}=0,
\tag{E192}
\]

and make difference operators BRST exact.  They encode unitarity and contour
identities rather than particle superpartners; see
[Haehl, Loganayagam and Rangamani](https://arxiv.org/abs/1610.01940) and
[Geracie et al.](https://arxiv.org/abs/1712.04459).
The executable instantiates only the minimal abstract quartet identities in
E192.  Its barred BRST matrix is not a positive-Hilbert adjoint, and neither a
full contour operator algebra nor a ghost metric is constructed.

## 7. What is now ruled out, allowed, and open

| Construction | Exact result | Physical reading |
|---|---|---|
| Standard local \(Q\) on one real line | \(N=1\) algebra passes; half cross blocks are zero | ordinary same-point SUSY |
| \(R_tq_\alpha\) on the unfolded line | fixed-fiber algebra passes | nonlocal and not translation commuting |
| Fundamental \(X_s\otimes q_\alpha\) | algebra and bidirectional exchange pass | viable internal-sheet algebra; bare time reflection still fails |
| One-way sheet charge | standard adjoint closure fails | no intrinsic arrow from ordinary \(N=1\) |
| Single-copy fixed temporal seam | only zero real preserved parameter | ordinary real half-SUSY contradicted |
| Doubled real fold projector | rank-four witness exists | action/domain/charge still open |
| SK timefold | BRST algebra passes | not particle \(N=1\) SUSY |

The strongest literal claim — “a standard local \(Q\) itself sends every
\(t>0\) state to the corresponding \(t<0\) state” — is contradicted.  The
weaker and more flexible claim — “a new fundamental doubled-sheet theory may
carry a unitary sheet-exchanging \(N=1\) charge” — is algebraically allowed
and is now the leading construction target.

## 8. Next direct calculation

The next calculation should stay rigid and free before returning to local
supergravity:

1. Put two complete free Wess–Zumino multiplets on the folded half-line
   \(\tau\ge0\), with the doubled real structure E191, and derive rather than
   assume its Pin/Clifford lift and reflection cocycle.
2. Derive the bulk variation and the most general quadratic \(\tau=0\)
   sewing/boundary functional without borrowing a spatial-wall sign.
3. Solve simultaneously for a positive inner product, a self-adjoint
   variational domain, and a conserved complex-linear fermionic charge.
4. Test whether a source-defined observable fixes the sheet projectors and
   distinguishes \(Q^X\) from the basis-equivalent local charge.

If that construction fails, the physically conservative endpoint remains a
CPT/Pin pairing between histories with ordinary SUSY acting inside each one.
If it succeeds, it supplies the missing action-and-domain bridge needed before
any cosmological or local-supergravity interpretation.
