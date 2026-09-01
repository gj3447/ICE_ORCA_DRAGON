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

## Controlled source freeze

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

The first result-producing command is deliberately withheld until these
source files are committed from a clean core tree.

## Explicit boundary

The only intended output is a complete real normalized
$\partial_\kappa G$ interval on the declared rectangle, with the signed
integral magnitude and lambda-multiplied tail radius shown separately.

Even if the interval excludes zero, this calculation does not itself compose
the earlier existence strip into transversality, monotonicity, uniqueness, a
root selector, continuation or velocity. It also supplies no absolute actual
$\Gamma_1$ amplitude/sign, roots outside the corridor, nonreal Weyl
$m$-function, spectral measure, RAQ, BFV, empirical or physical result.
