# Submission Checklist — 2 paper drafts (2026-05-19)

> Required actions / external dependencies / blockers documented.

---

## Paper 1: Asymmetric Lakatos Verdict — EJPS

| Item | Status | Blocker |
|---|---|---|
| Manuscript draft 0.2 | ✓ done (`asymmetric_lakatos_paper_draft_2026-05-18.md`, revised 2026-05-19) | — |
| Frontmatter (author/funding/data/AI disclosure) | ✓ done | author ORCID pending |
| Cross-references to ICE_WORKBENCH_REFRAME + meta-A3-S3 | ✓ done | — |
| References list (27 entries, 5 categories) | ✓ done | — |
| Cover letter | ✓ done (`COVER_LETTER_EJPS_asymmetric_lakatos.md`) | — |
| Suggested referees (4) | ✓ done | — |
| Word count | ~6,500 (excl. refs) | within EJPS 8k limit |
| LaTeX conversion | ⏳ pending | requires user time / Pandoc + cls download |
| ORCID registration | ❌ user gate | https://orcid.org/register |
| EJPS account (Editorial Manager) | ❌ user gate | https://www.editorialmanager.com/euij |
| **Actual submission** | ❌ user gate | requires ORCID + EJPS account |

## Paper 2: Pre-Registered Lakatos Rigorous Test — Synthese

| Item | Status | Blocker |
|---|---|---|
| Manuscript draft 0.2 | ✓ done (`prereg_lakatos_methodology_paper_draft_2026-05-18.md`, revised 2026-05-19) | — |
| Frontmatter (author/funding/data/AI disclosure) | ✓ done | author ORCID pending |
| Appendix A (28 primitives) | ✓ done | verify 28-row list against `ice_prereg_predictions.py` source |
| Appendix B (20 PDG observables) | ⏳ partial (referenced §3.2; standalone appendix needs PDG 2024 values pasted) | — |
| References list (27 entries, 5 categories) | ✓ done | — |
| Cover letter | ✓ done (`COVER_LETTER_Synthese_prereg_lakatos.md`) | — |
| Suggested referees (4) | ✓ done | — |
| Word count | ~5,800 (excl. refs + appendix) | within Synthese 10k limit |
| LaTeX conversion | ⏳ pending | requires Pandoc + Synthese cls |
| ORCID registration | ❌ user gate | https://orcid.org/register |
| Synthese account (Editorial Manager) | ❌ user gate | https://www.editorialmanager.com/synt |
| **Actual submission** | ❌ user gate | requires ORCID + Synthese account |

---

## Common LaTeX conversion procedure (when user provides credentials)

```bash
# 1. Pandoc convert markdown → LaTeX
pandoc papers/asymmetric_lakatos_paper_draft_2026-05-18.md \
       -o papers/asymmetric_lakatos.tex --citeproc

# 2. Download EJPS template
# https://www.springer.com/journal/13194/submission-guidelines
# → sn-jnl.cls

# 3. Compile
cd papers && pdflatex asymmetric_lakatos.tex && bibtex asymmetric_lakatos && pdflatex asymmetric_lakatos.tex (x2)
```

## arXiv pre-print (optional simultaneous deposit)

| Item | Status | Blocker |
|---|---|---|
| arXiv account | ❌ user gate | https://arxiv.org/user/register |
| First-time endorsement (philsci or physics.gen-ph) | ❌ user gate | need 1 author with prior arXiv submissions in domain |
| arXiv LaTeX format | ⏳ pending | same Pandoc conversion |
| Categories | math.HO (history) + philsci.PS (philosophy of science) | choose primary |

**arXiv endorsement bypass**: if no endorser available, post to PhilSci-Archive (https://philsci-archive.pitt.edu/) instead — no endorsement required, accepted by EJPS/Synthese as pre-print proof.

---

## Order of operations (user actions required)

1. **Register ORCID** (free, 5 min) — https://orcid.org/register
2. **Read both cover letters** + accept author info / make corrections
3. **Choose order**: which paper to submit first?
   - Recommended: submit asymmetric Lakatos to EJPS first (Tüchsen 2024 precedent makes EJPS the natural home)
   - 2-3 weeks later: submit prereg methodology to Synthese (allow time to cite reviewer feedback if any)
   - Simultaneously: arXiv / PhilSci-Archive both papers
4. **Register Editorial Manager accounts** (free, 5 min each) for EJPS + Synthese
5. **Decide PhilSci-Archive vs arXiv** (per endorsement availability)
6. **AI tool use disclosure** — user verdict on exact wording

---

## What can be done autonomously (no user gate)

- Polish drafts further (typo hunt, sentence-level tightening)
- Add additional appendices (e.g., full 15 prediction list with PDG matches)
- LaTeX conversion via Pandoc (if user authorizes pandoc install)
- Bibliography refinement (verify DOIs, add missing entries)
- Cross-reference completeness check
- Final proofread

# KG: submission-checklist-2026-05-19, papers-submission-ready-pending-user-credentials
