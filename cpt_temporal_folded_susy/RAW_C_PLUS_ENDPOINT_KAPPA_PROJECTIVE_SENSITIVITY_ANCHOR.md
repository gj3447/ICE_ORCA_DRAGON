# Raw-C plus-end kappa projective-sensitivity anchor

## Independent question

On the already certified correlated $K\times\Lambda$ strip, let $u$ be the
same selected real plus-recessive family and define

\[
\rho=-\frac{u_Q}{u}-6\pi^2e^Q-\frac12,
\qquad h=\partial_\kappa\rho.
\]

This bounded calculation asks only whether $h(4)$ has a finite uniform
strictly negative enclosure. It does not transport that derivative toward the
declared boundary.

## Two-parameter bridge

No differentiability of the singular-endpoint family is assumed. Hold
$\lambda$ fixed. For $\kappa_a<\kappa_b$, normalize
$v_i(Q)=u_i(Q)/u_i(4)$ and put $r_i=-u_{i,Q}/u_i$. The exact Wronskian
identity and the pinned tail envelope give

\[
\frac{r_b(4)-r_a(4)}{\kappa_b-\kappa_a}
=-(\kappa_a+\kappa_b)\int_4^\infty v_a(Q)v_b(Q)\,dQ.
\]

Indeed, $W(u_a,u_b)_Q=-(\kappa_b^2-\kappa_a^2)u_au_b$ and
$W/(u_au_b)=-(r_b-r_a)$. The envelope makes the Wronskian boundary term
vanish at infinity. The same formula at every finite $Q$ is a uniform local
Lipschitz bound in $\kappa$. Hence the normalized directions converge on
every finite interval, while the common integrable tail dominator controls
the rest. Dominated convergence gives the same limit from
$\kappa_a\uparrow\kappa$ and $\kappa_b\downarrow\kappa$. Thus the derivative
is two-sided at every corridor-interior point and one-sided at the two faces.

## Forced-Wronskian derivative

After the secant limit has established differentiability, put
$w=\partial_\kappa u$. Then $A_\kappa=-2\kappa$, and with
$W(u,w)=u w_Q-u_Qw$,

\[
W_Q=-2\kappa u^2,
\qquad
h=-\frac{W}{u^2}.
\]

Taking $\kappa_b\to\kappa_a=\kappa$ in the secant formula gives

\[
h(4)=-2\kappa\int_4^\infty
\left(\frac{u(Q)}{u(4)}\right)^2dQ<0.
\]

The previously audited full-strip envelope
$53e^Q\le -u_Q/u\le70e^Q$ bounds this scale-free integral. With
$y=e^Q-e^4$ and $dQ=dy/(e^4+y)$, the frozen rational relaxations use
$e^4>49$, $e^4+1/140<57$, and $e^{-1}>1/3$, giving

\[
\frac1{23940}<
u(4)^{-2}\int_4^\infty u(Q)^2dQ
<\frac1{5194}.
\]

## Explicit boundary

Even a successful endpoint sign does not certify
$\partial_\kappa G$. The backward switch transfer, differentiated $Q_0$
chart, kappa derivative of the reference solution, and complete
kappa-differentiated minus tail remain separate obligations. Root uniqueness,
a continuous selector, velocity, global roots, absolute $\Gamma_1$ amplitude or
sign, Weyl/spectral data, RAQ, and physics remain null.

## Controlled execution

- Frozen input SHA-256:
  `55bc49884d678719eda2a0e02dbdc028e15b2e52b1d3ca8558b51cd1c5c5becd`
- Frozen runner SHA-256:
  `7259aafee080dc9df96c341076856e23e01ef76e238e98a1d5e6c568a872a2c8`
- Source commit:
  `00049dc8d542065a7192be66eff476ed76efc231`
- Command:
  `./ice run raw_c_plus_endpoint_kappa_projective_sensitivity_anchor`
- Exit code: `0`; run status: `VALID_RUN`; verdict:
  `CERTIFY_UNIFORM_NEGATIVE_PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_ANCHOR`.
- Checks: `21/21` exact checks and all three theorem guards passed. No ODE,
  quadrature, root solve, finite difference, sample, panel, Bessel call or
  bisection was used.
- Result SHA-256:
  `adb89d5bba7e5abbc4870077ae1d4bd75ecb2547d0e02721769aef1fc390e2ca`
- Canonical payload SHA-256 without the self field:
  `152b077a8529df8f8189c875b43730ae9ec3adea47a45a3444ce35f551ca3f6e`.

The resulting strict uniform enclosure is

\[
-0.000779178759705569123<h(4)<-0.000168882810271960151.
\]

This is a repository-local exact analytic certificate for the declared strip,
not a physics observation. The explicit boundary above remains unchanged.

Post-run validation:

- the canonical payload hash recomputed exactly;
- `./ice ontology validate` returned `VALID`, `427/427` hashes, zero errors
  and the 70 already-unresolved external bridge warnings;
- the new claim's `ontology show` and `ontology trace` stop at the endpoint
  anchor and retained open transport node;
- `npm run check` passed strict TypeScript and all `69/69` Vitest tests.
