# Gate 1 — homogeneous trace-gauge FP admissibility

## Outcome

The homogeneous trace variable gives a genuine **local** Lorentzian
constraint–gauge reduction on each existing simple shell-root chart away from
its Faddeev–Popov horizon:

\[
\boxed{
\text{LOCAL TRACE-GAUGE FIBER}=\text{KEEP}
\quad (a>0,\ C_L=0,\ D_L\ne0)
}
\]

That does **not** validate deleting the negative \(p_a\) Gaussian, and it does
not repair the current finite \(m=2\) source by multiplication with extra
trace-gauge delta functions.  The existing source already uses the one
endpoint-preserving nonzero proper-time gauge mode and fixes \((a,\phi)\) at
the endpoints.  The bounded result is therefore

```text
LOCAL_TRACE_GAUGE_FIBER_KEEP_UNCHANGED_PROPER_TIME_M2_APPEND_KILLED
```

Here `APPEND_KILLED` is deliberately narrow.  It rejects only the shortcut

\[
\text{unchanged proper-time/fixed-}a\text{ source}
\longrightarrow
\text{same source}\times\delta(\chi)\,\Delta_{\rm FP}.
\]

It does not reject a separately derived canonical-gauge representation.  An
improved static construction with transformed endpoint states and a
time-dependent \(f(s)\) construction both remain open and uncomputed.

The successful run passed 22 exact checks, five separately scoped theorem
guards, and two high-precision Gaussian checks.  Gate 1 remains
`OPEN_PARTIAL_PROGRESS`; the full \(m=2\) BFV measure, physical original
cycle, full joint orientation, global \(n_\sigma\), physics claim, and TOE
claim remain null.

## 1. Constraint and Wick conventions

The calculation uses the repository Lorentzian homogeneous constraint

\[
C_L=
-\frac{p_a^2}{24\pi^2a}
+\frac{p_\phi^2}{4\pi^2a^3}
+2\pi^2[-3a+a^3V(\phi)],
\qquad a>0,
\]

and the Euclidean-continued constraint

\[
C_E=
-\frac{p_{Ea}^2}{24\pi^2a}
+\frac{p_{E\phi}^2}{4\pi^2a^3}
+2\pi^2[3a-a^3V(\phi)].
\]

With the Phase-27 convention \(p_L=i p_E\), exact substitution gives

\[
C_L(q,i p_E)=-C_E(q,p_E).
\]

This continuation matters for the FP sign.  The positive Euclidean clock
bracket recorded in Phase 31 cannot simply be imported into the Lorentzian
source.

## 2. The homogeneous trace pair

For the declared homogeneous ADM reduction, the integrated trace momentum is

\[
P_{\rm tr}=\frac a2p_a,
\qquad
Q=2\log a.
\]

The runner verifies

\[
\{Q,P_{\rm tr}\}=1,
\qquad
P_{\rm tr}\,dQ=p_a\,da.
\]

Thus \((Q,P_{\rm tr})\) is an exactly normalized canonical pair and
\(P_{\rm tr}=0\) is equivalent to \(p_a=0\) for \(a>0\).  This is a statement
about the integrated homogeneous trace variable, not an identification with
the unintegrated local ADM density \(p(x)\).

## 3. Exact Lorentzian FP bracket

For

\[
\chi=P_{\rm tr}-f(s),
\]

the exact bracket is

\[
\boxed{
D_L:=\{\chi,C_L\}
=-\frac{p_a^2}{16\pi^2a}
+\frac{3p_\phi^2}{8\pi^2a^3}
+3\pi^2a(1-a^2V).
}
\]

It obeys the stronger off-shell identity

\[
D_L=\frac32C_L+6\pi^2a(2-a^2V),
\]

so on the constraint surface

\[
\boxed{D_L\big|_{C_L=0}=6\pi^2a(2-a^2V).}
\]

The local FP horizon is therefore

\[
a^2V=2.
\]

The Euclidean bracket has the opposite algebraic Wick sign,

\[
D_L(q,i p_E)=-D_E(q,p_E).
\]

At the reflection neck \(p_a=p_\phi=0\), \(a^2V=3\), the two trace brackets
are

