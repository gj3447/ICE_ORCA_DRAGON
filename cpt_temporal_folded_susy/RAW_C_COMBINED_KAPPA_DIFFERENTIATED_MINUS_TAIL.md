# Raw-C combined kappa-differentiated minus tail

## Independent question

On the exact current real $K\times\Lambda$ rectangle, can the already
certified $Q_0$ projective kappa-sensitivity seed and the fixed-reference
variation close the entire differentiated minus-end Wronskian tail and give a
complete outward interval for $\partial_\kappa G$?

This is one bounded, numberless workbench calculation. It does not compose a
root theorem or start a descendant calculation.

## Exact combined identity

Use the repository convention

\[
W(f,g)=f g_Q-f_Qg,
\qquad
G(\kappa,\lambda)=-\lim_{Q\to-\infty}W(U,c_\kappa).
\]

With

\[
U_{QQ}=(V+\lambda a-\kappa^2)U,
\qquad
c_{\kappa,QQ}=(V-\kappa^2)c_\kappa,
\]

set $Z=\partial_\kappa U$ and $D=\partial_\kappa c_\kappa$. Then

\[
Z_{QQ}=(V+\lambda a-\kappa^2)Z-2\kappa U,
\qquad
D_{QQ}=(V-\kappa^2)D-2\kappa c_\kappa.
\]

The combined differentiated Wronskian

\[
H=W(Z,c_\kappa)+W(U,D)
\]

obeys

\[
H_Q=-\lambda a(Zc_\kappa+UD).
\]

The two $2\kappa Uc_\kappa$ terms cancel exactly. At $Q_0=-4$, the
hash-pinned normalized data are

\[
U=1,\quad Z=0,\quad Z_Q=-h,\quad
c_\kappa=1,\quad c_{\kappa,Q}=D=D_Q=0,
\]

so $H(Q_0)=h(Q_0)$. Consequently, with the signed integral

\[
I_{\rm signed}=\int_{-\infty}^{Q_0}
a(Zc_\kappa+UD)\,dQ,
\]

the sign fixed by the displayed Wronskian convention is

\[
\boxed{\partial_\kappa G=-h(Q_0)-\lambda I_{\rm signed}}.
\]

The singular Weyl--Titchmarsh source is used only for the scope of singular
Wronskian boundary values. It does not supply this derivative identity and it
does not turn the real calculation into a Weyl $m$-function.

## Why no cutoff propagation is needed

An initial design propagated the eight states
$(U,U_Q,Z,Z_Q,c,c_Q,D,D_Q)$ to finite cutoffs. A smaller complete bound is
available by taking the comparison start itself to be $Q_c=Q_0$.

For the rotating norm

\[
R_y=\sqrt{y^2+(y_Q/\kappa)^2},
\]

the free part is skew. With

\[
A_0=\int_{-\infty}^{Q_0}a\,dQ=4\pi^2e^{-6},
\quad
A_1=\int_{-\infty}^{Q_0}a(Q_0-Q)\,dQ=\frac23A_0,
\]

\[
V_0=\int_{-\infty}^{Q_0}V\,dQ=18\pi^4e^{-8},
\]

define

\[
q_U=\frac{V_0+|\lambda|A_0}{\kappa_{\min}},
\qquad
q_c=\frac{V_0}{\kappa_{\min}},
\]

\[
R_U=R_U(Q_0)e^{q_U},
\qquad
R_c=e^{q_c},
\qquad
R_{Z,0}=\frac{|h(Q_0)|}{\kappa_{\min}}.
\]

Rotating-frame Gronwall and variation of constants give, for
$t=Q_0-Q\ge0$,

\[
|U|\le R_U,\qquad |c_\kappa|\le R_c,
\]

\[
|Z|\le e^{q_U}R_{Z,0}+2R_Ut,
\qquad
|D|\le2R_ct.
\]

The exponent composition across the Duhamel split is exact; no second
full-tail exponent is needed on the forcing term. Hence

\[
|I_{\rm signed}|\le
R_c\left(e^{q_U}R_{Z,0}A_0+2R_UA_1\right)
+R_U\left(2R_cA_1\right).
\]

For the $UD$ term, the independently certified reference envelope also gives

\[
\int a|UD|\,dQ
\le R_U\sqrt{A_0}\,\|D\|_{L^2(a)},
\qquad
\|D\|_{L^2(a)}\le1.055544862153.
\]

The runner evaluates both valid $UD$ bounds and uses the smaller outward
upper endpoint. Because $a(Q)(1+Q_0-Q)$ is integrable, the same estimates give
a uniform dominator for the differentiated improper Wronskian limit.

If $B\ge|I_{\rm signed}|$, the computed interval is

\[
\partial_\kappa G
\in-h(Q_0)+[-|\lambda|B,+|\lambda|B].
\]

At $\lambda=0$, this reduces exactly to the independent regression
$\partial_\kappa G=-h(Q_0)$.

## Initial controlled source freeze

Before any result-producing execution:

- input SHA-256:
  `d5f8798e06087056baa4f62721a2c7b0509471a84f224893b42b67147d3146dc`;
- runner SHA-256:
  `4774418393de8f453731efa8b92a4c43b083c068335128d0bf6b4ac8f08400fe`;
