# Evidence guide

> This page is a human-readable memory and index over observed repository runs. It is **not** a preregistration, research contract, independent replication, peer review, final scientific verdict, or KG ratification.

Machine-readable records: [`graph.json`](../graph.json) and the Phase 16–30 snapshots in [`../evidence/`](../evidence/), including [`phase25-result.json`](../evidence/phase25-result.json), [`phase26-result.json`](../evidence/phase26-result.json), [`phase27-result.json`](../evidence/phase27-result.json), [`phase28-result.json`](../evidence/phase28-result.json), [`phase29-result.json`](../evidence/phase29-result.json), and [`phase30-result.json`](../evidence/phase30-result.json).

## Reading `PASS` correctly

All 292 Phase 16–30 named exact checks have `status: PASS`. The snapshots contain 124 typed numerical-ledger checks plus one legacy separately recorded Phase 18 SciPy control: 70 numerical controls through Phase 24 in the historical counting, then 12 in Phase 25, 9 in Phase 26, 8 in Phase 27, 9 in Phase 28, 7 in Phase 29, and 10 in Phase 30, for 125 numerical controls in all. Phase 30 contributes 10 exact checks. A `PASS` means that an executable verified its stated equality, rank, obstruction, mutation rejection, counterexample, or bounded numerical comparison. It does not mean every scientific claim passed, that the original-contour intersection coefficient is known, or that a physical state has been constructed.

The scientific direction is stored on:

```text
claim → HAS_EVIDENCE { polarity: SUPPORTS | CONTRADICTS } → evidence
```

Thus `P16.off_shell_b_i_obstruction: PASS` contributes to contradicting the claim that the strict truncation is SUSY-tangent. The snapshot payload may likewise say `FAIL_BY_EXACT_CLEAN_POINT_COUNTEREXAMPLE` for the proposed property while the test detecting that failure passes.

## Observed-run provenance

| Phase | Result and observation | Executable provenance | Outcome |
| --- | --- | --- | --- |
| 16 | `result:P16_BGG_SINGLE_SOURCE_20260816`; `2026-08-16T15:53:21Z` | `cpt_temporal_folded_susy/phase16_bgg_single_source.py`; SHA-256 `95c9346bf4607d955692778a2bf91638a307a3563f51bff57af0635bc548f55c`; introduced in `25bd216cfd1d85bde59c60ec4f2a9d91bdb53d78` | Exit `0`; 20 exact checks |
| 17 | `result:P17_TIME_LINE_FOLD_ALGEBRA_20260816`; `2026-08-16T15:53:21Z` | `cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py`; SHA-256 `4723f6217f1014c52001dd989fb393e7c8547a1a0556bf7c0141c0dcaa20d615`; introduced in `5c95692b4c9ca6d92c617382f5bb9bf6506bfb5d` | Exit `0`; 34 exact checks |
| 18 | `result:P18_GAUSSIAN_SEAM_SPECTRUM_20260816`; `2026-08-16T16:42:39Z` | `cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py`; SHA-256 `01f2d5d04341093494e185529dd67630aef5896e842a4bedddc6d1309271e221`; introduced in `1a5d6d4326da3451ff63274cee654fa504f82f9c` | Exit `0`; 47 exact checks plus 1 separately recorded numerical control |
| 19 | `result:P19_CLOSED_SUGRA_BOUNCE_20260816`; `2026-08-16T17:23:38Z` | `cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py`; SHA-256 `5dbfccd768bb13961222c289ba0754497bec94319f8b33ff602889eaeb469341`; introduced in `90aedef93eadab40156fc22daf87b2d6942f49a6` | Exit `0`; 17 exact checks plus 30 numerical checks |
| 20 | `result:P20_TWO_SHEET_WDW_SELECTION_20260816`; `2026-08-16T17:28:20Z` | `cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py`; SHA-256 `a55ebfca78f07246679fd5fa8791537a0efe1d3370dfa53d8d6410ffc6a95807`; introduced in `c5395bc095399ca450adf555d8d24e21a9166725` | Exit `0`; 18 exact checks plus 14 numerical checks |
| 21 | `result:P21_CONNECTED_SEAM_GAUSSIAN_20260816`; `2026-08-16T18:11:47Z` | `cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py`; SHA-256 `6ac7b2b36da9aa2eeda4c83494427c5d9f006bb9031d6b55d6678bf2ffc5b005`; introduced in `44e2865cc850bf7fef0c4ccebde788ca703ab8d8` | Exit `0`; 27 exact checks plus 7 numerical checks |
| 22 | `result:P22_FINITE_MODE_SEAM_DENSITY_20260817`; `2026-08-17T04:48:31Z` | `cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py`; SHA-256 `0a4da3c60bbd2231892938cb8a74f45bd3e491d9884df4adcc86051053d58dbe`; introduced in `d1befe783386f499818c3b902c90e5a9740e7fb4` | Exit `0`; 31 exact checks, 0 numerical checks |
| 23 | `result:P23_HOMOGENEOUS_MINISUPERSPACE_DENSITY_20260817`; `2026-08-17T05:45:44Z` | `cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py`; SHA-256 `62408abeeec2eb11f104d984c84ffde5c2d6f287e7f07a4021ee6fb3ec202ffd`; introduced in `634d984e25422063a66a497963380fc24ad9f9d2` | Exit `0`; 32 exact checks plus 4 numerical checks |
| 24 | `result:P24_CONNECTED_STAROBINSKY_INTERVAL_20260817`; `2026-08-17T14:21:16Z` | `cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py`; SHA-256 `a625c9390305a0e07ea3b38977dc34b4cce725f8dd19cec1c66b90d8ccf63256`; finalized in `1f5d60c33ace93eb3dd51b3236212dcf5a87703f` | Exit `0`; 6 exact checks plus 14 numerical checks |
| 25 | `result:P25_CONNECTED_LAPSE_SCAN_20260817`; `2026-08-17T15:26:44.354Z` | `cpt_temporal_folded_susy/phase25_connected_lapse_scan.py`; SHA-256 `5fe43ec6997d6bae9c10d78ddb5d13b1806e10934140fd5080fef0dca3492ee8`; introduced in `c9533dc1aa7a11d7a7e53fa10a657b94406a4e54` | Exit `0`; 5 exact checks plus 12 numerical checks |
| 26 | `result:P26_GLOBAL_LAPSE_FLOW_20260817`; `2026-08-17T15:26:44.354Z` | `cpt_temporal_folded_susy/phase26_global_lapse_flow.py`; SHA-256 `c41824d6667d38efe66f5ebf4d0e1ec572d27c78b146b7c044e2e1ffd9868d04`; introduced in `c64eedb5cfb0d2fc49d3cd0243ee198a15a12165` | Exit `0`; 4 exact checks plus 9 numerical checks |
| 27 | `result:P27_LORENTZIAN_LAPSE_ENDPOINT_20260817`; `2026-08-17T15:26:44.354Z` | `cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py`; SHA-256 `36a454ca3f98277cca2c24904a708ec67fa8f7c3556f376e6613cdc0823e0d04`; finalized in `2065de0125674ba9c72888e3d95bc84fec66850b` | Exit `0`; 13 exact checks plus 8 numerical checks |
| 28 | `result:P28_THIMBLE_BFV_INTERSECTION_20260817`; `2026-08-17T15:26:44.354Z` | `cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py`; SHA-256 `496990308456bcc1d28f9649b99053d2a05499c6d3c2c0d233d5576a39a3f018`; introduced in `2065de0125674ba9c72888e3d95bc84fec66850b` | Exit `0`; 10 exact checks plus 9 numerical checks |
| 29 | `result:P29_ZERO_LAPSE_UNIFORM_KERNEL_20260817`; `2026-08-17T15:45:17.466Z` | `cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py`; SHA-256 `0fa8314d3c0385c70ad569ce1c2ad65d506580eef50ef589e7fa2da5f7fb3e76`; introduced/finalized in `4794ff6de9f5f5726bcdd633f64fd4988eb197de` | Exit `0`; 18 exact checks plus 7 numerical checks |
| 30 | `result:P30_CONFORMAL_BFV_DETERMINANT_LINE_20260817`; `2026-08-17T16:38:39.344Z` | `cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py`; SHA-256 `4c402a50aa5f32966faa7e01d65623933ea7d9cff2b43f25b76f89b5efa36cc7`; introduced/finalized in `bbbaa7a9f4d00a9f6a2ef4ffad3d6df4f8ee076d` | Exit `0`; 10 exact checks plus 10 numerical checks |

The Phase 15R evidence node points to the committed [`PHASE15R_RUN_RESULT.json`](../../../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json). It is not duplicated under `ontology/.../evidence/`.

The Phase 25–28 report hashes are `921ffbb7…`, `99b7d7d7…`, `9db755b6…`, and `1c721018…`; the corresponding frozen snapshot hashes are `62e124dc…`, `69cea996…`, `121a440f…`, and `114374d8…`. Phase 28's executable first appears in `2065de0…`; its final report bytes, after source-scope and notation repair, first appear in `1d48edc6160ed915c1a13f21e6f82d7211e8e6fe`. Each executable, report, and snapshot is a distinct artifact node.

The Phase 29 report hash is `d3aa7abf…`; its frozen snapshot hash is `dd13f707…`. Both the final executable and report bytes first appear in `4794ff6de9f5f5726bcdd633f64fd4988eb197de`.

