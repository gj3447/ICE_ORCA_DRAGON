# Gate 1 — selected-\(H\) full-\(p\) regular-shell RAQ completion

## Result

For the already selected maximal multiplication operator

\[
h(\kappa,p)=3p^2-2\hbar^2\kappa^2
\]

on

\[
\mathcal H_{\mathrm{aux}}^{\mathrm{full}}
=L^2(\mathbb R_{+,\kappa}\times\mathbb R_p,d\kappa\,dp),
\]

the declared regular-shell test space has the scoped completion

\[
\overline{\Phi_{\mathrm{reg}}/\ker\eta_{\mathrm{reg}}}
\simeq L^2(\mathbb R,dx)_+\oplus L^2(\mathbb R,dx)_-.
\]

The observed verdict is

```text
KEEP_SELECTED_H_FULL_P_REGULAR_RAQ_DIRECT_SUM_NO_INHERITED_ORIGIN_ATOM
```

This closes the standard absolutely-continuous full-\(p\) completion only for the selected
\(H\), Lebesgue auxiliary measure and regular-shell form. It is not a uniqueness theorem against
separately adding an origin distribution, logarithmic finite part, parity/CPT quotient or branch-gluing
law. It supplies no raw-\(C\) ordering/domain, endpoint transform, absolute BFV measure, quantum-gravity,
physics or TOE conclusion.

## Exact regular-shell reduction

Write \(p=\sigma r\), with \(\sigma\in\{+1,-1\}\) and \(r>0\). The only positive-\(\kappa\)
root is

\[
\kappa_0(r)=\sqrt{\frac32}\frac r\hbar,
\qquad
\left|\partial_\kappa h\right|_{\kappa_0}
=2\sqrt6\,\hbar r.
\]

Regular coarea on the two disjoint rays therefore gives

\[
\eta_{\mathrm{reg}}(A,B)=
\sum_{\sigma=\pm1}\int_0^\infty
\frac{dr}{2\sqrt6\,\hbar r}\,
\overline{A\!\left(\kappa_0(r),\sigma r\right)}
B\!\left(\kappa_0(r),\sigma r\right).
\]

The \(p>0\) and \(p<0\) characteristic projectors are mutually orthogonal, so this form has no
cross-branch term. This statement does not impose a superselection rule: multiplication by
\(\operatorname{sgn}p\) distinguishes the branches, while parity is a unitary that exchanges them.
Restricting to an even or odd sector would be an additional quotient choice.

For any \(r_\star>0\), define

\[
x=\log(r/r_\star),\qquad
(U_\sigma A)(x)=
\frac{A\!\left(\kappa_0(r_\star e^x),\sigma r_\star e^x\right)}
{\sqrt{2\sqrt6\,\hbar}}.
\]

Since \(dr/r=dx\), \(U_+\oplus U_-\) is an exact isometry into the two \(L^2(dx)\) branches.
Compact smooth trace data in \(x\) extend to compact tubes about the regular rays, so their range is
dense. Replacing \(r_\star\) by \(q_\star\) only translates

\[
x\longmapsto x+\log(r_\star/q_\star),
\]

and hence changes no Hilbert-space completion.

## What happens at \(p=0\)

The ordinary branch coordinate sends

\[
r\to0^+\quad\Longleftrightarrow\quad x\to-\infty.
\]

Thus \(p=0\) is not a finite endpoint on either regular branch. Moreover, for the maximal
multiplication operator, \(E_h(\{0\})\) is multiplication by the indicator of the zero set of \(h\).
That zero set consists of two one-dimensional rays and their origin inside a two-dimensional Lebesgue
space, so its auxiliary measure is zero. There is no inherited normalizable zero eigenprojection and no
independent origin atom.

This is compatible with the earlier cutoff result: an on-shell amplitude nonzero at \(r=0\) has a
logarithmically divergent \(dr/r\) norm, while sufficiently vanishing amplitudes are ordinary \(L^2(dx)\)
tails. A separately declared origin-supported distribution or finite-part functional remains a different
quantization choice.

## Independent numerical checks

At \(\hbar=1\), the two witnesses were

\[
A_+(r)=r e^{-r},\qquad A_-(r)=2r^2e^{-r/2}.
\]

Their exact norms are respectively

\[
\frac{1}{8\sqrt6},\qquad \frac{12}{\sqrt6}.
\]

Direct \(r\)-quadrature and independent \(x\)-coordinate quadrature at
\(r_\star=1\) and \(r_\star=7/5\) all passed. The \(x\) checks used the fixed interval
\([-30,8]\); the omitted tails were compared with the full exact norms and stayed below the declared
\(10^{-24}\) absolute tolerance. The run used six quadratures, no root calls and no ODE calls.

## Execution and reproduction record

The initial committed runner attempted 80-digit infinite-\(x\)-interval quadrature. The controlled shell
terminated it at the 120-second wall-clock cap and no result artifact was written. Commit `01a4b7a`
replaced only that slow implementation with a fixed finite interval and explicit tail error; it changed no
scientific predicate.

The successful observed commands were

```text
./ice run gate1_v0_full_p_regular_raq_completion
VALID_RUN; 9/9 executable exact checks; 6/6 numerical checks;
6 analytic hypothesis/scope guards

./ice repro --only gate1_v0_full_p_regular_raq_completion
REPRO; 1 checked; 0 needs-attention

npm run check
67/67 tests passed
```

The input, runner and raw result are

- `GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_INPUTS.json`
- `gate1_v0_full_p_regular_raq_completion.py`
- `GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_RESULT.json`

## Remaining independent questions

This result does not automatically authorize or answer the next work unit. In particular, it leaves open:

- the raw-\(C\) minimal operator, boundary form, deficiency indices and measurable extension family;
- raw-\(C\leftrightarrow H\) rigging-map and observable equivalence;
- any separately justified origin sector or cross-branch gluing law;
- a raw-\(C\) or support-restricted exact endpoint intertwiner;
- an absolute BFV measure, closed-\(S^3\) constraint algebra, quantum anomaly, relational observables,
  semiclassical/decoherence control and empirical likelihood.

The full eight-stage ordering and literature boundaries are recorded in
`GATE1_V0_SIX_BRIDGE_LITERATURE_MAP_2026-08-28.md` and the local research graph.
