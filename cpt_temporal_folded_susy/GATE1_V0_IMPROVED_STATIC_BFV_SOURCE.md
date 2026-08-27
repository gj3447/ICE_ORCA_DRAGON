# Gate 1 — closed-FRW \(V=0\) local improved-static BFV source algebra

## Outcome

This bounded, non-numbered calculation closes one **local algebraic**
subproblem left open by the trace-gauge append falsifier.  On the exact
closed-FRW component

\[
\mathcal U_+
=\{(Q,P,\phi,p):p>0,\ R=3p^2-2P^2>0\},
\]

the hash-verified Darboux chart \((T,c,\Phi,p)\) supports one internally
consistent improved-static BFV zero-mode convention.  The implemented graded
bracket derives a nilpotent Abelian BRST differential, the transformed
endpoint polarization is BRST compatible, and the declared local
FP/Fourier/Berezin contraction is nonsingular and oriented.

The frozen verdict is

```text
KEEP_V0_LOCAL_IMPROVED_STATIC_BFV_ENDPOINT_SOURCE_ALGEBRA
```

with programme impact `NARROW_LOCAL_KEEP`.  This is not a KEEP for a full BFV
path measure or physical endpoint kernel.  It means only that the proposed
local replacement-source **algebra and zero-mode convention** survive their
declared checks.  The calculation did not append a trace delta or determinant
to the old fixed-\(a\), nonzero-proper-time source.

All 21 exact checks and all three 80-digit numerical checks passed.  Six
analytic scope guards were recorded separately; they delimit interpretation
and are not additional evidence of a physical theory.  Gate 1 remains
`OPEN_PARTIAL_PROGRESS`, global promotion remains `PROHIBITED`, and the
physical-cycle, full-trajectory, \(\delta(C)\), physics and TOE outputs remain
null.  The result starts no descendant calculation.

## 1. Source and interpretation boundary

Henneaux--Teitelboim--Vergara establish that generally covariant systems can
use time-independent canonical gauges when the endpoint action and endpoint
states are transformed consistently.  They do not derive the repository's
closed-FRW Darboux chart or the finite zero-mode measure convention below.

García--Vergara--Urrutia supply the extended BFV multiplier/ghost framework,
BRST charge, fermionic gauge fixing and compatible endpoint-data pattern.
They do not choose this model-specific gauge fermion, prove this source's
normalization, or construct a global determinant line or physical state.

Marolf supplies the full-real-lapse distributional constraint average as a
comparison target.  The local \(\delta(c)\) below is not that spectral or
rigging-map construction.  Banihashemi--Jacobson provide additional
constraint-plus-gauge and lapse-contour context, but do not derive the present
replacement source.

Primary sources:

- M. Henneaux, C. Teitelboim, and J. D. Vergara,
  [*Gauge invariance for generally covariant systems*](https://arxiv.org/abs/hep-th/9205092),
  Nucl. Phys. B 387 (1992) 391--418.
- J. A. García, J. D. Vergara, and L. F. Urrutia,
  [*BRST--BFV quantization and the Schwinger action principle*](https://arxiv.org/abs/hep-th/9511092),
  Int. J. Mod. Phys. A 11 (1996) 2689--2706,
  [doi:10.1142/S0217751X96001309](https://doi.org/10.1142/S0217751X96001309).
- D. Marolf,
  [*Path integrals and instantons in quantum gravity: Minisuperspace models*](https://arxiv.org/abs/gr-qc/9602019),
  Phys. Rev. D 53 (1996) 6979--6990.
- B. Banihashemi and T. Jacobson,
  [*On the lapse contour in the gravitational path integral*](https://arxiv.org/abs/2405.10307),
  Phys. Rev. D 111 (2025) 066014.

These sources bound the formal framework.  Every model-specific equation and
normalization choice below is a repository calculation or an explicitly
declared convention.

## 2. Hash-verified classical input

The calculation consumes, rather than independently rederives, the preceding
off-shell Darboux chart.  Its canonical pairs are

\[
(T,c),\qquad (\Phi,p),
\]

and its improved endpoint potential is

\[
B=PQ+W-cT-pW_p,
\qquad
P\,dQ+p\,d\phi=c\,dT+p\,d\Phi+dB,
\qquad
S_D=S_0-[B]_1^2.
\]

On \(\mathcal U_+\),

\[
D=-C_Q
=\frac{R+24\pi^4a^4}{8\pi^2a^3}>0,
\qquad
T_P=\frac1D>0,
\qquad
T(c,0,p)=0.
\]

Thus \(T=0\) is equivalent to \(P=0\) at fixed \((c,p)\), and the local
coarea relation is \(\delta(P)D=\delta(T)\).  The static representative has
\(B=0\).  These are downstream consequences of the pinned chart, not a new
global chart theorem.

## 3. Graded BFV algebra

Add the bosonic multiplier pair \((N,\Pi)\) and freeze the odd order as

\[
(c_g,\bar c,\rho,\bar\rho),
\]

with odd canonical pairs \((c_g,\bar\rho)\) and \((\bar c,\rho)\).  The
implemented even BFV bracket uses right derivatives on its left argument and
left derivatives on its right argument.  Consequently even fundamental
brackets are antisymmetric and odd fundamental brackets are symmetric.

For

\[
\Omega=c_g c+\rho\Pi,
\]

the runner derives, rather than separately declares,

\[
\begin{aligned}
sT&=c_g,& sN&=\rho,& s\bar c&=\Pi,& s\bar\rho&=c,\\
sc&=0,& s\Pi&=0,& s\Phi&=0,& sp&=0,& sc_g&=s\rho=0.
\end{aligned}
\]

It verifies \(\{\Omega,\Omega\}=0\) and \(s^2=0\) on every declared
generator.  With

\[
\Psi=\bar c\,T+\bar\rho\,N,
\]

the same bracket gives

\[
\boxed{s\Psi=\Pi T+Nc-c_g\bar c-\rho\bar\rho},
\qquad
\{s\Psi,\Omega\}=0.
\]

The multiplier kinetic convention obeys

\[
-N\dot\Pi=\Pi\dot N-\frac{d}{dt}(N\Pi).
\]

The boundary difference vanishes because \(\Pi=0\) at both endpoints.

## 4. Endpoint polarization is not the constraint delta

The endpoint data fix \(T=0\) and \(\Phi\), and impose

\[
c_g=\bar c=\Pi=0.
\]

The corresponding endpoint ideal is

\[
I_\partial=(T,\Pi,c_g,\bar c).
\]

It is BRST stable, and the fixed physical coordinate \(\Phi\) is invariant.
The conjugate constraint coordinate \(c\) is deliberately **not** in this
ideal.  It is not silently fixed as endpoint data.

Instead, the declared bosonic zero-mode phase is

\[
\exp\!\left[\frac{i}{\hbar}(\Pi T+Nc)\right].
\]

With the independently declared full-real Fourier measures

\[
\frac{d\Pi}{2\pi\hbar}\frac{dN}{2\pi\hbar},
\]

the unit pairing matrix gives \(\delta(T)\delta(c)\).  In particular,
\(\delta(c)\) is attributed to the \(N\) zero-mode integration, not to the
endpoint polarization.

## 5. Oriented ghost zero-mode convention

The actual quantum ghost factor is

\[
\exp\!\left[\frac{i}{\hbar}
(-c_g\bar c-\rho\bar\rho)\right].
\]

In the frozen order \(c_g\bar c\rho\bar\rho\), its raw top coefficient is

\[
-\frac1{\hbar^2}.
\]

The calculation explicitly declares the oriented local measure convention

\[
\int_{\rm oriented}D\theta\,F
:=-\hbar^2[c_g\bar c\rho\bar\rho]F,
\]

which makes this finite zero-mode factor \(+1\).  Under that convention,
\(\delta(T)\delta(c)\) contracts a generic local test polynomial to
\(F_0(\Phi,p)\).

This \(+1\) is not an absolute BFV functional-measure normalization.  The
calculation contains no nonzero trajectory modes, determinant/Pfaffian line,
global orientation or Gribov analysis.

## 6. Declared reduced identity compatibility

After the separately normalized gauge zero-mode factor, the calculation tests
the declared reduced one-step convention

\[
S_{\rm red}=p(\Phi_2-\Phi_1),
\qquad
\frac{dp}{2\pi\hbar}.
\]

With \(x=\Phi_2-\Phi_1\), its Gaussian regulator is

\[
K_\epsilon(x)
=\frac{e^{-x^2/(4\epsilon)}}{2\sqrt{\pi\epsilon}}.
\]

For \(g_\alpha(x)=e^{-\alpha x^2}\),

\[
\int_{\mathbb R}K_\epsilon(x)g_\alpha(x)\,dx
=\frac1{\sqrt{1+4\alpha\epsilon}}
\longrightarrow 1=g_\alpha(0).
\]

At \(\alpha=0.7\), the frozen quadratures gave:

| \(\epsilon\) | observed pairing | distance to 1 |
|---:|---:|---:|
| 0.20 | 0.8006407690254356674 | 0.1993592309745643326 |
| 0.05 | 0.9365858115816939659 | 0.0634141884183060341 |
| 0.01 | 0.9862873039405895583 | 0.0137126960594104417 |

All three direct 80-digit integrations matched the exact formula within the
declared \(10^{-60}\) relative tolerance, and the sampled distances decreased
monotonically.  This checks compatibility with a **declared canonical
identity distribution**.  It is not a two-endpoint full BFV propagator and is
not the spectral distribution \(\delta(\widehat C)\).

## 7. What changed, and what did not

### Computed fact

One local improved-static BFV zero-mode algebra is internally consistent on
\(\mathcal U_+\).  It avoids the already killed append-only construction and
reduces a concrete formal obstruction: the Darboux endpoint polarization,
BRST algebra, local constraint/gauge pairing and a frozen ghost orientation
can be made mutually consistent.

### Interpretation

This is useful source-design evidence inside the calculation workbench.  It
does not establish that the convention equals a normalized physical quantum
amplitude.  In particular, consistency of a finite algebra does not imply
gauge independence, a correct spectral measure, or agreement with nature.

### Open physical hypothesis

No physical hypothesis was tested.  No observable, external dataset, 3+1D
field mode, GR/QFT recovery result or discriminating prediction was produced.
Accordingly, this calculation does not materially change the prior estimate
of the programme's chance of reaching a defensible TOE claim.

The following remain uncomputed:

- a normalized endpoint-state transform and physical Hilbert measure;
- an ordering and self-adjoint domain for \(\widehat C\);
- a spectral or rigging-map \(\delta(\widehat C)\) pairing;
- a two-endpoint, finite-\(m\), or continuum BFV trajectory measure;
- equality to the old fixed-\(a\), proper-time kernel;
- other Darboux components, a global gauge atlas and Gribov census;
- a physical original cycle, global \(n_\sigma\), physics claim or TOE claim.

## 8. Next independent question

The highest-information next step is not to enlarge this immediately into a
full path integral.  First specify a Hilbert measure, operator ordering and
self-adjoint domain for \(\widehat C\); derive the normalized endpoint-state
transform associated with \(B\); and compare the resulting static pairing
with a spectral \(\delta(\widehat C)\) pairing on a compact, frozen family of
test states.

That comparison should have an explicit mismatch/null row.  It directly asks
whether the present local convention has a quantum target, whereas a larger
trajectory calculation would add regulator, contour and mode ambiguities
before that target is fixed.  No such calculation is authorized or launched
by this result.

## 9. Execution and provenance

Command:

```bash
./ice run cpt_temporal_folded_susy/gate1_v0_improved_static_bfv_source
```

Observed execution:

- exit code: `0`;
- wall time reported by the execution tool: `2.606376245 s`;
- environment: Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0;
- exact checks: `21/21`;
- numerical checks: `3/3`;
- quadratures: `3`; root and ODE calls: `0`;
- changed artifacts: one adjacent 26,688-byte result;
- automatic descendants: `0`.

Pinned provenance:

- source/input commit: `a0eb33c13b91b6a1b8a7407bf015d9b2093d2d04`;
- raw-result commit: `3e068389788676c69e8782eb9d34a2edb0416c96`;
- input SHA-256:
  `ad9297d33b5fa2e3da4b31969e4d412d5f7891e20ce15b43de6e5476964261a3`;
- runner SHA-256:
  `62f52d079c62b9b84ccea6562e44b952067cd6c8e10f7d1a9673cc124b949ccf`;
- raw-result SHA-256:
  `62f3c2fb2cb5574b495d64c4566e196e96fde4fca332636a2891999eefef9b55`;
- independently recomputed payload SHA-256 without self:
  `c62f45cf0bb0bedaf1f74a94d1ad96e5138ea50825f253c9a426293279e19925`.