The Phase 30 report hash is `0cf7a2cb39392ab07580207ec4bceb910f200eb9d07f4b5fc7090d1ea456914d`; its fresh snapshot hash is `3ebfec6c9ce43ed499f70ac151508be6a8ad90bca8341d0c7feec2adfac0fadf`. The exact final executable and report bytes first appear in `bbbaa7a9f4d00a9f6a2ef4ffad3d6df4f8ee076d`.

## Evidence-to-claim index

| Evidence group | Checks | Claim and polarity | Scope/source |
| --- | ---: | --- | --- |
| `evidence:p15r-run-result` | See Phase 15R result | Bosonic frozen-census parent — `SUPPORTS`; full off-shell frozen-census parent — `CONTRADICTS` | Frozen two-source census only |
| `evidence:p16-bosonic` | 13 | BGG bosonic kinetic parent — `SUPPORTS` | `(X,T,Y)` kinetic scope; `DERIVED_FROM` BGG |
| `evidence:p16-tangency` | 6 | Specified strict off-shell FLRW tangency — `CONTRADICTS` | Exact clean point on declared locus; `DERIVED_FROM` BGG |
| `evidence:p16-clock` | 1 | Scoped rolling-clock preserved SUSY — `CONTRADICTS` | `W=0`, `F=0`, nonzero real rate, Lorentzian conjugacy; `DERIVED_FROM` BGG |
| `evidence:p17-local` | 6 | Standard support-local half exchange — `CONTRADICTS` | Fixed positive-energy fiber plus support-locality; claim `CITES` HLS |
| `evidence:p17-doubled` | 11 | Fundamental bidirectional exchange — `SUPPORTS`; one-way closure — `CONTRADICTS`; unique basis selection — `CONTRADICTS` | Finite internal doubled-sheet algebra; no physical-action source edge |
| `evidence:p17-reflection` | 4 | Reflection-composed standard local charge — `CONTRADICTS` | Literal `t∈R` line; claim `CITES` HLS |
| `evidence:p17-seam` | 9 | Ordinary real temporal seam — `CONTRADICTS`; doubled-real projector — `SUPPORTS`; physical time reversal as the tested `Q` — `CONTRADICTS` | Finite seam/projector and literal-time scopes; boundary and reflection/Pin sources frame the first two claims, while CPT/Pin remains a separate concept |
| `evidence:p17-sk` | 4 | SK BRST as particle SUSY — `CONTRADICTS` | Abstract four-state quartet; claim cites two SK sources |
| `evidence:p18-charge-and-poles` | 18 exact | Elapsed time alone breaks SUSY — `CONTRADICTS`; free canonical seam generates permanent B/F pole splitting — `CONTRADICTS`; free seam can prepare a non-SUSY state without moving poles — `SUPPORTS` | Equal-mass free Wess–Zumino mode and unchanged future bulk operators; literature links are `CITES`, not `DERIVED_FROM` |
| `evidence:p18-state-and-cpt` | 17 exact | Free seam can prepare a non-SUSY state without moving poles — `SUPPORTS` | Finite scalar canonical kick, finite-mode fermion CAR witness, and CPT-compatible doubled scalar eigenchannels; not a local fermionic Pin action |
| `evidence:p18-uv-and-conditional-controls` | 12 exact + 1 numerical | Sharp spatially local scalar seam is UV admissible — `CONTRADICTS` | Sharp-kick cutoff asymptotics plus conditional Gaussian, collisionless FRW, and inserted-soft controls; no interacting self-energy or Higgs result |
| `evidence:p19-shift-sugra` | 8 exact | Shift reduction and \(\zeta=1/12\) \(H_V\)-heavy benchmark — `SUPPORTS`; displayed endpoint F direction vanishes — `SUPPORTS` | Exact one-field shift trajectory; `DERIVED_FROM` Kallosh–Linde 2010 |
| `evidence:p19-noscale-sugra` | 7 exact | Cecotti reduction and one-sixth sufficient/not-sharp statement — `SUPPORTS`; displayed endpoint F direction vanishes — `SUPPORTS` | Exact one-field no-scale trajectory; `DERIVED_FROM` Kallosh–Linde 2013 |
| `evidence:p19-bounce-local` | 2 exact | Bosonic time-reflection data leave \(\phi_0\) free — `SUPPORTS`; target-shot branches exist — `SUPPORTS` | Classical homogeneous \(k=+1\) turning point |
| `evidence:p19-bounce-shooting` | 24 numerical | Six target-shot \(N_{\rm acc}=50,55,60\) backgrounds — `SUPPORTS`; \(\phi_0\) remains unselected — `SUPPORTS` | Conditional classical background shooting; no state, uniqueness, or parameter-free radius claim |
| `evidence:p19-slowroll-r` | 6 numerical | Quadratic compatibility with current \(r\) bound — `CONTRADICTS`; Starobinsky first-order \(r\) below bound — `SUPPORTS` | Potential slow roll at selected \(N_*\); cited papers supply comparison limits, not the bounce |
| `evidence:p20-leading-wdw-envelope` | 12 exact + 6 numerical | Leading envelope selects \(5.44\) — `CONTRADICTS`; independent-pair \(e^{4sI}\) follows from CPT — `CONTRADICTS`; coherent symmetrization only rescales probability — `CONTRADICTS` | Constant-field de Sitter/WDW control; standard \(e^{2sI}\) versus conditional independent-pair joint probability; no exact complex saddle or sheet inner product |
| `evidence:p20-cecotti-f-direction` | 5 exact + 2 numerical | Cecotti \(5.44\) point is F-flat — `CONTRADICTS` | Classical \(S=0\), positive-real \(T\) trajectory only; not the quantum local-SUSY wavefunction |
| `evidence:p20-curvature-reheating-control` | 1 exact + 6 numerical | Conditional conversion is reproducible — `SUPPORTS`; displayed number is a seam prediction — `CONTRADICTS` | One Phase 19 branch with fixed matterlike reheating, entropy, units, and late-time inputs |
| `evidence:p21-single-mode-gaussian` | 12 exact | Unit baseline — `SUPPORTS`; normalization forces subtraction — `CONTRADICTS`; chosen zero-insertion identity — `SUPPORTS`; R-1 is connected — `CONTRADICTS`; log R is connected — `SUPPORTS` | Positive finite one-mode real-boson Gaussian only |
| `evidence:p21-multimode-gaussian` | 4 exact | Log R is the connected generator — `SUPPORTS` | Finite positive block kernel and singular-value gate; no field-theory determinant |
| `evidence:p21-flux-tail-and-prior` | 11 exact + 7 numerical | Reference subtraction guarantees normalizability — `CONTRADICTS`; one-flux constant-absolute toy sum — `SUPPORTS`; R-1 alone fixes physical flux probability — `CONTRADICTS` | One integer-flux toy with imposed kernel and prior comparisons; no WDW measure or joint \((n,\phi)\) distribution |
| `evidence:p22-susy-and-density` | 16 exact | Positive-frequency density — `SUPPORTS`; reduced Gibbs covariance — `SUPPORTS` | One free SUSY oscillator with \(\omega,\beta>0\); finite temperature is not an unbroken positive-H vacuum |
| `evidence:p22-graded-real-structure` | 5 exact | Graded anti-linear toy involution — `SUPPORTS` | Occupation-basis real structure only; no spacetime Clifford/Pin lift |
| `evidence:p22-bridge-and-sk` | 6 exact | Density/DtN factor two — `SUPPORTS`; equal-source SK normalization — `SUPPORTS` | Finite density covariance and unitarity; no SK ghost/BRST completion |
| `evidence:p22-zero-mode-obstruction` | 4 exact | Free noncompact zero mode has a trace-class TFD limit — `CONTRADICTS` | Fixed \(\beta>0\), \(\omega\to0^+\) in noncompact \(L^2(\mathbb R)\); compact/interacting constrained modes excluded |
| `evidence:p23-rigging-and-lapse` | 10 exact + 1 numerical | Full real lapse gives a distributional rigging map — `SUPPORTS`; it is a bounded kinematical projector — `CONTRADICTS` | Continuous single-constraint spectral calibration; half lapse is a resolvent, not the full rigging delta; Marolf frames RAQ |
| `evidence:p23-shell-and-current` | 10 exact + 1 numerical | Explicit clock/frequency gives positive integrated norm — `SUPPORTS`; positive-frequency local current is pointwise positive — `CONTRADICTS`; CPT-like reality plus zero signed current uniquely selects a density — `CONTRADICTS` | Compact KG-type shell/current control; induced product and signed local current remain distinct |
| `evidence:p23-trace-class-density` | 8 exact + 2 numerical | Imposed bridge gives a positive trace-class regulated density — `SUPPORTS`; unique selection from zero current — `CONTRADICTS` | Separate compact calibration with supplied \(L>0\), \(B_L\), branch orientation, and toy pairing; not cap-derived |
| `evidence:p23-zero-root-and-regulator` | 4 exact | Trace class survives massless decompactification — `CONTRADICTS`; quadratic zero root has a regular intrinsic clock — `CONTRADICTS` | Explicit double-root and massless-box obstruction models; not a universal homogeneous-density no-go |
| `evidence:p24-action-benchmark-and-saddle` | 3 exact + 4 numerical | Connected real Starobinsky interval saddle exists — `SUPPORTS`; the saddle selects \(\phi_0\) or a SUSY-breaking scale — `CONTRADICTS` | One frozen real homogeneous benchmark with supplied `phi_center=1` and `T0=0.7`; no selection principle or full local-SUGRA state |
| `evidence:p24-constrained-mixed-hessian` | 1 exact + 6 numerical | Connected principal function has nonzero cross-boundary response — `SUPPORTS`; constraint-preserving mixed Hessian has rank one — `SUPPORTS`; the small mixed singular value is a physical mode — `CONTRADICTS` | Proper length is solved as a modulus under endpoint variations; fourth-order convergence removes the second singular direction, while the fixed-length mutant remains full rank |
| `evidence:p24-conditional-scalar-gaussian` | 2 exact + 2 numerical | Fixed-scale scalar subblock defines a conditional positive Gaussian — `SUPPORTS` | Both endpoint scale factors fixed, flat \(d\phi_-d\phi_+\) measure, pure two-real-mode reading only; not a physical WDW density or seam entropy |
| `evidence:p24-real-contour-obstruction` | 2 numerical | Real boundary Hessian defines a positive normalizable Gaussian precision — `CONTRADICTS` | Full real-boundary Hessian and the naive real-contour scalar Schur complement are indefinite; no thimble or bulk Morse spectrum was computed |
| `evidence:p25-action-lapse-and-jacobi` | 4 exact + 7 numerical | Frozen endpoints define a lapse saddle — `SUPPORTS`; real lapse is the exp(-W) descent — `CONTRADICTS` | Supplied Phase-24 boundaries and fixed-length homogeneous action; no global cycle or gauge-fixed determinant |
| `evidence:p25-real-branch-and-fold` | 4 numerical | Tracked real branch reaches a Dirichlet caustic — `SUPPORTS` | One bounded reflection-symmetric real continuation; not branch completeness or a second lapse saddle |
| `evidence:p25-local-complex-segment` | 1 exact + 1 numerical | Local constant-phase complex segment exists — `SUPPORTS` | Local branch only; no original-contour coefficient |
| `evidence:p26-bounded-complex-flow` | 2 exact + 6 numerical | Long constant-phase arm exists — `SUPPORTS` | One analytic sheet with a declared field-norm cutoff; endpoint and relative homology remain open |
| `evidence:p26-real-fold-airy` | 1 exact + 2 numerical | Real fold is a lapse saddle — `CONTRADICTS`; Airy scaling — `SUPPORTS` | The fixed-length fold has nonzero W_T and generic local uniform scaling |
| `evidence:p26-asymptotic-and-real-cycle` | 1 exact + 1 numerical | Positive real Euclidean sheet is the recorded convergent cycle — `CONTRADICTS` | Frozen plateau length is a separate exact control; no full Starobinsky asymptotic endpoint |
| `evidence:p27-wick-map` | 4 exact | Declared Lorentzian–Euclidean map is consistent — `SUPPORTS` | Explicit convention only; not a contour selection rule |
| `evidence:p27-raw-zero-lapse-kernel` | 3 exact + 6 numerical | Raw equal-boundary fixed-T kernel is finite at zero lapse — `CONTRADICTS` | Unreduced two-coordinate Van Vleck kernel only; the full BFV/FP kernel is distinct and uncomputed |
| `evidence:p27-operator-and-contour` | 5 exact | Positive half-line is a sourced resolvent — `SUPPORTS`; it is a WDW projector — `CONTRADICTS` | Spectral operator identities; no positive density or global PL coefficient |
| `evidence:p27-signed-raw-branch` | 1 exact + 2 numerical | Signed raw branch has paired stationary points — `SUPPORTS` | Frozen raw-W samples; not a prefactored heteroclinic |
| `evidence:p28-bounded-upper-arm` | 4 exact + 6 numerical | Upper arm continues past the imaginary-T turn — `SUPPORTS` | Bounded monitored segment; not a complete thimble |
| `evidence:p28-bounded-crossings` | 1 exact + 2 numerical | Four finite vertical cycles cross the recorded dual branch — `SUPPORTS` | Constructed bounded geometry; not a physical original-cycle intersection number |
| `evidence:p28-homogeneous-bfv` | 5 exact + 1 numerical | Intrinsic clock regularity — `CONTRADICTS`; extrinsic p_a clock — `SUPPORTS`; Dirichlet ghosts remove proper length — `CONTRADICTS`; local Gaussian factor — `SUPPORTS` conditionally | Euclidean-continued homogeneous Abelian BFV only; determinant 2 is scheme-normalized, not a physical prefactor |
| `evidence:p29-leading-fresnel-kernel` | 2 exact + 4 numerical | Frozen leading kernel has a `delta_flat` identity limit — `SUPPORTS`; equal-endpoint pointwise limit is finite — `CONTRADICTS` | Real-lapse leading quadratic control under declared local flat `da dphi`; not the physical WDW measure or all-orders kernel |
| `evidence:p29-reduced-bfv-modulus` | 6 exact + 1 numerical | Fixed-parameter BFV modulus factor is T-independent — `SUPPORTS`; unit ghost cancels the pointwise pole — `CONTRADICTS` | Reduced one-constraint fixed-parameter gauge only; no full endpoint or nonzero-mode determinant |
| `evidence:p29-lapse-operator-and-bypass` | 7 exact + 1 numerical | Inserted lapse power is harmless — `CONTRADICTS`; positive half lapse is a projector — `CONTRADICTS` | Spectral distributions and bounded finite-truncation arc; no global PL coefficient |
| `evidence:p29-conformal-sign-and-density` | 3 exact + 1 numerical | One imaginary rotation damps both signs — `CONTRADICTS`; identity distribution is trace-class density — `CONTRADICTS` | Frozen indefinite kinetic form and identity cutoff; no conformal thimble or physical trace |
| `evidence:p30-principal-cycle-and-maslov` | 5 exact + 1 numerical | Finite-cutoff local coupled field–lapse Gaussian cycle exists — `SUPPORTS`; one holomorphic lapse sheet normalizes both real sides — `CONTRADICTS` | Principal homogeneous rays and real-axis Fresnel/Maslov control; no continuum determinant-line gluing |
| `evidence:p30-fibered-schur-cycle` | 3 exact + 4 numerical | Finite-cutoff local coupled field–lapse Gaussian cycle exists — `SUPPORTS`; tested standard product rotation is sufficient — `CONTRADICTS` | Frozen midpoint Hessians and Schur-shifted tangent only; no nonlinear global relative cycle or full BFV super-Hessian |
| `evidence:p30-relative-determinant-and-prefactor` | 1 exact + 5 numerical | Declared midpoint relative magnitude has a recorded limit — `SUPPORTS`; bare absolute lattice sign is cutoff independent — `CONTRADICTS` | Declared time slicing and reference magnitude; not an absolute zeta determinant or continuum determinant-line phase |
| `evidence:p30-endpoint-ray-limit` | 1 exact | Pointwise shifted-ray limit fixes an integer PL coefficient — `CONTRADICTS` | Common open-ray limit away from singular `N=0`; no endpoint-completed upward cycle or transverse intersection |