\[
D_L=-6\pi^2a,
\qquad
D_E=+6\pi^2a.
\]

The latter is the trace-normalized counterpart of the Phase-31 Euclidean
\(p_a\) bracket \(+12\pi^2\).

## 4. Reduction is not deletion

For \(a>0\),

\[
\delta(\chi)
=\frac2a\,
\delta\!\left(p_a-\frac{2f}{a}\right).
\]

Define

\[
C_f(a,\phi,p_\phi)
:=C_L\!\left(a,p_a=\frac{2f}{a},\phi,p_\phi\right).
\]

The runner proves the exact derivative identity

\[
\boxed{
\frac2aD_L\big|_{\chi=0}
=-\frac{dC_f}{da}.
}
\]

Consequently, at each simple \(a\)-root, the signed delta/ghost residue is
the pre-orientation value \(\operatorname{sgn}D_L\).  If the elementary
reduced-orbit delta Jacobian is taken with an absolute value, its weight is
instead \(+1\) per simple root.

These ledgers must remain separate.  A componentwise gauge orientation has
not been chosen globally, and the raw sign cannot be reused as a negative-arm
sign, a determinant-line orientation, or a physical relative coefficient.

The symplectic-rank control makes the distinction concrete:

- imposing only \(p_a=0\) leaves the pulled-back two-form with rank 2 on a
  3-dimensional surface, with a null \(\partial_a\) direction;
- imposing one transverse constraint–gauge pair leaves the scalar
  \((\phi,p_\phi)\) two-form with rank 2 on 2 dimensions.

The first is deletion followed by degeneracy.  The second is a local
reduction.

## 5. Root sheets and the exact FP horizon

At \(f=0\), the constraint gives

\[
p_\phi^2=8\pi^4a^4(3-a^2V).
\]

For a frozen \(V>0\), let

\[
u=a^2V,
\qquad
\kappa=\frac{p_\phi^2V^2}{8\pi^4}.
\]

The allowed shell domain is \(0<u\le3\), and

\[
\kappa=u^2(3-u),
\qquad
\frac{d\kappa}{du}=3u(2-u).
\]

Thus \((u,\kappa)=(2,4)\) is the exact maximum and FP horizon.  At the exact
benchmark \(\kappa=2\),

\[
u^3-3u^2+2
=(u-1)(u^2-2u-2),
\]

so the two positive roots are

\[
u_-=1,
\qquad
u_+=1+\sqrt3.
\]

Since \(D_L\propto2-u\) on shell, their pre-orientation signs are opposite.
This proves a branch/orientation problem and locates a horizon.  It does not
prove that the two roots are copies on one global gauge orbit or construct a
fundamental region.

## 6. What the static preservation equation does—and does not—say

The ordinary homogeneous classical preservation equation is

\[
\dot\chi=N D_L-\dot f.
\]

For \(f=0\) and \(D_L\ne0\), it gives

\[
N=0.
\]

This means that the ordinary regular static classical representative is not
the existing nonzero-constant-lapse history.  If one insists on a nonzero
homogeneous multiplier inside this representative, then

\[
N=\frac{\dot f}{D_L}
\]

requires a time-dependent \(f\).

This is not a no-go for every static canonical gauge.  A generally covariant
path integral may require an improved boundary action and gauge-related
endpoint states; in such a representation, physical proper-time information
need not be carried by the same classical multiplier.  The present runner
does not construct or validate that improved static route.  It also says
nothing about the inhomogeneous maximal-slicing lapse equation.

## 7. Why the current finite \(m=2\) source cannot be reused unchanged

For two elements with \(h=1/2\) and endpoint-vanishing gauge parameter
\(\epsilon_0=\epsilon_2=0\), the exact lapse variation is

\[
\delta(N_0,N_1)=(2\epsilon_1,-2\epsilon_1).
\]

It has rank one, while

\[
\delta T
=\frac12\delta(N_0+N_1)=0,
\qquad
\delta(N_0-N_1)=4\epsilon_1.
\]

