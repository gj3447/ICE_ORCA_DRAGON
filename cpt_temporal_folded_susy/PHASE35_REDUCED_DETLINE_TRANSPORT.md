# Phase 35 — reduced endpoint determinant-line transport

## Result

The complex endpoint-Jacobi section inherited from Phase 34,

\[
d(T)=\det B_v(T),
\qquad
B_v=M_{(a,\phi),(\dot a,\dot\phi)},
\]

was transported along the bounded upper and lower **dual-aligned reduced
stationary-family branches** of Phase 34.  In the declared endpoint basis it
does not vanish at any of the sampled points.  Its upper phase starts near
\(-\pi/2\), unwraps continuously past a total rotation larger than \(\pi\),
and reaches the Phase-34 endpoint at \(\operatorname{Re}T=13\).  The lower
line is the complex conjugate.

This determines a **relative finite-dimensional endpoint transport**.  It
does not fix the absolute square-root sign, a Maslov orientation, the full
BFV/SUGRA superdeterminant, or the global intersection coefficient.
In particular, it does not orient the incoming Picard--Lefschetz cycle into
either outgoing constant-phase branch.

## 1. Frozen convention

The row and column order is

\[
\text{rows}=(a,\phi),
\qquad
\text{columns}=(\dot a,\dot\phi).
\]

The Phase-34 fold null vector remains normalized with positive midpoint
scale-factor component.  With that convention the upper branch obeys

\[
\boxed{
d_+(\tau)=-i C_{\det}\sqrt{\tau}+O(\tau),
\qquad C_{\det}>0,
}
\]

where \(\tau=\operatorname{Re}T-T_c\).  Reordering an endpoint basis vector or
reversing an orientation can change this sign.  It is therefore a declared
local convention, not an absolute Maslov orientation.

Real coefficients give

\[
B_v^-(\tau)=\overline{B_v^+(\tau)},
\qquad
d_-(\tau)=\overline{d_+(\tau)}.
\]

Consequently

\[
d_+d_-=|d_+|^2>0
\]

whenever the sampled endpoint block is nonsingular.  This phase cancellation
is only for the displayed reduced bosonic endpoint pair; it is not a claim
about ghosts, gravitini, inhomogeneous modes, or a regulated
superdeterminant.

## 2. Continuous phase and square-root lift

For nonzero ordered samples \(d_j\), define

\[
\theta_0=\operatorname{Arg}d_0,
\qquad
\theta_{j+1}=\theta_j+
\operatorname{Arg}\!\left(\frac{d_{j+1}}{d_j}\right),
\]

where every increment uses the principal interval \((-\pi,\pi]\).  The code
checks

\[
e^{i\theta_j}=\frac{d_j}{|d_j|}
\]

at every point.  One continuous square-root lift is

\[
g_j=\sqrt{|d_j|}\,e^{i\theta_j/2},
\qquad g_j^2=d_j.
\]

The other lift is \(-g_j\).  Neither the local ODE nor the nonzero sampled
path chooses between them.  Phase 35 therefore reports

\[
e^{i\Delta\theta},
\qquad e^{i\Delta\theta/2},
\]

only as **relative unit transports** from the regulated first point.  Calling
the latter an absolute Gaussian or Maslov phase would require an oriented
original integration cycle and a compatible determinant regulator.

Also, \(g=\sqrt d\) is the lift of the displayed determinant section, not the
Gaussian prefactor itself.  If this endpoint block is the relevant regulated
Van Vleck block, its inverse-square-root factor has unit phase

\[
e^{-i\Delta\theta/2},
\]

the opposite of the square-root-section phase.  Establishing the exact
canonical/momentum-adjusted block and its measure belongs to the full BFV
calculation.

## 3. Numerical construction

The calculation begins at

\[
\tau_{\min}=2\times10^{-6}
\]

with the Phase-34 Airy seed.  It independently solves the five-equation
constant-\(\operatorname{Im}W\) boundary-value problem, takes continuation
steps no larger than \(0.04\), and records a dense determinant table through

\[
T=13+2.89138959974\,i.
\]

At each recorded point the full complex variational system is reintegrated.
The determinant, its smallest singular value, and both endpoint and root
residuals are checked before phase unwrapping.  Selected lower-branch points are
also integrated directly rather than being filled in by conjugation.

