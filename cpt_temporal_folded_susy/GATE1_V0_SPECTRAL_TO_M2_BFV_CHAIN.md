# Gate 1 — $V=0$ local spectral-to-$m=2$ BFV workbench chain

## Outcome

This user-directed sequence executed four separate, bounded, non-numbered
calculations after the local improved-static BFV zero-mode source.  It closes
two local representation questions, kills one uniqueness claim, and reaches
one deliberately narrowed finite-mode result:

| Direction | Frozen verdict | What changed |
|---|---|---|
| 1. Hilbert measure, ordering and domain | `KEEP_V0_LOCAL_CONSTRAINT_MULTIPLICATION_SPECTRAL_DOMAIN` | On the declared $U_+$ Darboux momentum base, $\widehat C_D=M_c$ has its maximal self-adjoint multiplication domain. |
| 2. Normalize the endpoint transform from $B$ | `KILL_UNIQUENESS_FROM_DECLARED_B_A0_HD_MC_DATA` | The declared $B,a_0,\mathcal H_D,M_c$ data do not choose a unique exact completion. Existence of even one completion remains open. |
| 3. Static pairing versus spectral $\delta(\widehat C_D)$ | `KEEP_V0_LOCAL_STATIC_ZERO_MODE_SPECTRAL_PAIRING_COMPATIBILITY` | The frozen $3\times3$ test form agrees at static and order-zero spectral level, including independent Gaussian-regulator integration. |
| 4. Minimal finite-trajectory extension | `NARROW_V0_M2_RELATIVE_QUARTET_KEEP_ZERO_MODE_COMPLETION_AMBIGUOUS` | One formal local $m=2$ nonzero BFV quartet has the expected relative determinant/Pfaffian identity, but the trajectory zero-mode prescription is not uniquely fixed. |

This is a calculation-workbench result, not a physics result.  Gate 1 remains
`OPEN_PARTIAL_PROGRESS`; global promotion remains `PROHIBITED`.  The exact
endpoint transform, original-variable ordering, physical inner product,
full-real-lapse group average, full BFV trajectory measure, physical cycle,
physics claim and TOE claim all remain null.  No automatic successor was
started.

## 1. Declared local spectral representation

The exact classical chart supplies the canonical pairs

\[
(T,c),\qquad (\Phi,p),
\]

only on

\[
U_+=\{p>0,\ R=3p^2-2P^2>0\}.
\]

The first calculation declares the local momentum-base convention

\[
X_+=\mathbb R_c\times\mathbb R_{+,p},
\qquad
\mathcal H_D=L^2(X_+,dc\,dp),
\]

and defines

\[
(\widehat C_D\psi)(c,p)=c\psi(c,p),
\qquad
D(\widehat C_D)
=\{\psi\in\mathcal H_D:c\psi\in\mathcal H_D\}.
\]

The runner verifies the nonreal resolvent identity and bound

\[
R_z(c)=\frac1{c-z},
\qquad
(c-z)R_z=1,
\qquad
|R_z(c)|\leq\frac1{|\operatorname{Im}z|}.
\]

The maximal real multiplication-operator theorem then gives self-adjointness,
spectrum $\mathbb R$, and the PVM

\[
(E(\Delta)\psi)(c,p)=1_\Delta(c)\psi(c,p).
\]

This has an important distributional boundary:

\[
E(\{0\})=0
\quad\hbox{in Lebesgue }L^2,
\]

whereas on the declared smooth test space the order-zero fiber form is

\[
\eta_0(\psi,\varphi)
=\langle\psi,\delta(\widehat C_D)\varphi\rangle
=\int_0^\infty dp\,
\overline{\psi(0,p)}\varphi(0,p).
\]

Thus $\delta(\widehat C_D)$ is not an ordinary bounded projector. The
measure $dc\,dp$ is a declared local kinematical half-density convention,
not a derived Wheeler--DeWitt or physical measure.

There is also a branch boundary. $U_+$ has $p>0$, while the preceding
reduced $\Phi$-identity check used a separately declared full-$p$ Fourier
integral.  The Abel-regulated positive-half-line kernel has an odd imaginary
part and is not that full-line delta identity.  Nothing here supplies a
self-adjoint $\Phi$ generator at the $p=0$ edge or a $p<0$ branch
completion.

## 2. Why $B$ does not normalize a unique exact transform

The prior principal FIO fixed