## Phase 16 check ledger

### Bosonic derivation — 13 checks

- `P16.connection`
- `P16.connection_mixed`
- `P16.curvature_antisymmetry`
- `P16.CPN26_ab`
- `P16.CPN26_ba_mutation`
- `P16.raw_boundary`
- `P16.first_order_gravity`
- `P16.same_source_scalar`
- `P16.first_order_L`
- `P16.hessian`
- `P16.hessian_invariants`
- `P16.momenta`
- `P16.Hamiltonian`

Together these establish the source convention, reject the transposed curvature reading, remove one endpoint, and verify the exact `(-,+,+)` kinetic Hessian, momenta, and Hamiltonian.

### Strict tangency counterexample — 6 checks

- `P16.spin32_projector`
- `P16.spin32_candidate_kernel`
- `P16.clean_spinor_bilinear`
- `P16.off_shell_b_i_obstruction`
- `P16.spin32_obstruction`
- `P16.spin32_residual_trace`

The two independent normal witnesses are a nonzero `F ε¹ χ̄^{dot1}` coefficient `1/√2` in `δb₃` and a nonzero gamma-traceless spatial spin-3/2 residual for the declared clean monomial. A single exact point suffices to refute tangency of the whole declared locus; it is not a full transcription of every CPN variation.

### Rolling-clock slice — 1 check

- `P16.rolling_clock_no_residual_susy`

On the declared `W=0`, `F=0`, nonzero real proper-time-rate slice, the `δχ` parameter map has rank two, leaving only the zero Lorentzian-real parameter. The result concerns preserved background SUSY, not existence of the underlying gauge symmetry.

## Phase 17 check ledger

### Standard local fiber and support locality — 6 checks

- `P17.branch_reflection`
- `P17.branch_projectors`
- `P17.N1_CAR`
- `P17.N1_fermion_parity`
- `P17.local_standard_closure`
- `P17.local_same_half`

### Doubled-sheet algebra and nonselection — 11 checks

- `P17.fold_fixed_fiber_closure`
- `P17.fold_physical_parity`
- `P17.fold_bidirectional_exchange`
- `P17.half_sign_is_not_fermion_parity`
- `P17.unitary_mixing_family`
- `P17.mixing_not_selected`
- `P17.exchange_phase_family`
- `P17.local_fold_basis_equivalence`
- `P17.one_way_cross`
- `P17.one_way_closure_rejected`
- `P17.nonunitary_branch_mutation`

These establish a finite bidirectional unitary-flip witness while rejecting a one-way arrow, a nonunitary branch mutation, and any claim that closure alone selects the exchange basis.

### Literal reflection, translation, and positivity — 4 checks

- `P17.reflection_reverses_time_momentum`
- `P17.reflection_translation_obstruction`
- `P17.sharp_half_not_translation_invariant`
- `P17.signed_time_generator_not_positive_closure`

