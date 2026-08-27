# Gate 1 — one densitized \(V=0\) quantum-cosmology derivation

## Outcome

Two separate bounded, non-numbered calculations establish the following
workbench result.

1. After the explicit classical rescaling

   \[
   H=12\pi^2e^{3Q/2}C,
   \]

   the flat Schrödinger ordering of \(H\) is exactly diagonalized on the
   \(p>0\) sector by a Fourier--Kontorovich--Lebedev transform. Its selected
   group average has the positive physical fiber

   \[
   \boxed{
   \mathcal H_{\rm phys}^{(H,+)}
   =L^2\!\left((0,\infty),\frac{dp}{2\sqrt6\,\hbar p}\right)
   }.
   \]

2. In the pinned algebraic BFV zero block, direct Berezin integration and
   correct ghost elimination agree. Eliminating the ghost pair requires its
   induced oriented factor \(\lambda\); deleting the pair without that factor
   fails the local gauge-fermion scaling Ward check.

The frozen verdicts are

```text
KEEP_V0_ONE_DENSITIZED_LIOUVILLE_KL_RAQ_MODEL
NARROW_V0_BFV_ZERO_GHOST_ELIMINATION_REQUIRES_INDUCED_DETERMINANT
```

This is a concrete, exactly solvable **constrained quantum-cosmology model**.
It is not the quantization of undensitized \(C\), is not proven equivalent to
the preceding declared \(M_c\) representation, and is not quantum gravity,
physics, or a TOE result. Gate 1 remains `OPEN_PARTIAL_PROGRESS`, global
promotion remains `PROHIBITED`, and no automatic successor was started.

## 1. Source and convention boundary

