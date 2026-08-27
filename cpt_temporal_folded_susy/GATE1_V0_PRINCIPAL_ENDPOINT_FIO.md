# Gate 1 — closed-FRW \(V=0\) local principal endpoint FIO

## Outcome

The preceding result supplied an exact **classical** Darboux chart on

\[
\mathcal U_+
=\{(Q,P,\phi,p):p>0,\ 3p^2-2P^2>0\}.
\]

This bounded follow-up determines the first quantum object that the kept
mixed generator actually supports.  On a smooth compact cutoff strictly
inside \(\mathcal U_+\) and its chart image, the old momentum polarization
\((P,p)\) and new momentum polarization \((c,p)\) are related at principal
semiclassical order by

\[
\boxed{
K_\hbar(c,p;P,p')
=\delta(p-p')\,
\frac{D(c,P,p)^{-1/2}}{\sqrt{2\pi\hbar}}
\exp\!\left[-\frac{i}{\hbar}W(c,P,p)\right]
}
\]

with

\[
W_{cP}=\frac1D>0.
\]

The phase sign, canonical relation, principal half-density, local Maslov
branch, endpoint boundary phase and \(c=0\) lineage all pass.  The corresponding
verdict is therefore

```text
KEEP_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO
```

The same calculation also gives a strict negative result.  The displayed
one-term Van Vleck kernel is **not** an exactly unitary finite-\(\hbar\)
transform.  In the adjoint composition its endpoint geometric-mean density
does not equal the secant/coarea density required for an exact delta kernel.
The second verdict is

```text
KILL_ONE_TERM_EXACT_UNITARITY
```

This KILL applies only to the uncorrected one-term amplitude.  It does not
exclude an \(\hbar\)-dependent full symbol or a separately constructed
spectral transform after ordering, domains and edge conditions have been
specified.

The combined frozen terminal row is

```text
KEEP_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO_KILL_ONE_TERM_EXACT_UNITARITY
```

Gate 1 remains `OPEN_PARTIAL_PROGRESS`.  A globally normalized endpoint
transform, BFV source, full-real-lapse \(\delta(C)\) rigging distribution,
old fixed-\(a\) kernel equivalence, physical cycle, physics claim and TOE all
remain uncomputed.  `automatic_next=null`.

## 1. Source and interpretation boundary

Henneaux–Teitelboim–Vergara require endpoint canonical variables, boundary
terms and endpoint state representations to be transformed consistently.
Their framework does not derive the repository generator or normalize the
kernel below.

García–Vergara–Urrutia show why a BFV endpoint construction additionally
needs multiplier, ghost, antighost, BRST-charge, gauge-fermion and fermionic
boundary data.  None of those data is supplied by this bosonic FIO.

Van Vleck supplies the semiclassical determinant-amplitude context, and
Hörmander supplies the local microlocal canonical-relation interpretation.
Neither source makes the displayed nonlinear one-term kernel exactly unitary.

Marolf supplies the distinct comparison target obtained from a full-real-lapse
constraint average.  Here \(c\) is a new endpoint momentum coordinate; it is
not itself \(\delta(C)\), and no continuous-spectrum delta is treated as a
bounded Hilbert-space projector.

Primary sources:

- M. Henneaux, C. Teitelboim, and J. D. Vergara,
  [*Gauge invariance for generally covariant systems*](https://arxiv.org/abs/hep-th/9205092),
  Nucl. Phys. B 387 (1992) 391–418.
- J. A. García, J. D. Vergara, and L. F. Urrutia,
  [*BRST–BFV quantization and Schwinger's action principle*](https://arxiv.org/abs/hep-th/9511092),
  Phys. Rev. D 53 (1996) 1368–1377.
- D. Marolf,
  [*Path integrals and instantons in quantum gravity: Minisuperspace models*](https://arxiv.org/abs/gr-qc/9602019),
  Phys. Rev. D 53 (1996) 6979–6990.
- J. H. Van Vleck,
  [*The Correspondence Principle in the Statistical Interpretation of Quantum Mechanics*](https://doi.org/10.1073/pnas.14.2.178),
  PNAS 14 (1928) 178–188.
- L. Hörmander,
  [*Fourier integral operators. I*](https://doi.org/10.1007/BF02392052),
  Acta Math. 127 (1971) 79–183.

These references bound the interpretation.  All model-specific equations and
checks below are repository calculations.

## 2. Polarization and phase

The classical generator obeys

\[
dW=T\,dc-Q\,dP+(\Phi-\phi)\,dp.
\]

It directly connects **momentum** polarizations, not the coordinate bases
\((Q,\phi)\) and \((T,\Phi)\).  With

\[
(U_\hbar\psi)(c,p)=\int dP\,dp'\,
K_\hbar(c,p;P,p')\psi(P,p'),
\]

the phase is

\[
S(c,P,p)=-W(c,P,p).
\]

This sign gives

\[
S_c=-T,
\qquad
S_P=Q.
\]

Consequently \(i\hbar\partial_c\) on the output and integration by parts
against \(i\hbar\partial_P\) on the input recover \(T\) and \(Q\) at principal
order.  Derivatives of the amplitude are explicit subprincipal terms; they
are not silently dropped from an exact intertwining claim.

An equivalent endpoint phase ledger is

\[
\Psi
=cT+p(\Phi-\phi)-PQ-W(c,P,p).
\]

Its critical equations are

\[
T=W_c,
\qquad
Q=-W_P,
\qquad
\Phi-\phi=W_p,
\]

and its critical value is

\[
\Psi_{\rm crit}
=cT+pW_p-PQ-W
=-B.
\]

Thus the phase recovers the previously kept classical boundary potential
without identifying this principal kernel with the older fixed-\(a\) kernel.

## 3. Principal half-density and local Maslov branch

The mixed twist Hessian is

\[
S_{cP}=-W_{cP}=-\frac1D,
\qquad
D>0\quad\text{on }\mathcal U_+.
\]

In the declared Lebesgue momentum convention, the principal determinant
factor is therefore

\[
a_0=|S_{cP}|^{1/2}=D^{-1/2}.
\]

It is not \(D\), \(\sqrt D\), or the physical Wheeler–DeWitt endpoint
measure.  Since \(W_{cP}\) never vanishes or changes sign inside the declared
component, a compact interior cutoff has no mixed-projection caustic and one
local Maslov branch may be held fixed.  This is not a global Maslov-bundle or
determinant-line orientation result.

Standard principal FIO composition then gives microlocal identity symbol on
the canonical graph.  The precise statement retained here is principal-order
microlocal unitarity, not equality of bounded operators at finite \(\hbar\).

## 4. Exact \(c=0\) lineage

Writing

\[
R=3p^2-2P^2,
\qquad
Q_0=\frac12\log\!\left(\frac{R}{72\pi^4}\right),
\]

the normalized shell generator is

\[
W_0
=-P Q_0+P
-\sqrt{\frac32}\,p\,
\operatorname{artanh}\!\left(\sqrt{\frac23}\frac Pp\right).
\]

Exact differentiation gives

\[
(W_0)_P=-Q_0,
\qquad
(W_0)_p
=-\sqrt{\frac32}\,
\operatorname{artanh}\!\left(\sqrt{\frac23}\frac Pp\right)
=\Phi_*-\phi.
\]

The quantum phase therefore preserves the exact classical shell lineage.  It
does not make \(c=0\) a normalizable physical state.

## 5. Why the one-term kernel is not exactly unitary

Let

\[
M(c,P,p)=W_{cP}=\frac1D
\]

and compare two input momenta

\[
P_\pm=\bar P\pm\frac{\delta P}{2}.
\]

In \(U_\hbar^*U_\hbar\), the phase difference satisfies

\[
\partial_c
\frac{W(c,P_+,p)-W(c,P_-,p)}{\delta P}
=M_{\rm sec},
\]

where

\[
M_{\rm sec}
=\frac{T(c,P_+,p)-T(c,P_-,p)}{\delta P}
=\frac1{\delta P}\int_{P_-}^{P_+}M(c,u,p)\,du.
\]

This is the coarea density that changes the composition integral to the exact
Fourier delta normalization.  The one-term endpoint amplitudes instead give

\[
M_{\rm geom}=\sqrt{M(c,P_+,p)M(c,P_-,p)}.
\]

At \(\bar P=0\), implicit differentiation of

\[
72\pi^4A^4+12\pi^2cA^3-3p^2+2P^2=0
\]

gives

\[
A_{PP}=-\frac1{6\pi^2A^2D},
\qquad
M_P=0,
\qquad
M_{PP}=\frac2{A^2D^3}>0.
\]

It follows that

\[
\frac{M_{\rm geom}}{M_{\rm sec}}
=1+\frac{\delta P^2}{6A^2D^2}
+O(\delta P^4).
\]

On \(c=0\), this reduces to

\[
\boxed{
\frac{M_{\rm geom}}{M_{\rm sec}}
=1+\frac{\delta P^2}{36p^2}
+O(\delta P^4)
}
\]

and there is also a finite, not merely formal, discriminator.  On the shell

\[
M(P)\propto(3p^2-2P^2)^{-1/4}
\]

is strictly increasing for \(0<P<\sqrt{3/2}\,p\).  For symmetric endpoints
\(P_\pm=\pm x\),

\[
M_{\rm geom}=M(x)
>\frac1x\int_0^xM(u)\,du
=M_{\rm sec}.
\]

Thus exact one-term coarea normalization fails for every nonzero allowed
\(x\), not just in a truncated Taylor series.

## 6. Independent numerical control

At 100 decimal digits with \(p=1\), three direct quadratures of the shell
secant mean were compared with the independent hypergeometric antiderivative.
The two methods agreed exactly at the retained precision.  The observed
ratios were

| \(\delta P\) | \(M_{\rm geom}/M_{\rm sec}\) | \((\rho-1)/\delta P^2\) |
|---:|---:|---:|
| 0.025 | 1.0000173623168410 | 0.0277797069456252 |
| 0.050 | 1.0000694637407896 | 0.0277854963158329 |
| 0.100 | 1.0002780868183535 | 0.0278086818353488 |

The exact small-separation coefficient is \(1/36=0.0277777777777778\).
The largest frozen coefficient error was
\(3.0904057571\times10^{-5}\), below the fixed \(2\times10^{-4}\) bound.

## 7. Execution and repair ledger

The frozen calculation was executed with

```bash
timeout --signal=TERM 120s \
  ./ice run cpt_temporal_folded_susy/gate1_v0_principal_endpoint_fio
```

The initial `VALID_RUN` completed in 2.2 seconds with 9/10 exact and 3/3
numerical checks.  Its only NONPASS compared two algebraically equal
factorizations of \(F_A\) by SymPy expression-tree equality:

\[
36\pi^2A^2(8\pi^2A+c)
=24\pi^2A^2(12\pi^2A+3c/2).
\]

An independent residual calculation returned exactly zero for this equality
and for the two downstream curvature identities.  The evaluator was changed
once to `simplify(lhs-rhs)==0`; the committed initial result preserves the
pre-repair terminal outcome in Git history.  One bounded replay then completed
in 2.2 seconds with:

```text
exact checks:                  10 / 10 PASS
high-precision controls:       3 / 3 PASS
analytic scope guards:         6 / 6 reviewed
root calls:                    0
quadratures:                   3
special-function evaluations: 3
ODE calls:                     0
automatic descendants:        0
result size:                   21,401 bytes
```

No additional retry or diagnostic descendant was started.

## 8. What remains open

The result does not compute:

- an \(\hbar\)-dependent subprincipal or full symbol;
- operator ordering, a self-adjoint domain, a spectral measure, or boundary
  conditions at \(R=0\) and \(p=0\);
- a global normalized endpoint transform or global Maslov gluing;
- a fixed-\((Q,\phi)\) to fixed-\((T,\Phi)\) coordinate kernel;
- multiplier, ghost and antighost endpoints, a nilpotent BRST charge, a gauge
  fermion, a replacement BFV measure or source lattice;
- equality with the old fixed-\((a,\phi)\) kernel;
- a zero-lapse extension or full-real-lapse \(\delta(C)\) rigging map;
- other components, a global canonical atlas, determinant-line orientation,
  a physical original cycle, a physics result, or a TOE.

The mathematically next dependency is not “run the same kernel harder.”  It is
to choose and derive either (a) a full-symbol/unitary spectral transform with
explicit ordering and domains, or (b) the extended BFV endpoint data and
replacement source.  This report authorizes neither automatically.

## 9. Artifacts

- `GATE1_V0_PRINCIPAL_ENDPOINT_FIO_INPUTS.json`
- `gate1_v0_principal_endpoint_fio.py`
- `GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT.json`