### Temporal seam, reality, and doubled projector — 9 checks

- `P17.real_temporal_seam_closure_obstruction`
- `P17.complexified_temporal_seam_control`
- `P17.geometric_reflection_linearity`
- `P17.physical_time_reversal_antilinearity`
- `P17.spatial_boundary_real_half`
- `P17.temporal_boundary_complex_half`
- `P17.temporal_boundary_no_real_half`
- `P17.doubled_real_temporal_projector`
- `P17.doubled_projector_mixes_sheets`

The positive control is a real rank-two spatial-boundary projector. The single-copy temporal projector preserves no nonzero real Majorana parameter. Adding a real two-sheet complex structure yields a rank-four real sheet-mixing projector, but only at finite projector level.

### Abstract Schwinger–Keldysh quartet — 4 checks

- `P17.SK_BRST_algebra`
- `P17.SK_BRST_parity`
- `P17.SK_difference_exact`
- `P17.SK_signed_contour_control_not_positive_H`

These verify nilpotence, mutual anticommutation, ghost oddness, and BRST exactness in the abstract quartet, while distinguishing its signed contour control from a positive physical-adjoint SUSY Hamiltonian.

## Phase 18 check ledger

### Conserved charge and free retarded poles — 18 exact checks

- `P18.time.conserved_charge`
- `P18.time.susy_state_stays_susy`
- `P18.domain.multiplet_marker`
- `P18.scalar.generator_square`
- `P18.scalar.evolution_equation`
- `P18.scalar.evolution_symplectic`
- `P18.scalar.general_seam_flux_identity`
- `P18.scalar.post_seam_evolution`
- `P18.scalar.characteristic_polynomial`
- `P18.fermion.hamiltonian_square`
- `P18.fermion.characteristic_polynomial`
- `P18.fermion.resolvent_factorization`
- `P18.fermion.evolution_equation`
- `P18.fermion.evolution_unitary`
- `P18.bulk.common_BF_shell`
- `P18.propagator.scalar_retarded_open_EOM`
- `P18.propagator.scalar_retarded_jump`
- `P18.propagator.scalar_retarded_seam_independence`

These checks separate time evolution from seam dynamics and prove the scoped free theorem. Conserved `[H,Q]=0` evolution keeps a `Q`-annihilated state in the kernel; an instantaneous Cauchy-data map changes amplitudes but not the unchanged future scalar or fermion generator. For the declared post-post retarded-pole definition, both characteristic denominators remain `p²-m²`, so `delta m_pole²=0`.

### Seam state and CPT-sheet controls — 17 exact checks

- `P18.seam.scalar_kick_symplectic`
- `P18.seam.scalar_kick_time_reversal_reciprocity`
- `P18.seam.scalar_mode_continuity`
- `P18.seam.scalar_mode_jump`
- `P18.seam.scalar_post_frequency`
- `P18.seam.scalar_bogoliubov_norm`
- `P18.prediction.scalar_occupation`
- `P18.seam.fermion_CAR`
- `P18.prediction.fermion_occupation`
- `P18.propagator.spectral_state_independence`
- `P18.propagator.statistical_state_dependence`
- `P18.propagator.image_bulk_equation`
- `P18.CPT.sheet_kernel`
- `P18.CPT.sheet_eigenchannels`
- `P18.CPT.real_sheet_diagonalization`
- `P18.CPT.doubled_kick_symplectic`
- `P18.prediction.sheet_occupation_sum_difference`

The explicit witnesses give scalar occupation `κ²/[4(k²+m²)]`, finite Nambu-pair fermion occupation `sin²θ`, and CPT-compatible scalar sheet eigenchannels. Unequal occupations can therefore define a non-SUSY state while the free spectral kernel remains state independent. The fermion construction is only a finite-mode CAR witness, not a local Weyl/Majorana Pin-seam action.

### UV and conditional controls — 12 exact checks plus 1 numerical control

- `P18.UV.number_density_primitive`
- `P18.UV.energy_density_primitive`
- `P18.UV.sharp_asymptotics`
- `P18.UV.gaussian_pulse_fourier`
- `P18.prediction.gaussian_Born_occupation`
- `P18.FRW.relativistic_dilution`
- `P18.FRW.nonrelativistic_dilution`
- `P18.soft.conditional_mass_ratio`
- `P18.soft.small_breaking_series`
- `P18.mutant.reject_noncanonical_scalar_seam`
- `P18.mutant.reject_nonunitary_fermion_seam`
- `P18.mutant.detect_inserted_bulk_soft_mass`

The sharp kick yields linear cutoff divergence in number density and leading energy density `κ²Λ²/(16π²)`, so it is not a finite-energy state. Gaussian smoothing, `a^-2`/`a^-3` collisionless dilution, and `sqrt(1+r²)` for an inserted persistent soft term are explicitly conditional controls, not predictions of an interacting seam theory.

The payload-only numerical control `P18.numeric.narrow_gaussian_delta_limit` used SciPy `solve_ivp` with DOP853 and passed with maximum absolute error `7.150719e-05` and Bogoliubov-normalization error `3.330669e-16`. It is recorded separately because the graph's evidence groups enumerate exact symbolic checks.

## Phase 19 check ledger

### Shift-symmetric exact reduction — 8 checks

- `P19.shift.canonical_inflaton_metric`
- `P19.shift.quadratic_potential`
- `P19.shift.orthogonal_inflaton_mass`
- `P19.shift.stabilizer_mass`
- `P19.shift.hubble_heavy_sufficient_benchmark`
- `P19.shift.gravitino_mass_on_path`
- `P19.shift.stabilizer_F_order_parameter`
- `P19.shift.susy_minkowski_endpoint`

These checks derive the quadratic path, distinguish \(H_V^2=V/3\) from geometric \(H(t)^2\), and verify the displayed stabilizer F direction vanishes at the fully checked minimal endpoint.

### Improved Cecotti exact reduction — 7 checks

- `P19.noscale.starobinsky_potential`
- `P19.noscale.canonical_log_modulus`
- `P19.noscale.stabilizer_hessian_mass`
- `P19.noscale.global_hessian_threshold`
- `P19.noscale.one_sixth_is_sufficient`
- `P19.noscale.gravitino_mass_on_path`
- `P19.noscale.nonzero_F_direction`

These checks derive the Starobinsky path, verify the degenerate path-local stabilizer Hessian, and show that \(\zeta>1/6\) is sufficient but not the sharp full-trajectory potential-Hessian threshold.

### Closed turning-point identities — 2 checks

- `P19.bounce.friedmann_constraint_at_turning_point`
- `P19.bounce.local_minimum_of_scale_factor`

The exact constraint fixes \(a_0\) only after \(\phi_0\) is supplied and gives a local scale-factor minimum. It does not select \(\phi_0\) or construct a CPT/Pin quantum state.

### Closed-background shooting — 24 checks