The special-function input is the modified-Bessel equation and the
Kontorovich--Lebedev transform pair in NIST DLMF
[§10.25(i)](https://dlmf.nist.gov/10.25.i) and
[§10.43(v)](https://dlmf.nist.gov/10.43.v). The single-constraint rigging-map
interpretation follows the framework of
[Marolf](https://arxiv.org/abs/gr-qc/9508015) and
[Giulini](https://arxiv.org/abs/gr-qc/0003040). Their work does not select the
model-specific constraint, ordering, branch, or measure below.

The field-dependent rescaling boundary is material. Classically equivalent
constraint rescalings can lead to quantum-domain and quantization differences;
the calculation therefore follows the warning analyzed by
[Louko and Martinez-Pascual](https://arxiv.org/abs/1107.1092) and makes no
raw-\(C\)/\(H\) equivalence claim.

The zero-mode action and bracket convention are hash-pinned by the preceding
local BFV calculations. The BFV scope follows
[Henneaux--Teitelboim--Vergara](https://arxiv.org/abs/hep-th/9205092) and
[Garcia--Vergara--Urrutia](https://arxiv.org/abs/hep-th/9511092), but those
sources do not choose the finite orientation or a gravitational lapse contour.

## 2. Exact classical densitization

Use the original homogeneous variables

\[
Q=2\log a,\qquad
P=\frac{ap_a}{2},\qquad
\{Q,P\}=\{\phi,p\}=1.
\]

For the closed-FRW \(V=0\) model, the classical constraint is

\[
C=
-\frac{e^{-3Q/2}P^2}{6\pi^2}
+\frac{e^{-3Q/2}p^2}{4\pi^2}
-6\pi^2e^{Q/2}.
\]

The calculation makes an additional declared choice: multiply \(C\) by the
strictly positive function \(12\pi^2e^{3Q/2}\). Exact simplification gives

\[
\boxed{
H=12\pi^2e^{3Q/2}C
=-2P^2+3p^2-72\pi^4e^{2Q}.
}
\]

This preserves the classical zero set and gauge orbits up to
reparametrization, but it does not automatically preserve a quantum operator,
domain, group-average normalization, or physical inner product. All results
below therefore carry the label \(H\), not raw \(C\).

## 3. Declared ordering and exact spectral reduction

Declare

\[
\mathcal H_{\rm aux}=L^2(\mathbb R_Q\times\mathbb R_\phi,dQ\,d\phi),
\qquad
P=-i\hbar\partial_Q,\qquad p=-i\hbar\partial_\phi,
\]

and apply the flat Schrödinger ordering to the already densitized polynomial:

\[
\boxed{
\widehat H
=2\hbar^2\partial_Q^2
-3\hbar^2\partial_\phi^2
-72\pi^4e^{2Q}.
}
\]

Fourier transform \(\phi\) with

\[
\psi(Q,\phi)
=(2\pi\hbar)^{-1/2}
\int_{\mathbb R}e^{ip\phi/\hbar}\widetilde\psi(Q,p)\,dp
\]

and retain the invariant \(p>0\) component. At fixed \(p\), set

\[
z=\frac{6\pi^2}{\hbar}e^Q,\qquad
dQ=\frac{dz}{z},\qquad
L=-\partial_Q^2+z^2.
\]

Since \(72\pi^4e^{2Q}=2\hbar^2z^2\),

\[
\widehat H_p=-2\hbar^2L+3p^2.
\]

The modified-Bessel equation at order \(\nu=i\kappa\) is

\[
z^2K''_{i\kappa}+zK'_{i\kappa}
-(z^2-\kappa^2)K_{i\kappa}=0,
\]

and therefore

\[
LK_{i\kappa}(z)=\kappa^2K_{i\kappa}(z).
\]

With

\[
\chi_\kappa(z)
=\frac{\sqrt{2\kappa\sinh(\pi\kappa)}}{\pi}K_{i\kappa}(z),
\]

the Kontorovich--Lebedev transform selects a unitary spectral realization of
\(L\) from \(L^2(dQ)=L^2(dz/z)\) to \(L^2(d\kappa)\). Together with the
\(\hbar\)-Fourier transform, the selected densitized constraint is the maximal
real multiplication operator

\[
\boxed{h(\kappa,p)=3p^2-2\hbar^2\kappa^2}
\]

on \(L^2(\mathbb R_{+,\kappa}\times\mathbb R_{+,p},d\kappa\,dp)\), with

\[
D(\widehat H)=\{A\in L^2:hA\in L^2\}.
\]

Self-adjointness here is by this explicitly selected Fourier--KL spectral
definition. It is not a claim that an undensitized Wheeler--DeWitt
differential expression has been ordered or globally completed.

## 4. Rigging map and physical measure

On smooth spectral tests compactly supported inside \(\kappa>0,p>0\), use

\[
\eta_H(A)[B]
=\int_{\mathbb R}\frac{dN}{2\pi\hbar}
\langle A,e^{-iN\widehat H/\hbar}B\rangle.
\]

The Fourier distribution gives

\[
\eta_H(A)[B]
=\int_0^\infty dp\int_0^\infty d\kappa\,
\delta(3p^2-2\hbar^2\kappa^2)
\overline{A(\kappa,p)}B(\kappa,p).
\]

For \(p>0\), there is one simple positive zero,

\[
\kappa_0(p)=\sqrt{\frac32}\frac p\hbar,
\]

and

\[
\left|\partial_\kappa h\right|_{\kappa_0}
=4\hbar^2\kappa_0
=2\sqrt6\,\hbar p.
\]

Hence

\[
\boxed{
\eta_H(A)[B]
=\int_0^\infty\frac{dp}{2\sqrt6\,\hbar p}\,
\overline{A(\kappa_0(p),p)}B(\kappa_0(p),p).
}
\]

The null space consists of tests whose restriction to
\(\kappa=\kappa_0(p)\) vanishes. Quotienting and completing gives

\[
\mathcal H_{\rm phys}^{(H,+)}
=L^2\!\left((0,\infty),\frac{dp}{2\sqrt6\,\hbar p}\right).
\]

The exact witnesses \(A_1(p)=pe^{-p}\) and \(A_2(p)=p^2e^{-p}\) have

\[
\|A_1\|^2=\frac1{8\sqrt6\,\hbar},\qquad
\|A_2\|^2=\frac3{16\sqrt6\,\hbar}.
\]

At \(p=0\), the zero ceases to be simple and the weight diverges. The runner
does not extend the result across that edge.

## 5. Comparison with the declared \(M_c\) fiber

The earlier local Darboux representation declared

\[
\eta_{M_c}(\psi,\varphi)
=\int_0^\infty dp\,\overline{\psi(0,p)}\varphi(0,p).
\]

The new derived \(H\)-measure contains \(1/(2\sqrt6\hbar p)\). Two exact
witness ratios show that the identity map cannot identify the two forms up to
one constant normalization. There is an abstract isometry

\[
(JA)(p)=\frac{A(p)}{\sqrt{2\sqrt6\,\hbar p}}
\]

from the weighted space to \(L^2(dp)\). But that reweighting is not the
missing endpoint transform from \((Q,\phi)\) to \((c,p)\), and it does not
intertwine raw \(C\), selected \(H\), and \(M_c\). Thus:

- one selected \(H\)-physical Hilbert space is now computed;
- the raw-\(C\) operator and physical inner product remain null;
- quantum constraint-rescaling equivalence remains null;
- exact identity with the declared \(M_c\) model remains null.

## 6. BFV zero-mode ledger repair

The pinned algebraic zero block is

\[
S_0(\lambda)
=\lambda(N_0c_0-\rho_0\bar\rho_0),\qquad \lambda>0.
\]

Under the inherited right-acting bracket convention,

\[
sN_0=\rho_0,\qquad
s\bar\rho_0=c_0,\qquad
s\rho_0=sc_0=0,
\]

so the generator images are nilpotent and

\[
s(N_0c_0)=s(\rho_0\bar\rho_0)=\rho_0c_0,\qquad sS_0=0.
\]

The full-real \(N_0\) integral supplies

\[
\int_{\mathbb R}\frac{dN_0}{2\pi\hbar}e^{i\lambda N_0c_0/\hbar}
=\delta(\lambda c_0)=\frac{\delta(c_0)}{\lambda}.
\]

For the ordered odd pair \((\rho_0,\bar\rho_0)\),

\[
e^{-i\lambda\rho_0\bar\rho_0/\hbar}
=1-\frac{i\lambda}{\hbar}\rho_0\bar\rho_0.
\]

The pinned extraction \(i\hbar[\rho_0\bar\rho_0]\) gives

\[
i\hbar\left(-\frac{i\lambda}{\hbar}\right)=\lambda.
\]

The action Hessian is

\[
F=\begin{pmatrix}0&-\lambda\\ \lambda&0\end{pmatrix},
\qquad
\det F=\lambda^2,\qquad
\operatorname{Pf}F=-\lambda.
\]

Its stationary equations set \(\rho_0=\bar\rho_0=0\), but correct Gaussian
elimination retains the oriented factor \(\lambda\). The ledgers are:

| route | ghost factor | coefficient of \(\delta(c_0)\) |
|---|---:|---:|
| direct Berezin integration | \(\lambda\) | \(1\) |
| weighted algebraic elimination | \(\lambda\) | \(1\) |
| unweighted deletion | \(1\) | \(1/\lambda\) |

Consequently

\[
\partial_\lambda Z_0^{\rm direct}
=\partial_\lambda Z_0^{\rm weighted}=0,\qquad
\partial_\lambda Z_0^{\rm delete}=-\lambda^{-2}.
\]

At \(\lambda=1/2,1,2\), both correct routes give \(1,1,1\), while the
negative control gives \(2,1,1/2\). The previous retained-versus-eliminated
mismatch is therefore an omitted odd Gaussian factor. Unweighted deletion is
killed as a ghost-elimination prescription.

This does **not** select whether \(N_0\) should be integrated over the full
real line, treated as a modulus, or placed on another gravitational contour.
The unique trajectory zero-mode completion remains null.

## 7. Scientific status

### Computed facts

- A specifically densitized and ordered homogeneous constraint has an exact
  Fourier--KL self-adjoint spectral realization.
- Its \(p>0\) zero shell gives the positive measure
  \(dp/(2\sqrt6\hbar p)\), away from the singular edge.
- The weighted physical fiber is not the prior declared \(dp\) fiber under
  identity normalization, though an explicit abstract isometry exists.
- Correct BFV ghost elimination agrees with direct Berezin integration; the
  former ledger mismatch came from dropping the induced \(\lambda\) factor.

### Interpretation

This advances the chain from a purely declared \(M_c\) spectral fiber to one
solvable **minisuperspace constraint quantization** with a derived measure.

### Still open

- an ordering and self-adjoint domain for undensitized raw \(C\);
- equivalence of raw \(C\), densitized \(H\), and Darboux \(M_c\);
- the \(p=0\) edge, \(p<0\) branch, and a global chart/domain;
- the gravitational lapse contour/modulus and zero-lapse contact terms;
- a continuum/full BFV operator, absolute Pfaffian line, anomalies, and BRST
  cohomology;
- inhomogeneous metric modes, the local GR constraint algebra, gravitons,
  renormalization, semiclassical Einstein dynamics, observables, and tests.

Because the last line is absent, this result does not yet explain quantum
gravity. It establishes one exact quantum-cosmology laboratory in which the
next genuinely gravitational obstruction can be stated precisely.

## 8. Execution and reproduction

Committed executions:

```text
./ice run gate1_v0_densitized_liouville_raq
./ice run gate1_v0_bfv_zero_mode_elimination_ward
```

Observed:

```text
VALID_RUN; 14/14 exact checks; 5 theorem guards;
KEEP_V0_ONE_DENSITIZED_LIOUVILLE_KL_RAQ_MODEL

VALID_RUN; 14/14 exact checks; 6 theorem guards;
NARROW_V0_BFV_ZERO_GHOST_ELIMINATION_REQUIRES_INDUCED_DETERMINANT
```

Both isolated commands

```text
./ice repro --only gate1_v0_densitized_liouville_raq
./ice repro --only gate1_v0_bfv_zero_mode_elimination_ward
```

reported `REPRO` with zero needs-attention cases. `npm run check` passed
strict TypeScript checking and all 67 tests.

| Calculation | Runner SHA-256 | Input SHA-256 | Result payload SHA-256 |
|---|---|---|---|
| densitized Liouville/KL/RAQ | `b5e346ec2992e860ccf99ef0ec7d06e9f4cac2667137714bb32fbe1f647c18f2` | `92f340a331fb38590d64ac2c1e273dd7b17b7f7b1c91b0f2e05c8db58d1d55cd` | `32c4cf7ae925d3fbbbba21d5e0e4466abdd80043e39db8312941c9548b346869` |
| BFV zero-mode elimination/Ward | `8462ccb52cbfc3ba588a6182e4e288f645d4524b0fbefbd016fd08f3d83b5c6a` | `912492397b0488562eacce1b37d8998faf73ad0c6b30d716fc3e8da98d99ecdd` | `22c8423c347084eb07e8167bb38101ab50a74cc3335b5d3f471099a1f54f0a6b` |

Raw results:

- [densitized Liouville/KL/RAQ result](GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT.json)
- [BFV zero-mode elimination/Ward result](GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT.json)

