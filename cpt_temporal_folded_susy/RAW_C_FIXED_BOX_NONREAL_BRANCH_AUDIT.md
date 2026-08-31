# Raw-C fixed-box nonreal branch audit

## Question and scope

For (p=0), (Q\ge4), and the one upper-half-plane box

\[
\operatorname{Re}z\in[-1/16,1/16],\qquad
\operatorname{Im}z\in[15/16,17/16],
\]

this bounded audit checks only whether the principal branch of

\[
A(Q,z)=36\pi^4e^{2Q}\left(1+\frac{ze^{-Q/2}}{6\pi^2}\right)
\]

is separated from the nonpositive-real cut and has positive real part.  The
nonreal raw-C coefficient convention is hash-pinned from
[`RAW_C_NONREAL_WEYL_PROXY_INPUTS.json`](RAW_C_NONREAL_WEYL_PROXY_INPUTS.json)
as provenance; its finite double-precision proxy is not used as a proof.

The operator-theoretic scope reference is
[Eckhardt--Gesztesy--Nichols--Teschl, arXiv:1208.4677](https://arxiv.org/abs/1208.4677).
It supplies singular Weyl--Titchmarsh terminology and does not supply a
model-specific endpoint enclosure.

## Three controls

1. Exact factorization and the strictly negative derivative
   \(d e^{-Q/2}/dQ=-e^{-Q/2}/2\) show that the
   (Q=4) box bounds all (Q\ge4).
2. `python-flint==0.9.0` evaluates outward `acb` rectangles at 128 and 256
   bits; each must be finite, remain inside the unit relative-perturbation
   disc, have positive cut distance, and give positive
   \(\operatorname{Re}\sqrt A\).  Their overlap is same-backend
   consistency, not independent evidence.
3. Executable exact SymPy inequalities
   \(\sqrt{290}/16<9/8\), \(e^{-2}<1/7\), and \(\pi^2>9\) give
   (|\delta|<1/336), hence distance from (1+\delta) to the nonpositive
   real axis exceeds (335/336).  Both ball tiers must be at least as sharp.

The corresponding half-line lower bound is

\[
\operatorname{Re}\sqrt{A(Q,z)}
\ge6\pi^2e^4\sqrt{335/336}>0.
\]

The recorded analytic guard uses the principal-branch identity
\(\operatorname{Re}\sqrt w^2=(|w|+\operatorname{Re}w)/2\).  Since
\(\operatorname{Re}w\ge1-|\delta|\), it gives
\(\operatorname{Re}\sqrt w\ge\sqrt{1-|\delta|}\).  This is elementary
branch algebra, not a complex-tail or endpoint theorem.

## Fail-closed boundary

This audit has no root solver, characteristic equation, boundary map, ODE,
quadrature, or real-axis sample.  It therefore cannot be a real-root result.
It does **not** enclose the actual recessive endpoint datum, construct a
singular Weyl (m(z)), a spectral measure or multiplicity, Stieltjes
inversion, a rigging map/RAQ product, or a (C/H) comparison.  Those outputs
remain explicit nulls in the result.

Run only after the runner and input are cleanly committed:

```text
./ice run raw_c_fixed_box_nonreal_branch_audit
```