- `P19.quadratic_shift_symmetric.Nacc_50`
- `P19.quadratic_shift_symmetric.table_phi0_50`
- `P19.quadratic_shift_symmetric.table_a0_50`
- `P19.quadratic_shift_symmetric.friedmann_constraint_50`
- `P19.quadratic_shift_symmetric.Nacc_55`
- `P19.quadratic_shift_symmetric.table_phi0_55`
- `P19.quadratic_shift_symmetric.table_a0_55`
- `P19.quadratic_shift_symmetric.friedmann_constraint_55`
- `P19.quadratic_shift_symmetric.Nacc_60`
- `P19.quadratic_shift_symmetric.table_phi0_60`
- `P19.quadratic_shift_symmetric.table_a0_60`
- `P19.quadratic_shift_symmetric.friedmann_constraint_60`
- `P19.improved_cecotti_starobinsky.Nacc_50`
- `P19.improved_cecotti_starobinsky.table_phi0_50`
- `P19.improved_cecotti_starobinsky.table_a0_50`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_50`
- `P19.improved_cecotti_starobinsky.Nacc_55`
- `P19.improved_cecotti_starobinsky.table_phi0_55`
- `P19.improved_cecotti_starobinsky.table_a0_55`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_55`
- `P19.improved_cecotti_starobinsky.Nacc_60`
- `P19.improved_cecotti_starobinsky.table_phi0_60`
- `P19.improved_cecotti_starobinsky.table_a0_60`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_60`

The 24 numerical checks cover two potentials, three target values \(N_{\rm acc}=50,55,60\), and four checks per row: target count, displayed \(\phi_0\), displayed radius, and Friedmann residual.

### First-order tensor comparison — 6 checks

- `P19.slowroll.quadratic_r_exceeds_current_N50`
- `P19.slowroll.starobinsky_r_below_current_N50`
- `P19.slowroll.quadratic_r_exceeds_current_N55`
- `P19.slowroll.starobinsky_r_below_current_N55`
- `P19.slowroll.quadratic_r_exceeds_current_N60`
- `P19.slowroll.starobinsky_r_below_current_N60`

These six checks compare only first-order potential slow-roll \(r\) values with the cited tensor limits. They do not perform a closed-bounce perturbation calculation, reheating map, or full \(n_s,r\) likelihood analysis.

## Phase 20 check ledger

### Leading de Sitter/WDW envelope — 12 exact plus 6 numerical checks

- `P20.WDW.hemisphere_action_normalization`
- `P20.WDW.action_derivative`
- `P20.WDW.standard_history_weight_slope`
- `P20.WDW.independent_pair_weight_slope`
- `P20.WDW.pair_slope_factor_two`
- `P20.WDW.no_finite_stationary_envelope`
- `P20.WDW.asymptotic_zero_slope_only`
- `P20.WDW.conjugate_saddle_interference`
- `P20.WDW.independent_pair_joint_probability`
- `P20.WDW.constant_symmetrization_does_not_move_slope`
- `P20.WDW.starobinsky_epsilon`
- `P20.WDW.constant_field_is_not_exact_saddle`
- `P20.numeric.standard_slope_coefficient`
- `P20.numeric.pair_slope_coefficient`
- `P20.numeric.standard_central_difference`
- `P20.numeric.pair_central_difference`
- `P20.numeric.HH_and_tunneling_opposite_monotonicity`
- `P20.numeric.slow_roll_not_constant_field`

The standard history probability is proportional to \(e^{2sI}\). The doubled-slope \(e^{4sI}\) expression is checked only as the joint probability of an independently factorized pair; it is not derived from CPT sewing. Both leading envelopes are monotone at the Phase 19 benchmark. The same group verifies the order-one coherent \(\cos^2S\) identity and that the benchmark has small but nonzero \(\epsilon_V\), so the calculation is not promoted to an exact Starobinsky WDW saddle or no-go theorem.

### Cecotti auxiliary direction — 5 exact plus 2 numerical checks

- `P20.SUSY.cecotti_DSW`
- `P20.SUSY.cecotti_inverse_metric`
- `P20.SUSY.cecotti_auxiliary`
- `P20.SUSY.cecotti_potential`
- `P20.SUSY.static_F_flat_point`
- `P20.numeric.T_star`
- `P20.numeric.nonzero_F_star`

These checks give \(T_*=85.1288467\ldots\) and \(F^S/M=-6.4475031\ldots\), contradicting classical F-flatness at \(\varphi_*=5.442969458\). They do not solve the coupled quantum local-SUSY constraints or exclude wavefunction support there.

### Conditional curvature–reheating bridge — 1 exact plus 6 numerical checks

- `P20.curvature.matterlike_temperature_exponent`
- `P20.numeric.phase19_Nacc_bridge`
- `P20.numeric.phase19_rho_end_bridge`
- `P20.numeric.phase19_constraint_bridge`
- `P20.numeric.curvature_reheating_coefficient`
- `P20.numeric.curvature_reheating_inverse`
- `P20.numeric.closed_curvature_sign`

The bridge independently recovers the Phase 19 60-e-fold endpoint and, for the frozen inputs, obtains \(\Omega_{K0}=-5.5258\times10^{-4}(T_{\rm reh}/10^9\,{\rm GeV})^{2/3}\). The sign, branch choice, reheating equation of state, temperature, entropy factors, units, and late-time constants are all explicit inputs. This is a reproducible conversion, not a curvature detection or seam prediction.

## Phase 21 check ledger

### Single-mode normalized Gaussian — 12 exact checks

- `P21.gaussian.kernel_determinant`
- `P21.gaussian.schur_factorization`
- `P21.gaussian.inverse_covariance`
- `P21.gaussian.normalized_ratio`
- `P21.gaussian.no_seam_baseline`
- `P21.gaussian.nonempty_bridge_series`
- `P21.gaussian.connected_log_series`
- `P21.gaussian.remainder_is_exponential_of_connected`
- `P21.gaussian.order_four_disconnected_piece`
- `P21.gaussian.source_derivative_correlation`
- `P21.gaussian.ratio_even_correlation_odd`
- `P21.gaussian.symmetric_normal_modes`

These checks establish \(R(0)=1\), the conditional identity for a chosen zero-insertion exclusion,
and the distinction \(R-1=\exp(\log R)-1\). They do not define an exclusive event or Born
probability.

### Multimode determinant — 4 exact checks

- `P21.multimode.schur_determinant`
- `P21.multimode.determinant_ratio`
- `P21.multimode.connected_trace_expansion`
- `P21.multimode.positivity_singular_value_gate`

The finite block result is \(R=\det(I-K^TK)^{-1/2}\), with
\(\log R=\tfrac12\sum_{j\ge1}{\rm Tr}[(K^TK)^j]/j\). Infinite-mode UV control and any
fermionic/Pfaffian phase remain outside this group.

### Flux tails, finite parts, and imposed priors — 11 exact plus 7 numerical checks

- `P21.flux.absolute_coupling_remainder_tail`
- `P21.flux.absolute_coupling_log_tail`
- `P21.flux.sector_partition_difference_tail`
- `P21.flux.relative_coupling_constant_tail`
- `P21.flux.normalized_ratio_lattice_dimension_threshold`
- `P21.flux.sector_difference_lattice_dimension_threshold`
- `P21.flux.relative_sector_difference_dimension_threshold`
- `P21.flux.WDW_HH_excess_tail`
- `P21.flux.WDW_tunneling_deficit_tail`
- `P21.flux.WDW_reference_lattice_dimension_threshold`
- `P21.regularization.constant_tail_finite_part`
- `P21.numeric.absolute_coupling_sum`
- `P21.numeric.connected_generator_sum`
- `P21.numeric.truncation_convergence`
- `P21.numeric.flat_remainder_zero_sector_peak`
- `P21.numeric.sector_partition_difference_sum`
- `P21.numeric.sector_partition_prior_dependence`
- `P21.numeric.relative_coupling_linear_divergence`

The recorded one-flux constant-absolute toy is summable. Its flat-sector \(R_n-1\) weighting has
\(p_0=0.484950\ldots\), while retaining \(Z_n(0)\) gives \(0.626161\ldots\). This is a
prior-dependence witness, not an inflationary flux prediction. The lattice thresholds are stated
weight by weight: \(d<4\) for the \(n^{-4}\) normalized-ratio tails, \(d<6\) for the
\(n^{-6}\) absolute sector difference, and \(d<2\) for the \(n^{-2}\) reference or
relative-coupling sector-difference tails.

## Phase 22 check ledger

### Fixed-energy SUSY and finite density — 16 exact checks

- `P22.susy.charge_nilpotent`
- `P22.susy.adjoint_nilpotent`
- `P22.susy.positive_closure`
- `P22.susy.energy_conservation`
- `P22.susy.fermion_oddness`
- `P22.density.boson_geometric_norm`
- `P22.density.fermion_pair_norm`
- `P22.density.pure_projector_hermitian`
- `P22.density.pure_projector_trace_one`
- `P22.density.pure_projector_idempotent_rank_one`
- `P22.density.partial_trace`
- `P22.density.reduced_trace`
- `P22.density.full_reduced_positivity`
- `P22.density.gibbs_partition`
- `P22.density.supermultiplet_equal_weights`
- `P22.density.finite_temperature_not_zero_energy`

These checks establish a normalized positive purification and a positive reduced Gibbs density for
\(0<r=e^{-\beta\omega}<1\). The density commutes with the fixed-mode charges because both members of
each positive-energy supermultiplet have equal weight. The positive energy at finite \(\beta\) is a
separate exact guard against calling this an unbroken thermal vacuum.

### Graded anti-linear real structure — 5 exact checks

- `P22.theta.involution_square`
- `P22.theta.state_invariance`
- `P22.theta.parity_compatibility`
- `P22.theta.energy_compatibility`
- `P22.theta.ungraded_swap_mutant_rejected`

The displayed phase and graded swap define an exact occupation-space toy involution. They do not
construct a 4D Clifford reflection, spin structure, reflection square, or local-SUGRA Pin gluing law.

### Euclidean bridge and SK trace — 6 exact checks

- `P22.bridge.local_covariance`
- `P22.bridge.cross_covariance`
- `P22.bridge.normalized_coefficient`
- `P22.bridge.amplitude_density_factor_two`
- `P22.SK.equal_source_unitarity`
- `P22.SK.wrong_adjoint_mutant_rejected`

The density covariance is \((2K_{\rm DtN})^{-1}\), while \(K_{\rm DtN}\) is the amplitude Hessian.
The SK check is the exact unitary identity \({\rm Tr}(U\rho U^\dagger)=1\); it is not a constructed
ghost quartet or BRST cohomology.

### Noncompact free zero-mode obstruction — 4 exact checks

- `P22.zero_mode.boson_partition_diverges`
- `P22.zero_mode.fermion_partition_finite`
- `P22.zero_mode.coordinate_variance_diverges`
- `P22.zero_mode.diagonal_stiffness_vanishes`

The payload records `P22.guard.free_noncompact_zero_mode_trace_class` with
`EXPECTED_OBSTRUCTION_CONFIRMED`. It is bounded to the unregulated noncompact free oscillator; a compact
mode or the interacting constrained \((a,\phi)\) sector requires a separate physical measure and
zero-mode treatment.

## Phase 23 check ledger

### Full-lapse rigging and seed calibration — 10 exact plus 1 numerical check

- `P23.rigging.full_real_lapse_abel_kernel`
- `P23.rigging.abel_delta_normalization`
- `P23.rigging.full_real_lapse_gaussian_kernel`
- `P23.rigging.kinematical_gaussian_norm`
- `P23.rigging.regulated_seed_norm`
- `P23.rigging.normalized_shell_profile`
- `P23.rigging.not_a_bounded_kinematical_projector`
- `P23.rigging.half_lapse_is_resolvent`
- `P23.rigging.half_lapse_is_not_projector_kernel`
- `P23.rigging.naive_euclidean_lapse_mutant_diverges`
- `P23.numeric.regulated_seed_norm`

The full real lapse gives normalized Abel and Gaussian delta sequences for one constraint. The Gaussian
seed is normalized before rigging and reduces to its chosen normalized shell profile after division by
the square root of the rigging norm. This continuous spectral calibration is distributional: the kernel
supremum diverges, the positive half-lapse transform is a resolvent, and a naive Euclidean exponential
diverges on the negative spectrum. It is separate from the compact density calibration below.

### Shell, branch, and current control — 10 exact plus 1 numerical check

- `P23.constraint.dirichlet_spectrum`
- `P23.constraint.frequency_roots`
- `P23.constraint.delta_shell_jacobian`
- `P23.constraint.clock_gauge_FP_cancellation`
- `P23.WDW.frequency_modes_solve_constraint`
- `P23.current.integrated_frequency_signs`
- `P23.current.induced_sum_vs_signed_difference`
- `P23.current.two_mode_continuity`
- `P23.current.integrated_density_equals_trace`
- `P23.current.local_density_not_pointwise_positive`
- `P23.numeric.current_slice_conservation`

For the compact Dirichlet normal form, the two simple roots have opposite integrated Klein–Gordon signs.
Choosing the \(T\)-clock and one frequency orientation supplies a positive integrated norm; the quadratic
constraint alone does not. An equal-weight relative-phase family has unit induced norm and zero signed
current, with orthogonal real witnesses, so zero current does not select a unique state. Separately, the
positive-frequency two-mode state has conserved unit integrated current but the exact local value
\(-55/(768\pi)\), so the local current is not a pointwise Born probability.

### Supplied compact bridge and density — 8 exact plus 2 numerical checks

- `P23.density.spectral_comparison_gap`
- `P23.density.trace_class_geometric_bound`
- `P23.density.truncated_purification`
- `P23.density.partial_trace_positive`
- `P23.density.spectral_stationarity`
- `P23.density.bridge_weight_ratio`
- `P23.theta.toy_pairing`
- `P23.selection.preparation_length_remains_input`
- `P23.numeric.trace_sum_convergence`
- `P23.numeric.two_mode_density_spectrum`

With supplied \(L>0\), \(B_L=e^{-L\sqrt h}\), and two outward-positive constrained copies, comparison
with a geometric series proves the infinite compact spectral sum is trace class. The finite matrix checks
verify purification, reduction, positivity, and the toy anti-linear pairing; the numerical sum gives
\(Z_L=0.072625937359366\) at \(\mu=L=1\). Neither group averaging nor CPT-like pairing derives \(L\),
the compact regulator, or the relative weights.

### Zero root and decompactification — 4 exact checks

- `P23.zero_root.quadratic_root_divergence`
- `P23.zero_root.clock_FP_vanishes`
- `P23.zero_root.linear_constraint_control`
- `P23.regulator.decompactification_not_trace_class`

At the quadratic \(E=0\) root, the regulated shell integral diverges as \(1/\sqrt{2\epsilon}\) and the
intrinsic-clock determinant vanishes. A linear constraint removes that double root only by choosing an
orientation. In the separate massless box, \(Z_R\sim R/(2L)\), so the compact trace-class result has no
trace-class decompactification limit in this control. These witnesses do not prove that the Starobinsky
homogeneous mode is gauge or rule out compact/interacting constrained models.

## Phase 24 check ledger

### Frozen action, supplied benchmark, and connected saddle — 3 exact plus 4 numerical checks

- `P24.action.starobinsky_derivative`
- `P24.action.canonical_momenta`
- `P24.action.off_shell_scale_equation`
- `P24.saddle.midpoint_constraint`
- `P24.saddle.connected_boundary_values`
- `P24.saddle.on_shell_action`
- `P24.saddle.bvp_and_constraint_residuals`

These checks freeze the reduced Euclidean action, distinguish its full off-shell scale equation from the constraint-reduced equation, and reproduce one connected `S3 x I` saddle. The values `phi_center=1` and base proper length `T0=0.7` are supplied calibrations; the result does not select either input or a SUSY-breaking scale.

### Constraint-preserving mixed Hamilton principal Hessian — 1 exact plus 6 numerical checks

- `P24.hessian.mixed_block_bilinear_transform`
- `P24.hessian.fourth_order_rank_convergence`
- `P24.hessian.symmetry`
- `P24.hessian.HJ_constraint_null_vectors`
- `P24.hessian.constraint_reduced_rank_one`
- `P24.hessian.fixed_length_mutant_full_rank`
- `P24.factorization.connected_response_nonzero`

The connected principal function has a nonzero mixed boundary response. With proper length solved as a modulus, the Hamilton–Jacobi constraint gives left and right null directions and the mixed block has one surviving direction. The small-to-large singular ratio converges away at fourth order; holding `T=0.7` fixed off shell instead leaves a full-rank mixed block. Rank is invariant under separate invertible endpoint configuration-coordinate changes, but the singular values are not, and no change of polarization or clock is covered.

### Conditional fixed-scale scalar Gaussian — 2 exact plus 2 numerical checks

- `P24.gaussian.schmidt_relation`
- `P24.gaussian.precision_covariance_sign`
- `P24.gaussian.fixed_scale_scalar_positive`
- `P24.gaussian.conditional_parameters`

After fixing both endpoint scale factors, the scalar precision block is positive and gives precision coupling `0.256319454`, position correlation `-0.256319454`, Schmidt magnitude `0.130336866`, and conditional entropy `0.087559403` nats. These are flat-measure two-real-mode diagnostics, not a physical WDW density, a Choi construction, or gravitational seam entanglement.

### Full real-contour obstruction — 2 numerical checks

- `P24.contour.full_boundary_hessian_indefinite`
- `P24.contour.real_scale_integration_not_positive`

The full boundary Hessian has two negative directions, and naively integrating the scale factors on the real contour leaves an indefinite scalar Schur complement. These boundary signs do not determine the bulk Dirichlet Morse spectrum; a lapse/conformal thimble, gauge-fixed primed bulk operator, ghosts, physical boundary measure, and trace-class test remain open.

## Phase 25 check ledger

### Action, lapse saddle, and Jacobi response — 4 exact plus 7 numerical checks

- `P25.action.full_off_shell_scale_equation`
- `P25.action.energy_constraint_identity`
- `P25.action.HJ_time_derivative_sign`
- `P25.jacobi.starobinsky_second_derivative`
- `P25.saddle.base_stationarity`
- `P25.action.time_derivative_control`
- `P25.saddle.negative_lapse_curvature`
- `P25.saddle.real_direction_is_not_descent`
- `P25.saddle.lapse_Schur_recovers_constrained_Hessian`
- `P25.jacobi.base_velocity_monodromy`
- `P25.jacobi.momentum_block_and_mixed_hessian`

The supplied Phase-24 endpoints give a stationary fixed-boundary lapse saddle at `T=0.7` with `W_TT=-8.9231430383`. The negative curvature makes the imaginary tangent locally convergent for `exp(-W)`; it does not determine the global integration cycle.

### Tracked real branch and simple fold — 4 numerical checks

- `P25.branch.tracked_real_continuation`
- `P25.caustic.symmetric_fold`
- `P25.caustic.simple_fold_transversality`
- `P25.caustic.two_branch_sign_bracket`

### Local complex continuation — 1 exact plus 1 numerical check

- `P25.thimble.local_steepest_direction`
- `P25.thimble.local_constant_phase_segment`

The real Dirichlet fold and local complex segment are two different diagnostics. Neither is a proof of a complete saddle census, relative-homology class, or intersection coefficient.

## Phase 26 check ledger

### Bounded complex arm — 2 exact plus 6 numerical checks

- `P26.flow.exp_minus_W_sign`
- `P26.saddle.local_tangents`
- `P26.saddle.base`
- `P26.flow.constant_phase_and_monotone_ReW`
- `P26.flow.gradient_alignment`
- `P26.flow.projection_turn`
- `P26.flow.field_norm_stop`
- `P26.flow.conjugate_lower_arm`

### Real fold — 1 exact plus 2 numerical checks

- `P26.fold.Airy_three_halves_law`
- `P26.fold.not_a_lapse_saddle`
- `P26.fold.Airy_scaling`

### Plateau and real-sheet controls — 1 exact plus 1 numerical check

- `P26.asymptotic.plateau_projected_length`
- `P26.contour.positive_real_not_recorded_decay_cycle`

The long arm is bounded by an explicit field-norm cutoff, and the exact `4π/3` projected length belongs only to the frozen plateau control. The positive real tracked sheet is not the recorded convergent cycle, but this does not determine another sheet or the Lorentzian original contour.

## Phase 27 check ledger

### Declared Wick map — 4 exact checks

- `P27.action.lapse_Wick_map`
- `P27.action.exponent_Wick_map`
- `P27.action.principal_derivative_map`
- `P27.action.canonical_constraint_Wick_map`

### Raw zero-lapse kernel — 3 exact plus 6 numerical checks

- `P27.short_time.equal_boundary_action`
- `P27.short_time.Jacobi_Van_Vleck_map`
- `P27.short_time.conformal_determinant_sign`
- `P27.short_time.action_linear_cubic_convergence`
- `P27.short_time.initial_velocity_convergence`
- `P27.short_time.velocity_Jacobi_scaling`
- `P27.short_time.momentum_Van_Vleck_scaling`
- `P27.endpoint.raw_W_zero_derivative_nonzero`
- `P27.benchmark.Phase24_25_endpoint`

The `1/|T|` magnitude is the raw two-coordinate fixed-T Van Vleck behavior. It is deliberately not identified with a zero-lapse-uniform, endpoint-completed, gauge-reduced BFV/FP kernel.

### Spectral operator and lateral-contour identities — 5 exact checks

- `P27.operator.fixed_lapse_constraint_evolution`
- `P27.operator.positive_half_line_resolvent`
- `P27.operator.full_line_constraint_support`
- `P27.contour.lateral_Wick_side`
- `P27.flow.exp_minus_W_monotonicity`

### Signed raw branch — 1 exact plus 2 numerical checks

- `P27.action.signed_classical_oddness`
- `P27.signed_branch.paired_stationary_actions`
- `P27.signed_branch.sampled_raw_W_control`

The paired raw stationary points and lateral sides do not fix a global Stokes matrix or physical half-line coefficient.

## Phase 28 check ledger

### Bounded upper arm — 4 exact plus 6 numerical checks

- `P28.PL.downward_flow_identity`
- `P28.PL.upward_flow_identity`
- `P28.PL.negative_mode_tangents`
- `P28.PL.Schwarz_reflection`
- `P28.downward.pseudo_arclength_residual`
- `P28.downward.gradient_alignment`
- `P28.downward.imaginary_projection_turn`
- `P28.downward.independent_fixed_imaginary_control`
- `P28.downward.conjugate_arm`
- `P28.downward.jacobi_and_scale_monitor`

### Constructed bounded crossings — 1 exact plus 2 numerical checks

- `P28.intersection.transverse_orientation`
- `P28.upward.real_branch_control`
- `P28.intersection.bounded_vertical_crossings`

The four crossings use declared finite vertical cycles and one recorded dual branch. Their local orientation and magnitude are not a global intersection number for a physical original contour.

### Euclidean-continued homogeneous BFV — 5 exact plus 1 numerical check

- `P28.BFV.neck_clock_Faddeev_Popov_brackets`
- `P28.BFV.abelian_constraint_algebra`
- `P28.BFV.Dirichlet_ghost_determinant`
- `P28.BFV.proper_length_BRST_invariance_after_auxiliary_elimination`
- `P28.BFV.local_lapse_Gaussian`
- `P28.saddle.curvature_and_local_prefactor`

At the neck, the intrinsic `a` and `phi` clocks are singular while `p_a` is locally regular. The unit-interval Dirichlet ghost operator has no zero mode and a chosen zeta-normalized determinant of `2`, but `sT=c(1)-c(0)=0`; proper length therefore survives in this reduced model. The local factor `i*0.8391333983*sqrt(hbar)` is conditional on the still-unknown global coefficient and full superdeterminant.

## Phase 29 check ledger

### Leading real-lapse Fresnel kernel — 2 exact plus 4 numerical checks

- `P29.kernel.distributional_identity_limit`
- `P29.kernel.Fourier_multiplier_identity_limit`
- `P29.numeric.frozen_metric`
- `P29.numeric.raw_and_normalized_prefactors`
- `P29.numeric.distributional_pairing_convergence`
- `P29.numeric.pointwise_pole`

The normalized frozen leading kernel tends to the identity delta distribution on the tested Schwartz/Gaussian functions under the declared local flat `da dphi` endpoint measure. Its equal-endpoint value still diverges as `1/N`. Distributional identity and pointwise finiteness are therefore not interchangeable.

### Reduced fixed-parameter BFV modulus — 6 exact plus 1 numerical check

- `P29.BFV.Dirichlet_ghost_length_scaling`
- `P29.BFV.fixed_parameter_ghost_is_modulus_independent`
- `P29.BFV.gauge_condition_rescaling_cancels`
- `P29.BFV.proper_time_modulus_is_gauge_invariant`
- `P29.BFV.nonzero_mode_factor_is_modulus_independent`
- `P29.BFV.unit_ghost_does_not_cancel_endpoint_pole`
- `P29.numeric.ghost_coordinate_length_dependence`

The standalone coordinate-interval determinant scales as `2L`, but the fixed-parameter rescaling and matching gauge-condition delta leave a T-independent reduced nonzero-mode factor. Proper time remains a modulus. This is not a derivation of the physical WDW endpoint measure.

### Lapse operators and endpoint bypass — 7 exact plus 1 numerical check

- `P29.endpoint.pointwise_vs_distributional_integrability`
- `P29.operator.half_line_is_sourced_resolvent`
- `P29.operator.ad_hoc_lapse_power_changes_resolvent`
- `P29.operator.full_line_constraint_support`
- `P29.operator.weighted_full_line_loses_constraint_annihilation`
- `P29.endpoint.lateral_bypass_Bessel_residues`
- `P29.endpoint.finite_spectral_arc_control`
- `P29.numeric.half_line_resolvent_residual`

An inserted `N` changes the half-line pole and full-line constraint distribution. Finite bounded spectral truncations have a vanishing small arc, but the off-diagonal lateral residue and full unbounded/global coefficient are not fixed.

### Conformal sign and density obstruction — 3 exact plus 1 numerical check

- `P29.kernel.indefinite_signature`
- `P29.kernel.single_Wick_rotation_obstruction`
- `P29.density.identity_not_Hilbert_Schmidt`
- `P29.numeric.identity_HS_divergence`

The frozen kinetic matrix has one negative and one positive direction, so one imaginary-lapse sign cannot damp both. The identity kernel's Hilbert–Schmidt norm grows with cutoff dimension. Thus neither the conformal contour nor a trace-class physical density follows from the leading real-lapse identity limit.

## Phase 30 check ledger

### Principal coupled rays and Maslov line — 5 exact plus 1 numerical check

- `P30.contour.coupled_principal_rays`
- `P30.contour.local_holomorphic_normalization`
- `P30.contour.Euclidean_conformal_ray`
- `P30.Maslov.real_side_phase_cancellation`
- `P30.Maslov.single_holomorphic_sheet_left_sign`
- `P30.contour.complex_principal_normalization`

The lapse-dependent gravity/scalar rays normalize the finite homogeneous principal Gaussian at the tested complex angles, including the Euclidean conformal ray. On the real axis the two Fresnel phases require the positive identity normalization `1/|N|`; a single holomorphic `1/N` sheet therefore has the wrong sign for negative real lapse. This diagnoses missing Maslov/determinant-line gluing rather than constructing it.

### Fibered field–lapse Schur cycle — 3 exact plus 4 numerical checks

- `P30.schur.field_lapse_completion`
- `P30.contour.fibered_completion_identity`
- `P30.lapse.Wick_and_thimble_jacobians`
- `P30.saddle.frozen_stationary_control`
- `P30.schur.discrete_bulk_lapse_convergence`
- `P30.contour.direct_product_fails`
- `P30.contour.fibered_cycle_passes`

The discrete Schur complement converges to the recorded negative lapse curvature. The tested independent field and lapse rotations retain one negative direction, whereas the field-dependent lapse shift removes the mixed block and makes the real part positive at every tested finite cutoff. This is a local tangent cycle for the frozen homogeneous quadratic control, not a global nonlinear Picard–Lefschetz cycle and not a full BFV calculation.

### Relative determinant magnitude and conditional prefactor — 1 exact plus 5 numerical checks

- `P30.determinant.declared_midpoint_measure_power`
- `P30.Jacobi.momentum_endpoint_identity`
- `P30.Jacobi.sampled_no_caustic_to_saddle`
- `P30.determinant.declared_midpoint_measure_convergence`
- `P30.determinant.cutoff_parity_phase_obstruction`
- `P30.prefactor.conditional_local_magnitude`

The declared midpoint configuration measure makes the recorded relative endpoint magnitude converge to `1.01502655703`, consistent with the endpoint Jacobi/Van Vleck control. The naked Hessian ratio grows strongly, and the absolute field-determinant sign alternates between odd and even cutoffs. The reference cancels that finite-lattice sign only in the relative ratio; no absolute zeta determinant or continuum determinant-line phase follows.

### Shifted endpoint rays — 1 exact check

- `P30.PL.shifted_rays_share_pointwise_open_limit`

Left- and right-shifted positive-imaginary rays have the same pointwise limit away from the singular endpoint. That equality does not create a transverse intersection at `N=0`, complete the upward dual cycle, or determine an integer PL coefficient.

Phase 30 evaluates no new BFV ghost complex and no full phase-space BFV super-Hessian. Those objects, their primed superdeterminant, the determinant line through `N=0`, and regulator/mode-cutoff limits remain open.

## Reproduction commands

The commands recorded in the snapshots are:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
uv run --locked python3 cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py
uv run --locked python3 cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py
uv run --locked python3 cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py
uv run --locked python3 cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py
uv run --locked python3 cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py
uv run --locked python3 cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py
uv run --locked python3 cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py
uv run --locked python3 cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py
uv run --locked python3 cpt_temporal_folded_susy/phase25_connected_lapse_scan.py
uv run --locked python3 cpt_temporal_folded_susy/phase26_global_lapse_flow.py
uv run --locked python3 cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py
uv run --locked python3 cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py
uv run --locked python3 cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py
uv run --locked python3 cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py
```

