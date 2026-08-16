# Phase 16 — BGG single-source calculation notes

This file preserves the useful source information from the abandoned Phase 16A contract/packet. It is
not a preregistration, decision table, or execution gate. The calculation may confirm or reject the
candidate directly.

## Primary source

Pierre Binétruy, Gilles Girardi, and Richard Grimm, “Supergravity couplings: a geometric formulation,”
[`hep-th/0005225v1`](https://arxiv.org/abs/hep-th/0005225v1).

- official e-print archive: 169,016 bytes,
  SHA-256 `9752bda85371cdb572f82a0d6d22c2e6447048620400e61e7c7ba7e7afffdcbc`
- decompressed tar: 624,640 bytes,
  SHA-256 `68a0ec23f7fe138e299a72b8a3f392cad977075e564f6bfdd5d47fe1366f9823`
- `PRmain.tex`: SHA-256 `3b776927675eafa3fb7ee5932d202b18cb0f77eb896281b7f2f910a6bce30d33`
- `AppendixA.tex`: SHA-256 `178da9280eda9aa356e84c7ec0df490186f60775c696db374963cca378cd9667`
- `Section3.tex`: SHA-256 `7bbd20f7a3a00e40a29b17f64f451bf329596db575eee0bb455bf23db937b037`
- `Section4.tex`: SHA-256 `b0e03e31bf3e925936362a3691a23aa93f752372e08d27c518403ec97c6657aa`

Relevant source anchors:

- Appendix A `Formdef`, `Leib`, `A.1`, `A.2`: exterior-form order and mostly-plus metric.
- Section 3 `spincom`: (T^A=dE^A+E^B\phi_B{}^A) and
  (R_B{}^A=d\phi_B{}^A+\phi_B{}^C\phi_C{}^A).
- Section 3 `GRA.240`–`GRA.242`: kinetic, Yang–Mills, and superpotential actions are additive.
- Section 4 `CPN.13`: torsion equation used to solve the bosonic spin connection.
- Section 4 `CPN.26`: the decisive scalar contraction
  \(\mathcal R=e_a{}^n e_b{}^m(R_{nm})^{ab}\). The printed Lorentz order is `ab`.
- Section 4 `CPN.59`, `CPN.130`: auxiliary-uneliminated matter and supergravity-plus-matter actions.
- Section 4 `CPN.74`–`CPN.100`: component local-SUSY transformations.
- Section 4 `CPN.133`–`CPN.143`: the separately additive superpotential sector.

## Model specialization

- one neutral flat chiral coordinate, (K=A\bar A), (g_{A\bar A}=1), zero Kähler curvature;
- no vector multiplets or gauging;
- (W\equiv0), so the additive superpotential sector vanishes without auxiliary equations of motion;
- retain (M,\bar M,b_a,F,\bar F) while checking source coverage;
- physical bridge (S_{\rm phys}=M_P^2S_{\rm BGG}) and
  \(\Phi=M_PA=(T+iY)/\sqrt2\);
- first geometry check:
  \(ds^2=-N(t)^2dt^2+a(t)^2\delta_{ij}dx^idx^j\), with (N,a,M_P,V_0>0);
- scale coordinate (X=\sqrt6M_P\ln a\).

Do not combine a BGG action coefficient with Hohl transformations or Kallosh curvature conventions.

## Direct calculation

1. Solve the bosonic connection from `CPN.13` and Lorentz antisymmetry.
2. Build the curvature two-form in the source order and contract it exactly as `CPN.26`; do not insert a
   preselected multiple of the FLRW curvature expression.
3. Reduce the same-source `CPN.130` + `CPN.59` action at arbitrary lapse, remove the single temporal
   second-derivative boundary term, and compute the (X,T,Y) velocity Hessian and Hamiltonian.
4. Cross-check the curvature/Hessian independently in Cadabra and SymPy or FLINT.
5. Only if the same source gives the needed action and component transformations, calculate homogeneous
   Bianchi-I SUSY tangency. A missing formula or nonzero discarded-mode residual is itself the result.

No target verdict, first-run ceremony, mutant census, or classification schema is required.

## Printed-source caveats

- `CPN.15` contains a repeated upper tangent index. Use `CPN.13` as the connection parent; treat
  `CPN.15` only as a source-local cross-check after index lowering.
- `CPN.99` has a conjugate chiralino free-index/species glyph mismatch. Do not use it silently in a
  tangency calculation; resolve it explicitly from the unbarred formula and conjugation if needed.
- `CPN.132` prints `sigma_m` in a conjugate derivative where the derivative index and conjugation suggest
  `sigma_n`; check this before using the fermionic formula.
- `CPN.129` prints `-mathcal R/4` with a hermitian-conjugate instruction, while `CPN.130` is the combined
  `-mathcal R/2` action. Do not apply the hermitian pair twice.
- The full action recap near Section 4 lines 1741–1858 is unlabeled in the TeX source; cite the line span,
  not a fabricated label.
