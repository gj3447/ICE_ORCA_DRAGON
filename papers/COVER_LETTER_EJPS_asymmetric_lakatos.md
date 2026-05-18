# Cover Letter — European Journal for Philosophy of Science (EJPS)

> Template for submission of `asymmetric_lakatos_paper_draft_2026-05-18.md` to EJPS.
> Submission portal: https://www.editorialmanager.com/euij
> Editor-in-Chief contact (as of 2024): F. A. Muller (Erasmus University Rotterdam), euij@editorialmanager.com

---

Dear Professor Muller and EJPS Editorial Board,

I am pleased to submit the enclosed manuscript, **"Asymmetric Lakatos Verdict via Fiber-Stratified Functor Evaluation"**, for consideration as a research article in *European Journal for Philosophy of Science*.

The paper advances a category-theoretic refinement of Lakatos's (1970) trichotomy of research programmes. Building directly on Tüchsen's recent (2024) introduction of the *Stagnant* third verdict class — published in this very journal — I show that programmes whose protective belts admit a disjoint sub-belt decomposition cannot in general receive a well-defined programme-wide Lakatos verdict. The verdict map must be *fiber-stratified*: each sub-belt receives its own colim-evaluation of the prediction- and confirmation-functors.

The main theoretical result is the **Asymmetric Lakatos Verdict** theorem, which establishes the consistency of a programme being simultaneously Progressive on one sub-fiber and Stagnant on another. The proof is constructive and formally verified in Lean 4 (companion sister project `MIND/lean_formalization/lakatos_stagnant/`, currently with `stagnant_implies_not_degenerating` sorry-free as of 2026-05-18).

The paper closes with the *first empirically pre-registered fiber-stratified Lakatos verdict* in the literature, applying the methodology to the hypercomplex physics programme ICE_ORCA_DRAGON. The empirical witness is documented under a sha256-cryptographic commit (hash `0bbcbe40272c3811f68e05b391c7746016cf54ca7fc2f28f39f03d0fb98900c2`) of 15 pre-registered predictions tested against 20 frozen PDG observables under MC null model and Bonferroni look-elsewhere correction — yielding 0/15 SIGNAL_GENUINE for the physics-prediction sub-fiber while leaving the algebra sub-fiber Progressive (Brown 1967, Moreno 1998, Reggiani 2024 + sedenion uniqueness theorem 2026-05-19).

I believe the paper is suitable for EJPS because:
1. It builds directly on a recent EJPS publication (Tüchsen 2024);
2. It combines formal philosophy (category theory) with empirical philosophy of physics (hypercomplex algebra programmes); and
3. The cryptographic-commit methodology generalizes to programmes well beyond the case study — string theory landscape, cosmology inflation/structure-formation fibers, and other algebra-based physics programmes (Furey, Gillard-Gresnigt, Lisi, Connes-Marcolli).

The manuscript is approximately 6,500 words (excluding references), with 27 references spanning the Lakatos-Tüchsen lineage, hypercomplex algebra literature, category theory, and pre-registration methodology. All data, code, sha256 commit log, and Lean 4 formalization source are openly available; the paper is fully reproducible from the SYMPOSIUM project repository.

This is an original submission, not under consideration elsewhere. No competing interests to declare. No funding to disclose.

Thank you for considering this work. I look forward to the editorial board's response.

Sincerely,

라경준 (Lagyeongjun Ra)
Independent researcher, SYMPOSIUM Project
⟨gj3447@gmail.com⟩
ORCID: 0009-0003-5827-6288 (https://orcid.org/0009-0003-5827-6288)

---

# Suggested referees (positive expertise)

1. **Robert Tüchsen** — University of Bonn — author of the foundational *Stagnant* category paper (arXiv:2404.18307); natural critic.
2. **Deborah G. Mayo** — Virginia Tech — pre-registration and severe-testing methodology.
3. **John Worrall** — LSE — structural realism + Lakatos lineage scholarship.
4. **Niels G. Gresnigt** — Xi'an Jiaotong-Liverpool University — sedenion/Cl(8) physics programme (Gresnigt 2024 EPJC 84:1129); independent expert on the case study algebra.

# Suggested referees to avoid (potential bias)

- None declared.