\[
K_h^{(0)}(c,p;P,p')
=\delta(p-p')\,(2\pi\hbar)^{-1/2}D^{-1/2}
e^{-iW/\hbar}
\]

at principal order on compact interiors, but its one-term finite-$\hbar$
exact unitarity was already killed by the geometric-mean versus secant coarea
mismatch.

The second calculation asks the narrower uniqueness question.  Conditional on
any exact unitary completion $U_0$ inside the class that fixes only
$B,a_0=D^{-1/2},\mathcal H_D,M_c$, define

\[
V_{\kappa,\hbar}=e^{i\hbar\kappa c},
\qquad
U_\kappa=V_{\kappa,\hbar}U_0.
\]

Then $V_{\kappa,\hbar}$ is exactly unitary, commutes strongly with $M_c$,
and preserves $D(M_c)$. Its kernel factor can be written as

\[
e^{-iW/\hbar}e^{i\hbar\kappa c}
=\exp\!\left[\frac{i}{\hbar}
\left(-W+\hbar^2\kappa c\right)\right].
\]

Consequently the classical $W$, boundary potential $B$, canonical graph
and principal half-density are unchanged, while

\[
a_1\longmapsto a_1+i\kappa c\,a_0.
\]

The family is not merely formal. For the normalized Gaussian $c$-factor
with density

\[
\sqrt{\frac{2\alpha}{\pi}}e^{-2\alpha c^2},
\]

and any normalized $p>0$ factor,

\[
\langle\psi,V_{\kappa,\hbar}\psi\rangle
=e^{-(\hbar\kappa)^2/(8\alpha)},
\]

\[
\|(V_{\kappa,\hbar}-1)\psi\|^2
=2\left[1-e^{-(\hbar\kappa)^2/(8\alpha)}\right]>0.
\]

All three 80-digit frozen quadratures agree with this formula.  However

\[
V_{\kappa,\hbar}(0,p)=1,
\]

so the order-zero $\delta(M_c)$ form cannot select $\kappa$.

The verdict kills uniqueness only in the explicitly declared data class.  An
additional exact observable-intertwining condition, endpoint-domain
condition, full-symbol transport equation or global gluing condition might
restrict this family.  None was supplied.  The calculation neither constructs
nor rules out $U_0$. Here $V_{\kappa,\hbar}$ acts on the full declared
$\mathcal H_D$, while only the principal FIO data are local; the verdict is
therefore restricted to that mixed declared-data class and says nothing about
unsupplied global edge or endpoint-domain conditions.

## 3. Frozen static–spectral comparison

Take

\[
\psi_j(c,p)=e^{-\alpha_jc^2}p^je^{-\beta_jp},
\qquad
(\alpha_0,\alpha_1,\alpha_2)=(1,2,3),
\qquad
(\beta_0,\beta_1,\beta_2)=(1,2,3).
\]

The hash-pinned improved-static source has the bosonic zero-mode phase

\[
\Pi T+Nc
\]

with measures $d\Pi/(2\pi\hbar)$, $dN/(2\pi\hbar)$, and its declared
oriented ghost factor is $+1$. After the $(T,c)$ contraction its frozen form
is

\[
B_{\rm stat}(j,k)
=\int_0^\infty dp\,
\overline{\psi_j(0,p)}\psi_k(0,p)
=\frac{(j+k)!}{(\beta_j+\beta_k)^{j+k+1}}.
\]

The exact matrix is

\[
\begin{pmatrix}
\tfrac12 & \tfrac19 & \tfrac1{32}\\
\tfrac19 & \tfrac1{32} & \tfrac6{625}\\
\tfrac1{32} & \tfrac6{625} & \tfrac1{324}
\end{pmatrix}.
\]

Its leading principal minors are

\[
\frac12,
\qquad
\frac{17}{5184},
\qquad
\frac{15994111}{83980800000000},
\]

so this frozen Gram matrix is positive definite.

Independently, the spectral form gives exactly the same matrix by $c=0$
fiber evaluation.  With

\[
\delta_\epsilon(c)
=\frac{e^{-c^2/(4\epsilon)}}{2\sqrt{\pi\epsilon}},
\]

the regulated entries are

\[
B_\epsilon(j,k)
=\frac{B_{\rm stat}(j,k)}
{\sqrt{1+4\epsilon(\alpha_j+\alpha_k)}}
\longrightarrow B_{\rm stat}(j,k).
\]

Nine independent $p>0$ integrals and 27 independent $c$-regulator
integrals all pass at 80 digits.  Every sampled entry approaches its static
value monotonically.

This agreement checks the normalization of one finite test form.  It does not
establish an arbitrary-state regulator theorem, a physical group average, an
endpoint transform or a two-endpoint BFV kernel.  It also leaves the entire
$\kappa$ family from Section 2 untouched.

## 4. Minimal $m=2$ gauge/ghost trajectory mode

Because an $m=1$ endpoint-vanishing regulator has no nonzero Dirichlet mode,
the smallest nontrivial extension uses

\[
e_0=1,
\qquad
e_c=\sqrt2\cos(\pi s),
\qquad
e_s=\sqrt2\sin(\pi s),
\qquad
\dot e_s=\pi e_c.
\]

These are boundary-sector functions, not one common orthogonal basis:

\[
\|e_0\|=\|e_c\|=\|e_s\|=1,
\qquad
\langle e_0,e_c\rangle
=\langle e_c,e_s\rangle=0,
\qquad
\langle e_0,e_s\rangle=\frac{2\sqrt2}{\pi}.
\]

The runner substitutes the functions directly into the action, so the
nonzero cross-sector overlap is retained rather than hidden by a false common
orthogonality assumption.

The physical pair is frozen as a spectator,

\[
p(s)=p_0>0,
\qquad
\Phi(s)=\Phi_0+s\Delta\Phi,
\]

and the gauge/ghost modes are

\[
T=T_1e_s,\quad
\Pi=\Pi_1e_s,\quad
c_g=g_1e_s,\quad
\bar c=b_1e_s,
\]

\[
c=c_0+c_1e_c,\quad
N=N_0+N_1e_c,\quad
\rho=\rho_0+\rho_1e_c,\quad
\bar\rho=\bar\rho_0+\bar\rho_1e_c.
\]

For $\lambda>0$, the projected even action is

\[
S_{\rm even}^{(2)}
=p_0\Delta\Phi
+\pi c_1T_1-\pi N_1\Pi_1
+\lambda(\Pi_1T_1+N_0c_0+N_1c_1),
\]

and the ordered ghost action is

\[
S_{\rm odd}^{(2)}
=\pi b_1\rho_1+\pi g_1\bar\rho_1
-\lambda(g_1b_1+\rho_0\bar\rho_0+\rho_1\bar\rho_1).
\]

The pinned bracket-derived generator maps project to

\[
sT_1=g_1,
\quad
sN_i=\rho_i,
\quad
sb_1=\Pi_1,
\quad
s\bar\rho_i=c_i,
\]

and square to zero.  The endpoint-vanishing sine sector remains stable.

For rows $(T_1,N_1)$ and columns $(c_1,\Pi_1)$, the bosonic cross matrix is

\[
A=\begin{pmatrix}
\pi & \lambda\\
\lambda & -\pi
\end{pmatrix},
\qquad
\det A=-(\pi^2+\lambda^2).
\]

For odd order $(g_1,b_1,\rho_1,\bar\rho_1)$,

\[
\operatorname{Pf}F=\pi^2+\lambda^2,
\qquad
\det F=(\pi^2+\lambda^2)^2.
\]

This is a relative same-regulator identity only.  It fixes no bosonic contour
phase, absolute Pfaffian orientation or functional measure.

The zero modes expose the remaining obstruction.  The common bosonic Fourier
factor is

\[
\int\frac{dN_0}{2\pi\hbar}
e^{i\lambda N_0c_0/\hbar}
=\delta(\lambda c_0)
=\frac1\lambda\delta(c_0).
\]

If the algebraic $(\rho_0,\bar\rho_0)$ pair is retained with the explicitly
declared oriented extraction $i\hbar[\rho_0\bar\rho_0]$, its factor is
$\lambda$, and the relative product is $1$. If that pair is eliminated
while $N_0$ is still Fourier-integrated, the relative product is
$1/\lambda$. At the frozen samples

\[
\lambda=(1/2,1,2),
\]

the two ledgers give

\[
(1,1,1)
\quad\hbox{versus}\quad
(2,1,1/2).
\]

The preceding static source and historical trajectory conventions do not
select between these ledgers or a retained lapse-modulus prescription.
Therefore the nonzero quartet is retained as a minimal relative control, but
the unique trajectory zero-mode completion and the full BFV measure stay
null.

The nonzero amplitudes here are only formal local tangent variables.  No
finite-amplitude inverse-chart containment was proved, and this hybrid
continuum-spectral mode is not an exact midpoint-difference lattice or a
continuum convergence result.

## 5. Execution and reproducibility

The executed research commands were

```bash
./ice run cpt_temporal_folded_susy/gate1_v0_constraint_spectral_domain
./ice run cpt_temporal_folded_susy/gate1_v0_endpoint_subprincipal_nonuniqueness
./ice run cpt_temporal_folded_susy/gate1_v0_static_spectral_pairing
./ice run cpt_temporal_folded_susy/gate1_v0_bfv_m2_spectral_trajectory
```

Final observed checks:

| Runner | Exact | Numerical | Analytic guards |
|---|---:|---:|---:|
| constraint spectral domain | 8/8 | 0 | 4 |
| endpoint subprincipal nonuniqueness | 10/10 | 3/3 | 5 |
| static spectral pairing | 11/11 | 36/36 | 4 |
| $m=2$ spectral BFV trajectory | 16/16 | 0 | 5 |

Two initial nonpasses are preserved in Git history rather than erased:

- commit `271e8bb` records the first endpoint-family run as `INCONCLUSIVE`
  because a composite SymPy positivity heuristic returned undecided; commit
  `8e72f9e` replaces that heuristic with the exact positive exponent plus
  strict exponential monotonicity;
- commit `a250c89` records the first $m=2$ run as `KILL` because the runner
  incorrectly required $(e_0,e_c,e_s)$ to form one orthonormal basis; commit
  `176d783` records and tests the actual nonzero $e_0$--$e_s$ overlap.

Portable isolated reproduction was then registered and observed:

```bash
./ice repro --only gate1_v0_constraint_spectral_domain
./ice repro --only gate1_v0_endpoint_subprincipal_nonuniqueness
./ice repro --only gate1_v0_static_spectral_pairing
./ice repro --only gate1_v0_bfv_m2_spectral_trajectory
```

All four reported `REPRO`, with zero `NONPORTABLE`, `SUPERSEDED` or
needs-attention cases.  `npm run check` passed strict TypeScript and all 67
Vitest tests.

Final raw result hashes:

| Result | SHA-256 | Payload SHA-256 without self field |
|---|---|---|
| `GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json` | `4447980c687724f6160da35a2e985c59a4619e4aa2a4072b3cd78afbaad15f48` | `4b4b10bee3dfc6f559e0d67cc9e2c7a6360715e1a4ced60f5b1950242c3b78cd` |
| `GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json` | `5be03cf1d9c8796298d5d561fa77506d88b8063409226e837693c001feaaff2f` | `e5520c2b1aa66c233c67a317e4191be2e8eb43f33ff75886ce7bd079259a7887` |
| `GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT.json` | `0b2c748bb99a11409b820796941538dd926f82eb04198e217a9c3ba780f2a7b4` | `820ce5fd01c1655a6e38c18e529be5f495e61f11490582a0cee84b491c0516b6` |
| `GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT.json` | `15beb4c1bd44d0d7aa8f34b7ea2f656c42452130b10817585b7a6c134ac4aef7` | `a12b719f2961363610c93ecf07d0185de316497708b809b4b2b1aca7bdfec92b` |

## 6. Source boundary and remaining obstruction

Primary framework sources:

- M. Henneaux, C. Teitelboim, and J. D. Vergara,
  [*Gauge invariance for generally covariant systems*](https://arxiv.org/abs/hep-th/9205092),
  Nucl. Phys. B 387 (1992) 391--418.
- J. A. García, J. D. Vergara, and L. F. Urrutia,
  [*BRST--BFV quantization and the Schwinger action principle*](https://arxiv.org/abs/hep-th/9511092),
  Int. J. Mod. Phys. A 11 (1996) 2689--2706.
- D. Marolf,
  [*Refined Algebraic Quantization: Systems with a single constraint*](https://arxiv.org/abs/gr-qc/9508015).
- D. Giulini,
  [*Group Averaging and Refined Algebraic Quantization*](https://arxiv.org/abs/gr-qc/0003040).
- L. Hörmander,
  [*Fourier integral operators. I*](https://doi.org/10.1007/BF02392052),
  Acta Math. 127 (1971) 79--183.

These sources delimit endpoint improvement, BFV and spectral/FIO frameworks.
They do not derive the repository's $V=0$ Darboux chart, select the local
measure, normalize the finite ghost ledgers or turn these controls into a
physical cosmology.

The sharp remaining blockers are now explicit:

1. an exact endpoint completion needs additional full-symbol or exact
   intertwining/domain data; $B$ and the principal half-density are
   insufficient;
2. the $p=0$ edge and the missing $p<0$ component prevent interpreting the
   prior full-$p$ $\Phi$ identity as an $U_+$ spectral identity;
3. a finite BFV trajectory needs a uniquely justified zero-mode/lapse-modulus
   prescription, an absolute contour/orientation and certified
   finite-amplitude chart containment;
4. none of the local results supplies a global atlas, Gribov census, physical
   original cycle, physical inner product or observable.

Accordingly this sequence is real local workbench progress, but it does not
materially raise the earlier user-level, non-posterior assessment that a
TOE-level claim remains well below one percent.
