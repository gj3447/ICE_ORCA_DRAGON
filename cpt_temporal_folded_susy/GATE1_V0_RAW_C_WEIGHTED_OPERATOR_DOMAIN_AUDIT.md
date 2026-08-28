# Gate 1 — weighted raw-\(C\) operator and domain audit

## Result

For one explicitly declared raw-constraint quantization,

\[
f(Q)=12\pi^2e^{3Q/2},\qquad
\mathcal H_C=L^2(\mathbb R_Q\times\mathbb R_\phi,f\,dQ\,d\phi),
\]

\[
C_{\min}=f^{-1}\widehat H\big|_{C_c^\infty},\qquad
\widehat H=2\hbar^2\partial_Q^2-3\hbar^2\partial_\phi^2-72\pi^4e^{2Q},
\]

the minimal scalar Fourier fibers have one limit-circle end at \(Q\to-\infty\)
and one limit-point end at \(Q\to+\infty\).  Under the stated Weyl and
direct-integral hypotheses, each fixed \(p\) fiber has
\(n_+=n_-=1\).  Consequently the classical positive rescaling \(H=fC\) does
not select a raw-\(C\) self-adjoint domain or establish quantum equivalence to
the already selected \(\widehat H\) realization.

The observed verdict is

```text
NARROW_V0_RAW_C_CANDIDATE_HAS_FIBER_EXTENSION_DEBT_GLOBAL_MEASURABILITY_OPEN
```

This is a result about one left-weighted ordering and its fiber domain debt. It
does not select \(\theta(p)\), construct a measurable global extension, give a
raw-\(C\) rigging map, or make a BFV, physics, quantum-gravity or TOE claim.

## Computed operator facts

The map \(U\chi=f^{1/2}\chi\) is unitary from \(\mathcal H_C\) to flat
\(L^2(dQ\,d\phi)\), with \(g=f^{-1/2}\) and

\[
UC_{\min}U^{-1}=g\widehat H g
=\frac{e^{-3Q/2}}{12\pi^2}
\left(2\hbar^2\partial_Q^2-3\hbar^2\partial_\phi^2
-3\hbar^2\partial_Q+\frac{9}{8}\hbar^2-72\pi^4e^{2Q}\right).
\]

After Fourier transformation in \(\phi\), the declared formal fiber is

\[
C_pu=f^{-1}\left[2\hbar^2u''+
\left(3p^2-72\pi^4e^{2Q}\right)u\right].
\]

The deficiency equation is

\[
2\hbar^2u''+
\left(3p^2-72\pi^4e^{2Q}-12\pi^2z e^{3Q/2}\right)u=0.
\]

At \(z=0\), setting \(x=6\pi^2e^Q/\hbar\) gives the modified-Bessel
equation with order \(i\sqrt{3/2}|p|/\hbar\).  The raw weighted norm becomes
proportional to \(x^{1/2}dx\).  Hence the two oscillatory small-\(x\) modes
for \(p\ne0\), and the \(1,\log x\) pair for \(p=0\), are integrable at the
minus end.  At the plus end, the \(K\) solution is integrable and the \(I\)
solution is not.

The oriented global Green form is

\[
2\hbar^2[W(\overline u,v)]_{-\infty}^{+\infty}.
\]

The plus-end contribution vanishes on the maximal domain.  For \(p\ne0\), the
formal travelling-coordinate contribution at the minus end is

\[
-4i\hbar^2k_p(\overline{A_u}A_v-\overline{B_u}B_v),
\]

and \(B=e^{i\theta}A\) is a fiber boundary line.  Actual maximal-domain
coordinates are Wronskian limits against a real zero-energy reference pair,
not literal limits of \(u\) and \(u'\) at \(-\infty\).  For \(p=0\), the
analogous affine line is \(B=\lambda A\), with real projective \(\lambda\).

## What was checked, and what was not

The successful run had 14/14 executable symbolic checks and 2/2 bounded
numerical checks.  The numerical diagnostics evaluated the Bessel equation and
\(W\{I_\nu,K_\nu\}=-1/x\) at 24 function samples (four \(p\) values and
three \(x\) values, for \(I\) and \(K\)).  The maximum normalized equation
residual was \(6.48\times10^{-72}\); the maximum Wronskian error was
\(3.24\times10^{-70}\), both against \(10^{-58}\).

Nine theorem guards are analytic hypothesis-and-scope audits, not executable
numerical predicates.  They cover the Fourier direct-integral core, Weyl's
alternative, fiber deficiency indices, Bessel asymptotic boundary coordinates,
and the extra measurable-field requirement for a decomposable extension.

In particular, a measurable \(\theta(p)\) is only a conditional
\(p\)-preserving recipe.  It does not construct a measurable global domain or
classify general deficiency-space unitaries that mix \(p\) fibers.  The
singleton \(p=0\) fiber is Lebesgue-null unless an extra atom is separately
introduced.

## Execution history

The first committed attempt, `7309cb8`, wrote a valid result but took the KILL
row with 13/14 exact checks.  The failed check was
`G1.rawc.endpoint.minus_zero_weighted_integrability`: SymPy left the improper
\(x^{1/2}\log^2x\) integral unevaluated.  This was a harness false negative,
not contrary endpoint evidence.

Commit `a64e9ef` repaired only that check by differentiating

\[
\int_0^1x^\alpha dx=\frac1{\alpha+1}
\]

twice in \(\alpha\), which gives the exact log-squared moment
\(16/27\).  The original failed artifact remains preserved at `7309cb8`.

The successful result was recorded in `1c3bd81`, and portable reproduction was
registered in `9029109`.

```text
./ice run gate1_v0_raw_c_weighted_operator_domain_audit
VALID_RUN; 14/14 executable exact checks; 2/2 numerical checks;
9 analytic hypothesis/scope guards

./ice repro --only gate1_v0_raw_c_weighted_operator_domain_audit
REPRO; 1 checked; 0 needs-attention

npm run check
67/67 tests passed
```

The input, runner and result are

- `GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_INPUTS.json`
- `gate1_v0_raw_c_weighted_operator_domain_audit.py`
- `GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_RESULT.json`

## Open boundary

The following remain null: a selected raw-\(C\) extension; a measurable
decomposable global extension; all \(p\)-mixing extensions; raw-\(C\) spectral
resolution, RAQ/group average and physical inner product; \(C\leftrightarrow H\)
or \(M_c\) equivalence; exact endpoint transform; absolute BFV measure; and
all inhomogeneous, relational, empirical and physics claims.
