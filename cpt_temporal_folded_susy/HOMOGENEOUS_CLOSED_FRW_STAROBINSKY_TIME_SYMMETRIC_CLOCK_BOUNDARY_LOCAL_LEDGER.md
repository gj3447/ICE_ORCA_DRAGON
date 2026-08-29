# Local \(P=0\) Starobinsky clock-boundary vector-field ledger

This unnumbered calculation is deliberately smaller than a trajectory audit.
It uses no ODE solver, chooses no cosmological initial state, and cannot show
that an orbit crosses either clock boundary.

It hash-pins the existing background export (which supplies \(M\) and the
three exported \(\phi_*\) values) and the two-clock domain audit (which
supplies the closed-FRW convention and the labels \(y=2,3\)).  The constructed
points are algebraic representatives, not initial data.

With lapse \(N=1\),

\[
\dot Q=-\frac{e^{-3Q/2}P}{3\pi^2},\quad
\dot\phi=\frac{e^{-3Q/2}p}{2\pi^2},\quad
\dot p=-2\pi^2e^{3Q/2}V'(\phi),
\]

\[
\dot P=-\frac{e^{-3Q/2}P^2}{4\pi^2}
+\frac{3e^{-3Q/2}p^2}{8\pi^2}
+3\pi^2e^{Q/2}-3\pi^2e^{3Q/2}V(\phi).
\]

For \(y=e^QV\), the exact local derivative is

\[
\dot y=\frac{e^{-Q/2}}{6\pi^2}\left[-2PV+3pV'\right].
\]

On \(C=0=P\),

\[
p^2=8\pi^4e^{2Q}(3-y).
\]

For each already exported \(\phi_*\), the ledger derives—not selects—the
representatives \(Q=\log[y/V(\phi_*)]\), \(P=0\).  At \(y=2\), both allowed
\(p\) signs are retained and \(\dot y\ne0\), since \(V'(\phi_*)\ne0\).  At
\(y=3\), \(p=0\) and \(\dot y=0\) at first order.  The latter is a tangent
instant, not a claim about later behavior.

The runner symbolically checks the displayed equations, the constraint family,
and \(dC/dt=\{C,C\}=0\).  It then evaluates high-precision algebraic
constraint, reconstruction, branch-parity, transversality, and tangency
controls for the three pinned \(\phi_*\) rows.  It makes zero ODE calls.

All trajectory initial-condition selection, integration, crossing evidence,
complete observables, quantum clocks, BO/decoherence, likelihood, physics,
and TOE fields remain null.  No result is included in this draft; after a
clean commit it may only be run through:

```text
./ice run homogeneous_closed_frw_starobinsky_time_symmetric_clock_boundary_local_ledger
```
