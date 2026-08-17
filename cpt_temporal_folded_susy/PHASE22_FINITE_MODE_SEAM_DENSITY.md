# Phase 22 — finite-mode CPT-like seam density control

## Outcome

This phase asks a deliberately smaller question than the full supergravity
seam problem.  For one positive-frequency supersymmetric oscillator, can a
two-sheet Euclidean preparation define a normalized positive density matrix,
respect the fixed-mode supersymmetry algebra, and satisfy the elementary
closed-time-path normalization identity?

The answer is yes for

\[
\omega>0,\qquad \beta>0.
\]

The exact state is a thermofield-double-like purification of a supersymmetric
oscillator.  It
has unit norm, a positive rank-one density matrix, a normalized Gibbs reduced
state, a CPT-like graded sheet involution, finite cross-sheet covariance, and
the unitary Schwinger--Keldysh normalization

\[
Z_{\rm SK}[J,J]=1.
\]

The same construction fails at \(\omega=0\).  The fermion factor stays finite,
but the bosonic partition sum and covariance diverge.  Equivalently,
\(e^{-\beta p^2/2}\) is not trace class on \(L^2(\mathbb R)\), so the free,
unregulated noncompact Gaussian mode has no normalizable limit.  This is a
precise obstruction for this ansatz, not a no-go for a compact zero mode or
the interacting inflaton zero mode: the latter must be treated in constrained
minisuperspace with its potential, measure, and collective-coordinate or
higher-order terms.

This calculation is **not** a full CPT/Pin \(4d\;N=1\) supergravity state.  It
does not construct a Clifford/Pin lift, a gravitino--Goldstino--ghost kernel,
BRST cohomology, the physical Wheeler--DeWitt projector, or a measure over
flux and inflaton initial data.

