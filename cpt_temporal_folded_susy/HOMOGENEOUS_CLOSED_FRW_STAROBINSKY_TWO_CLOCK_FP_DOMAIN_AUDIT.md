# Homogeneous closed-FRW Starobinsky two-clock FP-domain audit — draft

Status: unnumbered bounded exact runner draft. It has not been run, produces no
committed result in this change, and does not authorize a successor calculation.

## Pinned inputs and scope

The draft hash-pins these existing artifacts before any calculation:

- `CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_AUDIT_RESULT.json` — SHA-256
  `5d56bd94020ddebfda609ca8da3956cc75be5c74ad9b06cdb9ea3464ee616441`.
  It fixes the homogeneous closed-FRW convention
  \(Q=2\log a\), \(P=a p_a/2\), and the massless raw constraint.
- `CLOSED_STAROBINSKY_BACKGROUND_EXPORT_AUDIT_RESULT.json` — SHA-256
  `af6334f0c8a3f745ecfedd37280a8cae457f2ec7adfb5effb3b33f29dbc193e1`.
  It fixes the declared Starobinsky potential convention only. It contains no
  closed-FRW \(Q,P,p\) trajectory.

The source context is Halliwell--Hawking (closed-universe context), Starobinsky
(potential context), and Kallosh--Linde (improved-Cecotti realization), recorded
in the companion input. None is used as a result about a complete observable,
quantum clock, BO/decoherence, or likelihood.

## Fixed classical calculation

With \(\{Q,P\}=\{\phi,p\}=1\), the proposed exact calculation fixes

\[
C_V=-\frac{e^{-3Q/2}P^2}{6\pi^2}
+\frac{e^{-3Q/2}p^2}{4\pi^2}
-6\pi^2e^{Q/2}+2\pi^2e^{3Q/2}V(\phi),
\]

where

\[
V(\phi)=\frac{3M^2}{4}\left(1-e^{-\sqrt{2/3}\phi}\right)^2.
\]

The three clock/control factors to be derived by the runner are

\[
\{\phi,C_V\}=\frac{e^{-3Q/2}p}{2\pi^2},\qquad
\{Q,C_V\}=-\frac{e^{-3Q/2}P}{3\pi^2},\qquad
\{P,C_V\}=-\partial_QC_V.
\]

Thus \(Q\) is an explicit failure-control coordinate on the time-symmetric
slice \(P=0\); it is not asserted to be a global clock.

## Time-symmetric domain classification

Set \(y=e^Q V(\phi)\). On \(C_V=0=P\), direct elimination gives

\[
p^2=8\pi^4e^{2Q}(3-y).
\]

Consequently, real \(p\) requires \(y\le3\), and the scalar-clock FP zero
\(p=0\) is precisely its boundary \(y=3\).

The independent direct and constraint-eliminated derivations of the
trace-momentum-clock factor agree:

\[
\{P,C_V\}\big|_{C_V=P=0}=6\pi^2e^{Q/2}(2-y).
\]

Therefore its FP-zero locus is \(y=2\), which is inside the real-\(p\) domain.
This is deliberately checked twice in the runner. An earlier informal value
\(3/2\) is not retained: it does not follow from the displayed constraint.
For the independent elimination the runner uses the full scalar kinetic term
\(A=e^{-3Q/2}p^2/(4\pi^2)\), not one third of it, and verifies
\((3/2)A+3\pi^2e^{Q/2}-3\pi^2e^{3Q/2}V=6\pi^2e^{Q/2}(2-y)\).

For \(x=e^{-\sqrt{2/3}\phi}\),

\[
V'=\frac32M^2\sqrt{\frac23}x(1-x),\qquad
\dot p=-2\pi^2e^{3Q/2}V'.
\]

For \(M>0\), \(V\ge0\); \(V'\) has the sign of \(\phi\), so \(\dot p\)
has the opposite sign. These are local homogeneous equations, not an integrated
trajectory.

## Fail-closed boundary

The draft leaves null: which locus an actual solution crosses; complete
relational observables; clock-change maps and physical inner products; quantum
clocks; BO/decoherence; SVT/ADM/HDA; BFV anomaly freedom; CLASS/Cobaya inputs;
and likelihood or physical claims. The pinned background export cannot resolve
the trajectory-crossing null because it has no \(Q,P,p\) data.

No command has been run for this draft.

## Runner outcome protocol

The runner separates executable exact checks from analytic theorem/scope guards
(real-square domain and Starobinsky sign reasoning). It pins each upstream raw
SHA-256, run status, verdict, and payload-without-self hash. A passing exact
ledger selects the stated `KEEP` verdict; any failed executable check selects
the input's `KILL` verdict. The emitted result is designed to carry a canonical
payload-without-self hash, while the concise stdout summary separately prints
the SHA-256 of the serialized outer result. Neither hash is produced by this
unexecuted draft.
