# Source inventory

> This is a human-readable memory and index of sources already represented in [`graph.json`](../graph.json). It is **not** a preregistration, research contract, systematic literature review, completeness claim, endorsement, or KG ratification.

## How source edges are used

- `evidence → DERIVED_FROM → source` means the calculation was built from that source. Phase 16 uses this stronger provenance relation for BGG.
- `claim or concept → CITES → source` means the source frames the standard algebra, a comparison, or an interpretive boundary. It does not mean the paper performed the repository's exact finite calculation.
- No source edge by itself changes claim state; the attached evidence and `HAS_EVIDENCE.polarity` do that.

## Inventory

| Source ID and locator | Role in the graph | Boundary of that role |
| --- | --- | --- |
| `source:bgg-hep-th-0005225v1` — P. Binétruy, G. Girardi, R. Grimm, [*Supergravity couplings: a geometric formulation*](https://arxiv.org/abs/hep-th/0005225v1), `hep-th/0005225v1` | Primary single-source component-supergravity parent for all three Phase 16 evidence groups | Supports the source transcription and derived scoped checks; it does not itself assert this repository's truncation verdict or temporal-fold programme |
| `source:hls-1975` — R. Haag, J. T. Łopuszański, M. Sohnius, [*All Possible Generators of Supersymmetries of the S-Matrix*](https://doi.org/10.1016/0550-3213(75)90279-5) | Primary baseline for standard super-Poincaré algebra and translation closure; cited by the support-local and reflection-composed-charge claims | Not a calculation of sharp time-half projectors, folded sheets, or a temporal seam |
| `source:belyaev-van-nieuwenhuizen-2008` — D. V. Belyaev, P. van Nieuwenhuizen, [*Rigid supersymmetry with boundaries*](https://arxiv.org/abs/0801.2377) | Positive control for a timelike boundary with spacelike normal | Not authority for a temporal seam |
| `source:di-pietro-klinghoffer-shamir-2015` — L. Di Pietro, N. Klinghoffer, I. Shamir, [*On Supersymmetry, Boundary Actions and Brane Charges*](https://arxiv.org/abs/1502.05976) | Spatial-boundary subalgebra source and reality warning | Not a temporal-seam construction |
| `source:skenderis-townsend-2006` — K. Skenderis, P. K. Townsend, [*Pseudo-Supersymmetry and the Domain-Wall/Cosmology Correspondence*](https://arxiv.org/abs/hep-th/0610253) | Warning that wall-to-cosmology continuation changes the real/SUSY structure | Does not supply the proposed doubled temporal interface |
| `source:boyle-finn-turok-2018` — L. Boyle, K. Finn, N. Turok, [*CPT-Symmetric Universe*](https://arxiv.org/abs/1803.08928) | Primary example of horizontally CPT-related cosmological histories; cited from `concept:cpt-pin-sewing` | Does not identify CPT as a particle supercharge and is not the evidence edge for the narrower physical-time-reversal claim |
| `source:witten-2015` — E. Witten, [*Fermion Path Integrals And Topological Phases*](https://arxiv.org/abs/1508.04715) | Technical source for fermionic reflection structures | Does not construct this repository's doubled projector/action pair |
| `source:freed-hopkins-2016` — D. Freed, M. Hopkins, [*Reflection positivity and invertible topological phases*](https://arxiv.org/abs/1604.06527) | Technical source for Pin/reflection lifts and cocycle requirements | Makes those requirements visible; it does not close the open Pin lift here |
| `source:hlr-2016` — F. Haehl, R. Loganayagam, M. Rangamani, [*Schwinger–Keldysh formalism I*](https://arxiv.org/abs/1610.01940) | Primary source for topological SK BRST structure | SK BRST is not thereby positive-energy particle supersymmetry |
| `source:geracie-et-al-2017` — M. Geracie et al., [*Schwinger–Keldysh superspace in quantum mechanics*](https://arxiv.org/abs/1712.04459) | Concrete SK superspace/quartet realization | Does not complete the repository's contour Hilbert space or ghost metric |
| `source:wess-zumino-1974` — J. Wess, B. Zumino, [*A Lagrangian Model Invariant Under Supergauge Transformations*](https://doi.org/10.1016/0370-2693(74)90578-4) | Four-dimensional supersymmetric boson/fermion model used as the equal-mass free baseline | Does not supply the repository's temporal-seam theorem or a doubled Pin construction |
| `source:collins-initial-propagators-2013` — H. Collins, [*Initial state propagators*](https://arxiv.org/abs/1309.2656), `arXiv:1309.2656` | Baseline for encoding Gaussian initial data as propagator corrections with unchanged bulk frequencies | The exact Phase 18 state-versus-retarded-pole matrix proof remains local repository evidence |
| `source:collins-holman-2005` — H. Collins, R. Holman, [*Renormalization of initial conditions and the trans-Planckian problem of inflation*](https://arxiv.org/abs/hep-th/0501158), `hep-th/0501158` | Distinguishes standard bulk renormalization from divergences localized on an initial surface | Does not make the sharp infinite-energy scalar seam UV admissible |
| `source:hung-smolkin-sorkin-2013` — L.-Y. Hung, M. Smolkin, E. Sorkin, [*(Non) supersymmetric quantum quenches*](https://arxiv.org/abs/1307.0376), `arXiv:1307.0376` | Interacting proof of principle for late nonthermal SUSY breaking after a quench | The model is 2+1-dimensional large-`N`/Hartree–Fock, not a 3+1-dimensional Wess–Zumino vacuum-pole calculation |
| `source:girardello-grisaru-1982` — L. Girardello, M. T. Grisaru, [*Soft breaking of supersymmetry*](https://doi.org/10.1016/0550-3213(82)90512-0) | Classification baseline for soft versus hard SUSY-breaking operators | Does not derive a temporal-seam spurion or its magnitude |
| `source:boyle-turok-2021` — L. Boyle, N. Turok, [*Two-sheeted universe, analyticity and the arrow of time*](https://arxiv.org/abs/2109.06204), `arXiv:2109.06204` | Motivation for one analytic spacetime with two sheets exchanged by an isometry; cited from `concept:cpt-pin-sewing` | Neither proves a SUSY seam nor supplies the Phase 18 free-spectrum theorem |

Every source above has `state: PRIMARY` in the local graph. That is a source classification, not a claim that the sixteen-item inventory exhausts the literature.

## Claim-family coverage

| Claim family | Graph sources | Coverage type |
| --- | --- | --- |
| Phase 16 bosonic parent, strict tangency, rolling clock | BGG `hep-th/0005225v1` | Three `DERIVED_FROM` edges from evidence |
| Standard local SUSY and reflection-composed charge | Haag–Łopuszański–Sohnius | Two `CITES` edges establishing the standard closure baseline |
| Ordinary real temporal seam | Belyaev–van Nieuwenhuizen; Di Pietro–Klinghoffer–Shamir; Skenderis–Townsend | Three `CITES` edges: spatial positive controls and continuation/reality warnings |
| Doubled-real projector witness | Witten; Freed–Hopkins | Two `CITES` edges for reflection and Pin structure requirements |
| Physical time reversal is not the tested supercharge | No `CITES` edge from the claim | Local anti-complex-linearity and grading check within the literal-time-line scope |
| CPT/Pin sewing as a distinct structure | Boyle–Finn–Turok | One `CITES` edge from `concept:cpt-pin-sewing`, not from the physical-time-reversal claim |
| SK BRST is not particle SUSY | Haehl–Loganayagam–Rangamani; Geracie et al. | Two `CITES` edges for cohomological SK structure |
| Fundamental doubled exchange, one-way closure, basis nonselection | No `CITES` edge | Local finite calculations only; no physical realization is attributed to literature |
| Free equal-mass model and initial-state-versus-pole distinction | Wess–Zumino; Collins (2013) | Two `CITES` edges from Phase 18 concepts; neither is a `DERIVED_FROM` receipt for the local theorem |
| Sharp-seam UV admissibility | Collins–Holman | One `CITES` edge from the contradicted Phase 18 claim; initial-surface renormalization does not rescue its divergent state preparation |
| Persistent SUSY-breaking carrier and soft terms | Hung–Smolkin–Sorkin; Girardello–Grisaru | Two `CITES` edges from the persistent-carrier concept: an interacting quench proof of principle and an operator-classification baseline, not a seam-generated mass prediction |
| Analytic two-sheet motivation | Boyle–Turok (2021) | One additional `CITES` edge from `concept:cpt-pin-sewing`; motivation only, not evidence for a SUSY seam |

Phase 15R is intentionally represented as a historical **result pointer**, not a duplicated source
ledger. Its Hohl v1/Kallosh v3 hashes, locators, conventions, and role restrictions remain authoritative
in [`PHASE15R_SOURCE_CONVENTION_PACKET.json`](../../../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json).
The local graph therefore does not imply source completeness for Phase 15R; it preserves only the two
scoped target states needed to understand why Phase 16 tested BGG.

## Source pinning

BGG is the only source in the graph with a pinned archive version, local content hashes, and equation anchors. The pinned record is:

- Version: `hep-th/0005225v1`
- e-print gzip SHA-256: `9752bda85371cdb572f82a0d6d22c2e6447048620400e61e7c7ba7e7afffdcbc`
- `PRmain.tex`: `3b776927675eafa3fb7ee5932d202b18cb0f77eb896281b7f2f910a6bce30d33`
- `AppendixA.tex`: `178da9280eda9aa356e84c7ec0df490186f60775c696db374963cca378cd9667`
- `Section3.tex`: `7bbd20f7a3a00e40a29b17f64f451bf329596db575eee0bb455bf23db937b037`
- `Section4.tex`: `b0e03e31bf3e925936362a3691a23aa93f752372e08d27c518403ec97c6657aa`
- Anchors: `Formdef`, `Leib`, `A.1`, `A.2`, `spincom`, `GRA.240–GRA.242`, `CPN.13`, `CPN.26`, `CPN.40`, `CPN.59`, `CPN.74–CPN.100`, `CPN.130`, `CPN.133–CPN.143`

The other fifteen graph sources have stable DOI/arXiv locators but no stored local content hash or equation-level anchor. Consequently, the Phase 17 and Phase 18 literature links document framing and scope, while the exact matrix results remain repository evidence. See [`PHASE16_BGG_SOURCE_NOTES.md`](../../../cpt_temporal_folded_susy/PHASE16_BGG_SOURCE_NOTES.md) for the detailed BGG source ledger.

## Uncovered construction needs

The current source inventory does not provide a source-defined physical realization of the surviving doubled route. In particular, no graph source closes all of the following in one construction:

- a Pin/Clifford lift with square, cocycle, and Majorana bilinear;
- a real doubled Lorentzian bulk-plus-interface action;
- a variational and self-adjoint gluing domain;
- a conserved complex-linear fermionic charge with positive physical adjoint;
- charge/projector compatibility;
- a basis-invariant physical sheet anchor;
- full reality, positivity, and junction data.

Phase 18 adds four further uncovered calculations:

- interacting late-time boson and fermion Wigner self-energies after an admissible seam state;
- a finite-energy persistent `F`/`D` order parameter, memory sector, or vacuum-selection mechanism;
- FRW evolution including interactions, thermalization, and backreaction;
- regulator-independent Higgs power sensitivity in the completed interacting doubled parent.

These are represented as open-problem nodes, not hidden assumptions or implied literature results.