- `jq empty` passed for the manifest;
- `uv run python -m py_compile` passed for the runner;
- `./ice list --json` discovered the numberless runner;
- independent mathematics, source-scope and static code audits accepted the
  global $Q_0$ shortcut, corrected the Wronskian sign, unified the coefficient
  notation, and required full upstream execution-scope/self-hash checks.

The source-only freeze was committed as `24b95cf`. No result-producing command
ran before that commit.

## First controlled execution — fail closed

The first command

```text
./ice run raw_c_combined_kappa_differentiated_minus_tail
```

exited zero and wrote a `VALID_RUN`, but correctly refused certification:

- verdict: `COMBINED_KAPPA_DIFFERENTIATED_MINUS_TAIL_NOT_CERTIFIED`;
- exact/structural checks: 18/18;
- outward controls: 4/6;
- theorem guards: 5;
- raw result SHA-256:
  `615ee6de1cb9377f85a85e36e8bb985256d29aab842fae18509ef79999640254`;
- canonical payload SHA-256:
  `f9ccb1cafc14aa2a83cb3b769b8b854ac96ba46b0e9e3e36c46dda9e56dd89b2`.

Both elementary rows were finite and gave the same displayed strict-positive
complete interval. The failed controls were bookkeeping: scalar radii that
are *one-sided upper bounds* had been treated as set enclosures and required
to intersect across precisions. Their tiny precision-dependent outward
rounding balls need not intersect, even though each upper endpoint is valid.
This also made the aggregate radius `null` and forced the final control false.
The failure result is preserved in commit `969e33c` rather than overwritten in
history.

## Minimal control correction

The corrected runner requires cross-precision overlap only for the actual set
enclosures, namely $-h$ and the completed $\partial_\kappa G$ interval. For
one-sided magnitude bounds it records the conservative maximum of the two
valid upper endpoints. No equation, analytic bound, input, upstream pin,
resource cap, row value, verdict logic or fail-closed output changed.

The corrected runner SHA-256 is
`715e3c91cd22963c484671b421dad9f77630813d7befdf415780995562f11c41`;
`uv run python -m py_compile` and `git diff --check` passed. The second
controlled execution was withheld until this correction was committed.

## Corrected controlled execution — complete positive interval

The correction was committed as `f591484`. Running the same command from that
clean committed source produced:

- verdict:
  `CERTIFY_COMPLETE_UNIFORM_POSITIVE_NORMALIZED_G_KAPPA_INTERVAL_ONLY`;
- exact or structural checks: 18/18;
- outward controls: 6/6;
- theorem guards: 5;
- selected direct first-moment $UD$ bound:
  $0.235658847388127281023384253040$;
- independent $L^2$ Cauchy--Schwarz $UD$ bound:
  $0.445822534577852224868895031531$;
- complete signed-integral magnitude bound:
  $|I_{\rm signed}|\le0.805246826915456777116778778611$;
- lambda-multiplied complete-tail radius:
  $|\lambda I_{\rm signed}|\le8.0524682691545678\times10^{-5}$;
- complete normalized derivative interval:

  \[
  1.28166841529309749603271484375
  \le \partial_\kappa G \le
  3.85497434251010417938232421875.
  \]

The interval is strictly positive on the corridor interior, with the
corresponding one-sided derivative intervals at the two faces. The raw result
is 32,191 bytes with SHA-256
`ad61dee6f84f9f1edf409f26d9f78dfeb1ebd47142bd3e39f2a5f5fe78dbc6a8`.
Deleting its self-digest and canonicalizing compact sorted JSON reproduces
payload SHA-256
`eb38cbdd6e30c56c6c7acfe408ec3ac461ab19ff0b7fcd24508a8ff051c3d24d`.

This closes the complete combined-tail/$G_\kappa$ calculation only. The
independently supported at-least-one-root strip was not consumed as a theorem
hypothesis by this runner. A separate scope-and-theorem audit is the next open
question before transversality or uniqueness; no automatic descendant was
started.

## Explicit boundary

The only intended output is a complete real normalized
$\partial_\kappa G$ interval on the declared rectangle, with the signed
integral magnitude and lambda-multiplied tail radius shown separately.

Even if the interval excludes zero, this calculation does not itself compose
the earlier existence strip into transversality, monotonicity, uniqueness, a
root selector, continuation or velocity. It also supplies no absolute actual
$\Gamma_1$ amplitude/sign, roots outside the corridor, nonreal Weyl
$m$-function, spectral measure, RAQ, BFV, empirical or physical result.

## Completion audit

The completion bundle was checked independently against the input, runner,
raw result and compact ontology evidence. The result self-payload digest was
recomputed as
`eb38cbdd6e30c56c6c7acfe408ec3ac461ab19ff0b7fcd24508a8ff051c3d24d`;
all 18 exact or structural checks, all six controls and all five theorem guards
pass, and every required out-of-scope output remains `null`.

`./ice ontology validate` reports a valid four-graph collection with 432/432
stored hashes verified; its 70 warnings are the already-recorded unresolved
external bridges. `npm run check` passes strict TypeScript and all 69 Vitest
tests. `uv run python -m py_compile
cpt_temporal_folded_susy/raw_c_combined_kappa_differentiated_minus_tail.py`
and `git diff --check` also pass.
