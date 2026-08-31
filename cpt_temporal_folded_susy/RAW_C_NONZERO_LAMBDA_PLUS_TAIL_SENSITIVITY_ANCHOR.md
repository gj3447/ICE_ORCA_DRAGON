# Raw-C nonzero-lambda plus-tail sensitivity anchor

This bounded calculation addresses one P1 admission gap only: the entering
value (s(4)=\partial_\lambda[-u_Q/u](4)) for the actual real
plus-recessive family.  It uses the existing uniform Liouville--Green bound
on the logarithmic derivative, but never differentiates that remainder.

For (u_{QQ}=Au), (s_Q=2gs-A_\lambda), where (g=-u_Q/u).  The forced
Wronskian gives the normalization-invariant identity

\[
s(4)=\int_4^\infty A_\lambda(t)\,[u(t)/u(4)]^2\,dt.
\]

The pinned LG envelope is reduced deliberately to coarse elementary bounds

\[
53e^Q\le g(Q)\le70e^Q\quad(Q\ge4),
\]

then integrated directly in this identity.  With (x=e^Q), the lower bound
uses (g\le70x) and \(\sqrt{x_0}>7\); the upper bound uses (g\ge53x) and
\(\sqrt{x_0+y}<15/2+y/14\).  The output interval is therefore outward but
intentionally broad.  It is checked to contain the independent
exact-(\lambda=0) Bessel/Green (h(4)) certificate for root bracket 1.

It does not provide panelwise rho tubes, transport from (Q=4) to (Q_0), a
declared (\Gamma_1) value or sign, root continuation, Weyl data, spectral
measure, RAQ, or a physical claim.