Executable:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py
```

The executable records 31 exact checks and no floating-point fit, including
Hermiticity, unit trace, rank-one idempotence, and an explicit partial trace.

## 1. One-side supersymmetric oscillator

Let \(a,a^\dagger\) be a bosonic oscillator and \(f,f^\dagger\) one CAR mode.
With

\[
N_B=a^\dagger a,\qquad N_F=f^\dagger f,
\]

define

\[
H=\omega(N_B+N_F),\qquad
Q=\sqrt{2\omega}\,a^\dagger f,\qquad
Q^\dagger=\sqrt{2\omega}\,a f^\dagger .
\tag{E220}
\]

Then

\[
Q^2=(Q^\dagger)^2=0,\qquad
\{Q,Q^\dagger\}=2H,\qquad [H,Q]=0,
\]

and \(Q\) is odd under \((-1)^F\).  At every positive energy
\(E_m=m\omega\), \(m\ge1\), the states

\[
|m,0\rangle,\qquad |m-1,1\rangle
\]

form a degenerate boson--fermion doublet.  This is a \(0+1\)-dimensional
fixed-harmonic control, not a new spacetime superalgebra.

## 2. Exact two-sheet state

Set

\[
r=e^{-\beta\omega},\qquad 0<r<1.
\]

For sheets \(+\) and \(-\), take the bosonic purification

\[
|\Psi_B\rangle
=\sqrt{1-r}\sum_{n=0}^{\infty}r^{n/2}|n\rangle_+|n\rangle_-
\]

and the fermionic pair

\[
|\Psi_F\rangle
=\frac{|00\rangle+i\sqrt r\,|11\rangle}{\sqrt{1+r}}.
\]

The full state is

\[
\boxed{
|\Psi_\Sigma\rangle
=\sqrt{\frac{1-r}{1+r}}
\sum_{n=0}^{\infty}r^{n/2}|n,n\rangle_B
\otimes\left(|00\rangle+i\sqrt r\,|11\rangle\right)_F .
}
\tag{E221}
\]

Both geometric sums are exact, so

\[
\langle\Psi_\Sigma|\Psi_\Sigma\rangle=1,
\qquad
\rho_\Sigma=|\Psi_\Sigma\rangle\langle\Psi_\Sigma|,
\]

\[
\rho_\Sigma^\dagger=\rho_\Sigma,\qquad
\rho_\Sigma\ge0,\qquad
\operatorname{Tr}\rho_\Sigma=1,\qquad
\rho_\Sigma^2=\rho_\Sigma.
\]

Tracing out the minus sheet gives

\[
\boxed{
\rho_+
=\frac{1}{Z}\,e^{-\beta H},
\qquad
Z=\frac{1+r}{1-r}.
}
\tag{E222}
\]

Equivalently,

\[
\rho_B=(1-r)\sum_{n\ge0}r^n|n\rangle\langle n|,
\qquad
\rho_F=\frac{|0\rangle\langle0|+r|1\rangle\langle1|}{1+r}.
\]

Because \(Q\) preserves \(N_B+N_F\),

\[
[\rho_+,Q]=[\rho_+,Q^\dagger]=0.
\]

This algebraic commutation and equal weighting inside each positive-energy
supermultiplet must not be promoted to an unbroken physical thermal
supersymmetry claim.  Indeed,

\[
\operatorname{Tr}(\rho_+H)
=\frac{2\omega r}{1-r^2}>0
\qquad(0<r<1),
\]

so the finite-temperature purification is not a zero-energy vacuum of the
original positive Hamiltonian \(H_++H_-\).  Thermal/GNS supersymmetry has
additional domain and generator obstructions; see
[Buchholz and Ojima](https://arxiv.org/abs/hep-th/9701005).

## 3. CPT-like graded sheet involution

On the doubled fermion basis \((|00\rangle,|01\rangle,|10\rangle,|11\rangle)\),
let the graded swap be

\[
S_g|ab\rangle=(-1)^{ab}|ba\rangle.
\]

Let \(S_B\) exchange the two bosonic occupation factors and define the
anti-linear toy involution on the full occupation basis by

\[
\Theta_{\rm toy}=(S_B\otimes S_g)K,
\]

where \(K\) complex-conjugates coefficients in this basis.  The phase \(i\)
in E221 compensates the minus sign from exchanging two occupied fermionic
states, giving

\[
\Theta_{\rm toy}|\Psi_F\rangle=|\Psi_F\rangle,
\qquad
\Theta_{\rm toy}^2=1,
\qquad
[\Theta_{\rm toy},(-1)^{F_++F_-}]=0,
\qquad
\Theta_{\rm toy}H_{\rm tot}\Theta_{\rm toy}^{-1}=H_{\rm tot}.
\tag{E223}
\]

The bosonic factor is real and sheet symmetric, so the product is invariant.
The compensating phase is tied to the displayed graded tensor-ordering
convention.
This is only an exact doubled-oscillator real structure.  A physical Pin lift
also needs the spacetime Clifford action, reflection square, spin structure,
and local-SUGRA boundary transformation law, all of which remain open as in
Phase 17.

## 4. Correlations and the Euclidean bridge

For

\[
x=\frac{a+a^\dagger}{\sqrt{2\omega}},
\]

the state E221 gives

\[
\langle x_+^2\rangle
=\frac{1+r}{2\omega(1-r)}
=\frac{1}{2\omega}\coth\frac{\beta\omega}{2},
\]

\[
\boxed{
\langle x_+x_-\rangle
=\frac{\sqrt r}{\omega(1-r)}
=\frac{1}{2\omega\sinh(\beta\omega/2)} .
}
\tag{E224}
\]

The normalized correlation coefficient is

\[
\boxed{
\rho_x
=\frac{2\sqrt r}{1+r}
=\operatorname{sech}\frac{\beta\omega}{2}.
}
\tag{E225}
\]

Thus the bosonic factor is the normalized vectorization of the finite-interval
Dirichlet-to-Neumann amplitude with interval length \(L=\beta/2\).  The full
state additionally contains the displayed convention-dependent fermion
phase; that phase has not been derived from a Euclidean Pin/fermion kernel.
If the bosonic amplitude is \(\exp(-q^T K_Lq/2)\), its density is
\(\exp(-q^T K_Lq)\), so the covariance used in E224 is
\((2K_L)^{-1}\), not \(K_L^{-1}\).  In particular,

\[
(K_L^{-1})_{+-}=\frac{1}{\omega\sinh(\omega L)},
\qquad
\langle x_+x_-\rangle_{|\Psi|^2}
=\frac12(K_L^{-1})_{+-}.
\]

The normalized coefficient E225 is unchanged.  The construction derives a
finite cross-sheet correlation once \(\beta\) and \(\omega\) are supplied; it
does not select either one.

## 5. Closed-time-path normalization

For any unitary source evolution \(U[J]\) on the plus-sheet Hilbert space,

\[
Z_{\rm SK}[J,J]
=\operatorname{Tr}\!\left(U[J]\rho_+U[J]^\dagger\right)
=\operatorname{Tr}\rho_+=1.
\tag{E226}
\]

The executable includes an exact finite CAR rotation and a wrong-adjoint
negative control.  This is the elementary unitarity identity only.  It does
not construct the Schwinger--Keldysh ghost quartet or BRST algebra discussed
by [Haehl, Loganayagam, and Rangamani](https://arxiv.org/abs/1610.01940).

## 6. The homogeneous zero-mode obstruction

At fixed \(\beta>0\),

\[
Z_B=\frac{1}{1-e^{-\beta\omega}}
\sim\frac{1}{\beta\omega}
\qquad(\omega\to0^+),
\]

whereas \(Z_F=1+e^{-\beta\omega}\to2\).  Hence the obstruction is bosonic:

\[
\operatorname{Tr}_{\mathcal F_B}e^{-\beta H_B}\to\infty.
\]

The coordinate covariance diverges more strongly,

\[
\langle x^2\rangle
=\frac{1}{2\omega}\coth\frac{\beta\omega}{2}
\sim\frac{1}{\beta\omega^2},
\]

and the corresponding diagonal Gaussian stiffness vanishes,

\[
\Omega_{\rm diag}
=\omega\tanh\frac{\beta\omega}{2}
\sim\frac{\beta\omega^2}{2}\longrightarrow0.
\tag{E227}
\]

Therefore E221 has no normalizable \(\omega=0\) limit in the original bosonic
Fock representation.  This does **not** establish that the homogeneous
inflaton cannot be normalized.  Its potential and gravitational constraint
remove it from the free test-oscillator problem, and a genuine collective
coordinate requires a primed determinant, measure/Jacobian, and generally
non-Gaussian minisuperspace wavefunction.

## 7. Bounded verdict

| Question | Exact result | Scope |
|---|---|---|
| Positive-frequency two-sheet state | normalized positive purification exists | one free SUSY oscillator, \(\omega,\beta>0\) |
| Reduced state | exact Gibbs density matrix | no physical-projector or WDW measure |
| Fixed-mode SUSY algebra | closes; Gibbs weights match inside each doublet | not unbroken thermal or local SUSY |
| CPT/Pin | graded anti-linear toy involution exists | no spacetime Clifford/Pin lift |
| Cross-sheet correlation | E224--E225 finite | \(\beta\) and \(\omega\) remain inputs |
| SK identity | \(Z[J,J]=1\) | unitarity control, not SK BRST construction |
| Free \(\omega=0\) boson | not trace class; covariance diverges | noncompact \(L^2(\mathbb R)\) oscillator limit; does not decide a compact or interacting inflaton zero mode |
| Unique universe state | not computed | flux, \(\phi_0\), contour, and physical projector open |

Thermofield doubling and its connection to KMS states are standard; see
[Ojima](https://doi.org/10.1016/0003-4916(81)90058-0) and the black-hole
purification construction of
[Israel](https://doi.org/10.1016/0375-9601(76)90178-X).  These sources motivate
the doubled-state control but do not identify its two factors with literal
temporal universes or derive a cosmological seam.

## 8. Next direct calculation

The next non-arbitrary gate is now sharply separated into two pieces.

1. Treat the homogeneous \((a,\phi)\) sector as constrained minisuperspace,
   including its on-shell complex-cap action, zero-mode Jacobian, and physical
   WDW current rather than inserting \(\omega=0\) into E221.
2. On the same cap, calculate the gauge-fixed coupled
   gravitino--Goldstino--ghost boundary operator and Pfaffian phase, then test
   whether the physical projector makes the full seam density matrix positive
   and trace class.

Only after these pass should membrane-induced flux transfer be added and a
joint distribution in \((n,\phi)\) be tested for a cutoff-independent interior
peak.
