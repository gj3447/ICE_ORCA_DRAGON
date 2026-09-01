# Raw-\(C\) fixed-\(\lambda\) root-theorem composition

## Narrow question

Can the independently certified opposite-face sign strip and complete positive
\(\partial_\kappa G\) interval be composed for exactly the same selected
normalized real functional, without recomputing either calculation, to prove
one unique \(\kappa\)-transverse zero for every fixed \(\lambda\) in the
declared slab?

The answer is allowed to concern only

\[
G(\kappa,\lambda)
=\frac{\Gamma_{1,\kappa}(u_+)}{u_+(Q_0)}
=-\lim_{Q\to-\infty}W(U,c_\kappa)
\]

on the exact expanded root-1 corridor and
\(\Lambda=[-10^{-4},10^{-4}]\). It is not a global root census or a
nonreal spectral question.

## Pinned independent inputs

The audit consumes only these two unnumbered `VALID_RUN` artifacts:

1. `RAW_C_CORRELATED_KAPPA_LAMBDA_GAMMA1_SIGN_STRIP_RESULT.json`, raw
   SHA-256
   `e1a3245b6d00799ce378c2b4f509e6e6d1452e95998937421d0a8dc6696f6dc2`.
   It supplies joint continuity, a uniformly nonzero \(Q_0\) projective chart,
   and strict complete values
   \(G(\kappa_L,\lambda)<0<G(\kappa_R,\lambda)\) for every declared
   \(\lambda\).
2. `RAW_C_COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_RESULT.json`, raw
   SHA-256
   `ad61dee6f84f9f1edf409f26d9f78dfeb1ebd47142bd3e39f2a5f5fe78dbc6a8`.
   It supplies ordinary fixed-\(\lambda\) differentiability in the open
   corridor and

   \[
   1.28166841529309749603271484375
   \le \partial_\kappa G \le
   3.85497434251010417938232421875.
   \]

The runner recomputes both canonical self-payload hashes and rejects numbered,
non-`VALID_RUN`, schema-mutated or verdict-mutated inputs.

## Exact scope bridge

The two files agree exactly on \(Q_0=-4\), both rational corridor endpoints,
the rational lambda slab, the selected Liouville--Green real plus family and
the complete normalized functional displayed above. The sign-strip file uses
the historical symbol \(c_p\), but it also fixes

\[
p^2=\frac23\kappa^2,\qquad A_0=x^2-\kappa^2,
\]

and explicitly identifies that reference as \(c_\kappa\) on the positive real
kappa corridor. The audit checks this instantiation rather than pretending the
two historical strings are lexically identical. The common nonzero
\(u_+(Q_0)\) chart makes normalized \(G\) and the selected declared
\(\Gamma_1\) have exactly the same zeros on this rectangle; it does not fix an
absolute \(\Gamma_1\) amplitude or orientation.

## Calculus composition

Fix any \(\lambda\in\Lambda\). Joint continuity and the two strict face signs
give an interior zero by the intermediate value theorem. If two different
zeros \(\kappa_1<\kappa_2\) existed, the mean value theorem would give some
\(\xi\in(\kappa_1,\kappa_2)\) with

\[
0=\frac{G(\kappa_2,\lambda)-G(\kappa_1,\lambda)}
        {\kappa_2-\kappa_1}
=\partial_\kappa G(\xi,\lambda),
\]

contradicting the certified positive lower bound. Thus the zero is unique and,
because it lies in the open corridor where the ordinary derivative exists,
it is simple and transverse with respect to the \(\kappa\) direction.

There is also one immediate topological corollary. If
\(\lambda_n\to\lambda\), compactness gives a convergent subsequence of the
unique roots. Joint continuity makes its limit a root at \(\lambda\), and
uniqueness forces that limit to be the unique root there. Every subsequence has
the same limit, so the unique roots define a continuous selector
\(\kappa_*(\lambda)\) on the closed slab. This is continuity only. No
\(C^1\), differentiable or analytic selector and no velocity formula is
claimed.

## Fail-closed boundary

The audit deliberately performs zero ODE, quadrature, root, finite-difference,
sampling, bisection, Bessel, interval-row or nonreal evaluations. It emits no
root locations. In particular, it does not supply

- \(\partial_\lambda G\), a mixed derivative or
  \(\kappa_*'(\lambda)=-G_\lambda/G_\kappa\);
- roots outside the declared corridor or a global census;
- absolute actual-\(\Gamma_1\) amplitude/orientation;
- a selected measurable raw-\(C\) self-adjoint extension, nonreal Weyl
  \(m(z)\), spectral measure/multiplicity, RAQ, \(C/H\) quantum equivalence,
  BFV, empirical or physics result.

## Frozen execution

The input manifest SHA-256 is
`ad549c523fb5f06d43eeccd5a7299478fd0ca3a3bff445d6cbc13cfe2b4758a5`;
the source-only runner SHA-256 is
`d24f76446bc28697fb9c3a3ac2d324bf5bfa57b53cc681f89754211f196659cc`.
`uv run python -m py_compile` and `git diff --check` pass. The controlled
command

```text
./ice run raw_c_fixed_lambda_root_theorem_composition
```

is withheld until the input, runner and this scope report are committed from a
clean core tree.