To audit an observed result, compare the current executable hash with the snapshot's `script.sha256`, rerun the exact recorded command, and compare check IDs, statuses, statements, payload, exit code, and scope guard. A successful rerun increases reproducibility; it still does not constitute independent peer review or extend the declared scope.

## Two complete traces

Supported trace:

```text
claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p17-doubled
  → DEFINED_IN → artifact:p17-script
  → RECORDED_IN → artifact:p17-evidence-snapshot
  → VALID_WITHIN → scope:p17-fundamental-doubled-sheet
  → VALID_WITHIN → scope:p17-fixed-positive-energy-fiber
  → BLOCKED_BY → action/domain/charge/compatibility/anchor open nodes
```

Contradicted trace:

```text
claim:P16_SPECIFIED_OFF_SHELL_FLRW_GAMMA_TRACE_TANGENCY
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p16-tangency
  → DERIVED_FROM → source:bgg-hep-th-0005225v1
  → DEFINED_IN → artifact:p16-script
  → RECORDED_IN → artifact:p16-evidence-snapshot
  → VALID_WITHIN → scope:p16-strict-flrw-tangency
```

Phase 18's central polarity pair is:

```text
claim:P18_FREE_CANONICAL_SEAM_GENERATES_POLE_SPLITTING
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p18-charge-and-poles
  → DEFINED_IN → artifact:p18-script
  → RECORDED_IN → artifact:p18-evidence-snapshot
  → VALID_WITHIN → scope:p18-free-instantaneous-seam

claim:P18_FREE_SEAM_CAN_PREPARE_NONSUSY_STATE
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p18-state-and-cpt
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p18-charge-and-poles
  └─ VALID_WITHIN → scope:p18-free-instantaneous-seam
```

