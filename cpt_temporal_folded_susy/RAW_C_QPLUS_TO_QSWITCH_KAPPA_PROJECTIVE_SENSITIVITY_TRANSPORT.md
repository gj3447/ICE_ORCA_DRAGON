# Raw-C Qplus-to-Qswitch kappa projective-sensitivity transport

## Independent question

On the exact correlated $K\times\Lambda$ strip, does the selected real
plus-recessive projective derivative $h=\partial_\kappa\rho$ remain uniformly
strictly negative after transport from $Q_+=4$ to
$Q_{\rm switch}=-29/10$?

This is a new bounded question aimed directly at the next missing P1 link. It
does not replay the endpoint anchor or use the sign-strip face values as
derivative evidence.

## Comparison transport

With $x=6\pi^2e^Q$ and $p=-h$, exact differentiation at fixed $\lambda$ gives

\[
p_x=\left(2+\frac{1+2\rho}{x}\right)p-\frac{2\kappa}{x}.
\]

The pinned selected-family barrier $-1\leq\rho\leq1$ gives

\[
2-\frac1x\leq2+\frac{1+2\rho}{x}\leq2+\frac3x.
\]

Variation of constants therefore bounds the backward transport by the two
positive kernels

\[
e^{-2(t-a)}(a/t)^3,
\qquad e^{-2(t-a)}(t/a),
\]

where $a=x(Q_{\rm switch})$. The lower forcing integral is enclosed by
monotone 512/1024-panel ladders at 80/120 decimal digits through $y=24$;
the remaining nonnegative tail is discarded from the lower bound. The upper
forcing integral over the complete segment simplifies exactly because the
factor $t/a$ cancels the $1/t$ forcing.

The singular endpoint is not assigned an extra $C^1$ hypothesis. The upstream
anchor already supplies the derivative at $Q_+$; standard smooth parameter
dependence of the finite Riccati initial-value problem on the certified finite
$\rho$ tube propagates that seed over this leg.

An elementary $\Delta Q=1/10$ comparison also gives the independent strict
floor $p(Q_{\rm switch})>\kappa_{\rm left}/20>0$. The frozen relaxations are
$x_{\rm switch}<15/4$, $e^{1/10}-1<1/9$, and $e^{17/15}<4$.

## Explicit boundary

Even a strict signed result here is only a selected projective derivative at
$Q_{\rm switch}$. It does not provide the $Q_0$ derivative, the reference
state's kappa variation, the complete differentiated minus tail,
$\partial_\kappa G$, a mixed derivative, root transversality or uniqueness, a
selector, continuation, velocity, absolute $\Gamma_1$ amplitude/sign, global
roots, nonreal Weyl/spectral data, RAQ, BFV, a physical product, or physics.

## Controlled execution

- Frozen input SHA-256:
  `dff13b4a24cd8ea3f5ff76bd72778815dc3a608ec155463b8ee31e0fdbde446e`
- Initial runner SHA-256:
  `cf2b2171ef0a9029d220195e0cbd0b0c0bd4ce5b5e3974894589dd6a25c031b3`
- Common caps: 120 seconds; 262,144 bytes each for stdout/stderr; at most
  12 changed artifacts and 1,000,000 changed bytes.
- Declared calculation calls: 3,072 positive-kernel panels across the two
  precision tiers, and zero Bessel, ODE, quadrature, root, finite-difference,
  sampling, compact-transfer or bisection calls.

After source commit `6542b38a57e6554f367b8fcea6e05a3c89f51d11`, the
first invocation through
`./ice run raw_c_qplus_to_qswitch_kappa_projective_sensitivity_transport`
exited `1` before any scientific calculation or result artifact. Python 3.13
required the dynamically loaded, hash-pinned helper module to be present in
`sys.modules` while its `@dataclass` decorators ran.

The loader-only compatibility fix leaves the input and mathematics unchanged.
Its corrected pre-run runner SHA-256 is
`82c34b981ea58abd8525b26c01ede0564562b0b9f360e96858baaee5e60ad2c7`.

After loader-fix commit `f1eb3bbc48213cea367b497a29535a856c6068b6`, the
same control-plane command exited `0` with `VALID_RUN`, but correctly emitted
`VALID_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_NOT_CERTIFIED`. All `22/22` exact
checks and all three theorem guards passed; `6/8` interval controls passed.
The raw result SHA-256 is
`c3f38b4fe7cc9d12b681b317e8914b8b1663739cd3395a7c524070693af0a1e2`
and its canonical payload SHA-256 without the self field is
`b6770ab63e478fc3033bedfed286ff41425d2149ad5f65e70ea361bf9bd8ae64`.

Both failed controls were the two precision copies of the same compound panel
refinement predicate. The 1,024-panel lower forcing bounds did increase over
the 512-panel bounds,

\[
0.368936766823655\ldots < 0.382928053028844\ldots,
\]

and all four individual transport rows plus the cross-precision strict-sign
intersection passed. The unnecessary final conjunct required separately
constructed outward `p` balls to be literally nested at their upper endpoints,
even though that upper comparison is panel-independent. Their stored uppers
differed by about $7.9\times10^{-11}$ from ball wrapping. Therefore the
observed strict interval

\[
-0.621029251873584<h(Q_{\rm switch})
<-0.382928052604288
\]

is retained as non-promoted evidence under this result's authoritative
`NOT_CERTIFIED` verdict. No ontology change follows from this run.

The checker-only correction replaces that compound predicate with exactly the
declared panel-refinement fact: the 1,024-panel right-endpoint lower sum must
be no smaller than the 512-panel lower sum. It does not relax any individual
strict-sign transport control, the cross-precision intersection, the panel or
precision ladder, input, upstream hash, cap, equation, or null boundary. The
corrected pre-run runner SHA-256 is
`87af6053f0651b007667ffb61d7b8e1f84d5c70cb272327e44b007896e094534`.
No checker-corrected execution is claimed before this source is committed.
