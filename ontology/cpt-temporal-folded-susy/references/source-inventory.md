# Source inventory

> This is a human-readable memory and index of sources already represented in [`graph.json`](../graph.json). It is **not** a preregistration, research contract, systematic literature review, completeness claim, endorsement, or KG ratification.

## How source edges are used

- `evidence → DERIVED_FROM → source` means the calculation was built from that source. Phase 16 uses this stronger provenance relation for BGG; selected Phase 19/20 groups use it for their model, action, or observational-comparison inputs while keeping local algebra and numerics separate.
- `claim, concept, or open problem → CITES → source` means the source frames the standard algebra, a comparison, or an interpretive boundary. It does not mean the paper performed the repository's exact finite calculation.
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
| `source:witten-2015` — E. Witten, [*Fermion Path Integrals And Topological Phases*](https://arxiv.org/abs/1508.04715) | Technical source for fermion Pfaffian lines, spectral-flow, and reflection-anomaly requirements, including the Phase-37 bosonic-versus-fermionic-line boundary | Does not construct this repository's doubled projector/action pair or turn the sampled reduced bosonic half-form into a fermion Pfaffian |
| `source:freed-hopkins-2016` — D. Freed, M. Hopkins, [*Reflection positivity and invertible topological phases*](https://arxiv.org/abs/1604.06527) | Technical source for Pin/reflection lifts, cocycles, and invertible-phase requirements, including the Phase-37 interpretation boundary | Makes those requirements visible; it does not close the open Pin lift, derive a physical fermionic holonomy, or construct a supercharge here |
| `source:hlr-2016` — F. Haehl, R. Loganayagam, M. Rangamani, [*Schwinger–Keldysh formalism I*](https://arxiv.org/abs/1610.01940) | Primary source for topological SK BRST structure | SK BRST is not thereby positive-energy particle supersymmetry |
| `source:geracie-et-al-2017` — M. Geracie et al., [*Schwinger–Keldysh superspace in quantum mechanics*](https://arxiv.org/abs/1712.04459) | Concrete SK superspace/quartet realization | Does not complete the repository's contour Hilbert space or ghost metric |
| `source:wess-zumino-1974` — J. Wess, B. Zumino, [*A Lagrangian Model Invariant Under Supergauge Transformations*](https://doi.org/10.1016/0370-2693(74)90578-4) | Four-dimensional supersymmetric boson/fermion model used as the equal-mass free baseline | Does not supply the repository's temporal-seam theorem or a doubled Pin construction |
| `source:collins-initial-propagators-2013` — H. Collins, [*Initial state propagators*](https://arxiv.org/abs/1309.2656), `arXiv:1309.2656` | Baseline for encoding Gaussian initial data as propagator corrections with unchanged bulk frequencies | The exact Phase 18 state-versus-retarded-pole matrix proof remains local repository evidence |
| `source:collins-holman-2005` — H. Collins, R. Holman, [*Renormalization of initial conditions and the trans-Planckian problem of inflation*](https://arxiv.org/abs/hep-th/0501158), `hep-th/0501158` | Distinguishes standard bulk renormalization from divergences localized on an initial surface | Does not make the sharp infinite-energy scalar seam UV admissible |
| `source:hung-smolkin-sorkin-2013` — L.-Y. Hung, M. Smolkin, E. Sorkin, [*(Non) supersymmetric quantum quenches*](https://arxiv.org/abs/1307.0376), `arXiv:1307.0376` | Interacting proof of principle for late nonthermal SUSY breaking after a quench | The model is 2+1-dimensional large-`N`/Hartree–Fock, not a 3+1-dimensional Wess–Zumino vacuum-pole calculation |
| `source:girardello-grisaru-1982` — L. Girardello, M. T. Grisaru, [*Soft breaking of supersymmetry*](https://doi.org/10.1016/0550-3213(82)90512-0) | Classification baseline for soft versus hard SUSY-breaking operators | Does not derive a temporal-seam spurion or its magnitude |
| `source:boyle-turok-2021` — L. Boyle, N. Turok, [*Two-sheeted universe, analyticity and the arrow of time*](https://arxiv.org/abs/2109.06204), `arXiv:2109.06204` | Motivation for one analytic spacetime with two sheets exchanged by an isometry; cited from `concept:cpt-pin-sewing` | Neither proves a SUSY seam nor supplies the Phase 18 free-spectrum theorem |
| `source:kallosh-linde-2010` — R. Kallosh, A. Linde, [*New models of chaotic inflation in supergravity*](https://arxiv.org/abs/1008.3375v2), `arXiv:1008.3375v2` | Primary source for the Phase 19 shift-symmetric stabilizer construction; `DERIVED_FROM` the exact shift evidence | Does not select the closed-bounce initial amplitude or supply the repository's numerical shooting result |
| `source:kallosh-linde-2013` — R. Kallosh, A. Linde, [*Superconformal generalizations of the Starobinsky model*](https://arxiv.org/abs/1306.3214v2), `arXiv:1306.3214v2` | Primary source for improved Cecotti stabilization; `DERIVED_FROM` the exact no-scale evidence | The sharp local Hessian threshold is a repository derivation; the paper does not construct this closed bounce or a CPT/Pin state |
| `source:bicep-keck-2021` — BICEP/Keck Collaboration, [*Improved Constraints on Primordial Gravitational Waves using Planck, WMAP, and BICEP/Keck Observations through the 2018 Observing Season*](https://arxiv.org/abs/2110.00483), `arXiv:2110.00483` | Supplies the published \(r_{0.05}<0.036\) comparison used by the Phase 19 slow-roll evidence | Does not calculate either local SUGRA trajectory or the bounce |
| `source:balkenhol-et-al-2026` — L. Balkenhol et al., [*Inflation at the End of 2025: Constraints on \(r\) and \(n_s\) Using the Latest CMB and BAO Data*](https://arxiv.org/abs/2512.10613v2), `arXiv:2512.10613v2` | Supplies the updated \(r<0.034\) comparison and dataset-dependent scalar-tilt context | Does not calculate the bounce; its likelihood results cannot be replaced by the repository's first-order potential formulas |
| `source:hartle-hawking-1983` — J. B. Hartle, S. W. Hawking, [*Wave Function of the Universe*](https://doi.org/10.1103/PhysRevD.28.2960), Phys. Rev. D 28, 2960 (1983) | Primary no-boundary and Euclidean de Sitter-action baseline; `DERIVED_FROM` the leading Phase 20 WDW-envelope group | Does not supply an exact Starobinsky scalar-gravity saddle or any two-sheet probability rule |
| `source:hartle-hawking-hertog-2008` — J. B. Hartle, S. W. Hawking, T. Hertog, [*The No-Boundary Measure of the Universe*](https://arxiv.org/abs/0711.4630), `arXiv:0711.4630v4` | Frames semiclassical history weighting and the generally complex no-boundary saddle | Does not derive the repository's conditional independent-pair joint probability or evaluate this Cecotti branch |
| `source:halliwell-2009` — J. J. Halliwell, [*Probabilities in Quantum Cosmological Models: A Decoherent Histories Analysis Using a Complex Potential*](https://arxiv.org/abs/0909.2597), `arXiv:0909.2597` | Frames WDW currents, coarse histories, and approximate decoherence used to bound the coherent-interference interpretation | Does not choose the sheet inner product or compute the Phase 20 coherent phase |
| `source:cheng-death-moniz-1994` — A. D. Y. Cheng, P. D. D'Eath, P. R. L. V. Moniz, [*Quantization of a Locally Supersymmetric Friedmann Model with Supermatter*](https://arxiv.org/abs/gr-qc/9406048), `arXiv:gr-qc/9406048v2` | Primary example showing local-SUSY minisuperspace constraints as coupled first-order PDEs dependent on Kähler geometry | Does not solve those constraints for the Cecotti model or select \(\varphi=5.44\) |
| `source:desi-dr2-2025` — DESI Collaboration, [*DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints*](https://arxiv.org/abs/2503.14738), `arXiv:2503.14738` | Observational context for why the conditional curvature conversion is not treated as a detection | Does not supply the branch, reheating history, or a temporal-seam curvature prediction |
| `source:barvinsky-kamenshchik-mishakov-1996` — A. O. Barvinsky, A. Yu. Kamenshchik, I. V. Mishakov, [*Quantum origin of the early inflationary Universe*](https://arxiv.org/abs/gr-qc/9612004), `arXiv:gr-qc/9612004` | One-loop sharp-peak proof of principle cited by the open determinant problem | The model has large nonminimal coupling and is not the two-sheet Cecotti boson–fermion–gravitino determinant |
| `source:kubo-1962` — R. Kubo, [*Generalized Cumulant Expansion Method*](https://doi.org/10.1143/JPSJ.17.1100), JPSJ 17 (1962) 1100–1120 | Linked-cluster/cumulant reference for the distinction between \(R-1\) and \(\log R\) | Does not define a WDW probability or the Phase 21 flux-sector measure |
| `source:osterwalder-schrader-1975` — K. Osterwalder, R. Schrader, [*Axioms for Euclidean Green's Functions II*](https://doi.org/10.1007/BF01608978), CMP 42 (1975) 281–305 | Reflection-positivity boundary for interpreting a Euclidean determinant | Phase 21 verifies only a finite positive Gaussian and does not construct the full OS field theory |
| `source:hawking-1977-zeta` — S. W. Hawking, [*Zeta Function Regularization of Path Integrals in Curved Spacetime*](https://doi.org/10.1007/BF01626516), CMP 55 (1977) 133–148 | Functional-determinant regularization baseline | A finite determinant or finite part is not automatically a countably additive universe probability |
| `source:hartle-marolf-1997` — J. B. Hartle, D. Marolf, [*Comparing Formulations of Generalized Quantum Mechanics for Reparametrization-Invariant Systems*](https://doi.org/10.1103/PhysRevD.56.6247), `arXiv:gr-qc/9703021v1` | Frames induced products and alternative probability formulations for Phase 21 and the Phase 23 current/product distinction | Does not choose the flux prior, sheet kernel, compact bridge, or physical state |
| `source:marolf-1995` — D. Marolf, [*Refined Algebraic Quantization: Systems with a single constraint*](https://arxiv.org/abs/gr-qc/9508015), `arXiv:gr-qc/9508015v3` | Primary refined-algebraic-quantization and group-averaging framing for the Phase 23 distributional single-constraint rigging map | Does not derive the repository's concrete lapse regulators, compact bridge \(B_L\), positive-frequency choice, or cosmological density |
| `source:bousso-polchinski-2000` — R. Bousso, J. Polchinski, [*Quantization of Four-form Fluxes and Dynamical Neutralization of the Cosmological Constant*](https://doi.org/10.1088/1126-6708/2000/06/006), `arXiv:hep-th/0004134v3` | Compact flux and charged-membrane framework cited by the kernel open problem | Does not derive the Phase 21 Gaussian kernel or a WDW probability distribution |
| `source:bandos-et-al-2018` — I. Bandos et al., [*Three-forms, dualities and membranes in four-dimensional supergravity*](https://doi.org/10.1007/JHEP07(2018)028), `arXiv:1803.01405v2` | Compact three-form SUGRA, charged membranes, and an F-type auxiliary/flux route cited by the next gate | Without a membrane the integration constants are locally fixed on a source-free EFT region, but this is not a theorem forbidding a global path integral from summing sectors; the paper does not derive the seam, a D-type vector/gauging sector, or the sector weights |
| `source:ojima-1981` — I. Ojima, [*Gauge Fields at Finite Temperatures—Thermo Field Dynamics and the KMS Condition and Their Extension to Gauge Theories*](https://doi.org/10.1016/0003-4916(81)90058-0), Ann. Phys. 137 (1981) 1–32 | Primary thermofield/KMS framing for the finite doubled purification | Does not identify the two factors with literal universes or supply a local-SUGRA seam state |
| `source:israel-1976` — W. Israel, [*Thermo-field Dynamics of Black Holes*](https://doi.org/10.1016/0375-9601(76)90178-X), Phys. Lett. A 57 (1976) 107–110 | Primary doubled-purification example | Does not derive the Phase 22 graded phase, Pin lift, or cosmological state |
| `source:buchholz-ojima-1997` — D. Buchholz, I. Ojima, [*Spontaneous Collapse of Supersymmetry*](https://arxiv.org/abs/hep-th/9701005), `arXiv:hep-th/9701005v3` | Thermal-SUSY obstruction used to separate Gibbs covariance from an unbroken vacuum claim | Does not invalidate the exact finite matrix algebra or construct the requested seam state |
| `source:halliwell-1988` — J. J. Halliwell, [*Derivation of the Wheeler–DeWitt equation from a path integral for minisuperspace models*](https://doi.org/10.1103/PhysRevD.38.2468), Phys. Rev. D 38 (1988) 2468 | `CITES`-only Wheeler–DeWitt derivation and lapse-measure/operator-ordering boundary for the connected minisuperspace calculations | Does not establish generic boundary conditions or derive the frozen saddle, principal Hessian, zero-lapse asymptotics, or BFV kernel |
| `source:henneaux-teitelboim-vergara-1992` — M. Henneaux, C. Teitelboim, J. D. Vergara, [*Gauge invariance for generally covariant systems*](https://doi.org/10.1016/0550-3213(92)90166-9), Nucl. Phys. B 387 (1992) 391–418 | `CITES`-only canonical-gauge reference for transversality, gauge-related endpoint states, finite endpoint transformations, and improved boundary actions | Supplies the general endpoint framework, not this model's fixed-\(\Phi_*\) relational action. It does not prove a global trace gauge, choose normalized quantum endpoint states, or supply the replacement ghost/BFV measure |
| `source:marolf-1996-minisuperspace-path-integrals` — D. Marolf, [*Path integrals and instantons in quantum gravity: Minisuperspace models*](https://doi.org/10.1103/PhysRevD.53.6979), Phys. Rev. D 53 (1996) 6979–6990 | `CITES`-only full-real-lapse and gauge-fixed minisuperspace path-integral reference for the trace-gauge and distributional \(\delta(C)\) physical-inner-product boundary | Its model-specific modulus coordinate gauge is not a general signed-versus-absolute determinant theorem for this momentum gauge. It does not derive the repository's local action ledger, replacement source, or a full-real-lapse kernel here; on continuous zero spectrum the target is not described as an ordinary idempotent kinematical projector |
| `source:barvinsky-nesterov-2005` — A. O. Barvinsky, D. V. Nesterov, [*Quantum effective action in spacetimes with branes and boundaries*](https://arxiv.org/abs/hep-th/0512291), `arXiv:hep-th/0512291` | `CITES`-only framing for the relation between boundary response kernels and bulk operators | Does not supply the Phase 24 response matrix, prove a positive seam state, or perform its constraint-preserving endpoint variation |
| `source:gibbons-hawking-perry-1978` — G. W. Gibbons, S. W. Hawking, M. J. Perry, [*Path integrals and the indefiniteness of the gravitational action*](https://doi.org/10.1016/0550-3213(78)90161-X), Nucl. Phys. B 138 (1978) 141 | `CITES`-only contour warning for the indefinite gravitational action | Does not choose the Phase 24 thimble, orient the Phase-33 fold determinant line, compute an intersection number, or identify the bulk fluctuation spectrum |
| `source:donnelly-freidel-2016` — W. Donnelly, L. Freidel, [*Local subsystems in gauge theory and gravity*](https://arxiv.org/abs/1601.04744), `arXiv:1601.04744` | `CITES`-only factorization caveat for interpreting two gravitational boundaries as subsystems | Does not establish a two-universe Hilbert-space factorization, Choi state, physical measure, or trace-class density for Phase 24 |
| `source:bombelli-et-al-1986` — L. Bombelli, R. K. Koul, J. Lee, R. D. Sorkin, [*Quantum source of entropy for black holes*](https://doi.org/10.1103/PhysRevD.34.373), Phys. Rev. D 34 (1986) 373 | `CITES`-only pure-Gaussian Schmidt-entropy control for the conditional two-mode algebra | Does not turn the fixed-scale flat-measure diagnostic into gravitational seam entropy |
| `source:halliwell-louko-1989` — J. J. Halliwell, J. Louko, [*Steepest-descent contours in the path-integral approach to quantum cosmology. I. The de Sitter minisuperspace model*](https://doi.org/10.1103/PhysRevD.39.2206), Phys. Rev. D 39 (1989) 2206 | `CITES`-only motivation for the missing steepest-descent contour and intersection gate | Treats a de Sitter minisuperspace model and does not determine whether the Phase 24 Starobinsky interval contributes |
| `source:feldbrugge-lehners-turok-2017` — J. Feldbrugge, J.-L. Lehners, N. Turok, [*Lorentzian Quantum Cosmology*](https://arxiv.org/abs/1703.02076), `arXiv:1703.02076v2` | `CITES`-only Picard–Lefschetz lapse-cycle and dual-intersection framing | Does not determine the Phase 25–28 Starobinsky saddle census, endpoints, original contour, or coefficient |
| `source:witten-2010-picard-lefschetz` — E. Witten, [*Analytic Continuation Of Chern–Simons Theory*](https://arxiv.org/abs/1001.2933), `arXiv:1001.2933v4` | `CITES`-only relative-cycle and Morse/Picard–Lefschetz framework, including the distinction between Phase-37 root transport and the missing global original cycle | Does not select the repository's Airy contour/Stokes multiplier, orient the full determinant line, compute its global gravitational lapse thimble, or construct a physical WDW state |
| `source:chakrabarti-shafikov-2017-boundary-values` — D. Chakrabarti, R. Shafikov, [*Distributional boundary values of holomorphic functions on product domains*](https://arxiv.org/abs/1505.01230), `arXiv:1505.01230` | `CITES`-only polynomial-growth distributional-boundary and continuous canonical-extension framework predeclared for the Gate-1 scalar zero-lapse control | The invalid runner stopped before its theorem guards; this source neither repairs the harness nor proves that the repository amplitude satisfies every needed topology hypothesis |
| `source:brunetti-fredenhagen-2000-scaling-degree` — R. Brunetti, K. Fredenhagen, [*Microlocal Analysis and Interacting Quantum Field Theories: Renormalization on Physical Backgrounds*](https://arxiv.org/abs/math-ph/9903028), `arXiv:math-ph/9903028` | `CITES`-only scaling-degree-preserving extension theorem predeclared for the one-dimensional lapse contact analysis | Its uniqueness is only among extensions preserving scaling degree below the ambient dimension; the invalid runner produced no boundary distribution or scaling-degree evidence to which the theorem could be applied |
| `source:gutzwiller-1967` — M. C. Gutzwiller, [*Phase-integral approximation in momentum space and the bound states of an atom*](https://doi.org/10.1063/1.1705112), J. Math. Phys. 8 (1967) 1979 | `CITES`-only Jacobi, Van Vleck, and caustic semiclassical framing | Does not derive the repository's fixed-boundary branch, numerical fold, or gauge-reduced endpoint measure |
| `source:hormander-1971-fourier-integral-operators-i` — L. Hörmander, [*Fourier integral operators. I*](https://doi.org/10.1007/BF02392052), Acta Math. 127 (1971) 79–183 | `CITES`-only local microlocal canonical-relation and principal FIO-symbol framing for the V0 endpoint calculation | Does not derive the repository phase or half-density, establish an exact/global unitary operator, choose domains or a physical endpoint measure, or supply BFV data |
| `source:van-vleck-1928-correspondence-principle` — J. H. Van Vleck, [*The Correspondence Principle in the Statistical Interpretation of Quantum Mechanics*](https://doi.org/10.1073/pnas.14.2.178), PNAS 14 (1928) 178–188 | `CITES`-only historical semiclassical determinant-amplitude framing for the V0 endpoint calculation | Is not an exact finite-\(\hbar\) normalization theorem for this nonlinear canonical transform and does not supply its full symbol, ordering or domains |
| `source:chester-friedman-ursell-1957` — C. Chester, B. Friedman, F. Ursell, [*An extension of the method of steepest descents*](https://doi.org/10.1017/S0305004100032655), Proc. Camb. Phil. Soc. 53 (1957) 599 | `CITES`-only Airy uniformization framework, including the Phase-37 local root/half-form versus hard-CFU boundary | Does not supply the repository's branch or endpoint-determinant data, choose the original relative cycle or analytic amplitude, exclude intersample zeros, compute the hard coefficients, prove completeness of the sheets, or turn their fold into a lapse saddle |
| `source:teitelboim-1983` — C. Teitelboim, [*Causality versus Gauge Invariance in Quantum Gravity and Supergravity*](https://doi.org/10.1103/PhysRevLett.50.705), Phys. Rev. Lett. 50 (1983) 705 | `CITES`-only distinction between positive proper-time causal objects and gauge-invariant constraint constructions | Does not define the Phase 27 endpoint prescription, state, or PL coefficient |
| `source:banihashemi-jacobson-2025` — B. Banihashemi, T. Jacobson, [*On the lapse contour in the gravitational path integral*](https://doi.org/10.1103/PhysRevD.111.066014), Phys. Rev. D 111 (2025) 066014 | `CITES`-only contour and local trace-gauge/FP premise for its stated momentum-integration order, including the spatially flat benchmark that motivates the repository's frozen \(V=0\) control | Does not derive the repository's curved closed-FRW relational coordinate or endpoint action, fix the Phase 27–28 BFV endpoint factor, prove global gauge coverage, or determine \(n_\sigma\) |
| `source:batalin-vilkovisky-1981` — I. A. Batalin, G. A. Vilkovisky, [*Gauge Algebra and Quantization*](https://doi.org/10.1016/0370-2693(81)90205-7), Phys. Lett. B 102 (1981) 27 | `CITES`-only BV gauge-algebra completion framework | Phase 28 implements a reduced Hamiltonian BFV control, not the full BV master equation |
| `source:fradkin-vilkovisky-1975` — E. S. Fradkin, G. A. Vilkovisky, [*Quantization of Relativistic Systems with Constraints*](https://doi.org/10.1016/0370-2693(75)90448-7), Phys. Lett. B 55 (1975) 224 | `CITES`-only Hamiltonian constrained-path-integral and gauge-fixing framework | Does not supply the Phase 28 endpoint-completed determinant or physical normalization |
| `source:farakos-et-al-2017` — F. Farakos, S. Lanza, L. Martucci, D. Sorokin, [*Three-forms in Supergravity and Flux Compactifications*](https://arxiv.org/abs/1706.09422), `arXiv:1706.09422v2` | `CITES`-only double-three-form (N=1) SUGRA route in which parameters become four-form expectation values and can support an F-type breaking route | Does not derive the temporal seam, sector rule, D-type breaking, or soft spectrum |
| `source:witten-1996-flux-quantization` — E. Witten, [*On Flux Quantization in M-Theory and the Effective Action*](https://arxiv.org/abs/hep-th/9609122), `arXiv:hep-th/9609122v2` | `CITES`-only shifted flux lattice required if the completion is specifically M-theoretic | Is not a universal four-dimensional three-form quantization rule and does not select a seam sector |
| `source:camara-ibanez-uranga-2003` — P. G. Cámara, L. E. Ibáñez, A. M. Uranga, [*Flux-induced SUSY-breaking soft terms*](https://arxiv.org/abs/hep-th/0311241), `arXiv:hep-th/0311241v2` | `CITES`-only downstream D-brane flux/soft-term template | Does not show that the temporal seam selects the flux or fixes the present spectrum |
| `source:dienes-1994` — K. R. Dienes, [*Modular Invariance, Finiteness, and Misaligned Supersymmetry*](https://arxiv.org/abs/hep-th/9402006), `arXiv:hep-th/9402006v1` | `CITES`-only full-string modular UV-cancellation mechanism without level-by-level spacetime SUSY | Requires a complete tachyon-free modular-invariant spectrum that has not been built here |
| `source:kiermaier-okawa-zwiebach-2008` — M. Kiermaier, Y. Okawa, B. Zwiebach, [*The boundary state from open string fields*](https://arxiv.org/abs/0810.1737), `arXiv:0810.1737v2` | `CITES`-only BRST-cohomological boundary-state template | Worldsheet BRST is distinct from the Phase 28 homogeneous BFV charge and does not derive a temporal CPT seam |
| `source:moosavian-sen-verma-2019` — S. F. Moosavian, A. Sen, M. Verma, [*Superstring Field Theory with Open and Closed Strings*](https://arxiv.org/abs/1907.10632), `arXiv:1907.10632v3` | `CITES`-only quantum BV/master-equation completion gate | Does not provide the actual compactification, seam state, or saddle contribution |
| `source:teitelboim-1983-gravitational-field` — C. Teitelboim, [*Quantum Mechanics of the Gravitational Field in Asymptotically Flat Space*](https://doi.org/10.1103/PhysRevD.28.310), Phys. Rev. D 28 (1983) 310 | `CITES`-only positive-proper-time causal/source boundary for the Phase 29 half-line distinction | Does not derive the local flat endpoint measure, Fresnel normalization, physical density, or PL coefficient |
| `source:garcia-vergara-urrutia-1995` — J. A. García, J. D. Vergara, L. F. Urrutia, [*BRST–BFV quantization and the Schwinger action principle*](https://arxiv.org/abs/hep-th/9511092), Int. J. Mod. Phys. A 11 (1996) 2689–2706, [doi:10.1142/S0217751X96001309](https://doi.org/10.1142/S0217751X96001309) | `CITES`-only extended multiplier/ghost action, BRST charge, fermionic gauge fixing, endpoint boundary-condition and boundary-term framework | Does not determine the repository gauge fermion or local measure convention, Phase 29 gravitational determinant, conformal cycle, physical endpoint measure, or state |
| `source:forman-1987-functional-determinants` — R. Forman, [*Functional determinants and geometry*](https://doi.org/10.1007/BF01391828), Invent. Math. 88 (1987) 447–493 | `CITES`-only boundary-value functional-determinant framework for the Phase 30 magnitude/phase distinction | Does not turn the hybrid midpoint relative magnitude into an absolute gravitational determinant or fix its continuum determinant-line phase |
| `source:gratton-turok-2001` — S. Gratton, N. Turok, [*Homogeneous modes of cosmological instantons*](https://doi.org/10.1103/PhysRevD.63.123514), Phys. Rev. D 63 (2001) 123514 | `CITES`-only warning that homogeneous gravitational negative-mode reduction depends on variables and constraint treatment | Does not supply the Phase 30 phase-space BFV super-Hessian, ghost complex, or physical determinant |
| `source:halliwell-louko-1990-part-iii` — J. J. Halliwell, J. Louko, [*Steepest-descent contours in the path-integral approach to quantum cosmology. III. A general method with applications to anisotropic minisuperspace models*](https://doi.org/10.1103/PhysRevD.42.3997), Phys. Rev. D 42 (1990) 3997–4031 | `CITES`-only minisuperspace lapse-contour framework for the endpoint and global-cycle boundary | Does not determine this model's endpoint bypass, Airy connection data, Phase-35 physical Van Vleck block, complete upward cycle, determinant-line orientation, or integer PL coefficient |
| `source:rogers-2000-gauge-fixing-bfv` — A. Rogers, [*Gauge Fixing and BFV Quantization*](https://arxiv.org/abs/hep-th/9902133), Class. Quantum Grav. 17 (2000) 389–397 | `CITES`-only gauge-fermion admissibility and Gribov-boundary framework for the Phase 31 hybrid-BFV completion boundary | Does not validate the hybrid spectral/midpoint regulator, prove gauge-parameter independence, or supply an absolute physical determinant |
| `source:halliwell-ortiz-1993` — J. J. Halliwell, M. E. Ortiz, [*Sum-over-histories origin of the composition laws of relativistic quantum mechanics and quantum cosmology*](https://doi.org/10.1103/PhysRevD.48.748), Phys. Rev. D 48 (1993) 748–768 | `CITES`-only composition-law framing for distinguishing causal positive-proper-time kernels from constraint-supported objects in Phase 32 | Does not select the lapse contour class, compute the repository's projected crossing, or orient a signed full-joint/global intersection coefficient |

Every source above has a `PRIMARY*` source state in the local graph. That is a source classification, not a claim that the sixty-seven-item inventory exhausts the literature.

## Claim-family coverage

| Claim family | Graph sources | Coverage type |
| --- | --- | --- |
| Historical Phase 11–15R collar, rigid-wall, formal-WKB, compact-T3 charge and parent-sign lineage | Phase-local reports, contracts and source/convention packets; P15R Hohl v1/Kallosh v3 packet | Repository calculation evidence is hash-indexed separately from literature framing. The backfill preserves exact facts, contradictions, inconclusive construction boundaries and the Phase 15A invalid-sequence break; it does not assert literature completeness, a physical branch-superpartner theorem, or a TOE result. Primary-source node expansion remains a separate curation task because the frozen packets already preserve exact citations and locators. |
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
| Phase 19 exact SUGRA reductions | Kallosh–Linde (2010, 2013) | Two `DERIVED_FROM` edges from the shift and no-scale evidence; local Hessian thresholds and bounce shooting remain repository calculations |
| Phase 19 tensor-bound comparison | BICEP/Keck; Balkenhol et al. | Two limit inputs attached to the slow-roll evidence; neither source is attributed the local bounce calculation |
| Phase 20 leading WDW envelope | Hartle–Hawking; Hartle–Hawking–Hertog | The 1983 source provides the Euclidean-action baseline through `DERIVED_FROM`; the later paper frames complex-saddle/history-measure limits. Neither derives the conditional independent-pair rule |
| Phase 20 coherent interference and probabilities | Halliwell | One `CITES` edge for current/decoherent-histories interpretation; the algebraic \(\cos^2S\) identity remains local evidence |
| Phase 20 classical F-flatness versus quantum local SUSY | Cheng–D'Eath–Moniz; Kallosh–Linde (2013) | The Cecotti model source attaches to the local auxiliary calculation; the minisuperspace source frames why that does not solve the quantum constraint |
| Phase 20 curvature context | DESI DR2 | Observational boundary only; no `DERIVED_FROM` edge and no curvature-detection claim |
| Phase 20 loop-selection frontier | Barvinsky–Kamenshchik–Mishakov | Proof of principle attached to an open problem in a different model, not evidence that the requested determinant has the needed slope |
| Phase 21 remainder versus connected generator | Kubo | One `CITES` edge from the reusable distinction; the finite Gaussian coefficients remain repository evidence |
| Phase 21 determinant and regularization boundary | Osterwalder–Schrader II; Hawking | Technical interpretation boundaries only; neither source turns the finite Gaussian into a physical WDW probability |
| Phase 21 physical flux measure | Halliwell; Hartle–Marolf | Decoherence/current/constraint-system framing attached to the sector-measure concept, not a derived prior |
| Phase 21 three-form seam-kernel frontier | Bousso–Polchinski; Bandos et al. | Compact flux/membrane frameworks attached to an open problem; no transition rate or kernel is imported |
| Phase 22 finite doubled purification | Ojima; Israel | Thermofield/KMS and doubled-purification framing only; the 31 exact checks remain repository evidence |
| Phase 22 Gibbs covariance versus vacuum SUSY | Buchholz–Ojima | Prevents \([\rho,Q]=0\) from being promoted to an unbroken finite-temperature vacuum claim |
| Phase 22 equal-source SK trace | Haehl–Loganayagam–Rangamani | Reused to distinguish elementary unitarity from the unconstructed SK ghost/BRST completion |
| Phase 23 full-lapse rigging map | Marolf (1995) | `concept:distributional-rigging-map-versus-bounded-projector` cites the RAQ/group-averaging framework; the Abel/Gaussian regulators and seed calculation remain repository evidence |
| Phase 23 induced product versus signed WDW current | Hartle–Marolf | Reused to frame the distinction between induced products and constraint-system probability formulations; it does not derive the compact bridge or select a state |
| Phase 24 minisuperspace constraint and boundary response | Halliwell (1988); Barvinsky–Nesterov | `CITES`-only framing for the WDW/lapse measure-ordering and boundary-operator context; neither source is a `DERIVED_FROM` receipt for the frozen action, saddle, Hessian, or rank calculation |
| Phase 24 gravitational contour obstruction | Gibbons–Hawking–Perry; Halliwell–Louko | `CITES`-only bounds on the conformal/contour interpretation; Phase 24 computes neither a thimble intersection number nor the bulk fluctuation Morse spectrum |
| Phase 24 factorization and conditional Gaussian interpretation | Donnelly–Freidel; Bombelli et al. | `CITES`-only bounds on the subsystem and Schmidt-algebra reading; they do not define the physical boundary measure, a Choi prescription, trace-class density, or seam entropy |
| Phase 25 lapse saddle, Jacobi response, and local segment | Halliwell–Louko; Gutzwiller; Feldbrugge–Lehners–Turok | `CITES`-only principal-function, caustic, and thimble framing; the frozen saddle, curvature, monodromy, fold, and local segment are repository evidence |
| Phase 26 bounded arm and real Airy fold | Witten (2010); Feldbrugge–Lehners–Turok; Chester–Friedman–Ursell | `CITES`-only relative-cycle and uniform-asymptotic framing; no source supplies the recorded endpoint or global coefficient |
| Phase 27 Wick map, raw endpoint, and half-line operator | Halliwell (1988); Teitelboim; Marolf; Gutzwiller; Banihashemi–Jacobson | `CITES`-only WDW measure/ordering, causal-vs-gauge, RAQ, semiclassical, and integration-order boundaries; the raw (1/|T|) result remains distinct from a full BFV kernel |
| Phase 28 homogeneous BFV and bounded crossings | Fradkin–Vilkovisky; Batalin–Vilkovisky; Gibbons–Hawking–Perry; Halliwell–Louko; Feldbrugge–Lehners–Turok | `CITES`-only constrained-quantization and contour frameworks; they do not turn the scheme-normalized ghost determinant, local Gaussian, or finite crossings into a physical normalization or intersection coefficient |
| Phase 28 string/three-form completion gate | Farakos et al.; Bandos et al.; Witten (1996); Cámara–Ibáñez–Uranga; Dienes; Kiermaier–Okawa–Zwiebach; Moosavian–Sen–Verma | All are `CITES` only: the direct three-form sources motivate an F-type route, D-type breaking needs an extra vector/gauging sector, Witten's shifted lattice applies only to an M-theory embedding, and no cited source derives the temporal seam or its local-EFT sector rule |
| Phase 29 zero-lapse distribution and reduced BFV measure | Halliwell (1988); Teitelboim (1983, PRD 28); García–Vergara–Urrutia; Gibbons–Hawking–Perry; Marolf | `CITES`-only WDW measure/ordering, half-line causal/source, endpoint BFV, conformal-sign, and group-averaging boundaries; none derives the frozen `delta_flat` calculation or upgrades it to a physical WDW measure/state |
| Phase 30 coupled conformal tangent and determinant-line gate | Gibbons–Hawking–Perry; Forman; Gratton–Turok; Halliwell–Louko III | `CITES`-only conformal-factor, boundary-determinant, constrained negative-mode, and lapse-contour framing; none supplies the finite-cutoff Schur-shifted cycle, derives a full BFV super-Hessian, or fixes the determinant-line phase and integer PL coefficient |
| Phase 31 canonical lift and homogeneous BFV quartets | Gratton–Turok; Fradkin–Vilkovisky; García–Vergara–Urrutia; Rogers; Halliwell (1988) | `CITES`-only constrained negative-mode, BFV, endpoint, admissibility, and clock/polarization framing; none supplies the repository's finite Schur identities, relative cancellation, physical determinant, or SUSY/SUGRA Hessian |
| Phase 32 lapse prescriptions and projected lapse-base crossing | Teitelboim (1983, PRL); Halliwell–Ortiz; Banihashemi–Jacobson; Witten (2010); Feldbrugge–Lehners–Turok; Halliwell–Louko III; Gibbons–Hawking–Perry | `CITES`-only causal/group-average, below-origin-contour, relative-homology, and conformal-factor framing; none computes the recorded projected crossing, promotes its convention-conditional coordinate sign to a signed full-joint intersection, chooses the contour by CPT/Pin, or supplies the global coefficient |
| Phase 33 simple-fold Airy scale and global-cycle gate | Chester–Friedman–Ursell; Witten (2010); Halliwell–Louko III; Gibbons–Hawking–Perry | `CITES`-only coalescing-saddle, relative-cycle, lapse-contour, and conformal-factor framing; none supplies the measured two-branch data, selects the Airy contour/Stokes multiplier or analytic amplitude, or fixes the determinant line, full dual census, global coefficient, or physical state |
| Phase 34 reduced directed branch pair | Chester–Friedman–Ursell; Witten (2010); Halliwell–Louko III | `CITES`-only fold, relative-cycle, and lapse-contour framing; none supplies the recorded incoming segment or outgoing branch pair, connects them across the fold, or computes the full joint flow and global coefficient |
| Phase 35 sampled reduced endpoint determinant transport | Chester–Friedman–Ursell; Witten (2010); Halliwell–Louko III | `CITES`-only fold, determinant-line/orientation, and lapse-contour framing; none supplies the 57-point table, upgrades sampled nonvanishing to a continuum theorem, identifies the physical Van Vleck block, or fixes the absolute Maslov orientation, full superdeterminant, or global coefficient |
| Phase 36 declared local Airy bases and finite-radius BVP root laterals | Chester–Friedman–Ursell; Witten (2010); Halliwell–Louko III; Banihashemi–Jacobson | `CITES`-only uniformization, relative-cycle, lapse-contour, and below-origin prescription framing; none identifies the original gravitational cycle with a declared Airy contour, turns basis-dependent first duals into one transported physical dual, realizes formal upward cycles with the BVP roots, derives the hard Airy/Airy-prime amplitudes, selects an arm, or fixes the global coefficient or state |
| Phase 37 closed local root and reduced-half-form holonomy | Chester–Friedman–Ursell; Witten (2010); Witten (2015); Freed–Hopkins | `CITES`-only coalescing-saddle, relative-cycle, fermion-Pfaffian, and Pin/reflection frameworks; none supplies the six BVP paths or sampled lift, turns root monodromy into a relative-cycle map, excludes intersample determinant zeros or alias winding, identifies the reduced bosonic half-form with a fermion Pfaffian or spacetime Pin lift, constructs the full BFV/SUGRA operator or supercharge, or derives a state |
| Phase 38 Gate-1 identifiability and bounded end ledger | Witten (2010); Chester–Friedman–Ursell; Teitelboim (1983, PRL); Banihashemi–Jacobson | `CITES`-only relative-cycle, coalescing-saddle, causal-vs-gauge-invariant lapse, and below-origin-contour frameworks attached to the next open construction; none supplies a physical injectivity theorem or admissible completions, turns the finite surrogate into physical homology, provides the sampled continuation, promotes conjugation to an independent branch, proves continuous disjointness, classifies the box exits, fixes the global vector, or computes the hard CFU functions |
| Phase 39 frozen \(m=2\) local joint-intersection pilot | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only relative-cycle and lapse-contour framing inherited through the Gate-1 opens; none supplies the frozen action, cycle/metric choices, discrete saddle, finite-time upward-chart patch, local six-real determinant signs, sampled first-hit ledger, or global completion. No new literature source is introduced by Phase 39 |
| Gate-1 scalar zero-lapse planned boundary control | Chakrabarti–Shafikov; Brunetti–Fredenhagen | `CITES`-only boundary-value topology and scaling-degree extension framework frozen in the one-shot plan. The actual run was invalid before theorem guards, so neither source is represented as executed evidence or as support for a zero-lapse verdict |
| Phase 40 frozen \(m=3\) rank-one odd-response and local R10 pilot | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only relative-cycle and lapse-contour framing inherited through the still-open Gate 1; none supplies the three-midpoint action, rank-one phi source, odd response, fixed-mobility/launch-ellipsoid construction, five sampled local R10 signs, local clamp, or global completion. No new literature source is introduced by Phase 40 |
| Phase 41 frozen \(m=4\) two-source and local R14 pilot | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only relative-cycle and lapse-contour framing; none supplies the four-midpoint action, two-source response, five local R14 candidates, repairs the failed tangent contract, identifies a cross-cutoff determinant line, or licenses global completion. No new literature source is introduced by Phase 41 |
| Phase 42 fixed-root tangent disentanglement | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only framing inherited through the still-open Gate 1; none arbitrates the repository's solver-noise/step-pair diagnostics, local Hessian-action anomaly, endpoint time-column comparison, or sufficient normalized local-matrix homotopy. No new literature source is introduced by Phase 42 |
| Phase 43 frozen local high-precision RHS arbitration | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only framing inherited through the still-open Gate 1; none supplies the repository's independent exact/80/120-decimal derivative calculation, chooses its numerical thresholds, explains the 13/90 NumPy64 output mismatches or 28/33 finite-difference ledger, proves a formula defect, or promotes local arithmetic to an integrated tangent or global intersection invariant. No new literature source is introduced by Phase 43 |
| Phase 44 frozen NumPy64 local RHS error decomposition | Witten (2010); Teitelboim (1983, PRL); Banihashemi–Jacobson | Reused `CITES`-only framing inherited through the still-open Gate 1; none supplies the repository's exact independent/source formula comparison, byte-faithful AST trace, S0-to-S7 signed decomposition, six contraction alternatives, fixed forward-error envelopes, 13/77 cohort coverage, or nonexclusive mixed-rounding interpretation. No source proves correct rounding, selects one causal stage, repairs the integrated tangent, or licenses a global intersection invariant. No new literature source is introduced by Phase 44 |
| Non-numbered Gate-1 straight-lift, phase-band, scalar-source, finite bosonic canonical, trace-gauge, V0 endpoint, off-shell, principal-FIO and improved-static BFV zero-mode controls | Witten (2010); Banihashemi–Jacobson; Gibbons–Hawking–Perry; Henneaux–Teitelboim–Vergara; García–Vergara–Urrutia; Marolf (1996); Halliwell (1988); Rogers; Hörmander; Van Vleck | Witten supplies only relative-cycle/good-end framing. Banihashemi–Jacobson supplies the local trace-gauge/FP premise and spatially flat benchmark, not a global slicing theorem or this curved chart. Henneaux–Teitelboim–Vergara supplies endpoint-transformation/improved-action framing; García–Vergara–Urrutia supplies the extended BFV framework but not the repository gauge fermion or measure convention; Marolf and Halliwell bound full-lapse minisuperspace readings; Rogers separates local FP nonvanishing from global admissibility; Hörmander and Van Vleck frame principal microlocal and semiclassical determinant scope. Repository evidence supplies the bad subsequence, affine class, scalar-source link, convergence obstruction, trace reduction, relational action, U_plus classical Darboux chart, local principal momentum FIO, exact coarea nonpass for its uncorrected one-term amplitude, and one local improved-static BFV zero-mode source algebra under declared measures. It does not supply a corrected full symbol, normalized endpoint transform, Hilbert measure, ordering, self-adjoint domain, spectral delta(C), two-endpoint/full-trajectory BFV kernel, absolute functional measure, global normalization, other-component atlas, old fixed-a equality, zero lapse, physical cycle, global coefficient, physics or TOE. |

Phase 15R remains a historical **scoped census**, not a duplicated or literature-wide source ledger.
Its Hohl v1/Kallosh v3 hashes, locators, conventions, and role restrictions remain authoritative in
[`PHASE15R_SOURCE_CONVENTION_PACKET.json`](../../../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json).
The local graph now also pins its runner, report, result, replay and provenance artifacts and connects
them to the Phase 11–15A lead-in. This does not imply source completeness: it preserves only the two
frozen-census target states needed to understand why Phase 16 independently tested BGG.

## Source pinning

BGG is the only source in the graph with a pinned archive version, local content hashes, and equation anchors. The pinned record is:

- Version: `hep-th/0005225v1`
- e-print gzip SHA-256: `9752bda85371cdb572f82a0d6d22c2e6447048620400e61e7c7ba7e7afffdcbc`
- `PRmain.tex`: `3b776927675eafa3fb7ee5932d202b18cb0f77eb896281b7f2f910a6bce30d33`
- `AppendixA.tex`: `178da9280eda9aa356e84c7ec0df490186f60775c696db374963cca378cd9667`
- `Section3.tex`: `7bbd20f7a3a00e40a29b17f64f451bf329596db575eee0bb455bf23db937b037`
- `Section4.tex`: `b0e03e31bf3e925936362a3691a23aa93f752372e08d27c518403ec97c6657aa`
- Anchors: `Formdef`, `Leib`, `A.1`, `A.2`, `spincom`, `GRA.240–GRA.242`, `CPN.13`, `CPN.26`, `CPN.40`, `CPN.59`, `CPN.74–CPN.100`, `CPN.130`, `CPN.133–CPN.143`

The other sixty-two graph sources have stable DOI/arXiv locators but no stored local content hash or equation-level anchor. Consequently, the Phase 17–44 and non-numbered Gate-1 literature links document source models, framing, and comparison boundaries while the exact and numerical results remain repository evidence. See [`PHASE16_BGG_SOURCE_NOTES.md`](../../../cpt_temporal_folded_susy/PHASE16_BGG_SOURCE_NOTES.md) for the detailed BGG source ledger.

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

Phase 19 adds a separate background-and-state frontier:

- a minisuperspace wavefunction, seam path integral, or measure that selects \(\phi_0\);
- a CPT/Pin-compatible perturbation Gaussian state on a fixed closed background;
- full discrete \(S^3\) scalar and tensor propagation through the bounce;
- reheating and the map from \(N_{\rm acc}\) to the observed pivot \(N_*\);
- full covariant multifield and fermionic SUGRA stability.

Phase 20 sharpens the background-selection frontier without closing it:

- the exact complex Starobinsky scalar-gravity saddle, WDW current or decoherent-histories measure, and factor ordering;
- a CPT/Pin sheet Hilbert-space inner product, overlap, sewing action, and derived probability-composition rule;
- the local-SUGRA wavefunction including gravitino and ghost sectors;
- the gauge-fixed boson–fermion–gravitino one-loop determinant with zero modes and renormalization;
- an untuned quantized four-form selection spectrum;
- a joint seam derivation of initial amplitude, reheating history, and present curvature distribution.

Phase 21 adds the determinant-to-probability frontier:

- a flux- and harmonic-dependent cross-sheet kernel derived from compact three-form SUGRA or a charged-membrane saddle;
- membrane charge, tension, boundary ensemble, zero/negative modes, and determinant prefactors;
- a physical flux-sector base measure with a specified WDW current/inner product or decoherence functional;
- a finite joint distribution over \((n,\phi)\) with an interior peak, rather than a cutoff endpoint or imposed target.

Phase 22 adds the finite-to-full density frontier:

- a constrained homogeneous complex-cap density with a primed determinant, collective-coordinate
  Jacobian, and physical WDW current instead of a free \(\omega=0\) insertion;
- an infinite-mode Hilbert–Schmidt/UV-renormalized product-state test;
- a spacetime Clifford/Pin lift rather than the finite occupation-basis involution;
- the coupled gauge-fixed gravitino–Goldstino–ghost boundary operator, Pfaffian phase, physical
  projector, positivity, and trace-class test.

Phase 23 sharpens the constrained-density frontier without closing it:

- replace the continuous spectral normal form and compact Dirichlet calibration by the actual closed
  Starobinsky/Cecotti Wheeler–DeWitt operator and admissible lapse/complex-cap contour;
- derive, rather than supply, the bridge \(B\), physical product, relative weights, and any preparation
  parameter;
- establish factor-ordering, constraint-rescaling, clock-patch, zero-mode-measure, and regulator
  independence;
- only then test the coupled local-SUGRA/BRST boundary operator and its positivity or trace class.

Phase 24 supplies a connected real homogeneous interval but leaves two explicit frontier nodes open:

- `open:p24-gravitational-thimble-and-bulk-determinant`: choose the lapse/conformal Picard–Lefschetz
  contour, calculate its intersection number, and construct the gauge-fixed primed bulk fluctuation
  operator with Faddeev–Popov/BRST ghosts and determinant;
- establish the inhomogeneous scalar, vector, tensor, chiralino, gravitino, Goldstino, and ghost mode
  content, rather than identifying the boundary-Hessian signs with a bulk Morse census;
- `open:p24-physical-two-boundary-density-and-entropy`: specify an outgoing/outgoing or Choi reflection
  prescription, physical WDW/BFV boundary measure and inner product, trace normalization, and a
  trace-class test before interpreting the conditional scalar Gaussian as a density or entropy;
- only after those gates, test CPT/Pin sewing, local-SUGRA Calderón blocks and Ward identities, and any
  claimed selection of an inflaton value, curvature scale, or SUSY-breaking scale.

Phases 25–28 advance the lapse analysis but leave five sharper frontier nodes open:

- `open:p28-global-relative-homology-and-intersection`: complete the saddle and dual-cycle census,
  asymptotic endpoints, singular loci, Stokes jumps, and the integer coefficient of the specified
  physical original contour; a bounded arm or finite constructed crossing is not that coefficient;
- `open:p28-zero-lapse-uniform-bfv-kernel`: combine the endpoint factors, BFV/FP measure, zero modes,
  and a uniform determinant across `T=0`; the Phase 27 raw Van Vleck divergence and Phase 28 reduced
  Dirichlet-ghost control are different objects;
- `open:p28-full-gauge-reduced-superdeterminant`: include all nonzero-mode metric, conformal, scalar,
  fermion, gravitino, Goldstino, and ghost operators, their priming, phases, and renormalization;
- `open:p28-physical-state-and-density`: supply the WDW/BFV physical product, boundary factorization,
  normalization, positivity, and trace-class test after the contour and determinant are fixed;
- `open:p28-string-three-form-soft-spectrum`: derive rather than assume a compact temporal-seam
  kernel and local-EFT sector rule, then compute a persistent F-type breaking sector and soft terms.
  A D-type route needs an additional vector/gauging construction. Witten's shifted flux lattice is a
  requirement only for a specifically M-theoretic embedding. In source-free local EFT regions the
  three-form constants are fixed, while a global path integral may still require a separately derived
  sum over sectors.

Phase 29 closes only the frozen leading distributional normalization control and adds two explicit
frontiers:

- `open:p29-conformal-bfv-uniform-parametrix`: choose the conformal/BFV cycle and construct the
  endpoint-completed operator-valued parametrix beyond leading quadratic order with the full primed
  nonzero-mode determinant;
- `open:p29-physical-endpoint-measure-and-ordering`: derive the physical WDW endpoint measure,
  factor ordering, and product instead of assuming local flat `da dphi`, then re-test the identity
  limit, normalization, and state interpretation.

The leading `delta_flat` limit does not close either frontier, does not remove the pointwise `1/N`
pole, and does not determine the global PL coefficient.

Phase 30 partially advances the first frontier by constructing a finite-cutoff local coupled
field–lapse Gaussian tangent and recording a declared-measure relative endpoint magnitude. It also
sharpens the remaining obstructions: the tested product contour keeps a negative direction, the bare
determinant sign alternates with cutoff parity, one holomorphic lapse sheet has the wrong negative-axis
identity sign, and the shifted-ray endpoint limit is not an intersection number. No full BFV ghost
complex or phase-space BFV super-Hessian was evaluated. The nonlinear global cycle, determinant line
through `N=0`, full primed superdeterminant, upward-cycle intersections, and regulator removal therefore
remain within `open:p29-conformal-bfv-uniform-parametrix`.

Phase 31 partially supplies the previously absent homogeneous canonical/BFV layer. Exact momentum
elimination reproduces the configuration Hessian, the unreduced canonical sign is stable over the
recorded cutoffs, and nonzero alpha=0 quartet factors cancel in a same-hybrid-regulator relative ratio.
The bare bosonic BFV sign still alternates, however, and no absolute phase, zero-mode measure,
constraint reduction, gauge-parameter independence, inhomogeneous mode determinant, or SUSY/SUGRA
Hessian is obtained. The local `p_a` clock scan also changes endpoint polarization.

Phase 32 fixes a narrower contour question only after the lapse class is supplied as independent input.
The positive half-line has endpoint contact, while the full real line passing below zero gives one
recorded finite-radius projected crossing on the tracked homogeneous lapse-base sheet. Its coordinate
sign is `+1` only under the declared ambient, column, dual-flow, and Gaussian-lift orientations; no
signed full-joint local intersection is assigned. The upper bypass misses that positive dual. This does
not close `open:p28-global-relative-homology-and-intersection`: other dual
components, complex sheets, good ends, Stokes jumps, and the oriented superdeterminant are uncomputed.
Nor does complex conjugation close `open:p32-cpt-pin-lapse-class-selection`.

Phase 33 resolves the recorded real caustic only inside a local simple-fold chart. The universal Airy
normal form and two-branch scaling do not choose the complex argument phase, contour/Stokes multiplier,
analytic amplitude, measure, or determinant line. The chart's disjointness from the recorded lapse
pieces also does not continue any arm after it leaves the chart. These missing data are explicit in
`open:p33-airy-cycle-amplitude-and-global-continuation`; global `n_sigma` and the full uniform physical
kernel remain open.

Phase 34 continues a bounded conjugate pair of reduced stationary-family branches beyond the fold,
and Phase 35 transports their declared endpoint-Jacobi determinant section only on a finite sampled
table. The cited fold, relative-cycle, and lapse-contour sources frame those operations but do not
connect the incoming physical cycle to either branch, prove a zero-free determinant lift, identify the
physical Van Vleck block, or orient the absolute Maslov line.

Phase 36 fixes exact identities in separately ordered CW and CCW local Airy bases and independently
tracks both BVP root-sheet laterals on three finite radii. The first duals in those two bases use
different companion cycles, so the source-framed inverse-transpose algebra is not transport of one
common physical upward dual. The BVP root permutations likewise do not realize the formal upward
cycles. Chester--Friedman--Ursell, Witten, Halliwell--Louko, and Banihashemi--Jacobson remain
`CITES`-only boundaries: none supplies the missing original relative cycle, analytic hard quotient and
Airy/Airy-prime coefficients, absolute determinant orientation, complete good-end census, global
`n_sigma`, or physical BFV/SUGRA state recorded in
`open:p36-original-cycle-hard-determinant-and-global-bfv-state`.

Phase 37 replaces the separately based open laterals with six same-basepoint enclosing BVP paths and
records Z2 exchange of both local roots on three finite radii. It also records an order-four conjugacy
class only for the sampled reduced bosonic inverse-square-root lift, conditional on no unresolved
intersample zero or alias winding. Chester--Friedman--Ursell and Witten (2010) frame the local
coalescing-saddle and global relative-cycle distinction; Witten (2015) and Freed--Hopkins frame the
additional fermion-Pfaffian, reflection, and Pin requirements. All four remain `CITES`-only. None
identifies the root permutation with a physical cycle map, supplies the original global contour or hard
CFU coefficients, promotes the reduced bosonic half-form to a fermionic line, breaks the Phase-17 basis
equivalence, constructs a complete BFV/SUGRA operator or spinorial supercharge, or derives a quantum
constraint or state. Those gates remain explicit in
`open:p37-global-cycle-hard-cfu-full-bfv-pfaffian-gate`.

Phase 38 makes the Gate-1 data boundary executable. Witten (2010) frames the need for complete relative
cycles and oriented intersections; Teitelboim and Banihashemi--Jacobson frame why lapse prescriptions and
integration order must be kept explicit; Chester--Friedman--Ursell frames the later hard uniformization
problem. These are `CITES` edges from
`open:p38-explicit-joint-action-cycle-and-oriented-intersections`, not evidence receipts for the five
Phase-38 claims. In particular, no cited source proves that this model's physical projection is
noninjective or nonunique. Only the declared finite surrogate has a demonstrated kernel. Likewise, none
turns three sampled upper checkpoints and real-coefficient conjugation controls into a continuous
two-branch census or a global coefficient. Conditional hard-CFU exploration may proceed in parallel,
but physical promotion still requires Gate 1's typed cycle vector and a joint consistency check.

Phase 39 reuses those same literature boundaries but adds no source-derived physics result. Its explicit
two-segment midpoint action, discrete saddle, frozen Gaussian-lift cap/arm chain candidate,
Morse-whitened finite-time chart, and two direct local \(\mathbb R^6\) signs are repository calculations.
Witten (2010), Teitelboim, and Banihashemi--Jacobson do not select that candidate as the physical original
relative cycle, certify the nonlinear upward manifold, search its straight arms or reintersections,
classify the sampled box exits as good ends, choose a non-Stokes lateral chamber, or supply cutoff and
metric-homotopy stability. The calculation therefore stays a local Gate-1 pilot rather than a
literature-backed global Picard--Lefschetz coefficient.

Phase 40 likewise adds no source-derived physics claim. Its three-midpoint scalar, antisymmetric
rank-one phi endpoint source, resolved odd block and sampled response, fixed delta-zero flow mobility,
delta-dependent Morse launch ellipsoids, five local \(\mathbb R^{10}\) candidates, and K-launch clamp are
repository calculations. The inherited sources do not promote the endpoint mutation to a physical time
arrow or CPT breaking, supply the independent source needed to probe the full odd sector, identify a
launch ellipsoid with a physical metric deformation, prove a continuous candidate branch, or provide an
exact complete upward manifold. Witten's relative-cycle framework in particular keeps the five local
signs distinct from a physical original-cycle pairing and global Picard--Lefschetz coefficient.
Teitelboim and Banihashemi--Jacobson continue to frame lapse-prescription and integration-order questions;
they do not select this frozen cycle candidate. No new source node or literature edge was added, and the
missing \(m=4\)/cutoff comparison, arms, reintersections, component census, Stokes chamber, good ends,
BFV/Pfaffian/Pin orientation, state, and global coefficient remain open.

Phase 41 also adds no source-derived physics claim. Its four-midpoint action, independently continued
two-source saddle grids, finite-precision rank-two response, fixed zero-source mobility, and five local
\(\mathbb R^{14}\) cap candidates are repository calculations. The retained `u2` finite-difference
plateau failure leaves both source-scoped robustness claims inconclusive even though the local roots,
declared signs, overlap, launch, and path ledgers were computed. The inherited relative-cycle and
lapse-contour sources neither repair that tangent audit nor identify the separately audited m=3/m=4
signs with one determinant line. They also do not select a physical original joint cycle, complete the
arms or component/end census, fix a Stokes chamber, or supply a global Picard--Lefschetz coefficient.
No new source node or literature edge was added; Gate 1 remains open and every bounded/global,
cutoff/continuum, BFV/Pfaffian/Pin, SUSY, and quantum-gravity promotion remains unlicensed.

Phase 42 likewise adds no source-derived physics claim. Its checkpoint-only rerun, fixed-step derivative
tiers, solver envelopes, local real-directional Hessian-action tests, pointwise multi-cause ledger, and
normalized local-matrix homotopy are repository diagnostics at three immutable \(m=4\) roots. The
inherited sources do not decide whether finite-difference behavior comes from solver noise or the frozen
old step pair, prove that a protocol-defined local Hessian-action anomaly is an implementation bug, or
turn the appended time-column comparison into independent bug evidence. That time comparison uses
different solver endpoints and remains an endpoint solver/state diagnostic. Nor do those sources turn a
sufficient normalized local-matrix homotopy into reference-tangent correctness, a physical metric
homotopy, a common determinant line, or a global orientation theorem. The shared-zero reference fails
the frozen neighbor-stability threshold, so the all-column reference tangent remains inconclusive.
Exactly 16 global-completion prerequisites remain false and 6 promoted outputs remain null. No new
source node or literature edge was added; Gate 1 remains open and all global, continuum,
BFV/Pfaffian/Pin, SUSY, and quantum-gravity promotions remain unlicensed.

Phase 43 likewise adds no source-derived physics claim. Its exact binary64-ratio lifts, independently
rebuilt four-element action, direct-gradient directional identity, 80/120-decimal evaluation,
unchanged-step and prospective finite-difference ladders, uniform source threshold, 90-slot
implementation ledger, and all-33 anomaly quantifier are repository calculations. The inherited
relative-cycle and lapse-contour sources do not corroborate the local derivative reference, diagnose
the 13 NumPy64 output flags, assign a formula error or unique code defect, explain the five exceptions
to the all-33 sufficient finite-difference claim, or choose an arithmetic remediation. They also do not
turn frozen local algebra into an integrated tangent, ODE solver-noise result, local orientation,
determinant line, original regulated cycle, or global Picard--Lefschetz coefficient. Exactly 16
global-completion prerequisites remain false, 6 global outputs and 7 desired outputs remain null, and
the Phase-42 reference tangent remains inconclusive. No new source node or literature edge was added;
Gate 1 remains open and all global, continuum, BFV/Pfaffian/Pin, SUSY, and quantum-gravity promotions
remain unlicensed.

Phase 44 likewise adds no source-derived physics claim. Its exact componentwise comparison of the
declared source and independent formulas, byte-faithful NumPy64 boundary and AST traces, signed
S0-to-S7 telescopes, six fixed contraction alternatives, conditioning diagnostics, declared
forward-error envelopes, complete 13/77 cohort coverage, and nonexclusive tri-state ledger are
repository calculations. The inherited sources do not supply those formulas or traces, prove correct
rounding, select a unique coefficient/state/Hessian/contraction cause, identify a best algorithm,
authorize a source rewrite, or turn forward-envelope coverage into an integrated-tangent stability
result. They also do not turn this frozen local arithmetic into a local orientation, common determinant
line, original regulated cycle, or global Picard--Lefschetz coefficient. Exactly 16
global-completion prerequisites remain false, 6 global outputs and 7 desired outputs remain null, the
Phase-42 reference tangent remains inconclusive, and the historical Phase-43 13/90 label is preserved.
No new source node or literature edge was added; Gate 1 remains `OPEN_PARTIAL_PROGRESS` and all global,
continuum, BFV/Pfaffian/Pin, SUSY, and quantum-gravity promotions remain unlicensed.

The non-numbered trace-gauge discriminator adds two primary `CITES`-only source nodes and reuses three
existing ones. Banihashemi--Jacobson motivates a local trace gauge before the lower-lateral
momentum-first step; Henneaux--Teitelboim--Vergara supplies the endpoint-transversality and improved
action boundary; Marolf, Halliwell, and Rogers bound the full-lapse, gauge-fixed, and global-admissibility
interpretations. None supplies the repository's exact homogeneous pair, FP bracket, shell horizon,
rank calculation, inherited finite-\(m=2\) lapse transformation, or Gaussian benchmark. Those are local
workbench calculations. They support reduction only on existing simple-root charts away from the FP
horizon and contradict only appending the static trace factor to the unchanged proper-time fixed-\(a\)
source. At that discriminator stage the improved-static and time-dependent replacement routes, endpoint
states, BFV measure, source deformation, original cycle, global coefficient, physics, and TOE remained
open or null.

The V0 successor reuses Banihashemi--Jacobson, Henneaux--Teitelboim--Vergara, and Marolf without adding
a source node. It supplies a repository-derived classical local on-shell fixed-\(\Phi_*\) relational
action \(S_{\mathrm{rel}}=S_0-[P]\), finite endpoint flow, local FP reduction, and time-dependent
same-orbit control. The raw-static, HTV improved-static, relational, and auxiliary fixed-\((P,\phi)\)
\(S_0-[PQ]\) action ledgers remain distinct. The sources do not derive this model calculation. A full
off-shell chart, normalized quantum endpoint states, ghost/BFV replacement source and measure, old
fixed-\(a\) equality, full-real-lapse distributional \(\delta(\hat C)\) physical-inner-product kernel,
zero-lapse distribution, and every global, physics, or TOE output remain open or null. In the
continuous-zero-spectrum setting this kernel is not promoted to an ordinary bounded or idempotent
kinematical projector.

The next V0 calculation reuses the same three sources without adding another source node. The sources
bound, but do not derive, the repository's unique positive root for arbitrary real \(c=C\), mixed
generator \(W=-\int_0^P Q(c,u,p)du\), classical componentwise Darboux chart, endpoint potential
\(B=PQ+W-cT-pW_p\), or exact \(c=0\) recovery. Henneaux--Teitelboim--Vergara supplies only the
classical endpoint/canonical framework; Banihashemi--Jacobson supplies only the reduced/configuration
and lapse-contour boundary for its stated integration order; Marolf supplies only the still-uncomputed
full-real-lapse distributional physical-inner-product comparison. None turns the local identity
\(\{T,c\}=1\) into a ghost/BFV completion or global gauge theorem, and none promotes the chart into a
normalized quantum endpoint transform or \(\delta(\hat C)\) kernel.

The principal-endpoint-FIO successor adds Hörmander's original FIO paper and Van Vleck's original
semiclassical paper as `CITES`-only source nodes, and reuses Henneaux--Teitelboim--Vergara,
García--Vergara--Urrutia, and Marolf to keep the endpoint, BFV, and full-lapse layers separate. These
sources frame the local principal phase/symbol calculus and the missing extended data; they do not
derive the repository's phase \(-W\), half-density \(D^{-1/2}\), shell generator, or geometric-versus-
secant coarea discriminator. The repository calculation keeps only a compact-interior principal
momentum FIO and contradicts exact finite-\(\hbar\) unitarity only for its uncorrected one-term
amplitude. A corrected full symbol or spectral transform is not excluded. Ordering, self-adjoint
domains, edge conditions, global Maslov gluing and normalization, coordinate polarization, BFV source,
full-real-lapse \(\delta(\hat C)\), cycle, physics, and TOE remain open or null.

The improved-static BFV zero-mode successor reuses Henneaux--Teitelboim--Vergara,
García--Vergara--Urrutia, Marolf, and Banihashemi--Jacobson as `CITES`-only boundaries. The sources
frame improved endpoint data, the finite extended BFV algebra, and the distinct full-real-lapse target;
they do not derive the repository gauge fermion, endpoint ideal, Fourier measures, oriented
\(-\hbar^2\) coefficient-extraction convention, or reduced-identity control. The repository result
keeps only that finite local algebra. A normalized endpoint-state transform, spectral
\(\delta(\hat C)\), two-endpoint/full-trajectory BFV kernel, absolute functional measure, old-kernel
equality, global cycle, physics, and TOE remain open or null.

These are represented as open-problem nodes, not hidden assumptions or implied literature results.
