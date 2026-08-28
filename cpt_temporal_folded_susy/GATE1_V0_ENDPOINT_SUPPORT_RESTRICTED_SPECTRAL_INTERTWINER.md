# Gate 1 — selected-H support-restricted spectral intertwiner

## Result

For the selected densitized H spectral multiplier on the `p>0` component,

\[
h(\kappa,p)=3p^2-2\hbar^2\kappa^2,
\]

the exact spectral-coordinate map is unitary only to

\[
Y_+=\{(c,p):p>0,\ c<3p^2\}.
\]

The observed verdict is:

```text
NARROW_V0_SELECTED_H_EXACT_SPECTRAL_INTERTWINER_REQUIRES_SUPPORT_RESTRICTED_TARGET
```

This is an exact coordinate result for the selected H realization. It is not a
raw-C quantization, raw-C rigging map, physical inner product, or endpoint-state
transform. It does not identify with, repair, or replace the separate
`W(c,P,p)` one-term endpoint FIO; that FIO's exact-unitarity KILL remains in force.

## Coordinate unitary and zero fiber

On

\[
X_+=(0,\infty)_\kappa\times(0,\infty)_p,
\qquad \mathcal H_X=L^2(X_+,d\kappa\,dp),
\]

the map, inverse, and positive Jacobian are

\[
c=h(\kappa,p),\qquad
\kappa(c,p)=\sqrt{\frac{3p^2-c}{2\hbar^2}},\qquad
J=\left|\partial_\kappa h\right|=4\hbar^2\kappa.
\]

Consequently,

\[
(VA)(c,p)=J(c,p)^{-1/2}A(\kappa(c,p),p),
\qquad
(V^{-1}F)(\kappa,p)=\sqrt{J(\kappa,p)}F(h(\kappa,p),p)
\]

is an exact unitary from (L^2(d\kappa\,dp)) to (L^2(Y_+,dc\,dp)). The
spectral graph kernel

\[
\delta(p-p')\sqrt{J(\kappa,p)}\,\delta\!\left(c-h(\kappa,p)\right)
\]

has the same normalization: the one-dimensional coarea factor converts
(sqrt J) into (J^{-1/2}). It intertwines (M_h\leftrightarrow M_{c,<})
and (p\leftrightarrow p), including their maximal multiplication domains.

At the zero fiber,

\[
\kappa_0(p)=\sqrt{\frac32}\frac p\hbar,
\qquad J(\kappa_0,p)=2\sqrt6\,\hbar p,
\]

so the (dc) delta-fiber form pulls back to

\[
\frac{dp}{2\sqrt6\,\hbar p}.
\]

This reproduces the selected-H RAQ shell weight on the shared compact-interior
test class only. It is not a bounded delta projector or raw-C physical product.

## Unrestricted-target obstruction

The previously declared comparison target is

\[
\mathcal H_D=L^2(\mathbb R_c\times(0,\infty)_p,dc\,dp).
\]

Its complement to (Y_+) contains

\[
E=\{(c,p):p>0,\ c\ge3p^2\}.
\]

The witness

\[
\mathbf 1_{\{1<p<2,\ 4p^2<c<5p^2\}}
\]

lies in (E), with squared norm

\[
\int_1^2dp\int_{4p^2}^{5p^2}dc=\frac73>0.
\]

Every source point instead satisfies (h(\kappa,p)<3p^2). Thus no exact
unitary can simultaneously intertwine selected H with unrestricted (M_c) and
preserve (p): it would have to map a zero source joint-spectral projection to
a nonzero target one. This does not rule out a unitary that abandons (p)
preservation.

## Bounded scope and record

All seven exact checks and five analytic hypothesis/scope guards passed. The
FIO wording is only a compact-interior spectral graph interpretation, with
(\kappa>0) bounded away from zero. It provides no global assertion at
(\kappa=0) or (c=3p^2), no Maslov gluing, no `p<0` import, and no origin atom.

```text
./ice run gate1_v0_endpoint_support_restricted_spectral_intertwiner
VALID_RUN; 7/7 exact checks; 5 analytic hypothesis/scope guards

./ice repro --only gate1_v0_endpoint_support_restricted_spectral_intertwiner
REPRO; 1 checked; 0 needs-attention
```

Definition commit: `9230bb472a584e6005dfb3b710d53940c6da7f74`.
Result commit: `3c0c5ceaa950357fa56b8aacbc48208bb6a73308`
(2026-08-28T07:27:30Z). Reproduction mapping commit:
`974ded457d1357159d7eb05c2624e091a6bd390f`.

The pinned input, runner and raw result are

- `GATE1_V0_ENDPOINT_SUPPORT_RESTRICTED_SPECTRAL_INTERTWINER_INPUTS.json`
- `gate1_v0_endpoint_support_restricted_spectral_intertwiner.py`
- `GATE1_V0_ENDPOINT_SUPPORT_RESTRICTED_SPECTRAL_INTERTWINER_RESULT.json`

## Still null

Raw-C operator/domain and (C\leftrightarrow H) equivalence, a W full symbol or
endpoint-state transform, global (\kappa=0) completion, cross-branch gluing,
absolute BFV measure, anomaly, relational/semi-classical observables,
likelihood, quantum-gravity, physics, and TOE claims remain null. No automatic
next calculation is authorized.