Near the fold the first seven samples use

\[
\tau=(2,5,10,20,50,100,200)\times10^{-6}.
\]

They verify

\[
\arg d_+\longrightarrow-\frac{\pi}{2},
\qquad
\frac{d_+}{-i\sqrt\tau}\longrightarrow C_{\det}>0.
\]

The smallest-\(\tau\) coefficient is approximately

\[
C_{\det}=1.02368\times10^4,
\]

and the phase error has the expected leading square-root scaling.  This is a
coordinate-normalized coefficient; its sign and limiting direction are the
relevant outputs here, not its absolute magnitude.

The Phase-34 anchors are reproduced:

\[
d(2\times10^{-4})
=2.10846219-144.75976643\,i,
\]

\[
d(13-T_c)
=-191673.33713+465022.38727\,i.
\]

The upper endpoint argument is about \(1.9618\).  Since the fold limit is
\(-\pi/2\), the bounded upper path rotates by about \(3.5326\) radians from
that limiting direction.  The precise executable output separately reports
the rotation from the finite regulator \(\tau_{\min}\).

## 4. Independent continuity checks

The dense phase increments stay positive and well below \(\pi\), so the
unwrapping never hides a sampled branch-cut jump.  At five interior values of
\(\tau\), the code starts from the stored solution but independently resolves
the BVP at \(\tau-h\) and \(\tau+h\).  Their phases bracket the center phase,
their determinant changes are small, and their root residuals remain within
the same numerical gate.  This tests local branch continuity without merely
reapplying `numpy.unwrap` to the displayed samples.

Six selected lower determinants from independent conjugate integrations
agree with \(\overline{d_+}\).  Real-ODE conjugacy is then used to construct
the full sampled lower lift analytically.  With the same path ordering,

\[
\theta_-(\tau)=-\theta_+(\tau),
\qquad
\Delta\theta_-=-\Delta\theta_+.
\]

Thus the reduced upper/lower endpoint unit phases cancel.  The two
square-root signs on each branch remain unselected.  Therefore determinant-phase
cancellation alone does not prove cancellation of square-root or Gaussian
prefactors; that would additionally require a correlated lift orientation.

## 5. Claim boundary

Supported on the sampled Phase-34 dual-aligned reduced stationary-family
branch pair through \(\operatorname{Re}T=13\):

- the declared complex endpoint-Jacobi determinant section stays nonzero;
- its phase admits a continuous lift from the oriented fold asymptotic;
- the two relative square-root lifts differ by one global sign;
- the corresponding inverse-square-root endpoint factor has the opposite
  half phase, subject to the still-open canonical/measure completion;
- six direct lower integrations spot-check the analytically conjugated line;
- the relative reduced bosonic **determinant** endpoint phases cancel in the
  conjugate pair.

Open and not computed:

- an absolute determinant or Maslov orientation;
- the incoming-to-outgoing Picard--Lefschetz connection at the fold;
- Jacobi zeros between samples, on other sheets, or in other modes;
- every joint field--lapse dual branch/cycle and every good end;
- the regulated BFV/SUGRA superdeterminant including ghosts and fermions;
- the complete relative cycles and global \(n_\sigma\);
- a WDW density matrix or physical seam state.

In particular, sampled nonvanishing cannot prove global nonvanishing.  The
relative endpoint transport is an input to the next full-cycle calculation,
not its replacement.

## 6. Reproduction

Direct locked run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase35_reduced_detline_transport.py
```

Workbench entry point:

```bash
./ice run phase35_reduced_detline_transport
```

The final `PHASE35_RESULT` JSON contains:

```json
{"exact_checks": 6, "numerical_checks": 8}
```

The executable prints one deterministic `PHASE35_RESULT=` JSON payload and
writes no files.  Importing the module is silent.

## Primary-source boundary

- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655)
  supplies the local coalescing-saddle/Airy framework, not this determinant
  coefficient or global contour.
- [Witten](https://arxiv.org/abs/1001.2933) supplies the relative-cycle and
  Picard--Lefschetz framework in which an orientation would matter, not the
  missing original cycle or BFV regulator here.
- The finite-dimensional square-root lift used here is elementary.  It is
  not presented as an infinite-dimensional functional-determinant
  regularization theorem.
