# Raw-C correlated kappa-lambda Gamma_1 sign strip

## Fixed question

Let the closed lambda slab be

\[
\Lambda=[-10^{-4},10^{-4}],
\]

and let the closed kappa corridor be the first certified lambda-zero root
bracket enlarged by exactly (10^{-3}) on each side. This bounded calculation
asks whether the same selected real plus-recessive family has a nonzero
(Q_0=-4) chart throughout (K\times\Lambda), and whether its complete
(Q_0)-normalized declared boundary functional has strict opposite signs on
the two kappa faces.

If both facts and joint continuity are certified, the intermediate value
theorem gives

\[
\forall\lambda\in\Lambda\;\exists\kappa_\lambda\in\operatorname{int}K:
G(\kappa_\lambda,\lambda)=0,
\qquad
G=\frac{\Gamma_{1,\kappa}(u_+)}{u_+(Q_0)}.
\]

Because the same calculation must exclude zero from (u_+(Q_0)), a zero of
(G) is equivalent to a zero of the selected declared (Gamma_1). This is
only an existence statement; it does not select a root as lambda changes.

## Recomputed bridge

The microscopic root-bracket (Q_0) result is not widened by assertion. The
runner recomputes the necessary bridge on the expanded corridor:

1. recheck the forced-Wronskian plus-tail sensitivity enclosure from the
   pinned Liouville--Green real box;
2. evaluate the lambda-zero Bessel direction on the whole corridor and on
   both exact faces;
3. transport the affine mean-sensitivity enclosure to
   (Q_{\rm switch}=-29/10) with 512/1024 monotone kernel panels;
4. propagate the corridor and both faces from the switch to (Q_0) with
   order-12 whole-step interval Taylor enclosures, requiring the entire
   corridor amplitude to exclude zero;
5. propagate only the two faces to (Q_c=-5,-6), add analytic rotating-frame
   tail radii, and require strict opposite complete-functional signs.

The calculation uses 80- and 120-decimal Arb tiers. It makes no black-box ODE,
quadrature, root, finite-difference, sampling, or bisection call.

## Theorem boundary

Continuity is used only after the selected actual family is linked to the
uniform plus-end construction, the finite parameter-dependent transfers are
covered, the (Q_0) denominator is uniformly nonzero, and the omitted tail is
uniformly absolutely dominated by the displayed rotating-frame masses. The
face signs are the executable hypotheses of the intermediate value theorem.
Neither a product-box enclosure containing zero nor the previously computed
local lambda derivative is treated as a root curve.

## Explicit nonclaims

The following remain null even if the sign strip certifies: root uniqueness,
a continuous/correlated root selector, continuation, root velocity or a
kappa derivative, roots outside the corridor, a global root census, absolute
actual Gamma_1 amplitudes or signs away from the two faces and roots, a
nonreal Weyl function, spectral measure, RAQ/physical product, constraint
equivalence, BFV closure, empirical likelihood, or any physics claim.

## Controlled execution

The frozen input SHA-256 is
`d622cc761786dc0197578ce2b6d9e0cb8a2783d062f4881a942c4300d3ae56e9`;
the pre-run source SHA-256 is
`998de91dcf68033acc457cac37b535555fa401df32d893e63a47cfb2c77d63a2`.
The common control-plane wall/stdout/stderr/artifact caps are 120 seconds,
262,144 bytes, 262,144 bytes, and 12 files/1,000,000 bytes.

### First execution: valid run, sign strip not certified

After source commit `8bf680d`, the runner was executed exactly through

```text
./ice run raw_c_correlated_kappa_lambda_gamma1_sign_strip
```

It finished in about 2.6 seconds with `VALID_RUN` and verdict
`CORRELATED_GAMMA1_SIGN_STRIP_NOT_CERTIFIED`. All 24 exact checks passed;
62/66 controls passed. The four failures were the two precision copies of
the closed-corridor barrier and domain-seed controls. The broad-kappa
Bessel/affine switch enclosure was

\[
[-1.1050280244,-1.50338\times10^{-5}],
\]

so its lower endpoint missed the analytic barrier $[-1,1]$ by about 0.105.
This is interval wrapping across the full kappa corridor, not a certified
barrier violation: the newly evaluated $Q=4$ start lies inside
$[-0.009224,0.007882]$, and all inward vector-field margins are strictly
positive. The runner nevertheless failed closed because it had required the
raw switch enclosure itself to lie in $[-1,1]$, rather than intersecting it
with the independently proved invariant barrier.

The downstream finite calculations were informative but do not override the
failed verdict. The whole-corridor switch-normalized $Q_0$ amplitude was
strictly positive,

\[
v(Q_0)\in[4.4433575664,6.1722302344],
\]

and the completed face functionals had strict opposite signs,

\[
G(\kappa_L,\Lambda)\subset
[-0.00234624001,-0.00199293383],\qquad
G(\kappa_R,\Lambda)\subset
[0.00199518992,0.00235059808].
\]

The raw result file SHA-256 is
`7afdc98aa14dfaa21629735701a015015034ab4bde8f306db34d3b2d68803105`;
its payload SHA-256 is
`5c69d48209a258e6429b7932425b2f7cb9e35fb5652fa780eb13f9f1bef66ca1`.
No root-existence output is certified by this first execution. The narrow
same-question correction is to use the intersection of the raw affine switch
enclosure with the already audited invariant barrier before the $Q_0$
transfer. The first failed result is preserved in commit `f546af6`.

### Barrier-intersection correction prepared

The corrected runner proves the invariant barrier from the $Q=4$ selected
actual-family seed and the strict inward vector-field margins alone. It then
records the raw affine switch enclosure separately and sends only

\[
I_{\rm switch}^{\rm raw}\cap[-1,1]
\]

to the switch-to-$Q_0$ transfer. This is an intersection of two independently
valid enclosures of the same actual direction, not clipping an unwanted
endpoint. The corrected frozen input SHA-256 is
`175372c15b21d9c3082e8befdc3cf79e5c99e8f0685850552d343163cd6ffd3e`;
the corrected pre-run source SHA-256 is
`9820a8786502cbf9584cfd4dbb703bd35a490fe52d5f34c31a4a0e1161639bf3`.
No corrected execution is claimed until these changes are committed and run
through `./ice run`.