Phase 20's central bounded trace is:

```text
claim:P20_LEADING_DE_SITTER_WDW_ENVELOPE_SELECTS_5P44
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p20-leading-wdw-envelope
  → DEFINED_IN → artifact:p20-script
  → RECORDED_IN → artifact:p20-evidence-snapshot
  → VALID_WITHIN → scope:p20-leading-de-sitter-wdw-control
  → MOTIVATES → open:p20-exact-starobinsky-wdw-state
```

The scope edge is essential: the trace concerns the leading constant-field envelope, not an exact two-sheet local-SUGRA WDW no-go.

Phase 21's central distinction is:

```text
claim:P21_R_MINUS_ONE_IS_CONNECTED_VACUUM_FUNCTIONAL
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p21-single-mode-gaussian
  → DEFINED_IN → artifact:p21-script
  → RECORDED_IN → artifact:p21-evidence-snapshot
  → VALID_WITHIN → scope:p21-positive-euclidean-gaussian

claim:P21_LOG_R_IS_CONNECTED_VACUUM_GENERATOR
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p21-single-mode-gaussian
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p21-multimode-gaussian
  └─ VALID_WITHIN → scope:p21-positive-euclidean-gaussian
```

Neither trace supplies the separate physical flux-sector measure represented by
`open:p21-physical-flux-measure`.