Hence \(N_0=N_1\) fixes the sole endpoint-preserving nonzero lapse-gauge
mode and leaves \(T\) as the global modulus.  The current canonical source is
already the resulting constant-lapse/proper-time object.  It has no second
demonstrated residual gauge direction that licenses an extra trace FP gauge
with unchanged action and endpoints.

This rank calculation is a lapse-sector kinematic control.  It is not an
exactly gauge-invariant \(m=2\) replacement discretization.  A legitimate
trace-gauge source must return to a local-lapse/local-constraint formulation
and rederive the gauge, action, endpoint states, and measure before comparison
with the old source.

## 8. Endpoint transversality and boundary data

In the original fixed-\(Q=2\log a\) chart, the static endpoint condition has

\[
\left.
\frac{\partial C_L}{\partial P_{\rm tr}}
\right|_{P_{\rm tr}=0}=0,
\]

so that chart is not transverse at the static trace surface.  One possible
local implementation swaps the canonical chart,

\[
(Q',P')=(P_{\rm tr},-Q),
\]

for which

\[
\frac{\partial C_L}{\partial P'}
=\{P_{\rm tr},C_L\}=D_L.
\]

It is transverse where \(D_L\ne0\).  The corresponding fixed-momentum action
subtracts the boundary Legendre term

\[
[P_{\rm tr}Q].
\]

Phase 31's different fixed-\(p_a\) chart instead carries \([a p_a]\).  Either
choice changes the endpoint problem relative to the existing fixed-\(a\)
kernel.  The swapped fixed-\(P_{\rm tr}\) chart is one implementation used by
this control; it is not the unique endpoint construction required by the
general canonical-gauge formalism.

## 9. Formal local Gaussian after reduction

After the formal local trace reduction, only the positive scalar momentum
quadratic remains.  For the projector sign

\[
e^{-izC_L/\hbar},
\]

define

\[
\alpha=\frac{iz}{4\pi^2a^3\hbar}.
\]

On \(z=N-i\epsilon\),

\[
\operatorname{Re}\alpha
=\frac{\epsilon}{4\pi^2a^3\hbar}>0,
\]

whereas \(z=N+i\epsilon\) gives the opposite sign.  The effective FP factor
is only quadratic in \(p_\phi\), so it cannot spoil lower-lateral Gaussian
absolute convergence.

At the exact flat-potential benchmark \(a=1\), \(V=f=0\),

\[
C_{\chi=0}=\frac{p_\phi^2}{4\pi^2}-6\pi^2,
\qquad
\Delta_{\rm eff}
=\frac{3p_\phi^2}{4\pi^2}+6\pi^2>0.
\]

The constraint roots and their on-shell FP value are

\[
p_\phi=\pm2\sqrt6\,\pi^2,
\qquad
\Delta_{\rm eff}=24\pi^2.
\]

The elementary absolute-delta target is

\[
\int dp_\phi\,
\Delta_{\rm eff}\,
e^{ip_\phi q/\hbar}\,
\delta(C_{\chi=0})
=8\sqrt6\,\pi^2
\cos\!\left(\frac{2\sqrt6\,\pi^2q}{\hbar}\right).
\]

For \(\operatorname{Re}\alpha>0\), the independently checked
polynomial-Gaussian expression is

\[
\begin{aligned}
F(z,q)
={}&e^{i6\pi^2z/\hbar}
\sqrt{\frac{\pi}{\alpha}}
e^{-q^2/(4\alpha\hbar^2)}\\
&\times\left[
6\pi^2+
\frac{3}{4\pi^2}
\left(
\frac{1}{2\alpha}
-\frac{q^2}{4\alpha^2\hbar^2}
\right)
\right].
\end{aligned}
\]

At \(q=0.125\), \(\hbar=1\), the real-axis quadratures give relative errors

| \(z\) | relative error | required tolerance |
|---|---:|---:|
| \(-0.4i\) | \(3.42937\times10^{-70}\) | \(10^{-45}\) |
| \(0.2-0.4i\) | \(9.16035\times10^{-65}\) | \(10^{-45}\) |

These are normalization checks for the formal local reduced scalar fiber.
They do not prove a full lapse-to-\(\delta(C)\) contour identity, source
deformation, a full BFV measure, or equivalence to the old fixed-\(a\) kernel.

## 10. Primary-source boundary

- [Banihashemi and Jacobson](https://doi.org/10.1103/PhysRevD.111.066014)
  supply the constraint-plus-gauge FP premise and the lower-lateral
  momentum-first argument after removal of the negative full-theory trace
  block.  They do not derive this homogeneous preservation equation, \(m=2\)
  rank, endpoint transform, or orientation ledger.
- [Henneaux, Teitelboim, and Vergara](https://doi.org/10.1016/0550-3213(92)90166-9)
  frame canonical-gauge transversality, gauge-related endpoint states, boundary
  terms, and componentwise gauge orientation.  They do not prove that either
  open replacement route works for this repository model.
- [Marolf](https://doi.org/10.1103/PhysRevD.53.6979) frames the full-real-lapse
  minisuperspace constraint projection and gauge-fixed path integral.  The
  absolute simple-root delta Jacobian used here is an elementary calculation;
  it is not promoted from Marolf's coordinate-gauge formula to a general
  theorem for this momentum gauge.
- [Halliwell](https://doi.org/10.1103/PhysRevD.38.2468) frames the proper-time
  reduction and the full-line Wheeler–DeWitt homogeneous solution versus
  half-line Green-function distinction.  It does not derive this trace-gauge
  algebra.
- [Rogers](https://arxiv.org/abs/hep-th/9902133) bounds the interpretation:
  local FP nonvanishing is weaker than global BFV gauge-fermion admissibility
  and does not resolve Gribov obstructions.

## 11. Reproduction and review

The successful bounded command was

```bash
./ice run cpt_temporal_folded_susy/gate1_trace_gauge_fp_admissibility
```

Observed output:

```text
run_status = VALID_RUN
exact checks = 22/22
theorem guards = 5/5
numerical checks = 2/2
root calls = 0
ODE calls = 0
automatic descendants = 0
result bytes = 19,274
```

Two earlier bounded attempts stopped before writing a result.  Both were
SymPy structural-equality false negatives between exactly equal factorizations:

- \(3u(2-u)\) versus \(-3u(u-2)\);
- an expanded versus factored positive benchmark FP polynomial.

Commits `e8ea277` and `284c0ba` changed those checks to exact semantic
zero-difference tests.  They did not change the frozen question, formulas,
decision table, or scope.  The third run produced the only result artifact.

Three read-only reviews independently checked the conventions and scope; two
also recomputed the result hashes and formulas after execution.  No
conclusion-changing error remained.  In particular, the reviews narrowed the
static-gauge wording before execution so that the raw result leaves both an
improved static replacement and a time-dependent replacement open.

## 12. Decision and next discriminator

Computed facts:

- local homogeneous trace reduction: `KEEP` on existing simple-root charts
  with \(D_L\ne0\);
- naive \(p_a\) deletion: `NOT_REDUCTION`;
- unchanged proper-time/fixed-\(a\) \(m=2\) append shortcut: `KILLED / NOT
  LICENSED`;
- ordinary regular static classical representative: \(N=0\);
- improved static replacement: `OPEN_NOT_COMPUTED`;
- time-dependent replacement: `OPEN_CANDIDATE_NOT_COMPUTED`;
- global fundamental region and full \(m=2\) BFV measure: open/null.

The next calculation must **replace**, not append to, the current gauge.  It
must start from local lapse and constraint variables, choose and serialize an
endpoint construction, derive the FP/BFV measure, and only then reduce to a
finite source.  The smallest useful fork is:

1. an improved static canonical gauge with its transformed endpoint states
   and boundary action; or
2. a time-dependent \(P_{\rm tr}=f(s)\) chart with \(D_L\ne0\), reduced
   Hamiltonian, endpoint data, and an explicit fundamental root sheet.

Only after one replacement source reproduces its own constraint projector and
admits a controlled comparison with the old proper-time kernel can the
source-to-complex-cycle, zero-lapse, relative-end, determinant-line, and
global-intersection problems be resumed.

No physical or TOE claim is made.