Phase 22's positive and obstructed traces are:

```text
claim:P22_POSITIVE_FREQUENCY_TFD_LIKE_DENSITY_IS_NORMALIZED_AND_POSITIVE
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p22-susy-and-density
  → DEFINED_IN → artifact:p22-script
  → RECORDED_IN → artifact:p22-evidence-snapshot
  → VALID_WITHIN → scope:p22-positive-frequency-finite-mode-density

claim:P22_FREE_NONCOMPACT_ZERO_MODE_HAS_TRACE_CLASS_TFD_LIMIT
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p22-zero-mode-obstruction
  → DEFINED_IN → artifact:p22-script
  → RECORDED_IN → artifact:p22-evidence-snapshot
  → VALID_WITHIN → scope:p22-noncompact-zero-mode-limit
  → MOTIVATES → open:p22-homogeneous-minisuperspace-density
```

Phase 23's supplied positive density and selection obstruction are:

```text
claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p23-trace-class-density
  → DEFINED_IN → artifact:p23-script
  → RECORDED_IN → artifact:p23-evidence-snapshot
  → VALID_WITHIN → scope:p23-supplied-bridge-compact-density
  → MOTIVATES → open:p23-cap-derived-regulator-independent-density

claim:P23_CPT_REALITY_AND_ZERO_SIGNED_CURRENT_UNIQUELY_SELECT_A_DENSITY
  ├─ HAS_EVIDENCE {polarity: CONTRADICTS} → evidence:p23-shell-and-current
  ├─ HAS_EVIDENCE {polarity: CONTRADICTS} → evidence:p23-trace-class-density
  └─ VALID_WITHIN → scope:p23-supplied-bridge-compact-density
```

The first trace proves only a supplied compact regulated density. The full-lapse rigging map does not
derive \(B_L\), and neither trace is a cap-derived cosmological Born measure or local-SUGRA/BRST state.

Phase 24's conditional positive subblock and full-contour obstruction are:

```text
claim:P24_FIXED_SCALE_SCALAR_SUBBLOCK_DEFINES_A_CONDITIONAL_POSITIVE_GAUSSIAN
  ├─ HAS_EVIDENCE {polarity: SUPPORTS}
  │  → evidence:p24-conditional-scalar-gaussian
  │  ├─ DEFINED_IN → artifact:p24-script
  │  └─ RECORDED_IN → artifact:p24-evidence-snapshot
  ├─ DOCUMENTED_BY → artifact:p24-report
  └─ VALID_WITHIN → scope:p24-fixed-scale-flat-measure-scalar-gaussian

claim:P24_REAL_BOUNDARY_HESSIAN_DEFINES_A_POSITIVE_NORMALIZABLE_GAUSSIAN_PRECISION
  ├─ HAS_EVIDENCE {polarity: CONTRADICTS}
  │  → evidence:p24-real-contour-obstruction
  │  ├─ DEFINED_IN → artifact:p24-script
  │  └─ RECORDED_IN → artifact:p24-evidence-snapshot
  ├─ DOCUMENTED_BY → artifact:p24-report
  ├─ VALID_WITHIN → scope:p24-real-boundary-contour-diagnostic
  ├─ MOTIVATES → open:p24-gravitational-thimble-and-bulk-determinant
  └─ MOTIVATES → open:p24-physical-two-boundary-density-and-entropy
```

The first trace fixes both scale factors and assumes a flat scalar measure. The second is a real-boundary diagnostic, not a thimble computation or a bulk negative-mode census. Neither trace promotes the connected interval to a positive gravitational density or physical entropy.

Phase 27 and 28 keep the raw endpoint and reduced BFV diagnostics separate:

```text
claim:P27_EQUAL_BOUNDARY_RAW_FIXED_T_KERNEL_IS_FINITE_AT_ZERO_LAPSE
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p27-raw-zero-lapse-kernel
  → VALID_WITHIN → scope:p27-declared-wick-map-and-raw-zero-lapse-control
  → MOTIVATES → open:p28-zero-lapse-uniform-bfv-kernel

claim:P28_DIRICHLET_BFV_GHOST_REMOVES_PROPER_LENGTH_ZERO_MODE
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p28-homogeneous-bfv
  → VALID_WITHIN → scope:p28-bounded-pl-and-homogeneous-bfv
  → MOTIVATES → open:p28-zero-lapse-uniform-bfv-kernel
  → MOTIVATES → open:p28-full-gauge-reduced-superdeterminant
```

The first trace is an unreduced fixed-T Van Vleck statement. The second is a homogeneous Euclidean-continued BFV statement with Dirichlet ghost endpoints. Neither computes the full endpoint-completed gauge-reduced kernel. Likewise, `claim:P28_BOUNDED_VERTICAL_CYCLES_CROSS_RECORDED_DUAL_BRANCH` records bounded constructed geometry only; it points to `open:p28-global-relative-homology-and-intersection` rather than asserting a physical intersection coefficient.

Phase 29 refines, but does not erase, the raw pole trace:

```text
claim:P29_FROZEN_QUADRATIC_KERNEL_HAS_DELTA_FLAT_IDENTITY_LIMIT
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p29-leading-fresnel-kernel
  → VALID_WITHIN → scope:p29-frozen-leading-kernel-and-reduced-bfv-measure
  → MOTIVATES → open:p29-physical-endpoint-measure-and-ordering

claim:P29_EQUAL_ENDPOINT_POINTWISE_ZERO_LAPSE_LIMIT_IS_FINITE
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p29-leading-fresnel-kernel
  → VALID_WITHIN → scope:p29-frozen-leading-kernel-and-reduced-bfv-measure
```

Both traces are true together: the first is weak/distributional convergence under the declared local flat measure, while the second is pointwise behavior. `claim:P29_DISTRIBUTIONAL_IDENTITY_IS_TRACE_CLASS_DENSITY` is separately contradicted, so neither trace supplies a physical WDW density.

Phase 30 separates the local coupled cycle from the still-missing global determinant line:

```text
claim:P30_FINITE_CUTOFF_LOCAL_COUPLED_FIELD_LAPSE_CYCLE_EXISTS
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p30-fibered-schur-cycle
  → VALID_WITHIN → scope:p30-frozen-coupled-cycle-and-relative-determinant
  → MOTIVATES → open:p29-conformal-bfv-uniform-parametrix

claim:P30_TESTED_STANDARD_PRODUCT_ROTATION_IS_SUFFICIENT
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p30-fibered-schur-cycle
  → VALID_WITHIN → scope:p30-frozen-coupled-cycle-and-relative-determinant

claim:P30_BARE_ABSOLUTE_LATTICE_SIGN_IS_CUTOFF_INDEPENDENT
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p30-relative-determinant-and-prefactor
  → VALID_WITHIN → scope:p30-frozen-coupled-cycle-and-relative-determinant
  → MOTIVATES → open:p29-conformal-bfv-uniform-parametrix
```

The supported cycle is finite-cutoff, local, homogeneous, and quadratic. The supported relative magnitude uses the declared midpoint measure. Neither is a full BFV super-Hessian, a regulator-independent determinant-line phase, a global integer PL coefficient, or a physical state.

The [programme guide](../README.md) lists every scope and open problem; the [source inventory](./source-inventory.md) explains what the literature edges do and do not cover.
